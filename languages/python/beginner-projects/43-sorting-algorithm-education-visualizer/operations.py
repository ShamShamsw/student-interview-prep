"""Business logic for Project 43: Sorting Algorithm Education Visualizer."""

from __future__ import annotations

import random
import time
from collections import defaultdict
from datetime import datetime
from statistics import mean
from typing import Any, Dict, List

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

from models import (
    create_algorithm_report,
    create_array_record,
    create_benchmark_point,
    create_session_summary,
    create_trace_frame,
    create_visualizer_config,
)
from storage import (
    OUTPUTS_DIR,
    ensure_data_dirs,
    load_array_library,
    load_run_catalog,
    save_array_library,
    save_benchmark_file,
    save_run_record,
    save_trace_file,
)


ALGORITHM_LABELS = {
    'quicksort': 'Quick Sort',
    'mergesort': 'Merge Sort',
    'heapsort': 'Heap Sort',
}

ALGORITHM_COLORS = {
    'quicksort': '#1d3557',
    'mergesort': '#2a9d8f',
    'heapsort': '#e76f51',
}


def _session_id() -> str:
    """Build a compact session ID from UTC timestamp."""
    return datetime.utcnow().strftime('%Y%m%d_%H%M%S')


def _default_array_library() -> List[Dict[str, Any]]:
    """Return deterministic starter arrays used on first run."""
    return [
        create_array_record(
            array_id='array_001',
            label='lesson_random_12',
            values=[38, 12, 57, 9, 61, 24, 45, 17, 73, 30, 52, 4],
            description='Mixed unsorted values for the main storyboard demo.',
            tags=['demo', 'random', 'balanced'],
        ),
        create_array_record(
            array_id='array_002',
            label='lesson_nearly_sorted_12',
            values=[3, 7, 11, 14, 18, 22, 27, 31, 35, 40, 39, 44],
            description='Nearly sorted values to show best-case style behavior.',
            tags=['demo', 'nearly_sorted'],
        ),
        create_array_record(
            array_id='array_003',
            label='lesson_reversed_12',
            values=[88, 79, 71, 64, 57, 48, 39, 28, 20, 13, 6, 1],
            description='Descending values to emphasize difficult ordering patterns.',
            tags=['demo', 'reversed'],
        ),
        create_array_record(
            array_id='array_004',
            label='lesson_duplicates_12',
            values=[12, 7, 12, 3, 9, 7, 15, 3, 18, 15, 6, 9],
            description='Duplicate-heavy values for discussing stability and repeated keys.',
            tags=['demo', 'duplicates'],
        ),
    ]


def _new_counts() -> Dict[str, int]:
    """Return a fresh operation counter dictionary."""
    return {'comparisons': 0, 'writes': 0, 'swaps': 0, 'max_depth': 0}


def _record_frame(
    frames: List[Dict[str, Any]],
    values: List[int],
    active_indices: List[int],
    note: str,
    counts: Dict[str, int],
) -> None:
    """Capture one full-array frame for later visualization."""
    frames.append(
        create_trace_frame(
            step=len(frames),
            values=list(values),
            active_indices=list(active_indices),
            note=note,
            counts=counts,
        )
    )


def _sample_frames(frames: List[Dict[str, Any]], target_count: int) -> List[Dict[str, Any]]:
    """Down-sample a long frame list into a storyboard-friendly subset."""
    if len(frames) <= target_count:
        return list(frames)
    indices = []
    max_index = len(frames) - 1
    for slot in range(target_count):
        index = round(slot * max_index / (target_count - 1))
        if not indices or index != indices[-1]:
            indices.append(index)
    if indices[-1] != max_index:
        indices[-1] = max_index
    return [frames[index] for index in indices]


