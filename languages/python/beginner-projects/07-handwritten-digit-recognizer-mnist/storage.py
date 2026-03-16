"""
storage.py - Run artifact persistence for the MNIST project
===========================================================

This module stores evaluation summaries so training runs are reproducible
and comparable over time.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
RUNS_DIR = DATA_DIR / "runs"
LATEST_RUN = RUNS_DIR / "latest_run.json"
RUN_HISTORY = RUNS_DIR / "run_history.json"


def ensure_runs_dir() -> None:
    """
    Create data/runs if needed.

    Why this helper exists:
        Avoid repeating directory setup in every save/load function.
    """
    RUNS_DIR.mkdir(parents=True, exist_ok=True)


def _read_json(path: Path, default):
    """
    Read JSON from a file safely.

    Returns default value if file is missing or unreadable.
    """
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def _write_json(path: Path, payload) -> None:
    """Write JSON payload with stable formatting for readability."""
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def save_latest_run(summary: dict) -> None:
    """
    Save latest run summary and append to history.

    Parameters:
        summary (dict): Run summary object from models.create_run_summary.
    """
    ensure_runs_dir()
    _write_json(LATEST_RUN, summary)

    history = _read_json(RUN_HISTORY, default=[])
    history.append(summary)
    _write_json(RUN_HISTORY, history)


def load_latest_run() -> dict:
    """Load latest run summary, or empty dict if not found."""
    ensure_runs_dir()
    return _read_json(LATEST_RUN, default={})


def load_run_history() -> list:
    """Load all saved run summaries."""
    ensure_runs_dir()
    return _read_json(RUN_HISTORY, default=[])
