"""
display.py - Formatting helpers for podcast voice-to-text output
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
        + "  PODCASTING VOICE-TO-TEXT PIPELINE - SEARCHABLE TRANSCRIPTS\n"
        + "=" * 70
    )


def format_startup_guide(config: dict, keywords: list[str]) -> str:
    """Return startup guidance shown before the run begins.

    Parameters:
        config (dict): Runtime configuration.
        keywords (list[str]): Keywords tracked for highlights.

    Returns:
        str: Multi-line startup guide.
    """
    lines = [
        "",
        "Configuration:",
        f"  Audio input path: {config['audio_input_path']}",
        f"  Chunk duration: {config['chunk_duration_seconds']} seconds",
        f"  Max transcript segments: {config['max_segments']}",
        f"  Max highlights: {config['max_highlights']}",
        "",
        "Tracked keywords:",
        "  " + ", ".join(keywords),
        "",
        "Processing behavior:",
        "  1) Attempt to transcribe local WAV audio if dependencies are available.",
        "  2) Fall back to an included demo episode script when transcription is unavailable.",
    ]
    return "\n".join(lines)


def _format_top_keywords(summary: dict) -> list[str]:
    """Return readable keyword hit lines for the run report.

    Parameters:
        summary (dict): Session summary payload.

    Returns:
        list[str]: Formatted keyword-stat lines.
    """
    keyword_hits = summary.get("keyword_hits", {})
    if not keyword_hits:
        return ["  Keyword hits: none"]

    top_items = sorted(keyword_hits.items(), key=lambda item: (-item[1], item[0]))
    top_items = top_items[:5]
    return [
        "  Keyword hits (top): "
        + ", ".join(f"{keyword}={count}" for keyword, count in top_items)
    ]


def _format_highlights(summary: dict) -> list[str]:
    """Return formatted highlight lines for the run report.

    Parameters:
        summary (dict): Session summary payload.

    Returns:
        list[str]: Highlight block lines.
    """
    highlights = summary.get("highlights", [])
    if not highlights:
        return ["  Highlights: none"]

    lines = ["  Highlights:"]
    for highlight in highlights:
        lines.append(
            "    "
            f"[{highlight['start_seconds']:.1f}s-{highlight['end_seconds']:.1f}s] "
            f"score={highlight['score']:.2f} "
            f"keywords={', '.join(highlight['keywords'])}"
        )
    return lines


def format_run_report(summary: dict) -> str:
    """Format the final voice-to-text pipeline report.

    Parameters:
        summary (dict): Persisted session summary from operations.py.

    Returns:
        str: User-facing session summary.
    """
    lines = ["", "Run summary:"]

    if summary.get("status") not in {"completed", "completed_with_fallback"}:
        lines.extend(
            [
                f"  Status: {summary.get('status', 'failed')}",
                "  Check dependencies and project requirements, then run again.",
                "Saved run artifact: data/runs/latest_podcast_transcription_run.json",
            ]
        )
        return "\n".join(lines)

    lines.extend(
        [
            f"  Status: {summary['status']}",
            f"  Transcript source: {summary['transcript_source']}",
            f"  Segments captured: {summary['total_segments']}",
            f"  Total words: {summary['total_words']}",
            f"  Transcript duration: {summary['duration_seconds']:.1f} seconds",
        ]
    )
    lines.extend(_format_top_keywords(summary))
    lines.extend(_format_highlights(summary))
    lines.append("Saved run artifact: data/runs/latest_podcast_transcription_run.json")
    return "\n".join(lines)
