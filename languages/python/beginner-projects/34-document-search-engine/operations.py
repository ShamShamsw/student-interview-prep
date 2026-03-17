"""
operations.py - Business logic for Project 34: Document Search Engine
"""

from __future__ import annotations

from datetime import datetime
import re
import time
from typing import Any, Dict, List, Tuple

import numpy as np

from models import create_engine_config, create_run_summary, create_search_record
from storage import (
    OUTPUTS_DIR,
    ensure_data_dirs,
    load_document_corpus,
    load_query_set,
    load_run_catalog,
    load_search_catalog,
    save_document_corpus,
    save_query_set,
    save_run_record,
    save_search_record,
)


def _run_id() -> str:
    """Build a compact run ID from UTC timestamp."""
    return datetime.utcnow().strftime('%Y%m%d_%H%M%S')


def _default_documents() -> List[Dict[str, str]]:
    """Return a deterministic starter corpus used on first run."""
    return [
        {
            'doc_id': 'doc_001',
            'title': 'Python Data Classes Quick Guide',
            'category': 'python',
            'text': (
                'Data classes reduce boilerplate for classes that store state. '
                'They support generated initializers, comparison methods, and '
                'clean repr output for simple domain objects.'
            ),
        },
        {
            'doc_id': 'doc_002',
            'title': 'Understanding Breadth First Search',
            'category': 'algorithms',
            'text': (
                'Breadth first search explores graph nodes level by level. '
                'It uses a queue, guarantees shortest path in unweighted graphs, '
                'and helps solve connectivity problems.'
            ),
        },
        {
            'doc_id': 'doc_003',
            'title': 'FastAPI Routing Basics',
            'category': 'backend',
            'text': (
                'FastAPI route handlers map HTTP methods and paths to Python '
                'functions. Dependency injection and type hints improve '
                'validation, docs generation, and maintainability.'
            ),
        },
        {
            'doc_id': 'doc_004',
            'title': 'SQL Indexing Fundamentals',
            'category': 'databases',
            'text': (
                'Database indexes speed up lookups by organizing values into '
                'search-friendly structures. Composite indexes, selectivity, '
                'and query patterns determine effectiveness.'
            ),
        },
        {
            'doc_id': 'doc_005',
            'title': 'JavaScript Async Await Patterns',
            'category': 'javascript',
            'text': (
                'Async await syntax improves readability of asynchronous logic. '
                'Use try catch for error handling and Promise.all for concurrent '
                'independent tasks.'
            ),
        },
        {
            'doc_id': 'doc_006',
            'title': 'TF-IDF for Information Retrieval',
            'category': 'nlp',
            'text': (
                'TF-IDF assigns higher weights to terms that are frequent in a '
                'document but rare across the corpus. It is a practical baseline '
                'for ranking relevance in search systems.'
            ),
        },
        {
            'doc_id': 'doc_007',
            'title': 'Unit Testing with Pytest',
            'category': 'testing',
            'text': (
                'Pytest encourages small test functions, expressive assertions, '
                'fixtures for reusable setup, and parameterization to cover '
                'multiple cases with minimal duplication.'
            ),
        },
        {
            'doc_id': 'doc_008',
            'title': 'Caching Strategies in Web Apps',
            'category': 'architecture',
            'text': (
                'Caching reduces latency and backend load. Common layers include '
                'in-memory caches, CDN edge caching, and application-level '
                'memoization with eviction policies.'
            ),
        },
    ]


def _default_queries() -> List[Dict[str, str]]:
    """Return starter query batch used on first run."""
    return [
        {
            'query_id': 'q_001',
            'query_text': 'how tf idf improves document search relevance',
        },
        {
            'query_id': 'q_002',
            'query_text': 'best way to test python functions with fixtures',
        },
        {
            'query_id': 'q_003',
            'query_text': 'graph traversal shortest path with queue',
        },
        {
            'query_id': 'q_004',
            'query_text': 'optimize api latency with caching',
        },
    ]


def _tokenize(text: str, min_token_length: int) -> List[str]:
    """Tokenize and normalize free-form text."""
    tokens = re.findall(r"[a-zA-Z']+", text.lower())
    return [tok for tok in tokens if len(tok) >= min_token_length]


def _terms(text: str, min_token_length: int, include_bigrams: bool) -> List[str]:
    """Build token list, optionally extending it with bigrams."""
    tokens = _tokenize(text, min_token_length)
    if not include_bigrams or len(tokens) < 2:
        return tokens
    bigrams = [f'{tokens[i]}_{tokens[i + 1]}' for i in range(len(tokens) - 1)]
    return tokens + bigrams


