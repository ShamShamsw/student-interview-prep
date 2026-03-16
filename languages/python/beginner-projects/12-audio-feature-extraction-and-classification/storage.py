"""
storage.py - Persistence helpers for audio classification artifacts
=================================================================
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
RUNS_DIR = DATA_DIR / "runs"

LATEST_RUN = RUNS_DIR / "latest_audio_classification_run.json"
RUN_HISTORY = RUNS_DIR / "audio_classification_run_history.json"


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


def _json_default(value):
    """Convert non-native scalar/array values into JSON-compatible types.

    Parameters:
        value: Value that json.dumps cannot serialize natively.

    Returns:
        Any: Converted serializable value.
    """
    if hasattr(value, "item"):
        return value.item()
    if hasattr(value, "tolist"):
        return value.tolist()
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def _write_json(path: Path, payload) -> None:
    """Write JSON payload in a readable format.

    Parameters:
        path (Path): Destination file path.
        payload: JSON-serializable object.

    Returns:
        None
    """
    path.write_text(
        json.dumps(payload, indent=2, default=_json_default),
        encoding="utf-8",
    )


def save_latest_run(run: dict) -> None:
    """Save the latest training run and append to history.

    Parameters:
        run (dict): Persistable training summary payload.

    Returns:
        None
    """
    ensure_storage_dirs()
    _write_json(LATEST_RUN, run)

    history = _read_json(RUN_HISTORY, default=[])
    history.append(run)
    _write_json(RUN_HISTORY, history)


def load_latest_run() -> dict:
    """Load the most recent training artifact.

    Returns:
        dict: Latest saved run payload or an empty dict.
    """
    ensure_storage_dirs()
    return _read_json(LATEST_RUN, default={})
