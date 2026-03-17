"""display.py - Presentation helpers for Project 39: Interactive Optimization Visualizer."""

from typing import Any, Dict, List


def format_header() -> str:
    """Format session header banner."""
    return '=' * 70 + '\n' + '   INTERACTIVE OPTIMIZATION VISUALIZER\n' + '=' * 70


def format_startup_guide(config: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """Format startup configuration and historical profile."""
    recent = ', '.join(profile.get('recent_solutions', [])) or 'None yet'
    lines = [
        '',
        'Configuration:',
        f"   Project type:         {config['project_type']}",
        '   Solver stack:         scipy.optimize + matplotlib',
        f"   Linear grid points:   {config['linear_grid_points']}",
        f"   Max nonlinear iters:  {config['nonlinear_max_iterations']}",
        f"   Feasible region plot: {config['include_feasible_region_plot']}",
        f"   Convergence plot:     {config['include_convergence_plot']}",
        f"   Path contour plot:    {config['include_path_plot']}",
        f"   Max sols in report:   {config['max_solutions_in_report']}",
        f"   Random seed:          {config['random_seed']}",
        '',
        'Startup:',
        '   Data directory:       data/',
        '   Outputs directory:    data/outputs/',
        (
            f"   Problem library:      {profile['library_file']} "
            f"(loaded {profile['problems_available']} problems)"
        ),
        (
            f"   Run catalog:          {profile['catalog_file']} "
            f"(loaded {profile['runs_stored']} runs)"
        ),
        (
            f"   Solution catalog:     {profile['solution_catalog_file']} "
            f"(loaded {profile['solution_records_stored']} records)"
        ),
        f"   Recent solutions:     {recent}",
        '',
        '---',
    ]
    return '\n'.join(lines)


def format_solution_table(previews: List[Dict[str, Any]]) -> str:
    """Format optimization solution preview table."""
    if not previews:
        return 'No solutions generated.'
    lines = [
        'Solution previews:',
        '   ID      | Problem                      | Kind      | Objective | Iters | Status',
        '   --------+------------------------------+-----------+-----------+-------+----------------',
    ]
    for solution in previews:
        lines.append(
            '   '
            f"{solution['solution_id'][:7]:<7} | "
            f"{solution.get('problem_name', '')[:28]:<28} | "
            f"{solution.get('problem_kind', '')[:9]:<9} | "
            f"{solution.get('objective_value', 0.0):>9.3f} | "
            f"{solution.get('iterations', 0):>5} | "
            f"{solution.get('status', '')[:16]:<16}"
        )
    return '\n'.join(lines)


def format_run_report(summary: Dict[str, Any]) -> str:
    """Format final run report."""
    artifacts = summary.get('artifacts', {})
    metrics = summary.get('metrics', {})
    metadata_files = artifacts.get('metadata_files', [])
    lines = [
        '',
        'Run complete:',
        f"   Run ID:               {summary['run_id']}",
        f"   Problems loaded:      {summary['problems_loaded']}",
        f"   Solutions generated:  {summary['solutions_generated']}",
        f"   Successful solves:    {summary['successful_solves']}",
        f"   Elapsed time:         {summary['elapsed_ms']:.2f} ms",
        '',
        (
            f"Dataset metrics: success_rate={metrics.get('success_rate', 0.0):.1%} | "
            f"mean_iterations={metrics.get('mean_iterations', 0.0):.1f} | "
            f"best_linear_objective={metrics.get('best_linear_objective', 0.0):.3f} | "
            f"best_nonlinear_objective={metrics.get('best_nonlinear_objective', 0.0):.3f}"
        ),
        '',
        format_solution_table(summary.get('solution_previews', [])),
        '',
        'Artifacts saved:',
        f"   Run record:           {artifacts.get('run_file', 'N/A')}",
        f"   Bundle export:        {artifacts.get('bundle_file', 'N/A')}",
        f"   Feasible region plot: {artifacts.get('feasible_region_file', 'N/A')}",
        f"   Convergence plot:     {artifacts.get('convergence_file', 'N/A')}",
        f"   Path contour plot:    {artifacts.get('path_file', 'N/A')}",
        f"   Metadata exports:     {len(metadata_files)}",
    ]
    return '\n'.join(lines)


def format_message(message: str) -> str:
    """Format a user-facing message string."""
    return f'[Project 39] {message}'
