"""
operations.py - Core audio classification workflow
==================================================

Implements:
    - synthetic dataset generation for multiple audio classes
    - MFCC/chroma feature extraction plus core spectral statistics
    - train/test split with a RandomForest classifier
    - confusion-matrix/report generation and run artifact persistence
"""

from __future__ import annotations

from models import (
    create_audio_label_spec,
    create_feature_record,
    create_project_config,
    create_training_summary,
)
from storage import save_latest_run


def _load_dependencies():
    """Lazily import scientific dependencies with a clear error message.

    Returns:
        tuple: Imported modules used by this workflow.
    """
    try:
        import librosa
        import numpy as np
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
        from sklearn.model_selection import train_test_split

        return {
            "librosa": librosa,
            "np": np,
            "RandomForestClassifier": RandomForestClassifier,
            "accuracy_score": accuracy_score,
            "classification_report": classification_report,
            "confusion_matrix": confusion_matrix,
            "train_test_split": train_test_split,
        }
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependencies: install requirements.txt for this project before running audio classification."
        ) from exc


def load_audio_label_specs() -> list[dict]:
    """Return supported synthetic audio class definitions.

    Returns:
        list[dict]: Class descriptors used to generate labeled samples.
    """
    return [
        create_audio_label_spec(
            key="low_tone",
            label="low_tone",
            description="low-frequency harmonic tone with mild broadband noise",
            base_frequency_hz=160.0,
        ),
        create_audio_label_spec(
            key="mid_tone",
            label="mid_tone",
            description="mid-frequency steady tone plus a weak overtone",
            base_frequency_hz=440.0,
        ),
        create_audio_label_spec(
            key="high_tone",
            label="high_tone",
            description="high-frequency tone profile with sharper spectral centroid",
            base_frequency_hz=880.0,
        ),
    ]


def _generate_waveform(spec: dict, sample_index: int, config: dict, np):
    """Generate a synthetic waveform for one class sample.

    Parameters:
        spec (dict): Label specification with base frequency.
        sample_index (int): Index used to create deterministic variation.
        config (dict): Runtime configuration.
        np: Imported numpy module.

    Returns:
        np.ndarray: One-dimensional audio waveform in range approximately [-1, 1].
    """
    sample_rate = config["sample_rate"]
    duration = config["clip_duration_seconds"]
    total_samples = int(sample_rate * duration)
    timeline = np.linspace(0.0, duration, total_samples, endpoint=False)
    rng = np.random.default_rng(seed=config["random_state"] + sample_index * 13)

    base_frequency = spec["base_frequency_hz"]
    frequency_jitter = rng.uniform(-8.0, 8.0)
    primary = np.sin(2.0 * np.pi * (base_frequency + frequency_jitter) * timeline)
    overtone = 0.35 * np.sin(2.0 * np.pi * (base_frequency * 2.0) * timeline)

    # Envelope and low-level noise produce realistic variation while preserving class identity.
    attack = np.linspace(0.35, 1.0, max(1, int(0.15 * total_samples)))
    sustain = np.ones(total_samples - attack.size)
    envelope = np.concatenate([attack, sustain])
    noise_level = 0.02 + (sample_index % 5) * 0.003
    noise = rng.normal(0.0, noise_level, size=total_samples)

    waveform = (0.65 * primary + overtone + noise) * envelope
    waveform /= np.max(np.abs(waveform)) + 1e-8
    return waveform.astype(np.float32)


