"""
operations.py - Business logic for Project 35: Interactive Chemistry Visualizer
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime
import re
import time
from typing import Any, Dict, List, Tuple

from models import create_molecule_record, create_run_summary, create_visualizer_config
from storage import (
    OUTPUTS_DIR,
    ensure_data_dirs,
    load_library,
    load_molecule_catalog,
    load_run_catalog,
    save_library,
    save_molecule_record,
    save_run_record,
)


def _run_id() -> str:
    """Build a compact run ID from UTC timestamp."""
    return datetime.utcnow().strftime('%Y%m%d_%H%M%S')


# ---------------------------------------------------------------------------
# Minimal SMILES parser — no external dependencies
# ---------------------------------------------------------------------------

# Atomic weights (most common elements in organic chemistry)
_ATOMIC_WEIGHTS: Dict[str, float] = {
    'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999,
    'F': 18.998, 'P': 30.974, 'S': 32.06, 'Cl': 35.45,
    'Br': 79.904, 'I': 126.904, 'B': 10.811, 'Si': 28.085,
    'Na': 22.990, 'K': 39.098, 'Ca': 40.078, 'Mg': 24.305,
    'Fe': 55.845, 'Zn': 65.38, 'Cu': 63.546, 'Mn': 54.938,
    'Se': 78.971, 'As': 74.922,
}

# LogP contribution per atom type (simplified Wildman-Crippen-style)
_LOGP_CONTRIB: Dict[str, float] = {
    'C': 0.33, 'H': 0.12, 'N': -0.68, 'O': -0.67,
    'F': 0.14, 'P': 0.41, 'S': 0.20, 'Cl': 0.60,
    'Br': 0.88, 'I': 1.35, 'B': 0.10, 'Si': 0.25,
}


def _parse_smiles_atoms(smiles: str) -> List[str]:
    """Extract element symbols from a SMILES string.

    Returns a tuple of:
      - all heavy-atom symbols (uppercase, aromatic normalized)
      - Counter of aromatic atoms (originally lowercase in SMILES)
    """
    aromatic_map = {'c': 'C', 'n': 'N', 'o': 'O', 's': 'S', 'p': 'P', 'b': 'B'}

    # Extract atoms inside square brackets (e.g. [C@@H], [NH2+])
    bracket_atoms: List[str] = []
    for bracket_content in re.findall(r'\[([^\]]+)\]', smiles):
        m = re.match(r'([A-Z][a-z]?|[cnospb])', bracket_content)
        if m:
            sym = m.group(1)
            bracket_atoms.append(aromatic_map.get(sym, sym))

    # Strip bracket content so we don't double-count
    stripped = re.sub(r'\[[^\]]+\]', '', smiles)

    # Match known two-letter elements, then single uppercase, then aromatic lowercase
    two_letter = r'Cl|Br|Si|Se|As|Na|Mg|Ca|Fe|Zn|Cu|Mn'
    pattern = fr'{two_letter}|[A-Z]|[cnospb]'

    outer_atoms: List[str] = []
    aromatic_count: Counter = Counter()
    for tok in re.findall(pattern, stripped):
        if tok in aromatic_map:
            normalized = aromatic_map[tok]
            outer_atoms.append(normalized)
            aromatic_count[normalized] += 1
        else:
            outer_atoms.append(tok)

    return outer_atoms + bracket_atoms, aromatic_count


def _count_brackets(smiles: str, bracket: str) -> int:
    """Count occurrences of a bracket character in SMILES."""
    return smiles.count(bracket)


def _molecular_formula(atom_counts: Counter) -> str:
    """Format atom counts into Hill notation (C first, H second, rest alpha)."""
    parts: List[str] = []
    for elem in ['C', 'H']:
        count = atom_counts.get(elem, 0)
        if count == 1:
            parts.append(elem)
        elif count > 1:
            parts.append(f'{elem}{count}')
    for elem in sorted(atom_counts):
        if elem in ('C', 'H'):
            continue
        count = atom_counts[elem]
        if count == 1:
            parts.append(elem)
        else:
            parts.append(f'{elem}{count}')
    return ''.join(parts)


def _estimate_hydrogens(smiles: str, atoms: List[str]) -> int:
    """Estimate implicit H count from SMILES using valence-bond balance.

    Accepts the aromatic_count Counter (from _parse_smiles_atoms) so that
    aromatic atoms use their delocalized effective valence (C→3, N→2).
    """
    # Default valences (non-aromatic)
    normal_valence: Dict[str, int] = {
        'C': 4, 'N': 3, 'O': 2, 'S': 2, 'P': 3, 'B': 3,
        'F': 1, 'Cl': 1, 'Br': 1, 'I': 1, 'H': 1,
    }
    # Effective valence for aromatic atoms (delocalized pi system)
    # Effective valence for aromatic atoms (N=3: covers both N-substituted and ring-NH positions)
    aromatic_valence: Dict[str, int] = {
        'C': 3, 'N': 3, 'O': 2, 'S': 2, 'P': 3,
    }

    aromatic_count: Counter
    atoms, aromatic_count = atoms  # unpack tuple from _parse_smiles_atoms

    heavy = [a for a in atoms if a != 'H']
    n = len(heavy)
    if n == 0:
        return explicit_h

    # Valence sum distinguishing aromatic from non-aromatic atoms
    heavy_counter: Counter = Counter(heavy)
    valence_sum = 0
    for elem, total in heavy_counter.items():
        ar = aromatic_count.get(elem, 0)
        non_ar = total - ar
        valence_sum += ar * aromatic_valence.get(elem, normal_valence.get(elem, 0))
        valence_sum += non_ar * normal_valence.get(elem, 0)

    # Bonds between heavy atoms (linear chain + rings + extra bond orders)
    ring_closures = _count_rings(smiles)
    extra_bond_orders = smiles.count('=') + smiles.count('#') * 2
    bonds_between_heavy = (n - 1) + ring_closures + extra_bond_orders

    implicit_h = max(0, valence_sum - 2 * bonds_between_heavy)
    # The valence-bond balance already gives TOTAL H (implicit + any explicit bracket H).
    # Do NOT add explicit_h again — doing so would double-count atoms like [C@@H].
    return implicit_h

def _count_rings(smiles: str) -> int:
    """Estimate ring count from SMILES ring-closure digits."""
    ring_nums = re.findall(r'(?<![\[%])([1-9])|%([0-9]{2})', smiles)
    digits: List[str] = [a or b for a, b in ring_nums]
    seen: set = set()
    rings = 0
    for d in digits:
        if d in seen:
            rings += 1
            seen.discard(d)
        else:
            seen.add(d)
    return rings


def _compute_properties(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Derive molecular properties from a SMILES string without external libs."""
    smiles: str = entry.get('smiles', '')
    if not smiles:
        return {}

    heavy_atoms, aromatic_count = _parse_smiles_atoms(smiles)
    atom_counts: Counter = Counter(heavy_atoms)

    # Estimate implicit hydrogens (pass tuple so _estimate_hydrogens can read aromatic info)
    h_count = _estimate_hydrogens(smiles, (heavy_atoms, aromatic_count))
    atom_counts['H'] = h_count

    formula = _molecular_formula(atom_counts)
    mol_weight = sum(
        _ATOMIC_WEIGHTS.get(elem, 12.0) * cnt for elem, cnt in atom_counts.items()
    )

    num_rings = _count_rings(smiles)

    # H-bond donors: OH and NH groups
    hbd = len(re.findall(r'(?:O|N)H', smiles)) + len(re.findall(r'\[(?:OH|NH)', smiles))
    # H-bond acceptors: N and O atoms (rough estimate)
    hba = atom_counts.get('N', 0) + atom_counts.get('O', 0)

    # LogP: sum atomic contributions
    logp = sum(
        _LOGP_CONTRIB.get(elem, 0.0) * cnt for elem, cnt in atom_counts.items()
    )

    # Rotatable bonds: single bonds not in ring, ex. C-C, C-N, C-O
    # Approximate via non-ring single bonds
    rotatable_bonds = len(re.findall(r'(?<![=#])(?:CC|CN|CO|NC|OC|NO|ON)', smiles))

    # Lipinski Ro5
    lipinski_pass = (
        mol_weight <= 500 and
        logp <= 5 and
        hbd <= 5 and
        hba <= 10
    )

    return {
        'formula': formula,
        'mol_weight': round(mol_weight, 4),
        'num_rings': num_rings,
        'hbd': hbd,
        'hba': hba,
        'logp': round(logp, 4),
        'rotatable_bonds': rotatable_bonds,
        'lipinski_pass': lipinski_pass,
    }


