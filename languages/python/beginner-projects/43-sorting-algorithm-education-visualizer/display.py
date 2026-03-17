"""Presentation helpers for Project 43: Sorting Algorithm Education Visualizer."""

from typing import Any, Dict, List


ALGORITHM_LABELS = {
    'quicksort': 'Quick Sort',
    'mergesort': 'Merge Sort',
    'heapsort': 'Heap Sort',
}


def format_header() -> str:
    """Format session header banner."""
    return '=' * 70 + '\n' + '   SORTING ALGORITHM EDUCATION VISUALIZER\n' + '=' * 70


def format_startup_guide(config: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """Format startup configuration and historical profile."""
    recent = ', '.join(profile.get('recent_runs', [])) or 'None yet'
    lines = [
        '',
        'Configuration:',
        f"   Project type:           {config['project_type']}",
        f"   Algorithms:             {', '.join(ALGORITHM_LABELS.get(name, name) for name in config['algorithms'])}",
        f"   Demo array:             {config['demo_array_label']}",
        f"   Benchmark sizes:        {', '.join(str(size) for size in config['benchmark_sizes'])}",
        f"   Trials per size:        {config['benchmark_trials']}",
        f"   Storyboard frames:      {config['storyboard_frames']}",
        f"   Storyboard plot:        {config['include_storyboard_plot']}",
        f"   Runtime chart:          {config['include_runtime_chart']}",
        f"   Operations chart:       {config['include_operations_chart']}",
        f"   Max algorithms report:  {config['max_algorithms_in_report']}",
        f"   Random seed:            {config['random_seed']}",
        '',
        'Startup:',
        '   Data directory:         data/',
        '   Outputs directory:      data/outputs/',
        (
            f"   Array library:          {profile['library_file']} "
            f"(loaded {profile['arrays_available']} arrays)"
        ),
        (
            f"   Run catalog:            {profile['catalog_file']} "
            f"(loaded {profile['runs_stored']} runs)"
        ),
        f"   Recent runs:            {recent}",
        '',
        '---',
    ]
    return '\n'.join(lines)


def format_algorithm_table(algorithm_previews: List[Dict[str, Any]]) -> str:
    """Format demo algorithm preview table."""
    if not algorithm_previews:
        return 'No algorithm previews generated.'
    lines = [
        'Algorithm previews:',
        '   Algorithm  | Time (ms) | Comparisons | Writes | Swaps | Depth | Sorted',
        '   -----------+-----------+-------------+--------+-------+-------+--------',
    ]
    for report in algorithm_previews:
        lines.append(
            '   '
            f"{ALGORITHM_LABELS.get(report['algorithm'], report['algorithm'])[:10]:<10} | "
            f"{report['elapsed_ms']:<9.4f} | "
            f"{report['comparisons']:<11} | "
            f"{report['writes']:<6} | "
            f"{report['swaps']:<5} | "
            f"{report['max_depth']:<5} | "
            f"{'yes' if report['is_sorted'] else 'no'}"
        )
    return '\n'.join(lines)


def format_run_report(summary: Dict[str, Any]) -> str:
    """Format final session report."""
    artifacts = summary.get('artifacts', {})
    metrics = summary.get('metrics', {})
    fastest_algorithm = ALGORITHM_LABELS.get(metrics.get('fastest_algorithm', ''), metrics.get('fastest_algorithm', 'N/A'))
    cheapest_algorithm = ALGORITHM_LABELS.get(
        metrics.get('lowest_demo_ops_algorithm', ''),
        metrics.get('lowest_demo_ops_algorithm', 'N/A'),
    )
    lines = [
        '',
        'Session complete:',
        f"   Session ID:             {summary['session_id']}",
        f"   Arrays available:       {summary['arrays_available']}",
        f"   Demo array:             {summary['demo_array_label']} ({summary['demo_array_length']} items)",
        f"   Algorithms run:         {summary['algorithms_run']}",
        f"   Benchmark points:       {summary['benchmark_points']}",
        f"   Elapsed time:           {summary['elapsed_ms']:.2f} ms",
        '',
        (
            'Lesson metrics: '
            f"fastest_algorithm={fastest_algorithm} | "
            f"fastest_runtime_ms={metrics.get('fastest_runtime_ms', 0.0):.5f} | "
            f"lowest_demo_ops={cheapest_algorithm} ({metrics.get('lowest_demo_ops', 0)}) | "
            f"largest_array_size={metrics.get('largest_array_size', 0)}"
        ),
        '',
        format_algorithm_table(summary.get('algorithm_previews', [])),
        '',
        'Artifacts saved:',
        f"   Session record:         {artifacts.get('session_file', 'N/A')}",
        f"   Trace bundle:           {artifacts.get('trace_file', 'N/A')}",
        f"   Benchmark file:         {artifacts.get('benchmark_file', 'N/A')}",
        f"   Storyboard plot:        {artifacts.get('storyboard_file', 'N/A')}",
        f"   Runtime chart:          {artifacts.get('runtime_chart_file', 'N/A')}",
        f"   Operations chart:       {artifacts.get('operations_chart_file', 'N/A')}",
    ]
    return '\n'.join(lines)


def format_message(message: str) -> str:
    """Format a user-facing message string."""
    return f'[Project 43] {message}'
