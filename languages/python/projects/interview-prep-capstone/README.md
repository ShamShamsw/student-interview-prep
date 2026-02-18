# Interview Prep Platform Capstone (8-12 Weeks)

Build a production-style interview prep platform using Python where users can practice problems, track progress, and receive algorithm-focused feedback.

## Duration and workload

- Expected duration: **8-12 weeks**
- Recommended pace: **6-10 focused hours/week**
- Cadence: **2-week sprints** (4 to 6 total)

## Why this capstone

This capstone is designed to bridge "problem solving" and "real software engineering":
- architecture and tradeoffs
- iterative delivery with Agile sprints
- testing and CI discipline
- using AI and docs responsibly when stuck

## Prerequisites

- Python 3.11+
- Basic SQL and REST API knowledge
- Comfort with Git and branching
- Familiarity with your existing problems/projects in this repo

## What you will build

A backend-first platform with API endpoints for:
- user progress tracking
- problem attempts and outcomes
- spaced-review scheduling
- study plans and recommendations
- insights dashboard data

## Project structure

- `docs/01-design-and-architecture.md` — architecture principles before coding
- `docs/02-sprint-plan-agile.md` — 8-12 week sprint blueprint
- `docs/03-ai-and-resource-playbook.md` — how to get unstuck effectively
- `starter/` — scaffold with TODOs
- `final/` — target implementation shape and reference patterns
- `tests/` — permanent endpoint tests for final API behavior
- `walkthrough.ipynb` — guided execution plan
- `requirements.txt` — core dependencies for backend and tests

## Learning outcomes

By the end you should be able to:
- design service boundaries and data models intentionally
- break complex products into iterative sprint deliverables
- maintain quality gates with tests + CI
- use AI as a force multiplier without losing engineering judgment

## Build order (must follow)

1. Read `docs/01-design-and-architecture.md`.
2. Read `docs/02-sprint-plan-agile.md` and commit to a schedule.
3. Read `docs/03-ai-and-resource-playbook.md`.
4. Implement starter milestones sprint by sprint.
5. Compare decisions with `final/` reference.

## Definition of done

- Core API modules implemented and tested
- Regression tests and CI passing
- Architecture decision notes documented
- Weekly sprint review notes captured
- Postmortem completed with "what I would do next"

## Run tests

From `interview-prep-capstone/`:

```bash
python -m pytest tests -q
```

## Debug failing CI tests

When GitHub Actions fails on tests, use this checklist:

1. Re-run locally from `interview-prep-capstone/`:

	```bash
	python -m pytest tests -vv
	```

2. Compare local Python version with CI matrix (`3.10`, `3.11`, `3.12`).
3. Confirm dependencies are current:

	```bash
	python -m pip install -r requirements.txt
	```

4. Reproduce the exact failing test by node id (from CI logs), for example:

	```bash
	python -m pytest tests/test_endpoints.py::test_recommendations_prioritize_weaker_topic -vv
	```

5. Check for shared mutable state between tests (`ATTEMPTS`, `STUDY_PLANS`) and ensure reset in setup.
6. Commit only after local tests pass and behavior is understood.
