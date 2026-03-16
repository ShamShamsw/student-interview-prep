"""
storage.py - Persistence helpers for math tutoring session artifacts
===================================================================
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
RUNS_DIR = DATA_DIR / "runs"

LATEST_SESSION = RUNS_DIR / "latest_math_tutor_session.json"
SESSION_HISTORY = RUNS_DIR / "math_tutor_session_history.json"


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


def save_latest_session(session: dict) -> None:
    """Save the latest math tutoring session and append to history.

    Parameters:
        session (dict): Persistable session summary payload.

    Returns:
        None
    """
    ensure_storage_dirs()
    _write_json(LATEST_SESSION, session)

    history = _read_json(SESSION_HISTORY, default=[])
    history.append(session)
    _write_json(SESSION_HISTORY, history)


def load_latest_session() -> dict:
    """Load the most recent math tutoring session artifact.

    Returns:
        dict: Latest saved session payload or an empty dict.
    """
    ensure_storage_dirs()
    return _read_json(LATEST_SESSION, default={})
