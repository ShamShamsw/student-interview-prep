"""
operations.py - Segmentation training engine and analysis workflows
===================================================================

Implements:
    - Procedural image-mask dataset synthesis
    - Lightweight encoder-decoder training in NumPy
    - Validation quality tracking across epochs
    - Visual artifact generation and persistence
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from models import (
    create_epoch_record,
    create_project_config,
    create_training_metrics,
    create_training_result,
)
from storage import RUNS_DIR, save_latest_session


def load_dataset_profile() -> dict:
    """Return profile metadata for the synthetic segmentation dataset.

    Returns:
        dict: Dataset description and shape properties.
    """
    return {
        "name": "Synthetic 32x32 grayscale shapes",
        "description": "Mixed circles and rectangles with additive noise",
        "pixel_range": [0.0, 1.0],
        "mask_labels": [0, 1],
    }


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40.0, 40.0)))


def _relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(x, 0.0)


def _relu_grad(x: np.ndarray) -> np.ndarray:
    return (x > 0.0).astype(float)


def _sample_shape_pair(image_size: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Generate one synthetic grayscale image and its binary mask."""
    yy, xx = np.mgrid[0:image_size, 0:image_size]
    background = rng.normal(loc=0.12, scale=0.07, size=(image_size, image_size))
    background = np.clip(background, 0.0, 0.35)

    mask = np.zeros((image_size, image_size), dtype=float)

    shape_type = "circle" if rng.random() < 0.5 else "rectangle"
    if shape_type == "circle":
        radius = rng.uniform(image_size * 0.14, image_size * 0.28)
        cx = rng.uniform(radius + 1, image_size - radius - 1)
        cy = rng.uniform(radius + 1, image_size - radius - 1)
        mask[((xx - cx) ** 2 + (yy - cy) ** 2) <= radius**2] = 1.0
    else:
        width = int(rng.integers(image_size // 5, image_size // 2))
        height = int(rng.integers(image_size // 5, image_size // 2))
        x0 = int(rng.integers(1, image_size - width - 1))
        y0 = int(rng.integers(1, image_size - height - 1))
        mask[y0 : y0 + height, x0 : x0 + width] = 1.0

    edge_band = np.clip(mask - 0.85 * np.pad(mask[1:, :], ((0, 1), (0, 0))), 0.0, 1.0)
    foreground_intensity = rng.uniform(0.62, 0.95)
    edge_boost = rng.uniform(0.08, 0.18)

    image = background + mask * foreground_intensity + edge_band * edge_boost
    image += rng.normal(0.0, 0.04, size=(image_size, image_size))
    image = np.clip(image, 0.0, 1.0)

    return image, mask


def _create_dataset(
    num_samples: int,
    image_size: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Create synthetic segmentation dataset.

    Returns:
        tuple[np.ndarray, np.ndarray]: Flattened images and masks.
    """
    images = np.zeros((num_samples, image_size * image_size), dtype=float)
    masks = np.zeros((num_samples, image_size * image_size), dtype=float)

    for i in range(num_samples):
        image, mask = _sample_shape_pair(image_size=image_size, rng=rng)
        images[i] = image.reshape(-1)
        masks[i] = mask.reshape(-1)

    return images, masks


def _forward(
    x: np.ndarray,
    w1: np.ndarray,
    b1: np.ndarray,
    w2: np.ndarray,
    b2: np.ndarray,
    w3: np.ndarray,
    b3: np.ndarray,
    w4: np.ndarray,
    b4: np.ndarray,
) -> tuple[np.ndarray, ...]:
    """Run one forward pass through tiny encoder-decoder."""
    a1 = x @ w1 + b1
    h1 = _relu(a1)
    a2 = h1 @ w2 + b2
    bottleneck = np.tanh(a2)
    a3 = bottleneck @ w3 + b3
    h3 = _relu(a3)
    a4 = h3 @ w4 + b4
    out = _sigmoid(a4)
    return a1, h1, a2, bottleneck, a3, h3, a4, out


def _binary_cross_entropy(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    pos_weight: float = 1.0,
    eps: float = 1e-8,
) -> float:
    """Compute weighted BCE to reduce foreground/background imbalance."""
    return float(
        -np.mean(
            pos_weight * y_true * np.log(y_pred + eps)
            + (1.0 - y_true) * np.log(1.0 - y_pred + eps)
        )
    )


def _segmentation_scores(y_true: np.ndarray, y_prob: np.ndarray, threshold: float = 0.4) -> tuple[float, float, float]:
    """Compute pixel accuracy, IoU and Dice metrics."""
    y_hat = (y_prob >= threshold).astype(float)

    intersection = float(np.sum(y_hat * y_true))
    union = float(np.sum(np.clip(y_hat + y_true, 0.0, 1.0)))
    iou = intersection / (union + 1e-8)

    dice = (2.0 * intersection) / (float(np.sum(y_hat) + np.sum(y_true)) + 1e-8)
    pixel_accuracy = float(np.mean(y_hat == y_true))

    return pixel_accuracy, iou, dice


def _save_artifacts(
    history: list[dict],
    sample_images: np.ndarray,
    sample_masks: np.ndarray,
    sample_predictions: np.ndarray,
    image_size: int,
) -> dict:
    """Save learning curves and prediction panels.

    Returns:
        dict: Relative artifact paths.
    """
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    epochs = np.array([h["epoch"] for h in history])
    train_loss = np.array([h["train_loss"] for h in history], dtype=float)
    val_loss = np.array([h["val_loss"] for h in history], dtype=float)
    val_iou = np.array([h["val_iou"] for h in history], dtype=float)
    val_dice = np.array([h["val_dice"] for h in history], dtype=float)

    loss_path = RUNS_DIR / "segmentation_losses.png"
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(epochs, train_loss, label="Train BCE", linewidth=2)
    ax.plot(epochs, val_loss, label="Validation BCE", linewidth=2)
    ax.set_title("Segmentation Training Losses")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss")
    ax.legend()
    fig.tight_layout()
    fig.savefig(loss_path, dpi=160)
    plt.close(fig)

    quality_path = RUNS_DIR / "segmentation_quality.png"
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(epochs, val_iou, label="Validation IoU", linewidth=2.1)
    ax.plot(epochs, val_dice, label="Validation Dice", linewidth=2.1)
    ax.set_ylim(0.0, 1.02)
    ax.set_title("Segmentation Quality Trend")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Score")
    ax.legend()
    fig.tight_layout()
    fig.savefig(quality_path, dpi=160)
    plt.close(fig)

    panel_path = RUNS_DIR / "segmentation_samples_grid.png"
    n = min(6, sample_images.shape[0])
    fig, axes = plt.subplots(n, 3, figsize=(8, 2.4 * n))
    if n == 1:
        axes = np.array([axes])

    for i in range(n):
        raw_img = sample_images[i].reshape(image_size, image_size)
        gt_mask = sample_masks[i].reshape(image_size, image_size)
        pred_mask = (sample_predictions[i].reshape(image_size, image_size) >= 0.4).astype(float)

        axes[i, 0].imshow(raw_img, cmap="gray", vmin=0, vmax=1)
        axes[i, 0].set_title("Input")
        axes[i, 0].axis("off")

        axes[i, 1].imshow(gt_mask, cmap="gray", vmin=0, vmax=1)
        axes[i, 1].set_title("Ground truth")
        axes[i, 1].axis("off")

        axes[i, 2].imshow(pred_mask, cmap="gray", vmin=0, vmax=1)
        axes[i, 2].set_title("Prediction")
        axes[i, 2].axis("off")

    fig.suptitle("Segmentation Prediction Samples", y=0.995)
    fig.tight_layout()
    fig.savefig(panel_path, dpi=170)
    plt.close(fig)

    return {
        "loss_curve": str(Path("data") / "runs" / "segmentation_losses.png"),
        "quality_curve": str(Path("data") / "runs" / "segmentation_quality.png"),
        "sample_grid": str(Path("data") / "runs" / "segmentation_samples_grid.png"),
    }


def run_core_flow(config: dict | None = None) -> dict:
    """Execute the main segmentation training workflow.

    Parameters:
        config (dict | None): Optional override of default config.

    Returns:
        dict: Session summary with segmentation training outputs.
    """
    if config is None:
        config = create_project_config()

    image_size = config["image_size"]
    image_dim = image_size * image_size
    train_samples = config["train_samples"]
    val_samples = config["val_samples"]
    hidden_dim = config["hidden_dim"]
    bottleneck_dim = config["bottleneck_dim"]
    epochs = config["epochs"]
    batch_size = config["batch_size"]
    learning_rate = config["learning_rate"]
    snapshot_interval = config["snapshot_interval"]
    rng = np.random.default_rng(config.get("random_seed", 42))

    train_x, train_y = _create_dataset(num_samples=train_samples, image_size=image_size, rng=rng)
    val_x, val_y = _create_dataset(num_samples=val_samples, image_size=image_size, rng=rng)

    foreground_ratio = float(np.mean(train_y))
    pos_weight = float(np.clip((1.0 - foreground_ratio) / (foreground_ratio + 1e-8), 1.0, 8.0))

    w1 = rng.normal(0, np.sqrt(2.0 / (image_dim + hidden_dim)), size=(image_dim, hidden_dim))
    b1 = np.zeros((1, hidden_dim))
    w2 = rng.normal(0, np.sqrt(2.0 / (hidden_dim + bottleneck_dim)), size=(hidden_dim, bottleneck_dim))
    b2 = np.zeros((1, bottleneck_dim))
    w3 = rng.normal(0, np.sqrt(2.0 / (bottleneck_dim + hidden_dim)), size=(bottleneck_dim, hidden_dim))
    b3 = np.zeros((1, hidden_dim))
    w4 = rng.normal(0, np.sqrt(2.0 / (hidden_dim + image_dim)), size=(hidden_dim, image_dim))
    b4 = np.zeros((1, image_dim))

    history: list[dict] = []

    for epoch in range(1, epochs + 1):
        indices = rng.permutation(train_samples)

        for start in range(0, train_samples, batch_size):
            idx = indices[start : start + batch_size]
            x_batch = train_x[idx]
            y_batch = train_y[idx]
            batch_n = x_batch.shape[0]

            a1, h1, a2, bottleneck, a3, h3, _, y_prob = _forward(
                x_batch, w1, b1, w2, b2, w3, b3, w4, b4
            )

            weighted_delta = (
                (1.0 - y_batch) * y_prob - pos_weight * y_batch * (1.0 - y_prob)
            ) / max(1, batch_n)
            grad_w4 = h3.T @ weighted_delta
            grad_b4 = np.sum(weighted_delta, axis=0, keepdims=True)

            delta_h3 = (weighted_delta @ w4.T) * _relu_grad(a3)
            grad_w3 = bottleneck.T @ delta_h3
            grad_b3 = np.sum(delta_h3, axis=0, keepdims=True)

            delta_bottleneck = (delta_h3 @ w3.T) * (1.0 - np.tanh(a2) ** 2)
            grad_w2 = h1.T @ delta_bottleneck
            grad_b2 = np.sum(delta_bottleneck, axis=0, keepdims=True)

            delta_h1 = (delta_bottleneck @ w2.T) * _relu_grad(a1)
            grad_w1 = x_batch.T @ delta_h1
            grad_b1 = np.sum(delta_h1, axis=0, keepdims=True)

            w4 -= learning_rate * grad_w4
            b4 -= learning_rate * grad_b4
            w3 -= learning_rate * grad_w3
            b3 -= learning_rate * grad_b3
            w2 -= learning_rate * grad_w2
            b2 -= learning_rate * grad_b2
            w1 -= learning_rate * grad_w1
            b1 -= learning_rate * grad_b1

        _, _, _, _, _, _, _, train_prob = _forward(train_x, w1, b1, w2, b2, w3, b3, w4, b4)
        _, _, _, _, _, _, _, val_prob = _forward(val_x, w1, b1, w2, b2, w3, b3, w4, b4)

        train_loss = _binary_cross_entropy(train_y, train_prob, pos_weight=pos_weight)
        val_loss = _binary_cross_entropy(val_y, val_prob, pos_weight=pos_weight)
        pixel_accuracy, val_iou, val_dice = _segmentation_scores(val_y, val_prob)

        history.append(
            create_epoch_record(
                epoch=epoch,
                train_loss=train_loss,
                val_loss=val_loss,
                val_iou=val_iou,
                val_dice=val_dice,
                pixel_accuracy=pixel_accuracy,
            )
        )

        if epoch % snapshot_interval == 0 or epoch == epochs:
            pass

    _, _, _, _, _, _, _, final_val_prob = _forward(val_x, w1, b1, w2, b2, w3, b3, w4, b4)
    metrics = create_training_metrics(
        final_train_loss=history[-1]["train_loss"],
        final_val_loss=history[-1]["val_loss"],
        mean_iou_last_20=float(np.mean([h["val_iou"] for h in history[-20:]])),
        max_iou=float(np.max([h["val_iou"] for h in history])),
        final_dice=history[-1]["val_dice"],
        final_pixel_accuracy=history[-1]["pixel_accuracy"],
    )

    sample_count = min(12, val_samples)
    sample_images = val_x[:sample_count]
    sample_masks = val_y[:sample_count]
    sample_predictions = final_val_prob[:sample_count]

    sample_stats = {
        "predicted_foreground_ratio": float(np.mean(sample_predictions >= 0.4)),
        "ground_truth_foreground_ratio": float(np.mean(sample_masks >= 0.5)),
        "samples_visualized": int(sample_count),
    }
    artifacts = _save_artifacts(
        history=history,
        sample_images=sample_images,
        sample_masks=sample_masks,
        sample_predictions=sample_predictions,
        image_size=image_size,
    )

    architecture = {
        "encoder_decoder": {
            "input_dim": image_dim,
            "hidden_dim": hidden_dim,
            "bottleneck_dim": bottleneck_dim,
            "output_dim": image_dim,
            "activation": "relu + tanh + sigmoid",
        }
    }

    base_result = create_training_result(
        config=config,
        architecture=architecture,
        history=history,
        metrics=metrics,
        sample_stats=sample_stats,
        artifacts=artifacts,
    )

    session_summary = {
        "status": "completed",
        "config": config,
        "dataset_profile": load_dataset_profile(),
        "base_result": base_result,
    }
    save_latest_session(session_summary)
    return session_summary