def _build_tfidf_index(
    documents: List[Dict[str, Any]],
    min_token_length: int,
    include_bigrams: bool,
) -> Tuple[np.ndarray, Dict[str, int], np.ndarray]:
    """Build normalized TF-IDF vectors and return matrix, vocab, idf."""
    tokenized_docs: List[List[str]] = [
        _terms(doc.get('text', ''), min_token_length, include_bigrams)
        for doc in documents
    ]

    vocabulary: Dict[str, int] = {}
    for terms in tokenized_docs:
        for term in terms:
            if term not in vocabulary:
                vocabulary[term] = len(vocabulary)

    n_docs = len(tokenized_docs)
    vocab_size = len(vocabulary)
    if n_docs == 0 or vocab_size == 0:
        return np.zeros((0, 0), dtype=np.float32), vocabulary, np.zeros(0, dtype=np.float32)

    tf = np.zeros((n_docs, vocab_size), dtype=np.float32)
    df = np.zeros(vocab_size, dtype=np.float32)

    for row_idx, terms in enumerate(tokenized_docs):
        if not terms:
            continue
        counts: Dict[int, int] = {}
        for term in terms:
            col_idx = vocabulary[term]
            counts[col_idx] = counts.get(col_idx, 0) + 1
        denom = float(len(terms))
        for col_idx, count in counts.items():
            tf[row_idx, col_idx] = count / denom
        for col_idx in counts:
            df[col_idx] += 1.0

    idf = np.log((1.0 + n_docs) / (1.0 + df)) + 1.0
    tfidf = tf * idf

    norms = np.linalg.norm(tfidf, axis=1, keepdims=True)
    norms = np.where(norms == 0.0, 1.0, norms)
    normalized = tfidf / norms
    return normalized.astype(np.float32), vocabulary, idf.astype(np.float32)


def _vectorize_query(
    query_text: str,
    vocabulary: Dict[str, int],
    idf: np.ndarray,
    min_token_length: int,
    include_bigrams: bool,
) -> np.ndarray:
    """Vectorize query text into the same normalized TF-IDF space."""
    if not vocabulary:
        return np.zeros(0, dtype=np.float32)

    terms = _terms(query_text, min_token_length, include_bigrams)
    if not terms:
        return np.zeros(len(vocabulary), dtype=np.float32)

    counts: Dict[int, int] = {}
    for term in terms:
        col_idx = vocabulary.get(term)
        if col_idx is not None:
            counts[col_idx] = counts.get(col_idx, 0) + 1

    vec = np.zeros(len(vocabulary), dtype=np.float32)
    if not counts:
        return vec

    denom = float(len(terms))
    for col_idx, count in counts.items():
        vec[col_idx] = (count / denom) * float(idf[col_idx])

    norm = float(np.linalg.norm(vec))
    if norm > 0.0:
        vec /= norm
    return vec


def _jaccard_similarity(tokens_a: List[str], tokens_b: List[str]) -> float:
    """Compute lexical overlap with Jaccard index."""
    set_a = set(tokens_a)
    set_b = set(tokens_b)
    if not set_a and not set_b:
        return 0.0
    inter = len(set_a & set_b)
    union = len(set_a | set_b)
    return float(inter / union) if union else 0.0


