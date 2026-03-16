"""
main.py - Entry point for Topic Modeling And Visualization
==========================================================

This module is the thin controller layer.
It should coordinate execution and delegate business logic to operations.py
and formatting to display.py.
"""

from operations import run_full_pipeline
from display import format_header, format_run_report


def main() -> None:
    """
    Execute one complete topic modeling run.

    Flow:
        1. Print header.
        2. Run operations pipeline.
        3. Print report.
    """
    print(format_header())
    run_summary = run_full_pipeline()
    print(format_run_report(run_summary))


if __name__ == "__main__":
    # Guard: execute only when run directly from command line.
    # Importing this module from tests should not auto-start execution.
    main()
