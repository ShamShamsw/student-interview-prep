"""Business logic for Project 50: Notebook-Based Portfolio Website Generator."""

from __future__ import annotations

import random
import re
import time
from collections import defaultdict
from datetime import datetime
from statistics import mean
from typing import Any, Dict, List

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

from models import (
    create_history_entry,
    create_page_record,
    create_portfolio_case,
    create_portfolio_config,
    create_runtime_point,
    create_session_summary,
    create_strategy_result,
)
from storage import (
    OUTPUTS_DIR,
    ensure_data_dirs,
    load_history,
    load_portfolio_library,
    load_run_catalog,
    save_benchmark_file,
    save_history,
    save_portfolio_library,
    save_run_record,
    save_trace_file,
)


PLOT_COLORS = {
    'minimal_slate': '#d95f02',
    'bold_cards': '#1b9e77',
    'adaptive_grid': '#2c3e50',
    'selected_plan': '#e76f51',
}


def _session_id() -> str:
    """Build a compact session ID from UTC timestamp."""
    return datetime.utcnow().strftime('%Y%m%d_%H%M%S')


def _slugify(value: str) -> str:
    """Create a URL-safe slug from a title."""
    lowered = re.sub(r'[^a-z0-9]+', '-', str(value).strip().lower())
    return lowered.strip('-') or 'untitled-project'


def _default_portfolio_library() -> List[Dict[str, Any]]:
    """Return deterministic starter portfolio definitions used on first run."""
    return [
        create_portfolio_case(
            portfolio_id='portfolio_001',
            label='data_science_student',
            owner_name='Alex Johnson',
            headline='Building practical machine learning projects with strong storytelling.',
            about=(
                'Computer science student focused on reproducible experiments, clean analysis, '
                'and simple user-facing demos.'
            ),
            accent_palette='sunset_orange',
            preferred_layout='grid',
            projects=[
                {
                    'project_id': 'proj_001',
                    'title': 'Retail Demand Forecasting Notebook',
                    'source_type': 'notebook',
                    'tags': ['python', 'forecasting', 'timeseries'],
                    'highlights': [
                        'Compared ARIMA and gradient boosting baseline models.',
                        'Documented feature ablations and confidence intervals.',
                        'Published clear visual diagnostics for weekly seasonality.',
                    ],
                },
                {
                    'project_id': 'proj_002',
                    'title': 'Medical Text Summarization Report',
                    'source_type': 'markdown',
                    'tags': ['nlp', 'transformers', 'evaluation'],
                    'highlights': [
                        'Built synthetic benchmark pipeline for summarization quality checks.',
                        'Tracked ROUGE trends and failure examples by category.',
                        'Added clinician-friendly report formatting for review.',
                    ],
                },
                {
                    'project_id': 'proj_003',
                    'title': 'Interactive Fraud Detection Walkthrough',
                    'source_type': 'notebook',
                    'tags': ['classification', 'xgboost', 'dashboard'],
                    'highlights': [
                        'Balanced precision-recall tradeoffs for analyst workflows.',
                        'Explained threshold tuning with cost-sensitive scoring.',
                        'Exported confusion trends and drift snapshots.',
                    ],
                },
                {
                    'project_id': 'proj_004',
                    'title': 'Portfolio Reflection Essay',
                    'source_type': 'markdown',
                    'tags': ['writing', 'communication', 'career'],
                    'highlights': [
                        'Summarized technical growth and team collaboration outcomes.',
                        'Mapped projects to measurable impact and learning goals.',
                        'Outlined next milestones for production-ready ML delivery.',
                    ],
                },
            ],
        ),
        create_portfolio_case(
            portfolio_id='portfolio_002',
            label='fullstack_builder',
            owner_name='Sam Rivera',
            headline='Shipping data-backed web apps from prototype to deployment.',
            about='Full-stack developer blending product thinking with analytics instrumentation.',
            accent_palette='ocean_blue',
            preferred_layout='magazine',
            projects=[
                {
                    'project_id': 'proj_005',
                    'title': 'A/B Testing Notebook For Checkout Funnel',
                    'source_type': 'notebook',
                    'tags': ['experimentation', 'statistics', 'product'],
                    'highlights': [
                        'Designed robust randomization and significance checks.',
                        'Built annotation-rich plots for stakeholder review.',
                    ],
                },
                {
                    'project_id': 'proj_006',
                    'title': 'Developer Blog Series Generator',
                    'source_type': 'markdown',
                    'tags': ['automation', 'content', 'developer-experience'],
                    'highlights': [
                        'Converted engineering notes into release-ready writeups.',
                        'Added SEO metadata and accessibility-first heading structure.',
                    ],
                },
            ],
        ),
    ]


