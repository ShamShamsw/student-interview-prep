"""
models.py - Data models for Project 22: Interactive Data Labeling Tool
======================================================================

Defines:
    - Session configuration (label set, file paths, dataset info)
    - Annotation records (sample index, text, label, timestamp, skipped flag)
    - Session state container
    - Progress summary structure
"""

from datetime import datetime
from typing import Dict, List, Optional, Any


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp.

    Returns:
        str: Timestamp string with trailing Z.
    """
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def create_session_config(
    label_set: Optional[List[str]] = None,
    session_name: Optional[str] = None,
    dataset_source: Optional[str] = None,
    n_samples: int = 20,
) -> Dict[str, Any]:
    """Create the default configuration for a labeling session.

    Parameters:
        label_set (list[str] | None): Allowed label strings.
            Defaults to ['positive', 'negative', 'neutral'].
        session_name (str | None): Session file stem used for saving/loading.
            Defaults to a date-based name.
        dataset_source (str | None): Path to a plain-text sample file.
            None means synthetic samples are generated.
        n_samples (int): Number of samples when using synthetic generation.

    Returns:
        dict: Configuration dictionary with all session settings.

    TODO: Implement configuration creation with sensible defaults
    """
    pass


def create_annotation(
    sample_idx: int,
    text: str,
    label: str,
    skipped: bool = False,
) -> Dict[str, Any]:
    """Create a single annotation record for one labeled sample.

    Parameters:
        sample_idx (int): Zero-based index of the sample in the samples list.
        text (str): The raw text of the sample.
        label (str): The assigned label string.
        skipped (bool): True if this sample was skipped rather than labeled.

    Returns:
        dict: Annotation record with keys:
            - sample_idx: int
            - text: str
            - label: str
            - skipped: bool
            - timestamp: ISO-8601 UTC string

    TODO: Implement annotation record creation
    """
    pass


def create_session(config: Dict[str, Any], samples: List[str]) -> Dict[str, Any]:
    """Create a new empty session ready for annotation.

    Parameters:
        config (dict): Session configuration from create_session_config.
        samples (list[str]): Ordered list of text samples to label.

    Returns:
        dict: Session dictionary with keys:
            - config: dict
            - samples: list[str]
            - annotations: dict  (sample_idx as string key → annotation dict)
            - created_at: ISO-8601 timestamp
            - updated_at: ISO-8601 timestamp

    Design note:
        Annotations are stored as a dict keyed by string index (not a list)
        so that gaps (skipped/unlabeled samples) are trivially handled
        without keeping placeholder entries.

    TODO: Implement session creation
    """
    pass


def create_progress_summary(session: Dict[str, Any]) -> Dict[str, Any]:
    """Compute progress counts from the current session state.

    Parameters:
        session (dict): Current session dictionary.

    Returns:
        dict: Progress summary with keys:
            - total: int — total samples
            - labeled: int — annotated and not skipped
            - skipped: int — skipped samples
            - remaining: int — not yet touched
            - completion_pct: float — labeled / total * 100
            - label_counts: dict — {label_string: count}

    TODO: Implement progress calculation
    """
    pass
