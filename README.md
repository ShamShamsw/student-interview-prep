# Student Interview Prep

A comprehensive career guidance and technical interview preparation resource — 35+ coding problems across Python and JavaScript, practical projects, career path guidance, and structured learning paths for 10+ tech career tracks.

## Quick Start

```powershell
git clone https://github.com/ShamShamsw/student-interview-prep.git
cd student-interview-prep
.\setup.ps1
```

Run your first test:

```powershell
pytest languages/python/problems/tests/test_core_algorithms.py
```

See the [Quick Start Guide](docs/QUICKSTART.md) for manual setup, Docker, and troubleshooting.

---

## What's Inside

### Career Guidance

Start here if you're unsure which tech career to pursue:

- **[Career Paths Guide](learn/guides/CAREER_PATHS.md)** — comprehensive overview of 10+ tech careers with day-to-day work, skills needed, salary ranges, and how to get started
- **[Data Science Guide](learn/guides/DATA_SCIENCE_GUIDE.md)** — deep dive into the data science career track
- **[IDE Setup Guide](learn/guides/IDE_SETUP_GUIDE.md)** — setting up your development environment

### Coding Problems (35+)

Problems available in both Python ([`languages/python/problems/`](languages/python/problems/)) and JavaScript ([`languages/javascript/`](languages/javascript/)) with matching solutions and tests.

| Topic | Problems | Difficulty |
| Arrays & Hashing | 01–10 | Easy–Medium |
| Sliding Window | 11–14 | Medium–Hard |
| Two Pointers | 15–18 | Easy–Medium |
| Binary Search | 19–23 | Medium |
| Intervals | 24–25 | Medium |
| Linked Lists | 26–28 | Easy–Medium |
| Trees | 29–31 | Medium |
| Graphs | 32–33 | Medium |
| Heap / DP | 34–35 | Medium |

### Projects

Four hands-on projects in [`languages/python/projects/`](languages/python/projects/), each with starter code, a final solution, and a walkthrough notebook:

- **Sample Todo App** — best practices demo
- **Study Session Tracker** — time management tool
- **Interview Patterns API** — REST API with algorithm patterns
- **Interview Prep Capstone** — full-stack interview tracking app

### Beginner Projects (30 min – 4 hours each)

Plan-first, comment-heavy projects in [`languages/python/beginner-projects/`](languages/python/beginner-projects/) for those who know basic Python but haven't built anything from scratch yet:

- **Greeting Generator** — string formatting, conditionals, planning comments (30–45 min)
- **Quiz Game** — lists, dicts, functions, docstrings (45–75 min)
- **Contact Book** — CRUD, JSON persistence, architecture comments (1–1.5 hr)
- **Expense Tracker** — aggregation, formatted output, algorithm comments (1–2 hr)
- **Student Grade Report** — CSV processing, full documentation (1.5–2 hr)
- **Library Management System** — multi-entity data, multi-file architecture (2.5–4 hr)

### Mini-Projects (1–2 hours each)

Quick-build exercises in [`languages/python/mini-projects/`](languages/python/mini-projects/) that bridge the gap between individual problems and full projects:

- **LRU Cache** — hash map + linked list (classic interview design)
- **Markdown Link Checker** — file I/O, regex, HTTP requests
- **Rate Limiter** — sliding window, decorators
- **Stack Calculator** — expression parsing, stack operations
- **Word Frequency Counter** — hash maps, sorting, CLI
- **Excel Data Analysis** — pandas, data cleaning, business insights
- **Exploratory Data Analysis** — statistical analysis, visualization
- **SQL Analytics** — database queries, business reporting

### SQL Problems

10 SQL interview problems in [`languages/sql/`](languages/sql/) covering queries from basic SELECTs to window functions and self-joins.

### Learning Resources

Guides, cheatsheets, and study plans in [`learn/`](learn/):

**Study Plans & Guidance:**
- [Career Paths Guide](learn/guides/CAREER_PATHS.md) — choose your tech career track with confidence
- [Beginner Start Here](learn/guides/BEGINNER_START_HERE.md) — 2-week daily plan for newcomers
- [Learning Path](learn/paths/LEARNING_PATH.md) — 8-week and 12-week structured tracks
- [Mock Interview Guide](learn/guides/MOCK_INTERVIEW_GUIDE.md) — practice like the real thing
- [System Design Basics](learn/guides/SYSTEM_DESIGN_BASICS.md) — architecture fundamentals

