"""
display.py - Presentation helpers for Project 34: Document Search Engine
"""

from typing import Any, Dict, List


def format_header() -> str:
    """Format session header banner."""
    return '=' * 70 + '\n' + '   DOCUMENT SEARCH ENGINE\n' + '=' * 70


def format_startup_guide(config: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """Format startup configuration and historical profile."""
    recent = ', '.join(profile.get('recent_queries', [])) or 'None yet'
    lines = [
        '',
        'Configuration:',
        f"   Project type:         {config['project_type']}",
        '   Retrieval model:      tfidf semantic + lexical blend',
        f"   Top-k results:        {config['top_k']}",
        f"   Minimum score:        {config['min_score']:.2f}",
        f"   Include bigrams:      {config['include_bigrams']}",
        f"   Min token length:     {config['min_token_length']}",
        f"   Semantic weight:      {config['semantic_weight']:.2f}",
        f"   Lexical weight:       {config['lexical_weight']:.2f}",
        f"   Random seed:          {config['random_seed']}",
        '',
        'Startup:',
        '   Data directory:       data/',
        '   Outputs directory:    data/outputs/',
        f"   Document corpus:      {profile['documents_file']} (loaded {profile['documents_available']} docs)",
        f"   Query set:            {profile['queries_file']} (loaded {profile['queries_available']} queries)",
        f"   Run catalog:          {profile['catalog_file']} (loaded {profile['runs_stored']} runs)",
        f"   Search catalog:       {profile['search_catalog_file']} (loaded {profile['search_records_stored']} records)",
        f'   Recent results:       {recent}',
        '',
        '---',
    ]
    return '\n'.join(lines)


def format_query_table(query_previews: List[Dict[str, Any]]) -> str:
    """Format top result per query in a fixed-width table."""
    if not query_previews:
        return 'No query executions were available for this run.'
    lines = [
        'Query summary:',
        '   Query ID | Top document | Top score',
        '   ---------+--------------+----------',
    ]
    for item in query_previews:
        lines.append(
            '   '
            f"{item['query_id'][:8]:<8} | "
            f"{item['top_doc_id'][:12]:<12} | "
            f"{item['top_score']:.4f}"
        )
    return '\n'.join(lines)


def format_top_results_table(rows: List[Dict[str, Any]]) -> str:
    """Format top blended results across all queries."""
    if not rows:
        return 'No ranked results met the score threshold.'
    lines = [
        '',
        'Top blended matches:',
        '   Query   | Rank | Document ID | Blended | Semantic | Lexical',
        '   --------+------+-------------+---------+----------+--------',
    ]
    for row in rows:
        lines.append(
            '   '
            f"{row['query_id'][:7]:<7} | "
            f"{row.get('rank', 0):>4} | "
            f"{row['doc_id'][:11]:<11} | "
            f"{row['blended_score']:.4f} | "
            f"{row['semantic_score']:.4f}   | "
            f"{row['lexical_score']:.4f}"
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
        f"   Documents indexed:    {summary['documents_indexed']}",
        f"   Queries executed:     {summary['queries_executed']}",
        f"   Results returned:     {summary['results_returned']}",
        f"   Elapsed time:         {summary['elapsed_ms']:.2f} ms",
        '',
        f"Index metrics: vocab={metrics.get('vocab_size', 0)} | "
        f"mean_score={metrics.get('mean_blended_score', 0.0):.4f} | "
        f"min_score={metrics.get('min_blended_score', 0.0):.4f} | "
        f"max_score={metrics.get('max_blended_score', 0.0):.4f}",
        '',
        format_query_table(summary.get('query_previews', [])),
        format_top_results_table(summary.get('top_results', [])),
        '',
        'Artifacts saved:',
        f"   Run record:           {artifacts.get('run_file', 'N/A')}",
        f"   Index snapshot:       {artifacts.get('index_file', 'N/A')}",
        f"   Results report:       {artifacts.get('results_file', 'N/A')}",
        f"   Metadata exports:     {len(metadata_files)}",
    ]
    return '\n'.join(lines)


def format_message(message: str) -> str:
    """Format a user-facing message string."""
    return f'[Project 34] {message}'
