# Study Session Tracker (Python CLI)

Build a command-line app that logs interview study sessions and summarizes time spent per topic.

## Project objective

Create a CLI app that can:
- Add a study session (`topic`, `minutes`)
- List all sessions
- Remove one session by ID
- Clear all sessions
- Show summary totals per topic

Data should persist in a local JSON file.

## Prerequisites

- Python 3.10+
- Familiarity with Python lists/dicts and functions
- Basic terminal usage

## Estimated time

45-90 minutes

## Learning outcomes

By the end, you should be able to:
- Model records with dataclasses
- Read/write JSON files for local persistence
- Build subcommands with `argparse`
- Aggregate data by key (topic totals)

## Project structure

- `starter/` — partially implemented app with TODO functions
- `final/` — complete reference implementation
- `walkthrough.ipynb` — guided implementation steps

## Suggested workflow

1. Start with `starter/README.md`.
2. Implement the TODO functions in `starter/app.py`.
3. Verify using CLI commands.
4. Compare your approach with `final/app.py`.
5. Review `walkthrough.ipynb` for recap and reflection.

## Milestones

1. Implement persistence (`load_sessions`, `save_sessions`).
2. Implement CRUD-like operations (`add`, `remove`, `clear`).
3. Implement `summary` aggregation by topic.
4. Validate full CLI flow with sample commands.

## Example CLI session

From inside either `starter/` or `final/`:

```bash
python app.py list
python app.py add "arrays" 45
python app.py add "graphs" 30
python app.py summary
python app.py remove 1
python app.py clear
```

## Common pitfalls

- Not handling missing JSON file on first run.
- Forgetting to save after add/remove/clear operations.
- Allowing non-positive minute values.
- Mixing formatting of output between commands.
