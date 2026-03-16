"""
main.py - Entry point for NLP Text Summarizer Demo
==================================================

Thin-controller module.
Responsibilities:
    - start pipeline
    - call formatting helpers
    - print final report

Non-responsibilities:
    - model logic
    - text preprocessing logic
    - persistence internals
"""

from operations import run_full_pipeline
from display import format_header, format_run_report


def main() -> None:
    """
    Run one full summarization comparison cycle.

    Flow:
        1. Print header
        2. Execute pipeline in operations.py
        3. Print report built by display.py
    """
    print(format_header())
    summary = run_full_pipeline()
    print(format_run_report(summary))


if __name__ == "__main__":
    # Guard: avoid side effects when imported from tests.
    main()
