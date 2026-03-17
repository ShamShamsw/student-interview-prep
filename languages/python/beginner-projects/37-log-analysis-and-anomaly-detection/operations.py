"""
operations.py - Business logic for Project 37: Log Analysis And Anomaly Detection
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import re
import statistics
import time
from typing import Any, Dict, List, Tuple

from models import create_anomaly_record, create_log_analyzer_config, create_run_summary
from storage import (
    OUTPUTS_DIR,
    ensure_data_dirs,
    load_anomaly_catalog,
    load_log_library,
    load_run_catalog,
    save_anomaly_record,
    save_log_library,
    save_run_record,
)

LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+) (?P<ident>\S+) (?P<user>\S+) '
    r'\[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>[^ ]+) (?P<protocol>[^"]+)" '
    r'(?P<status>\d{3}) (?P<bytes>\S+) '
    r'"(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"$'
)
SUSPICIOUS_PATH_TOKENS = ('.env', 'wp-login', '/admin', '/etc/passwd', 'phpmyadmin')
AUTOMATED_CLIENT_TOKENS = ('curl', 'python-requests', 'wget', 'bot')


def _run_id() -> str:
    """Build a compact run ID from UTC timestamp."""
    return datetime.utcnow().strftime('%Y%m%d_%H%M%S')


def _default_library() -> List[Dict[str, Any]]:
    """Return deterministic starter log library used on first run."""
    return [
        {
            'source_id': 'log_001',
            'service': 'edge-proxy',
            'environment': 'prod',
            'raw_line': '198.51.100.10 - alice [17/Mar/2026:08:00:01 +0000] "GET / HTTP/1.1" 200 4210 "https://example.com/start" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"',
        },
        {
            'source_id': 'log_002',
            'service': 'edge-proxy',
            'environment': 'prod',
            'raw_line': '198.51.100.11 - bob [17/Mar/2026:08:00:08 +0000] "GET /products HTTP/1.1" 200 5820 "https://example.com/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"',
        },
        {
            'source_id': 'log_003',
            'service': 'edge-proxy',
            'environment': 'prod',
            'raw_line': '198.51.100.12 - carol [17/Mar/2026:08:01:17 +0000] "POST /api/cart HTTP/1.1" 201 920 "https://example.com/products" "Mozilla/5.0 (X11; Linux x86_64)"',
        },
        {
            'source_id': 'log_004',
            'service': 'auth-gateway',
            'environment': 'prod',
            'raw_line': '203.0.113.77 - - [17/Mar/2026:08:02:10 +0000] "POST /wp-login.php HTTP/1.1" 401 713 "-" "curl/8.5.0"',
        },
        {
            'source_id': 'log_005',
            'service': 'auth-gateway',
            'environment': 'prod',
            'raw_line': '203.0.113.77 - - [17/Mar/2026:08:02:18 +0000] "POST /wp-login.php HTTP/1.1" 403 713 "-" "curl/8.5.0"',
        },
        {
            'source_id': 'log_006',
            'service': 'auth-gateway',
            'environment': 'prod',
            'raw_line': '203.0.113.77 - - [17/Mar/2026:08:02:25 +0000] "POST /wp-login.php HTTP/1.1" 403 713 "-" "curl/8.5.0"',
        },
        {
            'source_id': 'log_007',
            'service': 'edge-proxy',
            'environment': 'prod',
            'raw_line': '198.51.100.42 - - [17/Mar/2026:08:03:09 +0000] "GET /.env HTTP/1.1" 404 289 "-" "python-requests/2.32.0"',
        },
        {
            'source_id': 'log_008',
            'service': 'api-gateway',
            'environment': 'prod',
            'raw_line': '192.0.2.55 - svc_export [17/Mar/2026:08:04:01 +0000] "POST /api/export HTTP/1.1" 500 0 "https://example.com/dashboard" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"',
        },
        {
            'source_id': 'log_009',
            'service': 'api-gateway',
            'environment': 'prod',
            'raw_line': '192.0.2.55 - svc_export [17/Mar/2026:08:04:11 +0000] "POST /api/export HTTP/1.1" 500 0 "https://example.com/dashboard" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"',
        },
        {
            'source_id': 'log_010',
            'service': 'api-gateway',
            'environment': 'prod',
            'raw_line': '192.0.2.55 - svc_export [17/Mar/2026:08:04:25 +0000] "POST /api/export HTTP/1.1" 502 0 "https://example.com/dashboard" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"',
        },
        {
            'source_id': 'log_011',
            'service': 'api-gateway',
            'environment': 'prod',
            'raw_line': '192.0.2.55 - svc_export [17/Mar/2026:08:04:39 +0000] "POST /api/export HTTP/1.1" 500 0 "https://example.com/dashboard" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"',
        },
        {
            'source_id': 'log_012',
            'service': 'admin-portal',
            'environment': 'prod',
            'raw_line': '10.24.8.9 - ops-admin [17/Mar/2026:02:15:42 +0000] "GET /admin/reports HTTP/1.1" 200 189342 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"',
        },
        {
            'source_id': 'log_013',
            'service': 'edge-proxy',
            'environment': 'prod',
            'raw_line': '198.51.100.14 - dan [17/Mar/2026:08:05:04 +0000] "GET /pricing HTTP/1.1" 200 4980 "https://example.com/" "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)"',
        },
        {
            'source_id': 'log_014',
            'service': 'edge-proxy',
            'environment': 'prod',
            'raw_line': '198.51.100.15 - erin [17/Mar/2026:08:05:12 +0000] "GET /docs HTTP/1.1" 200 6120 "https://example.com/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64)"',
        },
        {
            'source_id': 'log_015',
            'service': 'edge-proxy',
            'environment': 'prod',
            'raw_line': '198.51.100.16 - frank [17/Mar/2026:08:06:03 +0000] "GET /health HTTP/1.1" 200 96 "-" "kube-probe/1.29"',
        },
        {
            'source_id': 'log_016',
            'service': 'edge-proxy',
            'environment': 'prod',
            'raw_line': '198.51.100.17 - grace [17/Mar/2026:08:06:31 +0000] "GET /assets/logo.png HTTP/1.1" 304 0 "https://example.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"',
        },
        {
            'source_id': 'log_017',
            'service': 'api-gateway',
            'environment': 'prod',
            'raw_line': '198.51.100.18 - svc_batch [17/Mar/2026:08:07:02 +0000] "PUT /api/orders/183 HTTP/1.1" 200 834 "https://example.com/orders" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"',
        },
        {
            'source_id': 'log_018',
            'service': 'edge-proxy',
            'environment': 'prod',
            'raw_line': 'bad malformed line without common log format fields',
        },
    ]


def _parse_timestamp(value: str) -> datetime:
    """Parse common-log timestamp into a timezone-aware datetime."""
    return datetime.strptime(value, '%d/%b/%Y:%H:%M:%S %z')


def _parse_log_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Parse one raw log line into a structured record."""
    raw_line = str(entry.get('raw_line', ''))
    match = LOG_PATTERN.match(raw_line)
    if not match:
        return {
            'parsed_ok': False,
            'source_id': entry.get('source_id', 'unknown'),
            'service': entry.get('service', 'unknown'),
            'environment': entry.get('environment', 'unknown'),
            'raw_line': raw_line,
            'parse_error': 'line_did_not_match_common_log_format',
        }

    payload = match.groupdict()
    parsed_at = _parse_timestamp(payload['timestamp'])
    bytes_sent = 0 if payload['bytes'] == '-' else int(payload['bytes'])
    path = payload['path']
    method = payload['method']
    status_code = int(payload['status'])
    user_agent = payload['user_agent']
    lower_path = path.lower()
    lower_ua = user_agent.lower()

    return {
        'parsed_ok': True,
        'source_id': entry.get('source_id', 'unknown'),
        'service': entry.get('service', 'unknown'),
        'environment': entry.get('environment', 'unknown'),
        'ip_address': payload['ip'],
        'remote_user': payload['user'],
        'timestamp': parsed_at.isoformat(),
        'timestamp_sort': parsed_at,
        'method': method,
        'path': path,
        'protocol': payload['protocol'],
        'status_code': status_code,
        'bytes_sent': bytes_sent,
        'referrer': payload['referrer'],
        'user_agent': user_agent,
        'minute_bucket': parsed_at.strftime('%Y-%m-%dT%H:%M'),
        'hour_bucket': parsed_at.strftime('%Y-%m-%dT%H:00'),
        'is_offhours': parsed_at.hour < 6 or parsed_at.hour >= 23,
        'is_suspicious_path': any(token in lower_path for token in SUSPICIOUS_PATH_TOKENS),
        'is_automated_client': any(token in lower_ua for token in AUTOMATED_CLIENT_TOKENS),
        'raw_line': raw_line,
    }


