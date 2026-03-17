"""display.py - Presentation helpers for Project 40: Real-Time Collaborative Notebook Demo."""

from typing import Any, Dict, List


def format_header() -> str:
    """Format session header banner."""
    return '=' * 70 + '\n' + '   REAL-TIME COLLABORATIVE NOTEBOOK DEMO\n' + '=' * 70


def format_startup_guide(config: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """Format startup configuration and historical profile."""
    recent = ', '.join(profile.get('recent_edits', [])) or 'None yet'
    lines = [
        '',
        'Configuration:',
        f"   Project type:         {config['project_type']}",
        f"   Users:                {', '.join(config['users'])}",
        f"   Ops per user:         {config['ops_per_user']}",
        f"   Conflict window:      {config['conflict_window_ms']} ms",
        f"   Timeline plot:        {config['include_timeline_plot']}",
        f"   Conflict chart:       {config['include_conflict_chart']}",
        f"   Max edits in report:  {config['max_edits_in_report']}",
        f"   Random seed:          {config['random_seed']}",
        '',
        'Startup:',
        '   Data directory:       data/',
        '   Outputs directory:    data/outputs/',
        (
            f"   Notebook library:     {profile['library_file']} "
            f"(loaded {profile['notebooks_available']} notebooks)"
        ),
        (
            f"   Session catalog:      {profile['catalog_file']} "
            f"(loaded {profile['sessions_stored']} sessions)"
        ),
        (
            f"   Edit catalog:         {profile['edit_catalog_file']} "
            f"(loaded {profile['edit_records_stored']} edits)"
        ),
        f"   Recent edits:         {recent}",
        '',
        '---',
    ]
    return '\n'.join(lines)


def format_edit_table(edit_previews: List[Dict[str, Any]]) -> str:
    """Format collaborative edit preview table."""
    if not edit_previews:
        return 'No edits generated.'
    lines = [
        'Edit previews:',
        '   ID       | User    | Notebook | Cell   | Operation | Conflict | Status',
        '   ---------+---------+----------+--------+-----------+----------+----------',
    ]
    for edit in edit_previews:
        lines.append(
            '   '
            f"{edit['edit_id'][:8]:<8} | "
            f"{edit['user_id'][:7]:<7} | "
            f"{edit.get('notebook_id', '')[:8]:<8} | "
            f"{edit['cell_id'][:6]:<6} | "
            f"{edit['operation'][:9]:<9} | "
            f"{'yes' if edit['is_conflict'] else 'no':<8} | "
            f"{edit['status'][:10]:<10}"
        )
    return '\n'.join(lines)


def format_run_report(summary: Dict[str, Any]) -> str:
    """Format final session report."""
    artifacts = summary.get('artifacts', {})
    metrics = summary.get('metrics', {})
    lines = [
        '',
        'Session complete:',
        f"   Session ID:           {summary['session_id']}",
        f"   Notebooks processed:  {summary['notebooks_processed']}",
        f"   Total edits:          {summary['edits_total']}",
        f"   Conflicts detected:   {summary['conflicts_total']}",
        f"   Conflicts resolved:   {summary['conflicts_resolved']}",
        f"   Elapsed time:         {summary['elapsed_ms']:.2f} ms",
        '',
        (
            f"Dataset metrics: "
            f"conflict_rate={metrics.get('conflict_rate', 0.0):.1%} | "
            f"mean_edits_per_cell={metrics.get('mean_edits_per_cell', 0.0):.1f} | "
            f"max_conflicts_in_cell={metrics.get('max_conflicts_in_cell', 0)} | "
            f"resolution_strategy={metrics.get('resolution_strategy', 'N/A')}"
        ),
        '',
        format_edit_table(summary.get('edit_previews', [])),
        '',
        'Artifacts saved:',
        f"   Session record:       {artifacts.get('session_file', 'N/A')}",
        f"   Edit bundle:          {artifacts.get('bundle_file', 'N/A')}",
        f"   Timeline plot:        {artifacts.get('timeline_file', 'N/A')}",
        f"   Conflict chart:       {artifacts.get('conflict_chart_file', 'N/A')}",
        f"   Total edits logged:   {artifacts.get('edit_count', 0)}",
    ]
    return '\n'.join(lines)


def format_message(message: str) -> str:
    """Format a user-facing message string."""
    return f'[Project 40] {message}'
