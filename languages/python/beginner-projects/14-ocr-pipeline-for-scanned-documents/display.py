"""
display.py - Formatting helpers for OCR document extraction output
=================================================================
"""


def format_header() -> str:
    """Return the CLI banner for this project.

    Returns:
        str: User-facing banner string.
    """
    return (
        "=" * 70
        + "\n"
        + "  OCR PIPELINE FOR SCANNED DOCUMENTS - TEXT EXTRACTION + MARKUP\n"
        + "=" * 70
    )


def format_startup_guide(config: dict, search_terms: list[str]) -> str:
    """Return startup guidance shown before the run begins.

    Parameters:
        config (dict): Runtime configuration.
        search_terms (list[str]): Key terms to highlight in extracted text.

    Returns:
        str: Multi-line startup guide.
    """
    lines = [
        "",
        "Configuration:",
        f"  Document input path: {config['document_input_path']}",
        f"  Max pages to process: {config['max_pages']}",
        f"  Max key sections: {config['max_key_sections']}",
        f"  Language hint: {config['language']}",
        "",
        "Search terms for extraction:",
        "  " + ", ".join(search_terms),
        "",
        "Processing behavior:",
        "  1) Attempt to extract text from local image documents if OCR dependencies are available.",
        "  2) Fall back to a demo document when OCR is unavailable or no input files found.",
    ]
    return "\n".join(lines)


def _format_key_sections(summary: dict) -> list[str]:
    """Return readable key sections for the run report.

    Parameters:
        summary (dict): Session summary payload.

    Returns:
        list[str]: Formatted key-section lines.
    """
    sections = summary.get("key_sections", [])
    if not sections:
        return ["  Key sections: none"]

    lines = ["  Key sections:"]
    for section in sections:
        lines.append(
            "    "
            f"Page {section['page_number']}: "
            f"score={section['score']:.2f} "
            f"terms={', '.join(section['matched_terms'])}"
        )
    return lines


def _format_term_frequencies(summary: dict) -> list[str]:
    """Return formatted term frequency lines for the run report.

    Parameters:
        summary (dict): Session summary payload.

    Returns:
        list[str]: Term frequency block lines.
    """
    term_freq = summary.get("term_frequencies", {})
    if not term_freq:
        return ["  Term frequencies: none"]

    top_items = sorted(term_freq.items(), key=lambda item: (-item[1], item[0]))
    top_items = top_items[:5]
    return [
        "  Term frequencies (top): "
        + ", ".join(f"{term}={count}" for term, count in top_items)
    ]


def format_run_report(summary: dict) -> str:
    """Format the final OCR pipeline report.

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
                "Saved run artifact: data/runs/latest_ocr_pipeline_run.json",
            ]
        )
        return "\n".join(lines)

    lines.extend(
        [
            f"  Status: {summary['status']}",
            f"  Document source: {summary['document_source']}",
            f"  Pages processed: {summary['total_pages']}",
            f"  Total text characters: {summary['total_characters']}",
            f"  Average page confidence: {summary['average_confidence']:.2%}",
        ]
    )
    lines.extend(_format_term_frequencies(summary))
    lines.extend(_format_key_sections(summary))
    lines.append("Saved run artifact: data/runs/latest_ocr_pipeline_run.json")
    return "\n".join(lines)
