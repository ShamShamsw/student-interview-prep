"""
storage.py - Persistence layer for Project 26: Cryptocurrency Real-Time Tracker
================================================================================

Handles:
    - Local data directory setup
    - JSON tick history persistence and loading
    - Run summary persistence
    - Plotly price chart export
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


def save_ticks(filename: str, ticks: list) -> None:
    """Persist tick records to JSON in the data directory.

    Parameters:
        filename (str): Output JSON filename (e.g., 'ticks.json').
        ticks (list): List of tick record dicts to serialize.

    Returns:
        None

    TODO: Implement JSON serialization with indentation to DATA_DIR / filename.
    """
    pass


def load_ticks(filename: str) -> list:
    """Load previously saved tick records from the data directory.

    Parameters:
        filename (str): JSON filename to load.

    Returns:
        list: Previously saved tick records, or empty list if file is missing.

    TODO: Implement JSON load from DATA_DIR / filename with fallback for missing files.
    """
    pass


def save_run_summary(filename: str, summary: dict) -> None:
    """Save the final run summary as JSON in the outputs directory.

    Parameters:
        filename (str): Output JSON filename (e.g., 'run_summary.json').
        summary (dict): Run summary record to serialize.

    Returns:
        None

    TODO: Implement JSON serialization with indentation to OUTPUTS_DIR / filename.
    """
    pass


def save_price_chart(filename: str, fig) -> None:
    """Export a Plotly figure as an interactive HTML file in the outputs directory.

    Parameters:
        filename (str): Output HTML filename (e.g., 'price_chart.html').
        fig: Plotly Figure object to export.

    Returns:
        None

    TODO: Implement fig.write_html() to OUTPUTS_DIR / filename.
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

