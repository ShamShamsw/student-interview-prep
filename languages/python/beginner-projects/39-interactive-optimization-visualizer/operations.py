"""operations.py - Business logic for Project 39: Interactive Optimization Visualizer."""

from __future__ import annotations

from datetime import datetime
import json
import math
from pathlib import Path
import statistics
import time
from typing import Any, Dict, List, Sequence, Tuple

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
from scipy.optimize import Bounds, LinearConstraint, NonlinearConstraint, linprog, minimize

from models import create_run_summary, create_solution_record, create_visualizer_config
from storage import (
    OUTPUTS_DIR,
    ensure_data_dirs,
    load_problem_library,
    load_run_catalog,
    load_solution_catalog,
    save_problem_library,
    save_run_record,
    save_solution_record,
)


def _run_id() -> str:
    """Build a compact run ID from UTC timestamp."""
    return datetime.utcnow().strftime('%Y%m%d_%H%M%S')


def _default_problem_library() -> List[Dict[str, Any]]:
    """Return deterministic starter optimization problems used on first run."""
    return [
        {
            'problem_id': 'opt_001',
            'name': 'Production Mix Linear Program',
            'kind': 'linear',
            'objective_direction': 'maximize',
            'objective': 'maximize 3x + 5y',
            'variables': ['x', 'y'],
            'constraints': ['x + 2y <= 14', '3x - y <= 0', '0 <= x <= 6', '0 <= y <= 8'],
            'solver': {
                'c': [-3.0, -5.0],
                'A_ub': [[1.0, 2.0], [3.0, -1.0]],
                'b_ub': [14.0, 0.0],
                'bounds': [[0.0, 6.0], [0.0, 8.0]],
            },
            'plot': {'x_range': [0.0, 6.5], 'y_range': [0.0, 8.5]},
        },
        {
            'problem_id': 'opt_002',
            'name': 'Rippled Nonlinear Design Search',
            'kind': 'nonlinear',
            'objective_direction': 'minimize',
            'objective': 'minimize (x-1.8)^2 + (y-1.2)^2 + 0.25*sin(3x)*cos(2y)',
            'variables': ['x', 'y'],
            'constraints': ['x + y >= 2.2', 'x^2 + y^2 <= 9', '0 <= x <= 3.2', '0 <= y <= 3.2'],
            'solver': {
                'start': [0.35, 2.75],
                'bounds': [[0.0, 3.2], [0.0, 3.2]],
                'maxiter': 60,
            },
            'plot': {'x_range': [0.0, 3.2], 'y_range': [0.0, 3.2]},
        },
    ]


def _objective_non_linear(point: Sequence[float]) -> float:
    """Evaluate the nonlinear objective function at a point."""
    x_value, y_value = float(point[0]), float(point[1])
    return (x_value - 1.8) ** 2 + (y_value - 1.2) ** 2 + 0.25 * math.sin(3.0 * x_value) * math.cos(2.0 * y_value)


def _circle_constraint(point: Sequence[float]) -> float:
    """Return remaining radius slack for the nonlinear circular constraint."""
    x_value, y_value = float(point[0]), float(point[1])
    return 9.0 - x_value**2 - y_value**2


def _line_constraint(point: Sequence[float]) -> float:
    """Return slack for the nonlinear linear inequality constraint."""
    x_value, y_value = float(point[0]), float(point[1])
    return x_value + y_value - 2.2


