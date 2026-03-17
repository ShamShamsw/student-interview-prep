"""Business logic for Project 45: Interactive Unit Converter Plus Calculator."""

from __future__ import annotations

import ast
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
    create_conversion_case,
    create_conversion_result,
    create_converter_config,
    create_expression_result,
    create_history_entry,
    create_runtime_point,
    create_session_summary,
)
from storage import (
    OUTPUTS_DIR,
    ensure_data_dirs,
    load_case_library,
    load_history,
    load_run_catalog,
    save_benchmark_file,
    save_case_library,
    save_history,
    save_run_record,
    save_trace_file,
)


LINEAR_CATEGORY_FACTORS = {
    'length': {
        'meter': 1.0,
        'kilometer': 1000.0,
        'centimeter': 0.01,
        'inch': 0.0254,
        'foot': 0.3048,
        'mile': 1609.344,
    },
    'mass': {
        'gram': 1.0,
        'kilogram': 1000.0,
        'pound': 453.59237,
        'ounce': 28.349523125,
    },
    'volume': {
        'liter': 1.0,
        'milliliter': 0.001,
        'gallon': 3.785411784,
        'cup': 0.2365882365,
    },
    'speed': {
        'mps': 1.0,
        'kph': 0.2777777778,
        'mph': 0.44704,
    },
    'time': {
        'second': 1.0,
        'minute': 60.0,
        'hour': 3600.0,
    },
}

CATEGORY_COLORS = {
    'length': '#264653',
    'mass': '#2a9d8f',
    'temperature': '#e76f51',
    'volume': '#f4a261',
    'speed': '#457b9d',
    'time': '#8ab17d',
    'calculator': '#6d597a',
}

SUPPORTED_CATEGORIES = ['length', 'mass', 'temperature', 'volume', 'speed', 'time']


def _session_id() -> str:
    """Build a compact session ID from UTC timestamp."""
    return datetime.utcnow().strftime('%Y%m%d_%H%M%S')


def _default_case_library() -> List[Dict[str, Any]]:
    """Return deterministic starter conversion cases used on first run."""
    return [
        create_conversion_case(
            case_id='case_001',
            label='lesson_everyday_mix',
            category='length',
            from_unit='mile',
            to_unit='kilometer',
            value=3.0,
            description='Convert running distance to metric.',
            tags=['distance', 'fitness'],
        ),
        create_conversion_case(
            case_id='case_002',
            label='lesson_everyday_mix',
            category='temperature',
            from_unit='fahrenheit',
            to_unit='celsius',
            value=72.0,
            description='Convert room temperature.',
            tags=['weather'],
        ),
        create_conversion_case(
            case_id='case_003',
            label='lesson_everyday_mix',
            category='mass',
            from_unit='pound',
            to_unit='kilogram',
            value=180.0,
            description='Convert body weight units.',
            tags=['health'],
        ),
        create_conversion_case(
            case_id='case_004',
            label='lesson_everyday_mix',
            category='volume',
            from_unit='gallon',
            to_unit='liter',
            value=2.5,
            description='Convert fuel volume.',
            tags=['travel'],
        ),
        create_conversion_case(
            case_id='case_005',
            label='lesson_everyday_mix',
            category='speed',
            from_unit='mph',
            to_unit='kph',
            value=65.0,
            description='Convert speed limit signs.',
            tags=['driving'],
        ),
        create_conversion_case(
            case_id='case_006',
            label='lesson_everyday_mix',
            category='time',
            from_unit='hour',
            to_unit='minute',
            value=2.5,
            description='Convert meeting length units.',
            tags=['scheduling'],
        ),
    ]


def _to_celsius(value: float, unit: str) -> float:
    """Convert a temperature value to Celsius."""
    normalized = unit.lower()
    if normalized == 'celsius':
        return value
    if normalized == 'fahrenheit':
        return (value - 32.0) * (5.0 / 9.0)
    if normalized == 'kelvin':
        return value - 273.15
    raise ValueError(f'Unsupported temperature unit: {unit}')


