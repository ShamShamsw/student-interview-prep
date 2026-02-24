#!/usr/bin/env python3
"""Daily Challenge System for Interview Prep.

Generates a personalized daily coding challenge based on:
- Spaced repetition algorithm
- Topics that need review
- Your skill progression
- Problems you haven't attempted

Usage:
    python scripts/daily_challenge.py
    python scripts/daily_challenge.py --difficulty easy
    python scripts/daily_challenge.py --topic arrays
"""

from __future__ import annotations

import json
import random
from datetime import datetime, timedelta
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


class DailyChallengeSystem:
    """Generate personalized daily challenges using spaced repetition."""

    def __init__(self, workspace_root: Path | None = None):
        """Initialize the daily challenge system."""
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent
        
        self.workspace_root = Path(workspace_root)
        self.problems_dir = self.workspace_root / "languages" / "python" / "problems"
        self.challenge_file = self.workspace_root / ".daily_challenge.json"
        
        self.problems = self._discover_problems()
        self.challenge_data = self._load_challenge_data()
    
    def _discover_problems(self) -> dict[str, dict[str, Any]]:
        """Discover all problems from markdown files."""
        problems = {}
        
        if not self.problems_dir.exists():
            return problems
        
        for md_file in self.problems_dir.glob("*.md"):
            if md_file.name in ["README.md", "ISSUES_SEED.md"]:
                continue
            
            problem_id = md_file.stem
            content = md_file.read_text(encoding="utf-8")
            
            # Extract problem details
            difficulty = "Medium"
            topics = []
            statement = ""
            
            lines = content.split("\n")
            for i, line in enumerate(lines[:20]):
                if line.startswith("Difficulty:"):
                    difficulty = line.split(":", 1)[1].strip()
                elif line.startswith("Topics:"):
                    topics = [t.strip() for t in line.split(":", 1)[1].split(",")]
                elif line.startswith("Statement"):
                    # Get the next few lines for statement
                    statement = "\n".join(lines[i+1:i+4]).strip()
            
            problems[problem_id] = {
                "id": problem_id,
                "name": md_file.stem.replace("-", " ").title(),
                "difficulty": difficulty,
                "topics": topics,
                "statement": statement,
                "file": str(md_file.relative_to(self.workspace_root)),
            }
        
        return problems
    
    def _load_challenge_data(self) -> dict[str, Any]:
        """Load challenge history data."""
        if self.challenge_file.exists():
            try:
                return json.loads(self.challenge_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        
        return {
            "history": [],
            "problem_stats": {},
            "last_challenge_date": None,
        }
    
    def _save_challenge_data(self) -> None:
        """Save challenge data."""
        self.challenge_file.write_text(
            json.dumps(self.challenge_data, indent=2),
            encoding="utf-8",
        )
    
    def _calculate_review_score(self, problem_id: str) -> float:
        """Calculate when a problem should be reviewed (lower = sooner).
        
        Uses spaced repetition algorithm.
        """
        if problem_id not in self.challenge_data["problem_stats"]:
            return 0.0  # Never seen, high priority
        
        stats = self.challenge_data["problem_stats"][problem_id]
        last_attempt = datetime.fromisoformat(stats["last_attempt"])
        days_since = (datetime.now() - last_attempt).days
        
        # Calculate interval based on success rate
        success_count = stats.get("success_count", 0)
        attempt_count = stats.get("attempt_count", 0)
        success_rate = success_count / attempt_count if attempt_count > 0 else 0
        
        # Spaced repetition intervals: 1, 3, 7, 14, 30 days
        if success_rate < 0.5:
            target_interval = 1  # Review frequently if struggling
        elif success_rate < 0.7:
            target_interval = 3
        elif success_rate < 0.85:
            target_interval = 7
        elif success_rate < 0.95:
            target_interval = 14
        else:
            target_interval = 30  # Mastered, review monthly
        
        # Score: negative if overdue for review, positive if not yet time
        score = target_interval - days_since
        
        return score
    
    def select_daily_challenge(
        self,
        difficulty: str | None = None,
        topic: str | None = None,
    ) -> dict[str, Any] | None:
        """Select today's challenge."""
        today = datetime.now().date().isoformat()
        
        # Check if already challenged today
        if self.challenge_data.get("last_challenge_date") == today:
            # Return today's challenge from history
            for challenge in reversed(self.challenge_data["history"]):
                if challenge["date"] == today:
                    return self.problems.get(challenge["problem_id"])
        
        # Filter problems by criteria
        candidates = []
        
        for problem_id, problem in self.problems.items():
            # Apply filters
            if difficulty and problem["difficulty"] != difficulty:
                continue
            if topic and topic not in problem["topics"]:
                continue
            
            candidates.append((problem_id, problem))
        
        if not candidates:
            return None
        
        # Score each candidate
        scored = []
        for problem_id, problem in candidates:
            # Calculate multiple factors
            review_score = self._calculate_review_score(problem_id)
            
            # Bonus for never attempted
            stats = self.challenge_data["problem_stats"].get(problem_id, {})
            novelty_bonus = 100 if not stats else 0
            
            # Slight randomness for variety
            randomness = random.uniform(-5, 5)
            
            total_score = review_score + novelty_bonus + randomness
            scored.append((total_score, problem_id, problem))
        
        # Sort by score (lower = higher priority)
        scored.sort()
        
        # Select the top problem
        selected_problem_id = scored[0][1]
        selected_problem = scored[0][2]
        
        # Record the challenge
        self.challenge_data["history"].append({
            "date": today,
            "problem_id": selected_problem_id,
            "completed": False,
        })
        self.challenge_data["last_challenge_date"] = today
        self._save_challenge_data()
        
        return selected_problem
    
    def complete_challenge(self, problem_id: str, success: bool = True) -> None:
        """Mark today's challenge as complete."""
        today = datetime.now().date().isoformat()
        
        # Update history
        for challenge in reversed(self.challenge_data["history"]):
            if challenge["date"] == today and challenge["problem_id"] == problem_id:
                challenge["completed"] = True
                challenge["success"] = success
                break
        
        # Update problem stats
        if problem_id not in self.challenge_data["problem_stats"]:
            self.challenge_data["problem_stats"][problem_id] = {
                "attempt_count": 0,
                "success_count": 0,
                "last_attempt": datetime.now().isoformat(),
            }
        
        stats = self.challenge_data["problem_stats"][problem_id]
        stats["attempt_count"] += 1
        if success:
            stats["success_count"] += 1
        stats["last_attempt"] = datetime.now().isoformat()
        
        self._save_challenge_data()
    
    def display_challenge(self, problem: dict[str, Any] | None) -> None:
        """Display today's challenge."""
        if not problem:
            print(colorize("❌ No problems found matching criteria", "red"))
            return
        
        print(colorize("\n⭐ TODAY'S CHALLENGE ⭐\n", "bold"))
        print("=" * 60)
        
        print(colorize(f"\n📝 {problem['name']}", "cyan"))
        print(f"   Problem ID: {problem['id']}")
        print(f"   Difficulty: {colorize(problem['difficulty'], self._difficulty_color(problem['difficulty']))}")
        print(f"   Topics: {', '.join(problem['topics'])}")
        
        if problem.get("statement"):
            print(colorize("\n📖 Description:", "yellow"))
            print(f"   {problem['statement']}")
        
        print(colorize("\n📂 Files:", "yellow"))
        print(f"   Problem: {problem['file']}")
        print(f"   Solution: languages/python/problems/solutions/{problem['id']}.py")
        print(f"   Test: languages/python/problems/tests/test_{problem['id'].replace('-', '_')}.py")
        
        # Show stats if available
        if problem["id"] in self.challenge_data["problem_stats"]:
            stats = self.challenge_data["problem_stats"][problem["id"]]
            success_rate = stats["success_count"] / stats["attempt_count"] * 100
            print(colorize("\n📊 Your Stats:", "yellow"))
            print(f"   Attempts: {stats['attempt_count']}")
            print(f"   Success Rate: {success_rate:.0f}%")
            
            last = datetime.fromisoformat(stats["last_attempt"])
            days_ago = (datetime.now() - last).days
            print(f"   Last Attempt: {days_ago} days ago")
        else:
            print(colorize("\n✨ This is your first attempt at this problem!", "green"))
        
        print("\n" + "=" * 60)
        print(colorize("\n💡 Commands:", "cyan"))
        print("   # Start working on the problem")
        print(f"   code {problem['file']}")
        print()
        print("   # Run tests")
        print(f"   pytest languages/python/problems/tests/test_{problem['id'].replace('-', '_')}.py")
        print()
        print("   # Mark as complete when done")
        print(f"   python scripts/daily_challenge.py --complete {problem['id']} --success")
        print()
    
    def _difficulty_color(self, difficulty: str) -> str:
        """Get color for difficulty."""
        colors = {
            "Easy": "green",
            "Medium": "yellow",
            "Hard": "red",
        }
        return colors.get(difficulty, "reset")
    
    def show_history(self, days: int = 7) -> None:
        """Show challenge history."""
        print(colorize(f"\n📅 Challenge History (Last {days} Days)\n", "bold"))
        
        recent = [
            c for c in self.challenge_data["history"]
            if (datetime.now().date() - datetime.fromisoformat(c["date"]).date()).days < days
        ]
        
        if not recent:
            print("No recent challenges")
            return
        
        for challenge in reversed(recent):
            date = challenge["date"]
            problem_id = challenge["problem_id"]
            problem_name = self.problems.get(problem_id, {}).get("name", problem_id)
            
            if challenge.get("completed"):
                status = "✅" if challenge.get("success", True) else "❌"
            else:
                status = "⏳"
            
            print(f"{status} {date} - {problem_name}")
        
        # Stats
        completed = sum(1 for c in recent if c.get("completed"))
        success = sum(1 for c in recent if c.get("completed") and c.get("success", True))
        
        print(colorize(f"\n📊 Stats:", "cyan"))
        print(f"   Challenges: {len(recent)}")
        print(f"   Completed: {completed}/{len(recent)}")
        if completed > 0:
            print(f"   Success Rate: {success/completed*100:.0f}%")


def main() -> None:
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate your daily coding challenge")
    parser.add_argument("--difficulty", "-d", choices=["Easy", "Medium", "Hard"], help="Filter by difficulty")
    parser.add_argument("--topic", "-t", type=str, help="Filter by topic (e.g., arrays, trees)")
    parser.add_argument("--complete", "-c", type=str, help="Mark problem as complete (problem ID)")
    parser.add_argument("--success", "-s", action="store_true", help="Mark completion as successful")
    parser.add_argument("--history", action="store_true", help="Show challenge history")
    
    args = parser.parse_args()
    
    system = DailyChallengeSystem()
    
    if args.complete:
        system.complete_challenge(args.complete, success=args.success)
        print(colorize(f"✅ Marked {args.complete} as complete!", "green"))
        return
    
    if args.history:
        system.show_history()
        return
    
    # Generate and display today's challenge
    challenge = system.select_daily_challenge(
        difficulty=args.difficulty,
        topic=args.topic,
    )
    
    system.display_challenge(challenge)


if __name__ == "__main__":
    main()
