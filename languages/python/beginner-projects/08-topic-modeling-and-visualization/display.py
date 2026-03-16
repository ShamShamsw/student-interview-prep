"""
display.py - Reporting and formatting helpers for topic modeling output
======================================================================
"""


def format_header() -> str:
    """Return CLI header banner."""
    return (
        "=" * 55
        + "\n"
        + "  TOPIC MODELING AND VISUALIZATION - RUN\n"
        + "=" * 55
    )


def format_topics(title: str, topics: list) -> str:
    """
    Format topic list section.

    Parameters:
        title (str): Section title.
        topics (list[dict]): Topic entries.

    Returns:
        str: Human-readable topic section.
    """
    lines = [title]
    if not topics:
        lines.append("  (no topics)")
        return "\n".join(lines)

    for topic in topics:
        words = ", ".join(topic["top_words"])
        lines.append(f"  Topic {topic['topic_id']}: {words}")
    return "\n".join(lines)


def format_dominant_topic_summary(dominant_topics: list, preview_count: int = 5) -> str:
    """
    Format a short preview of document dominant topics.

    Parameters:
        dominant_topics (list[dict]): Document-topic assignments.
        preview_count (int): Number of rows to show.

    Returns:
        str: Dominant-topic preview section.
    """
    lines = ["Dominant topic preview:"]
    for row in dominant_topics[:preview_count]:
        lines.append(
            f"  Doc {row['doc_index']}: topic {row['dominant_topic']} (score={row['score']:.4f})"
        )
    if not dominant_topics:
        lines.append("  (no documents)")
    return "\n".join(lines)


def format_run_report(summary: dict) -> str:
    """
    Format full run report.

    Parameters:
        summary (dict): Run summary object.

    Returns:
        str: Multi-line report.
    """
    config = summary["config"]
    lines = [
        "",
        f"Corpus size: {summary['corpus_size']}",
        f"Vocabulary size: {summary['vocabulary_size']}",
        "",
        "Configuration:",
        f"  Topics: {config['num_topics']}",
        f"  Max features: {config['max_features']}",
        f"  Random state: {config['random_state']}",
        "",
        format_topics("Top NMF topics:", summary["nmf_topics"]),
        "",
        format_topics("Top LDA topics:", summary["lda_topics"]),
        "",
        format_dominant_topic_summary(summary["dominant_topics"]),
        "",
        "Saved artifact: data/runs/latest_topics.json",
    ]
    return "\n".join(lines)