def _build_linear_solution(problem: Dict[str, Any], run_id: str, config: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """Solve the linear program and save the feasible-region plot."""
    solver = problem['solver']
    result = linprog(
        c=solver['c'],
        A_ub=solver['A_ub'],
        b_ub=solver['b_ub'],
        bounds=solver['bounds'],
        method='highs',
    )

    x_value, y_value = (float(result.x[0]), float(result.x[1])) if result.x is not None else (0.0, 0.0)
    objective_value = 3.0 * x_value + 5.0 * y_value
    slack_map = {
        'x_plus_2y_le_14': 14.0 - (x_value + 2.0 * y_value),
        '3x_minus_y_le_0': 0.0 - (3.0 * x_value - y_value),
        'x_lower_bound': x_value,
        'y_lower_bound': y_value,
        'x_upper_bound': 6.0 - x_value,
        'y_upper_bound': 8.0 - y_value,
    }
    notes = [
        'objective converted to minimization form for scipy.linprog',
        'feasible-region plot highlights the optimal corner point',
    ]

    feasible_region_file = ''
    if config['include_feasible_region_plot']:
        feasible_region_file = _save_linear_plot(problem, run_id, x_value, y_value, objective_value, config)

    solution = create_solution_record(
        solution_id='sol_001',
        problem_id=str(problem['problem_id']),
        problem_name=str(problem['name']),
        problem_kind='linear',
        solver_name='scipy.optimize.linprog',
        status='optimal' if bool(result.success) else str(result.status),
        objective_direction=str(problem['objective_direction']),
        objective_value=objective_value,
        variable_values={'x': x_value, 'y': y_value},
        iterations=int(getattr(result, 'nit', 0) or 0),
        constraint_slacks=slack_map,
        convergence_history=[objective_value],
        artifacts={'feasible_region_plot': feasible_region_file},
        notes=notes,
    )
    return solution, {'feasible_region_plot': feasible_region_file}


def _build_nonlinear_solution(problem: Dict[str, Any], run_id: str, config: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """Solve the nonlinear program and save convergence/path plots."""
    solver = problem['solver']
    start = solver['start']
    bounds = Bounds([bound[0] for bound in solver['bounds']], [bound[1] for bound in solver['bounds']])
    objective_history = [_objective_non_linear(start)]
    point_history: List[Tuple[float, float]] = [(float(start[0]), float(start[1]))]

    def callback(current: Sequence[float]) -> None:
        point = (float(current[0]), float(current[1]))
        point_history.append(point)
        objective_history.append(_objective_non_linear(point))

    result = minimize(
        fun=_objective_non_linear,
        x0=start,
        method='SLSQP',
        bounds=bounds,
        constraints=[
            NonlinearConstraint(_line_constraint, 0.0, math.inf),
            NonlinearConstraint(_circle_constraint, 0.0, math.inf),
        ],
        callback=callback,
        options={'maxiter': min(int(solver['maxiter']), int(config['nonlinear_max_iterations'])), 'disp': False},
    )

    x_value, y_value = (float(result.x[0]), float(result.x[1])) if result.x is not None else (0.0, 0.0)
    objective_value = float(result.fun) if result.fun is not None else _objective_non_linear((x_value, y_value))
    final_point = (x_value, y_value)
    if point_history[-1] != final_point:
        point_history.append(final_point)
        objective_history.append(objective_value)

    slack_map = {
        'x_plus_y_ge_2_2': _line_constraint(final_point),
        'x_squared_plus_y_squared_le_9': _circle_constraint(final_point),
        'x_lower_bound': x_value,
        'y_lower_bound': y_value,
        'x_upper_bound': 3.2 - x_value,
        'y_upper_bound': 3.2 - y_value,
    }
    notes = [
        'SLSQP callback captured the iterative path for convergence reporting',
        'path contour plot overlays iterate locations on the nonlinear surface',
    ]

    artifacts = {'convergence_plot': '', 'path_plot': ''}
    if config['include_convergence_plot']:
        artifacts['convergence_plot'] = _save_convergence_plot(problem, run_id, objective_history)
    if config['include_path_plot']:
        artifacts['path_plot'] = _save_path_plot(problem, run_id, point_history)

    solution = create_solution_record(
        solution_id='sol_002',
        problem_id=str(problem['problem_id']),
        problem_name=str(problem['name']),
        problem_kind='nonlinear',
        solver_name='scipy.optimize.minimize[SLSQP]',
        status='optimal' if bool(result.success) else str(result.message),
        objective_direction=str(problem['objective_direction']),
        objective_value=objective_value,
        variable_values={'x': x_value, 'y': y_value},
        iterations=max(0, len(objective_history) - 1),
        constraint_slacks=slack_map,
        convergence_history=objective_history,
        artifacts=artifacts,
        notes=notes,
    )
    return solution, artifacts


def _save_linear_plot(
    problem: Dict[str, Any],
    run_id: str,
    x_value: float,
    y_value: float,
    objective_value: float,
    config: Dict[str, Any],
) -> str:
    """Persist a feasible-region plot for the linear optimization example."""
    plot = problem['plot']
    x_min, x_max = plot['x_range']
    y_min, y_max = plot['y_range']
    grid_points = int(config['linear_grid_points'])

    xs = [x_min + (x_max - x_min) * index / (grid_points - 1) for index in range(grid_points)]
    ys = [y_min + (y_max - y_min) * index / (grid_points - 1) for index in range(grid_points)]

    feasible_x: List[float] = []
    feasible_y: List[float] = []
    contour_x: List[float] = []
    contour_y: List[float] = []
    contour_z: List[float] = []

    for x_coord in xs:
        for y_coord in ys:
            is_feasible = (
                x_coord + 2.0 * y_coord <= 14.0 + 1e-9
                and 3.0 * x_coord - y_coord <= 1e-9
                and 0.0 <= x_coord <= 6.0 + 1e-9
                and 0.0 <= y_coord <= 8.0 + 1e-9
            )
            if is_feasible:
                feasible_x.append(x_coord)
                feasible_y.append(y_coord)
            contour_x.append(x_coord)
            contour_y.append(y_coord)
            contour_z.append(3.0 * x_coord + 5.0 * y_coord)

    figure, axis = plt.subplots(figsize=(8, 6))
    axis.scatter(feasible_x, feasible_y, s=5, alpha=0.18, color='#8ecae6', label='feasible region')
    axis.tricontour(contour_x, contour_y, contour_z, levels=10, colors='#355070', linewidths=0.8)
    axis.plot(xs, [(14.0 - x_coord) / 2.0 for x_coord in xs], color='#bc4749', label='x + 2y = 14')
    axis.plot(xs, [3.0 * x_coord for x_coord in xs], color='#6a994e', label='3x - y = 0')
    axis.scatter([x_value], [y_value], color='#d00000', s=80, zorder=3, label='optimal point')
    axis.annotate(
        f'optimum ({x_value:.2f}, {y_value:.2f})\nobjective={objective_value:.2f}',
        xy=(x_value, y_value),
        xytext=(x_value + 0.25, y_value - 1.0),
        arrowprops={'arrowstyle': '->', 'color': '#d00000'},
        fontsize=9,
    )
    axis.set_title(problem['name'])
    axis.set_xlabel('x')
    axis.set_ylabel('y')
    axis.set_xlim(x_min, x_max)
    axis.set_ylim(y_min, y_max)
    axis.legend(loc='upper right')
    axis.grid(alpha=0.25)
    figure.tight_layout()

    file_path = OUTPUTS_DIR / f'feasible_region_{run_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def _save_convergence_plot(problem: Dict[str, Any], run_id: str, objective_history: Sequence[float]) -> str:
    """Persist an optimization convergence plot."""
    figure, axis = plt.subplots(figsize=(8, 5))
    iteration_axis = list(range(len(objective_history)))
    axis.plot(iteration_axis, list(objective_history), marker='o', color='#1d3557', linewidth=2)
    axis.set_title(f"{problem['name']} - Objective Convergence")
    axis.set_xlabel('Iteration')
    axis.set_ylabel('Objective value')
    axis.grid(alpha=0.3)
    figure.tight_layout()

    file_path = OUTPUTS_DIR / f'convergence_{run_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def _save_path_plot(problem: Dict[str, Any], run_id: str, point_history: Sequence[Tuple[float, float]]) -> str:
    """Persist a contour plot with the nonlinear optimization path overlaid."""
    plot = problem['plot']
    x_min, x_max = plot['x_range']
    y_min, y_max = plot['y_range']
    grid_points = 140

    xs = [x_min + (x_max - x_min) * index / (grid_points - 1) for index in range(grid_points)]
    ys = [y_min + (y_max - y_min) * index / (grid_points - 1) for index in range(grid_points)]
    contour_x: List[float] = []
    contour_y: List[float] = []
    contour_z: List[float] = []

    for x_coord in xs:
        for y_coord in ys:
            contour_x.append(x_coord)
            contour_y.append(y_coord)
            contour_z.append(_objective_non_linear((x_coord, y_coord)))

    path_x = [point[0] for point in point_history]
    path_y = [point[1] for point in point_history]

    figure, axis = plt.subplots(figsize=(8, 6))
    axis.tricontourf(contour_x, contour_y, contour_z, levels=18, cmap='YlGnBu')
    axis.plot(path_x, path_y, color='#d00000', marker='o', linewidth=2, markersize=4, label='solver path')
    axis.plot(xs, [max(2.2 - x_coord, 0.0) for x_coord in xs], color='white', linestyle='--', linewidth=1.2, label='x + y = 2.2')
    circle_x = [3.0 * math.cos(2.0 * math.pi * idx / 120.0) for idx in range(121)]
    circle_y = [3.0 * math.sin(2.0 * math.pi * idx / 120.0) for idx in range(121)]
    axis.plot(circle_x, circle_y, color='white', linestyle=':', linewidth=1.2, label='x^2 + y^2 = 9')
    axis.set_title(f"{problem['name']} - Search Path")
    axis.set_xlabel('x')
    axis.set_ylabel('y')
    axis.set_xlim(x_min, x_max)
    axis.set_ylim(y_min, y_max)
    axis.legend(loc='upper right')
    figure.tight_layout()

    file_path = OUTPUTS_DIR / f'path_contour_{run_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def load_visualizer_profile() -> Dict[str, Any]:
    """Return startup profile built from previously saved catalogs."""
    runs = load_run_catalog()
    solutions = load_solution_catalog()
    library = load_problem_library()
    recent_solutions = [
        f"{item.get('solution_id', '')}:{item.get('problem_kind', '')}:{item.get('objective_value', 0.0):.3f}"
        for item in solutions[-6:]
    ]
    return {
        'catalog_file': 'data/runs.json',
        'solution_catalog_file': 'data/solutions.json',
        'library_file': 'data/problems.json',
        'runs_stored': len(runs),
        'solution_records_stored': len(solutions),
        'problems_available': len(library),
        'recent_solutions': recent_solutions,
    }


def run_core_flow() -> Dict[str, Any]:
    """Run one complete optimization visualization session."""
    ensure_data_dirs()
    config = create_visualizer_config()
    run_id = _run_id()
    started = time.perf_counter()

    library = load_problem_library()
    if not library:
        library = _default_problem_library()
        save_problem_library(library)

    solutions: List[Dict[str, Any]] = []
    metadata_files: List[str] = []
    artifact_index: Dict[str, str] = {'feasible_region_plot': '', 'convergence_plot': '', 'path_plot': ''}

    for problem in library:
        kind = str(problem.get('kind', '')).lower()
        if kind == 'linear':
            solution, artifacts = _build_linear_solution(problem, run_id, config)
        elif kind == 'nonlinear':
            solution, artifacts = _build_nonlinear_solution(problem, run_id, config)
        else:
            continue
        solutions.append(solution)
        metadata_files.append(save_solution_record(solution, run_id))
        for key, value in artifacts.items():
            if value:
                artifact_index[key] = value

    bundle_file = OUTPUTS_DIR / f'solutions_{run_id}.json'
    bundle_file.write_text(
        json.dumps(
            {
                'run_id': run_id,
                'project_type': config['project_type'],
                'problems': library,
                'solutions': solutions,
            },
            indent=2,
        ),
        encoding='utf-8',
    )

    elapsed_ms = (time.perf_counter() - started) * 1000.0
    successful_solves = sum(1 for solution in solutions if str(solution.get('status', '')).lower().startswith('optimal'))
    linear_solutions = [solution for solution in solutions if solution.get('problem_kind') == 'linear']
    nonlinear_solutions = [solution for solution in solutions if solution.get('problem_kind') == 'nonlinear']
    metrics: Dict[str, Any] = {
        'success_rate': round(successful_solves / len(solutions), 4) if solutions else 0.0,
        'mean_iterations': round(statistics.mean(solution['iterations'] for solution in solutions), 4)
        if solutions
        else 0.0,
        'best_linear_objective': round(
            max(solution['objective_value'] for solution in linear_solutions), 6
        )
        if linear_solutions
        else 0.0,
        'best_nonlinear_objective': round(
            min(solution['objective_value'] for solution in nonlinear_solutions), 6
        )
        if nonlinear_solutions
        else 0.0,
    }

    artifacts = {
        'run_file': '',
        'bundle_file': str(bundle_file),
        'feasible_region_file': artifact_index.get('feasible_region_plot', ''),
        'convergence_file': artifact_index.get('convergence_plot', ''),
        'path_file': artifact_index.get('path_plot', ''),
        'metadata_files': metadata_files,
    }

    summary = create_run_summary(
        run_id=run_id,
        problems_loaded=len(library),
        solutions_generated=len(solutions),
        successful_solves=successful_solves,
        elapsed_ms=elapsed_ms,
        artifacts=artifacts,
        solution_previews=solutions[: config['max_solutions_in_report']],
        metrics=metrics,
    )
    run_file = save_run_record(summary)
    artifacts['run_file'] = run_file
    summary['artifacts']['run_file'] = run_file
    return summary
