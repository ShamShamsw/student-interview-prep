"""
main.py - Entry point for Project 23: Network Analysis of Social Graphs
=======================================================================

Thin-controller module that only orchestrates calls to:
    - operations.py for the analysis pipeline
    - display.py for presentation formatting
    - storage.py for data persistence
    - models.py for configuration and data models
"""

import time
from display import format_header, format_startup_guide, format_run_report
from models import create_project_config
from operations import load_graph_profile, run_core_flow
from storage import ensure_data_dirs


def main() -> None:
    """Run one complete network analysis session.

    Workflow:
        1. Ensure data directories exist
        2. Print header banner
        3. Load configuration and graph profile
        4. Print startup guide
        5. Run analysis pipeline (operations.run_core_flow)
        6. Print the final analysis report

    Returns:
        None

    TODO: Implement main orchestration
    """
    # Ensure data directories exist before any file operations.
    ensure_data_dirs()

    # Print session header.
    print(format_header())

    # Build analysis configuration.
    config = create_project_config()

    # Load graph profile for startup display.
    profile = load_graph_profile()

    # Print startup guide.
    print(format_startup_guide(config, profile))

    # Run analysis pipeline.
    start_time = time.time()
    summary = run_core_flow()
    elapsed = time.time() - start_time
    summary['execution_time_seconds'] = elapsed

    # Print final report.
    print(format_run_report(summary))


if __name__ == "__main__":
    # Guard keeps imports side-effect free for tests and reuse.
    main()
