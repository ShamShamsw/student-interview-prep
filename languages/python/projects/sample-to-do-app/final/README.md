# Final: Sample TODO App

This folder contains the **complete reference implementation** of the sample TODO command-line app.

Use this after attempting `../starter/app.py`.

## What's included

- Full CRUD-style TODO operations (add/list/done/remove/clear)
- JSON persistence via `todos.json`
- Dataclass model for TODO items
- CLI built with `argparse`

## Run the app

From this folder (`final/`):

```bash
python app.py list
python app.py add "Prepare behavioral stories"
python app.py done 1
python app.py remove 1
python app.py clear
```

## Expected output style

- List format: `[ ] 1: Task text` or `[x] 1: Task text`
- Empty list message: `No TODO items yet.`

## How to use this as a learning reference

1. Finish the starter version first.
2. Compare function-by-function between starter and final.
3. Note handling of file I/O edge cases and persistence.
4. Review `../walkthrough.ipynb` for guided explanation.
