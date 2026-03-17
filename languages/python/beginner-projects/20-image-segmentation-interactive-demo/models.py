"""
models.py - Data models for Image Segmentation Interactive Demo
===============================================================

Defines:
    - Segmentation training configuration and architecture info
    - Epoch-level metric records
    - Session-level performance and quality summaries
"""

from datetime import datetime


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp.

    Returns:
        str: Timestamp string with trailing Z.
    """
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def create_project_config(
    image_size: int = 32,
    train_samples: int = 800,
    val_samples: int = 200,
    hidden_dim: int = 128,
    bottleneck_dim: int = 48,
    epochs: int = 160,
    batch_size: int = 32,
    learning_rate: float = 0.08,
    snapshot_interval: int = 20,
    random_seed: int = 42,
) -> dict:
    """Create the default runtime configuration for segmentation training.

    Parameters:
        image_size (int): Height and width of grayscale image.
        train_samples (int): Number of synthetic training samples.
        val_samples (int): Number of synthetic validation samples.
        hidden_dim (int): Width of encoder and decoder hidden layers.
        bottleneck_dim (int): Latent bottleneck width.
        epochs (int): Number of training epochs.
        batch_size (int): Mini-batch size per epoch.
        learning_rate (float): SGD step size.
        snapshot_interval (int): Epoch interval for prediction snapshots.
        random_seed (int): Random seed for reproducibility.

    Returns:
        dict: Configuration dictionary.
    """
    return {
        "image_size": image_size,
        "train_samples": train_samples,
        "val_samples": val_samples,
        "hidden_dim": hidden_dim,
        "bottleneck_dim": bottleneck_dim,
        "epochs": epochs,
        "batch_size": batch_size,
        "learning_rate": learning_rate,
        "snapshot_interval": snapshot_interval,
        "random_seed": random_seed,
        "created_at": _utc_timestamp(),
    }


def create_epoch_record(
    epoch: int,
    train_loss: float,
    val_loss: float,
    val_iou: float,
    val_dice: float,
    pixel_accuracy: float,
) -> dict:
    """Create one epoch metric record.

    Parameters:
        epoch (int): 1-based epoch index.
        train_loss (float): Training BCE loss for epoch.
        val_loss (float): Validation BCE loss for epoch.
        val_iou (float): Validation IoU score.
        val_dice (float): Validation Dice score.
        pixel_accuracy (float): Validation pixel-level accuracy.

    Returns:
        dict: Epoch summary dictionary.
    """
    return {
        "epoch": epoch,
        "train_loss": train_loss,
        "val_loss": val_loss,
        "val_iou": val_iou,
        "val_dice": val_dice,
        "pixel_accuracy": pixel_accuracy,
    }


def create_training_metrics(
    final_train_loss: float,
    final_val_loss: float,
    mean_iou_last_20: float,
    max_iou: float,
    final_dice: float,
    final_pixel_accuracy: float,
) -> dict:
    """Create aggregate training metrics.

    Returns:
        dict: Session-level metric summary.
    """
    return {
        "final_train_loss": final_train_loss,
        "final_val_loss": final_val_loss,
        "mean_iou_last_20": mean_iou_last_20,
        "max_iou": max_iou,
        "final_dice": final_dice,
        "final_pixel_accuracy": final_pixel_accuracy,
    }


def create_training_result(
    config: dict,
    architecture: dict,
    history: list[dict],
    metrics: dict,
    sample_stats: dict,
    artifacts: dict,
) -> dict:
    """Create complete segmentation session result.

    Parameters:
        config (dict): Training configuration.
        architecture (dict): Encoder-decoder architecture metadata.
        history (list[dict]): Epoch training history.
        metrics (dict): Aggregate training metrics.
        sample_stats (dict): Final prediction quality summary.
        artifacts (dict): Paths to saved visual artifacts.

    Returns:
        dict: Complete project output artifact.
    """
    return {
        "config": config,
        "architecture": architecture,
        "history": history,
        "metrics": metrics,
        "sample_stats": sample_stats,
        "artifacts": artifacts,
        "completed_at": _utc_timestamp(),
    }
