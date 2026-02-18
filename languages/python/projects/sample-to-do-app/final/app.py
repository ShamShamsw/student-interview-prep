"""Final TODO CLI app implementation.

Usage examples:
  python app.py list
  python app.py add "Buy milk"
  python app.py done 1
  python app.py remove 1
  python app.py clear
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

DB_PATH = Path(__file__).parent / "todos.json"


@dataclass
class TodoItem:
    id: int
    text: str
    done: bool = False


def load_todos(path: Path = DB_PATH) -> List[TodoItem]:
    if not path.exists():
        return []

    data = json.loads(path.read_text(encoding="utf-8"))
    return [TodoItem(**row) for row in data]


def save_todos(todos: List[TodoItem], path: Path = DB_PATH) -> None:
    data = [asdict(item) for item in todos]
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def next_id(todos: List[TodoItem]) -> int:
    if not todos:
        return 1
    return max(item.id for item in todos) + 1


def add_todo(text: str, path: Path = DB_PATH) -> TodoItem:
    todos = load_todos(path)
    item = TodoItem(id=next_id(todos), text=text, done=False)
    todos.append(item)
    save_todos(todos, path)
    return item


def list_todos(path: Path = DB_PATH) -> List[TodoItem]:
    return load_todos(path)


def mark_done(item_id: int, path: Path = DB_PATH) -> TodoItem | None:
    todos = load_todos(path)
    for item in todos:
        if item.id == item_id:
            item.done = True
            save_todos(todos, path)
            return item
    return None


def remove_todo(item_id: int, path: Path = DB_PATH) -> bool:
    todos = load_todos(path)
    filtered = [item for item in todos if item.id != item_id]

    if len(filtered) == len(todos):
        return False

    save_todos(filtered, path)
    return True


def clear_all(path: Path = DB_PATH) -> int:
    todos = load_todos(path)
    save_todos([], path)
    return len(todos)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple TODO command-line app")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List all TODO items")

    add_parser = subparsers.add_parser("add", help="Add a TODO item")
    add_parser.add_argument("text", help="Task description")

    done_parser = subparsers.add_parser("done", help="Mark a TODO item as done")
    done_parser.add_argument("id", type=int, help="ID of todo to mark done")

    remove_parser = subparsers.add_parser("remove", help="Remove a TODO item")
    remove_parser.add_argument("id", type=int, help="ID of todo to remove")

    subparsers.add_parser("clear", help="Remove all TODO items")

    return parser


def print_todos(todos: List[TodoItem]) -> None:
    if not todos:
        print("No TODO items yet.")
        return
    for item in todos:
        status = "x" if item.done else " "
        print(f"[{status}] {item.id}: {item.text}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        print_todos(list_todos())
    elif args.command == "add":
        item = add_todo(args.text)
        print(f"Added #{item.id}: {item.text}")
    elif args.command == "done":
        item = mark_done(args.id)
        if item is None:
            print(f"No TODO with id={args.id}")
        else:
            print(f"Marked #{item.id} as done")
    elif args.command == "remove":
        removed = remove_todo(args.id)
        if removed:
            print(f"Removed #{args.id}")
        else:
            print(f"No TODO with id={args.id}")
    elif args.command == "clear":
        count = clear_all()
        print(f"Cleared {count} item(s)")


if __name__ == "__main__":
    main()
