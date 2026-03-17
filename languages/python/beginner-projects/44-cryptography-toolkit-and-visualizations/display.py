"""Presentation helpers for Project 44: Cryptography Toolkit And Visualizations."""

from typing import Any, Dict, List


ALGORITHM_LABELS = {
    'caesar': 'Caesar',
    'vigenere': 'Vigenere',
    'rsa': 'RSA',
}


def format_header() -> str:
    """Format session header banner."""
    return '=' * 70 + '\n' + '   CRYPTOGRAPHY TOOLKIT AND VISUALIZATIONS\n' + '=' * 70


def format_startup_guide(config: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """Format startup configuration and historical profile."""
    recent = ', '.join(profile.get('recent_runs', [])) or 'None yet'
    lines = [
        '',
        'Configuration:',
        f"   Project type:           {config['project_type']}",
        f"   Classic demos:          {', '.join(ALGORITHM_LABELS.get(name, name) for name in config['classic_algorithms'])}",
        f"   Benchmark ciphers:      {', '.join(ALGORITHM_LABELS.get(name, name) for name in config['benchmark_algorithms'])}",
        f"   Demo message:           {config['demo_message_label']}",
        f"   Message lengths:        {', '.join(str(size) for size in config['benchmark_message_lengths'])}",
        f"   Trials per length:      {config['benchmark_trials']}",
        f"   RSA demo bits:          {config['rsa_demo_bits']}",
        f"   RSA attack bits:        {', '.join(str(bits) for bits in config['rsa_attack_bits'])}",
        f"   Frequency plot:         {config['include_frequency_plot']}",
        f"   Runtime chart:          {config['include_runtime_chart']}",
        f"   Attack chart:           {config['include_attack_chart']}",
        f"   Max preview rows:       {config['max_preview_rows']}",
        f"   Random seed:            {config['random_seed']}",
        '',
        'Startup:',
        '   Data directory:         data/',
        '   Outputs directory:      data/outputs/',
        (
            f"   Message library:        {profile['library_file']} "
            f"(loaded {profile['messages_available']} messages)"
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


def _clip_preview(value: str, width: int = 30) -> str:
    """Return a compact preview string for table output."""
    compact = value.replace('\n', ' ').strip()
    if len(compact) <= width:
        return compact
    return compact[: width - 3] + '...'


def format_demo_table(demo_previews: List[Dict[str, Any]]) -> str:
    """Format demo preview table."""
    if not demo_previews:
        return 'No demo previews generated.'
    lines = [
        'Demo previews:',
        '   Algorithm | Key material      | Cipher preview                  | Roundtrip',
        '   ----------+-------------------+---------------------------------+----------',
    ]
    for row in demo_previews:
        lines.append(
            '   '
            f"{ALGORITHM_LABELS.get(row['algorithm'], row['algorithm'])[:8]:<8} | "
            f"{_clip_preview(str(row['key_material']), 17):<17} | "
            f"{_clip_preview(str(row['ciphertext']), 31):<31} | "
            f"{'yes' if row.get('roundtrip_ok') else 'no'}"
        )
    return '\n'.join(lines)


def format_attack_table(attacks: List[Dict[str, Any]]) -> str:
    """Format attack demonstration table."""
    if not attacks:
        return 'No attack demonstrations generated.'
    lines = [
        'Attack demonstrations:',
        '   Attack                 | Target      | Success | Time (ms)',
        '   -----------------------+-------------+---------+----------',
    ]
    for attack in attacks:
        lines.append(
            '   '
            f"{attack.get('attack_name', '')[:23]:<23} | "
            f"{attack.get('target', '')[:11]:<11} | "
            f"{'yes' if attack.get('success') else 'no ':<7} | "
            f"{attack.get('elapsed_ms', 0.0):<8.5f}"
        )
    return '\n'.join(lines)


def format_run_report(summary: Dict[str, Any]) -> str:
    """Format final session report."""
    artifacts = summary.get('artifacts', {})
    metrics = summary.get('metrics', {})
    fastest_cipher = ALGORITHM_LABELS.get(metrics.get('fastest_cipher', ''), metrics.get('fastest_cipher', 'N/A'))
    lines = [
        '',
        'Session complete:',
        f"   Session ID:             {summary['session_id']}",
        f"   Messages available:     {summary['messages_available']}",
        f"   Demo message:           {summary['demo_message_label']} ({summary['demo_message_length']} chars)",
        f"   Runtime points:         {summary['runtime_points']}",
        f"   Attacks run:            {summary['attacks_run']}",
        f"   Elapsed time:           {summary['elapsed_ms']:.2f} ms",
        '',
        (
            'Toolkit metrics: '
            f"fastest_cipher={fastest_cipher} | "
            f"fastest_avg_runtime_ms={metrics.get('fastest_avg_runtime_ms', 0.0):.5f} | "
            f"rsa_factorization_ms={metrics.get('rsa_factorization_ms', 0.0):.5f} | "
            f"largest_message_length={metrics.get('largest_message_length', 0)}"
        ),
        '',
        format_demo_table(summary.get('demo_previews', [])),
        '',
        format_attack_table(summary.get('attacks', [])),
        '',
        'Artifacts saved:',
        f"   Session record:         {artifacts.get('session_file', 'N/A')}",
        f"   Trace bundle:           {artifacts.get('trace_file', 'N/A')}",
        f"   Benchmark file:         {artifacts.get('benchmark_file', 'N/A')}",
        f"   Frequency plot:         {artifacts.get('frequency_plot_file', 'N/A')}",
        f"   Runtime chart:          {artifacts.get('runtime_chart_file', 'N/A')}",
        f"   Attack chart:           {artifacts.get('attack_chart_file', 'N/A')}",
    ]
    return '\n'.join(lines)


def format_message(message: str) -> str:
    """Format a user-facing message string."""
    return f'[Project 44] {message}'
