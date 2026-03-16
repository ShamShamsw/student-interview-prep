"""
display.py - Formatting helpers for webcam demo output
======================================================
"""


def format_header() -> str:
    """Return the CLI banner for this project.

    Returns:
        str: User-facing banner string.
    """
    return (
        "=" * 63
        + "\n"
        + "  REAL-TIME WEBCAM COMPUTER VISION DEMOS - LIVE MODES\n"
        + "=" * 63
    )


def format_startup_guide(config: dict, modes: list[dict]) -> str:
    """Return startup guidance shown before the webcam loop begins.

    Parameters:
        config (dict): Runtime configuration.
        modes (list[dict]): Supported webcam demo modes.

    Returns:
        str: Multi-line startup guide.
    """
    lines = [
        "",
        "Startup configuration:",
        f"  Camera index: {config['camera_index']}",
        f"  Frame size: {config['frame_width']}x{config['frame_height']}",
        f"  Initial mode: {config['initial_mode']}",
        "",
        "Available modes:",
    ]

    for mode in modes:
        lines.append(
            f"  [{mode['hotkey']}] {mode['label']} - {mode['description']}"
        )

    lines.extend(
        [
            "",
            "Controls:",
            "  Press 1-4 to switch modes.",
            "  Press Q or ESC to quit and save the session summary.",
        ]
    )
    return "\n".join(lines)


def _format_last_metrics(summary: dict) -> list[str]:
    """Format the most recent frame metrics for the session report.

    Parameters:
        summary (dict): Session summary payload.

    Returns:
        list[str]: Report lines for the latest metrics.
    """
    recent_metrics = summary.get("recent_metrics", [])
    if not recent_metrics:
        return ["  Last detection count: 0", "  Last tracked regions: 0"]

    latest_metrics = recent_metrics[-1]
    return [
        f"  Last detection count: {latest_metrics['detection_count']}",
        f"  Last tracked regions: {latest_metrics['tracked_regions']}",
    ]


def format_run_report(summary: dict) -> str:
    """Format the final webcam session report.

    Parameters:
        summary (dict): Persisted session summary from operations.py.

    Returns:
        str: User-facing session summary.
    """
    lines = ["", "Session summary:"]

    if not summary.get("camera_opened", False):
        lines.extend(
            [
                "  Camera opened: no",
                "  Status: camera unavailable",
                "  Check whether another app is using the webcam or camera permissions are blocked.",
                "Saved run artifact: data/runs/latest_webcam_demo_run.json",
            ]
        )
        return "\n".join(lines)

    visited_modes = ", ".join(summary.get("visited_modes", [])) or "preview"
    lines.extend(
        [
            "  Camera opened: yes",
            f"  Frames processed: {summary['frames_processed']}",
            f"  Average FPS: {summary['average_fps']:.2f}",
            f"  Modes visited: {visited_modes}",
            f"  Exit reason: {summary['exit_reason']}",
        ]
    )
    lines.extend(_format_last_metrics(summary))
    lines.append("Saved run artifact: data/runs/latest_webcam_demo_run.json")
    return "\n".join(lines)