def _estimate_read_minutes(project: Dict[str, Any]) -> int:
    """Estimate read time from textual highlights."""
    joined = ' '.join(str(line) for line in project.get('highlights', []))
    words = len(joined.split())
    return max(1, round(words / 160.0))


def _score_project(project: Dict[str, Any], strategy: str, rng: random.Random) -> Dict[str, float]:
    """Estimate quality scores for one project under a strategy."""
    source_type = str(project.get('source_type', 'markdown'))
    tags = project.get('tags', [])
    highlight_count = len(project.get('highlights', []))

    base_quality = 0.72 + (0.025 * min(6, len(tags))) + (0.03 * min(4, highlight_count))
    notebook_bonus = 0.03 if source_type == 'notebook' else 0.0
    markdown_bonus = 0.02 if source_type == 'markdown' else 0.0

    if strategy == 'minimal_slate':
        quality_bias = 0.02 + markdown_bonus
        accessibility_bias = 0.05
        seo_bias = 0.03
    elif strategy == 'bold_cards':
        quality_bias = 0.03 + notebook_bonus
        accessibility_bias = 0.01
        seo_bias = 0.02
    else:
        quality_bias = 0.04 + (0.5 * notebook_bonus) + (0.5 * markdown_bonus)
        accessibility_bias = 0.04
        seo_bias = 0.04

    noise = rng.uniform(-0.015, 0.015)
    quality = min(0.99, max(0.55, base_quality + quality_bias + noise))
    accessibility = min(0.99, max(0.50, quality + accessibility_bias - 0.04))
    seo = min(0.99, max(0.50, quality + seo_bias - 0.03))

    return {
        'quality': quality,
        'accessibility': accessibility,
        'seo': seo,
    }


def _run_strategy(strategy: str, portfolio_case: Dict[str, Any], config: Dict[str, Any], rng: random.Random) -> Dict[str, Any]:
    """Generate and score one portfolio website strategy."""
    source_projects = list(portfolio_case.get('projects', []))[: config['max_projects']]
    pages: List[Dict[str, Any]] = []
    cumulative_layout_debt = 0.0
    quality_scores: List[float] = []
    accessibility_scores: List[float] = []
    seo_scores: List[float] = []

    for index, project in enumerate(source_projects, start=1):
        scoring = _score_project(project, strategy, rng)
        quality = scoring['quality']
        accessibility = scoring['accessibility']
        seo = scoring['seo']
        debt = 1.0 - quality
        cumulative_layout_debt += debt

        quality_scores.append(quality)
        accessibility_scores.append(accessibility)
        seo_scores.append(seo)

        title = str(project.get('title', f'Project {index}'))
        highlights = project.get('highlights', [])[: config['max_snippets_per_project']]
        pages.append(
            create_page_record(
                page_index=index,
                strategy=strategy,
                source_title=title,
                slug=_slugify(title),
                source_type=str(project.get('source_type', 'markdown')),
                tags=[str(tag) for tag in project.get('tags', [])],
                estimated_read_minutes=_estimate_read_minutes(project),
                section_count=max(2, len(highlights) + 1),
                quality_score=quality,
                layout_debt=debt,
                cumulative_layout_debt=cumulative_layout_debt,
            )
        )

    page_count = max(1, len(pages))
    return create_strategy_result(
        strategy=strategy,
        mean_quality_score=sum(quality_scores) / page_count,
        accessibility_score=sum(accessibility_scores) / page_count,
        seo_score=sum(seo_scores) / page_count,
        cumulative_layout_debt=cumulative_layout_debt,
        pages=pages,
        feasible=bool(pages),
    )


