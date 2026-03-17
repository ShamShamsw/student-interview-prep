"""Entry point for Project 42: Hand-Pose Sign Language Classifier."""

from display import format_header, format_run_report, format_startup_guide
from models import create_classifier_config
from operations import load_classifier_profile, run_core_flow
from storage import ensure_data_dirs


def main() -> None:
    """Run one complete hand-pose capture, training, and live inference session."""
    ensure_data_dirs()
    print(format_header())

    config = create_classifier_config()
    profile = load_classifier_profile()
    print(format_startup_guide(config, profile))

    summary = run_core_flow()
    print(format_run_report(summary))


if __name__ == '__main__':
    main()
