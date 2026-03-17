"""
display.py - Output formatting for Image Segmentation Interactive Demo
=====================================================================

Provides:
    - CLI banners and headers
    - Configuration display
    - Segmentation training report formatting
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
        + "  IMAGE SEGMENTATION INTERACTIVE DEMO - NUMPY ENCODER-DECODER\n"
        + "=" * 70
    )


def format_startup_guide(config: dict, dataset_profile: dict) -> str:
    """Return startup guidance shown before segmentation training begins.

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
        f"  Train samples: {config['train_samples']}",
        f"  Validation samples: {config['val_samples']}",
        f"  Hidden dimension: {config['hidden_dim']}",
        f"  Bottleneck dimension: {config['bottleneck_dim']}",
        f"  Epochs: {config['epochs']}",
        f"  Batch size: {config['batch_size']}",
        f"  Learning rate: {config['learning_rate']}",
        f"  Snapshot interval: every {config['snapshot_interval']} epochs",
        f"  Random seed: {config['random_seed']}",
        "",
        "Dataset profile:",
        f"  Name: {dataset_profile.get('name', 'unknown')}",
        f"  Description: {dataset_profile.get('description', 'n/a')}",
        f"  Pixel range: {tuple(dataset_profile.get('pixel_range', [0.0, 1.0]))}",
        f"  Mask labels: {tuple(dataset_profile.get('mask_labels', [0, 1]))}",
        "",
        "Session behavior:",
        "  1) Generate synthetic grayscale images with binary masks.",
        "  2) Train a tiny encoder-decoder to predict segmentation masks.",
        "  3) Track train/validation BCE loss each epoch.",
        "  4) Track IoU, Dice score, and pixel accuracy on validation data.",
        "  5) Save learning plots and segmentation prediction panels.",
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
            f"  Final train loss: {metrics.get('final_train_loss', 0.0):.4f}",
            f"  Final validation loss: {metrics.get('final_val_loss', 0.0):.4f}",
            f"  Mean IoU (last 20 epochs): {metrics.get('mean_iou_last_20', 0.0):.3f}",
            f"  Max IoU observed: {metrics.get('max_iou', 0.0):.3f}",
            f"  Final Dice score: {metrics.get('final_dice', 0.0):.3f}",
            f"  Final pixel accuracy: {metrics.get('final_pixel_accuracy', 0.0):.3f}",
            "  Final sample statistics:",
            f"    Predicted foreground ratio: {sample_stats.get('predicted_foreground_ratio', 0.0):.3f}",
            f"    Ground-truth foreground ratio: {sample_stats.get('ground_truth_foreground_ratio', 0.0):.3f}",
            f"    Samples visualized: {sample_stats.get('samples_visualized', 0)}",
            "  Saved plots: data/runs/segmentation_losses.png, data/runs/segmentation_quality.png",
            "  Saved sample grid: data/runs/segmentation_samples_grid.png",
            "Saved run artifact: data/runs/latest_segmentation_demo.json",
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
    return f"[Segmentation Demo] {message}"
