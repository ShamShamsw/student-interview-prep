#!/usr/bin/env python3
"""Visual Progress Tracker for Interview Prep.

Displays your problem-solving progress with:
- Visual progress bars
- Topic breakdown
- Difficulty distribution
- Streak tracking
- Achievement unlocks

Usage:
    python scripts/progress_tracker.py
    python scripts/progress_tracker.py --detailed
    python scripts/progress_tracker.py --export progress.json
"""

from __future__ import annotations

import json
import os
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# Color codes for terminal output
COLORS = {
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}


def colorize(text: str, color: str) -> str:
    """Apply color to text."""
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"


def progress_bar(completed: int, total: int, width: int = 30) -> str:
    """Generate a visual progress bar."""
    if total == 0:
        return "[" + " " * width + "] 0%"
    
    percentage = completed / total
    filled = int(width * percentage)
    bar = "█" * filled + "░" * (width - filled)
    
    color = "red" if percentage < 0.3 else "yellow" if percentage < 0.7 else "green"
    return colorize(f"[{bar}] {percentage * 100:.1f}%", color)


class ProgressTracker:
    """Track and display user progress through interview prep."""

    def __init__(self, workspace_root: Path | None = None):
        """Initialize the progress tracker."""
        if workspace_root is None:
            # Find workspace root (directory containing this script's parent)
            workspace_root = Path(__file__).parent.parent
        
        self.workspace_root = Path(workspace_root)
        self.problems_dir = self.workspace_root / "languages" / "python" / "problems"
        self.solutions_dir = self.problems_dir / "solutions"
        self.tests_dir = self.problems_dir / "tests"
        self.progress_file = self.workspace_root / ".progress_data.json"
        
        self.problems = self._discover_problems()
        self.progress_data = self._load_progress_data()
    
    def _discover_problems(self) -> dict[str, dict[str, Any]]:
        """Discover all problems from markdown files."""
        problems = {}
        
        if not self.problems_dir.exists():
            return problems
        
        for md_file in self.problems_dir.glob("*.md"):
            if md_file.name == "README.md" or md_file.name == "ISSUES_SEED.md":
                continue
            
            problem_id = md_file.stem
            content = md_file.read_text(encoding="utf-8")
            
            # Extract difficulty and topics
            difficulty = "Unknown"
            topics = []
            
            for line in content.split("\n")[:10]:
                if line.startswith("Difficulty:"):
                    difficulty = line.split(":", 1)[1].strip()
                elif line.startswith("Topics:"):
                    topics = [t.strip() for t in line.split(":", 1)[1].split(",")]
            
            problems[problem_id] = {
                "id": problem_id,
                "name": md_file.stem.replace("-", " ").title(),
                "difficulty": difficulty,
                "topics": topics,
                "file": str(md_file),
            }
        
        return problems
    
    def _load_progress_data(self) -> dict[str, Any]:
        """Load progress data from file."""
        if self.progress_file.exists():
            try:
                return json.loads(self.progress_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        
        return {
            "completed": [],
            "attempts": {},
            "streak_data": {"current": 0, "best": 0, "last_date": None},
            "achievements": [],
        }
    
    def _save_progress_data(self) -> None:
        """Save progress data to file."""
        self.progress_file.write_text(
            json.dumps(self.progress_data, indent=2),
            encoding="utf-8",
        )
    
    def _check_completed_problems(self) -> list[str]:
        """Check which problems have been completed based on solution files."""
        completed = []
        
        if not self.solutions_dir.exists():
            return completed
        
        for problem_id in self.problems:
            solution_file = self.solutions_dir / f"{problem_id}.py"
            if solution_file.exists():
                content = solution_file.read_text(encoding="utf-8")
                # Check if solution has actual implementation (not just template)
                if "pass" not in content or len(content) > 200:
                    completed.append(problem_id)
        
        return completed
    
    def update_progress(self, problem_id: str, solved: bool = True) -> None:
        """Manually update progress for a problem."""
        if solved and problem_id not in self.progress_data["completed"]:
            self.progress_data["completed"].append(problem_id)
            self._update_streak()
        elif not solved and problem_id in self.progress_data["completed"]:
            self.progress_data["completed"].remove(problem_id)
        
        # Record attempt
        if problem_id not in self.progress_data["attempts"]:
            self.progress_data["attempts"][problem_id] = []
        
        self.progress_data["attempts"][problem_id].append({
            "date": datetime.now().isoformat(),
            "solved": solved,
        })
        
        self._check_achievements()
        self._save_progress_data()
    
    def _update_streak(self) -> None:
        """Update streak data."""
        today = datetime.now().date().isoformat()
        last_date = self.progress_data["streak_data"].get("last_date")
        
        if last_date == today:
            return  # Already counted today
        
        if last_date:
            last = datetime.fromisoformat(last_date).date()
            yesterday = datetime.now().date() - timedelta(days=1)
            
            if last == yesterday:
                # Continue streak
                self.progress_data["streak_data"]["current"] += 1
            elif last < yesterday:
                # Streak broken, reset
                self.progress_data["streak_data"]["current"] = 1
        else:
            # First problem
            self.progress_data["streak_data"]["current"] = 1
        
        self.progress_data["streak_data"]["last_date"] = today
        
        # Update best streak
        current = self.progress_data["streak_data"]["current"]
        best = self.progress_data["streak_data"]["best"]
        if current > best:
            self.progress_data["streak_data"]["best"] = current
    
    def _check_achievements(self) -> None:
        """Check and unlock achievements."""
        achievements = [
            ("first_solve", "First Steps", "Solved your first problem!", lambda: len(self.progress_data["completed"]) >= 1),
            ("five_solved", "Getting Started", "Solved 5 problems!", lambda: len(self.progress_data["completed"]) >= 5),
            ("ten_solved", "Warming Up", "Solved 10 problems!", lambda: len(self.progress_data["completed"]) >= 10),
            ("twenty_solved", "Making Progress", "Solved 20 problems!", lambda: len(self.progress_data["completed"]) >= 20),
            ("all_solved", "Master", "Solved all problems!", lambda: len(self.progress_data["completed"]) >= len(self.problems)),
            ("streak_3", "Consistent", "3-day streak!", lambda: self.progress_data["streak_data"]["current"] >= 3),
            ("streak_7", "Dedicated", "7-day streak!", lambda: self.progress_data["streak_data"]["current"] >= 7),
            ("streak_30", "Unstoppable", "30-day streak!", lambda: self.progress_data["streak_data"]["current"] >= 30),
        ]
        
        for achievement_id, name, description, condition in achievements:
            if achievement_id not in self.progress_data["achievements"]:
                if condition():
                    self.progress_data["achievements"].append(achievement_id)
                    print(colorize(f"🏆 Achievement Unlocked: {name}", "yellow"))
                    print(f"   {description}\n")
    
    def display_progress(self, detailed: bool = False) -> None:
        """Display current progress."""
        completed = set(self._check_completed_problems())
        total = len(self.problems)
        
        # Update completed in progress data
        for problem_id in completed:
            if problem_id not in self.progress_data["completed"]:
                self.progress_data["completed"].append(problem_id)
        
        print(colorize("\n📊 INTERVIEW PREP PROGRESS TRACKER\n", "bold"))
        print("=" * 60)
        
        # Overall Progress
        print(colorize("\n📈 Overall Progress", "cyan"))
        print(f"Problems Completed: {len(completed)}/{total}")
        print(progress_bar(len(completed), total, 40))
        
        # Streak
        streak = self.progress_data["streak_data"]
        print(colorize(f"\n🔥 Current Streak: {streak['current']} days", "yellow"))
        print(colorize(f"   Best Streak: {streak['best']} days", "yellow"))
        
        # Difficulty Breakdown
        print(colorize("\n📊 By Difficulty", "cyan"))
        by_difficulty = defaultdict(lambda: {"total": 0, "completed": 0})
        
        for problem_id, problem in self.problems.items():
            difficulty = problem["difficulty"]
            by_difficulty[difficulty]["total"] += 1
            if problem_id in completed:
                by_difficulty[difficulty]["completed"] += 1
        
        for difficulty in ["Easy", "Medium", "Hard"]:
            if difficulty in by_difficulty:
                stats = by_difficulty[difficulty]
                print(f"\n  {difficulty:8} {stats['completed']:2}/{stats['total']:2} ", end="")
                print(progress_bar(stats["completed"], stats["total"], 25))
        
        # Topic Breakdown
        if detailed:
            print(colorize("\n📚 By Topic", "cyan"))
            by_topic = defaultdict(lambda: {"total": 0, "completed": 0})
            
            for problem_id, problem in self.problems.items():
                for topic in problem["topics"]:
                    by_topic[topic]["total"] += 1
                    if problem_id in completed:
                        by_topic[topic]["completed"] += 1
            
            for topic in sorted(by_topic.keys()):
                stats = by_topic[topic]
                print(f"\n  {topic:20} {stats['completed']:2}/{stats['total']:2} ", end="")
                print(progress_bar(stats["completed"], stats["total"], 20))
        
        # Recent Activity
        if self.progress_data["attempts"]:
            print(colorize("\n📅 Recent Activity", "cyan"))
            recent = sorted(
                [
                    (problem_id, attempt)
                    for problem_id, attempts in self.progress_data["attempts"].items()
                    for attempt in attempts
                ],
                key=lambda x: x[1]["date"],
                reverse=True,
            )[:5]
            
            for problem_id, attempt in recent:
                date = datetime.fromisoformat(attempt["date"]).strftime("%Y-%m-%d %H:%M")
                status = "✅" if attempt["solved"] else "❌"
                problem_name = self.problems.get(problem_id, {}).get("name", problem_id)
                print(f"  {status} {date} - {problem_name}")
        
        # Achievements
        if self.progress_data["achievements"]:
            print(colorize("\n🏆 Achievements Unlocked", "yellow"))
            achievement_names = {
                "first_solve": "First Steps",
                "five_solved": "Getting Started",
                "ten_solved": "Warming Up",
                "twenty_solved": "Making Progress",
                "all_solved": "Master",
                "streak_3": "Consistent",
                "streak_7": "Dedicated",
                "streak_30": "Unstoppable",
            }
            
            for achievement_id in self.progress_data["achievements"]:
                name = achievement_names.get(achievement_id, achievement_id)
                print(f"  🏆 {name}")
        
        print("\n" + "=" * 60)
        
        # Next Steps
        if len(completed) < total:
            print(colorize("\n💡 Keep Going!", "green"))
            print(f"   {total - len(completed)} problems remaining")
            print(f"   Run: python scripts/progress_tracker.py --detailed")
        else:
            print(colorize("\n🎉 CONGRATULATIONS! All problems completed!", "green"))
        
        print()
    
    def export_progress(self, output_file: str) -> None:
        """Export progress data to JSON file."""
        completed = self._check_completed_problems()
        
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "total_problems": len(self.problems),
            "completed_count": len(completed),
            "completion_rate": len(completed) / len(self.problems) if self.problems else 0,
            "completed_problems": completed,
            "streak": self.progress_data["streak_data"],
            "achievements": self.progress_data["achievements"],
            "attempts": self.progress_data["attempts"],
        }
        
        Path(output_file).write_text(json.dumps(export_data, indent=2), encoding="utf-8")
        print(colorize(f"✅ Progress exported to {output_file}", "green"))


def main() -> None:
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Track your interview prep progress")
    parser.add_argument("--detailed", "-d", action="store_true", help="Show detailed breakdown by topic")
    parser.add_argument("--export", "-e", type=str, help="Export progress to JSON file")
    parser.add_argument("--mark-complete", "-m", type=str, help="Mark a problem as complete (problem ID)")
    
    args = parser.parse_args()
    
    tracker = ProgressTracker()
    
    if args.mark_complete:
        tracker.update_progress(args.mark_complete, solved=True)
        print(colorize(f"✅ Marked {args.mark_complete} as complete!", "green"))
    
    if args.export:
        tracker.export_progress(args.export)
    else:
        tracker.display_progress(detailed=args.detailed)


if __name__ == "__main__":
    main()
