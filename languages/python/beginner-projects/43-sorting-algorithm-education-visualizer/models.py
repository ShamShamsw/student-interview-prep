"""Data models for Project 43: Sorting Algorithm Education Visualizer."""

from datetime import datetime
from typing import Any, Dict, List


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string."""
    return datetime.utcnow().isoformat(timespec='seconds') + 'Z'


def create_visualizer_config(
    algorithms: List[str] | None = None,
    demo_array_label: str = 'lesson_random_12',
    benchmark_sizes: List[int] | None = None,
    benchmark_trials: int = 3,
    storyboard_frames: int = 6,
    include_storyboard_plot: bool = True,
    include_runtime_chart: bool = True,
    include_operations_chart: bool = True,
    max_algorithms_in_report: int = 3,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """Create a validated configuration record for one visualization session."""
    resolved_algorithms = algorithms if algorithms else ['quicksort', 'mergesort', 'heapsort']
    resolved_sizes = benchmark_sizes if benchmark_sizes else [16, 32, 64, 96, 128]
    return {
        'project_type': 'sorting_algorithm_education_visualizer',
        'algorithms': list(resolved_algorithms),
        'demo_array_label': str(demo_array_label),
        'benchmark_sizes': [max(8, int(size)) for size in resolved_sizes],
        'benchmark_trials': max(1, int(benchmark_trials)),
        'storyboard_frames': max(4, int(storyboard_frames)),
        'include_storyboard_plot': bool(include_storyboard_plot),
        'include_runtime_chart': bool(include_runtime_chart),
        'include_operations_chart': bool(include_operations_chart),
        'max_algorithms_in_report': max(1, int(max_algorithms_in_report)),
        'random_seed': int(random_seed),
        'created_at': _utc_timestamp(),
    }


def create_array_record(
    array_id: str,
    label: str,
    values: List[int],
    description: str,
    tags: List[str],
) -> Dict[str, Any]:
    """Create one reusable lesson array record."""
    return {
        'array_id': str(array_id),
        'label': str(label),
        'values': [int(value) for value in values],
        'description': str(description),
        'tags': [str(tag) for tag in tags],
    }


def create_trace_frame(
    step: int,
    values: List[int],
    active_indices: List[int],
    note: str,
    counts: Dict[str, Any],
) -> Dict[str, Any]:
    """Create one captured sorting trace frame."""
    return {
        'step': int(step),
        'values': [int(value) for value in values],
        'active_indices': [int(index) for index in active_indices],
        'note': str(note),
        'counts': {
            'comparisons': int(counts.get('comparisons', 0)),
            'writes': int(counts.get('writes', 0)),
            'swaps': int(counts.get('swaps', 0)),
            'max_depth': int(counts.get('max_depth', 0)),
        },
    }


def create_algorithm_report(
    algorithm: str,
    sorted_values: List[int],
    comparisons: int,
    writes: int,
    swaps: int,
    max_depth: int,
    elapsed_ms: float,
    frame_count: int,
    sampled_frames: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Create a report describing one algorithm run on the demo array."""
    return {
        'algorithm': str(algorithm),
        'sorted_values': [int(value) for value in sorted_values],
        'comparisons': int(comparisons),
        'writes': int(writes),
        'swaps': int(swaps),
        'max_depth': int(max_depth),
        'elapsed_ms': round(float(elapsed_ms), 4),
        'frame_count': int(frame_count),
        'sampled_frames': list(sampled_frames),
        'is_sorted': sorted_values == sorted(sorted_values),
    }


def create_benchmark_point(
    algorithm: str,
    array_size: int,
    trial: int,
    elapsed_ms: float,
    comparisons: int,
    writes: int,
    swaps: int,
) -> Dict[str, Any]:
    """Create one benchmark-trial measurement record."""
    return {
        'algorithm': str(algorithm),
        'array_size': int(array_size),
        'trial': int(trial),
        'elapsed_ms': round(float(elapsed_ms), 5),
        'comparisons': int(comparisons),
        'writes': int(writes),
        'swaps': int(swaps),
        'primitive_ops': int(comparisons) + int(writes) + int(swaps),
    }


def create_session_summary(
    session_id: str,
    arrays_available: int,
    demo_array_label: str,
    demo_array_length: int,
    algorithms_run: int,
    benchmark_points: int,
    elapsed_ms: float,
    artifacts: Dict[str, Any],
    algorithm_previews: List[Dict[str, Any]],
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """Create final session summary for reporting and persistence."""
    return {
        'session_id': str(session_id),
        'arrays_available': int(arrays_available),
        'demo_array_label': str(demo_array_label),
        'demo_array_length': int(demo_array_length),
        'algorithms_run': int(algorithms_run),
        'benchmark_points': int(benchmark_points),
        'elapsed_ms': round(float(elapsed_ms), 4),
        'artifacts': dict(artifacts),
        'algorithm_previews': list(algorithm_previews),
        'metrics': dict(metrics),
        'finished_at': _utc_timestamp(),
    }


def create_record(**kwargs):
    """Backwards-compatible generic record factory."""
    return dict(kwargs)
