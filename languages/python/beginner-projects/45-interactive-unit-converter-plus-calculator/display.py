"""Presentation helpers for Project 45: Interactive Unit Converter Plus Calculator."""

from typing import Any, Dict, List


def format_header() -> str:
    """Format session header banner."""
    return '=' * 70 + '\n' + '   INTERACTIVE UNIT CONVERTER PLUS CALCULATOR\n' + '=' * 70


def format_startup_guide(config: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """Format startup configuration and historical profile."""
    recent = ', '.join(profile.get('recent_runs', [])) or 'None yet'
    lines = [
        '',
        'Configuration:',
        f"   Project type:           {config['project_type']}",
        f"   Categories:             {', '.join(config['enabled_categories'])}",
        f"   Demo sequence:          {config['demo_sequence_label']}",
        f"   Expressions:            {len(config['expression_suite'])}",
        f"   Benchmark magnitudes:   {', '.join(str(int(value)) if float(value).is_integer() else str(value) for value in config['benchmark_magnitudes'])}",
        f"   Trials per magnitude:   {config['benchmark_trials']}",
        f"   Category chart:         {config['include_category_plot']}",
        f"   History chart:          {config['include_history_plot']}",
        f"   Max preview rows:       {config['max_preview_rows']}",
        f"   Random seed:            {config['random_seed']}",
        '',
        'Startup:',
        '   Data directory:         data/',
        '   Outputs directory:      data/outputs/',
        (
            f"   Conversion library:     {profile['library_file']} "
            f"(loaded {profile['cases_available']} cases)"
        ),
        (
            f"   Run catalog:            {profile['catalog_file']} "
            f"(loaded {profile['runs_stored']} runs)"
        ),
        (
            f"   Calculator history:     {profile['history_file']} "
            f"(loaded {profile['history_entries']} entries)"
        ),
        f"   Recent runs:            {recent}",
        '',
        '---',
    ]
    return '\n'.join(lines)


def _clip_preview(value: str, width: int = 30) -> str:
    """Return a compact preview string for table output."""
    compact = value.replace('\n', ' ').strip()
    if len(compact) <= width:
        return compact
    return compact[: width - 3] + '...'


def format_conversion_table(conversions: List[Dict[str, Any]]) -> str:
    """Format conversion preview table."""
    if not conversions:
        return 'No conversion previews generated.'
    lines = [
        'Conversion previews:',
        '   Category     | From         | To           | Input        | Output',
        '   -------------+--------------+--------------+--------------+--------------',
    ]
    for row in conversions:
        lines.append(
            '   '
            f"{_clip_preview(str(row.get('category', '')), 11):<11} | "
            f"{_clip_preview(str(row.get('from_unit', '')), 12):<12} | "
            f"{_clip_preview(str(row.get('to_unit', '')), 12):<12} | "
            f"{row.get('input_value', 0.0):<12.5f} | "
            f"{row.get('output_value', 0.0):<12.5f}"
        )
    return '\n'.join(lines)


def format_expression_table(expressions: List[Dict[str, Any]]) -> str:
    """Format expression preview table."""
    if not expressions:
        return 'No expression previews generated.'
    lines = [
        'Calculator previews:',
        '   Expression                          | Result       | Valid | Time (ms)',
        '   ------------------------------------+--------------+-------+----------',
    ]
    for row in expressions:
        lines.append(
            '   '
            f"{_clip_preview(str(row.get('expression', '')), 34):<34} | "
            f"{row.get('result', 0.0):<12.6f} | "
            f"{'yes' if row.get('valid') else 'no ':<5} | "
            f"{row.get('elapsed_ms', 0.0):<8.5f}"
        )
    return '\n'.join(lines)


def format_history_table(history: List[Dict[str, Any]], max_rows: int) -> str:
    """Format history preview table."""
    if not history:
        return 'No history entries available.'
    lines = [
        'Recent history:',
        '   Event type   | Preview                              | Created at',
        '   -------------+--------------------------------------+----------------------',
    ]
    for row in history[-max_rows:]:
        payload = row.get('payload', {})
        preview = ''
        if row.get('event_type') == 'conversion':
            preview = f"{payload.get('input_value', 0)} {payload.get('from_unit', '')} -> {payload.get('output_value', 0)} {payload.get('to_unit', '')}"
        elif row.get('event_type') == 'expression':
            preview = f"{payload.get('expression', '')} = {payload.get('result', 0)}"
        else:
            preview = str(payload)
        lines.append(
            '   '
            f"{_clip_preview(str(row.get('event_type', '')), 11):<11} | "
            f"{_clip_preview(preview, 36):<36} | "
            f"{_clip_preview(str(row.get('created_at', '')), 20):<20}"
        )
    return '\n'.join(lines)


def format_run_report(summary: Dict[str, Any]) -> str:
    """Format final session report."""
    artifacts = summary.get('artifacts', {})
    metrics = summary.get('metrics', {})
    lines = [
        '',
        'Session complete:',
        f"   Session ID:             {summary['session_id']}",
        f"   Cases available:        {summary['cases_available']}",
        f"   Demo sequence:          {summary['demo_sequence_label']}",
        f"   Conversions run:        {summary['conversions_run']}",
        f"   Expressions run:        {summary['expressions_run']}",
        f"   Runtime points:         {summary['runtime_points']}",
        f"   Elapsed time:           {summary['elapsed_ms']:.2f} ms",
        '',
        (
            'Toolkit metrics: '
            f"fastest_series={metrics.get('fastest_series', 'N/A')} | "
            f"fastest_avg_runtime_ms={metrics.get('fastest_avg_runtime_ms', 0.0):.6f} | "
            f"avg_expression_result={metrics.get('avg_expression_result', 0.0):.5f} | "
            f"history_size={metrics.get('history_size', 0)}"
        ),
        '',
        format_conversion_table(summary.get('conversion_previews', [])),
        '',
        format_expression_table(summary.get('expression_previews', [])),
        '',
        format_history_table(summary.get('history_previews', []), max_rows=summary.get('max_preview_rows', 8)),
        '',
        'Artifacts saved:',
        f"   Session record:         {artifacts.get('session_file', 'N/A')}",
        f"   Trace bundle:           {artifacts.get('trace_file', 'N/A')}",
        f"   Benchmark file:         {artifacts.get('benchmark_file', 'N/A')}",
        f"   Category chart:         {artifacts.get('category_chart_file', 'N/A')}",
        f"   History chart:          {artifacts.get('history_chart_file', 'N/A')}",
    ]
    return '\n'.join(lines)


def format_message(message: str) -> str:
    """Format a user-facing message string."""
    return f'[Project 45] {message}'
