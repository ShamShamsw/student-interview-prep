"""
display.py - Presentation helpers for Project 33: Plagiarism Similarity Detector
"""

from typing import Any, Dict, List


def format_header() -> str:
    """Format session header banner."""
    return (
        '=' * 70
        + '\n'
        + '   PLAGIARISM SIMILARITY DETECTOR\n'
        + '=' * 70
    )


def format_startup_guide(config: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """Format startup configuration and historical profile."""
    recent = ', '.join(profile.get('recent_high_risk', [])) or 'None yet'
    lines = [
        '',
        'Configuration:',
        f"   Project type:         {config['project_type']}",
        '   Embedding method:     tfidf (unigram + optional bigram)',
        f"   Similarity threshold: {config['similarity_threshold']:.2f}",
        f"   Cluster threshold:    {config['cluster_threshold']:.2f}",
        f"   Include bigrams:      {config['include_bigrams']}",
        f"   Min token length:     {config['min_token_length']}",
        f"   Random seed:          {config['random_seed']}",
        f"   Max pairs in report:  {config['max_pairs_in_report']}",
        '',
        'Startup:',
        '   Data directory:       data/',
        '   Outputs directory:    data/outputs/',
        f"   Document corpus:      {profile['documents_file']} (loaded {profile['documents_available']} docs)",
        f"   Run catalog:          {profile['catalog_file']} (loaded {profile['runs_stored']} runs)",
        f"   Analysis catalog:     {profile['analysis_catalog_file']} (loaded {profile['analyses_stored']} records)",
        f'   Recent high-risk:     {recent}',
        '',
        '---',
    ]
    return '\n'.join(lines)


def format_pair_table(pair_previews: List[Dict[str, Any]]) -> str:
    """Format suspicious similarity pairs in a fixed-width table."""
    if not pair_previews:
        return 'No document pairs were available for comparison.'
    lines = [
        'Top pair similarities:',
        '   Pair                                | Semantic | Lexical  | Risk',
        '   ------------------------------------+----------+----------+---------',
    ]
    for item in pair_previews:
        pair_name = f"{item['doc_a_id']}:{item['doc_b_id']}"
        lines.append(
            '   '
            f"{pair_name[:36]:<36}| "
            f"  {item['semantic_score']:.4f}  | "
            f"  {item['lexical_score']:.4f}  | "
            f"{item['risk_level']:<8}"
        )
    return '\n'.join(lines)


def format_neighbor_table(neighbors: List[Dict[str, Any]]) -> str:
    """Format nearest-neighbor report for each document."""
    if not neighbors:
        return 'No nearest-neighbor data.'
    lines = [
        '',
        'Nearest-neighbor report:',
        '   Document ID | Most similar document | Score',
        '   ------------+-----------------------+--------',
    ]
    for row in neighbors:
        lines.append(
            '   '
            f"{row['doc_id'][:12]:<12}| "
            f"{row['nearest_doc_id'][:23]:<23}| "
            f"{row['score']:.4f}"
        )
    return '\n'.join(lines)


def format_cluster_table(clusters: List[Dict[str, Any]]) -> str:
    """Format cluster summary table."""
    if not clusters:
        return 'No clusters detected.'
    lines = [
        '',
        'Cluster summary:',
        '   Cluster      | Size | Avg similarity | Member preview',
        '   -------------+------+----------------+------------------------------',
    ]
    for cluster in clusters:
        preview = ', '.join(cluster.get('members', [])[:3])
        lines.append(
            '   '
            f"{cluster['cluster_id'][:13]:<13}| "
            f"{cluster['size']:>4} | "
            f"    {cluster['avg_similarity']:.4f}    | "
            f"{preview}"
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
        f"   Documents processed:  {summary['documents_processed']}",
        f"   Pairs compared:       {summary['pairs_compared']}",
        f"   Flagged pairs:        {summary['flagged_pairs']}",
        f"   Clusters found:       {summary['clusters_found']}",
        f"   Elapsed time:         {summary['elapsed_ms']:.2f} ms",
        '',
        f"Corpus metrics: vocab={metrics.get('vocab_size', 0)} | "
        f"mean_sim={metrics.get('mean_similarity', 0.0):.4f} | "
        f"median_pair={metrics.get('median_pair_similarity', 0.0):.4f} | "
        f"max_pair={metrics.get('max_pair_similarity', 0.0):.4f}",
        '',
        format_pair_table(summary.get('pair_previews', [])),
        format_neighbor_table(summary.get('nearest_neighbors', [])),
        format_cluster_table(summary.get('cluster_previews', [])),
        '',
        'Artifacts saved:',
        f"   Run record:           {artifacts.get('run_file', 'N/A')}",
        f"   Similarity matrix:    {artifacts.get('similarity_matrix_file', 'N/A')}",
        f"   Pair report:          {artifacts.get('pair_report_file', 'N/A')}",
        f"   Cluster report:       {artifacts.get('cluster_report_file', 'N/A')}",
        f"   Metadata exports:     {len(metadata_files)}",
    ]
    return '\n'.join(lines)

def format_message(message: str) -> str:
    """Format a user-facing message string."""
    return f'[Project 33] {message}'
