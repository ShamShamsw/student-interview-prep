"""main.py - Entry point for Project 40: Real-Time Collaborative Notebook Demo."""

from display import format_header, format_run_report, format_startup_guide
from models import create_notebook_config
from operations import load_collab_profile, run_core_flow
from storage import ensure_data_dirs


def main() -> None:
    """Run one complete collaborative notebook simulation session."""
    ensure_data_dirs()
    print(format_header())

    config = create_notebook_config()
    profile = load_collab_profile()
    print(format_startup_guide(config, profile))

    summary = run_core_flow()
    print(format_run_report(summary))


if __name__ == '__main__':
    main()
