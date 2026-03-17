"""
storage.py - Persistence layer for Project 34: Document Search Engine
"""

from pathlib import Path
import json
from typing import Any, Dict, List

DATA_DIR = Path(__file__).resolve().parent / 'data'
OUTPUTS_DIR = DATA_DIR / 'outputs'
CATALOG_FILE = DATA_DIR / 'runs.json'
SEARCH_CATALOG_FILE = DATA_DIR / 'searches.json'
DOCUMENTS_FILE = DATA_DIR / 'documents.json'
QUERIES_FILE = DATA_DIR / 'queries.json'


def ensure_data_dirs() -> None:
    """Create local data/output directories if they do not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def ensure_data_dir() -> None:
    """Backwards-compatible alias for older scaffold code."""
    ensure_data_dirs()


def _load_list_file(path: Path) -> List[Dict[str, Any]]:
    """Safely load a list-based JSON file."""
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def _save_list_file(path: Path, data: List[Dict[str, Any]]) -> None:
    """Persist list-based JSON with indentation."""
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')


def load_run_catalog() -> List[Dict[str, Any]]:
    """Load run catalog entries from disk."""
    ensure_data_dirs()
    return _load_list_file(CATALOG_FILE)


def save_run_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Persist run catalog to disk."""
    ensure_data_dirs()
    _save_list_file(CATALOG_FILE, catalog)


def load_search_catalog() -> List[Dict[str, Any]]:
    """Load search-result catalog entries from disk."""
    ensure_data_dirs()
    return _load_list_file(SEARCH_CATALOG_FILE)


def save_search_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Persist search-result catalog to disk."""
    ensure_data_dirs()
    _save_list_file(SEARCH_CATALOG_FILE, catalog)


def load_document_corpus() -> List[Dict[str, Any]]:
    """Load document corpus from disk."""
    ensure_data_dirs()
    return _load_list_file(DOCUMENTS_FILE)


def save_document_corpus(documents: List[Dict[str, Any]]) -> str:
    """Persist document corpus to disk."""
    ensure_data_dirs()
    _save_list_file(DOCUMENTS_FILE, documents)
    return str(DOCUMENTS_FILE)


def load_query_set() -> List[Dict[str, Any]]:
    """Load default query set from disk."""
    ensure_data_dirs()
    return _load_list_file(QUERIES_FILE)


def save_query_set(queries: List[Dict[str, Any]]) -> str:
    """Persist default query set to disk."""
    ensure_data_dirs()
    _save_list_file(QUERIES_FILE, queries)
    return str(QUERIES_FILE)


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
            'documents_indexed': run_record.get('documents_indexed', 0),
            'queries_executed': run_record.get('queries_executed', 0),
            'results_returned': run_record.get('results_returned', 0),
            'elapsed_ms': run_record.get('elapsed_ms', 0.0),
            'finished_at': run_record.get('finished_at', ''),
            'run_file': str(file_path),
        }
    )
    save_run_catalog(catalog)
    return str(file_path)


def save_search_record(search_record: Dict[str, Any], run_id: str) -> str:
    """Persist one search result record and update search catalog."""
    ensure_data_dirs()
    query_id = search_record['query_id']
    rank = int(search_record.get('rank', 0))
    file_path = OUTPUTS_DIR / f'search_{query_id}_rank_{rank:02d}_{run_id}.json'
    file_path.write_text(json.dumps(search_record, indent=2), encoding='utf-8')

    catalog = load_search_catalog()
    catalog.append(
        {
            'query_id': query_id,
            'run_id': run_id,
            'rank': rank,
            'doc_id': search_record.get('doc_id', ''),
            'blended_score': search_record.get('blended_score', 0.0),
            'created_at': search_record.get('created_at', ''),
            'metadata_file': str(file_path),
        }
    )
    save_search_catalog(catalog)
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
