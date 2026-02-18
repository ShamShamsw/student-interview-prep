# Starter: Sample TODO App

This folder contains a **partially implemented** command-line TODO app.

Your task is to complete the TODO-marked functions in `app.py`.

## What to implement

Complete these functions:
- `load_todos`
- `save_todos`
- `add_todo`
- `mark_done`
- `remove_todo`
- `clear_all`

Keep the command interface unchanged.

## Setup

From this folder (`starter/`):

```bash
python --version
python app.py list
```

## CLI commands to verify

Use these while implementing:

```bash
python app.py add "Buy groceries"
python app.py add "Review recursion"
python app.py list
python app.py done 1
python app.py list
python app.py remove 2
python app.py clear
```

## Success criteria

- Missing `todos.json` is handled without crashing.
- Added items persist across runs.
- `done` updates only the selected ID.
- `remove` returns correct behavior for missing IDs.
- `clear` empties all items and reports count.

## Compare with reference

After finishing, compare your implementation against `../final/app.py` and review `../walkthrough.ipynb`.
