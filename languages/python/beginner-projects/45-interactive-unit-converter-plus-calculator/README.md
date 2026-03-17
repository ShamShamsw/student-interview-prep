# Beginner Project 45: Interactive Unit Converter Plus Calculator

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Category-based unit conversion, safe arithmetic expression parsing, persistent history, and runtime/result visualizations

---

## Why This Project?

Unit conversion and calculator tools are common beginner projects, but they become much more educational when they are treated like a small, reproducible analytics workflow. Instead of only converting one value at a time, this project demonstrates how to organize conversion cases, evaluate expression sequences safely, save history across runs, and visualize trends in both runtime and computed values.

This project teaches end-to-end conversion and calculator workflow concepts where you can:

- load or auto-seed a reusable conversion-case library for deterministic demos,
- run category-based conversions for length, mass, temperature, volume, speed, and time,
- evaluate arithmetic expressions with a restricted AST parser (no unsafe eval),
- persist conversion and calculator history to support repeatable audit trails,
- benchmark conversion runtime across categories and growing input magnitudes,
- benchmark calculator parsing runtime across expression sizes,
- visualize runtime behavior as a multi-series chart,
- visualize calculator result trends across expression order,
- export trace bundles and benchmark bundles to JSON for inspection,
- persist historical run summaries for repeatable auditing,
- and print a readable terminal report with conversion previews, calculator previews, and artifact paths.

---

## Separate Repository

You can also access this project in a separate repository:

[interactive unit converter plus calculator Repository](interactive-unit-converter-plus-calculator.git)

---

## What You Will Build

You will build an interactive unit converter plus calculator workflow that:

1. Loads conversion cases from `data/conversion_sets.json` (or seeds a starter set of 6 cases).
2. Selects a deterministic demo sequence for conversion walkthroughs.
3. Converts values across six categories with category-specific unit sets.
4. Evaluates a calculator expression suite with safe parsing and validation.
5. Stores conversion and expression events in `data/calculator_history.json`.
6. Benchmarks conversion runtime across configured magnitudes and repeated trials.
7. Benchmarks calculator runtime across expression lengths.
8. Saves a category runtime chart under `data/outputs/`.
9. Saves a calculator result-trend chart under `data/outputs/`.
10. Persists trace, benchmark, and run-summary artifacts for future sessions.
11. Maintains a run catalog in `data/runs.json` for startup profiling.

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
   INTERACTIVE UNIT CONVERTER PLUS CALCULATOR
======================================================================

Configuration:
   Project type:           interactive_unit_converter_plus_calculator
   Categories:             length, mass, temperature, volume, speed, time
   Demo sequence:          lesson_everyday_mix
   Expressions:            5
   Benchmark magnitudes:   1, 10, 100, 1000, 10000
   Trials per magnitude:   4
   Category chart:         True
   History chart:          True
   Max preview rows:       8
   Random seed:            42

Startup:
   Data directory:         data/
   Outputs directory:      data/outputs/
   Conversion library:     data/conversion_sets.json (loaded 0 cases)
   Run catalog:            data/runs.json (loaded 0 runs)
   Calculator history:     data/calculator_history.json (loaded 0 entries)
   Recent runs:            None yet

---

Session complete:
   Session ID:             20260317_215442
   Cases available:        6
   Demo sequence:          lesson_everyday_mix
   Conversions run:        6
   Expressions run:        5
   Runtime points:         140
   Elapsed time:           336.00 ms

Toolkit metrics: fastest_series=volume | fastest_avg_runtime_ms=0.000560 | avg_expression_result=62.100000 | history_size=11

Conversion previews:
   Category     | From         | To           | Input        | Output
   -------------+--------------+--------------+--------------+--------------
   length       | mile         | kilometer    | 3.00000      | 4.82803
   temperature  | fahrenheit   | celsius      | 72.00000     | 22.22222
   mass         | pound        | kilogram     | 180.00000    | 81.64663

Calculator previews:
   Expression                          | Result       | Valid | Time (ms)
   ------------------------------------+--------------+-------+----------
   12 + 4 * 3                          | 24.000000    | yes   | 0.02131
   (18 / 3) + 7.5                      | 13.500000    | yes   | 0.01784
   2 ** 8 - 17                         | 239.000000   | yes   | 0.01955

Artifacts saved:
   Session record:         data/outputs/run_20260317_215442.json
   Trace bundle:           data/outputs/trace_20260317_215442.json
   Benchmark file:         data/outputs/benchmark_20260317_215442.json
   Category chart:         data/outputs/category_runtime_20260317_215442.png
   History chart:          data/outputs/history_trend_20260317_215442.png
```

---

## Run

```bash
python main.py
```
