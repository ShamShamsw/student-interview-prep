"""
display.py - Formatting helpers for math tutoring output
========================================================
"""


def format_header() -> str:
    """Return the CLI banner for this project.

    Returns:
        str: User-facing banner string.
    """
    return (
        "=" * 70
        + "\n"
        + "  INTERACTIVE MATH TUTOR - SYMBOLIC PROBLEM SOLVING + EXPLANATIONS\n"
        + "=" * 70
    )


def format_startup_guide(config: dict, difficulty_levels: list[dict]) -> str:
    """Return startup guidance shown before the session begins.

    Parameters:
        config (dict): Runtime configuration.
        difficulty_levels (list[dict]): Available difficulty levels.

    Returns:
        str: Multi-line startup guide.
    """
    lines = [
        "",
        "Configuration:",
        f"  Session difficulty: {config['difficulty_level']}",
        f"  Problems to solve: {config['num_problems']}",
        f"  Problem categories: {', '.join(config['categories'])}",
        f"  Show step-by-step: {config['show_steps']}",
        "",
        "Available difficulty levels:",
    ]

    for level in difficulty_levels:
        lines.append(f"  - {level['name']}: {level['description']}")

    lines.extend(
        [
            "",
            "Session behavior:",
            "  1) Generate symbolic math problems at your chosen difficulty.",
            "  2) Solve each problem and provide step-by-step explanations.",
            "  3) Track accuracy, time-to-solve, and learning progress.",
        ]
    )
    return "\n".join(lines)


def _format_performance_stats(summary: dict) -> list[str]:
    """Return readable performance statistics for the run report.

    Parameters:
        summary (dict): Session summary payload.

    Returns:
        list[str]: Formatted performance lines.
    """
    stats = summary.get("performance_stats", {})
    if not stats:
        return ["  Performance: no data"]

    return [
        f"  Accuracy: {stats['accuracy']:.1%}",
        f"  Average solve time: {stats['avg_time_seconds']:.1f}s",
        f"  Total session time: {stats['total_time_seconds']:.1f}s",
    ]


def _format_category_breakdown(summary: dict) -> list[str]:
    """Return formatted category breakdown for the run report.

    Parameters:
        summary (dict): Session summary payload.

    Returns:
        list[str]: Category breakdown lines.
    """
    breakdown = summary.get("category_breakdown", {})
    if not breakdown:
        return ["  Category breakdown: none"]

    lines = ["  Category breakdown:"]
    for category, stats in sorted(breakdown.items()):
        lines.append(
            f"    {category}: "
            f"{stats['correct']}/{stats['total']} correct "
            f"({stats['accuracy']:.0%})"
        )
    return lines


def format_run_report(summary: dict) -> str:
    """Format the final math tutoring session report.

    Parameters:
        summary (dict): Persisted session summary from operations.py.

    Returns:
        str: User-facing session summary.
    """
    lines = ["", "Session summary:"]

    if summary.get("status") != "completed":
        lines.extend(
            [
                f"  Status: {summary.get('status', 'failed')}",
                "  Check dependencies and project requirements, then run again.",
                "Saved run artifact: data/runs/latest_math_tutor_session.json",
            ]
        )
        return "\n".join(lines)

    lines.extend(
        [
            "  Status: completed",
            f"  Difficulty: {summary['difficulty_level']}",
            f"  Problems completed: {summary['problems_completed']}/{summary['problems_attempted']}",
        ]
    )
    lines.extend(_format_performance_stats(summary))
    lines.extend(_format_category_breakdown(summary))
    lines.append("Saved run artifact: data/runs/latest_math_tutor_session.json")
    return "\n".join(lines)
