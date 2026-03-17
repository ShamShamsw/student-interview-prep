"""operations.py - Business logic for Project 40: Real-Time Collaborative Notebook Demo."""

from __future__ import annotations

from datetime import datetime
import json
import math
import random
import statistics
import time
from typing import Any, Dict, List, Tuple

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

from models import (
    create_cell_record,
    create_conflict_record,
    create_edit_event,
    create_notebook_config,
    create_session_summary,
)
from storage import (
    OUTPUTS_DIR,
    ensure_data_dirs,
    load_edit_catalog,
    load_notebook_library,
    load_session_catalog,
    save_edit_bundle,
    save_notebook_library,
    save_session_record,
)


def _session_id() -> str:
    """Build a compact session ID from UTC timestamp."""
    return datetime.utcnow().strftime('%Y%m%d_%H%M%S')


def _default_notebook_library() -> List[Dict[str, Any]]:
    """Return deterministic starter notebooks used on first run."""
    return [
        {
            'notebook_id': 'nb_001',
            'name': 'Data Analysis Pipeline',
            'description': 'A shared notebook for exploratory data analysis.',
            'cells': [
                {'cell_id': 'cell_1', 'cell_type': 'code', 'content': 'import pandas as pd\nimport numpy as np', 'version': 0, 'last_editor': '', 'last_edited_at_ms': 0.0},
                {'cell_id': 'cell_2', 'cell_type': 'code', 'content': 'df = pd.read_csv("data.csv")', 'version': 0, 'last_editor': '', 'last_edited_at_ms': 0.0},
                {'cell_id': 'cell_3', 'cell_type': 'markdown', 'content': '## Summary Statistics', 'version': 0, 'last_editor': '', 'last_edited_at_ms': 0.0},
                {'cell_id': 'cell_4', 'cell_type': 'code', 'content': 'df.describe()', 'version': 0, 'last_editor': '', 'last_edited_at_ms': 0.0},
                {'cell_id': 'cell_5', 'cell_type': 'code', 'content': 'df.plot(kind="hist")', 'version': 0, 'last_editor': '', 'last_edited_at_ms': 0.0},
            ],
        },
        {
            'notebook_id': 'nb_002',
            'name': 'Model Training Runbook',
            'description': 'Shared runbook for training and evaluating a classifier.',
            'cells': [
                {'cell_id': 'cell_1', 'cell_type': 'markdown', 'content': '# Model Training', 'version': 0, 'last_editor': '', 'last_edited_at_ms': 0.0},
                {'cell_id': 'cell_2', 'cell_type': 'code', 'content': 'from sklearn.ensemble import RandomForestClassifier', 'version': 0, 'last_editor': '', 'last_edited_at_ms': 0.0},
                {'cell_id': 'cell_3', 'cell_type': 'code', 'content': 'model = RandomForestClassifier(n_estimators=100)', 'version': 0, 'last_editor': '', 'last_edited_at_ms': 0.0},
                {'cell_id': 'cell_4', 'cell_type': 'code', 'content': 'model.fit(X_train, y_train)', 'version': 0, 'last_editor': '', 'last_edited_at_ms': 0.0},
                {'cell_id': 'cell_5', 'cell_type': 'code', 'content': 'print(model.score(X_test, y_test))', 'version': 0, 'last_editor': '', 'last_edited_at_ms': 0.0},
            ],
        },
    ]


_OPERATION_TEMPLATES: Dict[str, List[str]] = {
    'replace': [
        'n_estimators=200',
        'df.dropna(inplace=True)',
        'df.fillna(0)',
        'model.fit(X_train, y_train, sample_weight=weights)',
        '## Revised Summary',
        'df.plot(kind="box")',
        'model = RandomForestClassifier(max_depth=5)',
        'print(model.score(X_test, y_test), "accuracy")',
    ],
    'insert': [
        '# inserted by user',
        'print("debug checkpoint")',
        '# TODO: review this cell',
        'assert df is not None',
    ],
    'delete': [''],
}


