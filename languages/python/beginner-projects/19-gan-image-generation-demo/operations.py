"""
operations.py - GAN training engine and analysis workflows
==========================================================

Implements:
    - Procedural real-image data sampler
    - Lightweight GAN training in NumPy
    - Quality tracking across epochs
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
    """Return profile metadata for the synthetic image dataset.

    Returns:
        dict: Dataset description and shape properties.
    """
    return {
        "name": "Synthetic 16x16 grayscale blobs",
        "description": "Random Gaussian blobs plus low-intensity noise",
        "pixel_range": [0.0, 1.0],
        "channels": 1,
    }


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40.0, 40.0)))


def _leaky_relu(x: np.ndarray, negative_slope: float = 0.2) -> np.ndarray:
    return np.where(x > 0.0, x, negative_slope * x)


def _leaky_relu_grad(x: np.ndarray, negative_slope: float = 0.2) -> np.ndarray:
    return np.where(x > 0.0, 1.0, negative_slope)


def _sample_real_batch(batch_size: int, image_size: int, rng: np.random.Generator) -> np.ndarray:
    """Generate synthetic real images with Gaussian blobs.

    Returns:
        np.ndarray: Batch of shape (batch_size, image_size * image_size).
    """
    yy, xx = np.mgrid[0:image_size, 0:image_size]
    images = np.zeros((batch_size, image_size, image_size), dtype=float)

    for i in range(batch_size):
        cx = rng.uniform(0, image_size - 1)
        cy = rng.uniform(0, image_size - 1)
        sigma = rng.uniform(1.3, 2.9)
        amplitude = rng.uniform(0.7, 1.0)

        blob = amplitude * np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2.0 * sigma * sigma))
        noise = rng.normal(loc=0.02, scale=0.03, size=(image_size, image_size))
        image = np.clip(blob + noise, 0.0, 1.0)
        images[i] = image

    return images.reshape(batch_size, image_size * image_size)


def _generator_forward(
    z: np.ndarray,
    w1: np.ndarray,
    b1: np.ndarray,
    w2: np.ndarray,
    b2: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Forward pass through generator."""
    g_a1 = z @ w1 + b1
    g_h1 = np.tanh(g_a1)
    g_a2 = g_h1 @ w2 + b2
    g_out = _sigmoid(g_a2)
    return g_a1, g_h1, g_a2, g_out


