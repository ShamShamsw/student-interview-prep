"""
main.py - Entry point for Real-Time Webcam Computer Vision Demos
================================================================

Thin-controller module that only orchestrates calls to:
    - operations.py for workflow execution
    - display.py for presentation formatting
"""

from display import format_header, format_run_report, format_startup_guide
from models import create_demo_config
from operations import load_demo_modes, run_core_flow


def main() -> None:
    """Run one complete webcam demo session.

    Returns:
        None
    """
    config = create_demo_config()
    modes = load_demo_modes()
    print(format_header())
    print(format_startup_guide(config, modes))
    run_summary = run_core_flow(config=config, modes=modes)
    print(format_run_report(run_summary))


if __name__ == "__main__":
    # Guard keeps imports side-effect free for tests and reuse.
    main()
