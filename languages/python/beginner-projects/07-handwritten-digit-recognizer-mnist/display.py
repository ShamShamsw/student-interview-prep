"""
display.py - Output formatting for the MNIST project
====================================================

Display functions return strings so presentation remains separate from
core ML logic in operations.py.
"""


def format_header() -> str:
    """Return the project header banner string."""
    return (
        "=" * 55
        + "\n"
        + "  HANDWRITTEN DIGIT RECOGNIZER - BASELINE RUN\n"
        + "=" * 55
    )


def format_confusions(confusions: list) -> str:
    """
    Format top confusion pairs.

    Parameters:
        confusions (list[dict]): Confusion pair objects.

    Returns:
        str: Human-readable confusion summary.
    """
    if not confusions:
        return "Top confusion pairs:\n  (none)"

    lines = ["Top confusion pairs:"]
    for item in confusions:
        lines.append(
            f"  {item['true_label']} -> {item['predicted_label']} : {item['count']} samples"
        )
    return "\n".join(lines)


def format_run_summary(summary: dict) -> str:
    """
    Format the final run summary block.

    Parameters:
        summary (dict): Run summary from operations.run_full_pipeline.

    Returns:
        str: Multi-line report.
    """
    config = summary["config"]
    lines = [
        "",
        "Run configuration:",
        f"  Model: {config['model_name']}",
        f"  Test size: {config['test_size']}",
        f"  Random state: {config['random_state']}",
        "",
        "Evaluation:",
        f"  Accuracy: {summary['accuracy']:.4f}",
        f"  Train samples: {summary['train_size']}",
        f"  Test samples: {summary['test_size']}",
        "",
        format_confusions(summary["top_confusions"]),
        "",
        "Saved artifact: data/runs/latest_run.json",
    ]
    return "\n".join(lines)
