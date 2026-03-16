"""
storage.py - Persistence layer for Project 33: Plagiarism Similarity Detector
"""

from pathlib import Path
import json

DATA_DIR = Path(__file__).resolve().parent / 'data'


def ensure_data_dir() -> None:
    """Create local data directory if it does not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_json(filename: str):
    """Load JSON data from the local data directory."""
    ensure_data_dir()
    path = DATA_DIR / filename
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding='utf-8'))


def save_json(filename: str, data) -> None:
    """Save JSON data to the local data directory."""
    ensure_data_dir()
    path = DATA_DIR / filename
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')
