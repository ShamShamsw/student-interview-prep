"""Business logic for Project 42: Hand-Pose Sign Language Classifier."""

from __future__ import annotations

import math
import random
import statistics
import time
from collections import Counter, defaultdict
from datetime import datetime
from typing import Any, Dict, List, Tuple

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

from models import (
    create_capture_record,
    create_classifier_config,
    create_prediction_record,
    create_session_summary,
    create_sign_template_record,
)
from storage import (
    OUTPUTS_DIR,
    ensure_data_dirs,
    load_dataset_catalog,
    load_run_catalog,
    load_template_library,
    save_dataset_catalog,
    save_live_inference_file,
    save_model_file,
    save_run_record,
    save_template_library,
)

SIGN_DESCRIPTIONS = {
    'A': 'closed fist with thumb beside the index finger',
    'B': 'flat hand with four extended fingers and tucked thumb',
    'C': 'curved open hand forming the outline of the letter C',
    'L': 'index finger and thumb extended at a right angle',
    'Y': 'thumb and pinky extended with middle fingers folded',
}


def _session_id() -> str:
    """Build a compact session ID from UTC timestamp."""
    return datetime.utcnow().strftime('%Y%m%d_%H%M%S')


def _distance(point_a: List[float], point_b: List[float]) -> float:
    """Return Euclidean distance between two 3D points."""
    return math.sqrt(sum((point_a[index] - point_b[index]) ** 2 for index in range(3)))


def _build_finger(base_x: float, openness: float, lean: float, z_shift: float) -> List[List[float]]:
    """Create four synthetic landmarks for a single finger."""
    points: List[List[float]] = []
    for index in range(4):
        stage = index + 1
        ratio = stage / 4.0
        y = 0.18 + ratio * (0.18 + 0.56 * openness)
        x = base_x + lean * ratio * (0.12 + 0.20 * (1.0 - openness))
        z = z_shift + ratio * 0.06 * (1.0 - openness)
        points.append([x, y, z])
    return points


def _build_thumb(openness: float, lift: float, spread: float) -> List[List[float]]:
    """Create four synthetic landmarks for the thumb."""
    base_x = -0.10 - 0.08 * spread
    tip_x = -0.16 - 0.32 * openness - 0.06 * spread
    return [
        [base_x, 0.10 + 0.03 * lift, 0.01],
        [base_x - 0.06 - 0.08 * openness, 0.16 + 0.05 * lift, 0.005],
        [base_x - 0.10 - 0.16 * openness, 0.22 + 0.08 * lift, -0.005],
        [tip_x, 0.28 + 0.12 * lift, -0.01 - 0.01 * openness],
    ]


def _make_landmarks(
    thumb_open: float,
    index_open: float,
    middle_open: float,
    ring_open: float,
    pinky_open: float,
    curvature: float = 0.0,
) -> List[List[float]]:
    """Build one normalized synthetic hand landmark set."""
    landmarks = [[0.0, 0.0, 0.0]]
    landmarks.extend(_build_thumb(thumb_open, lift=0.35 + 0.25 * thumb_open, spread=thumb_open))
    landmarks.extend(_build_finger(-0.20, index_open, lean=-0.05 - curvature, z_shift=0.02 * curvature))
    landmarks.extend(_build_finger(-0.04, middle_open, lean=-0.02 * curvature, z_shift=0.03 * curvature))
    landmarks.extend(_build_finger(0.10, ring_open, lean=0.04 + 0.5 * curvature, z_shift=0.04 * curvature))
    landmarks.extend(_build_finger(0.24, pinky_open, lean=0.07 + curvature, z_shift=0.05 * curvature))
    return landmarks


