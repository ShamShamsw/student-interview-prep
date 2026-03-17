# Beginner Project 40: Real-Time Collaborative Notebook Demo

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Simulated multi-user concurrent editing, conflict detection, last-writer-wins resolution, and collaborative session visualization

---

## Why This Project?

Collaborative editing is a fundamental challenge in modern software—every shared document, live notebook, or version-controlled file must handle the case where two people change the same thing at the same time. This project demonstrates how to model concurrent edits, detect conflicts, apply a deterministic resolution strategy, and visualize the result.

This project teaches end-to-end collaborative editing simulation concepts where you can:

- load or auto-seed a reusable local notebook library,
- simulate multiple named users each generating randomized edit operations,
- assign deterministic simulated timestamps to every edit event,
- detect conflicts when two different users edit the same cell within a configurable time window,
- apply last-writer-wins conflict resolution to produce a consistent final notebook state,
- track conflict frequency per cell across all notebooks,
- generate a scatter-plot timeline of edit events, coloring by user and marking conflicts,
- generate a bar chart of conflict counts per cell,
- export a full edit bundle and per-session metadata to JSON,
- persist session summaries and historical edit catalogs,
- and print a readable terminal report with edit previews and artifact paths.

---

## Separate Repository

You can also access this project in a separate repository:

[real-time-collaborative-notebook-demo Repository](https://github.com/ShamShamsw/real-time-collaborative-notebook-demo.git)

---

## What You Will Build

You will build a collaborative notebook simulator that:

1. Loads notebook definitions from `data/notebooks.json` (or seeds a starter set).
2. Includes at least two multi-cell notebooks with code and markdown cells.
3. Simulates three named users (alice, bob, carol) each making several edit operations.
4. Assigns each edit a pseudo-random simulated timestamp within a fixed time window.
5. Detects conflicts when two different users edit the same cell within the conflict window.
6. Resolves every conflict with a last-writer-wins strategy and marks losers as discarded.
7. Applies all resolved edits to produce the final notebook cell contents and version counters.
8. Saves a timeline scatter plot of all edit events across cells, color-coded by user.
9. Saves a bar chart showing how many conflicts occurred in each cell.
10. Persists a full edit bundle and session summary JSON under `data/outputs/`.
11. Maintains session and edit catalogs for history and auditing.

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
   REAL-TIME COLLABORATIVE NOTEBOOK DEMO
======================================================================

Configuration:
   Project type:         real_time_collaborative_notebook
   Users:                alice, bob, carol
   Ops per user:         4
   Conflict window:      250 ms
   Timeline plot:        True
   Conflict chart:       True
   Max edits in report:  8
   Random seed:          42

Startup:
   Data directory:       data/
   Outputs directory:    data/outputs/
   Notebook library:     data/notebooks.json (loaded 2 notebooks)
   Session catalog:      data/sessions.json (loaded 0 sessions)
   Edit catalog:         data/edits.json (loaded 0 edits)
   Recent edits:         None yet

---

Session complete:
   Session ID:           20260317_201208
   Notebooks processed:  2
   Total edits:          24
   Conflicts detected:   4
   Conflicts resolved:   4
   Elapsed time:         310.25 ms

Dataset metrics: conflict_rate=16.7% | mean_edits_per_cell=4.8 | max_conflicts_in_cell=1 | resolution_strategy=last_writer_wins

Edit previews:
   ID       | User    | Notebook | Cell   | Operation | Conflict | Status
   ---------+---------+----------+--------+-----------+----------+----------
   edit_007 | bob     | nb_001   | cell_3 | replace   | no       | applied
   edit_003 | alice   | nb_001   | cell_1 | replace   | no       | applied
   edit_001 | alice   | nb_001   | cell_1 | replace   | no       | applied
   edit_008 | bob     | nb_001   | cell_3 | replace   | no       | applied
   edit_005 | bob     | nb_001   | cell_5 | insert    | yes      | discarded
   edit_004 | alice   | nb_001   | cell_5 | delete    | yes      | applied
   edit_002 | alice   | nb_001   | cell_2 | replace   | no       | applied
   edit_006 | bob     | nb_001   | cell_3 | replace   | yes      | discarded

Artifacts saved:
   Session record:       data/outputs/session_20260317_201208.json
   Edit bundle:          data/outputs/edits_20260317_201208.json
   Timeline plot:        data/outputs/timeline_20260317_201208.png
   Conflict chart:       data/outputs/conflicts_20260317_201208.png
   Total edits logged:   24
```

---

## Run

```bash
python main.py
```
