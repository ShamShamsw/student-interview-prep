"""
display.py - Output formatting for GAN Image Generation Demo
============================================================

Provides:
    - CLI banners and headers
    - Configuration display
    - GAN training report formatting
    - Session summary generation
"""


def format_header() -> str:
    """Return the CLI banner for this project.

    Returns:
        str: User-facing banner string.
    """
    return (
        "=" * 70
        + "\n"
        + "  GAN IMAGE GENERATION DEMO - NUMPY ADVERSARIAL TRAINING\n"
        + "=" * 70
    )


def format_startup_guide(config: dict, dataset_profile: dict) -> str:
    """Return startup guidance shown before GAN training begins.

    Parameters:
        config (dict): Runtime configuration.
        dataset_profile (dict): Dataset metadata and description.

    Returns:
        str: Multi-line startup guide.
    """
    lines = [
        "",
        "Configuration:",
        f"  Image size: {config['image_size']}x{config['image_size']} (grayscale)",
        f"  Latent dimension: {config['latent_dim']}",
        f"  Hidden dimension: {config['hidden_dim']}",
        f"  Epochs: {config['epochs']}",
        f"  Batch size: {config['batch_size']}",
        f"  Generator learning rate: {config['learning_rate_generator']}",
        f"  Discriminator learning rate: {config['learning_rate_discriminator']}",
        f"  Snapshot interval: every {config['snapshot_interval']} epochs",
        f"  Random seed: {config['random_seed']}",
        "",
        "Dataset profile:",
        f"  Name: {dataset_profile.get('name', 'unknown')}",
        f"  Description: {dataset_profile.get('description', 'n/a')}",
        f"  Pixel range: {tuple(dataset_profile.get('pixel_range', [0.0, 1.0]))}",
        "",
        "Session behavior:",
        "  1) Sample synthetic real-image batches each epoch.",
        "  2) Train discriminator to separate real and generated images.",
        "  3) Train generator to fool discriminator.",
        "  4) Track GAN losses and a quality heuristic over epochs.",
        "  5) Save generated sample grid and learning plots.",
    ]
    return "\n".join(lines)


def format_run_report(summary: dict) -> str:
    """Return formatted session report for display.

    Parameters:
        summary (dict): Complete session summary.

    Returns:
        str: Formatted multi-line report.
    """
    lines = ["", "Session summary:"]
    lines.append(f"  Status: {summary.get('status', 'unknown')}")

    config = summary.get("config", {})
    lines.append(f"  Training epochs: {config.get('epochs', 0)}")

    base_result = summary.get("base_result", {})
    metrics = base_result.get("metrics", {})
    sample_stats = base_result.get("sample_stats", {})

    lines.extend(
        [
            f"  Final discriminator loss: {metrics.get('final_d_loss', 0.0):.4f}",
            f"  Final generator loss: {metrics.get('final_g_loss', 0.0):.4f}",
            f"  Mean quality (last 20 epochs): {metrics.get('mean_quality_last_20', 0.0):.3f}",
            f"  Max quality observed: {metrics.get('max_quality', 0.0):.3f}",
            f"  Final D(real) mean: {metrics.get('final_d_real_mean', 0.0):.3f}",
            f"  Final D(fake) mean: {metrics.get('final_d_fake_mean', 0.0):.3f}",
            "  Final sample statistics:",
            f"    Mean pixel intensity: {sample_stats.get('final_generated_mean', 0.0):.3f}",
            f"    Pixel std deviation: {sample_stats.get('final_generated_std', 0.0):.3f}",
            f"    Snapshots saved: {sample_stats.get('num_snapshots', 0)}",
            "  Saved plots: data/runs/gan_losses.png, data/runs/quality_curve.png",
            "  Saved sample grid: data/runs/generated_samples_grid.png",
            "Saved run artifact: data/runs/latest_gan_demo.json",
            "",
        ]
    )
    return "\n".join(lines)


def format_message(message: str) -> str:
    """Format a user-facing message string.

    Parameters:
        message (str): Raw message text.

    Returns:
        str: Prefixed message string.
    """
    return f"[GAN Demo] {message}"
