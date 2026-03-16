"""
storage.py - Persistence helpers for OCR document extraction artifacts
=====================================================================
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
RUNS_DIR = DATA_DIR / "runs"

LATEST_RUN = RUNS_DIR / "latest_ocr_pipeline_run.json"
RUN_HISTORY = RUNS_DIR / "ocr_pipeline_run_history.json"
LATEST_EXTRACTIONS = RUNS_DIR / "latest_ocr_extracted_pages.json"


def ensure_storage_dirs() -> None:
    """Create required storage directories for this project.

    Returns:
        None
    """
    RUNS_DIR.mkdir(parents=True, exist_ok=True)


def _read_json(path: Path, default):
    """Read JSON from disk with a safe fallback.

    Parameters:
        path (Path): File path to read.
        default: Value returned when the file is missing or invalid.

    Returns:
        Any: Parsed JSON payload or the fallback value.
    """
    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def _write_json(path: Path, payload) -> None:
    """Write JSON payload in a readable format.

    Parameters:
        path (Path): Destination file path.
        payload: JSON-serializable object.

    Returns:
        None
    """
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def save_latest_run(run: dict) -> None:
    """Save the latest OCR pipeline run and append to history.

    Parameters:
        run (dict): Persistable session summary payload.

    Returns:
        None
    """
    ensure_storage_dirs()
    _write_json(LATEST_RUN, run)

    history = _read_json(RUN_HISTORY, default=[])
    history.append(run)
    _write_json(RUN_HISTORY, history)


def save_latest_extractions(pages: list[dict]) -> None:
    """Save full extracted pages for the latest run.

    Parameters:
        pages (list[dict]): Extracted page records for the session.

    Returns:
        None
    """
    ensure_storage_dirs()
    _write_json(LATEST_EXTRACTIONS, pages)


def load_latest_run() -> dict:
    """Load the most recent OCR pipeline artifact.

    Returns:
        dict: Latest saved run payload or an empty dict.
    """
    ensure_storage_dirs()
    return _read_json(LATEST_RUN, default={})