def _discriminator_forward(
    x: np.ndarray,
    v1: np.ndarray,
    c1: np.ndarray,
    v2: np.ndarray,
    c2: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Forward pass through discriminator."""
    d_a1 = x @ v1 + c1
    d_h1 = _leaky_relu(d_a1)
    d_a2 = d_h1 @ v2 + c2
    d_prob = _sigmoid(d_a2)
    return d_a1, d_h1, d_a2, d_prob


def _save_artifacts(
    history: list[dict],
    snapshots: list[np.ndarray],
    image_size: int,
) -> dict:
    """Save learning curves and generated sample grids.

    Returns:
        dict: Relative artifact paths.
    """
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    epochs = np.array([h["epoch"] for h in history])
    d_loss = np.array([h["d_loss"] for h in history], dtype=float)
    g_loss = np.array([h["g_loss"] for h in history], dtype=float)
    quality = np.array([h["quality_score"] for h in history], dtype=float)

    loss_path = RUNS_DIR / "gan_losses.png"
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(epochs, d_loss, label="Discriminator loss", linewidth=2)
    ax.plot(epochs, g_loss, label="Generator loss", linewidth=2)
    ax.set_title("GAN Training Losses")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss")
    ax.legend()
    fig.tight_layout()
    fig.savefig(loss_path, dpi=160)
    plt.close(fig)

    quality_path = RUNS_DIR / "quality_curve.png"
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(epochs, quality, color="#2b8cbe", linewidth=2.2)
    ax.set_ylim(0.0, 1.05)
    ax.set_title("Generated Sample Quality Trend")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Quality score")
    fig.tight_layout()
    fig.savefig(quality_path, dpi=160)
    plt.close(fig)

    sample_path = RUNS_DIR / "generated_samples_grid.png"
    if snapshots:
        n = min(16, snapshots[-1].shape[0])
        cols = 4
        rows = 4
        fig, axes = plt.subplots(rows, cols, figsize=(6, 6))
        flat_axes = axes.flatten()
        for i in range(rows * cols):
            ax = flat_axes[i]
            ax.axis("off")
            if i < n:
                ax.imshow(snapshots[-1][i].reshape(image_size, image_size), cmap="gray", vmin=0, vmax=1)
        fig.suptitle("Final Generator Samples", y=0.92)
        fig.tight_layout()
        fig.savefig(sample_path, dpi=170)
        plt.close(fig)

    return {
        "loss_curve": str(Path("data") / "runs" / "gan_losses.png"),
        "quality_curve": str(Path("data") / "runs" / "quality_curve.png"),
        "sample_grid": str(Path("data") / "runs" / "generated_samples_grid.png"),
    }


def run_core_flow(config: dict | None = None) -> dict:
    """Execute the main GAN training workflow.

    Parameters:
        config (dict | None): Optional override of default config.

    Returns:
        dict: Session summary with GAN training outputs.
    """
    if config is None:
        config = create_project_config()

    image_size = config["image_size"]
    latent_dim = config["latent_dim"]
    hidden_dim = config["hidden_dim"]
    image_dim = image_size * image_size
    epochs = config["epochs"]
    batch_size = config["batch_size"]
    lr_g = config["learning_rate_generator"]
    lr_d = config["learning_rate_discriminator"]
    snapshot_interval = config["snapshot_interval"]
    rng = np.random.default_rng(config.get("random_seed", 42))

    # Xavier-like initialization for stable gradients.
    w1 = rng.normal(0, np.sqrt(2.0 / (latent_dim + hidden_dim)), size=(latent_dim, hidden_dim))
    b1 = np.zeros((1, hidden_dim))
    w2 = rng.normal(0, np.sqrt(2.0 / (hidden_dim + image_dim)), size=(hidden_dim, image_dim))
    b2 = np.zeros((1, image_dim))

    v1 = rng.normal(0, np.sqrt(2.0 / (image_dim + hidden_dim)), size=(image_dim, hidden_dim))
    c1 = np.zeros((1, hidden_dim))
    v2 = rng.normal(0, np.sqrt(2.0 / (hidden_dim + 1)), size=(hidden_dim, 1))
    c2 = np.zeros((1, 1))

    history: list[dict] = []
    snapshots: list[np.ndarray] = []

    eps = 1e-8

    for epoch in range(1, epochs + 1):
        real_x = _sample_real_batch(batch_size, image_size, rng)
        z = rng.normal(0.0, 1.0, size=(batch_size, latent_dim))

        # --------------------
        # Discriminator update
        # --------------------
        _, _, _, fake_x = _generator_forward(z, w1, b1, w2, b2)

        d_a1_real, d_h1_real, _, d_prob_real = _discriminator_forward(real_x, v1, c1, v2, c2)
        d_a1_fake, d_h1_fake, _, d_prob_fake = _discriminator_forward(fake_x, v1, c1, v2, c2)

        d_loss = -np.mean(np.log(d_prob_real + eps) + np.log(1.0 - d_prob_fake + eps))

        delta_out_real = d_prob_real - 1.0
        delta_out_fake = d_prob_fake - 0.0

        grad_v2 = (d_h1_real.T @ delta_out_real + d_h1_fake.T @ delta_out_fake) / batch_size
        grad_c2 = np.mean(delta_out_real + delta_out_fake, axis=0, keepdims=True)

        delta_h_real = (delta_out_real @ v2.T) * _leaky_relu_grad(d_a1_real)
        delta_h_fake = (delta_out_fake @ v2.T) * _leaky_relu_grad(d_a1_fake)

        grad_v1 = (real_x.T @ delta_h_real + fake_x.T @ delta_h_fake) / batch_size
        grad_c1 = np.mean(delta_h_real + delta_h_fake, axis=0, keepdims=True)

        v2 -= lr_d * grad_v2
        c2 -= lr_d * grad_c2
        v1 -= lr_d * grad_v1
        c1 -= lr_d * grad_c1

        # ----------------
        # Generator update
        # ----------------
        g_a1, g_h1, g_a2, fake_x = _generator_forward(z, w1, b1, w2, b2)
        d_a1_fake2, _, _, d_prob_fake2 = _discriminator_forward(fake_x, v1, c1, v2, c2)

        g_loss = -np.mean(np.log(d_prob_fake2 + eps))

        delta_out_g = d_prob_fake2 - 1.0
        delta_h_d = (delta_out_g @ v2.T) * _leaky_relu_grad(d_a1_fake2)
        delta_x = delta_h_d @ v1.T

        delta_g_a2 = delta_x * (fake_x * (1.0 - fake_x))
        grad_w2 = (g_h1.T @ delta_g_a2) / batch_size
        grad_b2 = np.mean(delta_g_a2, axis=0, keepdims=True)

        delta_g_h1 = (delta_g_a2 @ w2.T) * (1.0 - np.tanh(g_a1) ** 2)
        grad_w1 = (z.T @ delta_g_h1) / batch_size
        grad_b1 = np.mean(delta_g_h1, axis=0, keepdims=True)

        w2 -= lr_g * grad_w2
        b2 -= lr_g * grad_b2
        w1 -= lr_g * grad_w1
        b1 -= lr_g * grad_b1

        # Heuristic quality: encourage fake confidence near 0.5 and moderate diversity.
        fake_mean = float(np.mean(fake_x))
        fake_std = float(np.std(fake_x))
        balance = float(1.0 - abs(float(np.mean(d_prob_fake2)) - 0.5) * 2.0)
        diversity = float(np.clip(fake_std / 0.30, 0.0, 1.0))
        quality = float(np.clip(0.6 * balance + 0.4 * diversity, 0.0, 1.0))

        history.append(
            create_epoch_record(
                epoch=epoch,
                d_loss=float(d_loss),
                g_loss=float(g_loss),
                d_real_mean=float(np.mean(d_prob_real)),
                d_fake_mean=float(np.mean(d_prob_fake2)),
                quality_score=quality,
            )
        )

        if epoch % snapshot_interval == 0 or epoch == epochs:
            snapshot_z = rng.normal(0.0, 1.0, size=(16, latent_dim))
            _, _, _, snapshot_fake = _generator_forward(snapshot_z, w1, b1, w2, b2)
            snapshots.append(snapshot_fake)

    metrics = create_training_metrics(
        final_d_loss=history[-1]["d_loss"],
        final_g_loss=history[-1]["g_loss"],
        mean_quality_last_20=float(np.mean([h["quality_score"] for h in history[-20:]])),
        max_quality=float(np.max([h["quality_score"] for h in history])),
        final_d_real_mean=history[-1]["d_real_mean"],
        final_d_fake_mean=history[-1]["d_fake_mean"],
    )

    sample_stats = {
        "final_generated_mean": float(np.mean(snapshots[-1])) if snapshots else 0.0,
        "final_generated_std": float(np.std(snapshots[-1])) if snapshots else 0.0,
        "num_snapshots": len(snapshots),
    }
    artifacts = _save_artifacts(history, snapshots, image_size)

    architecture = {
        "generator": {
            "input_dim": latent_dim,
            "hidden_dim": hidden_dim,
            "output_dim": image_dim,
            "activation": "tanh + sigmoid",
        },
        "discriminator": {
            "input_dim": image_dim,
            "hidden_dim": hidden_dim,
            "output_dim": 1,
            "activation": "leaky_relu + sigmoid",
        },
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