def _score_event(
    event: Dict[str, Any],
    ip_minute_counts: Counter[Tuple[str, str]],
    ip_error_counts: Counter[str],
    ip_auth_fail_counts: Counter[str],
    path_counts: Counter[str],
) -> Tuple[float, str, List[str]]:
    """Score one parsed event and return score, anomaly type, and evidence."""
    contributions: List[Tuple[str, float, str]] = []

    def add(kind: str, points: float, evidence: str) -> None:
        contributions.append((kind, points, evidence))

    ip_address = event['ip_address']
    minute_bucket = event['minute_bucket']
    status_code = event['status_code']
    path = event['path']

    if status_code >= 500:
        add('server_error_spike', 3.0, f'5xx response observed ({status_code})')
        if ip_error_counts[ip_address] >= 3:
            add('server_error_spike', 1.5, f'repeated error activity from {ip_address}')

    if status_code in {401, 403} and ip_auth_fail_counts[ip_address] >= 2:
        add('repeated_auth_failures', 2.5, 'multiple authentication failures from same IP')

    if event['is_suspicious_path']:
        add('suspicious_path_probe', 2.5, f'suspicious path requested ({path})')

    if '/admin' in path.lower() and event['is_offhours']:
        add('off_hours_admin_access', 2.5, 'admin route accessed during off-hours window')

    if ip_minute_counts[(ip_address, minute_bucket)] >= 4:
        add('burst_request_pattern', 2.5, f'burst traffic from {ip_address} within one minute')

    if event['bytes_sent'] >= 100_000:
        add('large_payload_transfer', 1.5, f"large response payload ({event['bytes_sent']} bytes)")

    if path_counts[path] == 1 and status_code >= 400:
        add('rare_error_path', 1.0, 'rare failing endpoint appears only once in sample')

    if event['is_automated_client']:
        add('automated_client_activity', 1.0, 'request issued by automated client user-agent')

    total_score = sum(points for _, points, _ in contributions)
    if not contributions:
        return 0.0, 'normal_activity', []
    primary_type = max(contributions, key=lambda item: item[1])[0]
    evidence = [item[2] for item in contributions]
    return total_score, primary_type, evidence


