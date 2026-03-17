"""
main.py - Entry point for Project 32: Image Augmentation Playground
"""

from display import format_header, format_run_report, format_startup_guide
from models import create_playground_config
from operations import load_playground_profile, run_core_flow
from storage import ensure_data_dirs


def main() -> None:
    """Run one complete image augmentation playground session."""
    ensure_data_dirs()
    print(format_header())

    config = create_playground_config()
    profile = load_playground_profile()
    print(format_startup_guide(config, profile))

    summary = run_core_flow()
    print(format_run_report(summary))


if __name__ == '__main__':
    main()

