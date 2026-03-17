"""
display.py - Presentation helpers for Project 22: Interactive Data Labeling Tool
================================================================================

Formats:
    - Session header banner
    - Startup guide with configuration and resume info
    - Per-sample annotation prompt with label legend
    - Live progress display
    - Annotation review table
    - Final session summary with label distribution
"""

from typing import Dict, List, Any


def format_header() -> str:
    """Return a formatted banner for the labeling session.

    Returns:
        str: ASCII header with title and separator lines.

    Design note:
        A consistent header helps users immediately identify the tool and
        its current action without reading a wall of text.

    TODO: Implement header with decorative separators (70-char wide)
    """
    pass


def format_startup_guide(config: Dict[str, Any], session: Dict[str, Any]) -> str:
    """Format the startup/configuration block shown at session start.

    Parameters:
        config (dict): Session configuration from models.create_session_config.
        session (dict): Current session (may contain existing annotations).

    Returns:
        str: Formatted startup info showing label set, file paths, and
             how many annotations were resumed from a previous session.

    TODO: Implement configuration display with resume indicator
    """
    pass


def format_sample_prompt(
    sample_idx: int,
    total: int,
    text: str,
    label_set: List[str],
) -> str:
    """Format the per-sample annotation prompt.

    Parameters:
        sample_idx (int): Zero-based sample index.
        total (int): Total number of samples.
        text (str): The sample text to display.
        label_set (list[str]): Allowed label strings.

    Returns:
        str: Formatted block showing sample number, text, and label legend.

    Example output:
        ──────────────────────────────────────────────────
        Sample #13 of 50
        ──────────────────────────────────────────────────

          "Scientists discover breakthrough treatment"

        Labels:  [P] positive   [N] negative   [U] neutral
                 [S] skip       [R] review all  [Q] quit

    TODO: Implement prompt formatting with label shortcuts
    """
    pass


def format_progress(session: Dict[str, Any]) -> str:
    """Format a single-line progress display.

    Parameters:
        session (dict): Current session dictionary.

    Returns:
        str: Progress string, e.g.:
            'Progress: 13 / 50 labeled  |  2 skipped  |  35 remaining'

    TODO: Implement progress line using create_progress_summary
    """
    pass


def format_review_table(session: Dict[str, Any]) -> str:
    """Format a table of all current annotations for review.

    Parameters:
        session (dict): Current session dictionary.

    Returns:
        str: ASCII table with columns: #, Text (truncated), Label, Skipped, Time.

    TODO: Implement table with aligned columns and truncated text
    """
    pass


def format_session_summary(session: Dict[str, Any], export_path: str) -> str:
    """Format the final session completion summary.

    Parameters:
        session (dict): Completed or quit session dictionary.
        export_path (str): Path where the CSV was saved.

    Returns:
        str: Formatted summary showing totals, label distribution, and file paths.

    TODO: Implement summary with label distribution percentages
    """
    pass


def format_run_report(session: Dict[str, Any]) -> str:
    """Format a brief end-of-session report.

    Parameters:
        session (dict): Final session dictionary.

    Returns:
        str: End-of-session report string.

    TODO: Delegate to format_session_summary with appropriate export_path
    """
    pass
