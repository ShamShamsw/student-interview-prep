# Beginner Project 14: OCR Pipeline For Scanned Documents

**Time:** 3-5 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** image OCR, text extraction, document indexing, and structured artifact preservation

---

## Why This Project?

Converting paper documents to searchable text is a common task in many industries.
This project gives you a practical beginner workflow where you can:

- extract text from scanned document images,
- index documents for keyword-based retrieval,
- rank and extract key sections for quick review,
- and save reproducible run artifacts for audit and comparison.

---

## Separate Repository

You can also access this project in a separate repository:

[ocr pipeline for scanned documents Repository](https://github.com/ShamShamsw/ocr-pipeline-for-scanned-documents.git)

---

## What You Will Build

You will build a command-line OCR processing pipeline that:

1. Attempts to extract text from local image files (PNG, JPG) using Tesseract OCR.
2. Falls back to a deterministic demo document if OCR dependencies/images are unavailable.
3. Produces timestamped extracted page records with character counts.
4. Computes search-term hit counts across the full document.
5. Ranks and reports top key sections detected.
6. Saves run metadata and extracted page artifacts to JSON.

---

## Requirements

- Python 3.11+
- `pytesseract`
- `Pillow`
- Tesseract OCR engine (system-level dependency)

Install with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
  OCR PIPELINE FOR SCANNED DOCUMENTS - TEXT EXTRACTION + MARKUP
======================================================================

Configuration:
  Document input path: data/input/sample_document.png
  Max pages to process: 50
  Max key sections: 3
  Language hint: eng

Search terms for extraction:
  date, total, amount, signature, approved, received, invoice

Processing behavior:
  1) Attempt to extract text from local image documents if OCR dependencies are available.
  2) Fall back to a demo document when OCR is unavailable or no input files found.

Run summary:
  Status: completed_with_fallback
  Document source: demo_document
  Pages processed: 3
  Total text characters: 501
  Average page confidence: 95.00%
  Term frequencies (top): amount=2, approved=1, date=1, invoice=1, received=1
  Key sections:
    Page 3: score=10.33 terms=amount, approved, received, signature, total
    Page 1: score=6.32 terms=amount, date, invoice
Saved run artifact: data/runs/latest_ocr_pipeline_run.json
```

---

## Build Order

Follow this order for clean architecture:

1. `storage.py`
2. `models.py`
3. `operations.py`
4. `display.py`
5. `main.py`

---

## File Responsibilities

- `storage.py`: handles extracted-page and run artifact persistence in `data/runs/`.
- `models.py`: creates consistent payloads for configuration, extracted pages, key sections, and run summaries.
- `operations.py`: OCR/fallback logic, text extraction, term indexing, key-section ranking, and run persistence.
- `display.py`: formats a readable CLI banner, startup guide, and run summary.
- `main.py`: thin orchestration entry point.

---

## Suggested Reflection Prompts

Add answers in your own notes after running the project:

- Which search terms produced the most relevant key sections?
- How did extraction quality differ between real OCR and fallback/demo mode?
- What document preprocessing steps would improve OCR accuracy in production?

---

## Stretch Goals

1. Add document rotation/skew correction before OCR processing.
2. Extract tables and bounding boxes for visual element markup.
3. Support batch processing with directory input and multi-format output (Markdown, CSV).
4. Build a simple search interface for cross-document term lookup.
