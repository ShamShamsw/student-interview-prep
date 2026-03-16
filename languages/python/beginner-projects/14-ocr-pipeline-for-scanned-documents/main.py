"""
main.py - Entry point for OCR Pipeline For Scanned Documents
========================================================

Thin-controller module that only orchestrates calls to:
    - operations.py for workflow execution
    - display.py for presentation formatting
"""

from display import format_header, format_run_report, format_startup_guide
from models import create_project_config
from operations import load_default_search_terms, run_core_flow


def main() -> None:
    """Run one complete OCR pipeline session.

    Returns:
        None
    """
    config = create_project_config()
    search_terms = load_default_search_terms()
    print(format_header())
    print(format_startup_guide(config, search_terms))
    run_summary = run_core_flow(config=config, search_terms=search_terms)
    print(format_run_report(run_summary))


if __name__ == "__main__":
    # Guard keeps imports side-effect free for tests and reuse.
    main()
