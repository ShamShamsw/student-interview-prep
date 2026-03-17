"""models.py - Data models for Project 39: Interactive Optimization Visualizer."""

from datetime import datetime
from typing import Any, Dict, List


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string."""
    return datetime.utcnow().isoformat(timespec='seconds') + 'Z'


def create_visualizer_config(
    linear_grid_points: int = 220,
    nonlinear_max_iterations: int = 60,
    include_feasible_region_plot: bool = True,
    include_convergence_plot: bool = True,
    include_path_plot: bool = True,
    max_solutions_in_report: int = 6,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """Create a validated configuration record for the optimization visualizer."""
    return {
        'project_type': 'interactive_optimization_visualizer',
        'linear_grid_points': max(80, int(linear_grid_points)),
        'nonlinear_max_iterations': max(10, int(nonlinear_max_iterations)),
        'include_feasible_region_plot': bool(include_feasible_region_plot),
        'include_convergence_plot': bool(include_convergence_plot),
        'include_path_plot': bool(include_path_plot),
        'max_solutions_in_report': max(2, int(max_solutions_in_report)),
        'random_seed': int(random_seed),
        'created_at': _utc_timestamp(),
    }


def create_solution_record(
    solution_id: str,
    problem_id: str,
    problem_name: str,
    problem_kind: str,
    solver_name: str,
    status: str,
    objective_direction: str,
    objective_value: float,
    variable_values: Dict[str, float],
    iterations: int,
    constraint_slacks: Dict[str, float],
    convergence_history: List[float],
    artifacts: Dict[str, str],
    notes: List[str],
) -> Dict[str, Any]:
    """Create one computed optimization solution record."""
    return {
        'solution_id': solution_id,
        'problem_id': problem_id,
        'problem_name': problem_name,
        'problem_kind': problem_kind,
        'solver_name': solver_name,
        'status': status,
        'objective_direction': objective_direction,
        'objective_value': round(float(objective_value), 6),
        'variable_values': {key: round(float(value), 6) for key, value in variable_values.items()},
        'iterations': int(iterations),
        'constraint_slacks': {key: round(float(value), 6) for key, value in constraint_slacks.items()},
        'convergence_history': [round(float(value), 6) for value in convergence_history],
        'artifacts': dict(artifacts),
        'notes': list(notes),
        'created_at': _utc_timestamp(),
    }


def create_run_summary(
    run_id: str,
    problems_loaded: int,
    solutions_generated: int,
    successful_solves: int,
    elapsed_ms: float,
    artifacts: Dict[str, Any],
    solution_previews: List[Dict[str, Any]],
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """Create final run summary for reporting and persistence."""
    return {
        'run_id': run_id,
        'problems_loaded': int(problems_loaded),
        'solutions_generated': int(solutions_generated),
        'successful_solves': int(successful_solves),
        'elapsed_ms': float(elapsed_ms),
        'artifacts': dict(artifacts),
        'solution_previews': list(solution_previews),
        'metrics': dict(metrics),
        'finished_at': _utc_timestamp(),
    }


def create_record(**kwargs):
    """Backwards-compatible generic record factory."""
    return dict(kwargs)
