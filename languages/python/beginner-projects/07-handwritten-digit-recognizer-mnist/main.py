"""
main.py - Entry point for the Handwritten Digit Recognizer project
==================================================================

This module handles user interaction and orchestration only.
It should stay thin:

    user intent -> main.py -> operations.py -> storage.py
                                |
                                +-> display.py for formatting output

main.py should not contain ML math or model training internals.
That logic belongs in operations.py so it is testable and reusable.
"""

from operations import run_full_pipeline
from display import format_header, format_run_summary


def main() -> None:
    """
    Run one complete training/evaluation cycle.

    Flow:
        1. Print a project header.
        2. Execute the ML pipeline in operations.py.
        3. Print the formatted summary report.

    Why this function is small:
        Keeping orchestration code separate from data science logic
        makes it easier to test and refactor each part independently.
    """
    # TODO: Add optional menu controls (train only, evaluate only, inspect runs).
    print(format_header())
    summary = run_full_pipeline()
    print(format_run_summary(summary))


if __name__ == "__main__":
    # Guard: run only when executed directly.
    # If imported from tests, main() does not auto-run.
    main()
