# Beginner Project 15: Interactive Math Tutor Notebook

**Time:** 3-5 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** symbolic math problem generation, solution explanation, performance tracking, and session artifacts

---

## Why This Project?

Learning mathematics requires both practice and clear explanations of solving steps.
This project gives you a practical beginner workflow where you can:

- generate diverse math problems at multiple difficulty levels,
- provide step-by-step symbolic solutions and explanations,
- track learning progress across problem categories,
- and save reproducible session artifacts for review and improvement.

---

## Separate Repository

This project is currently maintained in this monorepo.

---

## What You Will Build

You will build a command-line interactive math tutoring system that:

1. Generates symbolic math problems spanning beginner, intermediate, and advanced difficulty levels.
2. Presents problems with automatic solving simulation.
3. Provides step-by-step solution explanations for each problem.
4. Tracks accuracy, solve time, and performance by problem category.
5. Computes aggregate performance statistics and category breakdowns.
6. Saves session metadata and problem records to JSON for learning analysis.

---

## Requirements

- Python 3.11+
- `sympy`

Install with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
  INTERACTIVE MATH TUTOR - SYMBOLIC PROBLEM SOLVING + EXPLANATIONS
======================================================================

Configuration:
  Session difficulty: beginner
  Problems to solve: 5
  Problem categories: algebra, geometry
  Show step-by-step: True

Available difficulty levels:
  - beginner: Basic arithmetic and simple algebraic equations
  - intermediate: Quadratic equations and polynomial problems
  - advanced: Systems of equations and calculus concepts

Session behavior:
  1) Generate symbolic math problems at your chosen difficulty.
  2) Solve each problem and provide step-by-step explanations.
  3) Track accuracy, time-to-solve, and learning progress.

Session summary:
  Status: completed
  Difficulty: beginner
  Problems completed: 5/5
  Accuracy: 100.0%
  Average solve time: 34.8s
  Total session time: 174.1s
  Category breakdown:
    algebra: 5/5 correct (100%)
Saved run artifact: data/runs/latest_math_tutor_session.json
```

---

## Build Order

Follow this order for clean architecture:

1. `storage.py`
2. `models.py`
3. `operations.py`
4. `display.py`
5. `main.py`

---

## File Responsibilities

- `storage.py`: handles session and problem-record artifact persistence in `data/runs/`.
- `models.py`: creates consistent payloads for configuration, problem records, difficulty levels, and session summaries.
- `operations.py`: problem generation, solution simulation, performance tracking, and session persistence.
- `display.py`: formats a readable CLI banner, startup guide, and session summary.
- `main.py`: thin orchestration entry point.

---

## Suggested Reflection Prompts

Add answers in your own notes after running the project:

- Which problem categories had the highest success rate in your session?
- How did solve time vary between difficulty levels?
- What additional features would make this an effective self-study tool?

---

## Stretch Goals

1. Add interactive mode where you can input your own answers instead of simulation.
2. Export session reports to PDF with visualizations.
3. Implement adaptive difficulty that adjusts based on accuracy.
4. Add multi-session progress tracking and learning analytics.