def _run_quicksort(values: List[int], capture_frames: bool = True) -> Dict[str, Any]:
    """Run quicksort with deterministic instrumentation."""
    numbers = list(values)
    counts = _new_counts()
    frames: List[Dict[str, Any]] = []

    if capture_frames:
        _record_frame(frames, numbers, [], 'Initial state', counts)

    def partition(low: int, high: int, depth: int) -> int:
        counts['max_depth'] = max(counts['max_depth'], depth)
        pivot = numbers[high]
        store_index = low
        for scan_index in range(low, high):
            counts['comparisons'] += 1
            if capture_frames:
                _record_frame(
                    frames,
                    numbers,
                    [scan_index, high],
                    f'Compare {numbers[scan_index]} against pivot {pivot}',
                    counts,
                )
            if numbers[scan_index] <= pivot:
                if store_index != scan_index:
                    numbers[store_index], numbers[scan_index] = numbers[scan_index], numbers[store_index]
                    counts['swaps'] += 1
                    counts['writes'] += 2
                    if capture_frames:
                        _record_frame(
                            frames,
                            numbers,
                            [store_index, scan_index],
                            f'Swap values to grow pivot-left partition around {pivot}',
                            counts,
                        )
                store_index += 1
        if store_index != high:
            numbers[store_index], numbers[high] = numbers[high], numbers[store_index]
            counts['swaps'] += 1
            counts['writes'] += 2
        if capture_frames:
            _record_frame(
                frames,
                numbers,
                [store_index],
                f'Place pivot {pivot} at sorted position {store_index}',
                counts,
            )
        return store_index

    def quicksort(low: int, high: int, depth: int) -> None:
        counts['max_depth'] = max(counts['max_depth'], depth)
        if low >= high:
            return
        pivot_index = partition(low, high, depth)
        quicksort(low, pivot_index - 1, depth + 1)
        quicksort(pivot_index + 1, high, depth + 1)

    started = time.perf_counter()
    if numbers:
        quicksort(0, len(numbers) - 1, 1)
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    if capture_frames:
        _record_frame(frames, numbers, [], 'Array sorted', counts)
    return {
        'sorted_values': numbers,
        'counts': counts,
        'elapsed_ms': elapsed_ms,
        'frames': frames,
    }


def _run_mergesort(values: List[int], capture_frames: bool = True) -> Dict[str, Any]:
    """Run mergesort with deterministic instrumentation."""
    numbers = list(values)
    counts = _new_counts()
    frames: List[Dict[str, Any]] = []

    if capture_frames:
        _record_frame(frames, numbers, [], 'Initial state', counts)

    def mergesort(start: int, end: int, depth: int) -> None:
        counts['max_depth'] = max(counts['max_depth'], depth)
        if end - start <= 1:
            return
        middle = (start + end) // 2
        mergesort(start, middle, depth + 1)
        mergesort(middle, end, depth + 1)

        left = numbers[start:middle]
        right = numbers[middle:end]
        left_index = 0
        right_index = 0
        target = start

        while left_index < len(left) and right_index < len(right):
            counts['comparisons'] += 1
            if left[left_index] <= right[right_index]:
                numbers[target] = left[left_index]
                left_index += 1
            else:
                numbers[target] = right[right_index]
                right_index += 1
            counts['writes'] += 1
            if capture_frames:
                _record_frame(
                    frames,
                    numbers,
                    [target],
                    f'Merge segment [{start}:{end}) back into the main array',
                    counts,
                )
            target += 1

        while left_index < len(left):
            numbers[target] = left[left_index]
            left_index += 1
            target += 1
            counts['writes'] += 1
            if capture_frames:
                _record_frame(frames, numbers, [target - 1], f'Flush left remainder for [{start}:{end})', counts)

        while right_index < len(right):
            numbers[target] = right[right_index]
            right_index += 1
            target += 1
            counts['writes'] += 1
            if capture_frames:
                _record_frame(frames, numbers, [target - 1], f'Flush right remainder for [{start}:{end})', counts)

    started = time.perf_counter()
    mergesort(0, len(numbers), 1)
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    if capture_frames:
        _record_frame(frames, numbers, [], 'Array sorted', counts)
    return {
        'sorted_values': numbers,
        'counts': counts,
        'elapsed_ms': elapsed_ms,
        'frames': frames,
    }


