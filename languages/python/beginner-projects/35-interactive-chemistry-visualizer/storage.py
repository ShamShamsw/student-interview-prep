"""
storage.py - Persistence layer for Project 35: Interactive Chemistry Visualizer
"""

from pathlib import Path
import json
from typing import Any, Dict, List

DATA_DIR = Path(__file__).resolve().parent / 'data'
OUTPUTS_DIR = DATA_DIR / 'outputs'
CATALOG_FILE = DATA_DIR / 'runs.json'
MOLECULE_CATALOG_FILE = DATA_DIR / 'molecules.json'
LIBRARY_FILE = DATA_DIR / 'library.json'


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


def load_molecule_catalog() -> List[Dict[str, Any]]:
    """Load molecule property catalog entries from disk."""
    ensure_data_dirs()
    return _load_list_file(MOLECULE_CATALOG_FILE)


def save_molecule_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Persist molecule property catalog to disk."""
    ensure_data_dirs()
    _save_list_file(MOLECULE_CATALOG_FILE, catalog)


def load_library() -> List[Dict[str, Any]]:
    """Load molecule library from disk."""
    ensure_data_dirs()
    return _load_list_file(LIBRARY_FILE)


def save_library(library: List[Dict[str, Any]]) -> str:
    """Persist molecule library to disk."""
    ensure_data_dirs()
    _save_list_file(LIBRARY_FILE, library)
    return str(LIBRARY_FILE)


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
            'molecules_processed': run_record.get('molecules_processed', 0),
            'properties_computed': run_record.get('properties_computed', 0),
            'lipinski_pass_count': run_record.get('lipinski_pass_count', 0),
            'elapsed_ms': run_record.get('elapsed_ms', 0.0),
            'finished_at': run_record.get('finished_at', ''),
            'run_file': str(file_path),
        }
    )
    save_run_catalog(catalog)
    return str(file_path)


def save_molecule_record(mol_record: Dict[str, Any], run_id: str) -> str:
    """Persist one molecule property record and update molecule catalog."""
    ensure_data_dirs()
    mol_id = mol_record['mol_id']
    file_path = OUTPUTS_DIR / f'mol_{mol_id}_{run_id}.json'
    file_path.write_text(json.dumps(mol_record, indent=2), encoding='utf-8')

    catalog = load_molecule_catalog()
    catalog.append(
        {
            'mol_id': mol_id,
            'run_id': run_id,
            'name': mol_record.get('name', ''),
            'formula': mol_record.get('formula', ''),
            'mol_weight': mol_record.get('mol_weight', 0.0),
            'lipinski_pass': mol_record.get('lipinski_pass', False),
            'created_at': mol_record.get('created_at', ''),
            'metadata_file': str(file_path),
        }
    )
    save_molecule_catalog(catalog)
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