def _from_celsius(value: float, unit: str) -> float:
    """Convert a Celsius temperature value into the target unit."""
    normalized = unit.lower()
    if normalized == 'celsius':
        return value
    if normalized == 'fahrenheit':
        return (value * 9.0 / 5.0) + 32.0
    if normalized == 'kelvin':
        return value + 273.15
    raise ValueError(f'Unsupported temperature unit: {unit}')


def convert_units(category: str, value: float, from_unit: str, to_unit: str) -> float:
    """Convert one numeric value between units inside the same category."""
    normalized_category = category.lower()
    source = from_unit.lower()
    target = to_unit.lower()

    if normalized_category == 'temperature':
        celsius = _to_celsius(float(value), source)
        return _from_celsius(celsius, target)

    if normalized_category not in LINEAR_CATEGORY_FACTORS:
        raise ValueError(f'Unsupported category: {category}')

    factors = LINEAR_CATEGORY_FACTORS[normalized_category]
    if source not in factors or target not in factors:
        raise ValueError(f'Unsupported unit conversion: {from_unit} -> {to_unit} in {category}')

    base_value = float(value) * factors[source]
    return base_value / factors[target]


def _safe_eval_ast(node: ast.AST) -> float:
    """Evaluate a restricted arithmetic AST safely."""
    if isinstance(node, ast.Expression):
        return _safe_eval_ast(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        operand = _safe_eval_ast(node.operand)
        return operand if isinstance(node.op, ast.UAdd) else -operand
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv)):
        left = _safe_eval_ast(node.left)
        right = _safe_eval_ast(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Pow):
            return left**right
        if isinstance(node.op, ast.Mod):
            return left % right
        if isinstance(node.op, ast.FloorDiv):
            return left // right
    raise ValueError('Expression contains unsupported operations.')


def evaluate_expression(expression: str) -> float:
    """Evaluate calculator expressions using a safe parser."""
    tree = ast.parse(expression, mode='eval')
    for node in ast.walk(tree):
        if isinstance(node, (ast.Call, ast.Name, ast.Attribute, ast.Subscript, ast.List, ast.Dict, ast.Tuple)):
            raise ValueError('Expression contains disallowed syntax.')
    return _safe_eval_ast(tree)


