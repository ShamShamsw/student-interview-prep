import json
from pathlib import Path
from typing import Any, Dict, List

DATA_DIR = Path(__file__).resolve().parent / 'data'
OUTPUTS_DIR = DATA_DIR / 'outputs'
RUN_CATALOG_FILE = DATA_DIR / 'runs.json'
SOLUTION_CATALOG_FILE = DATA_DIR / 'solutions.json'
PROBLEM_LIBRARY_FILE = DATA_DIR / 'problems.json'


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


def load_solution_catalog() -> List[Dict[str, Any]]:
    """Load optimization solution catalog entries from disk."""
    ensure_data_dirs()
    return _load_list_file(SOLUTION_CATALOG_FILE)


def save_solution_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Persist optimization solution catalog to disk."""
    ensure_data_dirs()
    _save_list_file(SOLUTION_CATALOG_FILE, catalog)


def load_problem_library() -> List[Dict[str, Any]]:
    """Load optimization problem definitions from disk."""
    ensure_data_dirs()
    return _load_list_file(PROBLEM_LIBRARY_FILE)


def save_problem_library(library: List[Dict[str, Any]]) -> str:
    """Persist optimization problem definitions to disk."""
    ensure_data_dirs()
    _save_list_file(PROBLEM_LIBRARY_FILE, library)
    return str(PROBLEM_LIBRARY_FILE)


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
            'problems_loaded': run_record.get('problems_loaded', 0),
            'solutions_generated': run_record.get('solutions_generated', 0),
            'successful_solves': run_record.get('successful_solves', 0),
            'elapsed_ms': run_record.get('elapsed_ms', 0.0),
            'finished_at': run_record.get('finished_at', ''),
            'run_file': str(file_path),
        }
    )
    save_run_catalog(catalog)
    return str(file_path)


def save_solution_record(solution_record: Dict[str, Any], run_id: str) -> str:
    """Persist one optimization solution record and update solution catalog."""
    ensure_data_dirs()
    solution_id = solution_record['solution_id']
    file_path = OUTPUTS_DIR / f'solution_{solution_id}_{run_id}.json'
    file_path.write_text(json.dumps(solution_record, indent=2), encoding='utf-8')

    catalog = load_solution_catalog()
    catalog.append(
        {
            'solution_id': solution_id,
            'run_id': run_id,
            'problem_id': solution_record.get('problem_id', ''),
            'problem_name': solution_record.get('problem_name', ''),
            'problem_kind': solution_record.get('problem_kind', ''),
            'solver_name': solution_record.get('solver_name', ''),
            'objective_value': solution_record.get('objective_value', 0.0),
            'status': solution_record.get('status', ''),
            'metadata_file': str(file_path),
        }
    )
    save_solution_catalog(catalog)
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
