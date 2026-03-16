"""
models.py - Data constructors for math tutoring session artifacts
=================================================================
"""

from datetime import datetime


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp.

    Returns:
        str: Timestamp string with trailing Z.
    """
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def create_project_config(
    difficulty_level: str = "beginner",
    num_problems: int = 5,
    categories: list[str] | None = None,
    show_steps: bool = True,
) -> dict:
    """Create the default runtime configuration.

    Parameters:
        difficulty_level (str): Problem difficulty (beginner, intermediate, advanced).
        num_problems (int): Number of problems to generate.
        categories (list[str] | None): Math topics to include.
        show_steps (bool): Whether to show step-by-step solutions.

    Returns:
        dict: Configuration payload.
    """
    return {
        "difficulty_level": difficulty_level,
        "num_problems": int(num_problems),
        "categories": list(categories or ["algebra", "geometry"]),
        "show_steps": bool(show_steps),
        "created_at": _utc_timestamp(),
    }


def create_difficulty_level(name: str, description: str, complexity: int) -> dict:
    """Create one difficulty level descriptor.

    Parameters:
        name (str): Level name (beginner, intermediate, advanced).
        description (str): Human-readable description.
        complexity (int): Complexity score for problem generation.

    Returns:
        dict: Difficulty level payload.
    """
    return {
        "name": name,
        "description": description,
        "complexity": int(complexity),
    }


def create_problem_record(
    problem_id: str,
    category: str,
    problem_text: str,
    correct_answer: str,
    user_answer: str | None = None,
    solved_correctly: bool | None = None,
    solve_time_seconds: float | None = None,
    steps: list[str] | None = None,
) -> dict:
    """Create one math problem record with solution metadata.

    Parameters:
        problem_id (str): Unique problem identifier.
        category (str): Problem category (algebra, geometry, etc).
        problem_text (str): Problem statement.
        correct_answer (str): Correct symbolic answer.
        user_answer (str | None): User's provided answer.
        solved_correctly (bool | None): Whether answer was correct.
        solve_time_seconds (float | None): Time taken to solve.
        steps (list[str] | None): Step-by-step explanation.

    Returns:
        dict: Problem record payload.
    """
    payload = {
        "problem_id": problem_id,
        "category": category,
        "problem_text": problem_text,
        "correct_answer": correct_answer,
    }
    if user_answer is not None:
        payload["user_answer"] = user_answer
    if solved_correctly is not None:
        payload["solved_correctly"] = solved_correctly
    if solve_time_seconds is not None:
        payload["solve_time_seconds"] = round(float(solve_time_seconds), 2)
    if steps:
        payload["steps"] = list(steps)
    return payload


def create_session_summary(
    config: dict,
    difficulty_level: str,
    problems_attempted: int,
    problems_completed: int,
    performance_stats: dict,
    category_breakdown: dict,
    problem_records: list[dict],
    status: str,
) -> dict:
    """Create the persistable summary for one tutoring session.

    Parameters:
        config (dict): Runtime configuration.
        difficulty_level (str): Session difficulty level.
        problems_attempted (int): Number of problems generated.
        problems_completed (int): Number of problems solved.
        performance_stats (dict): Aggregated performance metrics.
        category_breakdown (dict): Per-category statistics.
        problem_records (list[dict]): Problem solution records.
        status (str): Session outcome indicator.

    Returns:
        dict: Session summary payload.
    """
    return {
        "config": config,
        "difficulty_level": difficulty_level,
        "problems_attempted": int(problems_attempted),
        "problems_completed": int(problems_completed),
        "performance_stats": dict(performance_stats),
        "category_breakdown": dict(category_breakdown),
        "problem_records": list(problem_records),
        "status": status,
        "saved_at": _utc_timestamp(),
    }
