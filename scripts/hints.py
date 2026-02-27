#!/usr/bin/env python3
"""Interactive Hint System for Interview Prep.

Provides progressive hints without spoiling the solution.

Usage python scripts/hints.py 01-two-sum
    python scripts/hints.py 15-valid-palindrome --level 2
    python scripts/hints.py 35-coin-change --all
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Color codes
COLORS = {
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}


def colorize(text: str, color: str) -> str:
    """Apply color to text."""
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"


class HintSystem:
    """Progressive hint system for coding problems."""

    def __init__(self, workspace_root: Path | None = None):
        """Initialize hint system."""
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent

        self.workspace_root = Path(workspace_root)
        self.hints_file = self.workspace_root / "learn" / "resources" / "HINTS.json"

        # Load or create hints database
        self.hints_db = self._load_hints()
        if not self.hints_db:
            self.hints_db = self._create_default_hints()
            self._save_hints()

    def _load_hints(self) -> dict[str, Any]:
        """Load hints from file."""
        if self.hints_file.exists():
            try:
                return json.loads(self.hints_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {}

    def _save_hints(self) -> None:
        """Save hints to file."""
        self.hints_file.parent.mkdir(parents=True, exist_ok=True)
        self.hints_file.write_text(
            json.dumps(self.hints_db, indent=2),
            encoding="utf-8",
        )

    def _create_default_hints(self) -> dict[str, Any]:
        """Create default hints for common problems."""
        return {
            "01-two-sum": {
                "name": "Two Sum",
                "hints": [
                    {
                        "level": 1,
                        "hint": "Think about what data structure allows O(1) lookup time.",
                    },
                    {
                        "level": 2,
                        "hint": "For each number, you need to find target - number. Store seen numbers as you iterate.",
                    },
                    {
                        "level": 3,
                        "hint": "Use a hash table (dictionary) to store {value: index} pairs.",
                    },
                    {
                        "level": 4,
                        "hint": "For each num, check if (target - num) exists in your hash table.",
                    },
                    {
                        "level": 5,
                        "hint": "Time: O(n), Space: O(n). One pass through the array.",
                    },
                ],
                "approaches": ["Hash Table", "Brute Force (O(n²))"],
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
            },
            "15-valid-palindrome": {
                "name": "Valid Palindrome",
                "hints": [
                    {
                        "level": 1,
                        "hint": "A palindrome reads the same forwards and backwards.",
                    },
                    {
                        "level": 2,
                        "hint": "Use two pointers, one at each end of the string.",
                    },
                    {
                        "level": 3,
                        "hint": "Ignore non-alphanumeric characters and compare case-insensitively.",
                    },
                    {
                        "level": 4,
                        "hint": "Move pointers inward while they match. If they meet, it's a palindrome.",
                    },
                    {
                        "level": 5,
                        "hint": "Time: O(n), Space: O(1). In-place comparison.",
                    },
                ],
                "approaches": ["Two Pointers", "Reverse and Compare"],
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
            },
            "21-binary-search": {
                "name": "Binary Search",
                "hints": [
                    {"level": 1, "hint": "Exploit the fact that the array is sorted."},
                    {
                        "level": 2,
                        "hint": "Each comparison allows you to eliminate half of the remaining elements.",
                    },
                    {
                        "level": 3,
                        "hint": "Maintain left and right pointers. Check the middle element.",
                    },
                    {
                        "level": 4,
                        "hint": "If target < mid, search left half. If target > mid, search right half.",
                    },
                    {
                        "level": 5,
                        "hint": "Time: O(log n), Space: O(1). Classic divide and conquer.",
                    },
                ],
                "approaches": ["Iterative Binary Search", "Recursive Binary Search"],
                "time_complexity": "O(log n)",
                "space_complexity": "O(1)",
            },
            "26-reverse-linked-list": {
                "name": "Reverse Linked List",
                "hints": [
                    {
                        "level": 1,
                        "hint": "You need to reverse the direction of all pointers.",
                    },
                    {
                        "level": 2,
                        "hint": "Think about reversing one connection at a time.",
                    },
                    {
                        "level": 3,
                        "hint": "Keep track of previous, current, and next nodes.",
                    },
                    {
                        "level": 4,
                        "hint": "Iterate: save next, point current to previous, advance all pointers.",
                    },
                    {"level": 5, "hint": "Time: O(n), Space: O(1). In-place reversal."},
                ],
                "approaches": ["Iterative", "Recursive"],
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
            },
            "35-coin-change": {
                "name": "Coin Change",
                "hints": [
                    {
                        "level": 1,
                        "hint": "This is a classic dynamic programming problem.",
                    },
                    {
                        "level": 2,
                        "hint": "Build up solutions for smaller amounts first.",
                    },
                    {
                        "level": 3,
                        "hint": "Create a DP array where dp[i] = minimum coins for amount i.",
                    },
                    {
                        "level": 4,
                        "hint": "For each amount, try using each coin: dp[i] = min(dp[i], dp[i-coin] + 1).",
                    },
                    {
                        "level": 5,
                        "hint": "Time: O(amount × coins), Space: O(amount). Bottom-up DP.",
                    },
                ],
                "approaches": ["Dynamic Programming", "BFS", "DFS with Memoization"],
                "time_complexity": "O(amount × coins)",
                "space_complexity": "O(amount)",
            },
        }

    def show_hints(
        self,
        problem_id: str,
        level: int | None = None,
        show_all: bool = False,
    ) -> None:
        """Show hints for a problem."""
        if problem_id not in self.hints_db:
            print(colorize(f"\n❌ No hints available for {problem_id}", "red"))
            print(colorize("\n💡 Tip: Try solving without hints first!", "cyan"))
            return

        problem_hints = self.hints_db[problem_id]
        hints = problem_hints["hints"]

        print(colorize(f"\n💡 HINTS: {problem_hints['name']}\n", "bold"))
        print("=" * 60)

        if show_all:
            # Show all hints
            for hint in hints:
                lvl = hint["level"]
                print(f"\n{colorize(f'Level {lvl}:', 'yellow')}")
                print(f"   {hint['hint']}")
        elif level is not None:
            # Show specific level
            hint = next((h for h in hints if h["level"] == level), None)
            if hint:
                print(f"\n{colorize(f'Level {level} Hint:', 'yellow')}")
                print(f"   {hint['hint']}")
            else:
                print(colorize(f"\n❌ No hint at level {level}", "red"))
        else:
            # Show progressive hints
            print(
                colorize(
                    "Progressive Hints (use --level N for specific hint):\n", "cyan"
                )
            )
            print(colorize("Level 1 (Concept):", "green"))
            print(f"   {hints[0]['hint']}")

            if len(hints) > 1:
                print(colorize("\n💭 Need more help? Use:", "dim"))
                for i in range(1, len(hints)):
                    print(f"   --level {i+1} for Level {i+1} hint")

        # Show complexity
        print(colorize("\n⚡ Target Complexity:", "cyan"))
        print(f"   Time: {problem_hints.get('time_complexity', 'N/A')}")
        print(f"   Space: {problem_hints.get('space_complexity', 'N/A')}")

        # Show approaches
        if "approaches" in problem_hints:
            print(colorize("\n🎯 Possible Approaches:", "cyan"))
            for approach in problem_hints["approaches"]:
                print(f"   • {approach}")

        print("\n" + "=" * 60)
        print()

    def list_available(self) -> None:
        """List all problems with hints."""
        print(colorize("\n📚 AVAILABLE HINTS\n", "bold"))
        print("=" * 60)

        for problem_id, data in sorted(self.hints_db.items()):
            name = data.get("name", problem_id)
            hint_count = len(data.get("hints", []))
            print(f"  {colorize(problem_id, 'cyan')}: {name} ({hint_count} hints)")

        print("\n" + "=" * 60)
        print(colorize("\nUsage: python scripts/hints.py <problem-id>", "dim"))
        print()


def main() -> None:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Get hints for coding problems")
    parser.add_argument("problem_id", nargs="?", help="Problem ID (e.g., 01-two-sum)")
    parser.add_argument("--level", "-l", type=int, help="Show specific hint level")
    parser.add_argument("--all", "-a", action="store_true", help="Show all hints")
    parser.add_argument(
        "--list", action="store_true", help="List all problems with hints"
    )

    args = parser.parse_args()

    system = HintSystem()

    if args.list:
        system.list_available()
        return

    if not args.problem_id:
        system.list_available()
        return

    system.show_hints(args.problem_id, level=args.level, show_all=args.all)


if __name__ == "__main__":
    main()
