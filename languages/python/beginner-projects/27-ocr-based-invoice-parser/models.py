"""
models.py - Data models for Project 27: OCR-Based Invoice Parser
=================================================================

Defines:
    - Parser configuration (input directory, OCR engine, confidence threshold)
    - Invoice document records (vendor, dates, amounts, line items)
    - Line item records (description, quantity, unit price, amount)
    - Field extraction records (extracted value, regex pattern, confidence)
    - Validation result records (field name, is_valid, error_message)
    - Final parsing summary record for reporting and persistence
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string.

    Returns:
        str: UTC timestamp with trailing Z.
    """
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def create_parser_config(
    input_directory: str = "data/invoices/",
    ocr_engine: str = "Tesseract",
    confidence_threshold: float = 0.75,
    output_format: str = "JSON",
) -> Dict[str, Any]:
    """Create a default parser configuration record.

    Parameters:
        input_directory (str): Path to directory containing invoice images.
        ocr_engine (str): OCR engine label (e.g., 'Tesseract').
        confidence_threshold (float): Minimum confidence for field extraction (0.0-1.0).
        output_format (str): Output format label (e.g., 'JSON').

    Returns:
        dict: Configuration dictionary used throughout the parser pipeline.

    TODO: Implement configuration creation with default values and basic validation.
    """
    pass


def create_invoice_document(
    filename: str,
    vendor: Optional[str] = None,
    invoice_date: Optional[str] = None,
    due_date: Optional[str] = None,
    subtotal: Optional[float] = None,
    tax: Optional[float] = None,
    total: Optional[float] = None,
    line_items: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Create a normalized invoice document record.

    Parameters:
        filename (str): Source invoice filename (e.g., 'invoice_001.jpg').
        vendor (str | None): Extracted vendor/company name.
        invoice_date (str | None): Invoice date in ISO-8601 format (YYYY-MM-DD).
        due_date (str | None): Payment due date in ISO-8601 format.
        subtotal (float | None): Pre-tax amount.
        tax (float | None): Tax amount extracted or calculated.
        total (float | None): Final invoice total.
        line_items (list[dict] | None): List of line item records.

    Returns:
        dict: Normalized invoice record including a parsed_at timestamp.

    TODO: Implement invoice record creation with parsed_at timestamp from _utc_timestamp().
    """
    pass


def create_line_item(
    description: str,
    quantity: float,
    unit_price: float,
    amount: float,
    confidence: float = 0.0,
) -> Dict[str, Any]:
    """Create a normalized line item record.

    Parameters:
        description (str): Item description or SKU.
        quantity (float): Quantity ordered.
        unit_price (float): Price per unit.
        amount (float): Line total (quantity * unit_price).
        confidence (float): Extraction confidence score (0.0-1.0).

    Returns:
        dict: Normalized line item record.

    TODO: Implement line item record creation.
    """
    pass


def create_field_extraction(
    field_name: str,
    extracted_value: Any,
    regex_pattern: str,
    confidence: float,
) -> Dict[str, Any]:
    """Create a field extraction record documenting an extracted value.

    Parameters:
        field_name (str): Name of the field extracted (e.g., 'vendor', 'total').
        extracted_value (Any): The value extracted from OCR text.
        regex_pattern (str): Regex pattern used for extraction.
        confidence (float): Confidence score for this extraction (0.0-1.0).

    Returns:
        dict: Extraction record including a UTC extracted_at timestamp.

    TODO: Implement extraction record creation with extracted_at timestamp.
    """
    pass


def create_validation_result(
    field_name: str,
    is_valid: bool,
    error_message: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a validation result record for a parsed field.

    Parameters:
        field_name (str): Name of the field being validated.
        is_valid (bool): True if validation passed.
        error_message (str | None): Error description if validation failed.

    Returns:
        dict: Validation result record.

    TODO: Implement validation record creation.
    """
    pass


def create_parsing_summary(
    config: Dict[str, Any],
    invoices_processed: int,
    extraction_rate: float,
    avg_confidence: float,
    total_amount_extracted: float,
    artifacts: Dict[str, str],
) -> Dict[str, Any]:
    """Create the final parsing summary record.

    Parameters:
        config (dict): Parser configuration snapshot.
        invoices_processed (int): Number of invoices successfully parsed.
        extraction_rate (float): Percentage of invoices with successful extraction (0.0-1.0).
        avg_confidence (float): Average extraction confidence across all fields.
        total_amount_extracted (float): Sum of all extracted invoice totals.
        artifacts (dict): Saved output paths (parsed invoices, logs, cache).

    Returns:
        dict: Complete parsing summary for display and persistence including a
              UTC completed_at timestamp.

    TODO: Implement summary creation with timestamp from _utc_timestamp().
    """
    pass
