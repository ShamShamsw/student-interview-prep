# Beginner Project 27: OCR-Based Invoice Parser

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** OCR preprocessing, regex field extraction, line item parsing, confidence scoring, and JSON export

---

## Why This Project?

Processing scanned invoices at scale requires extracting structured data from unstructured images. Production OCR pipelines must handle image preprocessing, text recognition noise, regex-based field extraction, and line-item parsing with confidence scoring.

This project teaches a professional document extraction pipeline where you can:

- preprocess invoice images (crop, denoise, upscale) before OCR,
- extract text from scanned invoices using OCR (Tesseract via pytesseract),
- normalize and parse dates, amounts, and inventory fields robustly,
- apply regex rules to extract vendor, totals, and line items automatically,
- score extraction confidence by comparing detected fields against templates,
- validate extracted data against a schema,
- export parsed invoices to a consistent JSON structure,
- and persist all outputs and extraction logs to disk for later review.

---

## Separate Repository

You can also access this project in a separate repository:

[OCR-Based Invoice Parser Repository](https://github.com/ShamShamsw/ocr-based-invoice-parser.git)

---

## What You Will Build

You will build a command-line invoice parser that:

1. Accepts a directory of invoice images (JPEG, PNG, PDF).
2. Preprocesses each image for optimal OCR performance.
3. Extracts raw text using Tesseract OCR.
4. Applies regex rules to extract vendor, invoice date, due date, and totals.
5. Parses line items (description, quantity, unit price, amount).
6. Scores extraction confidence for each detected field.
7. Validates extracted data against a schema.
8. Exports parsed invoices to JSON with metadata.
9. Prints an extraction report showing vendor, totals, line count, and confidence.
10. Persists parsed invoices and extraction summary to disk.

---

## Requirements

- Python 3.11+
- `pytesseract` (requires Tesseract-OCR system installation)
- `pillow`
- `regex`
- `spacy`

Install with:

```bash
pip install -r requirements.txt
```

Note: Tesseract-OCR must be installed separately from https://github.com/UB-Mannheim/tesseract/wiki

---

## Example Session

```text
======================================================================
   OCR-BASED INVOICE PARSER
======================================================================

Configuration:
   Input directory:   data/invoices/
   OCR engine:        Tesseract
   Confidence threshold: 0.75
   Output format:     JSON

Startup:
   Data directory:    data/
   Outputs directory: data/outputs/
   Previously parsed: 0 invoices

Processing invoices:
   [LOADED]  data/invoices/invoice_001.jpg    format=JPEG   size=2480x3507 px

OCR & Extraction (invoice_001.jpg):
   Raw text length:    2847 chars
   Vendor:             ACME Corp (confidence=0.92)
   Invoice Date:       2024-03-15 (confidence=0.88)
   Due Date:           2024-04-14 (confidence=0.85)
   Subtotal:           $1,250.00 (confidence=0.98)
   Tax:                $100.00 (confidence=0.91)
   Total:              $1,350.00 (confidence=0.96)
   Line Items:         5 detected

Line Items:
   Item        Quantity   Unit Price   Amount      Confidence
   Widget A       10      $50.00       $500.00     0.94
   Widget B       20      $25.00       $500.00     0.93
   Service X      5       $30.00       $150.00     0.89
   Discount       1      -$100.00     -$100.00    0.87
   Tax             -          -        $100.00     0.91

Validation:
   [PASS]  Schema validation succeeded
   [PASS]  Sum of line items matches total
   [PASS]  Required fields present

Summary:
   Invoices processed:     1
   Extraction rate:        100%
   Average confidence:     0.92
   Total amount extracted: $1,350.00

Artifacts saved:
   Parsed invoices:   data/parsed_invoices.json
   Extraction logs:   data/outputs/extraction_summary.json
   OCR text cache:    data/outputs/ocr_cache.json
```
