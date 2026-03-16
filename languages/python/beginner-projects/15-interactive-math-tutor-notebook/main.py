"""
main.py - Entry point for Interactive Math Tutor Notebook
========================================================

Thin-controller module that only orchestrates calls to:
    - operations.py for workflow execution
    - display.py for presentation formatting
"""

from display import format_header, format_run_report, format_startup_guide
from models import create_project_config
from operations import load_difficulty_levels, run_core_flow


def main() -> None:
    """Run one complete math tutoring session.

    Returns:
        None
    """
    config = create_project_config()
    difficulty_levels = load_difficulty_levels()
    print(format_header())
    print(format_startup_guide(config, difficulty_levels))
    run_summary = run_core_flow(config=config, difficulty_levels=difficulty_levels)
    print(format_run_report(run_summary))


if __name__ == "__main__":
    # Guard keeps imports side-effect free for tests and reuse.
    main()