**Cheatsheets:**
- [Python Cheatsheet](learn/cheatsheets/PYTHON_CHEATSHEET.md) — complexity & pattern reference
- [Data Science Cheatsheet](learn/cheatsheets/DATA_SCIENCE_CHEATSHEET.md) — pandas, NumPy, machine learning
- [SQL Analytics Cheatsheet](learn/cheatsheets/SQL_ANALYTICS_CHEATSHEET.md) — window functions, CTEs, optimization
- [Excel Formulas Cheatsheet](learn/cheatsheets/EXCEL_FORMULAS_CHEATSHEET.md) — VLOOKUP, pivot tables, data analysis

**Interview Questions by Career Track:**
- [Behavioral Interview Questions](learn/interview-questions/01-behavioral.md) — STAR method, culture fit
- [Frontend Questions](learn/interview-questions/03-frontend.md) — React, JavaScript, CSS
- [Backend Questions](learn/interview-questions/04-backend.md) — APIs, databases, system design
- [Fullstack Questions](learn/interview-questions/05-fullstack.md) — end-to-end development
- [Data Science Questions](learn/interview-questions/08-data-science.md) — statistics, ML, Python
- [Data Engineering Questions](learn/interview-questions/09-data-engineering.md) — pipelines, SQL, cloud
- [Complete List](learn/interview-questions/README.md) — all categories

**Reference:**
- [Glossary](learn/resources/GLOSSARY.md) — technical terms explained
- [External Resources](learn/resources/EXTERNAL_RESOURCES.md) — curated learning links

---

## Tools

The `scripts/` directory includes utilities to support your practice:

| Command | What it does |
|---------|--------------|
| `python scripts/progress_tracker.py` | Visual progress bars, streaks, achievements |
| `python scripts/daily_challenge.py` | Spaced-repetition daily problem selector |
| `python scripts/hints.py 01-two-sum` | Progressive 5-level hint system |
| `python scripts/achievements.py` | Unlock badges as you progress |
| `python scripts/analyze_code.py <file>` | Code quality & complexity analysis |
| `python scripts/visualize.py two-sum --array "[2,7,11,15]" --target 9` | Terminal algorithm visualization |
| Open `scripts/visualizer.html` in a browser | Interactive visual algorithm animations |

---

## Learning Paths

### New to Tech (12 weeks)
1. **[Career Paths Guide](learn/guides/CAREER_PATHS.md)** — decide which career track interests you
2. [Beginner Start Here](learn/guides/BEGINNER_START_HERE.md) — environment setup + Python basics
3. [Learning Path](learn/paths/LEARNING_PATH.md) — 12-week track
4. Problems 01–15 (Easy), then the Sample Todo App project
5. Weekly self-assessment with [Confidence Check](learn/checklists/WEEKLY_CONFIDENCE_CHECK.md)

### Interview Ready (8 weeks)
1. **[Career Paths Guide](learn/guides/CAREER_PATHS.md)** — salary negotiation & scam awareness
2. [Python Cheatsheet](learn/cheatsheets/PYTHON_CHEATSHEET.md) — review patterns
3. [Learning Path](learn/paths/LEARNING_PATH.md) — 8-week fast track
4. All 35 problems + Interview Patterns API project
5. [Mock Interviews](learn/guides/MOCK_INTERVIEW_GUIDE.md) + [System Design](learn/guides/SYSTEM_DESIGN_BASICS.md)

### Self-Paced
Browse [problems by topic](languages/python/problems/), track progress with the [checklist](learn/paths/LEARNING_PATH_CHECKLIST.md), build projects as you go.

---

## Development

**Requirements:** Python 3.10+, Git. Optional: Docker.

```powershell
pytest                              # Run all tests
pytest --cov=./ --cov-report=html   # Coverage report
ruff check .                        # Lint
black .                             # Format
python scripts/verify_setup.py      # Verify environment
```

Pre-commit hooks auto-format and lint on every commit. See [Commands Reference](docs/COMMANDS_REFERENCE.md) for the full list and [Infrastructure Setup](docs/INFRASTRUCTURE_SETUP.md) for Docker and CI details.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards.

---

## Further Reading

- [Quick Start Guide](docs/QUICKSTART.md) — setup, common tasks, troubleshooting
- [Commands Reference](docs/COMMANDS_REFERENCE.md) — every command in one place
- [Repository Structure](docs/REPOSITORY_STRUCTURE.md) — full directory map
- [FAQ](learn/guides/FAQ.md) — common questions
- [External Resources](learn/resources/EXTERNAL_RESOURCES.md) — curated links

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 ShamShamsw / Jacob Haseman.
