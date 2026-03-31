# Student Interview Prep

A career + interview prep repository with coding practice, guided projects, and study resources for software, data, and analytics roles.

## Start in 5 Minutes

```powershell
git clone https://github.com/ShamShamsw/student-interview-prep.git
cd student-interview-prep
.\setup.ps1
pytest languages/python/problems/tests/test_core_algorithms.py
```

Need manual setup or Docker? See [Quick Start Guide](docs/QUICKSTART.md).

---

## Quick Navigation

Use this table to jump directly to what you need.

| I want to... | Go here |
|---|---|
| Pick a career direction | [Career Paths Guide](learn/guides/CAREER_PATHS.md) |
| Start as a complete beginner | [Beginner Start Here](learn/guides/BEGINNER_START_HERE.md) |
| Practice interview coding problems | [Python Problems](languages/python/problems/) / [JavaScript Track](languages/javascript/README.md) |
| Follow a structured weekly plan | [Learning Path (8/12 week)](learn/paths/LEARNING_PATH.md) |
| Build projects (beginner -> capstone) | [Python Projects Hub](languages/python/README.md) |
| Prepare for mock interviews | [Mock Interview Guide](learn/guides/MOCK_INTERVIEW_GUIDE.md) |
| Learn SQL interview patterns | [SQL Track](languages/sql/README.md) |
| Review all learning resources | [Learning Resources Index](learn/README.md) |

---

## Recommended Paths by Skill and Goal

### 1) New to Coding (Entry Level)

Start here if you are early in your coding journey.

1. [Beginner Start Here](learn/guides/BEGINNER_START_HERE.md)
2. [Python Track Overview](languages/python/README.md)
3. Beginner projects in order:
	- [01 Greeting Generator](languages/python/beginner-projects/01-greeting-generator/)
	- [02 Quiz Game](languages/python/beginner-projects/02-quiz-game/)
	- [03 Contact Book](languages/python/beginner-projects/03-contact-book/)
	- [04 Expense Tracker](languages/python/beginner-projects/04-expense-tracker/)
4. Easy coding problems: [languages/python/problems/](languages/python/problems/)
5. Weekly check-in: [Learning Path Checklist](learn/paths/LEARNING_PATH_CHECKLIST.md)

### 2) Building Core Problem-Solving Skills

Best for learners who know basic syntax and want stronger algorithm patterns.

1. [Python Cheatsheet](learn/cheatsheets/PYTHON_CHEATSHEET.md)
2. Solve problems by topic in [languages/python/problems/](languages/python/problems/)
3. Build mini-projects (1-2 hours each):
	- [01 LRU Cache](languages/python/mini-projects/01-lru-cache/)
	- [03 Rate Limiter](languages/python/mini-projects/03-rate-limiter/)
	- [04 Stack Calculator](languages/python/mini-projects/04-stack-calculator/)
4. Track progress with [scripts/progress_tracker.py](scripts/progress_tracker.py)

### 3) Interview Preparation (Job Ready)

Use this track if interviews are your primary goal.

1. [Learning Path (8-week)](learn/paths/LEARNING_PATH.md)
2. Complete all core problems in [languages/python/problems/](languages/python/problems/)
3. Build interview-focused projects:
	- [Interview Patterns API](languages/python/projects/interview-patterns-api/)
	- [Interview Prep Capstone](languages/python/projects/interview-prep-capstone/)
4. Practice with [Mock Interview Guide](learn/guides/MOCK_INTERVIEW_GUIDE.md)
5. Add [System Design Basics](learn/guides/SYSTEM_DESIGN_BASICS.md)

### 4) Data / Analytics Focus

Choose this if you are targeting data analyst, data science, or data engineering roles.

1. [Data Science Guide](learn/guides/DATA_SCIENCE_GUIDE.md)
2. [SQL Track](languages/sql/README.md) + SQL problems in [languages/sql/](languages/sql/)
3. Data-focused mini-projects:
	- [06 Excel Data Analysis](languages/python/mini-projects/06-excel-data-analysis/)
	- [07 Exploratory Data Analysis](languages/python/mini-projects/07-exploratory-data-analysis/)
	- [08 SQL Analytics](languages/python/mini-projects/08-sql-analytics/)
4. Capstone options:
	- [Data Science Capstone](languages/python/projects/data-science-capstone/)
	- [Study Session Tracker](languages/python/projects/study-session-tracker/)

---

## What's Included

### Language Tracks

- [Languages Overview](languages/README.md)
- [Python Track](languages/python/README.md)
- [JavaScript Track](languages/javascript/README.md)
- [SQL Track](languages/sql/README.md)

### Coding Problems (35+)

Available in Python and JavaScript with matching tests and reference solutions.

| Topic | Problems | Difficulty |
|---|---|---|
| Arrays & Hashing | 01-10 | Easy-Medium |
| Sliding Window | 11-14 | Medium-Hard |
| Two Pointers | 15-18 | Easy-Medium |
| Binary Search | 19-23 | Medium |
| Intervals | 24-25 | Medium |
| Linked Lists | 26-28 | Easy-Medium |
| Trees | 29-31 | Medium |
| Graphs | 32-33 | Medium |
| Heap / DP | 34-35 | Medium |

### Project Types

- Beginner projects: [languages/python/beginner-projects/](languages/python/beginner-projects/)
- Mini-projects: [languages/python/mini-projects/](languages/python/mini-projects/)
- Full projects and capstones: [languages/python/projects/](languages/python/projects/)

### Learning Resources

- [Learning Resources Index](learn/README.md)
- [Interview Questions by Track](learn/interview-questions/README.md)
- [Cheatsheets](learn/cheatsheets/)
- [Glossary](learn/resources/GLOSSARY.md)
- [External Resources](learn/resources/EXTERNAL_RESOURCES.md)

---

## Useful Scripts

| Command | Purpose |
|---|---|
| `python scripts/progress_tracker.py` | Visual progress bars, streaks, achievements |
| `python scripts/daily_challenge.py` | Daily spaced-repetition problem selector |
| `python scripts/hints.py 01-two-sum` | Progressive 5-level hints |
| `python scripts/achievements.py` | Badge and milestone tracking |
| `python scripts/analyze_code.py <file>` | Code quality and complexity analysis |
| `python scripts/visualize.py two-sum --array "[2,7,11,15]" --target 9` | Terminal algorithm visualization |
| Open `scripts/visualizer.html` in a browser | Interactive algorithm visualizations |

---

## Development and Quality

Requirements: Python 3.10+, Git (Docker optional).

```powershell
pytest                              # Run all tests
pytest --cov=./ --cov-report=html   # Coverage report
ruff check .                        # Lint
black .                             # Format
mypy --ignore-missing-imports scripts .github/scripts
pytest --no-cov tests/scripts/
python .github/scripts/check_docs_consistency.py
python scripts/verify_setup.py
```

References:

- [Commands Reference](docs/COMMANDS_REFERENCE.md)
- [Infrastructure Setup](docs/INFRASTRUCTURE_SETUP.md)
- [Repository Structure](docs/REPOSITORY_STRUCTURE.md)

---

## Contributing

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CONTRIBUTING_CHECKLIST.md](CONTRIBUTING_CHECKLIST.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

---

## License

MIT - see [LICENSE](LICENSE). Copyright (c) 2026 ShamShamsw / Jacob Haseman.