def _default_library() -> List[Dict[str, str]]:
    """Return a deterministic starter molecule library used on first run."""
    return [
        {'mol_id': 'mol_001', 'name': 'Aspirin',          'smiles': 'CC(=O)Oc1ccccc1C(=O)O'},
        {'mol_id': 'mol_002', 'name': 'Caffeine',         'smiles': 'Cn1cnc2c1c(=O)n(C)c(=O)n2C'},
        {'mol_id': 'mol_003', 'name': 'Ethanol',          'smiles': 'CCO'},
        {'mol_id': 'mol_004', 'name': 'Glucose',          'smiles': 'OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O'},
        {'mol_id': 'mol_005', 'name': 'Benzene',          'smiles': 'c1ccccc1'},
        {'mol_id': 'mol_006', 'name': 'Penicillin G',     'smiles': 'CC1(C)SC2C(NC(=O)Cc3ccccc3)C(=O)N2C1C(=O)O'},
        {'mol_id': 'mol_007', 'name': 'Ibuprofen',        'smiles': 'CC(C)Cc1ccc(cc1)C(C)C(=O)O'},
        {'mol_id': 'mol_008', 'name': 'Paracetamol',      'smiles': 'CC(=O)Nc1ccc(O)cc1'},
    ]


def _json_dumps_local(data: Any) -> str:
    import json
    return json.dumps(data, indent=2, sort_keys=False)


