from __future__ import annotations

from scripts.daily_challenge import DailyChallengeSystem
from scripts.hints import HintSystem, colorize as hints_colorize
from scripts.progress_tracker import progress_bar


def test_progress_bar_handles_zero_total() -> None:
    output = progress_bar(completed=0, total=0, width=10)
    assert output == "[          ] 0%"


def test_progress_bar_contains_percentage_for_non_zero_total() -> None:
    output = progress_bar(completed=3, total=4, width=10)
    assert "75.0%" in output


def test_hints_colorize_adds_reset_code() -> None:
    output = hints_colorize("test", "green")
    assert output.endswith("\033[0m")
    assert "test" in output


def test_hint_system_loads_default_hints(tmp_path) -> None:
    system = HintSystem(workspace_root=tmp_path)
    assert "01-two-sum" in system.hints_db
    assert system.hints_file.exists()


def test_daily_challenge_returns_none_for_missing_problem_set(tmp_path) -> None:
    system = DailyChallengeSystem(workspace_root=tmp_path)
    challenge = system.select_daily_challenge()
    assert challenge is None
