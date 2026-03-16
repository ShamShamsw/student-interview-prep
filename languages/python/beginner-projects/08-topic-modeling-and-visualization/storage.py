"""
storage.py - Persistence layer for topic modeling run artifacts
==============================================================
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
RUNS_DIR = DATA_DIR / "runs"
LATEST_TOPICS = RUNS_DIR / "latest_topics.json"
TOPIC_HISTORY = RUNS_DIR / "topic_history.json"


def ensure_runs_dir() -> None:
    """Create the run artifact directory if missing."""
    RUNS_DIR.mkdir(parents=True, exist_ok=True)


def _read_json(path: Path, default):
    """
    Read JSON safely and return default if missing or invalid.
    """
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def _write_json(path: Path, payload) -> None:
    """Write JSON with stable formatting for readability."""
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def save_latest_run(summary: dict) -> None:
    """
    Save latest topic-modeling run and append to history.

    Parameters:
        summary (dict): Run summary object.
    """
    ensure_runs_dir()
    _write_json(LATEST_TOPICS, summary)

    history = _read_json(TOPIC_HISTORY, default=[])
    history.append(summary)
    _write_json(TOPIC_HISTORY, history)


def load_latest_run() -> dict:
    """Load latest saved run, or empty dict if none found."""
    ensure_runs_dir()
    return _read_json(LATEST_TOPICS, default={})


def load_run_history() -> list:
    """Load all saved topic-modeling runs."""
    ensure_runs_dir()
    return _read_json(TOPIC_HISTORY, default=[])