def _run_heapsort(values: List[int], capture_frames: bool = True) -> Dict[str, Any]:
    """Run heapsort with deterministic instrumentation."""
    numbers = list(values)
    counts = _new_counts()
    frames: List[Dict[str, Any]] = []

    if capture_frames:
        _record_frame(frames, numbers, [], 'Initial state', counts)

    def sift_down(root: int, end: int, depth: int) -> None:
        counts['max_depth'] = max(counts['max_depth'], depth)
        while True:
            left = 2 * root + 1
            right = left + 1
            largest = root

            if left < end:
                counts['comparisons'] += 1
                if numbers[left] > numbers[largest]:
                    largest = left
            if right < end:
                counts['comparisons'] += 1
                if numbers[right] > numbers[largest]:
                    largest = right
            if largest == root:
                return

            numbers[root], numbers[largest] = numbers[largest], numbers[root]
            counts['swaps'] += 1
            counts['writes'] += 2
            if capture_frames:
                _record_frame(
                    frames,
                    numbers,
                    [root, largest],
                    'Restore max-heap order by sifting the root downward',
                    counts,
                )
            root = largest
            depth += 1
            counts['max_depth'] = max(counts['max_depth'], depth)

    started = time.perf_counter()
    for root in range(len(numbers) // 2 - 1, -1, -1):
        sift_down(root, len(numbers), 1)
    if capture_frames:
        _record_frame(frames, numbers, [0], 'Max heap constructed', counts)

    for end in range(len(numbers) - 1, 0, -1):
        numbers[0], numbers[end] = numbers[end], numbers[0]
        counts['swaps'] += 1
        counts['writes'] += 2
        if capture_frames:
            _record_frame(
                frames,
                numbers,
                [0, end],
                f'Move current maximum into final position {end}',
                counts,
            )
        sift_down(0, end, 1)

    elapsed_ms = (time.perf_counter() - started) * 1000.0
    if capture_frames:
        _record_frame(frames, numbers, [], 'Array sorted', counts)
    return {
        'sorted_values': numbers,
        'counts': counts,
        'elapsed_ms': elapsed_ms,
        'frames': frames,
    }


ALGORITHM_RUNNERS = {
    'quicksort': _run_quicksort,
    'mergesort': _run_mergesort,
    'heapsort': _run_heapsort,
}


def _run_demo_algorithms(config: Dict[str, Any], demo_values: List[int]) -> List[Dict[str, Any]]:
    """Run each algorithm on the main lesson array and collect trace reports."""
    reports = []
    for algorithm in config['algorithms']:
        result = ALGORITHM_RUNNERS[algorithm](demo_values, capture_frames=True)
        reports.append(
            create_algorithm_report(
                algorithm=algorithm,
                sorted_values=result['sorted_values'],
                comparisons=result['counts']['comparisons'],
                writes=result['counts']['writes'],
                swaps=result['counts']['swaps'],
                max_depth=result['counts']['max_depth'],
                elapsed_ms=result['elapsed_ms'],
                frame_count=len(result['frames']),
                sampled_frames=_sample_frames(result['frames'], config['storyboard_frames']),
            )
        )
    return reports


def _generate_random_array(size: int, rng: random.Random) -> List[int]:
    """Generate one reproducible benchmark array."""
    return [rng.randint(1, size * 12) for _ in range(size)]


def _run_benchmark(config: Dict[str, Any], rng: random.Random) -> List[Dict[str, Any]]:
    """Benchmark each algorithm across multiple array sizes and trials."""
    points: List[Dict[str, Any]] = []
    for size in config['benchmark_sizes']:
        for trial in range(1, config['benchmark_trials'] + 1):
            source_values = _generate_random_array(size, rng)
            for algorithm in config['algorithms']:
                result = ALGORITHM_RUNNERS[algorithm](source_values, capture_frames=False)
                points.append(
                    create_benchmark_point(
                        algorithm=algorithm,
                        array_size=size,
                        trial=trial,
                        elapsed_ms=result['elapsed_ms'],
                        comparisons=result['counts']['comparisons'],
                        writes=result['counts']['writes'],
                        swaps=result['counts']['swaps'],
                    )
                )
    return points


def _aggregate_benchmark(benchmark_points: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, float]]]:
    """Average benchmark measurements by algorithm and array size."""
    grouped: Dict[str, Dict[int, List[Dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for point in benchmark_points:
        grouped[point['algorithm']][point['array_size']].append(point)

    summary: Dict[str, List[Dict[str, float]]] = {}
    for algorithm, sizes in grouped.items():
        summary[algorithm] = []
        for array_size in sorted(sizes):
            points = sizes[array_size]
            summary[algorithm].append(
                {
                    'array_size': array_size,
                    'elapsed_ms': round(mean(point['elapsed_ms'] for point in points), 5),
                    'comparisons': round(mean(point['comparisons'] for point in points), 2),
                    'writes': round(mean(point['writes'] for point in points), 2),
                    'swaps': round(mean(point['swaps'] for point in points), 2),
                    'primitive_ops': round(mean(point['primitive_ops'] for point in points), 2),
                }
            )
    return summary


def _save_storyboard_plot(algorithm_reports: List[Dict[str, Any]], session_id: str) -> str:
    """Persist a storyboard of sampled sort states for each algorithm."""
    max_frames = max(len(report['sampled_frames']) for report in algorithm_reports)
    figure, axes = plt.subplots(len(algorithm_reports), max_frames, figsize=(3.2 * max_frames, 2.8 * len(algorithm_reports)))

    if len(algorithm_reports) == 1:
        axes = [axes]
    for row_index, report in enumerate(algorithm_reports):
        row_axes = axes[row_index] if max_frames > 1 else [axes[row_index]]
        for column_index in range(max_frames):
            axis = row_axes[column_index]
            if column_index >= len(report['sampled_frames']):
                axis.axis('off')
                continue
            frame = report['sampled_frames'][column_index]
            colors = [ALGORITHM_COLORS[report['algorithm']]] * len(frame['values'])
            for active_index in frame['active_indices']:
                if 0 <= active_index < len(colors):
                    colors[active_index] = '#d62828'
            axis.bar(range(len(frame['values'])), frame['values'], color=colors, width=0.85)
            axis.set_title(f"{ALGORITHM_LABELS[report['algorithm']]} | step {frame['step']}", fontsize=9)
            axis.set_xticks([])
            axis.set_yticks([])
            axis.text(0.02, 0.95, frame['note'], transform=axis.transAxes, fontsize=7, va='top')
        row_axes[0].set_ylabel(ALGORITHM_LABELS[report['algorithm']], fontsize=9)

    figure.suptitle('Sorting Storyboard Across Algorithms', fontsize=14)
    figure.tight_layout(rect=[0, 0, 1, 0.96])
    file_path = OUTPUTS_DIR / f'storyboard_{session_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def _save_runtime_chart(benchmark_summary: Dict[str, List[Dict[str, float]]], session_id: str) -> str:
    """Persist average runtime chart across benchmark sizes."""
    figure, axis = plt.subplots(figsize=(8.5, 4.8))
    for algorithm, points in benchmark_summary.items():
        axis.plot(
            [point['array_size'] for point in points],
            [point['elapsed_ms'] for point in points],
            marker='o',
            linewidth=2,
            color=ALGORITHM_COLORS[algorithm],
            label=ALGORITHM_LABELS[algorithm],
        )
    axis.set_title('Average Runtime by Input Size')
    axis.set_xlabel('Array size')
    axis.set_ylabel('Elapsed time (ms)')
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()
    file_path = OUTPUTS_DIR / f'runtime_{session_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def _save_operations_chart(benchmark_summary: Dict[str, List[Dict[str, float]]], session_id: str) -> str:
    """Persist average primitive-operations chart across benchmark sizes."""
    figure, axis = plt.subplots(figsize=(8.5, 4.8))
    for algorithm, points in benchmark_summary.items():
        axis.plot(
            [point['array_size'] for point in points],
            [point['primitive_ops'] for point in points],
            marker='o',
            linewidth=2,
            color=ALGORITHM_COLORS[algorithm],
            label=ALGORITHM_LABELS[algorithm],
        )
    axis.set_title('Average Primitive Operations by Input Size')
    axis.set_xlabel('Array size')
    axis.set_ylabel('Comparisons + writes + swaps')
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()
    file_path = OUTPUTS_DIR / f'operations_{session_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def load_visualizer_profile() -> Dict[str, Any]:
    """Return startup profile built from previously saved catalogs."""
    ensure_data_dirs()
    run_catalog = load_run_catalog()
    library = load_array_library()
    recent_runs = [
        f"{item.get('session_id', '')}:{item.get('fastest_algorithm', '')}:{item.get('demo_array_label', '')}"
        for item in run_catalog[-5:]
    ]
    return {
        'catalog_file': 'data/runs.json',
        'library_file': 'data/array_sets.json',
        'runs_stored': len(run_catalog),
        'arrays_available': len(library),
        'recent_runs': recent_runs,
    }


def run_core_flow() -> Dict[str, Any]:
    """Run one complete sorting lesson, benchmark, and visualization session."""
    ensure_data_dirs()
    config = create_visualizer_config()
    session_id = _session_id()
    rng = random.Random(config['random_seed'])
    started = time.perf_counter()

    array_library = load_array_library()
    if not array_library:
        array_library = _default_array_library()
        save_array_library(array_library)

    demo_record = next(
        (record for record in array_library if record['label'] == config['demo_array_label']),
        array_library[0],
    )
    demo_values = list(demo_record['values'])

    algorithm_reports = _run_demo_algorithms(config, demo_values)
    benchmark_points = _run_benchmark(config, rng)
    benchmark_summary = _aggregate_benchmark(benchmark_points)

    trace_payload = {
        'session_id': session_id,
        'config': config,
        'demo_array': demo_record,
        'algorithm_reports': algorithm_reports,
    }
    benchmark_payload = {
        'session_id': session_id,
        'config': config,
        'summary': benchmark_summary,
        'points': benchmark_points,
    }

    storyboard_file = ''
    runtime_chart_file = ''
    operations_chart_file = ''
    if config['include_storyboard_plot']:
        storyboard_file = _save_storyboard_plot(algorithm_reports, session_id)
    if config['include_runtime_chart']:
        runtime_chart_file = _save_runtime_chart(benchmark_summary, session_id)
    if config['include_operations_chart']:
        operations_chart_file = _save_operations_chart(benchmark_summary, session_id)

    trace_file = save_trace_file(trace_payload, session_id)
    benchmark_file = save_benchmark_file(benchmark_payload, session_id)

    elapsed_ms = (time.perf_counter() - started) * 1000.0
    runtime_leaderboard = sorted(
        [
            (
                algorithm,
                mean(point['elapsed_ms'] for point in benchmark_points if point['algorithm'] == algorithm),
            )
            for algorithm in config['algorithms']
        ],
        key=lambda item: item[1],
    )
    operations_leaderboard = sorted(
        [
            (
                report['algorithm'],
                report['comparisons'] + report['writes'] + report['swaps'],
            )
            for report in algorithm_reports
        ],
        key=lambda item: item[1],
    )

    metrics: Dict[str, Any] = {
        'fastest_algorithm': runtime_leaderboard[0][0] if runtime_leaderboard else '',
        'fastest_runtime_ms': round(runtime_leaderboard[0][1], 5) if runtime_leaderboard else 0.0,
        'lowest_demo_ops_algorithm': operations_leaderboard[0][0] if operations_leaderboard else '',
        'lowest_demo_ops': operations_leaderboard[0][1] if operations_leaderboard else 0,
        'storyboard_frames_per_algorithm': config['storyboard_frames'],
        'benchmark_trials': config['benchmark_trials'],
        'largest_array_size': max(config['benchmark_sizes']) if config['benchmark_sizes'] else 0,
    }

    artifacts = {
        'trace_file': trace_file,
        'benchmark_file': benchmark_file,
        'storyboard_file': storyboard_file,
        'runtime_chart_file': runtime_chart_file,
        'operations_chart_file': operations_chart_file,
    }

    summary = create_session_summary(
        session_id=session_id,
        arrays_available=len(array_library),
        demo_array_label=demo_record['label'],
        demo_array_length=len(demo_values),
        algorithms_run=len(algorithm_reports),
        benchmark_points=len(benchmark_points),
        elapsed_ms=elapsed_ms,
        artifacts=artifacts,
        algorithm_previews=algorithm_reports[: config['max_algorithms_in_report']],
        metrics=metrics,
    )

    run_record = dict(summary)
    session_file = save_run_record(run_record)
    summary['artifacts']['session_file'] = session_file
    return summary
