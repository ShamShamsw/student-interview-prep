from pathlib import Path
import json
import sys


def iter_notebooks(root: Path):
    for path in root.rglob("*.ipynb"):
        if ".git" in path.parts:
            continue
        yield path


def validate_notebook(path: Path):
    errors = []
    try:
        with path.open("r", encoding="utf-8") as file:
            notebook = json.load(file)
    except Exception as exc:
        return [f"{path}: invalid JSON ({exc})"]

    if not isinstance(notebook, dict):
        return [f"{path}: notebook root must be an object"]

    cells = notebook.get("cells")
    if not isinstance(cells, list):
        return [f"{path}: missing or invalid 'cells' array"]

    for index, cell in enumerate(cells, start=1):
        if not isinstance(cell, dict):
            errors.append(f"{path}: cell {index} is not an object")
            continue

        metadata = cell.get("metadata", {})
        if not isinstance(metadata, dict):
            errors.append(f"{path}: cell {index} has invalid metadata")
            continue

        if "language" not in metadata:
            errors.append(f"{path}: cell {index} missing metadata.language")

        if "source" not in cell:
            errors.append(f"{path}: cell {index} missing source")

    return errors


def main():
    repo_root = Path(__file__).resolve().parents[2]
    notebooks = list(iter_notebooks(repo_root))

    if not notebooks:
        print("No notebooks found. Check passed.")
        return 0

    all_errors = []
    for notebook in notebooks:
        all_errors.extend(validate_notebook(notebook))

    if all_errors:
        print("Notebook validation failed:")
        for error in all_errors:
            print(f"- {error}")
        return 1

    print(f"Notebook validation passed for {len(notebooks)} notebook(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