def _default_template_library() -> List[Dict[str, Any]]:
    """Return deterministic starter templates used on first run."""
    templates = {
        'A': _make_landmarks(thumb_open=0.60, index_open=0.08, middle_open=0.07, ring_open=0.06, pinky_open=0.07),
        'B': _make_landmarks(thumb_open=0.18, index_open=1.00, middle_open=1.00, ring_open=0.96, pinky_open=0.92),
        'C': _make_landmarks(thumb_open=0.78, index_open=0.56, middle_open=0.60, ring_open=0.57, pinky_open=0.50, curvature=0.22),
        'L': _make_landmarks(thumb_open=1.00, index_open=1.00, middle_open=0.05, ring_open=0.05, pinky_open=0.05),
        'Y': _make_landmarks(thumb_open=0.98, index_open=0.06, middle_open=0.05, ring_open=0.04, pinky_open=0.94),
    }
    library = []
    for index, label in enumerate(['A', 'B', 'C', 'L', 'Y'], start=1):
        library.append(
            create_sign_template_record(
                sign_id=f'sign_{index:03d}',
                label=label,
                description=SIGN_DESCRIPTIONS[label],
                landmarks=templates[label],
            )
        )
    return library


def _normalize_landmarks(landmarks: List[List[float]]) -> List[List[float]]:
    """Center landmarks on the wrist and normalize by max radius."""
    if not landmarks:
        return []
    wrist = landmarks[0]
    centered = [[point[0] - wrist[0], point[1] - wrist[1], point[2] - wrist[2]] for point in landmarks]
    scale = max((_distance([0.0, 0.0, 0.0], point) for point in centered[1:]), default=1.0)
    scale = scale if scale > 1e-6 else 1.0
    return [[point[0] / scale, point[1] / scale, point[2] / scale] for point in centered]


def _extract_feature_vector(landmarks: List[List[float]]) -> List[float]:
    """Extract a compact geometric feature vector from one hand pose."""
    normalized = _normalize_landmarks(landmarks)
    if not normalized:
        return []

    features: List[float] = []
    for point in normalized:
        features.extend(point)

    wrist = normalized[0]
    fingertip_ids = [4, 8, 12, 16, 20]
    finger_base_ids = [1, 5, 9, 13, 17]

    for tip_id in fingertip_ids:
        features.append(_distance(normalized[tip_id], wrist))
    for base_id, tip_id in zip(finger_base_ids, fingertip_ids):
        features.append(_distance(normalized[tip_id], normalized[base_id]))
    for left_id, right_id in zip(fingertip_ids, fingertip_ids[1:]):
        features.append(_distance(normalized[left_id], normalized[right_id]))

    return [round(value, 5) for value in features]


def _jitter_landmarks(
    landmarks: List[List[float]],
    jitter_std: float,
    rng: random.Random,
    challenge_multiplier: float = 1.0,
) -> List[List[float]]:
    """Add deterministic noise, scale, and slight rotation to a template."""
    angle = rng.gauss(0.0, jitter_std * 1.6 * challenge_multiplier)
    scale = 1.0 + rng.gauss(0.0, jitter_std * 0.7 * challenge_multiplier)
    shift_x = rng.gauss(0.0, jitter_std * 0.5 * challenge_multiplier)
    shift_y = rng.gauss(0.0, jitter_std * 0.4 * challenge_multiplier)
    shift_z = rng.gauss(0.0, jitter_std * 0.3 * challenge_multiplier)
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)

    jittered: List[List[float]] = []
    for x_coord, y_coord, z_coord in landmarks:
        rotated_x = x_coord * cos_angle - y_coord * sin_angle
        rotated_y = x_coord * sin_angle + y_coord * cos_angle
        jittered.append(
            [
                rotated_x * scale + shift_x + rng.gauss(0.0, jitter_std * 0.5 * challenge_multiplier),
                rotated_y * scale + shift_y + rng.gauss(0.0, jitter_std * 0.5 * challenge_multiplier),
                z_coord * scale + shift_z + rng.gauss(0.0, jitter_std * 0.35 * challenge_multiplier),
            ]
        )
    return [[round(value, 4) for value in point] for point in jittered]


