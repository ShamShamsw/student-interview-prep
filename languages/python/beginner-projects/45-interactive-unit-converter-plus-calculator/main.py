"""Entry point for Project 45: Interactive Unit Converter Plus Calculator."""

from display import format_header, format_run_report, format_startup_guide
from models import create_converter_config
from operations import load_converter_profile, run_core_flow
from storage import ensure_data_dirs


def main() -> None:
    """Run one complete unit-conversion and calculator lesson session."""
    ensure_data_dirs()
    print(format_header())

    config = create_converter_config()
    profile = load_converter_profile()
    print(format_startup_guide(config, profile))

    summary = run_core_flow()
    print(format_run_report(summary))


if __name__ == '__main__':
    main()
