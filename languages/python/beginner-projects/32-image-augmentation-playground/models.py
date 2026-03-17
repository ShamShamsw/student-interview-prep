"""
models.py - Data models for Project 32: Image Augmentation Playground
"""

from datetime import datetime
from typing import Any, Dict, List


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string."""
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def create_playground_config(
    image_width: int = 256,
    image_height: int = 256,
    num_samples: int = 8,
    augmentation_rounds: int = 3,
    random_seed: int = 42,
    export_dpi: int = 120,
    color_mode: str = "rgb",
    evaluate_classifier: bool = True,
) -> Dict[str, Any]:
    """Create a validated image augmentation playground configuration record."""
    width = max(64, int(image_width))
    height = max(64, int(image_height))
    return {
        "project_type": "image_augmentation_playground",
        "image_width": width,
        "image_height": height,
        "num_samples": max(2, int(num_samples)),
        "augmentation_rounds": max(1, int(augmentation_rounds)),
        "random_seed": int(random_seed),
        "export_dpi": max(72, int(export_dpi)),
        "color_mode": color_mode.strip() or "rgb",
        "evaluate_classifier": bool(evaluate_classifier),
        "created_at": _utc_timestamp(),
    }


def create_augmentation_record(
    aug_id: str,
    pipeline_name: str,
    operations: List[str],
    original_stats: Dict[str, float],
    augmented_stats: Dict[str, float],
    grid_file: str,
) -> Dict[str, Any]:
    """Create a persisted augmentation pipeline result record."""
    return {
        "aug_id": aug_id,
        "pipeline_name": pipeline_name,
        "operations": operations,
        "original_stats": original_stats,
        "augmented_stats": augmented_stats,
        "grid_file": grid_file,
        "created_at": _utc_timestamp(),
    }


def create_evaluation_result(
    classifier: str,
    baseline_accuracy: float,
    augmented_accuracy: float,
    dataset_size_baseline: int,
    dataset_size_augmented: int,
    test_size: int,
) -> Dict[str, Any]:
    """Create a classifier evaluation comparison record."""
    return {
        "classifier": classifier,
        "baseline_accuracy": float(baseline_accuracy),
        "augmented_accuracy": float(augmented_accuracy),
        "dataset_size_baseline": int(dataset_size_baseline),
        "dataset_size_augmented": int(dataset_size_augmented),
        "test_size": int(test_size),
        "accuracy_delta": float(augmented_accuracy - baseline_accuracy),
    }


def create_run_summary(
    run_id: str,
    pipelines_applied: int,
    grids_exported: int,
    elapsed_ms: float,
    artifacts: Dict[str, Any],
    pipeline_previews: List[Dict[str, Any]],
    evaluation: Dict[str, Any],
) -> Dict[str, Any]:
    """Create a final run summary for reporting and persistence."""
    return {
        "run_id": run_id,
        "pipelines_applied": int(pipelines_applied),
        "grids_exported": int(grids_exported),
        "elapsed_ms": float(elapsed_ms),
        "artifacts": artifacts,
        "pipeline_previews": pipeline_previews,
        "evaluation": evaluation,
        "finished_at": _utc_timestamp(),
    }


def create_record(**kwargs: Any) -> Dict[str, Any]:
    """Backwards-compatible generic record factory."""
    return dict(kwargs)

