"""
models.py - Data models for Project 34: Document Search Engine
"""

from datetime import datetime
from typing import Any, Dict, List


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string."""
    return datetime.utcnow().isoformat(timespec='seconds') + 'Z'


def create_engine_config(
    top_k: int = 4,
    min_score: float = 0.10,
    min_token_length: int = 2,
    include_bigrams: bool = True,
    query_weight_semantic: float = 0.80,
    query_weight_lexical: float = 0.20,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """Create a validated search-engine configuration record."""
    semantic_weight = max(0.0, min(1.0, float(query_weight_semantic)))
    lexical_weight = max(0.0, min(1.0, float(query_weight_lexical)))
    total = semantic_weight + lexical_weight
    if total <= 0.0:
        semantic_weight = 1.0
        lexical_weight = 0.0
    else:
        semantic_weight /= total
        lexical_weight /= total

    return {
        'project_type': 'document_search_engine',
        'top_k': max(1, int(top_k)),
        'min_score': max(0.0, min(1.0, float(min_score))),
        'min_token_length': max(1, int(min_token_length)),
        'include_bigrams': bool(include_bigrams),
        'semantic_weight': semantic_weight,
        'lexical_weight': lexical_weight,
        'random_seed': int(random_seed),
        'created_at': _utc_timestamp(),
    }


def create_search_record(
    query_id: str,
    query_text: str,
    rank: int,
    doc_id: str,
    title: str,
    semantic_score: float,
    lexical_score: float,
    blended_score: float,
) -> Dict[str, Any]:
    """Create one persisted ranked-search result record."""
    return {
        'query_id': query_id,
        'query_text': query_text,
        'rank': int(rank),
        'doc_id': doc_id,
        'title': title,
        'semantic_score': float(semantic_score),
        'lexical_score': float(lexical_score),
        'blended_score': float(blended_score),
        'created_at': _utc_timestamp(),
    }


def create_run_summary(
    run_id: str,
    documents_indexed: int,
    queries_executed: int,
    results_returned: int,
    elapsed_ms: float,
    artifacts: Dict[str, Any],
    query_previews: List[Dict[str, Any]],
    top_results: List[Dict[str, Any]],
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """Create final run summary for reporting and persistence."""
    return {
        'run_id': run_id,
        'documents_indexed': int(documents_indexed),
        'queries_executed': int(queries_executed),
        'results_returned': int(results_returned),
        'elapsed_ms': float(elapsed_ms),
        'artifacts': artifacts,
        'query_previews': query_previews,
        'top_results': top_results,
        'metrics': metrics,
        'finished_at': _utc_timestamp(),
    }


def create_record(**kwargs: Any) -> Dict[str, Any]:
    """Backwards-compatible generic record factory."""
    return dict(kwargs)