def _generate_edits_for_notebook(
    notebook: Dict[str, Any],
    config: Dict[str, Any],
    rng: random.Random,
    edit_counter: List[int],
) -> List[Dict[str, Any]]:
    """Simulate all user edits for one notebook."""
    users = config['users']
    ops_per_user = config['ops_per_user']
    cells = notebook['cells']
    notebook_id = notebook['notebook_id']
    time_window_ms = 2000.0

    edits: List[Dict[str, Any]] = []
    operations = ['replace', 'replace', 'replace', 'insert', 'delete']

    for user in users:
        for _ in range(ops_per_user):
            cell = rng.choice(cells)
            operation = rng.choice(operations)
            templates = _OPERATION_TEMPLATES[operation]
            new_content = rng.choice(templates)
            timestamp_ms = rng.uniform(0.0, time_window_ms)
            edit_counter[0] += 1
            edit_id = f'edit_{edit_counter[0]:03d}'
            edits.append(
                create_edit_event(
                    edit_id=edit_id,
                    user_id=user,
                    notebook_id=notebook_id,
                    cell_id=cell['cell_id'],
                    operation=operation,
                    old_content=cell['content'],
                    new_content=new_content,
                    timestamp_ms=timestamp_ms,
                    is_conflict=False,
                    conflict_resolution='',
                    status='pending',
                )
            )

    edits.sort(key=lambda edit: edit['timestamp_ms'])
    return edits


