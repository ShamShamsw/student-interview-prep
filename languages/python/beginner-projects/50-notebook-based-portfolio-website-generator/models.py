"""Data models for Project 50: Notebook-Based Portfolio Website Generator."""

from datetime import datetime
from typing import Any, Dict, List


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string."""
    return datetime.utcnow().isoformat(timespec='seconds') + 'Z'


def create_portfolio_config(
    strategy: str = 'adaptive_grid',
    enabled_strategies: List[str] | None = None,
    demo_portfolio_label: str = 'data_science_student',
    max_projects: int = 8,
    max_snippets_per_project: int = 3,
    benchmark_project_counts: List[int] | None = None,
    benchmark_trials: int = 4,
    include_runtime_plot: bool = True,
    include_debt_plot: bool = True,
    max_preview_rows: int = 8,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """Create a validated configuration record for one generator session."""
    strategies = (
        enabled_strategies
        if enabled_strategies
        else ['minimal_slate', 'bold_cards', 'adaptive_grid']
    )
    benchmark_sizes = benchmark_project_counts if benchmark_project_counts else [3, 5, 8, 12, 16]
    normalized_strategy = str(strategy).strip().lower()
    selected_strategy = normalized_strategy if normalized_strategy in strategies else 'adaptive_grid'
    return {
        'project_type': 'notebook_based_portfolio_website_generator',
        'strategy': selected_strategy,
        'enabled_strategies': [str(value) for value in strategies],
        'demo_portfolio_label': str(demo_portfolio_label),
        'max_projects': max(1, int(max_projects)),
        'max_snippets_per_project': max(1, int(max_snippets_per_project)),
        'benchmark_project_counts': [max(1, int(value)) for value in benchmark_sizes],
        'benchmark_trials': max(1, int(benchmark_trials)),
        'include_runtime_plot': bool(include_runtime_plot),
        'include_debt_plot': bool(include_debt_plot),
        'max_preview_rows': max(1, int(max_preview_rows)),
        'random_seed': int(random_seed),
        'created_at': _utc_timestamp(),
    }


def create_portfolio_case(
    portfolio_id: str,
    label: str,
    owner_name: str,
    headline: str,
    about: str,
    projects: List[Dict[str, Any]],
    accent_palette: str,
    preferred_layout: str,
) -> Dict[str, Any]:
    """Create one reusable portfolio source definition record."""
    return {
        'portfolio_id': str(portfolio_id),
        'label': str(label),
        'owner_name': str(owner_name),
        'headline': str(headline),
        'about': str(about),
        'projects': list(projects),
        'accent_palette': str(accent_palette),
        'preferred_layout': str(preferred_layout),
    }


def create_page_record(
    page_index: int,
    strategy: str,
    source_title: str,
    slug: str,
    source_type: str,
    tags: List[str],
    estimated_read_minutes: int,
    section_count: int,
    quality_score: float,
    layout_debt: float,
    cumulative_layout_debt: float,
) -> Dict[str, Any]:
    """Create one generated page summary record."""
    return {
        'page_index': int(page_index),
        'strategy': str(strategy),
        'source_title': str(source_title),
        'slug': str(slug),
        'source_type': str(source_type),
        'tags': [str(tag) for tag in tags],
        'estimated_read_minutes': int(estimated_read_minutes),
        'section_count': int(section_count),
        'quality_score': round(float(quality_score), 6),
        'layout_debt': round(float(layout_debt), 6),
        'cumulative_layout_debt': round(float(cumulative_layout_debt), 6),
    }


def create_strategy_result(
    strategy: str,
    mean_quality_score: float,
    accessibility_score: float,
    seo_score: float,
    cumulative_layout_debt: float,
    pages: List[Dict[str, Any]],
    feasible: bool,
) -> Dict[str, Any]:
    """Create one strategy result record."""
    return {
        'strategy': str(strategy),
        'mean_quality_score': round(float(mean_quality_score), 6),
        'accessibility_score': round(float(accessibility_score), 6),
        'seo_score': round(float(seo_score), 6),
        'cumulative_layout_debt': round(float(cumulative_layout_debt), 6),
        'pages': list(pages),
        'feasible': bool(feasible),
    }


def create_runtime_point(series: str, size: float, trial: int, elapsed_ms: float) -> Dict[str, Any]:
    """Create one benchmark runtime point."""
    return {
        'series': str(series),
        'size': float(size),
        'trial': int(trial),
        'elapsed_ms': round(float(elapsed_ms), 6),
    }


def create_history_entry(event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Create one persistent history entry."""
    return {
        'event_type': str(event_type),
        'payload': dict(payload),
        'created_at': _utc_timestamp(),
    }


def create_session_summary(
    session_id: str,
    portfolios_available: int,
    demo_portfolio_label: str,
    strategy_selected: str,
    strategy_runs: int,
    pages_generated: int,
    runtime_points: int,
    elapsed_ms: float,
    artifacts: Dict[str, Any],
    page_previews: List[Dict[str, Any]],
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """Create final session summary for reporting and persistence."""
    return {
        'session_id': str(session_id),
        'portfolios_available': int(portfolios_available),
        'demo_portfolio_label': str(demo_portfolio_label),
        'strategy_selected': str(strategy_selected),
        'strategy_runs': int(strategy_runs),
        'pages_generated': int(pages_generated),
        'runtime_points': int(runtime_points),
        'elapsed_ms': round(float(elapsed_ms), 5),
        'artifacts': dict(artifacts),
        'page_previews': list(page_previews),
        'metrics': dict(metrics),
        'finished_at': _utc_timestamp(),
    }


def create_record(**kwargs):
    """Backwards-compatible generic record factory."""
    return dict(kwargs)