def load_visualizer_profile() -> Dict[str, Any]:
    """Return startup profile built from previously saved catalogs."""
    runs = load_run_catalog()
    molecules = load_molecule_catalog()
    library = load_library()
    recent_molecules = [
        f"{item.get('mol_id', '')}:{item.get('name', '')}:{item.get('mol_weight', 0.0):.1f}g/mol"
        for item in molecules[-8:]
    ]
    return {
        'catalog_file': 'data/runs.json',
        'molecule_catalog_file': 'data/molecules.json',
        'library_file': 'data/library.json',
        'runs_stored': len(runs),
        'molecule_records_stored': len(molecules),
        'library_available': len(library),
        'recent_molecules': recent_molecules,
    }


def run_core_flow() -> Dict[str, Any]:
    """Run one complete chemistry visualizer session."""
    ensure_data_dirs()
    config = create_visualizer_config()

    run_id = _run_id()
    started = time.perf_counter()

    library = load_library()
    if not library:
        library = _default_library()
        save_library(library)

    computed: List[Dict[str, Any]] = []
    metadata_files: List[str] = []

    for entry in library:
        props = _compute_properties(entry)
        if not props:
            continue
        record = create_molecule_record(
            mol_id=entry['mol_id'],
            name=entry['name'],
            smiles=entry['smiles'],
            formula=props['formula'],
            mol_weight=props['mol_weight'],
            num_rings=props['num_rings'],
            hbd=props['hbd'],
            hba=props['hba'],
            logp=props['logp'],
            rotatable_bonds=props['rotatable_bonds'],
            lipinski_pass=props['lipinski_pass'],
        )
        metadata_files.append(save_molecule_record(record, run_id))
        computed.append(record)

    computed.sort(key=lambda r: r['mol_weight'])

    # Write properties table artifact
    props_file = OUTPUTS_DIR / f'properties_{run_id}.json'
    props_file.write_text(
        _json_dumps_local({
            'run_id': run_id,
            'molecules': computed,
        }),
        encoding='utf-8',
    )

    # Write Lipinski summary artifact
    lip_pass = [r for r in computed if r['lipinski_pass']]
    lip_file = OUTPUTS_DIR / f'lipinski_{run_id}.json'
    lip_file.write_text(
        _json_dumps_local({
            'run_id': run_id,
            'lipinski_rule_of_five': {
                'mw_threshold': 500,
                'logp_threshold': 5,
                'hbd_threshold': 5,
                'hba_threshold': 10,
            },
            'pass_molecules': lip_pass,
        }),
        encoding='utf-8',
    )

    elapsed_ms = (time.perf_counter() - started) * 1000.0
    weights = [r['mol_weight'] for r in computed]
    logps = [r['logp'] for r in computed]

    import statistics
    metrics: Dict[str, Any] = {
        'mean_mol_weight': round(statistics.mean(weights), 4) if weights else 0.0,
        'min_mol_weight': round(min(weights), 4) if weights else 0.0,
        'max_mol_weight': round(max(weights), 4) if weights else 0.0,
        'mean_logp': round(statistics.mean(logps), 4) if logps else 0.0,
        'lipinski_pass_rate': round(len(lip_pass) / len(computed), 4) if computed else 0.0,
    }

    artifacts: Dict[str, Any] = {
        'run_file': str(OUTPUTS_DIR / f'run_{run_id}.json'),
        'properties_file': str(props_file),
        'lipinski_file': str(lip_file),
        'metadata_files': metadata_files,
    }

    previews = computed[: config['max_molecules_in_report']]

    summary = create_run_summary(
        run_id=run_id,
        molecules_processed=len(computed),
        properties_computed=len(computed) * config['top_properties'],
        lipinski_pass_count=len(lip_pass),
        elapsed_ms=elapsed_ms,
        artifacts=artifacts,
        molecule_previews=previews,
        metrics=metrics,
    )

    save_run_record(summary)
    return summary
