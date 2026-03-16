"""
models.py - Data constructors for audio classification session artifacts
=======================================================================
"""

from datetime import datetime


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp.

    Returns:
        str: Timestamp string with trailing Z.
    """
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def create_project_config(
    sample_rate: int = 22050,
    clip_duration_seconds: float = 2.0,
    samples_per_label: int = 24,
    n_mfcc: int = 13,
    n_fft: int = 2048,
    hop_length: int = 512,
    test_size: float = 0.25,
    random_state: int = 42,
) -> dict:
    """Create the default runtime configuration.

    Parameters:
        sample_rate (int): Audio sampling rate used for synthesis and analysis.
        clip_duration_seconds (float): Length of each generated clip.
        samples_per_label (int): Number of clips generated for each class.
        n_mfcc (int): Number of MFCC coefficients to extract.
        n_fft (int): FFT window size used by spectral features.
        hop_length (int): Hop length used by frame-based feature extraction.
        test_size (float): Fraction of rows reserved for testing.
        random_state (int): Seed for reproducible dataset generation and model splitting.

    Returns:
        dict: Configuration payload.
    """
    return {
        "sample_rate": int(sample_rate),
        "clip_duration_seconds": float(clip_duration_seconds),
        "samples_per_label": int(samples_per_label),
        "n_mfcc": int(n_mfcc),
        "n_fft": int(n_fft),
        "hop_length": int(hop_length),
        "test_size": float(test_size),
        "random_state": int(random_state),
        "created_at": _utc_timestamp(),
    }


def create_audio_label_spec(
    key: str,
    label: str,
    description: str,
    base_frequency_hz: float,
) -> dict:
    """Create one class descriptor used for synthetic audio generation.

    Parameters:
        key (str): Internal identifier for the class.
        label (str): Human-readable class label.
        description (str): Short explanation of the class sound profile.
        base_frequency_hz (float): Baseline tone frequency for synthesis.

    Returns:
        dict: Label descriptor payload.
    """
    return {
        "key": key,
        "label": label,
        "description": description,
        "base_frequency_hz": float(base_frequency_hz),
    }


def create_feature_record(
    sample_id: str,
    label: str,
    mfcc_means: list[float],
    chroma_means: list[float],
    zero_crossing_rate: float,
    spectral_centroid: float,
    rms_energy: float,
) -> dict:
    """Create extracted-feature metadata for one audio clip.

    Parameters:
        sample_id (str): Unique sample identifier.
        label (str): Ground-truth class label.
        mfcc_means (list[float]): Mean MFCC values across frames.
        chroma_means (list[float]): Mean chroma values across frames.
        zero_crossing_rate (float): Mean zero-crossing rate.
        spectral_centroid (float): Mean spectral centroid.
        rms_energy (float): Mean RMS energy.

    Returns:
        dict: Feature record payload.
    """
    return {
        "sample_id": sample_id,
        "label": label,
        "mfcc_means": [round(float(value), 6) for value in mfcc_means],
        "chroma_means": [round(float(value), 6) for value in chroma_means],
        "zero_crossing_rate": round(float(zero_crossing_rate), 6),
        "spectral_centroid": round(float(spectral_centroid), 6),
        "rms_energy": round(float(rms_energy), 6),
    }


def create_training_summary(
    config: dict,
    labels: list[str],
    total_samples: int,
    train_samples: int,
    test_samples: int,
    feature_vector_size: int,
    accuracy: float,
    confusion_matrix: list[list[int]],
    classification_report: dict,
    recent_features: list[dict],
    status: str,
) -> dict:
    """Create the persistable summary for one training session.

    Parameters:
        config (dict): Runtime configuration.
        labels (list[str]): Sorted list of label names in the session.
        total_samples (int): Total generated clips.
        train_samples (int): Samples used for training.
        test_samples (int): Samples used for evaluation.
        feature_vector_size (int): Number of numeric values per feature row.
        accuracy (float): Model accuracy on the held-out split.
        confusion_matrix (list[list[int]]): Confusion matrix rows.
        classification_report (dict): Per-class precision/recall/f1 values.
        recent_features (list[dict]): Tail of extracted-feature records.
        status (str): Session outcome indicator.

    Returns:
        dict: Session summary payload.
    """
    return {
        "config": config,
        "labels": list(labels),
        "total_samples": int(total_samples),
        "train_samples": int(train_samples),
        "test_samples": int(test_samples),
        "feature_vector_size": int(feature_vector_size),
        "accuracy": round(float(accuracy), 4),
        "confusion_matrix": confusion_matrix,
        "classification_report": classification_report,
        "recent_features": list(recent_features),
        "status": status,
        "saved_at": _utc_timestamp(),
    }