def _capture_dataset(
    templates: List[Dict[str, Any]],
    config: Dict[str, Any],
    session_id: str,
    rng: random.Random,
) -> List[Dict[str, Any]]:
    """Simulate dataset capture mode by augmenting seeded hand templates."""
    samples_by_sign: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    sample_counter = 0

    for template in templates:
        label = template['label']
        for _ in range(config['capture_samples_per_sign']):
            sample_counter += 1
            jittered_landmarks = _jitter_landmarks(
                template['landmarks'],
                config['capture_jitter_std'],
                rng,
            )
            samples_by_sign[label].append(
                create_capture_record(
                    sample_id=f'sample_{session_id}_{sample_counter:03d}',
                    session_id=session_id,
                    sign_label=label,
                    split='pending',
                    landmarks=jittered_landmarks,
                    features=_extract_feature_vector(jittered_landmarks),
                    source='synthetic_capture',
                )
            )

    all_samples: List[Dict[str, Any]] = []
    for label, samples in samples_by_sign.items():
        rng.shuffle(samples)
        train_count = max(1, int(len(samples) * config['train_split']))
        if train_count >= len(samples):
            train_count = len(samples) - 1
        for index, sample in enumerate(samples):
            sample['split'] = 'train' if index < train_count else 'test'
            all_samples.append(sample)

    return all_samples


def _average_feature_vectors(vectors: List[List[float]]) -> List[float]:
    """Compute the elementwise mean of equally sized feature vectors."""
    if not vectors:
        return []
    length = len(vectors[0])
    return [round(sum(vector[index] for vector in vectors) / len(vectors), 5) for index in range(length)]


