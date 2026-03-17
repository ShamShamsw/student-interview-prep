# Beginner Project 44: Cryptography Toolkit And Visualizations

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Caesar and Vigenere cipher walkthroughs, textbook RSA encryption/decryption, weak-key attack demos, and empirical visualization of crypto behavior

---

## Why This Project?

Cryptography feels abstract until you can see messages transform, keys drive behavior, and weak assumptions fail under attack. This project builds a compact educational lab where students can explore classical substitution ciphers and modern public-key encryption with the same reproducible workflow.

This project teaches end-to-end cryptography visualization concepts where you can:

- load or auto-seed a reusable lesson-message library for deterministic demos,
- run Caesar and Vigenere encryption/decryption with round-trip validation,
- generate weak educational RSA keypairs and perform textbook RSA encryption/decryption,
- brute-force Caesar ciphertext and rank likely plaintext candidates,
- factor weak RSA moduli with trial division to recover private keys,
- compare plaintext and ciphertext letter distributions in a frequency plot,
- benchmark cipher runtime as message length grows,
- benchmark weak-key factorization cost across increasing RSA bit sizes,
- export trace bundles and benchmark bundles to JSON for inspection,
- persist historical run summaries for repeatable auditing,
- and print a readable terminal report with demo previews and artifact paths.

---

## Separate Repository

You can also access this project in a separate repository:

[cryptography toolkit and visualizations Repository](https://github.com/ShamShamsw/cryptography-toolkit-and-visualizations.git)

---

## What You Will Build

You will build a cryptography toolkit and visualization workflow that:

1. Loads lesson messages from `data/message_sets.json` (or seeds a starter set of 4 messages).
2. Selects a deterministic demo message for encryption and attack demonstrations.
3. Runs Caesar encryption/decryption with configurable shift keys.
4. Runs Vigenere encryption/decryption with configurable alphabetic keys.
5. Generates a weak educational RSA keypair and performs RSA encryption/decryption.
6. Demonstrates Caesar brute-force recovery by testing all 26 shifts.
7. Demonstrates weak RSA factorization by recovering primes from the modulus.
8. Benchmarks Caesar, Vigenere, and RSA runtime across increasing message lengths.
9. Benchmarks factorization cost across weak RSA bit sizes.
10. Saves frequency, runtime, and attack-cost plots under `data/outputs/`.
11. Persists trace, benchmark, and run-summary artifacts for future sessions.

---

## Requirements

- Python 3.11+
- `matplotlib`

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
   CRYPTOGRAPHY TOOLKIT AND VISUALIZATIONS
======================================================================

Configuration:
   Project type:           cryptography_toolkit_and_visualizations
   Classic demos:          Caesar, Vigenere
   Benchmark ciphers:      Caesar, Vigenere, RSA
   Demo message:           lesson_affine_safe
   Message lengths:        24, 64, 128, 256
   Trials per length:      3
   RSA demo bits:          16
   RSA attack bits:        12, 14, 16, 18
   Frequency plot:         True
   Runtime chart:          True
   Attack chart:           True
   Max preview rows:       6
   Random seed:            42

Startup:
   Data directory:         data/
   Outputs directory:      data/outputs/
   Message library:        data/message_sets.json (loaded 0 messages)
   Run catalog:            data/runs.json (loaded 0 runs)
   Recent runs:            None yet

---

Session complete:
   Session ID:             20260317_213836
   Messages available:     4
   Demo message:           lesson_affine_safe (59 chars)
   Runtime points:         36
   Attacks run:            2
   Elapsed time:           596.46 ms

Toolkit metrics: fastest_cipher=Caesar | fastest_avg_runtime_ms=0.04649 | rsa_factorization_ms=0.05150 | largest_message_length=256

Demo previews:
   Algorithm | Key material      | Cipher preview                  | Roundtrip
   ----------+-------------------+---------------------------------+----------
   Caesar   | shift=7           | ZLJBYL ZFZALTZ YLSF VU NVVK ... | yes
   Vigenere | key=VECTOR        | NIENFV NCUMSDN VGEM FI KQHR ... | yes
   RSA      | n=31439 e=65537   | 8577 12337 22665 10902 27995... | yes

Attack demonstrations:
   Attack                 | Target      | Success | Time (ms)
   -----------------------+-------------+---------+----------
   caesar_bruteforce       | Caesar      | yes     | 0.60370
   rsa_trial_division_fact | RSA         | yes     | 0.05150

Artifacts saved:
   Session record:         data/outputs/run_20260317_213836.json
   Trace bundle:           data/outputs/trace_20260317_213836.json
   Benchmark file:         data/outputs/benchmark_20260317_213836.json
   Frequency plot:         data/outputs/frequency_20260317_213836.png
   Runtime chart:          data/outputs/runtime_20260317_213836.png
   Attack chart:           data/outputs/attack_cost_20260317_213836.png
```

---

## Run

```bash
python main.py
```
