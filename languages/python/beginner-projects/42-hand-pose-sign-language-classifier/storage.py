import json
from pathlib import Path
from typing import Any, Dict, List

"""Persistence layer for Project 42: Hand-Pose Sign Language Classifier."""

DATA_DIR = Path(__file__).resolve().parent / 'data'
OUTPUTS_DIR = DATA_DIR / 'outputs'
TEMPLATE_LIBRARY_FILE = DATA_DIR / 'sign_templates.json'
DATASET_FILE = DATA_DIR / 'dataset.json'
RUN_CATALOG_FILE = DATA_DIR / 'runs.json'


def ensure_data_dirs() -> None:
    """Create local data and output directories if they do not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


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


def load_template_library() -> List[Dict[str, Any]]:
    """Load sign templates from disk."""
    ensure_data_dirs()
    return _load_list_file(TEMPLATE_LIBRARY_FILE)


def save_template_library(library: List[Dict[str, Any]]) -> str:
    """Persist sign template definitions to disk."""
    ensure_data_dirs()
    _save_list_file(TEMPLATE_LIBRARY_FILE, library)
    return str(TEMPLATE_LIBRARY_FILE)


def load_dataset_catalog() -> List[Dict[str, Any]]:
    """Load captured dataset records from disk."""
    ensure_data_dirs()
    return _load_list_file(DATASET_FILE)


def save_dataset_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Persist captured dataset records to disk."""
    ensure_data_dirs()
    _save_list_file(DATASET_FILE, catalog)


def load_run_catalog() -> List[Dict[str, Any]]:
    """Load run catalog entries from disk."""
    ensure_data_dirs()
    return _load_list_file(RUN_CATALOG_FILE)


def save_run_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Persist run catalog entries to disk."""
    ensure_data_dirs()
    _save_list_file(RUN_CATALOG_FILE, catalog)


def save_model_file(model_payload: Dict[str, Any], session_id: str) -> str:
    """Persist the trained classifier payload for a session."""
    ensure_data_dirs()
    file_path = OUTPUTS_DIR / f'model_{session_id}.json'
    file_path.write_text(json.dumps(model_payload, indent=2), encoding='utf-8')
    return str(file_path)


def save_live_inference_file(predictions: List[Dict[str, Any]], session_id: str) -> str:
    """Persist the live inference bundle for a session."""
    ensure_data_dirs()
    file_path = OUTPUTS_DIR / f'live_inference_{session_id}.json'
    file_path.write_text(
        json.dumps({'session_id': session_id, 'predictions': predictions}, indent=2),
        encoding='utf-8',
    )
    return str(file_path)


def save_run_record(run_record: Dict[str, Any]) -> str:
    """Persist one run record and update the run catalog."""
    ensure_data_dirs()
    session_id = run_record['session_id']
    file_path = OUTPUTS_DIR / f'run_{session_id}.json'
    file_path.write_text(json.dumps(run_record, indent=2), encoding='utf-8')

    catalog = load_run_catalog()
    catalog.append(
        {
            'session_id': session_id,
            'signs_modeled': run_record.get('signs_modeled', 0),
            'captures_total': run_record.get('captures_total', 0),
            'training_samples': run_record.get('training_samples', 0),
            'test_samples': run_record.get('test_samples', 0),
            'test_accuracy': run_record.get('test_accuracy', 0.0),
            'live_frames': run_record.get('live_frames', 0),
            'low_confidence_frames': run_record.get('low_confidence_frames', 0),
            'elapsed_ms': run_record.get('elapsed_ms', 0.0),
            'finished_at': run_record.get('finished_at', ''),
            'run_file': str(file_path),
        }
    )
    save_run_catalog(catalog)
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
