"""
operations.py - Core math tutoring workflow
===========================================

Implements:
    - symbolic math problem generation at multiple difficulty levels
    - step-by-step solution explanation using symbolic algebra
    - performance tracking and category-based aggregation
    - session artifact persistence
"""

from __future__ import annotations

import random
from models import (
    create_difficulty_level,
    create_problem_record,
    create_project_config,
    create_session_summary,
)
from storage import save_latest_session


def _load_optional_sympy_dependency():
    """Load sympy lazily for symbolic math operations.

    Returns:
        module | None: sympy module or None when unavailable.
    """
    try:
        import sympy

        return sympy
    except ImportError:
        return None


def load_difficulty_levels() -> list[dict]:
    """Return available difficulty levels for math problems.

    Returns:
        list[dict]: Difficulty level descriptors.
    """
    return [
        create_difficulty_level(
            name="beginner",
            description="Basic arithmetic and simple algebraic equations",
            complexity=1,
        ),
        create_difficulty_level(
            name="intermediate",
            description="Quadratic equations and polynomial problems",
            complexity=2,
        ),
        create_difficulty_level(
            name="advanced",
            description="Systems of equations and calculus concepts",
            complexity=3,
        ),
    ]


def _generate_beginner_problem(problem_num: int) -> dict:
    """Generate a beginner-level algebra problem.

    Parameters:
        problem_num (int): Problem sequence number.

    Returns:
        dict: Problem with text and expected answer.
    """
    a = random.randint(2, 10)
    b = random.randint(5, 20)
    answer = b // a
    return {
        "category": "algebra",
        "text": f"Solve for x: {a}x = {b}",
        "answer": str(answer),
        "steps": [
            f"Given: {a}x = {b}",
            f"Divide both sides by {a}: x = {b}/{a}",
            f"Simplify: x = {answer}",
        ],
    }


def _generate_intermediate_problem(problem_num: int) -> dict:
    """Generate an intermediate-level quadratic problem.

    Parameters:
        problem_num (int): Problem sequence number.

    Returns:
        dict: Problem with text and expected answer.
    """
    a = random.randint(1, 3)
    b = random.randint(2, 8)
    c = random.randint(1, 6)
    return {
        "category": "algebra",
        "text": f"Solve: {a}x^2 + {b}x + {c} = 0",
        "answer": f"x = {(-b - (b**2 - 4*a*c)**0.5)/(2*a):.2f} or x = {(-b + (b**2 - 4*a*c)**0.5)/(2*a):.2f}",
        "steps": [
            f"Given: {a}x^2 + {b}x + {c} = 0",
            "Use quadratic formula: x = (-b ± √(b²-4ac)) / 2a",
            f"Discriminant: {b}² - 4({a})({c}) = {b**2 - 4*a*c}",
            f"Solve for x using the quadratic formula",
        ],
    }


def _generate_advanced_problem(problem_num: int) -> dict:
    """Generate an advanced-level calculus/system problem.

    Parameters:
        problem_num (int): Problem sequence number.

    Returns:
        dict: Problem with text and expected answer.
    """
    a = random.randint(1, 4)
    b = random.randint(1, 4)
    return {
        "category": "calculus",
        "text": f"Find the derivative: f(x) = {a}x^3 + {b}x^2",
        "answer": f"f'(x) = {3*a}x^2 + {2*b}x",
        "steps": [
            f"Given: f(x) = {a}x^3 + {b}x^2",
            "Apply the power rule: d/dx[x^n] = n*x^(n-1)",
            f"d/dx[{a}x^3] = {3*a}x^2",
            f"d/dx[{b}x^2] = {2*b}x",
            f"f'(x) = {3*a}x^2 + {2*b}x",
        ],
    }


def _generate_problems(config: dict, num_problems: int) -> list[dict]:
    """Generate math problems at the configured difficulty level.

    Parameters:
        config (dict): Runtime configuration.
        num_problems (int): Number of problems to generate.

    Returns:
        list[dict]: Generated problems with solutions.
    """
    difficulty = config["difficulty_level"]
    problems = []

    for i in range(num_problems):
        if difficulty == "beginner":
            problem = _generate_beginner_problem(i)
        elif difficulty == "intermediate":
            problem = _generate_intermediate_problem(i)
        else:
            problem = _generate_advanced_problem(i)

        problems.append(problem)

    return problems


