"""
models.py - Data constructors for OCR document extraction session artifacts
===========================================================================
"""

from datetime import datetime


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp.

    Returns:
        str: Timestamp string with trailing Z.
    """
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def create_project_config(
    document_input_path: str = "data/input/sample_document.png",
    max_pages: int = 50,
    max_key_sections: int = 3,
    language: str = "eng",
) -> dict:
    """Create the default runtime configuration.

    Parameters:
        document_input_path (str): Image file or folder path for OCR input.
        max_pages (int): Maximum document pages to process.
        max_key_sections (int): Maximum key sections to extract.
        language (str): Language code for OCR engine.

    Returns:
        dict: Configuration payload.
    """
    return {
        "document_input_path": document_input_path,
        "max_pages": int(max_pages),
        "max_key_sections": int(max_key_sections),
        "language": language,
        "created_at": _utc_timestamp(),
    }


def create_extracted_page(
    page_number: int,
    source_file: str,
    text: str,
    character_count: int,
    confidence: float | None = None,
) -> dict:
    """Create one page extraction record with OCR metadata.

    Parameters:
        page_number (int): Document page number (1-indexed).
        source_file (str): Source image file name.
        text (str): Extracted text content.
        character_count (int): Number of characters extracted.
        confidence (float | None): Optional OCR confidence estimate.

    Returns:
        dict: Extracted page payload.
    """
    payload = {
        "page_number": int(page_number),
        "source_file": source_file,
        "text": text.strip(),
        "character_count": int(character_count),
    }
    if confidence is not None:
        payload["confidence"] = round(float(confidence), 4)
    return payload


def create_key_section(
    page_number: int,
    text_snippet: str,
    matched_terms: list[str],
    score: float,
) -> dict:
    """Create one key section highlight from extracted document content.

    Parameters:
        page_number (int): Document page containing the section.
        text_snippet (str): Extracted text excerpt.
        matched_terms (list[str]): Matched search terms in the snippet.
        score (float): Ranking score for prioritization.

    Returns:
        dict: Key section payload.
    """
    return {
        "page_number": int(page_number),
        "text_snippet": text_snippet.strip(),
        "matched_terms": sorted(set(matched_terms)),
        "score": round(float(score), 4),
    }


def create_run_summary(
    config: dict,
    total_pages: int,
    total_characters: int,
    average_confidence: float,
    document_source: str,
    term_frequencies: dict[str, int],
    key_sections: list[dict],
    page_preview: list[dict],
    status: str,
) -> dict:
    """Create the persistable summary for one OCR pipeline session.

    Parameters:
        config (dict): Runtime configuration.
        total_pages (int): Number of document pages processed.
        total_characters (int): Total extracted characters.
        average_confidence (float): Average OCR confidence across pages.
        document_source (str): Source type for document processing.
        term_frequencies (dict[str, int]): Search term frequency table.
        key_sections (list[dict]): Ranked key section snippets.
        page_preview (list[dict]): Short page extraction preview.
        status (str): Session outcome indicator.

    Returns:
        dict: Session summary payload.
    """
    return {
        "config": config,
        "total_pages": int(total_pages),
        "total_characters": int(total_characters),
        "average_confidence": round(float(average_confidence), 4),
        "document_source": document_source,
        "term_frequencies": dict(term_frequencies),
        "key_sections": list(key_sections),
        "page_preview": list(page_preview),
        "status": status,
        "saved_at": _utc_timestamp(),
    }
