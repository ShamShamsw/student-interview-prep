# Beginner Project 22: Interactive Data Labeling Tool

**Time:** 3-5 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Dataset annotation workflows, label management, progress tracking, file I/O with JSON, and interactive command-line UI design

---

## Why This Project?

High-quality labeled data is the foundation of every machine learning model. Before a model can learn, a human must annotate examples—and this is exactly what data labeling tools do.

This project teaches you how to build a professional annotation workflow where you can:

- load a collection of short text samples from a file or generate them synthetically,
- present each sample to the user one at a time with a clean interactive interface,
- accept and validate user-provided labels from a configurable label set,
- track annotation progress (labeled / remaining / skipped),
- save annotations to JSON so sessions are resumable across runs,
- review, edit, and delete previous labels during the session,
- and export a final labeled dataset ready for downstream ML pipelines.

---

## Separate Repository

You can also access this project in a separate repository:

[Interactive Data Labeling Tool Repository](https://github.com/ShamShamsw/interactive-data-labeling-tool.git)

---

## What You Will Build

You will build a command-line data labeling tool that:

1. Loads or generates a collection of short text samples (e.g., news headlines, product reviews).
2. Presents samples one at a time with a numbered prompt and allowed label choices.
3. Accepts a label input, validates it against the configured label set, and saves the annotation.
4. Supports skipping a sample (mark as "skipped" to revisit later).
5. Tracks live progress: total samples, labeled count, skipped count, remaining count.
6. Allows the user to review all annotations so far during the session.
7. Allows editing or deleting a previous annotation by sample index.
8. Saves all annotations to a JSON file after every label so progress is never lost.
9. Displays a final summary when all samples are labeled or the user quits.
10. Exports a clean CSV file of the completed labeled dataset.

---

## Requirements

- Python 3.11+
- `numpy`
- `pandas`
- `rich` (for colored terminal output; falls back to plain text if unavailable)

Install with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
   INTERACTIVE DATA LABELING TOOL - TEXT ANNOTATION SESSION
======================================================================

Configuration:
   Dataset: Synthetic news headlines (50 samples)
   Label set: ['positive', 'negative', 'neutral']
   Session file: data/sessions/session_20260316.json
   Auto-save: enabled (after each label)
   Resume: 12 annotations found from previous session

Progress: 12 / 50 labeled  |  2 skipped  |  36 remaining

──────────────────────────────────────────────────
Sample #13 of 50
──────────────────────────────────────────────────

  "Scientists discover breakthrough treatment for rare disease"

Labels:  [P] positive   [N] negative   [U] neutral
         [S] skip       [R] review all  [Q] quit

Your label: P
✓ Labeled as: positive

Progress: 13 / 50 labeled  |  2 skipped  |  35 remaining

──────────────────────────────────────────────────
Sample #14 of 50
──────────────────────────────────────────────────

  "Stock market crashes amid rising inflation fears"

Labels:  [P] positive   [N] negative   [U] neutral
         [S] skip       [R] review all  [Q] quit

Your label: N
✓ Labeled as: negative

Progress: 14 / 50 labeled  |  2 skipped  |  34 remaining

... (continuing) ...

======================================================================
   SESSION COMPLETE
======================================================================

   Total samples:   50
   Labeled:         48
   Skipped:          2
   Completion:      96.0%

   Label distribution:
      positive:  22  (45.8%)
      negative:  19  (39.6%)
      neutral:    7  (14.6%)

   Session file:  data/sessions/session_20260316.json
   CSV export:    data/exports/labeled_dataset_20260316.csv

   Exported 48 labeled samples. Ready for ML pipeline.
```

---

## Build Order

Follow this order for clean architecture:

1. `storage.py` — Load/save samples, annotations, and session JSON
2. `models.py` — Define sample and annotation data models
3. `operations.py` — Core labeling workflow and annotation logic
4. `display.py` — Format prompts, progress bars, review tables
5. `main.py` — Orchestrate the interactive labeling session

---

## Step-by-Step Instructions

### Step 1: Implement `storage.py`

Create functions to:
- Load text samples from a plain `.txt` file (one sample per line) or generate synthetic headlines
- Load an existing session JSON (to resume annotation progress)
- Save the current session to JSON after each annotation
- Export completed annotations to CSV

**Key functions:**
- `load_or_generate_samples(source: str, n_samples: int) → list[str]`
- `load_session(session_file: str) → dict` — returns empty session if file not found
- `save_session(session_file: str, session: dict) → None`
- `export_csv(export_path: str, samples: list, annotations: dict) → int` — returns count of exported rows

### Step 2: Implement `models.py`

Define data models and constants:
- Session configuration with label set, session file path, dataset info
- Annotation record (sample index, sample text, label, timestamp, skipped flag)
- Session progress summary

**Key structures:**
- `create_session_config(label_set: list, session_name: str, ...) → dict`
- `create_annotation(sample_idx: int, text: str, label: str, skipped: bool) → dict`
- `create_session(config: dict, samples: list) → dict` — new empty session ready for annotation
- `create_progress_summary(session: dict) → dict` — counts labeled/skipped/remaining

### Step 3: Implement `operations.py`

Build the core annotation workflow:
- Apply a label to a sample (validate label, create annotation record, auto-save)
- Skip a sample
- Edit a previous annotation
- Delete an annotation
- Find the next unlabeled sample index
- Check whether the session is complete

**Key functions:**
- `apply_label(session: dict, sample_idx: int, label: str) → dict` — returns updated session
- `skip_sample(session: dict, sample_idx: int) → dict`
- `edit_annotation(session: dict, sample_idx: int, new_label: str) → dict`
- `delete_annotation(session: dict, sample_idx: int) → dict`
- `next_unlabeled_index(session: dict) → int | None`
- `is_session_complete(session: dict) → bool`
- `run_core_flow() → dict` — orchestrates the interactive loop

### Step 4: Implement `display.py`

Format all user-facing output:
- Header banner
- Per-sample prompt with sample text and label key legend
- Progress tracker (labeled / skipped / remaining)
- Review table of all current annotations
- Final session summary with label distribution
- Confirmation messages for labeling, editing, deleting

**Key functions:**
- `format_header() → str`
- `format_startup_guide(config: dict, session: dict) → str`
- `format_sample_prompt(sample_idx: int, total: int, text: str, label_set: list) → str`
- `format_progress(session: dict) → str`
- `format_review_table(session: dict) → str`
- `format_session_summary(session: dict, export_path: str) → str`
- `format_run_report(summary: dict) → str`

### Step 5: Implement `main.py`

Orchestrate the interactive loop:
1. Load configuration and samples
2. Load or create session (for resumability)
3. Print header and startup guide
4. Enter the labeling loop (present → accept input → validate → apply → save → repeat)
5. Handle special commands: skip, review, quit, edit
6. On completion or quit: display session summary and export CSV

---

## Done Criteria

- [ ] The project runs from `main.py` without crashes.
- [ ] At least 3 label classes are supported and validated.
- [ ] Annotations are saved to JSON after every label (no data lost on crash).
- [ ] Sessions are resumable: restarting loads existing annotations.
- [ ] Skip, review, and quit commands work correctly.
- [ ] Final summary shows label counts and percentages.
- [ ] A CSV export is generated at session end.
- [ ] Every function has a docstring.
- [ ] Code is organized by concern (models, operations, display, storage).

---

## Stretch Goals

1. Add an "undo last label" command that reverts the most recent annotation.
2. Support image labeling: display a file path and ask for a label (e.g., for classifying filenames).
3. Add inter-annotator agreement: load two session files and compute Cohen's Kappa.
4. Support multi-label annotation (a sample can have more than one label).
5. Add a confidence score input alongside each label (1–5 scale).
6. Load samples from a CSV column instead of a plain text file.
7. Generate an annotation report PDF summarizing label distribution and sample statistics.
