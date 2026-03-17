"""Data models for Project 44: Cryptography Toolkit And Visualizations."""

from datetime import datetime
from typing import Any, Dict, List


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string."""
    return datetime.utcnow().isoformat(timespec='seconds') + 'Z'


def create_toolkit_config(
    classic_algorithms: List[str] | None = None,
    benchmark_algorithms: List[str] | None = None,
    demo_message_label: str = 'lesson_affine_safe',
    benchmark_message_lengths: List[int] | None = None,
    benchmark_trials: int = 3,
    rsa_demo_bits: int = 16,
    rsa_attack_bits: List[int] | None = None,
    include_frequency_plot: bool = True,
    include_runtime_chart: bool = True,
    include_attack_chart: bool = True,
    max_preview_rows: int = 6,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """Create a validated configuration record for one toolkit session."""
    resolved_classic = classic_algorithms if classic_algorithms else ['caesar', 'vigenere']
    resolved_benchmark = benchmark_algorithms if benchmark_algorithms else ['caesar', 'vigenere', 'rsa']
    resolved_lengths = benchmark_message_lengths if benchmark_message_lengths else [24, 64, 128, 256]
    resolved_attack_bits = rsa_attack_bits if rsa_attack_bits else [12, 14, 16, 18]
    return {
        'project_type': 'cryptography_toolkit_and_visualizations',
        'classic_algorithms': list(resolved_classic),
        'benchmark_algorithms': list(resolved_benchmark),
        'demo_message_label': str(demo_message_label),
        'benchmark_message_lengths': [max(8, int(length)) for length in resolved_lengths],
        'benchmark_trials': max(1, int(benchmark_trials)),
        'rsa_demo_bits': max(10, int(rsa_demo_bits)),
        'rsa_attack_bits': [max(10, int(bits)) for bits in resolved_attack_bits],
        'include_frequency_plot': bool(include_frequency_plot),
        'include_runtime_chart': bool(include_runtime_chart),
        'include_attack_chart': bool(include_attack_chart),
        'max_preview_rows': max(1, int(max_preview_rows)),
        'random_seed': int(random_seed),
        'created_at': _utc_timestamp(),
    }


def create_message_record(
    message_id: str,
    label: str,
    plaintext: str,
    caesar_shift: int,
    vigenere_key: str,
    description: str,
    tags: List[str],
) -> Dict[str, Any]:
    """Create one reusable lesson-message record."""
    return {
        'message_id': str(message_id),
        'label': str(label),
        'plaintext': str(plaintext),
        'caesar_shift': max(0, int(caesar_shift)) % 26,
        'vigenere_key': str(vigenere_key).upper(),
        'description': str(description),
        'tags': [str(tag) for tag in tags],
    }


def create_cipher_demo(
    algorithm: str,
    key_material: str,
    ciphertext: str,
    recovered_plaintext: str,
    elapsed_ms: float,
) -> Dict[str, Any]:
    """Create one encryption/decryption demo result record."""
    return {
        'algorithm': str(algorithm),
        'key_material': str(key_material),
        'ciphertext': str(ciphertext),
        'recovered_plaintext': str(recovered_plaintext),
        'elapsed_ms': round(float(elapsed_ms), 5),
        'roundtrip_ok': ciphertext != recovered_plaintext and bool(recovered_plaintext),
    }


def create_attack_record(
    attack_name: str,
    target: str,
    success: bool,
    elapsed_ms: float,
    details: Dict[str, Any],
) -> Dict[str, Any]:
    """Create one cryptographic attack demonstration record."""
    return {
        'attack_name': str(attack_name),
        'target': str(target),
        'success': bool(success),
        'elapsed_ms': round(float(elapsed_ms), 5),
        'details': dict(details),
    }


def create_runtime_point(
    algorithm: str,
    message_length: int,
    trial: int,
    elapsed_ms: float,
) -> Dict[str, Any]:
    """Create one runtime benchmark point for a cipher algorithm."""
    return {
        'algorithm': str(algorithm),
        'message_length': int(message_length),
        'trial': int(trial),
        'elapsed_ms': round(float(elapsed_ms), 6),
    }


def create_attack_point(
    key_bits: int,
    modulus_n: int,
    trial_divisions: int,
    elapsed_ms: float,
    success: bool,
) -> Dict[str, Any]:
    """Create one RSA weakness benchmark point."""
    return {
        'key_bits': int(key_bits),
        'modulus_n': int(modulus_n),
        'trial_divisions': int(trial_divisions),
        'elapsed_ms': round(float(elapsed_ms), 6),
        'success': bool(success),
    }


def create_session_summary(
    session_id: str,
    messages_available: int,
    demo_message_label: str,
    demo_message_length: int,
    runtime_points: int,
    attacks_run: int,
    elapsed_ms: float,
    artifacts: Dict[str, Any],
    demo_previews: List[Dict[str, Any]],
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """Create final session summary for reporting and persistence."""
    return {
        'session_id': str(session_id),
        'messages_available': int(messages_available),
        'demo_message_label': str(demo_message_label),
        'demo_message_length': int(demo_message_length),
        'runtime_points': int(runtime_points),
        'attacks_run': int(attacks_run),
        'elapsed_ms': round(float(elapsed_ms), 5),
        'artifacts': dict(artifacts),
        'demo_previews': list(demo_previews),
        'metrics': dict(metrics),
        'finished_at': _utc_timestamp(),
    }


def create_record(**kwargs):
    """Backwards-compatible generic record factory."""
    return dict(kwargs)