def _run_conversion_demo(cases: List[Dict[str, Any]], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Run configured conversion cases for the lesson demo."""
    results: List[Dict[str, Any]] = []
    for case in cases:
        if case['category'] not in config['enabled_categories']:
            continue
        started = time.perf_counter()
        output_value = convert_units(case['category'], case['value'], case['from_unit'], case['to_unit'])
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        results.append(
            create_conversion_result(
                category=case['category'],
                from_unit=case['from_unit'],
                to_unit=case['to_unit'],
                input_value=case['value'],
                output_value=output_value,
                elapsed_ms=elapsed_ms,
            )
        )
    return results


def _run_expression_demo(expressions: List[str]) -> List[Dict[str, Any]]:
    """Run calculator expression suite and record timing."""
    results: List[Dict[str, Any]] = []
    for expression in expressions:
        started = time.perf_counter()
        valid = True
        numeric_result = 0.0
        try:
            numeric_result = evaluate_expression(expression)
        except (SyntaxError, ValueError, ZeroDivisionError):
            valid = False
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        results.append(create_expression_result(expression, numeric_result, elapsed_ms, valid))
    return results


def _benchmark_category_runtime(config: Dict[str, Any], rng: random.Random) -> List[Dict[str, Any]]:
    """Benchmark conversion runtime by category and input magnitude."""
    exemplar_units = {
        'length': ('meter', 'mile'),
        'mass': ('gram', 'pound'),
        'temperature': ('celsius', 'fahrenheit'),
        'volume': ('liter', 'gallon'),
        'speed': ('mps', 'mph'),
        'time': ('second', 'hour'),
    }
    points: List[Dict[str, Any]] = []
    for category in config['enabled_categories']:
        source, target = exemplar_units[category]
        for size in config['benchmark_magnitudes']:
            for trial in range(1, config['benchmark_trials'] + 1):
                jitter = 1.0 + rng.uniform(-0.03, 0.03)
                value = float(size) * jitter
                started = time.perf_counter()
                convert_units(category, value, source, target)
                elapsed = (time.perf_counter() - started) * 1000.0
                points.append(create_runtime_point(category, size, trial, elapsed))
    return points


def _benchmark_expression_runtime(expressions: List[str], trials: int) -> List[Dict[str, Any]]:
    """Benchmark expression parser runtime."""
    points: List[Dict[str, Any]] = []
    for expression in expressions:
        expression_size = float(len(expression))
        for trial in range(1, trials + 1):
            started = time.perf_counter()
            try:
                evaluate_expression(expression)
            except (SyntaxError, ValueError, ZeroDivisionError):
                pass
            elapsed = (time.perf_counter() - started) * 1000.0
            points.append(create_runtime_point('calculator', expression_size, trial, elapsed))
    return points


def _aggregate_runtime(points: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, float]]]:
    """Average runtime benchmark points by series and size."""
    grouped: Dict[str, Dict[float, List[float]]] = defaultdict(lambda: defaultdict(list))
    for point in points:
        grouped[point['series']][point['size']].append(point['elapsed_ms'])

    summary: Dict[str, List[Dict[str, float]]] = {}
    for series, size_buckets in grouped.items():
        rows: List[Dict[str, float]] = []
        for size in sorted(size_buckets):
            rows.append({'size': size, 'elapsed_ms': round(mean(size_buckets[size]), 6)})
        summary[series] = rows
    return summary


def _save_category_chart(runtime_summary: Dict[str, List[Dict[str, float]]], session_id: str) -> str:
    """Persist conversion and calculator runtime chart."""
    figure, axis = plt.subplots(figsize=(9.2, 5.0))
    for series, rows in runtime_summary.items():
        axis.plot(
            [row['size'] for row in rows],
            [row['elapsed_ms'] for row in rows],
            marker='o',
            linewidth=2,
            label=series.title(),
            color=CATEGORY_COLORS.get(series, '#6c757d'),
        )
    axis.set_title('Average Runtime By Conversion Category And Calculator')
    axis.set_xlabel('Input magnitude (or expression length)')
    axis.set_ylabel('Elapsed time (ms)')
    axis.grid(alpha=0.25)
    axis.legend(ncol=2)
    figure.tight_layout()
    file_path = OUTPUTS_DIR / f'category_runtime_{session_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def _save_history_chart(expressions: List[Dict[str, Any]], session_id: str) -> str:
    """Persist plot of calculator results across expression order."""
    valid_rows = [row for row in expressions if row.get('valid')]
    figure, axis = plt.subplots(figsize=(8.8, 4.8))
    if valid_rows:
        axis.plot(
            list(range(1, len(valid_rows) + 1)),
            [row['result'] for row in valid_rows],
            marker='o',
            linewidth=2,
            color=CATEGORY_COLORS['calculator'],
        )
    axis.set_title('Calculated Value Trend Across Expression Sequence')
    axis.set_xlabel('Expression index')
    axis.set_ylabel('Result value')
    axis.grid(alpha=0.25)
    figure.tight_layout()
    file_path = OUTPUTS_DIR / f'history_trend_{session_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def load_converter_profile() -> Dict[str, Any]:
    """Return startup profile built from previously saved catalogs."""
    ensure_data_dirs()
    run_catalog = load_run_catalog()
    library = load_case_library()
    history = load_history()
    recent_runs = [
        f"{item.get('session_id', '')}:{item.get('fastest_series', '')}:{item.get('demo_sequence_label', '')}"
        for item in run_catalog[-5:]
    ]
    return {
        'catalog_file': 'data/runs.json',
        'library_file': 'data/conversion_sets.json',
        'history_file': 'data/calculator_history.json',
        'runs_stored': len(run_catalog),
        'cases_available': len(library),
        'history_entries': len(history),
        'recent_runs': recent_runs,
    }


def run_core_flow() -> Dict[str, Any]:
    """Run one complete converter, calculator, benchmark, and plotting session."""
    ensure_data_dirs()
    config = create_converter_config()
    session_id = _session_id()
    rng = random.Random(config['random_seed'])
    started = time.perf_counter()

    case_library = load_case_library()
    if not case_library:
        case_library = _default_case_library()
        save_case_library(case_library)

    demo_cases = [case for case in case_library if case['label'] == config['demo_sequence_label']]
    if not demo_cases:
        demo_cases = case_library[:]

    conversion_results = _run_conversion_demo(demo_cases, config)
    expression_results = _run_expression_demo(config['expression_suite'])

    conversion_history_entries = [create_history_entry('conversion', row) for row in conversion_results]
    expression_history_entries = [create_history_entry('expression', row) for row in expression_results]

    history = load_history()
    history.extend(conversion_history_entries)
    history.extend(expression_history_entries)
    history = history[-400:]
    history_file = save_history(history)

    conversion_runtime_points = _benchmark_category_runtime(config, rng)
    expression_runtime_points = _benchmark_expression_runtime(config['expression_suite'], config['benchmark_trials'])
    runtime_points = conversion_runtime_points + expression_runtime_points
    runtime_summary = _aggregate_runtime(runtime_points)

    trace_payload = {
        'session_id': session_id,
        'config': config,
        'cases': demo_cases,
        'conversions': conversion_results,
        'expressions': expression_results,
        'history_file': history_file,
    }
    benchmark_payload = {
        'session_id': session_id,
        'runtime_points': runtime_points,
        'runtime_summary': runtime_summary,
    }

    category_chart_file = ''
    history_chart_file = ''
    if config['include_category_plot']:
        category_chart_file = _save_category_chart(runtime_summary, session_id)
    if config['include_history_plot']:
        history_chart_file = _save_history_chart(expression_results, session_id)

    trace_file = save_trace_file(trace_payload, session_id)
    benchmark_file = save_benchmark_file(benchmark_payload, session_id)
    elapsed_ms = (time.perf_counter() - started) * 1000.0

    average_by_series = {
        series: mean(row['elapsed_ms'] for row in rows)
        for series, rows in runtime_summary.items()
        if rows
    }
    fastest_series = min(average_by_series.items(), key=lambda item: item[1])[0] if average_by_series else ''
    valid_expression_results = [row['result'] for row in expression_results if row['valid']]

    metrics = {
        'fastest_series': fastest_series,
        'fastest_avg_runtime_ms': round(average_by_series.get(fastest_series, 0.0), 6),
        'avg_expression_result': round(mean(valid_expression_results), 6) if valid_expression_results else 0.0,
        'history_size': len(history),
    }

    artifacts = {
        'trace_file': trace_file,
        'benchmark_file': benchmark_file,
        'category_chart_file': category_chart_file,
        'history_chart_file': history_chart_file,
        'history_file': history_file,
    }

    summary = create_session_summary(
        session_id=session_id,
        cases_available=len(case_library),
        demo_sequence_label=config['demo_sequence_label'],
        conversions_run=len(conversion_results),
        expressions_run=len(expression_results),
        runtime_points=len(runtime_points),
        elapsed_ms=elapsed_ms,
        artifacts=artifacts,
        conversion_previews=conversion_results[: config['max_preview_rows']],
        expression_previews=expression_results[: config['max_preview_rows']],
        metrics=metrics,
    )
    summary['history_previews'] = history[-config['max_preview_rows'] :]
    summary['max_preview_rows'] = config['max_preview_rows']

    run_record = dict(summary)
    session_file = save_run_record(run_record)
    summary['artifacts']['session_file'] = session_file
    return summary
