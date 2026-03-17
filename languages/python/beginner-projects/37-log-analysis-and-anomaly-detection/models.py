"""
models.py - Data models for Project 37: Log Analysis And Anomaly Detection
"""

from datetime import datetime
from typing import Any, Dict, List


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string."""
    return datetime.utcnow().isoformat(timespec='seconds') + 'Z'


def create_log_analyzer_config(
    top_patterns: int = 6,
    score_threshold: float = 3.0,
    include_timeline: bool = True,
    include_ip_summary: bool = True,
    include_path_summary: bool = True,
    max_anomalies_in_report: int = 10,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """Create a validated log analyzer configuration record."""
    return {
        'project_type': 'log_analysis_and_anomaly_detection',
        'top_patterns': max(1, int(top_patterns)),
        'score_threshold': float(score_threshold),
        'include_timeline': bool(include_timeline),
        'include_ip_summary': bool(include_ip_summary),
        'include_path_summary': bool(include_path_summary),
        'max_anomalies_in_report': max(3, int(max_anomalies_in_report)),
        'random_seed': int(random_seed),
        'created_at': _utc_timestamp(),
    }


def create_anomaly_record(
    anomaly_id: str,
    source_id: str,
    timestamp: str,
    ip_address: str,
    method: str,
    path: str,
    status_code: int,
    anomaly_type: str,
    score: float,
    evidence: List[str],
    bytes_sent: int,
    minute_bucket: str,
    user_agent: str,
) -> Dict[str, Any]:
    """Create one computed anomaly record."""
    return {
        'anomaly_id': anomaly_id,
        'source_id': source_id,
        'timestamp': timestamp,
        'ip_address': ip_address,
        'method': method,
        'path': path,
        'status_code': int(status_code),
        'anomaly_type': anomaly_type,
        'score': round(float(score), 4),
        'evidence': list(evidence),
        'bytes_sent': int(bytes_sent),
        'minute_bucket': minute_bucket,
        'user_agent': user_agent,
        'created_at': _utc_timestamp(),
    }


def create_run_summary(
    run_id: str,
    log_lines_processed: int,
    parsed_events: int,
    anomalies_detected: int,
    unique_ips: int,
    elapsed_ms: float,
    artifacts: Dict[str, Any],
    anomaly_previews: List[Dict[str, Any]],
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """Create final run summary for reporting and persistence."""
    return {
        'run_id': run_id,
        'log_lines_processed': int(log_lines_processed),
        'parsed_events': int(parsed_events),
        'anomalies_detected': int(anomalies_detected),
        'unique_ips': int(unique_ips),
        'elapsed_ms': float(elapsed_ms),
        'artifacts': artifacts,
        'anomaly_previews': anomaly_previews,
        'metrics': metrics,
        'finished_at': _utc_timestamp(),
    }


def create_record(**kwargs):
    """Backwards-compatible generic record factory."""
    return dict(kwargs)
