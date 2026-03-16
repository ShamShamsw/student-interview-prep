"""
main.py - Entry point for Project 17: Bayesian Modeling Tutorial
================================================================

Thin-controller module that only orchestrates calls to:
    - operations.py for workflow execution
    - display.py for presentation formatting
"""

from display import format_header, format_run_report, format_startup_guide
from models import create_project_config
from operations import load_prior_presets, run_core_flow


def main() -> None:
    """Run one complete Bayesian inference session.

    Returns:
        None
    """
    config = create_project_config()
    presets = load_prior_presets()
    print(format_header())
    print(format_startup_guide(config, presets))
    run_summary = run_core_flow(config=config)
    print(format_run_report(run_summary))


if __name__ == "__main__":
    # Guard keeps imports side-effect free for tests and reuse.
    main()
