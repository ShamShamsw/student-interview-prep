# Student Interview Prep

A beginner-friendly repository for technical interview preparation — 35+ coding problems, practical projects, and guided learning paths in Python (with JavaScript support starting).

## Quick Start

```powershell
git clone https://github.com/ShamShamsw/student-interview-prep.git
cd student-interview-prep
.\setup.ps1
```

Run your first test:

```powershell
pytest languages/python/problems/tests/test_01_two_sum.py
```

See the [Quick Start Guide](docs/QUICKSTART.md) for manual setup, Docker, and troubleshooting.

---

## What's Inside

### Coding Problems (35+)

All problems live in [`languages/python/problems/`](languages/python/problems/) with matching solutions and tests.

| Topic | Problems | Difficulty |
|-------|----------|------------|
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

### Learning Resources

Guides, cheatsheets, and study plans in [`learn/`](learn/):

- [Beginner Start Here](learn/guides/BEGINNER_START_HERE.md) — 2-week daily plan for newcomers
- [Learning Path](learn/paths/LEARNING_PATH.md) — 8-week and 12-week structured tracks
- [Python Cheatsheet](learn/cheatsheets/PYTHON_CHEATSHEET.md) — complexity & pattern reference
- [Interview Questions](learn/interview-questions/README.md) — categorized questions by role & level
- [Mock Interview Guide](learn/guides/MOCK_INTERVIEW_GUIDE.md) — practice like the real thing
- [System Design Basics](learn/guides/SYSTEM_DESIGN_BASICS.md) — architecture fundamentals
- [Glossary](learn/resources/GLOSSARY.md) — technical terms explained

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

### Beginner (12 weeks)
1. [Beginner Start Here](learn/guides/BEGINNER_START_HERE.md) — environment setup + Python basics
2. [Learning Path](learn/paths/LEARNING_PATH.md) — 12-week track
3. Problems 01–15 (Easy), then the Sample Todo App project
4. Weekly self-assessment with [Confidence Check](learn/checklists/WEEKLY_CONFIDENCE_CHECK.md)

### Interview Ready (8 weeks)
1. [Python Cheatsheet](learn/cheatsheets/PYTHON_CHEATSHEET.md) — review patterns
2. [Learning Path](learn/paths/LEARNING_PATH.md) — 8-week fast track
3. All 35 problems + Interview Patterns API project
4. [Mock Interviews](learn/guides/MOCK_INTERVIEW_GUIDE.md) + [System Design](learn/guides/SYSTEM_DESIGN_BASICS.md)

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

MIT — see [LICENSE](LICENSE).
