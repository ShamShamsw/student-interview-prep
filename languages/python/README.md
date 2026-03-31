# Python Interview Prep

Python is the primary language track in this repository. If you are unsure where to start, start here.

This track includes:
- Canonical interview problems
- Beginner projects with step-by-step guidance
- Mini-projects to practice design and implementation speed
- Larger guided projects with starter/final structure

## Quick Start

Prerequisites:
- Python 3.10+
- Git

From the repository root:

```powershell
.\setup.ps1
pytest languages/python/problems/tests/test_core_algorithms.py
```

If you prefer manual setup:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

## What To Practice First

Suggested order:

1. Core problems in `problems/` (build pattern recognition).
2. Beginner projects in `beginner-projects/` (build from a blank file with comments and planning).
3. Mini-projects in `mini-projects/` (build speed and architecture discipline).
4. Full projects in `projects/` (integrate testing, structure, and documentation).

## Folder Map

```text
languages/python/
	problems/             # Interview problems and canonical solutions
	problems/tests/       # Pytest harness for problem validation
	beginner-projects/    # Guided, comment-first build projects
	mini-projects/        # Short practical implementation projects
	projects/             # Larger guided projects with starter/final versions
```

## How To Work Through A Problem

1. Read the prompt and examples carefully.
2. Write expected behavior in plain language first.
3. Implement a correct baseline solution.
4. Optimize only after correctness is verified.
5. Record time and space complexity.
6. Run tests and verify edge cases.

## Testing And Quality Commands

From the repository root:

```powershell
pytest
ruff check .
black .
```

## Contribution Guidelines (Python)

When adding or updating Python content:
- Follow naming conventions already used in each folder.
- Keep explanations short and practical.
- Include tests for executable logic.
- Keep notebooks focused on one topic and one learning goal.
- Match existing project layout patterns (for example: split models/operations/storage for multi-file apps).

For full contribution policy, see [CONTRIBUTING.md](../../CONTRIBUTING.md).
