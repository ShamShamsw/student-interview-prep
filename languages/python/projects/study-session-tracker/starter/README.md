# Starter: Study Session Tracker

This starter contains a partially implemented command-line app for tracking interview study sessions.

Your goal is to complete the TODO-marked functions in `app.py`.

## Functions to implement

- `load_sessions`
- `save_sessions`
- `add_session`
- `remove_session`
- `clear_sessions`
- `summarize_minutes`

## Setup

From this `starter/` folder:

```bash
python app.py list
```

## Verification commands

```bash
python app.py add "arrays" 40
python app.py add "trees" 35
python app.py list
python app.py summary
python app.py remove 1
python app.py clear
```

## Success criteria

- Missing `sessions.json` does not crash the app.
- Added sessions persist across runs.
- `summary` reports total minutes grouped by topic.
- `remove` correctly handles missing IDs.
- `clear` removes all sessions and returns correct count.

## Compare after finishing

Use `../final/app.py` as your reference solution and review `../walkthrough.ipynb`.