def _rank_query(
    query: Dict[str, str],
    documents: List[Dict[str, Any]],
    doc_matrix: np.ndarray,
    vocabulary: Dict[str, int],
    idf: np.ndarray,
    config: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Compute ranked search results for one query."""
    query_text = query.get('query_text', '')
    query_vec = _vectorize_query(
        query_text,
        vocabulary,
        idf,
        min_token_length=config['min_token_length'],
        include_bigrams=config['include_bigrams'],
    )
    if query_vec.size == 0 or doc_matrix.size == 0:
        return []

    semantic_scores = np.clip(doc_matrix @ query_vec, -1.0, 1.0)
    query_tokens = _tokenize(query_text, config['min_token_length'])

    rows: List[Dict[str, Any]] = []
    for idx, doc in enumerate(documents):
        doc_tokens = _tokenize(doc.get('text', ''), config['min_token_length'])
        lexical = _jaccard_similarity(query_tokens, doc_tokens)
        semantic = float(semantic_scores[idx])
        blended = (
            config['semantic_weight'] * semantic
            + config['lexical_weight'] * lexical
        )
        rows.append(
            {
                'query_id': query.get('query_id', ''),
                'query_text': query_text,
                'doc_id': doc.get('doc_id', ''),
                'title': doc.get('title', ''),
                'semantic_score': semantic,
                'lexical_score': lexical,
                'blended_score': blended,
            }
        )

    rows.sort(key=lambda item: item['blended_score'], reverse=True)
    thresholded = [row for row in rows if row['blended_score'] >= config['min_score']]
    top_k = config['top_k']
    for rank, row in enumerate(thresholded[:top_k], start=1):
        row['rank'] = rank
    return thresholded[:top_k]


def load_search_profile() -> Dict[str, Any]:
    """Return startup profile built from previously saved catalogs."""
    runs = load_run_catalog()
    searches = load_search_catalog()
    documents = load_document_corpus()
    queries = load_query_set()
    recent_queries = [
        f"{item.get('query_id', '')}:{item.get('doc_id', '')}:{item.get('blended_score', 0.0):.2f}"
        for item in searches[-8:]
    ]
    return {
        'catalog_file': 'data/runs.json',
        'search_catalog_file': 'data/searches.json',
        'documents_file': 'data/documents.json',
        'queries_file': 'data/queries.json',
        'runs_stored': len(runs),
        'search_records_stored': len(searches),
        'documents_available': len(documents),
        'queries_available': len(queries),
        'recent_queries': recent_queries,
    }


def run_core_flow() -> Dict[str, Any]:
    """Run one complete document-search engine session."""
    ensure_data_dirs()
    config = create_engine_config()

    run_id = _run_id()
    started = time.perf_counter()

    documents = load_document_corpus()
    if not documents:
        documents = _default_documents()
        save_document_corpus(documents)

    queries = load_query_set()
    if not queries:
        queries = _default_queries()
        save_query_set(queries)

    doc_matrix, vocabulary, idf = _build_tfidf_index(
        documents,
        min_token_length=config['min_token_length'],
        include_bigrams=config['include_bigrams'],
    )

    query_reports: List[Dict[str, Any]] = []
    all_results: List[Dict[str, Any]] = []
    metadata_files: List[str] = []

    for query in queries:
        ranked = _rank_query(
            query,
            documents,
            doc_matrix,
            vocabulary,
            idf,
            config,
        )
        query_reports.append(
            {
                'query_id': query.get('query_id', ''),
                'query_text': query.get('query_text', ''),
                'results': ranked,
            }
        )
        for row in ranked:
            result_record = create_search_record(
                query_id=row['query_id'],
                query_text=row['query_text'],
                rank=row['rank'],
                doc_id=row['doc_id'],
                title=row['title'],
                semantic_score=row['semantic_score'],
                lexical_score=row['lexical_score'],
                blended_score=row['blended_score'],
            )
            metadata_files.append(save_search_record(result_record, run_id))
            all_results.append(row)

    all_results.sort(key=lambda item: item['blended_score'], reverse=True)

    index_payload = {
        'run_id': run_id,
        'doc_ids': [doc['doc_id'] for doc in documents],
        'doc_titles': [doc['title'] for doc in documents],
        'vocabulary_size': len(vocabulary),
        'idf': idf.round(6).tolist(),
    }
    index_file = OUTPUTS_DIR / f'index_{run_id}.json'
    index_file.write_text(json_dumps(index_payload), encoding='utf-8')

    results_file = OUTPUTS_DIR / f'results_{run_id}.json'
    results_file.write_text(
        json_dumps(
            {
                'run_id': run_id,
                'config': {
                    'top_k': config['top_k'],
                    'min_score': config['min_score'],
                    'semantic_weight': config['semantic_weight'],
                    'lexical_weight': config['lexical_weight'],
                },
                'query_reports': query_reports,
            }
        ),
        encoding='utf-8',
    )

    elapsed_ms = (time.perf_counter() - started) * 1000.0

    artifacts: Dict[str, Any] = {
        'run_file': str(OUTPUTS_DIR / f'run_{run_id}.json'),
        'index_file': str(index_file),
        'results_file': str(results_file),
        'metadata_files': metadata_files,
    }

    query_previews = []
    for report in query_reports:
        top_hit = report['results'][0] if report['results'] else None
        query_previews.append(
            {
                'query_id': report['query_id'],
                'query_text': report['query_text'],
                'top_doc_id': top_hit['doc_id'] if top_hit else '-',
                'top_score': float(top_hit['blended_score']) if top_hit else 0.0,
            }
        )

    scores = [row['blended_score'] for row in all_results]
    mean_score = float(np.mean(scores)) if scores else 0.0
    max_score = max(scores) if scores else 0.0
    min_score = min(scores) if scores else 0.0

    summary = create_run_summary(
        run_id=run_id,
        documents_indexed=len(documents),
        queries_executed=len(queries),
        results_returned=len(all_results),
        elapsed_ms=elapsed_ms,
        artifacts=artifacts,
        query_previews=query_previews,
        top_results=all_results[:10],
        metrics={
            'vocab_size': len(vocabulary),
            'mean_blended_score': mean_score,
            'max_blended_score': max_score,
            'min_blended_score': min_score,
            'min_score_threshold': config['min_score'],
        },
    )

    save_run_record(summary)
    return summary


def json_dumps(data: Any) -> str:
    """Serialize JSON with deterministic formatting."""
    import json

    return json.dumps(data, indent=2, sort_keys=False)
