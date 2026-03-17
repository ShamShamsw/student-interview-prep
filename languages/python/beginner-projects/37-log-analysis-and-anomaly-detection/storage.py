"""
storage.py - Persistence layer for Project 37: Log Analysis And Anomaly Detection
"""

from pathlib import Path
import json
from typing import Any, Dict, List

DATA_DIR = Path(__file__).resolve().parent / 'data'
OUTPUTS_DIR = DATA_DIR / 'outputs'
RUN_CATALOG_FILE = DATA_DIR / 'runs.json'
ANOMALY_CATALOG_FILE = DATA_DIR / 'anomalies.json'
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
    return _load_list_file(RUN_CATALOG_FILE)


def save_run_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Persist run catalog to disk."""
    ensure_data_dirs()
    _save_list_file(RUN_CATALOG_FILE, catalog)


def load_anomaly_catalog() -> List[Dict[str, Any]]:
    """Load anomaly catalog entries from disk."""
    ensure_data_dirs()
    return _load_list_file(ANOMALY_CATALOG_FILE)


def save_anomaly_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Persist anomaly catalog to disk."""
    ensure_data_dirs()
    _save_list_file(ANOMALY_CATALOG_FILE, catalog)


def load_log_library() -> List[Dict[str, Any]]:
    """Load log library from disk."""
    ensure_data_dirs()
    return _load_list_file(LIBRARY_FILE)


def save_log_library(library: List[Dict[str, Any]]) -> str:
    """Persist log library to disk."""
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
            'log_lines_processed': run_record.get('log_lines_processed', 0),
            'parsed_events': run_record.get('parsed_events', 0),
            'anomalies_detected': run_record.get('anomalies_detected', 0),
            'unique_ips': run_record.get('unique_ips', 0),
            'elapsed_ms': run_record.get('elapsed_ms', 0.0),
            'finished_at': run_record.get('finished_at', ''),
            'run_file': str(file_path),
        }
    )
    save_run_catalog(catalog)
    return str(file_path)


def save_anomaly_record(anomaly_record: Dict[str, Any], run_id: str) -> str:
    """Persist one anomaly record and update anomaly catalog."""
    ensure_data_dirs()
    anomaly_id = anomaly_record['anomaly_id']
    file_path = OUTPUTS_DIR / f'anomaly_{anomaly_id}_{run_id}.json'
    file_path.write_text(json.dumps(anomaly_record, indent=2), encoding='utf-8')

    catalog = load_anomaly_catalog()
    catalog.append(
        {
            'anomaly_id': anomaly_id,
            'run_id': run_id,
            'source_id': anomaly_record.get('source_id', ''),
            'anomaly_type': anomaly_record.get('anomaly_type', ''),
            'score': anomaly_record.get('score', 0.0),
            'timestamp': anomaly_record.get('timestamp', ''),
            'metadata_file': str(file_path),
        }
    )
    save_anomaly_catalog(catalog)
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
