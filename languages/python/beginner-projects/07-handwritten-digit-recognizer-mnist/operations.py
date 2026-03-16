"""
operations.py - Core ML workflow for the MNIST project
======================================================

This module contains the main data science logic:
    - load data,
    - split data,
    - train baseline model,
    - evaluate,
    - summarize errors,
    - save run artifacts.

No print formatting should live here. Return structured data and let
display.py decide how to present it.
"""

from collections import Counter

from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

from models import create_confusion_pair, create_run_config, create_run_summary
from storage import save_latest_run


def load_dataset() -> tuple:
    """
    Load the digit dataset.

    Returns:
        tuple: (X, y) where X is feature matrix and y is labels.

    Why `load_digits` here:
        It is built into scikit-learn, lightweight, and reliable for a
        beginner baseline workflow. You can swap in full MNIST later.
    """
    # TODO: Add optional support for external MNIST source.
    dataset = load_digits()
    return dataset.data, dataset.target


def split_dataset(X, y, test_size: float, random_state: int) -> tuple:
    """
    Split features and labels into train/test sets.

    Parameters:
        X: Feature matrix.
        y: Target labels.
        test_size (float): Test ratio.
        random_state (int): Seed for reproducibility.

    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )


def train_baseline_model(X_train, y_train):
    """
    Train a baseline Logistic Regression model.

    Parameters:
        X_train: Training features.
        y_train: Training labels.

    Returns:
        object: Trained sklearn model.

    Why logistic regression first:
        Fast training + strong baseline + interpretable behavior.
    """
    # TODO: expose these hyperparameters in run config.
    model = LogisticRegression(max_iter=1200)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test) -> dict:
    """
    Evaluate model predictions on the test set.

    Parameters:
        model: Trained model object.
        X_test: Test features.
        y_test: Test labels.

    Returns:
        dict: Includes accuracy, confusion matrix, and predictions.
    """
    predictions = model.predict(X_test)
    cm = confusion_matrix(y_test, predictions)
    return {
        "accuracy": accuracy_score(y_test, predictions),
        "confusion_matrix": cm,
        "y_true": y_test,
        "y_pred": predictions,
    }


def get_top_confusions(y_true, y_pred, limit: int = 5) -> list:
    """
    Identify the most common misclassification pairs.

    Parameters:
        y_true: Ground truth labels.
        y_pred: Predicted labels.
        limit (int): Number of top pairs to return.

    Returns:
        list[dict]: Top confusion pairs sorted by descending count.

    Example pair:
        true=8, predicted=1, count=3
    """
    counter = Counter()
    for actual, predicted in zip(y_true, y_pred):
        if int(actual) != int(predicted):
            counter[(int(actual), int(predicted))] += 1

    top = counter.most_common(limit)
    return [create_confusion_pair(t, p, c) for (t, p), c in top]


def run_full_pipeline() -> dict:
    """
    Execute one full baseline run and save summary artifact.

    Returns:
        dict: Run summary object for display.
    """
    config = create_run_config()
    X, y = load_dataset()
    X_train, X_test, y_train, y_test = split_dataset(
        X,
        y,
        test_size=config["test_size"],
        random_state=config["random_state"],
    )

    model = train_baseline_model(X_train, y_train)
    evaluation = evaluate_model(model, X_test, y_test)
    top_confusions = get_top_confusions(evaluation["y_true"], evaluation["y_pred"])

    summary = create_run_summary(
        config=config,
        accuracy=evaluation["accuracy"],
        train_size=len(X_train),
        test_size=len(X_test),
        top_confusions=top_confusions,
        notes="Baseline logistic regression run.",
    )

    save_latest_run(summary)
    return summary
