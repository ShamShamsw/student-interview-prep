"""
operations.py - Business logic for Project 33: Plagiarism Similarity Detector
"""

from __future__ import annotations

from datetime import datetime
import re
import time
from typing import Any, Dict, List, Tuple

import numpy as np

from models import (
    create_detector_config,
    create_run_summary,
    create_similarity_record,
)
from storage import (
    OUTPUTS_DIR,
    ensure_data_dirs,
    load_analysis_catalog,
    load_document_corpus,
    load_run_catalog,
    save_analysis_record,
    save_document_corpus,
    save_run_record,
)


def _run_id() -> str:
    """Build a compact run ID from UTC timestamp."""
    return datetime.utcnow().strftime('%Y%m%d_%H%M%S')


def _default_documents() -> List[Dict[str, str]]:
    """Return a deterministic starter corpus used on first run."""
    return [
        {
            'doc_id': 'doc_001',
            'title': 'Neural Network Basics Essay',
            'author': 'student_a',
            'text': (
                'A neural network is a layered function approximator. '
                'Training updates weights with gradient descent so predictions '
                'match labeled examples.'
            ),
        },
        {
            'doc_id': 'doc_002',
            'title': 'Intro To Neural Networks',
            'author': 'student_b',
            'text': (
                'Neural networks approximate complex functions with layers. '
                'During training, gradient descent adjusts weights to reduce '
                'the prediction error on labeled data.'
            ),
        },
        {
            'doc_id': 'doc_003',
            'title': 'Photosynthesis Overview',
            'author': 'student_c',
            'text': (
                'Photosynthesis converts light energy into chemical energy. '
                'Plants use chlorophyll to capture light and produce glucose '
                'from carbon dioxide and water.'
            ),
        },
        {
            'doc_id': 'doc_004',
            'title': 'Plant Energy Conversion Notes',
            'author': 'student_d',
            'text': (
                'Plants transform sunlight into stored chemical energy. '
                'Chlorophyll captures light so the plant can synthesize glucose '
                'using water and carbon dioxide.'
            ),
        },
        {
            'doc_id': 'doc_005',
            'title': 'Roman Empire Timeline',
            'author': 'student_e',
            'text': (
                'The Roman Empire expanded across Europe and the Mediterranean. '
                'Administrative reforms and military organization helped it rule '
                'for centuries before western decline.'
            ),
        },
        {
            'doc_id': 'doc_006',
            'title': 'Bread Baking Process',
            'author': 'student_f',
            'text': (
                'Bread baking starts by mixing flour, water, yeast, and salt. '
                'After kneading and proofing, the dough is baked until crust '
                'and crumb structure are formed.'
            ),
        },
        {
            'doc_id': 'doc_007',
            'title': 'Classical Mechanics Summary',
            'author': 'student_g',
            'text': (
                'Classical mechanics explains motion with force, mass, and '
                'acceleration. Newton laws describe how objects respond to '
                'external interactions.'
            ),
        },
        {
            'doc_id': 'doc_008',
            'title': 'Newtonian Motion Notes',
            'author': 'student_h',
            'text': (
                'Newtonian mechanics models motion through forces acting on mass. '
                'The three laws of motion determine acceleration and momentum '
                'changes in physical systems.'
            ),
        },
    ]


def _tokenize(text: str, min_token_length: int) -> List[str]:
    """Tokenize and normalize free-form text."""
    tokens = re.findall(r"[a-zA-Z']+", text.lower())
    return [tok for tok in tokens if len(tok) >= min_token_length]


def _document_terms(
    text: str, min_token_length: int, include_bigrams: bool
) -> List[str]:
    """Build token list, optionally extending it with bigrams."""
    tokens = _tokenize(text, min_token_length)
    if not include_bigrams or len(tokens) < 2:
        return tokens
    bigrams = [f'{tokens[i]}_{tokens[i + 1]}' for i in range(len(tokens) - 1)]
    return tokens + bigrams


