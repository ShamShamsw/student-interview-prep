"""
storage.py - Persistence helpers for summarization run artifacts
===============================================================
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
RUNS_DIR = DATA_DIR / "runs"
LATEST_RUN = RUNS_DIR / "latest_summary_run.json"
RUN_HISTORY = RUNS_DIR / "summary_run_history.json"


def ensure_runs_dir() -> None:
    """Ensure run artifact folder exists."""
    RUNS_DIR.mkdir(parents=True, exist_ok=True)


def _read_json(path: Path, default):
    """
    Read JSON from path with safe fallback.
    """
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def _write_json(path: Path, payload) -> None:
    """Write JSON payload with human-readable indentation."""
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def save_latest_run(run: dict) -> None:
    """
    Save latest run and append to run history.

    Parameters:
        run (dict): Run artifact payload.
    """
    ensure_runs_dir()
    _write_json(LATEST_RUN, run)

    history = _read_json(RUN_HISTORY, default=[])
    history.append(run)
    _write_json(RUN_HISTORY, history)


def load_latest_run() -> dict:
    """Load latest run artifact or empty dict if unavailable."""
    ensure_runs_dir()
    return _read_json(LATEST_RUN, default={})


def load_run_history() -> list:
    """Load all historical summarization runs."""
    ensure_runs_dir()
    return _read_json(RUN_HISTORY, default=[])
