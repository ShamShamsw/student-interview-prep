"""
models.py - Data models for GAN Image Generation Demo
=====================================================

Defines:
    - GAN training configuration and architecture info
    - Epoch-level metric records
    - Session-level training and quality summaries
"""

from datetime import datetime


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp.

    Returns:
        str: Timestamp string with trailing Z.
    """
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def create_project_config(
    image_size: int = 16,
    latent_dim: int = 24,
    hidden_dim: int = 64,
    epochs: int = 250,
    batch_size: int = 64,
    learning_rate_generator: float = 0.025,
    learning_rate_discriminator: float = 0.015,
    snapshot_interval: int = 25,
    random_seed: int = 42,
) -> dict:
    """Create the default runtime configuration for GAN training.

    Parameters:
        image_size (int): Height and width of grayscale output image.
        latent_dim (int): Dimension of generator latent noise vector.
        hidden_dim (int): Hidden layer width for both networks.
        epochs (int): Number of GAN training epochs.
        batch_size (int): Mini-batch size per epoch.
        learning_rate_generator (float): Generator SGD step size.
        learning_rate_discriminator (float): Discriminator SGD step size.
        snapshot_interval (int): Epoch interval for generated-image snapshots.
        random_seed (int): Random seed for reproducibility.

    Returns:
        dict: Configuration dictionary.
    """
    return {
        "image_size": image_size,
        "latent_dim": latent_dim,
        "hidden_dim": hidden_dim,
        "epochs": epochs,
        "batch_size": batch_size,
        "learning_rate_generator": learning_rate_generator,
        "learning_rate_discriminator": learning_rate_discriminator,
        "snapshot_interval": snapshot_interval,
        "random_seed": random_seed,
        "created_at": _utc_timestamp(),
    }


def create_epoch_record(
    epoch: int,
    d_loss: float,
    g_loss: float,
    d_real_mean: float,
    d_fake_mean: float,
    quality_score: float,
) -> dict:
    """Create one epoch metric record.

    Parameters:
        epoch (int): 1-based epoch index.
        d_loss (float): Discriminator loss at epoch.
        g_loss (float): Generator loss at epoch.
        d_real_mean (float): Mean discriminator score on real samples.
        d_fake_mean (float): Mean discriminator score on generated samples.
        quality_score (float): Heuristic quality score in [0, 1].

    Returns:
        dict: Epoch summary dictionary.
    """
    return {
        "epoch": epoch,
        "d_loss": d_loss,
        "g_loss": g_loss,
        "d_real_mean": d_real_mean,
        "d_fake_mean": d_fake_mean,
        "quality_score": quality_score,
    }


def create_training_metrics(
    final_d_loss: float,
    final_g_loss: float,
    mean_quality_last_20: float,
    max_quality: float,
    final_d_real_mean: float,
    final_d_fake_mean: float,
) -> dict:
    """Create aggregate training metrics.

    Returns:
        dict: Session-level metric summary.
    """
    return {
        "final_d_loss": final_d_loss,
        "final_g_loss": final_g_loss,
        "mean_quality_last_20": mean_quality_last_20,
        "max_quality": max_quality,
        "final_d_real_mean": final_d_real_mean,
        "final_d_fake_mean": final_d_fake_mean,
    }


def create_training_result(
    config: dict,
    architecture: dict,
    history: list[dict],
    metrics: dict,
    sample_stats: dict,
    artifacts: dict,
) -> dict:
    """Create complete GAN session result.

    Parameters:
        config (dict): Training configuration.
        architecture (dict): Generator/discriminator architecture metadata.
        history (list[dict]): Epoch training history.
        metrics (dict): Aggregate training metrics.
        sample_stats (dict): Final sample distribution summary.
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
