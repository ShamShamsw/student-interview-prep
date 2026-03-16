"""
main.py - Entry point for Podcasting Voice-To-Text Pipeline
===========================================================

Thin-controller module that only orchestrates calls to:
    - operations.py for workflow execution
    - display.py for presentation formatting
"""

from display import format_header, format_run_report, format_startup_guide
from models import create_project_config
from operations import load_default_keywords, run_core_flow


def main() -> None:
    """Run one complete voice-to-text pipeline session.

    Returns:
        None
    """
    config = create_project_config()
    keywords = load_default_keywords()
    print(format_header())
    print(format_startup_guide(config, keywords))
    run_summary = run_core_flow(config=config, keywords=keywords)
    print(format_run_report(run_summary))


if __name__ == "__main__":
    # Guard keeps imports side-effect free for tests and reuse.
    main()
