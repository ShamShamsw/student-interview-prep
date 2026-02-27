#!/usr/bin/env python3
"""Achievement System for Interview Prep.

Track and display achievements, badges, and milestones.

Usage:
    python scripts/achievements.py
    python scripts/achievements.py --next
    python scripts/achievements.py --export badges.md
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Color codes
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


@dataclass
class Achievement:
    """Represents an achievement."""

    id: str
    name: str
    description: str
    icon: str
    tier: str  # Bronze, Silver, Gold, Diamond
    category: str
    condition_fn: Any
    points: int = 10


class AchievementSystem:
    """Track and manage achievements."""

    def __init__(self, workspace_root: Path | None = None):
        """Initialize achievement system."""
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent

        self.workspace_root = Path(workspace_root)
        self.progress_file = self.workspace_root / ".progress_data.json"
        self.achievement_file = self.workspace_root / ".achievements.json"

        self.progress_data = self._load_progress()
        self.achievement_data = self._load_achievements()
        self.achievements = self._define_achievements()

    def _load_progress(self) -> dict[str, Any]:
        """Load progress data."""
        if self.progress_file.exists():
            try:
                return json.loads(self.progress_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"completed": [], "streak_data": {"current": 0, "best": 0}}

    def _load_achievements(self) -> dict[str, Any]:
        """Load achievement data."""
        if self.achievement_file.exists():
            try:
                return json.loads(self.achievement_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"unlocked": [], "progress": {}, "total_points": 0}

    def _save_achievements(self) -> None:
        """Save achievement data."""
        self.achievement_file.write_text(
            json.dumps(self.achievement_data, indent=2),
            encoding="utf-8",
        )

    def _define_achievements(self) -> list[Achievement]:
        """Define all available achievements."""
        completed_count = len(self.progress_data.get("completed", []))
        self.progress_data.get("streak_data", {}).get("current", 0)
        best_streak = self.progress_data.get("streak_data", {}).get("best", 0)

        return [
            # Getting Started
            Achievement(
                "first_solve",
                "First Steps",
                "Solved your first problem!",
                "🌟",
                "Bronze",
                "Getting Started",
                lambda: completed_count >= 1,
                10,
            ),
            Achievement(
                "five_solved",
                "Getting Started",
                "Solved 5 problems!",
                "🔰",
                "Bronze",
                "Getting Started",
                lambda: completed_count >= 5,
                25,
            ),
            Achievement(
                "ten_solved",
                "Warming Up",
                "Solved 10 problems!",
                "📈",
                "Silver",
                "Getting Started",
                lambda: completed_count >= 10,
                50,
            ),
            Achievement(
                "twenty_solved",
                "Making Progress",
                "Solved 20 problems!",
                "💪",
                "Silver",
                "Getting Started",
                lambda: completed_count >= 20,
                100,
            ),
            Achievement(
                "all_solved",
                "Master",
                "Solved all 35 problems!",
                "🏅",
                "Gold",
                "Getting Started",
                lambda: completed_count >= 35,
                500,
            ),
            # Streaks
            Achievement(
                "streak_3",
                "Consistent",
                "Maintain a 3-day streak!",
                "🔥",
                "Bronze",
                "Streaks",
                lambda: best_streak >= 3,
                30,
            ),
            Achievement(
                "streak_7",
                "Dedicated",
                "Maintain a 7-day streak!",
                "⚡",
                "Silver",
                "Streaks",
                lambda: best_streak >= 7,
                70,
            ),
            Achievement(
                "streak_30",
                "Unstoppable",
                "Maintain a 30-day streak!",
                "🚀",
                "Gold",
                "Streaks",
                lambda: best_streak >= 30,
                300,
            ),
            Achievement(
                "streak_100",
                "Legend",
                "Maintain a 100-day streak!",
                "💎",
                "Diamond",
                "Streaks",
                lambda: best_streak >= 100,
                1000,
            ),
            # Speed Challenges
            Achievement(
                "speed_demon",
                "Speed Demon",
                "Solve 5 problems in one day!",
                "⚡",
                "Silver",
                "Speed",
                lambda: False,  # TODO: Track this
                100,
            ),
            Achievement(
                "marathon",
                "Marathon Runner",
                "Solve 10 problems in one week!",
                "🏃",
                "Gold",
                "Speed",
                lambda: False,  # TODO: Track this
                200,
            ),
        ]

    def check_achievements(self) -> list[Achievement]:
        """Check for newly unlocked achievements."""
        newly_unlocked = []

        for achievement in self.achievements:
            if achievement.id not in self.achievement_data["unlocked"]:
                try:
                    if achievement.condition_fn():
                        self.achievement_data["unlocked"].append(achievement.id)
                        self.achievement_data["total_points"] += achievement.points
                        newly_unlocked.append(achievement)
                except Exception:
                    pass

        if newly_unlocked:
            self._save_achievements()

        return newly_unlocked

    def display_achievements(self, show_locked: bool = True) -> None:
        """Display all achievements."""
        newly_unlocked = self.check_achievements()

        # Show newly unlocked
        if newly_unlocked:
            print(colorize("\n🎉 NEW ACHIEVEMENTS UNLOCKED!\n", "yellow"))
            for achievement in newly_unlocked:
                print(
                    f"{achievement.icon} {colorize(achievement.name, 'green')} (+{achievement.points} pts)"
                )
                print(f"   {achievement.description}\n")

        print(colorize("\n🏆 YOUR ACHIEVEMENTS\n", "bold"))
        print("=" * 70)

        # Group by category
        by_category = {}
        for achievement in self.achievements:
            if achievement.category not in by_category:
                by_category[achievement.category] = []
            by_category[achievement.category].append(achievement)

        # Display by category
        for category, achievements in by_category.items():
            print(colorize(f"\n{category}", "cyan"))

            for achievement in achievements:
                is_unlocked = achievement.id in self.achievement_data["unlocked"]

                if is_unlocked:
                    print(
                        f"  ✅ {achievement.icon} {colorize(achievement.name, 'green')} [{achievement.tier}]"
                    )
                    print(
                        f"      {achievement.description} (+{achievement.points} pts)"
                    )
                elif show_locked:
                    print(
                        f"  🔒 ❓ {colorize(achievement.name, 'reset')} [{achievement.tier}]"
                    )
                    print(
                        f"      {achievement.description} (+{achievement.points} pts)"
                    )

        # Summary
        unlocked_count = len(self.achievement_data["unlocked"])
        total_count = len(self.achievements)
        total_points = self.achievement_data["total_points"]

        print("\n" + "=" * 70)
        print(
            colorize(
                f"\n📊 Progress: {unlocked_count}/{total_count} achievements unlocked",
                "cyan",
            )
        )
        print(colorize(f"🎯 Total Points: {total_points}", "yellow"))

        completion_pct = (unlocked_count / total_count * 100) if total_count > 0 else 0
        print(f"💫 Completion: {completion_pct:.1f}%")

        # Rank
        rank = self._calculate_rank(total_points)
        print(colorize(f"\n🏅 Current Rank: {rank}", "green"))
        print()

    def _calculate_rank(self, points: int) -> str:
        """Calculate rank based on points."""
        if points >= 1000:
            return "💎 Diamond"
        elif points >= 500:
            return "🥇 Gold"
        elif points >= 200:
            return "🥈 Silver"
        elif points >= 50:
            return "🥉 Bronze"
        else:
            return "🌱 Beginner"

    def show_next_achievements(self) -> None:
        """Show next achievable achievements."""
        print(colorize("\n🎯 NEXT ACHIEVEMENTS\n", "bold"))
        print("=" * 70)

        # Find locked achievements that are close to unlocking
        completed_count = len(self.progress_data.get("completed", []))

        next_milestones = [
            ("first_solve", 1, completed_count),
            ("five_solved", 5, completed_count),
            ("ten_solved", 10, completed_count),
            ("twenty_solved", 20, completed_count),
            ("all_solved", 35, completed_count),
        ]

        for achievement_id, target, current in next_milestones:
            achievement = next(
                (a for a in self.achievements if a.id == achievement_id), None
            )

            if achievement and achievement_id not in self.achievement_data["unlocked"]:
                remaining = target - current
                print(f"\n{achievement.icon} {colorize(achievement.name, 'yellow')}")
                print(f"   {achievement.description}")
                print(f"   Progress: {current}/{target} problems")
                if remaining > 0:
                    print(colorize(f"   🎯 {remaining} more to unlock!", "cyan"))
                break

        print()

    def export_badges(self, output_file: str) -> None:
        """Export badges to markdown file."""
        lines = ["# 🏆 My Achievements\n"]
        lines.append(
            f"*Earned {len(self.achievement_data['unlocked'])} achievements*\n"
        )
        lines.append(f"*Total Points: {self.achievement_data['total_points']}*\n")
        lines.append("\n---\n\n")

        for achievement in self.achievements:
            if achievement.id in self.achievement_data["unlocked"]:
                lines.append(f"## {achievement.icon} {achievement.name}\n")
                lines.append(f"*{achievement.description}*\n")
                lines.append(
                    f"**Tier:** {achievement.tier} | **Points:** {achievement.points}\n\n"
                )

        Path(output_file).write_text("".join(lines), encoding="utf-8")
        print(colorize(f"✅ Badges exported to {output_file}", "green"))


def main() -> None:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="View your achievements")
    parser.add_argument(
        "--next", "-n", action="store_true", help="Show next achievements"
    )
    parser.add_argument(
        "--export", "-e", type=str, help="Export badges to markdown file"
    )
    parser.add_argument(
        "--hide-locked", action="store_true", help="Hide locked achievements"
    )

    args = parser.parse_args()

    system = AchievementSystem()

    if args.next:
        system.show_next_achievements()
    elif args.export:
        system.export_badges(args.export)
    else:
        system.display_achievements(show_locked=not args.hide_locked)


if __name__ == "__main__":
    main()
