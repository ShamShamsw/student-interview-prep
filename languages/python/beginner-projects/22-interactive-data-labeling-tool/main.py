"""
main.py - Entry point for Project 22: Interactive Data Labeling Tool
====================================================================

Thin-controller module that only orchestrates calls to:
    - operations.py for the interactive labeling workflow
    - display.py for presentation formatting
    - storage.py for data persistence
    - models.py for configuration and data models
"""

from display import format_header, format_startup_guide, format_run_report
from models import create_session_config
from operations import load_dataset_profile, run_core_flow
from storage import ensure_data_dirs


def main() -> None:
    """Run one complete interactive data labeling session.

    Workflow:
        1. Ensure data directories exist
        2. Print header banner
        3. Load configuration and dataset profile
        4. Print startup guide (shows resume info if prior session exists)
        5. Delegate to operations.run_core_flow for the interactive loop
        6. Print the final session report

    Returns:
        None

    TODO: Implement main orchestration
    """
    # Ensure data directories exist before any file operations.
    ensure_data_dirs()

    # Print session header.
    print(format_header())

    # Build session configuration.
    config = create_session_config()

    # Load dataset profile for display.
    profile = load_dataset_profile()

    # Print startup guide.
    # (startup_guide needs session for resume info — run_core_flow handles that)
    print(format_startup_guide(config, {}))

    # Run interactive labeling workflow.
    final_session = run_core_flow()

    # Print final report.
    print(format_run_report(final_session))


if __name__ == "__main__":
    # Guard keeps imports side-effect free for tests and reuse.
    main()
