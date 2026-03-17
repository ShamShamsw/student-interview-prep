"""storage.py - Persistence layer for Project 40: Real-Time Collaborative Notebook Demo."""

import json
from pathlib import Path
from typing import Any, Dict, List

DATA_DIR = Path(__file__).resolve().parent / 'data'
OUTPUTS_DIR = DATA_DIR / 'outputs'
NOTEBOOK_LIBRARY_FILE = DATA_DIR / 'notebooks.json'
SESSION_CATALOG_FILE = DATA_DIR / 'sessions.json'
EDIT_CATALOG_FILE = DATA_DIR / 'edits.json'


def ensure_data_dirs() -> None:
    """Create local data/output directories if they do not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def ensure_data_dir() -> None:
    """Backwards-compatible alias."""
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


def load_notebook_library() -> List[Dict[str, Any]]:
    """Load notebook definitions from disk."""
    ensure_data_dirs()
    return _load_list_file(NOTEBOOK_LIBRARY_FILE)


def save_notebook_library(library: List[Dict[str, Any]]) -> str:
    """Persist notebook definitions to disk."""
    ensure_data_dirs()
    _save_list_file(NOTEBOOK_LIBRARY_FILE, library)
    return str(NOTEBOOK_LIBRARY_FILE)


def load_session_catalog() -> List[Dict[str, Any]]:
    """Load session catalog entries from disk."""
    ensure_data_dirs()
    return _load_list_file(SESSION_CATALOG_FILE)


def save_session_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Persist session catalog to disk."""
    ensure_data_dirs()
    _save_list_file(SESSION_CATALOG_FILE, catalog)


def load_edit_catalog() -> List[Dict[str, Any]]:
    """Load edit catalog entries from disk."""
    ensure_data_dirs()
    return _load_list_file(EDIT_CATALOG_FILE)


def save_edit_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Persist edit catalog to disk."""
    ensure_data_dirs()
    _save_list_file(EDIT_CATALOG_FILE, catalog)


def save_session_record(session_record: Dict[str, Any]) -> str:
    """Persist one session record and update session catalog."""
    ensure_data_dirs()
    session_id = session_record['session_id']
    file_path = OUTPUTS_DIR / f'session_{session_id}.json'
    file_path.write_text(json.dumps(session_record, indent=2), encoding='utf-8')

    catalog = load_session_catalog()
    catalog.append(
        {
            'session_id': session_id,
            'notebooks_processed': session_record.get('notebooks_processed', 0),
            'edits_total': session_record.get('edits_total', 0),
            'conflicts_total': session_record.get('conflicts_total', 0),
            'elapsed_ms': session_record.get('elapsed_ms', 0.0),
            'finished_at': session_record.get('finished_at', ''),
            'session_file': str(file_path),
        }
    )
    save_session_catalog(catalog)
    return str(file_path)


def save_edit_bundle(edits: List[Dict[str, Any]], session_id: str) -> str:
    """Persist the full edit log bundle for a session."""
    ensure_data_dirs()
    file_path = OUTPUTS_DIR / f'edits_{session_id}.json'
    file_path.write_text(
        json.dumps({'session_id': session_id, 'edits': edits}, indent=2),
        encoding='utf-8',
    )
    catalog = load_edit_catalog()
    for edit in edits:
        catalog.append(
            {
                'edit_id': edit.get('edit_id', ''),
                'session_id': session_id,
                'user_id': edit.get('user_id', ''),
                'cell_id': edit.get('cell_id', ''),
                'operation': edit.get('operation', ''),
                'is_conflict': edit.get('is_conflict', False),
                'status': edit.get('status', ''),
            }
        )
    save_edit_catalog(catalog)
    return str(file_path)


def load_json(filename: str):
    """Load JSON data from the local data directory."""
    ensure_data_dirs()
    path = DATA_DIR / filename
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []


def save_json(filename: str, data) -> None:
    """Save JSON data to the local data directory."""
    ensure_data_dirs()
    path = DATA_DIR / filename
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')
