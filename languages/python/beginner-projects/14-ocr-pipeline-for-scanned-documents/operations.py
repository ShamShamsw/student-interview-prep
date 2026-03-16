"""
operations.py - Core OCR document extraction workflow
====================================================

Implements:
    - optional single/multi-page image OCR with pytesseract
    - deterministic demo document fallback when OCR is unavailable
    - text extraction with character counts and confidence metrics
    - term frequency indexing for document search
    - key section extraction and run artifact persistence
"""

from __future__ import annotations

import re
from pathlib import Path

from models import (
    create_extracted_page,
    create_key_section,
    create_project_config,
    create_run_summary,
)
from storage import save_latest_extractions, save_latest_run


def _load_optional_ocr_dependency():
    """Load pytesseract lazily for optional image OCR.

    Returns:
        module | None: pytesseract module or None when unavailable.
    """
    try:
        import pytesseract

        return pytesseract
    except ImportError:
        return None


def load_default_search_terms() -> list[str]:
    """Return default document search terms.

    Returns:
        list[str]: Terms used for indexing and key section extraction.
    """
    return [
        "date",
        "total",
        "amount",
        "signature",
        "approved",
        "received",
        "invoice",
    ]


def _normalize_text(value: str) -> str:
    """Normalize text for case-insensitive token matching.

    Parameters:
        value (str): Input text.

    Returns:
        str: Lowercased alphanumeric text with normalized spaces.
    """
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", value.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def _character_count(text: str) -> int:
    """Count characters in free-form text.

    Parameters:
        text (str): Input text.

    Returns:
        int: Character count including whitespace.
    """
    return len(text)


def _create_demo_pages() -> list[dict]:
    """Create a deterministic document used when OCR is unavailable.

    Returns:
        list[dict]: Demo document pages with extracted text.
    """
    demo_pages = [
        "Invoice #INV-2024-001 Date: January 15, 2024 Bill To: Customer Inc. Address: 123 Main Street Amount Due: $1,250.00 Description: Professional services rendered.",
        "Services and Hourly Breakdown January 3-5 2024: Design consultation 5 hrs at $75/hr. Development and testing 12 hrs at $85/hr. Project review and approval meeting 2 hrs at $65/hr.",
        "Total Amount Due: $1,250.00 Payment Terms: Net 30 days. Please remit payment to: Acme Corp Finance Dept. Authorized by: John Smith Signature approved and received.",
    ]

    pages = []
    for index, text in enumerate(demo_pages, start=1):
        pages.append(
            create_extracted_page(
                page_number=index,
                source_file="demo_document.pdf",
                text=text,
                character_count=_character_count(text),
                confidence=0.95,
            )
        )
    return pages


def _extract_images_with_pytesseract(image_paths: list[Path]) -> list[dict]:
    """Extract text from image files using pytesseract.

    Parameters:
        image_paths (list[Path]): Paths to image files (PNG, JPG, etc).

    Returns:
        list[dict]: Extracted page records; empty when OCR fails.
    """
    pytesseract = _load_optional_ocr_dependency()
    if pytesseract is None:
        return []

    from PIL import Image

    pages = []
    for page_num, image_path in enumerate(image_paths, start=1):
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
        except Exception:
            text = ""

        if text.strip():
            pages.append(
                create_extracted_page(
                    page_number=page_num,
                    source_file=image_path.name,
                    text=text,
                    character_count=_character_count(text),
                    confidence=0.88,
                )
            )

    return pages


def _count_term_frequencies(pages: list[dict], search_terms: list[str]) -> dict[str, int]:
    """Count search term frequencies across extracted pages.

    Parameters:
        pages (list[dict]): Extracted page records.
        search_terms (list[str]): Search terms to index.

    Returns:
        dict[str, int]: Term occurrence table.
    """
    counts = {term: 0 for term in search_terms}
    for page in pages:
        normalized = " " + _normalize_text(page["text"]) + " "
        for term in search_terms:
            token = f" {term.lower()} "
            counts[term] += normalized.count(token)
    return counts


def _extract_key_sections(
    pages: list[dict], search_terms: list[str], max_sections: int
) -> list[dict]:
    """Extract ranked key document sections based on term matches.

    Parameters:
        pages (list[dict]): Extracted page records.
        search_terms (list[str]): Search terms to highlight.
        max_sections (int): Maximum sections to return.

    Returns:
        list[dict]: Ranked key section payloads.
    """
    ranked = []

    for page in pages:
        text = page["text"]
        normalized = " " + _normalize_text(text) + " "
        matched = [term for term in search_terms if f" {term.lower()} " in normalized]

        if not matched:
            continue

        snippet = text[:200] if len(text) > 200 else text
        score = float(len(matched) * 2 + len(page["text"]) / 500.0)
        ranked.append(
            create_key_section(
                page_number=page["page_number"],
                text_snippet=snippet,
                matched_terms=matched,
                score=score,
            )
        )

    ranked.sort(key=lambda item: (-item["score"], item["page_number"]))
    return ranked[:max_sections]


def run_core_flow(config: dict | None = None, search_terms: list[str] | None = None) -> dict:
    """Execute OCR document extraction and save a run artifact.

    Parameters:
        config (dict | None): Optional runtime configuration override.
        search_terms (list[str] | None): Optional search term list override.

    Returns:
        dict: Persisted session summary.
    """
    runtime_config = config or create_project_config()
    active_terms = search_terms or load_default_search_terms()

    input_path = Path(runtime_config["document_input_path"])
    extracted_pages = []
    document_source = "demo_document"
    status = "completed_with_fallback"

    image_paths = []
    if input_path.exists():
        if input_path.is_file() and input_path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            image_paths = [input_path]
        elif input_path.is_dir():
            image_paths = sorted(
                list(input_path.glob("*.png")) + list(input_path.glob("*.jpg")) + list(input_path.glob("*.jpeg"))
            )

    if image_paths:
        extracted_pages = _extract_images_with_pytesseract(
            image_paths[: runtime_config["max_pages"]]
        )
        if extracted_pages:
            document_source = "image_files"
            status = "completed"

    if not extracted_pages:
        extracted_pages = _create_demo_pages()

    extracted_pages = extracted_pages[: runtime_config["max_pages"]]
    total_characters = sum(page["character_count"] for page in extracted_pages)
    avg_confidence = (
        sum(page.get("confidence", 0.0) for page in extracted_pages) / len(extracted_pages)
        if extracted_pages
        else 0.0
    )
    term_frequencies = _count_term_frequencies(extracted_pages, active_terms)
    key_sections = _extract_key_sections(
        pages=extracted_pages,
        search_terms=active_terms,
        max_sections=runtime_config["max_key_sections"],
    )

    summary = create_run_summary(
        config=runtime_config,
        total_pages=len(extracted_pages),
        total_characters=total_characters,
        average_confidence=avg_confidence,
        document_source=document_source,
        term_frequencies=term_frequencies,
        key_sections=key_sections,
        page_preview=extracted_pages[:2],
        status=status,
    )
    save_latest_extractions(extracted_pages)
    save_latest_run(summary)
    return summary