def _compare_strategies(portfolio_case: Dict[str, Any], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Run configured generation strategies for side-by-side comparison."""
    results: List[Dict[str, Any]] = []
    base_seed = int(config['random_seed'])
    for offset, strategy in enumerate(config['enabled_strategies'], start=1):
        strategy_rng = random.Random(base_seed + (offset * 97))
        results.append(_run_strategy(strategy, portfolio_case, config, strategy_rng))
    return results


def _expand_projects(base_projects: List[Dict[str, Any]], target_count: int) -> List[Dict[str, Any]]:
    """Expand source projects to requested count for runtime benchmarks."""
    if not base_projects:
        return []
    expanded: List[Dict[str, Any]] = []
    index = 0
    while len(expanded) < target_count:
        project = dict(base_projects[index % len(base_projects)])
        project['title'] = f"{project.get('title', 'Project')} #{len(expanded) + 1}"
        expanded.append(project)
        index += 1
    return expanded


def _benchmark_runtime(config: Dict[str, Any], portfolio_case: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Benchmark strategy runtime across increasing portfolio sizes."""
    points: List[Dict[str, Any]] = []
    base_seed = int(config['random_seed'])
    base_projects = list(portfolio_case.get('projects', []))

    for project_count in config['benchmark_project_counts']:
        bench_case = dict(portfolio_case)
        bench_case['projects'] = _expand_projects(base_projects, project_count)
        for strategy_index, strategy in enumerate(config['enabled_strategies'], start=1):
            for trial in range(1, config['benchmark_trials'] + 1):
                trial_seed = base_seed + (project_count * 13) + (strategy_index * 101) + trial
                trial_rng = random.Random(trial_seed)
                started = time.perf_counter()
                _run_strategy(strategy, bench_case, config, trial_rng)
                elapsed_ms = (time.perf_counter() - started) * 1000.0
                points.append(create_runtime_point(strategy, float(project_count), trial, elapsed_ms))
    return points


def _aggregate_runtime(points: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, float]]]:
    """Average runtime benchmark points by strategy and portfolio size."""
    grouped: Dict[str, Dict[float, List[float]]] = defaultdict(lambda: defaultdict(list))
    for point in points:
        grouped[point['series']][point['size']].append(point['elapsed_ms'])

    summary: Dict[str, List[Dict[str, float]]] = {}
    for strategy, buckets in grouped.items():
        rows: List[Dict[str, float]] = []
        for size in sorted(buckets):
            rows.append({'size': size, 'elapsed_ms': round(mean(buckets[size]), 6)})
        summary[strategy] = rows
    return summary


