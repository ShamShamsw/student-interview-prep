"""
models.py - Data models for Project 33: Plagiarism Similarity Detector
"""

from datetime import datetime
from typing import Any, Dict, List


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string."""
    return datetime.utcnow().isoformat(timespec='seconds') + 'Z'


def create_detector_config(
    similarity_threshold: float = 0.12,
    cluster_threshold: float = 0.12,
    max_pairs_in_report: int = 8,
    random_seed: int = 42,
    min_token_length: int = 2,
    include_bigrams: bool = True,
) -> Dict[str, Any]:
    """Create a validated plagiarism detector configuration record."""
    sim_threshold = max(0.0, min(1.0, float(similarity_threshold)))
    cluster_sim = max(0.0, min(1.0, float(cluster_threshold)))
    return {
        'project_type': 'plagiarism_similarity_detector',
        'similarity_threshold': sim_threshold,
        'cluster_threshold': cluster_sim,
        'max_pairs_in_report': max(3, int(max_pairs_in_report)),
        'random_seed': int(random_seed),
        'min_token_length': max(1, int(min_token_length)),
        'include_bigrams': bool(include_bigrams),
        'created_at': _utc_timestamp(),
    }


def create_similarity_record(
    pair_id: str,
    doc_a_id: str,
    doc_b_id: str,
    doc_a_title: str,
    doc_b_title: str,
    semantic_score: float,
    lexical_score: float,
    risk_level: str,
) -> Dict[str, Any]:
    """Create one persisted similarity-pair result record."""
    return {
        'pair_id': pair_id,
        'doc_a_id': doc_a_id,
        'doc_b_id': doc_b_id,
        'doc_a_title': doc_a_title,
        'doc_b_title': doc_b_title,
        'semantic_score': float(semantic_score),
        'lexical_score': float(lexical_score),
        'risk_level': risk_level,
        'created_at': _utc_timestamp(),
    }


def create_run_summary(
    run_id: str,
    documents_processed: int,
    pairs_compared: int,
    flagged_pairs: int,
    clusters_found: int,
    elapsed_ms: float,
    artifacts: Dict[str, Any],
    pair_previews: List[Dict[str, Any]],
    nearest_neighbors: List[Dict[str, Any]],
    cluster_previews: List[Dict[str, Any]],
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """Create final run summary for reporting and persistence."""
    return {
        'run_id': run_id,
        'documents_processed': int(documents_processed),
        'pairs_compared': int(pairs_compared),
        'flagged_pairs': int(flagged_pairs),
        'clusters_found': int(clusters_found),
        'elapsed_ms': float(elapsed_ms),
        'artifacts': artifacts,
        'pair_previews': pair_previews,
        'nearest_neighbors': nearest_neighbors,
        'cluster_previews': cluster_previews,
        'metrics': metrics,
        'finished_at': _utc_timestamp(),
    }


def create_record(**kwargs: Any) -> Dict[str, Any]:
    """Backwards-compatible generic record factory."""
    return dict(kwargs)
