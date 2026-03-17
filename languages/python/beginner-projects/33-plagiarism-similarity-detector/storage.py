"""
storage.py - Persistence layer for Project 33: Plagiarism Similarity Detector
"""

from pathlib import Path
import json
from typing import Any, Dict, List

DATA_DIR = Path(__file__).resolve().parent / 'data'
OUTPUTS_DIR = DATA_DIR / 'outputs'
CATALOG_FILE = DATA_DIR / 'runs.json'
ANALYSIS_CATALOG_FILE = DATA_DIR / 'analyses.json'
DOCUMENTS_FILE = DATA_DIR / 'documents.json'


def ensure_data_dirs() -> None:
    """Create local data/output directories if they do not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def ensure_data_dir() -> None:
    """Backwards-compatible alias for older scaffold code."""
    ensure_data_dirs()


def load_run_catalog() -> List[Dict[str, Any]]:
    """Load run catalog entries from disk."""
    ensure_data_dirs()
    if not CATALOG_FILE.exists():
        return []
    try:
        data = json.loads(CATALOG_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def save_run_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Persist run catalog to disk."""
    ensure_data_dirs()
    CATALOG_FILE.write_text(json.dumps(catalog, indent=2), encoding='utf-8')


def load_analysis_catalog() -> List[Dict[str, Any]]:
    """Load similarity-analysis catalog entries from disk."""
    ensure_data_dirs()
    if not ANALYSIS_CATALOG_FILE.exists():
        return []
    try:
        data = json.loads(ANALYSIS_CATALOG_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def save_analysis_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Persist similarity-analysis catalog to disk."""
    ensure_data_dirs()
    ANALYSIS_CATALOG_FILE.write_text(json.dumps(catalog, indent=2), encoding='utf-8')


def load_document_corpus() -> List[Dict[str, Any]]:
    """Load document corpus from disk."""
    ensure_data_dirs()
    if not DOCUMENTS_FILE.exists():
        return []
    try:
        data = json.loads(DOCUMENTS_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def save_document_corpus(documents: List[Dict[str, Any]]) -> str:
    """Persist document corpus to disk."""
    ensure_data_dirs()
    DOCUMENTS_FILE.write_text(json.dumps(documents, indent=2), encoding='utf-8')
    return str(DOCUMENTS_FILE)


def save_run_record(run_record: Dict[str, Any]) -> str:
    """Persist one run record and update run catalog."""
    ensure_data_dirs()
    run_id = run_record['run_id']
    file_path = OUTPUTS_DIR / f'run_{run_id}.json'
    file_path.write_text(json.dumps(run_record, indent=2), encoding='utf-8')

    catalog = load_run_catalog()
    catalog.append(
        {
            'run_id': run_id,
            'documents_processed': run_record.get('documents_processed', 0),
            'pairs_compared': run_record.get('pairs_compared', 0),
            'flagged_pairs': run_record.get('flagged_pairs', 0),
            'clusters_found': run_record.get('clusters_found', 0),
            'elapsed_ms': run_record.get('elapsed_ms', 0.0),
            'finished_at': run_record.get('finished_at', ''),
            'run_file': str(file_path),
        }
    )
    save_run_catalog(catalog)
    return str(file_path)


def save_analysis_record(analysis_record: Dict[str, Any], run_id: str) -> str:
    """Persist one similarity record and update analysis catalog."""
    ensure_data_dirs()
    pair_id = analysis_record['pair_id']
    file_path = OUTPUTS_DIR / f'analysis_{pair_id}_{run_id}.json'
    file_path.write_text(json.dumps(analysis_record, indent=2), encoding='utf-8')

    catalog = load_analysis_catalog()
    catalog.append(
        {
            'pair_id': pair_id,
            'run_id': run_id,
            'doc_a_id': analysis_record.get('doc_a_id', ''),
            'doc_b_id': analysis_record.get('doc_b_id', ''),
            'semantic_score': analysis_record.get('semantic_score', 0.0),
            'risk_level': analysis_record.get('risk_level', ''),
            'created_at': analysis_record.get('created_at', ''),
            'metadata_file': str(file_path),
        }
    )
    save_analysis_catalog(catalog)
    return str(file_path)


def load_json(filename: str) -> Any:
    """Load JSON data from the local data directory."""
    ensure_data_dirs()
    path = DATA_DIR / filename
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []


def save_json(filename: str, data: Any) -> None:
    """Save JSON data to the local data directory."""
    ensure_data_dirs()
    path = DATA_DIR / filename
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')
