# Beginner Project 50: Notebook-Based Portfolio Website Generator

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Deterministic portfolio page generation from notebook/markdown sources, strategy benchmarking, persistent history, and runtime/layout-debt visualizations

---

## Why This Project?

Turning notebooks and markdown reports into a polished portfolio is a practical skill for students and early-career developers. Many projects stay hidden in raw notebooks because the publishing step is inconsistent and manual. This project gives you a reproducible, strategy-driven generator workflow that turns source artifacts into structured portfolio pages while tracking quality and runtime tradeoffs.

This project teaches end-to-end portfolio generator workflow concepts where you can:

- load or auto-seed a reusable portfolio source library for deterministic demos,
- model notebook and markdown projects as a unified page generation pipeline,
- compare minimal slate, bold cards, and adaptive grid generation strategies,
- estimate quality with mean quality score, accessibility score, and SEO score,
- track per-page layout debt and cumulative debt across full generation order,
- persist session and sampled-page history for reproducible audit trails,
- benchmark strategy runtime across increasing project counts,
- visualize runtime behavior as a multi-series chart,
- visualize cumulative layout debt trend for selected strategy,
- export trace bundles and benchmark bundles to JSON for inspection,
- persist historical run summaries for repeatable profiling,
- and print a readable terminal report with page previews and artifact paths.

---

## Separate Repository

You can also access this project in a separate repository:

[notebook based portfolio website generator Repository](https://github.com/ShamShamsw/notebook-based-portfolio-website-generator.git)

---

## What You Will Build

You will build a notebook-based portfolio generation workflow that:

1. Loads portfolio definitions from `data/portfolio_sets.json` (or seeds a starter set of 2 portfolios).
2. Selects a deterministic demo portfolio for strategy walkthroughs.
3. Generates page summaries from notebook/markdown project source metadata.
4. Simulates minimal slate, bold cards, and adaptive grid strategies.
5. Compares strategy quality using mean quality score, accessibility score, and SEO score.
6. Tracks cumulative layout debt across generated page order.
7. Stores session and sampled-page events in `data/portfolio_history.json`.
8. Benchmarks strategy runtime across configured project counts and repeated trials.
9. Aggregates runtime points into strategy-level average performance summaries.
10. Saves a strategy runtime chart under `data/outputs/`.
11. Saves a cumulative layout debt chart under `data/outputs/`.
12. Persists trace, benchmark, and run-summary artifacts for future sessions.
13. Maintains a run catalog in `data/runs.json` for startup profiling.

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
   NOTEBOOK-BASED PORTFOLIO WEBSITE GENERATOR
======================================================================

Configuration:
   Project type:           notebook_based_portfolio_website_generator
   Strategy selected:      adaptive_grid
   Strategy set:           minimal_slate, bold_cards, adaptive_grid
   Demo portfolio label:   data_science_student
   Max projects:           8
   Snippets per project:   3
   Benchmark project counts: 3, 5, 8, 12, 16
   Trials per count:       4
   Runtime chart:          True
   Layout debt chart:      True
   Max preview rows:       8
   Random seed:            42

Startup:
   Data directory:         data/
   Outputs directory:      data/outputs/
   Portfolio library:      data/portfolio_sets.json (loaded 0 portfolios)
   Run catalog:            data/runs.json (loaded 0 runs)
   Portfolio history:      data/portfolio_history.json (loaded 0 entries)
   Recent runs:            None yet

---

Session complete:
   Session ID:             20260317_235921
   Portfolios available:   2
   Demo portfolio label:   data_science_student
   Strategy selected:      adaptive_grid
   Strategy runs:          3
   Pages generated:        4
   Runtime points:         60
   Elapsed time:           98.63 ms

Portfolio metrics: best_strategy=minimal_slate | best_avg_runtime_ms=0.138440 | selected_mean_quality_score=0.867593 | selected_accessibility_score=0.867593 | selected_seo_score=0.867593 | selected_cumulative_layout_debt=0.529628 | history_size=21

Selected strategy totals: mean_quality_score=0.867593 | accessibility_score=0.867593 | seo_score=0.867593 | cumulative_layout_debt=0.529628

Page previews:
   # | Strategy        | Slug                       | Type      | Quality | CumDebt
   --+-----------------+----------------------------+-----------+---------+--------
   1  | adaptive_grid   | retail-demand-forecasti... | notebook  | 0.8532  | 0.1468
   2  | adaptive_grid   | medical-text-summarizat... | markdown  | 0.8641  | 0.2827
   3  | adaptive_grid   | interactive-fraud-detec... | notebook  | 0.8760  | 0.4067

Artifacts saved:
   Session record:         data/outputs/run_20260317_235921.json
   Trace bundle:           data/outputs/trace_20260317_235921.json
   Benchmark file:         data/outputs/benchmark_20260317_235921.json
   Runtime chart:          data/outputs/strategy_runtime_20260317_235921.png
   Layout debt chart:      data/outputs/layout_debt_20260317_235921.png
```

---

## Run

```bash
python main.py
```
