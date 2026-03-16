"""
display.py - Formatting helpers for summarization comparison output
===================================================================
"""


def format_header() -> str:
    """Return CLI banner for this project."""
    return (
        "=" * 55
        + "\n"
        + "  NLP TEXT SUMMARIZER DEMO - COMPARISON RUN\n"
        + "=" * 55
    )


def format_summary_block(title: str, payload: dict) -> str:
    """
    Format one summary result block.

    Parameters:
        title (str): Display title.
        payload (dict): Summary result object.

    Returns:
        str: Formatted text block.
    """
    lines = [
        title,
        f"  Word count: {payload['word_count']}",
        f"  Compression ratio: {payload['compression_ratio']:.3f}",
        f"  Text: {payload['text']}",
    ]
    return "\n".join(lines)


def format_metrics(metrics: dict) -> str:
    """
    Format comparison metrics section.

    Parameters:
        metrics (dict): Comparison metrics payload.

    Returns:
        str: Metric section string.
    """
    return "\n".join(
        [
            "Comparison metrics:",
            f"  Source words: {metrics['source_word_count']}",
            f"  Extractive overlap: {metrics['extractive_overlap']:.4f}",
            f"  Abstractive overlap: {metrics['abstractive_overlap']:.4f}",
        ]
    )


def format_run_report(run: dict) -> str:
    """
    Format full final report string.

    Parameters:
        run (dict): Run summary from operations.

    Returns:
        str: Multi-line formatted report.
    """
    lines = [
        "",
        "Configuration:",
        f"  Extractive sentences: {run['config']['extractive_sentences']}",
        f"  Abstractive max words: {run['config']['abstractive_max_words']}",
        "",
        format_summary_block("Extractive summary:", run["extractive"]),
        "",
        format_summary_block("Abstractive summary:", run["abstractive"]),
        "",
        format_metrics(run["metrics"]),
        "",
        "Saved artifact: data/runs/latest_summary_run.json",
    ]
    return "\n".join(lines)
