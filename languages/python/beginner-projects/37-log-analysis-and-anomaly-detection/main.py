"""
main.py - Entry point for Project 37: Log Analysis And Anomaly Detection
"""

from display import format_header, format_run_report, format_startup_guide
from models import create_log_analyzer_config
from operations import load_analyzer_profile, run_core_flow
from storage import ensure_data_dirs


def main() -> None:
    """Run one complete log analysis session."""
    ensure_data_dirs()
    print(format_header())

    config = create_log_analyzer_config()
    profile = load_analyzer_profile()
    print(format_startup_guide(config, profile))

    summary = run_core_flow()
    print(format_run_report(summary))


if __name__ == '__main__':
    main()
