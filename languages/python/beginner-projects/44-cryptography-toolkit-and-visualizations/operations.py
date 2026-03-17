"""Business logic for Project 44: Cryptography Toolkit And Visualizations."""

from __future__ import annotations

import math
import random
import time
from collections import Counter, defaultdict
from datetime import datetime
from statistics import mean
from typing import Any, Dict, List, Tuple

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

from models import (
    create_attack_point,
    create_attack_record,
    create_cipher_demo,
    create_message_record,
    create_runtime_point,
    create_session_summary,
    create_toolkit_config,
)
from storage import (
    OUTPUTS_DIR,
    ensure_data_dirs,
    load_message_library,
    load_run_catalog,
    save_benchmark_file,
    save_message_library,
    save_run_record,
    save_trace_file,
)


ALGORITHM_LABELS = {
    'caesar': 'Caesar',
    'vigenere': 'Vigenere',
    'rsa': 'RSA',
}

ALGORITHM_COLORS = {
    'caesar': '#264653',
    'vigenere': '#2a9d8f',
    'rsa': '#e76f51',
}

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
COMMON_WORDS = {
    'THE',
    'AND',
    'TO',
    'OF',
    'THAT',
    'FOR',
    'IS',
    'IN',
    'YOU',
    'SECURE',
    'SORT',
    'DATA',
}


def _session_id() -> str:
    """Build a compact session ID from UTC timestamp."""
    return datetime.utcnow().strftime('%Y%m%d_%H%M%S')


def _default_message_library() -> List[Dict[str, Any]]:
    """Return deterministic starter plaintext examples used on first run."""
    return [
        create_message_record(
            message_id='msg_001',
            label='lesson_affine_safe',
            plaintext='SECURE SYSTEMS RELY ON GOOD KEYS AND CAREFUL IMPLEMENTATION',
            caesar_shift=7,
            vigenere_key='VECTOR',
            description='Balanced educational sentence with repeated letters for frequency plots.',
            tags=['demo', 'balanced', 'frequency'],
        ),
        create_message_record(
            message_id='msg_002',
            label='lesson_short_alert',
            plaintext='MEET AT LAB TWO AT NINE',
            caesar_shift=3,
            vigenere_key='ALPHA',
            description='Short operational message for compact examples.',
            tags=['demo', 'short'],
        ),
        create_message_record(
            message_id='msg_003',
            label='lesson_long_form',
            plaintext='CRYPTOGRAPHY PROTECTS CONFIDENTIALITY INTEGRITY AND AUTHENTICITY WHEN USED CORRECTLY',
            caesar_shift=11,
            vigenere_key='MATRIX',
            description='Longer sentence for runtime scaling and key-length effects.',
            tags=['demo', 'long', 'benchmark'],
        ),
        create_message_record(
            message_id='msg_004',
            label='lesson_attack_phrase',
            plaintext='WEAK MODULUS SIZES ALLOW PRACTICAL FACTORIZATION ATTACKS',
            caesar_shift=5,
            vigenere_key='CIPHER',
            description='Phrase tuned to accompany RSA attack demonstration.',
            tags=['demo', 'attack'],
        ),
    ]


def _normalize_text(value: str) -> str:
    """Upper-case text while preserving spaces and punctuation."""
    return value.upper()


def _caesar_encrypt(plaintext: str, shift: int) -> str:
    """Encrypt text with Caesar substitution."""
    output: List[str] = []
    for character in _normalize_text(plaintext):
        if character in ALPHABET:
            index = (ALPHABET.index(character) + shift) % 26
            output.append(ALPHABET[index])
        else:
            output.append(character)
    return ''.join(output)


def _caesar_decrypt(ciphertext: str, shift: int) -> str:
    """Decrypt Caesar ciphertext by reversing the shift."""
    return _caesar_encrypt(ciphertext, -shift)


