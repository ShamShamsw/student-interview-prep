"""
storage.py - Persistence layer for Project 31: Fractal And Procedural Art Studio
"""

from pathlib import Path
import json
from typing import Any, Dict, List

DATA_DIR = Path(__file__).resolve().parent / 'data'
OUTPUTS_DIR = DATA_DIR / 'outputs'
CATALOG_FILE = DATA_DIR / 'runs.json'
ARTWORK_CATALOG_FILE = DATA_DIR / 'artworks.json'


def ensure_data_dirs() -> None:
    """Create local data and output directories if they do not exist."""
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


def load_artwork_catalog() -> List[Dict[str, Any]]:
    """Load artwork catalog entries from disk."""
    ensure_data_dirs()
    if not ARTWORK_CATALOG_FILE.exists():
        return []
    try:
        data = json.loads(ARTWORK_CATALOG_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def save_artwork_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Persist artwork catalog to disk."""
    ensure_data_dirs()
    ARTWORK_CATALOG_FILE.write_text(json.dumps(catalog, indent=2), encoding='utf-8')


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
            'artworks_created': run_record.get('artworks_created', 0),
            'elapsed_ms': run_record.get('elapsed_ms', 0.0),
            'finished_at': run_record.get('finished_at', ''),
            'run_file': str(file_path),
        }
    )
    save_run_catalog(catalog)
    return str(file_path)


def save_artwork_record(artwork_record: Dict[str, Any]) -> str:
    """Persist one artwork record and update artwork catalog."""
    ensure_data_dirs()
    artwork_id = artwork_record['artwork_id']
    file_path = OUTPUTS_DIR / f'artwork_{artwork_id}.json'
    file_path.write_text(json.dumps(artwork_record, indent=2), encoding='utf-8')

    catalog = load_artwork_catalog()
    catalog.append(
        {
            'artwork_id': artwork_id,
            'title': artwork_record.get('title', ''),
            'style': artwork_record.get('style', ''),
            'image_file': artwork_record.get('image_file', ''),
            'created_at': artwork_record.get('created_at', ''),
            'metadata_file': str(file_path),
        }
    )
    save_artwork_catalog(catalog)
    return str(file_path)


def load_json(filename: str):
    """Load JSON data from the local data directory."""
    ensure_data_dirs()
    path = DATA_DIR / filename
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding='utf-8'))


def save_json(filename: str, data: Any) -> None:
    """Save JSON data to the local data directory."""
    ensure_data_dirs()
    path = DATA_DIR / filename
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')
