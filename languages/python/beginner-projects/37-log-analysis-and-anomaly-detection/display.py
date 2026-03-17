"""
display.py - Presentation helpers for Project 37: Log Analysis And Anomaly Detection
"""

from typing import Any, Dict, List


def format_header() -> str:
    """Format session header banner."""
    return '=' * 70 + '\n' + '   LOG ANALYSIS AND ANOMALY DETECTION\n' + '=' * 70


def format_startup_guide(config: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """Format startup configuration and historical profile."""
    recent = ', '.join(profile.get('recent_anomalies', [])) or 'None yet'
    lines = [
        '',
        'Configuration:',
        f"   Project type:         {config['project_type']}",
        '   Analyzer engine:     common-log parser + rule scoring (stdlib only)',
        f"   Top patterns:         {config['top_patterns']}",
        f"   Score threshold:      {config['score_threshold']}",
        f"   Include timeline:     {config['include_timeline']}",
        f"   Include IP summary:   {config['include_ip_summary']}",
        f"   Include path summary: {config['include_path_summary']}",
        f"   Max anomalies report: {config['max_anomalies_in_report']}",
        f"   Random seed:          {config['random_seed']}",
        '',
        'Startup:',
        '   Data directory:       data/',
        '   Outputs directory:    data/outputs/',
        (
            f"   Log library:          {profile['library_file']} "
            f"(loaded {profile['library_available']} log lines)"
        ),
        (
            f"   Run catalog:          {profile['catalog_file']} "
            f"(loaded {profile['runs_stored']} runs)"
        ),
        (
            f"   Anomaly catalog:      {profile['anomaly_catalog_file']} "
            f"(loaded {profile['anomaly_records_stored']} records)"
        ),
        f"   Recent anomalies:     {recent}",
        '',
        '---',
    ]
    return '\n'.join(lines)


def format_anomaly_table(previews: List[Dict[str, Any]]) -> str:
    """Format anomaly preview table."""
    if not previews:
        return 'No anomalies detected.'
    lines = [
        'Anomaly previews:',
        '   ID      | Time                 | IP              | Type                     | Score | Evidence',
        '   --------+----------------------+-----------------+--------------------------+-------+------------------------------',
    ]
    for anomaly in previews:
        evidence = '; '.join(anomaly.get('evidence', [])[:2])[:30]
        lines.append(
            '   '
            f"{anomaly['anomaly_id'][:7]:<7} | "
            f"{anomaly.get('timestamp', '')[:20]:<20} | "
            f"{anomaly.get('ip_address', 'unknown')[:15]:<15} | "
            f"{anomaly.get('anomaly_type', '')[:24]:<24} | "
            f"{anomaly.get('score', 0.0):>5.1f} | "
            f"{evidence}"
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
        f"   Log lines processed:  {summary['log_lines_processed']}",
        f"   Parsed events:        {summary['parsed_events']}",
        f"   Anomalies detected:   {summary['anomalies_detected']}",
        f"   Unique IPs:           {summary['unique_ips']}",
        f"   Elapsed time:         {summary['elapsed_ms']:.2f} ms",
        '',
        (
            f"Dataset metrics: error_rate={metrics.get('error_rate', 0.0):.1%} | "
            f"server_error_rate={metrics.get('server_error_rate', 0.0):.1%} | "
            f"offhours_share={metrics.get('offhours_share', 0.0):.1%} | "
            f"peak_minute_volume={metrics.get('peak_minute_volume', 0)} | "
            f"max_score={metrics.get('max_anomaly_score', 0.0):.1f}"
        ),
        '',
        format_anomaly_table(summary.get('anomaly_previews', [])),
        '',
        'Artifacts saved:',
        f"   Run record:           {artifacts.get('run_file', 'N/A')}",
        f"   Parsed export:        {artifacts.get('parsed_file', 'N/A')}",
        f"   Anomaly export:       {artifacts.get('anomalies_file', 'N/A')}",
        f"   Timeline export:      {artifacts.get('timeline_file', 'N/A')}",
        f"   Metadata exports:     {len(metadata_files)}",
    ]
    return '\n'.join(lines)


def format_message(message: str) -> str:
    """Format a user-facing message string."""
    return f'[Project 37] {message}'
