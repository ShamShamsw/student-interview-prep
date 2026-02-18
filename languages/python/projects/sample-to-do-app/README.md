# Sample TODO App (Python CLI)

Build a small command-line TODO app to practice Python fundamentals used in interviews: file I/O, lists/dicts, dataclasses, and CLI argument parsing.

## Project objective

Create a TODO app that can:
- Add items
- List items
- Mark items as done
- Remove items
- Clear all items

Data is persisted to a local JSON file.

## Prerequisites

- Python 3.10+
- Basic Python syntax
- Comfortable running commands in a terminal

## Estimated time

45-90 minutes

## Learning outcomes

By the end of this project you should be able to:
- Model simple data with a dataclass
- Read and write JSON files safely
- Build a command-line interface with `argparse`
- Organize logic into testable functions

## Project structure

- `starter/` — partially implemented app with TODOs
- `final/` — complete reference implementation
- `walkthrough.ipynb` — guided explanation of the build process

## Suggested workflow

1. Read `starter/README.md`.
2. Implement all TODO functions in `starter/app.py`.
3. Run CLI commands to verify behavior.
4. Compare your solution with `final/app.py`.
5. Review `walkthrough.ipynb` for a step-by-step breakdown.

## Milestones

1. Implement persistence (`load_todos`, `save_todos`).
2. Implement item operations (`add_todo`, `mark_done`, `remove_todo`, `clear_all`).
3. Verify CLI behavior from the command line.
4. Compare to the final implementation and note differences.

## Example CLI session

From inside either `starter/` or `final/`:

```bash
python app.py list
python app.py add "Prepare interview notes"
python app.py add "Practice arrays"
python app.py done 1
python app.py list
python app.py remove 2
python app.py clear
```

## Common pitfalls

- Forgetting to handle a missing `todos.json` file.
- Not writing JSON with UTF-8 encoding.
- Forgetting to save after updates.
- Mutating data but not persisting changes.
