"""
models.py - Data constructors for MNIST pipeline objects
========================================================

We use plain dictionaries in this beginner project instead of custom classes.
Reason:
    - easy to inspect in print output,
    - easy to serialize to JSON,
    - lower conceptual overhead while learning ML workflow structure.

Stretch goal: replace these with dataclasses later.
"""

from datetime import datetime


def create_run_config(
    model_name: str = "LogisticRegression",
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict:
    """
    Create a run configuration object.

    Parameters:
        model_name (str): Baseline model identifier.
        test_size (float): Fraction of data reserved for test split.
        random_state (int): Seed for deterministic splits.

    Returns:
        dict: Configuration record used by operations.py.
    """
    # TODO: Add optional hyperparameter map and dataset source metadata.
    return {
        "model_name": model_name,
        "test_size": test_size,
        "random_state": random_state,
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }


def create_confusion_pair(true_label: int, predicted_label: int, count: int) -> dict:
    """
    Create a confusion pair summary entry.

    Parameters:
        true_label (int): Actual class label.
        predicted_label (int): Predicted class label.
        count (int): Number of samples in this confusion pair.

    Returns:
        dict: Structured confusion pair object.
    """
    return {
        "true_label": int(true_label),
        "predicted_label": int(predicted_label),
        "count": int(count),
    }


def create_run_summary(
    config: dict,
    accuracy: float,
    train_size: int,
    test_size: int,
    top_confusions: list,
    notes: str = "",
) -> dict:
    """
    Create a training run summary object for persistence and display.

    Parameters:
        config (dict): Run configuration object.
        accuracy (float): Test set accuracy.
        train_size (int): Number of training samples.
        test_size (int): Number of test samples.
        top_confusions (list[dict]): Common confusion pairs.
        notes (str): Optional free-text notes for the run.

    Returns:
        dict: Complete run summary record.
    """
    return {
        "config": config,
        "accuracy": float(accuracy),
        "train_size": int(train_size),
        "test_size": int(test_size),
        "top_confusions": top_confusions,
        "notes": notes,
        "saved_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
