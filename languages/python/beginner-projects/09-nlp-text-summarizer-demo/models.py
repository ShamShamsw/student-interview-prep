"""
models.py - Data constructors for summarization run artifacts
============================================================
"""

from datetime import datetime


def create_run_config(
    extractive_sentences: int = 3,
    abstractive_max_words: int = 120,
    random_state: int = 42,
) -> dict:
    """
    Create run configuration for summarization pipeline.

    Parameters:
        extractive_sentences (int): Number of sentences to keep in extractive mode.
        abstractive_max_words (int): Word limit for abstractive output.
        random_state (int): Reproducibility seed.

    Returns:
        dict: Run configuration.
    """
    return {
        "extractive_sentences": int(extractive_sentences),
        "abstractive_max_words": int(abstractive_max_words),
        "random_state": int(random_state),
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }


def create_summary_result(method: str, text: str, source_word_count: int) -> dict:
    """
    Create summary result record for one method.

    Parameters:
        method (str): Method name, e.g., Extractive or Abstractive.
        text (str): Summary text output.
        source_word_count (int): Original source length in words.

    Returns:
        dict: Summary result with compression ratio.
    """
    summary_words = len(text.split())
    ratio = 0.0
    if source_word_count > 0:
        ratio = summary_words / source_word_count

    return {
        "method": method,
        "text": text,
        "word_count": summary_words,
        "compression_ratio": ratio,
    }


def create_comparison_metrics(
    extractive_overlap: float,
    abstractive_overlap: float,
    source_word_count: int,
) -> dict:
    """
    Create metrics object for summary quality comparison.

    Parameters:
        extractive_overlap (float): Overlap score for extractive summary.
        abstractive_overlap (float): Overlap score for abstractive summary.
        source_word_count (int): Source text word count.

    Returns:
        dict: Comparison metrics object.
    """
    return {
        "source_word_count": int(source_word_count),
        "extractive_overlap": float(extractive_overlap),
        "abstractive_overlap": float(abstractive_overlap),
    }


def create_run_summary(config: dict, source_text: str, extractive: dict, abstractive: dict, metrics: dict) -> dict:
    """
    Create complete run summary payload.

    Returns:
        dict: Persistable run summary object.
    """
    return {
        "config": config,
        "source_text": source_text,
        "extractive": extractive,
        "abstractive": abstractive,
        "metrics": metrics,
        "saved_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
