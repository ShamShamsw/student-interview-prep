"""Entry point for Project 44: Cryptography Toolkit And Visualizations."""

from display import format_header, format_run_report, format_startup_guide
from models import create_toolkit_config
from operations import load_toolkit_profile, run_core_flow
from storage import ensure_data_dirs


def main() -> None:
    """Run one complete cryptography toolkit lesson and benchmark session."""
    ensure_data_dirs()
    print(format_header())

    config = create_toolkit_config()
    profile = load_toolkit_profile()
    print(format_startup_guide(config, profile))

    summary = run_core_flow()
    print(format_run_report(summary))


if __name__ == '__main__':
    main()
