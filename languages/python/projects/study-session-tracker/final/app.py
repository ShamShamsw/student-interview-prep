"""Final: Study Session Tracker CLI

Track interview study sessions by topic and minutes.

Usage examples:
  python app.py list
  python app.py add "arrays" 45
  python app.py summary
  python app.py remove 1
  python app.py clear
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List

DB_PATH = Path(__file__).parent / "sessions.json"


@dataclass
class StudySession:
    id: int
    topic: str
    minutes: int


def load_sessions(path: Path = DB_PATH) -> List[StudySession]:
    if not path.exists():
        return []

    data = json.loads(path.read_text(encoding="utf-8"))
    return [StudySession(**row) for row in data]


def save_sessions(sessions: List[StudySession], path: Path = DB_PATH) -> None:
    data = [asdict(session) for session in sessions]
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def next_id(sessions: List[StudySession]) -> int:
    if not sessions:
        return 1
    return max(session.id for session in sessions) + 1


def add_session(topic: str, minutes: int, path: Path = DB_PATH) -> StudySession:
    sessions = load_sessions(path)
    session = StudySession(id=next_id(sessions), topic=topic, minutes=minutes)
    sessions.append(session)
    save_sessions(sessions, path)
    return session


def list_sessions(path: Path = DB_PATH) -> List[StudySession]:
    return load_sessions(path)


def remove_session(session_id: int, path: Path = DB_PATH) -> bool:
    sessions = load_sessions(path)
    filtered = [session for session in sessions if session.id != session_id]

    if len(filtered) == len(sessions):
        return False

    save_sessions(filtered, path)
    return True


def clear_sessions(path: Path = DB_PATH) -> int:
    sessions = load_sessions(path)
    save_sessions([], path)
    return len(sessions)


def summarize_minutes(path: Path = DB_PATH) -> dict[str, int]:
    sessions = load_sessions(path)
    summary: dict[str, int] = {}

    for session in sessions:
        summary[session.topic] = summary.get(session.topic, 0) + session.minutes

    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Study session tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List logged sessions")

    add_parser = subparsers.add_parser("add", help="Add a study session")
    add_parser.add_argument("topic", help="Topic studied")
    add_parser.add_argument("minutes", type=int, help="Minutes spent")

    remove_parser = subparsers.add_parser("remove", help="Remove a session by id")
    remove_parser.add_argument("id", type=int, help="Session id")

    subparsers.add_parser("summary", help="Show total minutes per topic")
    subparsers.add_parser("clear", help="Clear all sessions")

    return parser


def print_sessions(sessions: List[StudySession]) -> None:
    if not sessions:
        print("No study sessions logged yet.")
        return

    for session in sessions:
        print(f"#{session.id} | {session.topic} | {session.minutes} min")


def print_summary(summary: dict[str, int]) -> None:
    if not summary:
        print("No study data to summarize.")
        return

    for topic in sorted(summary):
        print(f"{topic}: {summary[topic]} min")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        print_sessions(list_sessions())
    elif args.command == "add":
        if args.minutes <= 0:
            print("Minutes must be a positive integer.")
            return
        session = add_session(args.topic, args.minutes)
        print(f"Added session #{session.id}: {session.topic} ({session.minutes} min)")
    elif args.command == "remove":
        removed = remove_session(args.id)
        if removed:
            print(f"Removed session #{args.id}")
        else:
            print(f"No session with id={args.id}")
    elif args.command == "summary":
        print_summary(summarize_minutes())
    elif args.command == "clear":
        count = clear_sessions()
        print(f"Cleared {count} session(s)")


if __name__ == "__main__":
    main()
