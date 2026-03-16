"""
operations.py - Core NLP summarization workflow
==============================================

Implements:
    - text preprocessing
    - extractive summarization
    - abstractive summarization (optional model, fallback if unavailable)
    - basic overlap-based comparison metrics
    - run artifact persistence
"""

import importlib
import re
from collections import Counter

from models import (
    create_comparison_metrics,
    create_run_config,
    create_run_summary,
    create_summary_result,
)
from storage import save_latest_run


def load_sample_text() -> str:
    """
    Return a built-in sample document for local runs.

    Returns:
        str: Example source document.
    """
    return (
        "Natural language processing is a field of artificial intelligence that focuses "
        "on interactions between computers and human language. Modern NLP systems are "
        "used for translation, summarization, sentiment analysis, and question answering. "
        "As organizations process increasing amounts of unstructured text, summarization "
        "helps reduce reading time and highlights key points for faster decision-making. "
        "Extractive methods select important sentences directly from the source text, while "
        "abstractive methods generate new phrasing to condense ideas. Extractive systems are "
        "typically more faithful to source wording but can feel disjointed. Abstractive systems "
        "can be more fluent but may introduce factual errors if not carefully evaluated. "
        "In production settings, teams often combine automatic metrics with human review "
        "to balance precision, readability, and trustworthiness."
    )


def split_sentences(text: str) -> list[str]:
    """
    Split source text into rough sentence units.

    Parameters:
        text (str): Input text.

    Returns:
        list[str]: Sentence-like segments.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]


def tokenize_words(text: str) -> list[str]:
    """
    Tokenize text into lowercase words.

    Parameters:
        text (str): Input text.

    Returns:
        list[str]: Token list.
    """
    return re.findall(r"[a-zA-Z']+", text.lower())


def build_sentence_scores(sentences: list[str]) -> list[float]:
    """
    Score each sentence by aggregate token frequency.

    Parameters:
        sentences (list[str]): Sentence list.

    Returns:
        list[float]: Scores aligned with sentence index.

    Why this baseline:
        Frequency-based scoring is simple, transparent, and explainable.
    """
    all_tokens = tokenize_words(" ".join(sentences))
    token_counts = Counter(all_tokens)

    scores = []
    for sentence in sentences:
        sent_tokens = tokenize_words(sentence)
        if not sent_tokens:
            scores.append(0.0)
            continue
        score = sum(token_counts[t] for t in sent_tokens) / len(sent_tokens)
        scores.append(score)
    return scores


def generate_extractive_summary(text: str, max_sentences: int) -> str:
    """
    Generate extractive summary by selecting highest scoring sentences.

    Parameters:
        text (str): Source text.
        max_sentences (int): Number of sentences to keep.

    Returns:
        str: Extractive summary text.
    """
    sentences = split_sentences(text)
    if not sentences:
        return ""

    scores = build_sentence_scores(sentences)
    ranked = sorted(range(len(sentences)), key=lambda idx: scores[idx], reverse=True)
    selected = sorted(ranked[: max(1, max_sentences)])
    return " ".join(sentences[i] for i in selected)


def generate_abstractive_summary(text: str, max_words: int) -> str:
    """
    Generate abstractive summary.

    Parameters:
        text (str): Source text.
        max_words (int): Maximum words in summary.

    Returns:
        str: Abstractive-style summary.

    Behavior:
        Attempts transformer summarization if available; otherwise falls back
        to a compact heuristic summary so the project runs without heavy models.
    """
    try:
        transformers_module = importlib.import_module("transformers")
        pipeline = transformers_module.pipeline

        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        out = summarizer(text, max_length=max_words, min_length=30, do_sample=False)
        return out[0]["summary_text"].strip()
    except Exception:
        # Fallback keeps project runnable in constrained environments.
        sentences = split_sentences(text)
        fallback = " ".join(sentences[:2]).strip()
        words = fallback.split()
        return " ".join(words[:max_words])


def lexical_overlap(source: str, summary: str) -> float:
    """
    Compute simple lexical overlap ratio.

    Parameters:
        source (str): Source text.
        summary (str): Summary text.

    Returns:
        float: Ratio of unique summary words appearing in source.

    Note:
        This is a lightweight proxy metric, not a replacement for ROUGE.
    """
    source_tokens = set(tokenize_words(source))
    summary_tokens = set(tokenize_words(summary))
    if not summary_tokens:
        return 0.0
    return len(source_tokens.intersection(summary_tokens)) / len(summary_tokens)


def run_full_pipeline() -> dict:
    """
    Execute one end-to-end summarization comparison run.

    Returns:
        dict: Run summary object.
    """
    config = create_run_config()
    source = load_sample_text()
    source_word_count = len(tokenize_words(source))

    extractive_text = generate_extractive_summary(source, config["extractive_sentences"])
    abstractive_text = generate_abstractive_summary(source, config["abstractive_max_words"])

    extractive = create_summary_result("Extractive", extractive_text, source_word_count)
    abstractive = create_summary_result("Abstractive", abstractive_text, source_word_count)

    metrics = create_comparison_metrics(
        extractive_overlap=lexical_overlap(source, extractive_text),
        abstractive_overlap=lexical_overlap(source, abstractive_text),
        source_word_count=source_word_count,
    )

    run = create_run_summary(config, source, extractive, abstractive, metrics)
    save_latest_run(run)
    return run