def _save_runtime_chart(runtime_summary: Dict[str, List[Dict[str, float]]], session_id: str) -> str:
    """Persist benchmark runtime chart."""
    figure, axis = plt.subplots(figsize=(9.2, 5.0))
    for series, rows in runtime_summary.items():
        axis.plot(
            [row['size'] for row in rows],
            [row['elapsed_ms'] for row in rows],
            marker='o',
            linewidth=2,
            label=series.replace('_', ' ').title(),
            color=PLOT_COLORS.get(series, '#6c757d'),
        )
    axis.set_title('Average Runtime By Portfolio Size And Strategy')
    axis.set_xlabel('Projects included')
    axis.set_ylabel('Elapsed time (ms)')
    axis.grid(alpha=0.25)
    axis.legend(ncol=2)
    figure.tight_layout()
    file_path = OUTPUTS_DIR / f'strategy_runtime_{session_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def _save_debt_chart(selected_pages: List[Dict[str, Any]], session_id: str) -> str:
    """Persist cumulative layout debt chart for selected strategy."""
    figure, axis = plt.subplots(figsize=(8.8, 4.8))
    if selected_pages:
        axis.plot(
            [int(row['page_index']) for row in selected_pages],
            [float(row['cumulative_layout_debt']) for row in selected_pages],
            marker='o',
            markersize=2.0,
            linewidth=1.8,
            color=PLOT_COLORS['selected_plan'],
        )
    axis.set_title('Cumulative Layout Debt Across Generated Pages')
    axis.set_xlabel('Generated page index')
    axis.set_ylabel('Cumulative layout debt')
    axis.grid(alpha=0.25)
    figure.tight_layout()
    file_path = OUTPUTS_DIR / f'layout_debt_{session_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def _page_preview_points(pages: List[Dict[str, Any]], max_rows: int) -> List[Dict[str, Any]]:
    """Build evenly sampled page previews across one generation trace."""
    if not pages:
        return []
    interval = max(1, len(pages) // max(1, max_rows))
    selected = [pages[index] for index in range(0, len(pages), interval)]
    return selected[:max_rows]


def load_generator_profile() -> Dict[str, Any]:
    """Return startup profile built from previously saved catalogs."""
    ensure_data_dirs()
    run_catalog = load_run_catalog()
    library = load_portfolio_library()
    history = load_history()
    recent_runs = [
        f"{item.get('session_id', '')}:{item.get('best_strategy', '')}:{item.get('demo_portfolio_label', '')}"
        for item in run_catalog[-5:]
    ]
    return {
        'catalog_file': 'data/runs.json',
        'library_file': 'data/portfolio_sets.json',
        'history_file': 'data/portfolio_history.json',
        'runs_stored': len(run_catalog),
        'portfolios_available': len(library),
        'history_entries': len(history),
        'recent_runs': recent_runs,
    }


def run_core_flow() -> Dict[str, Any]:
    """Run one complete generation, benchmark, and plotting session."""
    ensure_data_dirs()
    config = create_portfolio_config()
    session_id = _session_id()
    started = time.perf_counter()

    library = load_portfolio_library()
    if not library:
        library = _default_portfolio_library()
        save_portfolio_library(library)

    demo_portfolio = next(
        (item for item in library if item['label'] == config['demo_portfolio_label']),
        library[0],
    )

    comparison = _compare_strategies(demo_portfolio, config)
    selected_result = next((item for item in comparison if item['strategy'] == config['strategy']), None)
    if selected_result is None and comparison:
        selected_result = max(comparison, key=lambda item: float(item['mean_quality_score']))
    selected_result = selected_result or create_strategy_result('none', 0.0, 0.0, 0.0, 0.0, [], False)

    history = load_history()
    history.append(
        create_history_entry(
            'generation_session',
            {
                'session_id': session_id,
                'strategy': selected_result['strategy'],
                'pages_generated': len(selected_result['pages']),
                'mean_quality_score': selected_result['mean_quality_score'],
                'cumulative_layout_debt': selected_result['cumulative_layout_debt'],
            },
        )
    )
    sampled_pages = _page_preview_points(selected_result['pages'], max_rows=20)
    for page in sampled_pages:
        history.append(create_history_entry('generated_page', page))
    history = history[-500:]
    history_file = save_history(history)

    runtime_points = _benchmark_runtime(config, demo_portfolio)
    runtime_summary = _aggregate_runtime(runtime_points)

    trace_payload = {
        'session_id': session_id,
        'config': config,
        'portfolio_case': demo_portfolio,
        'strategy_comparison': comparison,
        'selected_result': selected_result,
        'history_file': history_file,
    }
    benchmark_payload = {
        'session_id': session_id,
        'runtime_points': runtime_points,
        'runtime_summary': runtime_summary,
    }

    runtime_chart_file = ''
    debt_chart_file = ''
    if config['include_runtime_plot']:
        runtime_chart_file = _save_runtime_chart(runtime_summary, session_id)
    if config['include_debt_plot']:
        debt_chart_file = _save_debt_chart(selected_result['pages'], session_id)

    trace_file = save_trace_file(trace_payload, session_id)
    benchmark_file = save_benchmark_file(benchmark_payload, session_id)
    elapsed_ms = (time.perf_counter() - started) * 1000.0

    average_by_series = {
        series: mean(row['elapsed_ms'] for row in rows)
        for series, rows in runtime_summary.items()
        if rows
    }
    best_strategy = min(average_by_series.items(), key=lambda item: item[1])[0] if average_by_series else ''

    metrics = {
        'best_strategy': best_strategy,
        'best_avg_runtime_ms': round(average_by_series.get(best_strategy, 0.0), 6),
        'selected_mean_quality_score': round(float(selected_result['mean_quality_score']), 6),
        'selected_accessibility_score': round(float(selected_result['accessibility_score']), 6),
        'selected_seo_score': round(float(selected_result['seo_score']), 6),
        'selected_cumulative_layout_debt': round(float(selected_result['cumulative_layout_debt']), 6),
        'history_size': len(history),
    }

    artifacts = {
        'trace_file': trace_file,
        'benchmark_file': benchmark_file,
        'runtime_chart_file': runtime_chart_file,
        'debt_chart_file': debt_chart_file,
        'history_file': history_file,
    }

    page_previews = _page_preview_points(selected_result['pages'], config['max_preview_rows'])
    summary = create_session_summary(
        session_id=session_id,
        portfolios_available=len(library),
        demo_portfolio_label=demo_portfolio['label'],
        strategy_selected=selected_result['strategy'],
        strategy_runs=len(comparison),
        pages_generated=len(selected_result['pages']),
        runtime_points=len(runtime_points),
        elapsed_ms=elapsed_ms,
        artifacts=artifacts,
        page_previews=page_previews,
        metrics=metrics,
    )
    summary['history_previews'] = history[-config['max_preview_rows'] :]
    summary['max_preview_rows'] = config['max_preview_rows']
    summary['selected_result'] = selected_result

    run_record = dict(summary)
    session_file = save_run_record(run_record)
    summary['artifacts']['session_file'] = session_file
    return summary
