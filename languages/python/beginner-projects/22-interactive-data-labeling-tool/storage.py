"""
storage.py - Persistence layer for Project 22: Interactive Data Labeling Tool
==============================================================================

Handles:
    - Loading/generating text samples for annotation
    - Saving and loading session state as JSON (for resumability)
    - Exporting completed annotations to CSV
    - File I/O and directory management
"""

from pathlib import Path
import json
import csv
from datetime import datetime
from typing import Dict, List, Optional

DATA_DIR = Path(__file__).resolve().parent / 'data'
SESSIONS_DIR = DATA_DIR / 'sessions'
EXPORTS_DIR = DATA_DIR / 'exports'

# Synthetic headlines used when no source file is provided.
_SYNTHETIC_SAMPLES = [
    "Scientists discover breakthrough treatment for rare disease",
    "Stock market crashes amid rising inflation fears",
    "Local team wins championship after decade-long drought",
    "Government announces new climate policy targets",
    "Tech giant lays off thousands of employees",
    "Community rallies to support flood victims",
    "New study links social media use to anxiety in teens",
    "Record-breaking heatwave sweeps across the continent",
    "Startup raises $100 million in Series B funding",
    "Historic peace agreement signed between rival nations",
    "Wildfire forces thousands to evacuate their homes",
    "Researchers develop biodegradable plastic alternative",
    "Central bank raises interest rates for third time this year",
    "Award-winning film breaks box office records worldwide",
    "City council approves new public transit expansion plan",
    "Outbreak of rare virus reported in three countries",
    "Volunteer program transforms lives in underserved communities",
    "Inflation hits 40-year high, consumers feel the squeeze",
    "Mountain rescue team saves stranded hikers",
    "New renewable energy plant powers 50,000 homes",
]


def ensure_data_dirs() -> None:
    """Create local data, sessions, and exports directories if they do not exist.

    Returns:
        None
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_or_generate_samples(
    source: Optional[str] = None,
    n_samples: int = 20,
) -> List[str]:
    """Load text samples from a file or generate a synthetic set.

    Parameters:
        source (str | None): Path to a plain-text file (one sample per line).
            If None or the file is not found, synthetic samples are used.
        n_samples (int): Number of synthetic samples to use when no file is given.

    Returns:
        list[str]: Ordered list of text samples ready for annotation.

    Design note:
        Falling back to synthetic data means the tool is runnable immediately
        without external files — important for beginners exploring the project.

    TODO: Implement file loading with fallback to synthetic samples
    """
    pass


def load_session(session_file: str) -> dict:
    """Load an existing annotation session from JSON.

    Parameters:
        session_file (str): Filename (not full path) of the session JSON.

    Returns:
        dict: Session dictionary with 'config', 'samples', and 'annotations' keys.
              Returns an empty dict if the file does not exist.

    TODO: Implement JSON deserialization with missing-file handling
    """
    pass


def save_session(session_file: str, session: dict) -> None:
    """Persist the current session state to JSON.

    Parameters:
        session_file (str): Filename (not full path) for the session JSON.
        session (dict): Full session dictionary to serialize.

    Returns:
        None

    Design note:
        Saving after every annotation ensures no progress is lost if the
        program crashes. The overhead is negligible for small datasets.

    TODO: Implement JSON serialization with ensure_data_dirs guard
    """
    pass


def export_csv(
    export_path: str,
    samples: List[str],
    annotations: Dict[str, dict],
) -> int:
    """Export labeled annotations to a CSV file.

    Parameters:
        export_path (str): Filename (not full path) for the CSV output.
        samples (list[str]): Full list of text samples (indexed from 0).
        annotations (dict): Mapping of sample index (str) to annotation dict.

    Returns:
        int: Number of rows written to the CSV (excludes skipped/unlabeled).

    CSV columns:
        index, text, label, timestamp

    TODO: Implement CSV writing using the csv module
    """
    pass


def session_filename_for_today() -> str:
    """Return a session filename based on today's date.

    Returns:
        str: Filename string like 'session_20260316.json'.
    """
    return f"session_{datetime.now().strftime('%Y%m%d')}.json"


def export_filename_for_today() -> str:
    """Return an export CSV filename based on today's date.

    Returns:
        str: Filename string like 'labeled_dataset_20260316.csv'.
    """
    return f"labeled_dataset_{datetime.now().strftime('%Y%m%d')}.csv"