def _build_tfidf_matrix(
    documents: List[Dict[str, Any]],
    min_token_length: int,
    include_bigrams: bool,
) -> Tuple[np.ndarray, Dict[str, int]]:
    """Build a TF-IDF matrix using only numpy + python stdlib."""
    tokenized_docs: List[List[str]] = [
        _document_terms(doc.get('text', ''), min_token_length, include_bigrams)
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
        return np.zeros((0, 0), dtype=np.float32), vocabulary

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
    return normalized.astype(np.float32), vocabulary


def _cosine_similarity_matrix(vectors: np.ndarray) -> np.ndarray:
    """Compute dense cosine similarity matrix for normalized vectors."""
    if vectors.size == 0:
        return np.zeros((0, 0), dtype=np.float32)
    sim = vectors @ vectors.T
    sim = np.clip(sim, -1.0, 1.0)
    np.fill_diagonal(sim, 1.0)
    return sim.astype(np.float32)


def _jaccard_similarity(tokens_a: List[str], tokens_b: List[str]) -> float:
    """Compute lexical overlap with Jaccard index."""
    set_a = set(tokens_a)
    set_b = set(tokens_b)
    if not set_a and not set_b:
        return 0.0
    inter = len(set_a & set_b)
    union = len(set_a | set_b)
    return float(inter / union) if union else 0.0


def _risk_label(score: float) -> str:
    """Map similarity score to coarse plagiarism risk bands."""
    if score >= 0.25:
        return 'critical'
    if score >= 0.15:
        return 'high'
    if score >= 0.10:
        return 'medium'
    return 'low'


def _pairwise_rows(
    documents: List[Dict[str, Any]],
    semantic_matrix: np.ndarray,
    min_token_length: int,
) -> List[Dict[str, Any]]:
    """Flatten upper-triangle similarity matrix into sortable pair rows."""
    doc_tokens = [
        _tokenize(doc.get('text', ''), min_token_length) for doc in documents
    ]
    rows: List[Dict[str, Any]] = []
    n_docs = len(documents)
    for i in range(n_docs):
        for j in range(i + 1, n_docs):
            semantic_score = float(semantic_matrix[i, j])
            lexical_score = _jaccard_similarity(doc_tokens[i], doc_tokens[j])
            rows.append(
                {
                    'pair_id': f'{documents[i]["doc_id"]}__{documents[j]["doc_id"]}',
                    'doc_a_id': documents[i]['doc_id'],
                    'doc_b_id': documents[j]['doc_id'],
                    'doc_a_title': documents[i]['title'],
                    'doc_b_title': documents[j]['title'],
                    'semantic_score': semantic_score,
                    'lexical_score': lexical_score,
                    'risk_level': _risk_label(semantic_score),
                }
            )
    rows.sort(key=lambda item: item['semantic_score'], reverse=True)
    return rows


def _nearest_neighbor_rows(
    documents: List[Dict[str, Any]], semantic_matrix: np.ndarray
) -> List[Dict[str, Any]]:
    """Build nearest-neighbor report row for each document."""
    rows: List[Dict[str, Any]] = []
    n_docs = len(documents)
    if n_docs <= 1:
        return rows
    for i in range(n_docs):
        scores = semantic_matrix[i].copy()
        scores[i] = -1.0
        j = int(np.argmax(scores))
        rows.append(
            {
                'doc_id': documents[i]['doc_id'],
                'title': documents[i]['title'],
                'nearest_doc_id': documents[j]['doc_id'],
                'nearest_title': documents[j]['title'],
                'score': float(scores[j]),
            }
        )
    rows.sort(key=lambda item: item['score'], reverse=True)
    return rows


def _cluster_documents(
    documents: List[Dict[str, Any]],
    semantic_matrix: np.ndarray,
    threshold: float,
) -> List[Dict[str, Any]]:
    """Cluster documents via threshold graph connected components."""
    n_docs = len(documents)
    visited = [False] * n_docs
    clusters: List[List[int]] = []

    adjacency: List[List[int]] = [[] for _ in range(n_docs)]
    for i in range(n_docs):
        for j in range(i + 1, n_docs):
            if float(semantic_matrix[i, j]) >= threshold:
                adjacency[i].append(j)
                adjacency[j].append(i)

    for start in range(n_docs):
        if visited[start]:
            continue
        stack = [start]
        visited[start] = True
        component: List[int] = []
        while stack:
            node = stack.pop()
            component.append(node)
            for nbr in adjacency[node]:
                if not visited[nbr]:
                    visited[nbr] = True
                    stack.append(nbr)
        clusters.append(sorted(component))

    rows: List[Dict[str, Any]] = []
    for idx, members in enumerate(sorted(clusters, key=len, reverse=True), start=1):
        member_titles = [documents[m]['title'] for m in members]
        avg_internal = 1.0
        if len(members) > 1:
            pairs = []
            for a in range(len(members)):
                for b in range(a + 1, len(members)):
                    pairs.append(float(semantic_matrix[members[a], members[b]]))
            avg_internal = float(np.mean(pairs)) if pairs else 1.0
        rows.append(
            {
                'cluster_id': f'cluster_{idx:02d}',
                'size': len(members),
                'avg_similarity': avg_internal,
                'members': [documents[m]['doc_id'] for m in members],
                'titles_preview': member_titles[:3],
            }
        )
    return rows


def load_detector_profile() -> Dict[str, Any]:
    """Return startup profile built from previously saved catalogs."""
    runs = load_run_catalog()
    analyses = load_analysis_catalog()
    documents = load_document_corpus()
    recent_high_risk = [
        f"{item.get('pair_id', '')}:{item.get('semantic_score', 0.0):.2f}"
        for item in analyses[-8:]
        if item.get('risk_level') in {'high', 'critical'}
    ]
    return {
        'catalog_file': 'data/runs.json',
        'analysis_catalog_file': 'data/analyses.json',
        'documents_file': 'data/documents.json',
        'runs_stored': len(runs),
        'analyses_stored': len(analyses),
        'documents_available': len(documents),
        'recent_high_risk': recent_high_risk,
    }


def run_core_flow() -> Dict[str, Any]:
    """Run one complete plagiarism similarity detection session."""
    ensure_data_dirs()
    config = create_detector_config()

    run_id = _run_id()
    started = time.perf_counter()

    documents = load_document_corpus()
    if not documents:
        documents = _default_documents()
        save_document_corpus(documents)

    matrix, vocabulary = _build_tfidf_matrix(
        documents,
        min_token_length=config['min_token_length'],
        include_bigrams=config['include_bigrams'],
    )
    semantic_matrix = _cosine_similarity_matrix(matrix)
    pair_rows = _pairwise_rows(
        documents,
        semantic_matrix,
        min_token_length=config['min_token_length'],
    )

    similarity_threshold = config['similarity_threshold']
    flagged = [row for row in pair_rows if row['semantic_score'] >= similarity_threshold]
    nearest_rows = _nearest_neighbor_rows(documents, semantic_matrix)
    cluster_rows = _cluster_documents(
        documents,
        semantic_matrix,
        threshold=config['cluster_threshold'],
    )

    matrix_payload = {
        'run_id': run_id,
        'doc_ids': [doc['doc_id'] for doc in documents],
        'doc_titles': [doc['title'] for doc in documents],
        'similarity_matrix': semantic_matrix.round(6).tolist(),
    }
    matrix_file = OUTPUTS_DIR / f'similarity_matrix_{run_id}.json'
    matrix_file.write_text(
        json_dumps(matrix_payload),
        encoding='utf-8',
    )

    pair_file = OUTPUTS_DIR / f'pairs_{run_id}.json'
    pair_file.write_text(
        json_dumps(
            {
                'run_id': run_id,
                'similarity_threshold': similarity_threshold,
                'pairs': pair_rows,
                'flagged_pairs': flagged,
            }
        ),
        encoding='utf-8',
    )

    cluster_file = OUTPUTS_DIR / f'clusters_{run_id}.json'
    cluster_file.write_text(
        json_dumps(
            {
                'run_id': run_id,
                'cluster_threshold': config['cluster_threshold'],
                'clusters': cluster_rows,
            }
        ),
        encoding='utf-8',
    )

    metadata_files: List[str] = []
    for row in flagged:
        record = create_similarity_record(
            pair_id=row['pair_id'],
            doc_a_id=row['doc_a_id'],
            doc_b_id=row['doc_b_id'],
            doc_a_title=row['doc_a_title'],
            doc_b_title=row['doc_b_title'],
            semantic_score=row['semantic_score'],
            lexical_score=row['lexical_score'],
            risk_level=row['risk_level'],
        )
        metadata_files.append(save_analysis_record(record, run_id))

    mean_similarity = float(np.mean(semantic_matrix)) if semantic_matrix.size else 0.0
    off_diag_scores = [r['semantic_score'] for r in pair_rows]
    median_off_diag = float(np.median(off_diag_scores)) if off_diag_scores else 0.0
    max_pair_score = max(off_diag_scores) if off_diag_scores else 0.0

    elapsed_ms = (time.perf_counter() - started) * 1000.0

    artifacts: Dict[str, Any] = {
        'run_file': str(OUTPUTS_DIR / f'run_{run_id}.json'),
        'similarity_matrix_file': str(matrix_file),
        'pair_report_file': str(pair_file),
        'cluster_report_file': str(cluster_file),
        'metadata_files': metadata_files,
    }

    summary = create_run_summary(
        run_id=run_id,
        documents_processed=len(documents),
        pairs_compared=len(pair_rows),
        flagged_pairs=len(flagged),
        clusters_found=len([c for c in cluster_rows if c['size'] > 1]),
        elapsed_ms=elapsed_ms,
        artifacts=artifacts,
        pair_previews=pair_rows[: config['max_pairs_in_report']],
        nearest_neighbors=nearest_rows,
        cluster_previews=cluster_rows,
        metrics={
            'vocab_size': len(vocabulary),
            'mean_similarity': mean_similarity,
            'median_pair_similarity': median_off_diag,
            'max_pair_similarity': max_pair_score,
            'threshold': similarity_threshold,
        },
    )

    save_run_record(summary)
    return summary


def json_dumps(data: Any) -> str:
    """Serialize JSON with deterministic formatting."""
    import json

    return json.dumps(data, indent=2, sort_keys=False)
