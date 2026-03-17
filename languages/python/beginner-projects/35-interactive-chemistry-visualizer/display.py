"""
display.py - Presentation helpers for Project 35: Interactive Chemistry Visualizer
"""

from typing import Any, Dict, List


def format_header() -> str:
    """Format session header banner."""
    return '=' * 70 + '\n' + '   INTERACTIVE CHEMISTRY VISUALIZER\n' + '=' * 70


def format_startup_guide(config: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """Format startup configuration and historical profile."""
    recent = ', '.join(profile.get('recent_molecules', [])) or 'None yet'
    lines = [
        '',
        'Configuration:',
        f"   Project type:         {config['project_type']}",
        '   Property engine:      SMILES-based (no external chem libs)',
        f"   Top properties:       {config['top_properties']}",
        f"   Include formula:      {config['include_formula']}",
        f"   Include weight:       {config['include_weight']}",
        f"   Include rings:        {config['include_rings']}",
        f"   Include H-bond:       {config['include_hbond']}",
        f"   Max molecules report: {config['max_molecules_in_report']}",
        f"   Random seed:          {config['random_seed']}",
        '',
        'Startup:',
        '   Data directory:       data/',
        '   Outputs directory:    data/outputs/',
        f"   Molecule library:     {profile['library_file']} (loaded {profile['library_available']} molecules)",
        f"   Run catalog:          {profile['catalog_file']} (loaded {profile['runs_stored']} runs)",
        f"   Molecule catalog:     {profile['molecule_catalog_file']} (loaded {profile['molecule_records_stored']} records)",
        f'   Recent molecules:     {recent}',
        '',
        '---',
    ]
    return '\n'.join(lines)


def format_molecule_table(previews: List[Dict[str, Any]]) -> str:
    """Format molecule property table."""
    if not previews:
        return 'No molecule data available.'
    lines = [
        'Molecule properties:',
        '   ID      | Name              | Formula       | MW (g/mol) | Rings | logP  | Ro5',
        '   --------+-------------------+---------------+------------+-------+-------+----',
    ]
    for mol in previews:
        ro5 = 'PASS' if mol.get('lipinski_pass') else 'FAIL'
        lines.append(
            '   '
            f"{mol['mol_id'][:7]:<7} | "
            f"{mol['name'][:17]:<17} | "
            f"{mol.get('formula', '')[:13]:<13} | "
            f"{mol.get('mol_weight', 0.0):>10.2f} | "
            f"{mol.get('num_rings', 0):>5} | "
            f"{mol.get('logp', 0.0):>5.2f} | "
            f"{ro5}"
        )
    return '\n'.join(lines)


def format_run_report(summary: Dict[str, Any]) -> str:
    """Format final run report."""
    artifacts = summary.get('artifacts', {})
    metrics = summary.get('metrics', {})
    metadata_files = artifacts.get('metadata_files', [])
    lines = [
        '',
        'Run complete:',
        f"   Run ID:               {summary['run_id']}",
        f"   Molecules processed:  {summary['molecules_processed']}",
        f"   Properties computed:  {summary['properties_computed']}",
        f"   Lipinski pass:        {summary['lipinski_pass_count']}/{summary['molecules_processed']}",
        f"   Elapsed time:         {summary['elapsed_ms']:.2f} ms",
        '',
        f"Library metrics: mean_MW={metrics.get('mean_mol_weight', 0.0):.2f} | "
        f"min_MW={metrics.get('min_mol_weight', 0.0):.2f} | "
        f"max_MW={metrics.get('max_mol_weight', 0.0):.2f} | "
        f"mean_logP={metrics.get('mean_logp', 0.0):.2f} | "
        f"Ro5_rate={metrics.get('lipinski_pass_rate', 0.0):.0%}",
        '',
        format_molecule_table(summary.get('molecule_previews', [])),
        '',
        'Artifacts saved:',
        f"   Run record:           {artifacts.get('run_file', 'N/A')}",
        f"   Properties report:    {artifacts.get('properties_file', 'N/A')}",
        f"   Lipinski report:      {artifacts.get('lipinski_file', 'N/A')}",
        f"   Metadata exports:     {len(metadata_files)}",
    ]
    return '\n'.join(lines)


def format_message(message: str) -> str:
    """Format a user-facing message string."""
    return f'[Project 35] {message}'
