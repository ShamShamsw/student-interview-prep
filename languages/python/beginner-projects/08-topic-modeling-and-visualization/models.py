"""
models.py - Data constructors for topic modeling artifacts
==========================================================

This project uses dictionary-based records for readability and easy JSON
serialization. Use explicit constructor functions to keep a stable schema.
"""

from datetime import datetime


def create_run_config(
    num_topics: int = 5,
    max_features: int = 1000,
    random_state: int = 42,
) -> dict:
    """
    Create run configuration for topic modeling.

    Parameters:
        num_topics (int): Number of topics to extract.
        max_features (int): Vocabulary cap for vectorizer.
        random_state (int): Seed for deterministic behavior.

    Returns:
        dict: Run configuration object.
    """
    return {
        "num_topics": int(num_topics),
        "max_features": int(max_features),
        "random_state": int(random_state),
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }


def create_topic(topic_id: int, top_words: list[str], model_name: str) -> dict:
    """
    Create a topic record.

    Parameters:
        topic_id (int): Topic index.
        top_words (list[str]): Top terms for this topic.
        model_name (str): Source model name, e.g., NMF or LDA.

    Returns:
        dict: Topic summary object.
    """
    return {
        "topic_id": int(topic_id),
        "top_words": list(top_words),
        "model_name": model_name,
    }


def create_document_topic(doc_index: int, dominant_topic: int, score: float) -> dict:
    """
    Create a dominant-topic summary for one document.

    Parameters:
        doc_index (int): Document index in corpus.
        dominant_topic (int): Strongest topic assignment.
        score (float): Dominance score (relative weight/probability).

    Returns:
        dict: Document-topic summary entry.
    """
    return {
        "doc_index": int(doc_index),
        "dominant_topic": int(dominant_topic),
        "score": float(score),
    }


def create_run_summary(
    config: dict,
    corpus_size: int,
    vocabulary_size: int,
    nmf_topics: list,
    lda_topics: list,
    dominant_topics: list,
) -> dict:
    """
    Build persisted run summary object.

    Returns:
        dict: Aggregate summary for reporting and persistence.
    """
    return {
        "config": config,
        "corpus_size": int(corpus_size),
        "vocabulary_size": int(vocabulary_size),
        "nmf_topics": nmf_topics,
        "lda_topics": lda_topics,
        "dominant_topics": dominant_topics,
        "saved_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