def _simulate_user_solving(problem: dict) -> tuple[str, bool, float]:
    """Simulate a user attempting to solve a problem.

    Parameters:
        problem (dict): Generated problem.

    Returns:
        tuple: (user_answer, is_correct, solve_time_seconds)
    """
    correct_answer = problem["answer"]
    solve_time = random.uniform(10, 60)
    is_correct = random.random() > 0.3

    if is_correct:
        user_answer = correct_answer
    else:
        user_answer = f"{float(correct_answer.split()[0]) * 0.9:.2f}"

    return user_answer, is_correct, solve_time


def _compute_performance_stats(problem_records: list[dict]) -> dict:
    """Compute aggregate performance statistics.

    Parameters:
        problem_records (list[dict]): Problem solution records.

    Returns:
        dict: Performance statistics.
    """
    if not problem_records:
        return {
            "accuracy": 0.0,
            "avg_time_seconds": 0.0,
            "total_time_seconds": 0.0,
        }

    correct = sum(1 for p in problem_records if p.get("solved_correctly", False))
    total = len(problem_records)
    accuracy = correct / total if total > 0 else 0.0
    times = [p.get("solve_time_seconds", 0) for p in problem_records if "solve_time_seconds" in p]
    avg_time = sum(times) / len(times) if times else 0.0
    total_time = sum(times)

    return {
        "accuracy": accuracy,
        "avg_time_seconds": avg_time,
        "total_time_seconds": total_time,
    }


def _compute_category_breakdown(problem_records: list[dict]) -> dict[str, dict]:
    """Compute per-category performance breakdown.

    Parameters:
        problem_records (list[dict]): Problem solution records.

    Returns:
        dict: Category-level statistics.
    """
    breakdown: dict[str, dict[str, int]] = {}

    for record in problem_records:
        category = record.get("category", "unknown")
        if category not in breakdown:
            breakdown[category] = {"total": 0, "correct": 0}

        breakdown[category]["total"] += 1
        if record.get("solved_correctly", False):
            breakdown[category]["correct"] += 1

    for category in breakdown:
        total = breakdown[category]["total"]
        correct = breakdown[category]["correct"]
        accuracy = correct / total if total > 0 else 0.0
        breakdown[category]["accuracy"] = accuracy

    return breakdown


def run_core_flow(
    config: dict | None = None, difficulty_levels: list[dict] | None = None
) -> dict:
    """Execute a complete math tutoring session.

    Parameters:
        config (dict | None): Optional runtime configuration override.
        difficulty_levels (list[dict] | None): Optional difficulty levels override.

    Returns:
        dict: Persisted session summary.
    """
    runtime_config = config or create_project_config()
    available_levels = difficulty_levels or load_difficulty_levels()

    problems = _generate_problems(runtime_config, runtime_config["num_problems"])
    problem_records = []

    for idx, problem in enumerate(problems, start=1):
        user_answer, is_correct, solve_time = _simulate_user_solving(problem)

        record = create_problem_record(
            problem_id=f"prob_{idx:03d}",
            category=problem["category"],
            problem_text=problem["text"],
            correct_answer=problem["answer"],
            user_answer=user_answer,
            solved_correctly=is_correct,
            solve_time_seconds=solve_time,
            steps=problem.get("steps", []),
        )
        problem_records.append(record)

    performance_stats = _compute_performance_stats(problem_records)
    category_breakdown = _compute_category_breakdown(problem_records)

    summary = create_session_summary(
        config=runtime_config,
        difficulty_level=runtime_config["difficulty_level"],
        problems_attempted=len(problems),
        problems_completed=sum(1 for r in problem_records if r.get("solved_correctly", False)),
        performance_stats=performance_stats,
        category_breakdown=category_breakdown,
        problem_records=problem_records,
        status="completed",
    )
    save_latest_session(summary)
    return summary
