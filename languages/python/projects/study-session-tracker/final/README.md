# Final: Study Session Tracker

This folder contains the complete reference implementation of the Study Session Tracker CLI.

## Included functionality

- Add/list/remove/clear study sessions
- Per-topic time summary
- JSON persistence to `sessions.json`
- CLI command routing via `argparse`

## Run commands

From this `final/` folder:

```bash
python app.py list
python app.py add "arrays" 45
python app.py add "dp" 30
python app.py summary
python app.py remove 1
python app.py clear
```

## Output examples

- Session list: `#2 | arrays | 45 min`
- Summary line: `arrays: 75 min`

## How to use this reference

1. Finish the starter implementation first.
2. Compare function-by-function with `../starter/app.py`.
3. Focus on persistence and aggregation patterns.
4. Review `../walkthrough.ipynb` for the guided flow.
