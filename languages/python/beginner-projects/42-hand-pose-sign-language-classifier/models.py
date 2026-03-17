"""Data models for Project 42: Hand-Pose Sign Language Classifier."""

from datetime import datetime
from typing import Any, Dict, List


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string."""
    return datetime.utcnow().isoformat(timespec='seconds') + 'Z'


def _round_landmarks(landmarks: List[List[float]]) -> List[List[float]]:
    """Round nested landmark coordinates for stable persistence."""
    return [[round(float(value), 4) for value in point] for point in landmarks]


def _round_features(features: List[float]) -> List[float]:
    """Round feature vectors to keep exported JSON compact."""
    return [round(float(value), 5) for value in features]


def create_classifier_config(
    signs: List[str] | None = None,
    landmarks_per_hand: int = 21,
    capture_samples_per_sign: int = 24,
    train_split: float = 0.75,
    live_frames: int = 12,
    capture_jitter_std: float = 0.028,
    live_jitter_std: float = 0.018,
    low_confidence_threshold: float = 0.58,
    include_confusion_matrix: bool = True,
    include_confidence_timeline: bool = True,
    max_predictions_in_report: int = 8,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """Create a validated configuration record for one classifier session."""
    resolved_signs = signs if signs else ['A', 'B', 'C', 'L', 'Y']
    return {
        'project_type': 'hand_pose_sign_classifier',
        'signs': list(resolved_signs),
        'landmarks_per_hand': max(5, int(landmarks_per_hand)),
        'capture_samples_per_sign': max(6, int(capture_samples_per_sign)),
        'train_split': min(0.9, max(0.5, float(train_split))),
        'live_frames': max(4, int(live_frames)),
        'capture_jitter_std': max(0.001, float(capture_jitter_std)),
        'live_jitter_std': max(0.001, float(live_jitter_std)),
        'low_confidence_threshold': min(0.95, max(0.2, float(low_confidence_threshold))),
        'include_confusion_matrix': bool(include_confusion_matrix),
        'include_confidence_timeline': bool(include_confidence_timeline),
        'max_predictions_in_report': max(3, int(max_predictions_in_report)),
        'random_seed': int(random_seed),
        'created_at': _utc_timestamp(),
    }


def create_sign_template_record(
    sign_id: str,
    label: str,
    description: str,
    landmarks: List[List[float]],
) -> Dict[str, Any]:
    """Create one sign template record."""
    return {
        'sign_id': str(sign_id),
        'label': str(label),
        'description': str(description),
        'landmarks': _round_landmarks(landmarks),
    }


def create_capture_record(
    sample_id: str,
    session_id: str,
    sign_label: str,
    split: str,
    landmarks: List[List[float]],
    features: List[float],
    source: str,
) -> Dict[str, Any]:
    """Create one captured landmark sample record."""
    return {
        'sample_id': str(sample_id),
        'session_id': str(session_id),
        'sign_label': str(sign_label),
        'split': str(split),
        'landmarks': _round_landmarks(landmarks),
        'features': _round_features(features),
        'source': str(source),
        'captured_at': _utc_timestamp(),
    }


def create_prediction_record(
    frame_id: str,
    expected_label: str,
    predicted_label: str,
    confidence: float,
    is_low_confidence: bool,
    top_candidates: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Create one live inference prediction record."""
    return {
        'frame_id': str(frame_id),
        'expected_label': str(expected_label),
        'predicted_label': str(predicted_label),
        'confidence': round(float(confidence), 4),
        'is_low_confidence': bool(is_low_confidence),
        'top_candidates': [
            {
                'label': str(item.get('label', '')),
                'score': round(float(item.get('score', 0.0)), 4),
            }
            for item in top_candidates
        ],
    }


def create_session_summary(
    session_id: str,
    signs_modeled: int,
    captures_total: int,
    training_samples: int,
    test_samples: int,
    test_accuracy: float,
    live_frames: int,
    low_confidence_frames: int,
    elapsed_ms: float,
    artifacts: Dict[str, Any],
    prediction_previews: List[Dict[str, Any]],
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """Create final session summary for reporting and persistence."""
    return {
        'session_id': str(session_id),
        'signs_modeled': int(signs_modeled),
        'captures_total': int(captures_total),
        'training_samples': int(training_samples),
        'test_samples': int(test_samples),
        'test_accuracy': round(float(test_accuracy), 4),
        'live_frames': int(live_frames),
        'low_confidence_frames': int(low_confidence_frames),
        'elapsed_ms': float(elapsed_ms),
        'artifacts': dict(artifacts),
        'prediction_previews': list(prediction_previews),
        'metrics': dict(metrics),
        'finished_at': _utc_timestamp(),
    }


def create_record(**kwargs):
    """Backwards-compatible generic record factory."""
    return dict(kwargs)
