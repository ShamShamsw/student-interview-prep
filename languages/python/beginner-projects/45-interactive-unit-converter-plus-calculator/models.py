"""Data models for Project 45: Interactive Unit Converter Plus Calculator."""

from datetime import datetime
from typing import Any, Dict, List


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string."""
    return datetime.utcnow().isoformat(timespec='seconds') + 'Z'


def create_converter_config(
    enabled_categories: List[str] | None = None,
    demo_sequence_label: str = 'lesson_everyday_mix',
    expression_suite: List[str] | None = None,
    benchmark_magnitudes: List[float] | None = None,
    benchmark_trials: int = 4,
    include_category_plot: bool = True,
    include_history_plot: bool = True,
    max_preview_rows: int = 8,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """Create a validated configuration record for one converter session."""
    categories = enabled_categories if enabled_categories else ['length', 'mass', 'temperature', 'volume', 'speed', 'time']
    expressions = expression_suite if expression_suite else [
        '12 + 4 * 3',
        '(18 / 3) + 7.5',
        '2 ** 8 - 17',
        '((5 + 3) * (9 - 2)) / 4',
        '100 / (3 + 2)',
    ]
    magnitudes = benchmark_magnitudes if benchmark_magnitudes else [1, 10, 100, 1000, 10000]
    return {
        'project_type': 'interactive_unit_converter_plus_calculator',
        'enabled_categories': [str(category) for category in categories],
        'demo_sequence_label': str(demo_sequence_label),
        'expression_suite': [str(expression) for expression in expressions],
        'benchmark_magnitudes': [max(0.0001, float(value)) for value in magnitudes],
        'benchmark_trials': max(1, int(benchmark_trials)),
        'include_category_plot': bool(include_category_plot),
        'include_history_plot': bool(include_history_plot),
        'max_preview_rows': max(1, int(max_preview_rows)),
        'random_seed': int(random_seed),
        'created_at': _utc_timestamp(),
    }


def create_conversion_case(
    case_id: str,
    label: str,
    category: str,
    from_unit: str,
    to_unit: str,
    value: float,
    description: str,
    tags: List[str],
) -> Dict[str, Any]:
    """Create one reusable conversion case record."""
    return {
        'case_id': str(case_id),
        'label': str(label),
        'category': str(category),
        'from_unit': str(from_unit),
        'to_unit': str(to_unit),
        'value': float(value),
        'description': str(description),
        'tags': [str(tag) for tag in tags],
    }


def create_conversion_result(
    category: str,
    from_unit: str,
    to_unit: str,
    input_value: float,
    output_value: float,
    elapsed_ms: float,
) -> Dict[str, Any]:
    """Create one conversion output record."""
    return {
        'category': str(category),
        'from_unit': str(from_unit),
        'to_unit': str(to_unit),
        'input_value': round(float(input_value), 8),
        'output_value': round(float(output_value), 8),
        'elapsed_ms': round(float(elapsed_ms), 6),
    }


def create_expression_result(expression: str, result: float, elapsed_ms: float, valid: bool) -> Dict[str, Any]:
    """Create one calculator evaluation result record."""
    return {
        'expression': str(expression),
        'result': round(float(result), 8),
        'elapsed_ms': round(float(elapsed_ms), 6),
        'valid': bool(valid),
    }


def create_history_entry(event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Create one persistent history entry."""
    return {
        'event_type': str(event_type),
        'payload': dict(payload),
        'created_at': _utc_timestamp(),
    }


def create_runtime_point(series: str, size: float, trial: int, elapsed_ms: float) -> Dict[str, Any]:
    """Create one benchmark runtime point."""
    return {
        'series': str(series),
        'size': float(size),
        'trial': int(trial),
        'elapsed_ms': round(float(elapsed_ms), 6),
    }


def create_session_summary(
    session_id: str,
    cases_available: int,
    demo_sequence_label: str,
    conversions_run: int,
    expressions_run: int,
    runtime_points: int,
    elapsed_ms: float,
    artifacts: Dict[str, Any],
    conversion_previews: List[Dict[str, Any]],
    expression_previews: List[Dict[str, Any]],
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """Create final session summary for reporting and persistence."""
    return {
        'session_id': str(session_id),
        'cases_available': int(cases_available),
        'demo_sequence_label': str(demo_sequence_label),
        'conversions_run': int(conversions_run),
        'expressions_run': int(expressions_run),
        'runtime_points': int(runtime_points),
        'elapsed_ms': round(float(elapsed_ms), 5),
        'artifacts': dict(artifacts),
        'conversion_previews': list(conversion_previews),
        'expression_previews': list(expression_previews),
        'metrics': dict(metrics),
        'finished_at': _utc_timestamp(),
    }


def create_record(**kwargs):
    """Backwards-compatible generic record factory."""
    return dict(kwargs)
