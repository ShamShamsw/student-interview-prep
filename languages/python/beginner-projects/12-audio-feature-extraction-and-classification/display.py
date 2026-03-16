"""
display.py - Formatting helpers for audio classification output
===============================================================
"""


def format_header() -> str:
    """Return the CLI banner for this project.

    Returns:
        str: User-facing banner string.
    """
    return (
        "=" * 70
        + "\n"
        + "  AUDIO FEATURE EXTRACTION AND CLASSIFICATION - MFCC + CHROMA + ML\n"
        + "=" * 70
    )


def format_startup_guide(config: dict, label_specs: list[dict]) -> str:
    """Return startup guidance shown before the run begins.

    Parameters:
        config (dict): Runtime configuration.
        label_specs (list[dict]): Supported synthetic classes.

    Returns:
        str: Multi-line startup guide.
    """
    lines = [
        "",
        "Configuration:",
        f"  Sample rate: {config['sample_rate']} Hz",
        f"  Clip duration: {config['clip_duration_seconds']:.1f} seconds",
        f"  Samples per label: {config['samples_per_label']}",
        f"  MFCC count: {config['n_mfcc']}",
        f"  FFT window: {config['n_fft']}",
        f"  Hop length: {config['hop_length']}",
        f"  Test split: {config['test_size']:.2f}",
        "",
        "Synthetic labels:",
    ]

    for spec in label_specs:
        lines.append(
            f"  - {spec['label']} ({spec['base_frequency_hz']:.1f} Hz): {spec['description']}"
        )

    return "\n".join(lines)


def _format_confusion_matrix(summary: dict) -> list[str]:
    """Return a readable confusion-matrix block.

    Parameters:
        summary (dict): Session summary payload.

    Returns:
        list[str]: Formatted confusion-matrix lines.
    """
    labels = summary.get("labels", [])
    matrix = summary.get("confusion_matrix", [])
    if not labels or not matrix:
        return ["  Confusion matrix: unavailable"]

    lines = ["  Confusion matrix (rows=true, cols=pred):"]
    lines.append("    labels: " + ", ".join(labels))
    for index, row in enumerate(matrix):
        lines.append(f"    {labels[index]}: {row}")
    return lines


def format_run_report(summary: dict) -> str:
    """Format the final training report.

    Parameters:
        summary (dict): Persisted session summary from operations.py.

    Returns:
        str: User-facing session summary.
    """
    lines = ["", "Run summary:"]

    if summary.get("status") != "completed":
        lines.extend(
            [
                f"  Status: {summary.get('status', 'failed')}",
                "  Check dependencies and project requirements, then run again.",
                "Saved run artifact: data/runs/latest_audio_classification_run.json",
            ]
        )
        return "\n".join(lines)

    lines.extend(
        [
            "  Status: completed",
            f"  Total samples: {summary['total_samples']}",
            f"  Train/Test split: {summary['train_samples']}/{summary['test_samples']}",
            f"  Feature vector size: {summary['feature_vector_size']}",
            f"  Accuracy: {summary['accuracy']:.4f}",
        ]
    )
    lines.extend(_format_confusion_matrix(summary))
    lines.append("Saved run artifact: data/runs/latest_audio_classification_run.json")
    return "\n".join(lines)
