"""
main.py - Entry point for Audio Feature Extraction And Classification
====================================================================

Thin-controller module that only orchestrates calls to:
    - operations.py for workflow execution
    - display.py for presentation formatting
"""

from display import format_header, format_run_report, format_startup_guide
from models import create_project_config
from operations import load_audio_label_specs, run_core_flow


def main() -> None:
    """Run one complete audio feature extraction and classification session.

    Returns:
        None
    """
    config = create_project_config()
    label_specs = load_audio_label_specs()
    print(format_header())
    print(format_startup_guide(config, label_specs))
    run_summary = run_core_flow(config=config, label_specs=label_specs)
    print(format_run_report(run_summary))


if __name__ == "__main__":
    # Guard keeps imports side-effect free for tests and reuse.
    main()
