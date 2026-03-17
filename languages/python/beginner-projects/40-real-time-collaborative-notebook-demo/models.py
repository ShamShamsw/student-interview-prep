"""models.py - Data models for Project 40: Real-Time Collaborative Notebook Demo."""

from datetime import datetime
from typing import Any, Dict, List


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string."""
    return datetime.utcnow().isoformat(timespec='seconds') + 'Z'


def create_notebook_config(
    users: List[str] | None = None,
    ops_per_user: int = 4,
    conflict_window_ms: int = 250,
    include_timeline_plot: bool = True,
    include_conflict_chart: bool = True,
    max_edits_in_report: int = 8,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """Create a validated configuration record for the collaborative session."""
    resolved_users = users if users else ['alice', 'bob', 'carol']
    return {
        'project_type': 'real_time_collaborative_notebook',
        'users': list(resolved_users),
        'ops_per_user': max(1, int(ops_per_user)),
        'conflict_window_ms': max(50, int(conflict_window_ms)),
        'include_timeline_plot': bool(include_timeline_plot),
        'include_conflict_chart': bool(include_conflict_chart),
        'max_edits_in_report': max(2, int(max_edits_in_report)),
        'random_seed': int(random_seed),
        'created_at': _utc_timestamp(),
    }


def create_cell_record(
    cell_id: str,
    cell_type: str,
    content: str,
    version: int,
    last_editor: str,
    last_edited_at_ms: float,
) -> Dict[str, Any]:
    """Create one notebook cell record."""
    return {
        'cell_id': cell_id,
        'cell_type': cell_type,
        'content': str(content),
        'version': int(version),
        'last_editor': str(last_editor),
        'last_edited_at_ms': float(last_edited_at_ms),
    }


def create_edit_event(
    edit_id: str,
    user_id: str,
    notebook_id: str,
    cell_id: str,
    operation: str,
    old_content: str,
    new_content: str,
    timestamp_ms: float,
    is_conflict: bool = False,
    conflict_resolution: str = '',
    status: str = 'pending',
) -> Dict[str, Any]:
    """Create one collaborative edit event record."""
    return {
        'edit_id': str(edit_id),
        'user_id': str(user_id),
        'notebook_id': str(notebook_id),
        'cell_id': str(cell_id),
        'operation': str(operation),
        'old_content': str(old_content),
        'new_content': str(new_content),
        'timestamp_ms': round(float(timestamp_ms), 3),
        'is_conflict': bool(is_conflict),
        'conflict_resolution': str(conflict_resolution),
        'status': str(status),
    }


def create_conflict_record(
    conflict_id: str,
    notebook_id: str,
    cell_id: str,
    edit_a_id: str,
    edit_b_id: str,
    resolution: str,
    winner_edit_id: str,
    detected_at_ms: float,
) -> Dict[str, Any]:
    """Create one detected conflict record."""
    return {
        'conflict_id': str(conflict_id),
        'notebook_id': str(notebook_id),
        'cell_id': str(cell_id),
        'edit_a_id': str(edit_a_id),
        'edit_b_id': str(edit_b_id),
        'resolution': str(resolution),
        'winner_edit_id': str(winner_edit_id),
        'detected_at_ms': round(float(detected_at_ms), 3),
    }


def create_session_summary(
    session_id: str,
    notebooks_processed: int,
    edits_total: int,
    conflicts_total: int,
    conflicts_resolved: int,
    elapsed_ms: float,
    artifacts: Dict[str, Any],
    edit_previews: List[Dict[str, Any]],
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """Create final session summary for reporting and persistence."""
    return {
        'session_id': str(session_id),
        'notebooks_processed': int(notebooks_processed),
        'edits_total': int(edits_total),
        'conflicts_total': int(conflicts_total),
        'conflicts_resolved': int(conflicts_resolved),
        'elapsed_ms': float(elapsed_ms),
        'artifacts': dict(artifacts),
        'edit_previews': list(edit_previews),
        'metrics': dict(metrics),
        'finished_at': _utc_timestamp(),
    }


def create_record(**kwargs):
    """Backwards-compatible generic record factory."""
    return dict(kwargs)