def _detect_and_resolve_conflicts(
    edits: List[Dict[str, Any]],
    conflict_window_ms: float,
    notebook_id: str,
    conflict_counter: List[int],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Detect concurrent edits to the same cell and apply last-writer-wins resolution."""
    from collections import defaultdict

    cell_edits: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for edit in edits:
        if edit['notebook_id'] == notebook_id:
            cell_edits[edit['cell_id']].append(edit)

    conflicts: List[Dict[str, Any]] = []
    conflict_ids: set = set()

    for cell_id, cell_edit_list in cell_edits.items():
        sorted_cell_edits = sorted(cell_edit_list, key=lambda edit: edit['timestamp_ms'])
        for idx in range(len(sorted_cell_edits) - 1):
            edit_a = sorted_cell_edits[idx]
            edit_b = sorted_cell_edits[idx + 1]
            time_diff = edit_b['timestamp_ms'] - edit_a['timestamp_ms']
            if time_diff <= conflict_window_ms and edit_a['user_id'] != edit_b['user_id']:
                conflict_counter[0] += 1
                conflict_id = f'conflict_{conflict_counter[0]:03d}'
                winner = edit_b if edit_b['timestamp_ms'] >= edit_a['timestamp_ms'] else edit_a
                loser = edit_a if winner is edit_b else edit_b
                conflicts.append(
                    create_conflict_record(
                        conflict_id=conflict_id,
                        notebook_id=notebook_id,
                        cell_id=cell_id,
                        edit_a_id=edit_a['edit_id'],
                        edit_b_id=edit_b['edit_id'],
                        resolution='last_writer_wins',
                        winner_edit_id=winner['edit_id'],
                        detected_at_ms=edit_b['timestamp_ms'],
                    )
                )
                conflict_ids.add(loser['edit_id'])
                winner['is_conflict'] = True
                winner['conflict_resolution'] = 'last_writer_wins:winner'
                loser['is_conflict'] = True
                loser['conflict_resolution'] = 'last_writer_wins:discarded'

    for edit in edits:
        if edit['edit_id'] in conflict_ids:
            edit['status'] = 'discarded'
        elif edit['status'] == 'pending':
            edit['status'] = 'applied'

    return edits, conflicts


def _apply_edits_to_notebook(
    notebook: Dict[str, Any],
    edits: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Apply resolved edits in timestamp order to produce the final notebook state."""
    cell_map = {cell['cell_id']: dict(cell) for cell in notebook['cells']}

    for edit in sorted(edits, key=lambda e: e['timestamp_ms']):
        if edit['status'] != 'applied':
            continue
        cell_id = edit['cell_id']
        if cell_id not in cell_map:
            continue
        cell = cell_map[cell_id]
        cell['old_content'] = cell['content']
        cell['content'] = edit['new_content']
        cell['version'] = cell.get('version', 0) + 1
        cell['last_editor'] = edit['user_id']
        cell['last_edited_at_ms'] = edit['timestamp_ms']

    return {**notebook, 'cells': list(cell_map.values())}


def _save_timeline_plot(
    all_edits: List[Dict[str, Any]],
    session_id: str,
    users: List[str],
) -> str:
    """Persist a scatter plot of edit events over simulated time."""
    user_colors = ['#1d3557', '#e63946', '#2a9d8f', '#f4a261', '#a8dadc']
    color_map = {user: user_colors[idx % len(user_colors)] for idx, user in enumerate(users)}

    figure, axis = plt.subplots(figsize=(10, 5))

    cell_ids = sorted({edit['cell_id'] for edit in all_edits})
    cell_y = {cell_id: idx for idx, cell_id in enumerate(cell_ids)}

    for user in users:
        user_edits = [edit for edit in all_edits if edit['user_id'] == user]
        xs = [edit['timestamp_ms'] for edit in user_edits]
        ys = [cell_y[edit['cell_id']] for edit in user_edits]
        axis.scatter(xs, ys, label=user, color=color_map[user], s=60, alpha=0.85, zorder=3)

    conflict_edits = [edit for edit in all_edits if edit['is_conflict']]
    if conflict_edits:
        cx = [edit['timestamp_ms'] for edit in conflict_edits]
        cy = [cell_y[edit['cell_id']] for edit in conflict_edits]
        axis.scatter(cx, cy, marker='x', color='#ff006e', s=90, linewidths=2.0, zorder=4, label='conflict')

    axis.set_yticks(list(cell_y.values()))
    axis.set_yticklabels(list(cell_y.keys()), fontsize=8)
    axis.set_xlabel('Simulated time (ms)')
    axis.set_ylabel('Cell ID')
    axis.set_title('Collaborative Edit Timeline')
    axis.legend(loc='upper right', fontsize=8)
    axis.grid(alpha=0.25)
    figure.tight_layout()

    file_path = OUTPUTS_DIR / f'timeline_{session_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def _save_conflict_chart(
    all_conflicts: List[Dict[str, Any]],
    session_id: str,
) -> str:
    """Persist a bar chart showing conflict count per cell."""
    from collections import Counter

    counts = Counter(conflict['cell_id'] for conflict in all_conflicts)
    cell_ids = sorted(counts.keys())
    heights = [counts[cell_id] for cell_id in cell_ids]

    figure, axis = plt.subplots(figsize=(8, 4))
    bar_colors = ['#e63946' if height > 1 else '#f4a261' for height in heights]
    bars = axis.bar(cell_ids, heights, color=bar_colors, edgecolor='white', linewidth=0.8)
    for bar, height in zip(bars, heights):
        if height > 0:
            axis.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.05,
                str(height),
                ha='center',
                va='bottom',
                fontsize=9,
            )
    axis.set_xlabel('Cell ID')
    axis.set_ylabel('Conflicts detected')
    axis.set_title('Conflict Frequency by Cell')
    axis.grid(axis='y', alpha=0.3)
    figure.tight_layout()

    file_path = OUTPUTS_DIR / f'conflicts_{session_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def load_collab_profile() -> Dict[str, Any]:
    """Return startup profile built from previously saved catalogs."""
    sessions = load_session_catalog()
    edit_catalog = load_edit_catalog()
    library = load_notebook_library()
    recent_edits = [
        f"{item.get('edit_id', '')}:{item.get('user_id', '')}:{item.get('cell_id', '')}"
        for item in edit_catalog[-6:]
    ]
    return {
        'catalog_file': 'data/sessions.json',
        'edit_catalog_file': 'data/edits.json',
        'library_file': 'data/notebooks.json',
        'sessions_stored': len(sessions),
        'edit_records_stored': len(edit_catalog),
        'notebooks_available': len(library),
        'recent_edits': recent_edits,
    }