def _vigenere_encrypt(plaintext: str, key: str) -> str:
    """Encrypt text with Vigenere substitution."""
    key_stream = [character for character in _normalize_text(key) if character in ALPHABET]
    if not key_stream:
        raise ValueError('Vigenere key must contain alphabetic characters.')

    output: List[str] = []
    key_index = 0
    for character in _normalize_text(plaintext):
        if character in ALPHABET:
            shift = ALPHABET.index(key_stream[key_index % len(key_stream)])
            index = (ALPHABET.index(character) + shift) % 26
            output.append(ALPHABET[index])
            key_index += 1
        else:
            output.append(character)
    return ''.join(output)


def _vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt Vigenere ciphertext with the same key."""
    key_stream = [character for character in _normalize_text(key) if character in ALPHABET]
    if not key_stream:
        raise ValueError('Vigenere key must contain alphabetic characters.')

    output: List[str] = []
    key_index = 0
    for character in _normalize_text(ciphertext):
        if character in ALPHABET:
            shift = ALPHABET.index(key_stream[key_index % len(key_stream)])
            index = (ALPHABET.index(character) - shift) % 26
            output.append(ALPHABET[index])
            key_index += 1
        else:
            output.append(character)
    return ''.join(output)


def _english_score(candidate: str) -> float:
    """Heuristic score used for Caesar brute-force ranking."""
    words = [word for word in candidate.split() if word]
    common_hits = sum(1 for word in words if word in COMMON_WORDS)
    vowels = sum(1 for char in candidate if char in 'AEIOU')
    letters = max(1, sum(1 for char in candidate if char in ALPHABET))
    vowel_ratio = vowels / letters
    vowel_bias = 1.0 - abs(vowel_ratio - 0.38)
    return common_hits * 2.0 + vowel_bias


def _caesar_attack(ciphertext: str) -> Tuple[int, str, List[Dict[str, Any]]]:
    """Brute-force all Caesar shifts and rank likely plaintext candidates."""
    candidates: List[Dict[str, Any]] = []
    for shift in range(26):
        decrypted = _caesar_decrypt(ciphertext, shift)
        score = _english_score(decrypted)
        candidates.append({'shift': shift, 'plaintext': decrypted, 'score': score})
    ranked = sorted(candidates, key=lambda item: item['score'], reverse=True)
    best = ranked[0]
    return int(best['shift']), str(best['plaintext']), ranked[:5]


def _count_letters(text: str) -> Dict[str, int]:
    """Count A-Z frequencies in text."""
    counts = Counter(character for character in text if character in ALPHABET)
    return {letter: int(counts.get(letter, 0)) for letter in ALPHABET}


def _is_prime(value: int) -> bool:
    """Return True if value is prime using trial division."""
    if value < 2:
        return False
    if value in (2, 3):
        return True
    if value % 2 == 0:
        return False
    limit = int(math.isqrt(value))
    for factor in range(3, limit + 1, 2):
        if value % factor == 0:
            return False
    return True


def _generate_prime(bits: int, rng: random.Random) -> int:
    """Generate a deterministic random prime near the requested bit size."""
    lower = 1 << (bits - 1)
    upper = (1 << bits) - 1
    candidate = rng.randrange(lower | 1, upper, 2)
    while not _is_prime(candidate):
        candidate += 2
        if candidate > upper:
            candidate = lower | 1
    return candidate


def _extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Return gcd and Bezout coefficients."""
    if b == 0:
        return (a, 1, 0)
    gcd, x1, y1 = _extended_gcd(b, a % b)
    return (gcd, y1, x1 - (a // b) * y1)


def _mod_inverse(value: int, modulus: int) -> int:
    """Return multiplicative inverse of value mod modulus."""
    gcd, x, _ = _extended_gcd(value, modulus)
    if gcd != 1:
        raise ValueError('No modular inverse exists for the provided values.')
    return x % modulus


def _generate_rsa_keypair(bits: int, rng: random.Random) -> Dict[str, int]:
    """Generate a weak educational RSA keypair."""
    prime_bits = max(5, bits // 2)
    p = _generate_prime(prime_bits, rng)
    q = _generate_prime(prime_bits, rng)
    while q == p:
        q = _generate_prime(prime_bits, rng)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    if math.gcd(e, phi) != 1:
        e = 3
        while e < phi and math.gcd(e, phi) != 1:
            e += 2

    d = _mod_inverse(e, phi)
    return {
        'p': p,
        'q': q,
        'n': n,
        'phi': phi,
        'e': e,
        'd': d,
        'bits': bits,
    }


def _rsa_encrypt(plaintext: str, e: int, n: int) -> List[int]:
    """Encrypt text into integer blocks using textbook RSA."""
    return [pow(ord(character), e, n) for character in plaintext]


def _rsa_decrypt(cipher_blocks: List[int], d: int, n: int) -> str:
    """Decrypt RSA integer blocks back to text."""
    return ''.join(chr(pow(block, d, n)) for block in cipher_blocks)


def _factor_modulus_trial(n: int) -> Tuple[int, int, int]:
    """Factor n by trial division and return p, q, and attempts."""
    attempts = 0
    if n % 2 == 0:
        return (2, n // 2, 1)
    limit = int(math.isqrt(n))
    for factor in range(3, limit + 1, 2):
        attempts += 1
        if n % factor == 0:
            return (factor, n // factor, attempts)
    return (1, n, attempts)


def _run_classic_demo(message: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Run Caesar and Vigenere demonstrations for one plaintext."""
    plaintext = _normalize_text(str(message['plaintext']))
    shift = int(message['caesar_shift'])
    key = str(message['vigenere_key'])

    classic_demos: List[Dict[str, Any]] = []

    started = time.perf_counter()
    caesar_cipher = _caesar_encrypt(plaintext, shift)
    caesar_plain = _caesar_decrypt(caesar_cipher, shift)
    caesar_ms = (time.perf_counter() - started) * 1000.0
    classic_demos.append(create_cipher_demo('caesar', f'shift={shift}', caesar_cipher, caesar_plain, caesar_ms))

    started = time.perf_counter()
    vigenere_cipher = _vigenere_encrypt(plaintext, key)
    vigenere_plain = _vigenere_decrypt(vigenere_cipher, key)
    vigenere_ms = (time.perf_counter() - started) * 1000.0
    classic_demos.append(create_cipher_demo('vigenere', f'key={key}', vigenere_cipher, vigenere_plain, vigenere_ms))

    attack_started = time.perf_counter()
    inferred_shift, inferred_plaintext, top_candidates = _caesar_attack(caesar_cipher)
    attack_elapsed_ms = (time.perf_counter() - attack_started) * 1000.0

    attack_record = create_attack_record(
        attack_name='caesar_bruteforce',
        target='Caesar',
        success=(inferred_plaintext == plaintext),
        elapsed_ms=attack_elapsed_ms,
        details={
            'expected_shift': shift,
            'inferred_shift': inferred_shift,
            'expected_plaintext': plaintext,
            'inferred_plaintext': inferred_plaintext,
            'top_candidates': top_candidates,
        },
    )

    return classic_demos, {
        'plaintext': plaintext,
        'caesar_ciphertext': caesar_cipher,
        'vigenere_ciphertext': vigenere_cipher,
        'caesar_attack': attack_record,
    }


def _run_rsa_demo(message: Dict[str, Any], config: Dict[str, Any], rng: random.Random) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Run textbook RSA demo plus a modulus-factorization attack."""
    plaintext = _normalize_text(str(message['plaintext']))
    keypair = _generate_rsa_keypair(config['rsa_demo_bits'], rng)

    started = time.perf_counter()
    cipher_blocks = _rsa_encrypt(plaintext, keypair['e'], keypair['n'])
    recovered_plaintext = _rsa_decrypt(cipher_blocks, keypair['d'], keypair['n'])
    rsa_elapsed_ms = (time.perf_counter() - started) * 1000.0

    rsa_demo = create_cipher_demo(
        algorithm='rsa',
        key_material=f"n={keypair['n']} e={keypair['e']}",
        ciphertext=' '.join(str(value) for value in cipher_blocks[:8]) + (' ...' if len(cipher_blocks) > 8 else ''),
        recovered_plaintext=recovered_plaintext,
        elapsed_ms=rsa_elapsed_ms,
    )

    attack_started = time.perf_counter()
    p, q, trial_divisions = _factor_modulus_trial(keypair['n'])
    phi = (p - 1) * (q - 1) if p > 1 else 0
    reconstructed_d = _mod_inverse(keypair['e'], phi) if phi else 0
    attack_plaintext = _rsa_decrypt(cipher_blocks, reconstructed_d, keypair['n']) if reconstructed_d else ''
    attack_elapsed_ms = (time.perf_counter() - attack_started) * 1000.0

    attack_record = create_attack_record(
        attack_name='rsa_trial_division_factorization',
        target='RSA',
        success=(attack_plaintext == plaintext and p * q == keypair['n']),
        elapsed_ms=attack_elapsed_ms,
        details={
            'n': keypair['n'],
            'e': keypair['e'],
            'p': p,
            'q': q,
            'trial_divisions': trial_divisions,
            'recovered_plaintext': attack_plaintext,
        },
    )

    return rsa_demo, {
        'keypair': {k: keypair[k] for k in ('n', 'e', 'd', 'bits')},
        'cipher_blocks': cipher_blocks,
        'attack': attack_record,
    }


def _random_message(length: int, rng: random.Random) -> str:
    """Generate deterministic benchmark plaintext with letters and spaces."""
    letters = ALPHABET + '     '
    return ''.join(rng.choice(letters) for _ in range(length)).strip() or 'DATA'


def _benchmark_runtimes(config: Dict[str, Any], rng: random.Random, rsa_keypair: Dict[str, int]) -> List[Dict[str, Any]]:
    """Benchmark cipher runtime as message length increases."""
    points: List[Dict[str, Any]] = []
    for length in config['benchmark_message_lengths']:
        for trial in range(1, config['benchmark_trials'] + 1):
            message = _random_message(length, rng)

            if 'caesar' in config['benchmark_algorithms']:
                started = time.perf_counter()
                cipher = _caesar_encrypt(message, 11)
                _caesar_decrypt(cipher, 11)
                elapsed = (time.perf_counter() - started) * 1000.0
                points.append(create_runtime_point('caesar', length, trial, elapsed))

            if 'vigenere' in config['benchmark_algorithms']:
                started = time.perf_counter()
                cipher = _vigenere_encrypt(message, 'VECTOR')
                _vigenere_decrypt(cipher, 'VECTOR')
                elapsed = (time.perf_counter() - started) * 1000.0
                points.append(create_runtime_point('vigenere', length, trial, elapsed))

            if 'rsa' in config['benchmark_algorithms']:
                started = time.perf_counter()
                blocks = _rsa_encrypt(message, rsa_keypair['e'], rsa_keypair['n'])
                _rsa_decrypt(blocks, rsa_keypair['d'], rsa_keypair['n'])
                elapsed = (time.perf_counter() - started) * 1000.0
                points.append(create_runtime_point('rsa', length, trial, elapsed))
    return points


def _benchmark_rsa_attack(bits_list: List[int], rng: random.Random) -> List[Dict[str, Any]]:
    """Benchmark trial-division factoring time over weak RSA sizes."""
    points: List[Dict[str, Any]] = []
    for bits in bits_list:
        keypair = _generate_rsa_keypair(bits, rng)
        started = time.perf_counter()
        p, q, trial_divisions = _factor_modulus_trial(keypair['n'])
        elapsed = (time.perf_counter() - started) * 1000.0
        points.append(
            create_attack_point(
                key_bits=bits,
                modulus_n=keypair['n'],
                trial_divisions=trial_divisions,
                elapsed_ms=elapsed,
                success=(p * q == keypair['n']),
            )
        )
    return points


def _aggregate_runtime(points: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, float]]]:
    """Average runtime benchmark points by algorithm and message length."""
    grouped: Dict[str, Dict[int, List[Dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for point in points:
        grouped[point['algorithm']][point['message_length']].append(point)

    summary: Dict[str, List[Dict[str, float]]] = {}
    for algorithm, lengths in grouped.items():
        summary[algorithm] = []
        for length in sorted(lengths):
            bucket = lengths[length]
            summary[algorithm].append(
                {
                    'message_length': length,
                    'elapsed_ms': round(mean(point['elapsed_ms'] for point in bucket), 6),
                }
            )
    return summary


def _save_frequency_plot(plaintext: str, ciphertext: str, session_id: str) -> str:
    """Persist side-by-side letter frequency chart for Caesar demo."""
    plain_counts = _count_letters(plaintext)
    cipher_counts = _count_letters(ciphertext)
    x_positions = list(range(len(ALPHABET)))

    figure, axis = plt.subplots(figsize=(10.5, 4.8))
    axis.bar([position - 0.2 for position in x_positions], [plain_counts[letter] for letter in ALPHABET], width=0.4, color='#264653', label='Plaintext')
    axis.bar([position + 0.2 for position in x_positions], [cipher_counts[letter] for letter in ALPHABET], width=0.4, color='#e76f51', label='Caesar ciphertext')
    axis.set_title('Letter Frequency Shift: Plaintext vs Caesar Ciphertext')
    axis.set_xlabel('Letter')
    axis.set_ylabel('Count')
    axis.set_xticks(x_positions)
    axis.set_xticklabels(list(ALPHABET), fontsize=8)
    axis.grid(axis='y', alpha=0.25)
    axis.legend()
    figure.tight_layout()
    file_path = OUTPUTS_DIR / f'frequency_{session_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def _save_runtime_chart(runtime_summary: Dict[str, List[Dict[str, float]]], session_id: str) -> str:
    """Persist average runtime chart across message lengths."""
    figure, axis = plt.subplots(figsize=(8.5, 4.8))
    for algorithm, rows in runtime_summary.items():
        axis.plot(
            [row['message_length'] for row in rows],
            [row['elapsed_ms'] for row in rows],
            marker='o',
            linewidth=2,
            color=ALGORITHM_COLORS.get(algorithm, '#6c757d'),
            label=ALGORITHM_LABELS.get(algorithm, algorithm),
        )
    axis.set_title('Average Cipher Runtime by Message Length')
    axis.set_xlabel('Message length (characters)')
    axis.set_ylabel('Elapsed time (ms)')
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()
    file_path = OUTPUTS_DIR / f'runtime_{session_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def _save_attack_chart(attack_points: List[Dict[str, Any]], session_id: str) -> str:
    """Persist RSA trial-division attack cost across weak key sizes."""
    figure, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    bits = [point['key_bits'] for point in attack_points]
    timings = [point['elapsed_ms'] for point in attack_points]
    trial_divisions = [point['trial_divisions'] for point in attack_points]

    axes[0].plot(bits, timings, marker='o', linewidth=2, color='#e76f51')
    axes[0].set_title('Factorization Time vs RSA Bit Size')
    axes[0].set_xlabel('Weak RSA bit size')
    axes[0].set_ylabel('Elapsed time (ms)')
    axes[0].grid(alpha=0.25)

    axes[1].bar(bits, trial_divisions, color='#2a9d8f', width=1.2)
    axes[1].set_title('Trial Divisions Needed to Factor n')
    axes[1].set_xlabel('Weak RSA bit size')
    axes[1].set_ylabel('Trial divisions')
    axes[1].grid(axis='y', alpha=0.25)

    figure.tight_layout()
    file_path = OUTPUTS_DIR / f'attack_cost_{session_id}.png'
    figure.savefig(file_path, dpi=150)
    plt.close(figure)
    return str(file_path)


def load_toolkit_profile() -> Dict[str, Any]:
    """Return startup profile built from previously saved catalogs."""
    ensure_data_dirs()
    run_catalog = load_run_catalog()
    library = load_message_library()
    recent_runs = [
        f"{item.get('session_id', '')}:{item.get('fastest_cipher', '')}:{item.get('demo_message_label', '')}"
        for item in run_catalog[-5:]
    ]
    return {
        'catalog_file': 'data/runs.json',
        'library_file': 'data/message_sets.json',
        'runs_stored': len(run_catalog),
        'messages_available': len(library),
        'recent_runs': recent_runs,
    }


def run_core_flow() -> Dict[str, Any]:
    """Run one complete cryptography demo, attack lab, and benchmark session."""
    ensure_data_dirs()
    config = create_toolkit_config()
    session_id = _session_id()
    rng = random.Random(config['random_seed'])
    started = time.perf_counter()

    message_library = load_message_library()
    if not message_library:
        message_library = _default_message_library()
        save_message_library(message_library)

    message = next(
        (record for record in message_library if record['label'] == config['demo_message_label']),
        message_library[0],
    )

    classic_demos, classic_payload = _run_classic_demo(message)
    rsa_demo, rsa_payload = _run_rsa_demo(message, config, rng)

    demo_previews = list(classic_demos)
    demo_previews.append(rsa_demo)

    runtime_points = _benchmark_runtimes(config, rng, {
        'e': rsa_payload['keypair']['e'],
        'd': rsa_payload['keypair']['d'],
        'n': rsa_payload['keypair']['n'],
    })
    attack_points = _benchmark_rsa_attack(config['rsa_attack_bits'], rng)
    runtime_summary = _aggregate_runtime(runtime_points)

    attacks = [classic_payload['caesar_attack'], rsa_payload['attack']]

    trace_payload = {
        'session_id': session_id,
        'config': config,
        'message': message,
        'demos': demo_previews,
        'attacks': attacks,
        'rsa_payload': rsa_payload,
    }
    benchmark_payload = {
        'session_id': session_id,
        'runtime_points': runtime_points,
        'runtime_summary': runtime_summary,
        'attack_points': attack_points,
    }

    frequency_plot_file = ''
    runtime_chart_file = ''
    attack_chart_file = ''
    if config['include_frequency_plot']:
        frequency_plot_file = _save_frequency_plot(classic_payload['plaintext'], classic_payload['caesar_ciphertext'], session_id)
    if config['include_runtime_chart']:
        runtime_chart_file = _save_runtime_chart(runtime_summary, session_id)
    if config['include_attack_chart']:
        attack_chart_file = _save_attack_chart(attack_points, session_id)

    trace_file = save_trace_file(trace_payload, session_id)
    benchmark_file = save_benchmark_file(benchmark_payload, session_id)

    elapsed_ms = (time.perf_counter() - started) * 1000.0

    average_by_algorithm = {
        algorithm: mean(row['elapsed_ms'] for row in rows)
        for algorithm, rows in runtime_summary.items()
        if rows
    }
    fastest_cipher = min(average_by_algorithm.items(), key=lambda item: item[1])[0] if average_by_algorithm else ''

    metrics = {
        'fastest_cipher': fastest_cipher,
        'fastest_avg_runtime_ms': round(average_by_algorithm.get(fastest_cipher, 0.0), 6),
        'rsa_factorization_ms': rsa_payload['attack']['elapsed_ms'],
        'largest_message_length': max(config['benchmark_message_lengths']) if config['benchmark_message_lengths'] else 0,
        'caesar_attack_recovered_shift': classic_payload['caesar_attack']['details'].get('inferred_shift', -1),
        'rsa_attack_trial_divisions': rsa_payload['attack']['details'].get('trial_divisions', 0),
    }

    artifacts = {
        'trace_file': trace_file,
        'benchmark_file': benchmark_file,
        'frequency_plot_file': frequency_plot_file,
        'runtime_chart_file': runtime_chart_file,
        'attack_chart_file': attack_chart_file,
    }

    summary = create_session_summary(
        session_id=session_id,
        messages_available=len(message_library),
        demo_message_label=message['label'],
        demo_message_length=len(str(message['plaintext'])),
        runtime_points=len(runtime_points),
        attacks_run=len(attacks),
        elapsed_ms=elapsed_ms,
        artifacts=artifacts,
        demo_previews=demo_previews[: config['max_preview_rows']],
        metrics=metrics,
    )
    summary['attacks'] = attacks

    run_record = dict(summary)
    session_file = save_run_record(run_record)
    summary['artifacts']['session_file'] = session_file
    return summary