def _train_classifier(train_samples: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Train a nearest-centroid classifier from captured features."""
    grouped: Dict[str, List[List[float]]] = defaultdict(list)
    for sample in train_samples:
        grouped[sample['sign_label']].append(sample['features'])

    centroids = {
        label: _average_feature_vectors(vectors)
        for label, vectors in grouped.items()
    }

    feature_dimension = len(next(iter(centroids.values()), []))
    return {
        'classifier_type': 'nearest_centroid',
        'feature_dimension': feature_dimension,
        'labels': sorted(centroids),
        'centroids': centroids,
        'train_counts': {label: len(vectors) for label, vectors in grouped.items()},
    }


def _vector_distance(vector_a: List[float], vector_b: List[float]) -> float:
    """Return Euclidean distance between two feature vectors."""
    return math.sqrt(sum((vector_a[index] - vector_b[index]) ** 2 for index in range(len(vector_a))))


def _predict_features(features: List[float], model: Dict[str, Any]) -> Tuple[str, float, List[Dict[str, Any]]]:
    """Predict one sign label from a feature vector."""
    distances = []
    for label in model['labels']:
        centroid = model['centroids'][label]
        distance = _vector_distance(features, centroid)
        distances.append((label, distance))

    distances.sort(key=lambda item: item[1])
    inverse_scores = [1.0 / (item[1] + 1e-6) for item in distances]
    total_inverse = sum(inverse_scores) or 1.0
    ranked = [
        {'label': label, 'score': score / total_inverse}
        for (label, _distance_value), score in zip(distances, inverse_scores)
    ]
    best = ranked[0]
    return best['label'], best['score'], ranked[:3]


def _evaluate_classifier(
    test_samples: List[Dict[str, Any]],
    model: Dict[str, Any],
    config: Dict[str, Any],
) -> Dict[str, Any]:
    """Evaluate the classifier on the held-out test split."""
    labels = config['signs']
    confusion = {expected: {predicted: 0 for predicted in labels} for expected in labels}
    predictions: List[Dict[str, Any]] = []
    correct = 0

    for index, sample in enumerate(test_samples, start=1):
        predicted_label, confidence, top_candidates = _predict_features(sample['features'], model)
        is_correct = predicted_label == sample['sign_label']
        correct += 1 if is_correct else 0
        confusion[sample['sign_label']][predicted_label] += 1
        predictions.append(
            create_prediction_record(
                frame_id=f'test_{index:03d}',
                expected_label=sample['sign_label'],
                predicted_label=predicted_label,
                confidence=confidence,
                is_low_confidence=confidence < config['low_confidence_threshold'],
                top_candidates=top_candidates,
            )
        )

    accuracy = correct / len(test_samples) if test_samples else 0.0
    per_sign_accuracy = {}
    for label in labels:
        total = sum(confusion[label].values())
        per_sign_accuracy[label] = confusion[label][label] / total if total else 0.0

    return {
        'accuracy': accuracy,
        'per_sign_accuracy': per_sign_accuracy,
        'confusion': confusion,
        'predictions': predictions,
    }


def _scripted_live_sequence(signs: List[str], live_frames: int) -> List[str]:
    """Build a repeatable live demo sequence from the supported vocabulary."""
    seed_sequence = ['A', 'B', 'C', 'L', 'Y', 'L', 'C', 'B', 'A', 'Y']
    sequence = []
    while len(sequence) < live_frames:
        sequence.extend(sign for sign in seed_sequence if sign in signs)
    return sequence[:live_frames]


def _run_live_inference(
    templates: List[Dict[str, Any]],
    model: Dict[str, Any],
    config: Dict[str, Any],
    rng: random.Random,
) -> List[Dict[str, Any]]:
    """Simulate live inference on a scripted stream of synthetic frames."""
    template_map = {template['label']: template for template in templates}
    predictions: List[Dict[str, Any]] = []
    expected_sequence = _scripted_live_sequence(config['signs'], config['live_frames'])

    for index, expected_label in enumerate(expected_sequence, start=1):
        challenge_multiplier = 1.0 + (0.7 if index % 4 == 0 else 0.0)
        landmarks = _jitter_landmarks(
            template_map[expected_label]['landmarks'],
            config['live_jitter_std'],
            rng,
            challenge_multiplier=challenge_multiplier,
        )
        features = _extract_feature_vector(landmarks)
        predicted_label, confidence, top_candidates = _predict_features(features, model)
        predictions.append(
            create_prediction_record(
                frame_id=f'live_{index:03d}',
                expected_label=expected_label,
                predicted_label=predicted_label,
                confidence=confidence,
                is_low_confidence=confidence < config['low_confidence_threshold'],
                top_candidates=top_candidates,
            )
        )

    return predictions


def _save_confusion_matrix_plot(
    evaluation: Dict[str, Any],
    session_id: str,
    labels: List[str],
) -> str:
    """Persist a confusion matrix heatmap for held-out evaluation."""
    matrix = [[evaluation['confusion'][expected][predicted] for predicted in labels] for expected in labels]
    figure, axis = plt.subplots(figsize=(6, 5))
    image = axis.imshow(matrix, cmap='YlGnBu')
    axis.set_xticks(range(len(labels)), labels)
    axis.set_yticks(range(len(labels)), labels)
    axis.set_xlabel('Predicted sign')
    axis.set_ylabel('Expected sign')
    axis.set_title('Held-Out Sign Classification Confusion Matrix')

    for row_index, row in enumerate(matrix):
        for column_index, value in enumerate(row):
            axis.text(column_index, row_index, str(value), ha='center', va='center', color='#102a43')

    figure.colorbar(image, ax=axis, fraction=0.046, pad=0.04)
    figure.tight_layout()
    file_path = OUTPUTS_DIR / f'confusion_matrix_{session_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def _save_confidence_timeline(predictions: List[Dict[str, Any]], session_id: str, threshold: float) -> str:
    """Persist a confidence timeline for the scripted live demo."""
    frames = list(range(1, len(predictions) + 1))
    confidences = [prediction['confidence'] for prediction in predictions]
    colors = ['#d62828' if prediction['is_low_confidence'] else '#2a9d8f' for prediction in predictions]

    figure, axis = plt.subplots(figsize=(10, 4))
    axis.plot(frames, confidences, color='#1d3557', linewidth=1.5, alpha=0.85)
    axis.scatter(frames, confidences, c=colors, s=45, zorder=3)
    axis.axhline(threshold, color='#d62828', linestyle='--', linewidth=1.0, label='low-confidence threshold')
    axis.set_xlabel('Live frame')
    axis.set_ylabel('Confidence')
    axis.set_ylim(0.0, 1.02)
    axis.set_title('Live Inference Confidence Timeline')
    axis.grid(alpha=0.25)
    axis.legend(loc='lower right', fontsize=8)
    figure.tight_layout()
    file_path = OUTPUTS_DIR / f'confidence_timeline_{session_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def load_classifier_profile() -> Dict[str, Any]:
    """Return startup profile built from previously saved catalogs."""
    run_catalog = load_run_catalog()
    dataset_catalog = load_dataset_catalog()
    library = load_template_library()
    recent_samples = [
        f"{item.get('sample_id', '')}:{item.get('sign_label', '')}:{item.get('split', '')}"
        for item in dataset_catalog[-6:]
    ]
    return {
        'catalog_file': 'data/runs.json',
        'dataset_file': 'data/dataset.json',
        'library_file': 'data/sign_templates.json',
        'runs_stored': len(run_catalog),
        'samples_stored': len(dataset_catalog),
        'templates_available': len(library),
        'recent_samples': recent_samples,
    }


def run_core_flow() -> Dict[str, Any]:
    """Run one complete capture, training, evaluation, and live inference session."""
    ensure_data_dirs()
    config = create_classifier_config()
    session_id = _session_id()
    rng = random.Random(config['random_seed'])
    started = time.perf_counter()

    template_library = load_template_library()
    if not template_library:
        template_library = _default_template_library()
        save_template_library(template_library)

    captures = _capture_dataset(template_library, config, session_id, rng)
    train_samples = [sample for sample in captures if sample['split'] == 'train']
    test_samples = [sample for sample in captures if sample['split'] == 'test']

    model = _train_classifier(train_samples)
    evaluation = _evaluate_classifier(test_samples, model, config)
    live_predictions = _run_live_inference(template_library, model, config, rng)

    confusion_matrix_file = ''
    confidence_timeline_file = ''
    if config['include_confusion_matrix']:
        confusion_matrix_file = _save_confusion_matrix_plot(evaluation, session_id, config['signs'])
    if config['include_confidence_timeline']:
        confidence_timeline_file = _save_confidence_timeline(
            live_predictions,
            session_id,
            config['low_confidence_threshold'],
        )

    model_payload = {
        'session_id': session_id,
        'config': config,
        'model': model,
        'evaluation': {
            'accuracy': round(evaluation['accuracy'], 4),
            'per_sign_accuracy': evaluation['per_sign_accuracy'],
            'confusion': evaluation['confusion'],
        },
    }
    model_file = save_model_file(model_payload, session_id)
    live_file = save_live_inference_file(live_predictions, session_id)

    dataset_catalog = load_dataset_catalog()
    dataset_catalog.extend(captures)
    save_dataset_catalog(dataset_catalog)

    elapsed_ms = (time.perf_counter() - started) * 1000.0
    live_correct = sum(
        1 for prediction in live_predictions if prediction['expected_label'] == prediction['predicted_label']
    )
    low_confidence_frames = sum(1 for prediction in live_predictions if prediction['is_low_confidence'])
    per_sign_accuracy_values = list(evaluation['per_sign_accuracy'].values())
    macro_accuracy = (
        statistics.mean(per_sign_accuracy_values)
        if per_sign_accuracy_values
        else 0.0
    )
    average_live_confidence = (
        statistics.mean(prediction['confidence'] for prediction in live_predictions)
        if live_predictions
        else 0.0
    )
    predicted_distribution = Counter(prediction['predicted_label'] for prediction in live_predictions)

    metrics: Dict[str, Any] = {
        'macro_accuracy': round(macro_accuracy, 4),
        'avg_live_confidence': round(average_live_confidence, 4),
        'feature_dimension': model['feature_dimension'],
        'classifier_type': model['classifier_type'],
        'live_demo_accuracy': round(live_correct / len(live_predictions), 4) if live_predictions else 0.0,
        'low_confidence_rate': round(low_confidence_frames / len(live_predictions), 4) if live_predictions else 0.0,
        'predicted_distribution': dict(predicted_distribution),
    }

    prediction_previews = live_predictions[: config['max_predictions_in_report']]
    artifacts = {
        'model_file': model_file,
        'live_file': live_file,
        'confusion_matrix_file': confusion_matrix_file,
        'confidence_timeline_file': confidence_timeline_file,
        'capture_count': len(captures),
    }

    summary = create_session_summary(
        session_id=session_id,
        signs_modeled=len(template_library),
        captures_total=len(captures),
        training_samples=len(train_samples),
        test_samples=len(test_samples),
        test_accuracy=evaluation['accuracy'],
        live_frames=len(live_predictions),
        low_confidence_frames=low_confidence_frames,
        elapsed_ms=elapsed_ms,
        artifacts=artifacts,
        prediction_previews=prediction_previews,
        metrics=metrics,
    )

    run_record = dict(summary)
    session_file = save_run_record(run_record)
    summary['artifacts']['session_file'] = session_file
    return summary