def _build_timeline_report(
    events: List[Dict[str, Any]],
    anomalies: List[Dict[str, Any]],
) -> str:
    """Create a text timeline view for output export."""
    hour_counts = Counter(event['hour_bucket'] for event in events)
    hour_anomalies = Counter(anomaly.get('timestamp', '')[:13] + ':00' for anomaly in anomalies if anomaly.get('timestamp'))
    status_counts = Counter(str(event['status_code']) for event in events)

    lines = [
        'LOG ANALYSIS TIMELINE',
        '=====================',
        '',
        'Hourly activity:',
    ]
    for hour in sorted(hour_counts):
        lines.append(
            f"- {hour}: requests={hour_counts[hour]} anomalies={hour_anomalies.get(hour, 0)}"
        )

    lines.extend(
        [
            '',
            'Status distribution:',
        ]
    )
    for status_code, count in sorted(status_counts.items()):
        lines.append(f'- {status_code}: {count}')

    lines.extend(
        [
            '',
            'Top anomalies:',
        ]
    )
    if not anomalies:
        lines.append('- None detected')
    else:
        for anomaly in anomalies[:8]:
            evidence = '; '.join(anomaly.get('evidence', [])[:2])
            lines.append(
                f"- {anomaly['anomaly_id']} | {anomaly.get('timestamp', '')} | "
                f"{anomaly.get('ip_address', 'unknown')} | {anomaly.get('anomaly_type', '')} | "
                f"score={anomaly.get('score', 0.0):.1f} | {evidence}"
            )
    return '\n'.join(lines)


def load_analyzer_profile() -> Dict[str, Any]:
    """Return startup profile built from previously saved catalogs."""
    runs = load_run_catalog()
    anomalies = load_anomaly_catalog()
    library = load_log_library()
    recent_anomalies = [
        f"{item.get('anomaly_id', '')}:{item.get('anomaly_type', '')}:{item.get('score', 0.0):.1f}"
        for item in anomalies[-8:]
    ]
    return {
        'catalog_file': 'data/runs.json',
        'anomaly_catalog_file': 'data/anomalies.json',
        'library_file': 'data/library.json',
        'runs_stored': len(runs),
        'anomaly_records_stored': len(anomalies),
        'library_available': len(library),
        'recent_anomalies': recent_anomalies,
    }


