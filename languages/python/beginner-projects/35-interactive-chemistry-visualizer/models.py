"""
models.py - Data models for Project 35: Interactive Chemistry Visualizer
"""

from datetime import datetime
from typing import Any, Dict, List


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string."""
    return datetime.utcnow().isoformat(timespec='seconds') + 'Z'


def create_visualizer_config(
    top_properties: int = 6,
    include_formula: bool = True,
    include_weight: bool = True,
    include_rings: bool = True,
    include_hbond: bool = True,
    max_molecules_in_report: int = 8,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """Create a validated chemistry visualizer configuration record."""
    return {
        'project_type': 'interactive_chemistry_visualizer',
        'top_properties': max(1, int(top_properties)),
        'include_formula': bool(include_formula),
        'include_weight': bool(include_weight),
        'include_rings': bool(include_rings),
        'include_hbond': bool(include_hbond),
        'max_molecules_in_report': max(3, int(max_molecules_in_report)),
        'random_seed': int(random_seed),
        'created_at': _utc_timestamp(),
    }


def create_molecule_record(
    mol_id: str,
    name: str,
    smiles: str,
    formula: str,
    mol_weight: float,
    num_rings: int,
    hbd: int,
    hba: int,
    logp: float,
    rotatable_bonds: int,
    lipinski_pass: bool,
) -> Dict[str, Any]:
    """Create one computed molecule property record."""
    return {
        'mol_id': mol_id,
        'name': name,
        'smiles': smiles,
        'formula': formula,
        'mol_weight': round(float(mol_weight), 4),
        'num_rings': int(num_rings),
        'hbd': int(hbd),
        'hba': int(hba),
        'logp': round(float(logp), 4),
        'rotatable_bonds': int(rotatable_bonds),
        'lipinski_pass': bool(lipinski_pass),
        'created_at': _utc_timestamp(),
    }


def create_run_summary(
    run_id: str,
    molecules_processed: int,
    properties_computed: int,
    lipinski_pass_count: int,
    elapsed_ms: float,
    artifacts: Dict[str, Any],
    molecule_previews: List[Dict[str, Any]],
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """Create final run summary for reporting and persistence."""
    return {
        'run_id': run_id,
        'molecules_processed': int(molecules_processed),
        'properties_computed': int(properties_computed),
        'lipinski_pass_count': int(lipinski_pass_count),
        'elapsed_ms': float(elapsed_ms),
        'artifacts': artifacts,
        'molecule_previews': molecule_previews,
        'metrics': metrics,
        'finished_at': _utc_timestamp(),
    }


def create_record(**kwargs: Any) -> Dict[str, Any]:
    """Backwards-compatible generic record factory."""
    return dict(kwargs)