def _extract_features(sample_id: str, label: str, waveform, config: dict, deps: dict):
    """Extract an engineered feature vector and metadata for one waveform.

    Parameters:
        sample_id (str): Unique sample identifier.
        label (str): Ground-truth class label.
        waveform: One-dimensional audio signal.
        config (dict): Runtime configuration.
        deps (dict): Imported dependency bundle.

    Returns:
        tuple: Numeric feature vector and structured feature record.
    """
    librosa = deps["librosa"]
    np = deps["np"]
    sample_rate = config["sample_rate"]
    n_fft = config["n_fft"]
    hop_length = config["hop_length"]

    mfcc = librosa.feature.mfcc(
        y=waveform,
        sr=sample_rate,
        n_mfcc=config["n_mfcc"],
        n_fft=n_fft,
        hop_length=hop_length,
    )
    chroma = librosa.feature.chroma_stft(
        y=waveform,
        sr=sample_rate,
        n_fft=n_fft,
        hop_length=hop_length,
    )
    zero_crossing_rate = librosa.feature.zero_crossing_rate(
        y=waveform,
        hop_length=hop_length,
    )
    spectral_centroid = librosa.feature.spectral_centroid(
        y=waveform,
        sr=sample_rate,
        n_fft=n_fft,
        hop_length=hop_length,
    )
    rms = librosa.feature.rms(y=waveform, frame_length=n_fft, hop_length=hop_length)

    mfcc_means = mfcc.mean(axis=1)
    chroma_means = chroma.mean(axis=1)
    zcr_mean = float(zero_crossing_rate.mean())
    centroid_mean = float(spectral_centroid.mean())
    rms_mean = float(rms.mean())

    feature_vector = np.concatenate(
        [mfcc_means, chroma_means, np.array([zcr_mean, centroid_mean, rms_mean])]
    )

    feature_record = create_feature_record(
        sample_id=sample_id,
        label=label,
        mfcc_means=mfcc_means.tolist(),
        chroma_means=chroma_means.tolist(),
        zero_crossing_rate=zcr_mean,
        spectral_centroid=centroid_mean,
        rms_energy=rms_mean,
    )
    return feature_vector, feature_record


def run_core_flow(config: dict | None = None, label_specs: list[dict] | None = None) -> dict:
    """Execute audio feature extraction and model training.

    Parameters:
        config (dict | None): Optional runtime configuration override.
        label_specs (list[dict] | None): Optional class specification override.

    Returns:
        dict: Persisted training summary.
    """
    deps = _load_dependencies()
    np = deps["np"]
    runtime_config = config or create_project_config()
    labels_config = label_specs or load_audio_label_specs()

    features = []
    labels = []
    feature_records = []
    sample_counter = 0

    for spec in labels_config:
        for local_index in range(runtime_config["samples_per_label"]):
            sample_counter += 1
            sample_id = f"{spec['key']}_{local_index:03d}"
            waveform = _generate_waveform(
                spec=spec,
                sample_index=sample_counter,
                config=runtime_config,
                np=np,
            )
            feature_vector, feature_record = _extract_features(
                sample_id=sample_id,
                label=spec["label"],
                waveform=waveform,
                config=runtime_config,
                deps=deps,
            )
            features.append(feature_vector)
            labels.append(spec["label"])
            feature_records.append(feature_record)

    feature_matrix = np.vstack(features)
    class_labels = sorted(set(labels))

    train_test_split = deps["train_test_split"]
    x_train, x_test, y_train, y_test = train_test_split(
        feature_matrix,
        labels,
        test_size=runtime_config["test_size"],
        random_state=runtime_config["random_state"],
        stratify=labels,
    )

    RandomForestClassifier = deps["RandomForestClassifier"]
    classifier = RandomForestClassifier(
        n_estimators=180,
        random_state=runtime_config["random_state"],
        max_depth=14,
    )
    classifier.fit(x_train, y_train)
    predictions = classifier.predict(x_test)

    accuracy_score = deps["accuracy_score"]
    classification_report = deps["classification_report"]
    confusion_matrix = deps["confusion_matrix"]

    accuracy = float(accuracy_score(y_test, predictions))
    report_dict = classification_report(
        y_test,
        predictions,
        labels=class_labels,
        output_dict=True,
        zero_division=0,
    )
    matrix = confusion_matrix(y_test, predictions, labels=class_labels).tolist()

    summary = create_training_summary(
        config=runtime_config,
        labels=class_labels,
        total_samples=feature_matrix.shape[0],
        train_samples=x_train.shape[0],
        test_samples=x_test.shape[0],
        feature_vector_size=feature_matrix.shape[1],
        accuracy=accuracy,
        confusion_matrix=matrix,
        classification_report=report_dict,
        recent_features=feature_records[-6:],
        status="completed",
    )
    save_latest_run(summary)
    return summary