def run_core_flow() -> Dict[str, Any]:
    """Run one complete log analysis and anomaly detection session."""
    ensure_data_dirs()
    config = create_log_analyzer_config()

    run_id = _run_id()
    started = time.perf_counter()

    library = load_log_library()
    if not library:
        library = _default_library()
        save_log_library(library)

    parsed_events: List[Dict[str, Any]] = []
    malformed_events: List[Dict[str, Any]] = []
    for entry in library:
        parsed = _parse_log_entry(entry)
        if parsed.get('parsed_ok'):
            parsed_events.append(parsed)
        else:
            malformed_events.append(parsed)

    parsed_events.sort(key=lambda item: item['timestamp_sort'])

    ip_counts = Counter(event['ip_address'] for event in parsed_events)
    path_counts = Counter(event['path'] for event in parsed_events)
    minute_counts = Counter(event['minute_bucket'] for event in parsed_events)
    ip_minute_counts = Counter((event['ip_address'], event['minute_bucket']) for event in parsed_events)
    ip_error_counts = Counter(event['ip_address'] for event in parsed_events if event['status_code'] >= 400)
    ip_auth_fail_counts = Counter(event['ip_address'] for event in parsed_events if event['status_code'] in {401, 403})

    anomaly_records: List[Dict[str, Any]] = []
    metadata_files: List[str] = []
    anomaly_index = 1

    for malformed in malformed_events:
        anomaly_id = f'anm_{anomaly_index:03d}'
        anomaly_index += 1
        record = create_anomaly_record(
            anomaly_id=anomaly_id,
            source_id=malformed.get('source_id', 'unknown'),
            timestamp='',
            ip_address='unknown',
            method='UNKNOWN',
            path='unparsed',
            status_code=0,
            anomaly_type='malformed_log_entry',
            score=9.0,
            evidence=['log line did not match expected common-log pattern'],
            bytes_sent=0,
            minute_bucket='',
            user_agent='',
        )
        anomaly_records.append(record)
        metadata_files.append(save_anomaly_record(record, run_id))

    for event in parsed_events:
        score, anomaly_type, evidence = _score_event(
            event,
            ip_minute_counts=ip_minute_counts,
            ip_error_counts=ip_error_counts,
            ip_auth_fail_counts=ip_auth_fail_counts,
            path_counts=path_counts,
        )
        if score < config['score_threshold']:
            continue

        anomaly_id = f'anm_{anomaly_index:03d}'
        anomaly_index += 1
        record = create_anomaly_record(
            anomaly_id=anomaly_id,
            source_id=event['source_id'],
            timestamp=event['timestamp'],
            ip_address=event['ip_address'],
            method=event['method'],
            path=event['path'],
            status_code=event['status_code'],
            anomaly_type=anomaly_type,
            score=score,
            evidence=evidence,
            bytes_sent=event['bytes_sent'],
            minute_bucket=event['minute_bucket'],
            user_agent=event['user_agent'],
        )
        anomaly_records.append(record)
        metadata_files.append(save_anomaly_record(record, run_id))

    anomaly_records.sort(key=lambda item: (-item['score'], item.get('timestamp', ''), item['anomaly_id']))

    parsed_file = OUTPUTS_DIR / f'parsed_{run_id}.json'
    parsed_file.write_text(
        json.dumps(
            [
                {key: value for key, value in event.items() if key != 'timestamp_sort'}
                for event in parsed_events
            ],
            indent=2,
        ),
        encoding='utf-8',
    )

    anomalies_file = OUTPUTS_DIR / f'anomalies_{run_id}.json'
    anomalies_file.write_text(json.dumps(anomaly_records, indent=2), encoding='utf-8')

    timeline_file = OUTPUTS_DIR / f'timeline_{run_id}.txt'
    timeline_file.write_text(_build_timeline_report(parsed_events, anomaly_records), encoding='utf-8')

    elapsed_ms = (time.perf_counter() - started) * 1000.0
    total_events = len(parsed_events)
    error_events = [event for event in parsed_events if event['status_code'] >= 400]
    server_errors = [event for event in parsed_events if event['status_code'] >= 500]
    offhours_events = [event for event in parsed_events if event['is_offhours']]
    suspicious_events = [event for event in parsed_events if event['is_suspicious_path']]
    mean_requests_per_ip = (
        statistics.mean(ip_counts.values()) if ip_counts else 0.0
    )

    metrics: Dict[str, Any] = {
        'error_rate': round(len(error_events) / total_events, 4) if total_events else 0.0,
        'server_error_rate': round(len(server_errors) / total_events, 4) if total_events else 0.0,
        'offhours_share': round(len(offhours_events) / total_events, 4) if total_events else 0.0,
        'suspicious_path_share': round(len(suspicious_events) / total_events, 4) if total_events else 0.0,
        'mean_requests_per_ip': round(mean_requests_per_ip, 4),
        'peak_minute_volume': max(minute_counts.values()) if minute_counts else 0,
        'malformed_lines': len(malformed_events),
        'max_anomaly_score': round(max((item['score'] for item in anomaly_records), default=0.0), 4),
    }

    artifacts: Dict[str, Any] = {
        'run_file': str(OUTPUTS_DIR / f'run_{run_id}.json'),
        'parsed_file': str(parsed_file),
        'anomalies_file': str(anomalies_file),
        'timeline_file': str(timeline_file),
        'metadata_files': metadata_files,
    }

    summary = create_run_summary(
        run_id=run_id,
        log_lines_processed=len(library),
        parsed_events=len(parsed_events),
        anomalies_detected=len(anomaly_records),
        unique_ips=len(ip_counts),
        elapsed_ms=elapsed_ms,
        artifacts=artifacts,
        anomaly_previews=anomaly_records[: config['max_anomalies_in_report']],
        metrics=metrics,
    )

    save_run_record(summary)
    return summary