def run_core_flow() -> Dict[str, Any]:
    """Run one complete collaborative notebook simulation session."""
    ensure_data_dirs()
    config = create_notebook_config()
    session_id = _session_id()
    rng = random.Random(config['random_seed'])
    started = time.perf_counter()

    library = load_notebook_library()
    if not library:
        library = _default_notebook_library()
        save_notebook_library(library)

    all_edits: List[Dict[str, Any]] = []
    all_conflicts: List[Dict[str, Any]] = []
    edit_counter = [0]
    conflict_counter = [0]

    for notebook in library:
        notebook_edits = _generate_edits_for_notebook(notebook, config, rng, edit_counter)
        resolved_edits, notebook_conflicts = _detect_and_resolve_conflicts(
            notebook_edits,
            float(config['conflict_window_ms']),
            notebook['notebook_id'],
            conflict_counter,
        )
        _apply_edits_to_notebook(notebook, resolved_edits)
        all_edits.extend(resolved_edits)
        all_conflicts.extend(notebook_conflicts)

    timeline_file = ''
    conflict_chart_file = ''
    if config['include_timeline_plot']:
        timeline_file = _save_timeline_plot(all_edits, session_id, config['users'])
    if config['include_conflict_chart']:
        conflict_chart_file = _save_conflict_chart(all_conflicts, session_id)

    bundle_file = save_edit_bundle(all_edits, session_id)

    elapsed_ms = (time.perf_counter() - started) * 1000.0
    applied_edits = [edit for edit in all_edits if edit['status'] == 'applied']
    conflicts_total = len(all_conflicts)
    unique_users = sorted({edit['user_id'] for edit in all_edits})
    cell_edit_counts = {}
    for edit in all_edits:
        cell_edit_counts[edit['cell_id']] = cell_edit_counts.get(edit['cell_id'], 0) + 1
    conflict_cell_counts: Dict[str, int] = {}
    for conflict in all_conflicts:
        conflict_cell_counts[conflict['cell_id']] = conflict_cell_counts.get(conflict['cell_id'], 0) + 1

    metrics: Dict[str, Any] = {
        'conflict_rate': round(conflicts_total / len(all_edits), 4) if all_edits else 0.0,
        'mean_edits_per_cell': round(statistics.mean(cell_edit_counts.values()), 3) if cell_edit_counts else 0.0,
        'max_conflicts_in_cell': max(conflict_cell_counts.values()) if conflict_cell_counts else 0,
        'resolution_strategy': 'last_writer_wins',
        'applied_edits': len(applied_edits),
        'discarded_edits': len(all_edits) - len(applied_edits),
        'unique_users': unique_users,
    }

    edit_previews = [
        {
            'edit_id': edit['edit_id'],
            'user_id': edit['user_id'],
            'notebook_id': edit['notebook_id'],
            'cell_id': edit['cell_id'],
            'operation': edit['operation'],
            'is_conflict': edit['is_conflict'],
            'status': edit['status'],
        }
        for edit in all_edits[: config['max_edits_in_report']]
    ]

    artifacts = {
        'bundle_file': bundle_file,
        'timeline_file': timeline_file,
        'conflict_chart_file': conflict_chart_file,
        'edit_count': len(all_edits),
    }

    summary = create_session_summary(
        session_id=session_id,
        notebooks_processed=len(library),
        edits_total=len(all_edits),
        conflicts_total=conflicts_total,
        conflicts_resolved=conflicts_total,
        elapsed_ms=elapsed_ms,
        artifacts=artifacts,
        edit_previews=edit_previews,
        metrics=metrics,
    )

    session_file = save_session_record(summary)
    summary['artifacts']['session_file'] = session_file
    return summary
