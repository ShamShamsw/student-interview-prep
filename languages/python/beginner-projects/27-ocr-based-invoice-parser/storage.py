"""
storage.py - Persistence layer for Project 27: OCR-Based Invoice Parser
=======================================================================

Handles:
    - Local data directory setup
    - Invoice image file discovery and loading
    - JSON parsed invoice persistence and loading
    - Extraction logs and OCR text cache persistence
    - Parsing summary export
"""

from pathlib import Path
import json

DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUTS_DIR = DATA_DIR / "outputs"


def ensure_data_dirs() -> None:
    """Create local data and outputs directories if missing.

    Returns:
        None
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def get_invoice_files(input_directory: str) -> list:
    """Discover all invoice image files in the input directory.

    Parameters:
        input_directory (str): Path to directory containing invoice images.

    Returns:
        list: Paths to all invoice files (JPEG, PNG, PDF).

    TODO: Implement file discovery using pathlib.glob() for image extensions.
    """
    pass


def save_parsed_invoices(filename: str, invoices: list) -> None:
    """Persist parsed invoice records to JSON in the data directory.

    Parameters:
        filename (str): Output JSON filename (e.g., 'parsed_invoices.json').
        invoices (list): List of parsed invoice record dicts to serialize.

    Returns:
        None

    TODO: Implement JSON serialization with indentation to DATA_DIR / filename.
    """
    pass


def load_parsed_invoices(filename: str) -> list:
    """Load previously saved parsed invoice records from the data directory.

    Parameters:
        filename (str): JSON filename to load.

    Returns:
        list: Previously saved invoice records, or empty list if file is missing.

    TODO: Implement JSON load from DATA_DIR / filename with fallback for missing files.
    """
    pass


def save_extraction_summary(filename: str, summary: dict) -> None:
    """Save the extraction summary as JSON in the outputs directory.

    Parameters:
        filename (str): Output JSON filename (e.g., 'extraction_summary.json').
        summary (dict): Summary record to serialize.

    Returns:
        None

    TODO: Implement JSON serialization with indentation to OUTPUTS_DIR / filename.
    """
    pass


def save_ocr_cache(filename: str, cache: dict) -> None:
    """Save cached OCR text extracts as JSON in the outputs directory.

    Parameters:
        filename (str): Output JSON filename (e.g., 'ocr_cache.json').
        cache (dict): Mapping of invoice filename to extracted OCR text.

    Returns:
        None

    TODO: Implement JSON serialization with indentation to OUTPUTS_DIR / filename.
    """
    pass


def load_json(filename: str):
    """Load JSON data from the data directory.

    Parameters:
        filename (str): JSON filename in the data directory.

    Returns:
        object: Parsed JSON content, or empty list if the file is missing.
    """
    ensure_data_dirs()
    path = DATA_DIR / filename
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))
