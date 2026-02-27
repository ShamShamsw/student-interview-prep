# Repository Structure

Overview of how the project is organized and where to find things.

```
student-interview-prep/
│
├── languages/                         # All coding content
│   ├── python/
│   │   ├── problems/                  # 35+ coding problems
│   │   │   ├── 01-two-sum.md          # Problem descriptions (.md)
│   │   │   ├── ...
│   │   │   ├── 35-coin-change.md
│   │   │   ├── solutions/             # Solution files (.py)
│   │   │   └── tests/                 # Test files + harness
│   │   └── projects/                  # Practical projects
│   │       ├── sample-to-do-app/
│   │       ├── study-session-tracker/
│   │       ├── interview-patterns-api/
│   │       └── interview-prep-capstone/
│   └── javascript/
│       ├── solutions/                 # JS solutions (2 available)
│       └── tests/                     # Jest test files
│
├── learn/                             # Learning materials
│   ├── guides/                        # Step-by-step guides
│   │   ├── BEGINNER_START_HERE.md     # 2-week beginner plan
│   │   ├── FAQ.md                     # Common questions
│   │   ├── IDE_SETUP_GUIDE.md         # Editor configuration
│   │   ├── INTERVIEW_QUESTIONS.md     # Behavioral prep
│   │   ├── MOCK_INTERVIEW_GUIDE.md    # Interview practice
│   │   └── SYSTEM_DESIGN_BASICS.md    # Architecture intro
│   ├── paths/                         # Structured learning tracks
│   │   ├── LEARNING_PATH.md           # 8-week & 12-week plans
│   │   ├── LEARNING_PATH_CHECKLIST.md # Progress checklist
│   │   └── ROADMAP.md                 # Project roadmap
│   ├── cheatsheets/
│   │   └── PYTHON_CHEATSHEET.md       # Patterns & complexity
│   ├── checklists/
│   │   └── WEEKLY_CONFIDENCE_CHECK.md # Self-assessment
│   └── resources/
│       ├── GLOSSARY.md                # Technical terms
│       └── EXTERNAL_RESOURCES.md      # Curated links
│
├── scripts/                           # Utility tools
│   ├── achievements.py                # Achievement/badge tracker
│   ├── analyze_code.py                # Code quality analysis
│   ├── daily_challenge.py             # Spaced-repetition challenges
│   ├── hints.py                       # Progressive hint system
│   ├── progress_tracker.py            # Visual progress tracking
│   ├── verify_setup.py                # Environment verification
│   ├── visualize.py                   # Terminal algorithm visualizer
│   ├── visualizer.html                # Browser algorithm visualizer
│   └── create_python_problem_issues.ps1 # GitHub issue creation
│
├── docs/                              # Extended documentation
│   ├── QUICKSTART.md                  # 5-minute setup guide
│   ├── COMMANDS_REFERENCE.md          # Complete command reference
│   ├── INFRASTRUCTURE_SETUP.md        # Dev environment details
│   └── REPOSITORY_STRUCTURE.md        # This file
│
├── docker/                            # Docker configuration
│   └── Dockerfile
│
├── .github/                           # GitHub configuration
│   ├── workflows/                     # CI/CD (6 workflows)
│   ├── ISSUE_TEMPLATE/                # Issue templates (4)
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── scripts/                       # CI helper scripts
│   └── dependabot.yml
│
├── README.md                          # Start here
├── CONTRIBUTING.md                    # How to contribute
├── CODE_OF_CONDUCT.md                 # Community standards
├── CHANGELOG.md                       # Version history
├── LICENSE                            # MIT License
├── setup.ps1                          # Automated setup
├── Makefile                           # Common dev commands
├── pytest.ini                         # Test configuration
├── ruff.toml                          # Linter configuration
├── requirements-dev.txt               # Python dev dependencies
├── docker-compose.yml                 # Docker Compose config
└── .gitignore, .yamllint, etc.        # Dotfiles
```

---

## Quick Navigation

### I want to...

**Learn to code:**
- Start: [BEGINNER_START_HERE.md](../learn/guides/BEGINNER_START_HERE.md)
- Follow: [LEARNING_PATH.md](../learn/paths/LEARNING_PATH.md)
- Track: [LEARNING_PATH_CHECKLIST.md](../learn/paths/LEARNING_PATH_CHECKLIST.md)

**Practice problems:**
- Browse: [languages/python/problems/](../languages/python/problems/)
- Solutions: [languages/python/problems/solutions/](../languages/python/problems/solutions/)
- Test: `pytest languages/python/problems/tests/test_01_two_sum.py`

**Build projects:**
- All projects: [languages/python/projects/](../languages/python/projects/)
- API project: [interview-patterns-api/](../languages/python/projects/interview-patterns-api/)
- Capstone: [interview-prep-capstone/](../languages/python/projects/interview-prep-capstone/)

**Prepare for interviews:**
- Questions: [INTERVIEW_QUESTIONS.md](../learn/guides/INTERVIEW_QUESTIONS.md)
- Mock interviews: [MOCK_INTERVIEW_GUIDE.md](../learn/guides/MOCK_INTERVIEW_GUIDE.md)
- System design: [SYSTEM_DESIGN_BASICS.md](../learn/guides/SYSTEM_DESIGN_BASICS.md)
- Cheatsheet: [PYTHON_CHEATSHEET.md](../learn/cheatsheets/PYTHON_CHEATSHEET.md)

**Set up development environment:**
- Quick setup: [QUICKSTART.md](QUICKSTART.md)
- Full setup: [INFRASTRUCTURE_SETUP.md](INFRASTRUCTURE_SETUP.md)
- Commands: [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md)

**Contribute:**
- Guidelines: [CONTRIBUTING.md](../CONTRIBUTING.md)
- Code of conduct: [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md)

---

## Problem Categories

| # | Topic | Problems |
|---|-------|----------|
| 01–10 | Arrays & Hashing | Two Sum, Valid Parentheses, Merge Sorted Arrays, Best Time to Buy/Sell Stock, Contains Duplicate, Valid Anagram, Product of Array Except Self, Group Anagrams, Top K Frequent, Encode/Decode Strings |
| 11–14 | Sliding Window | Longest Substring Without Repeating, Longest Repeating Character Replacement, Permutation in String, Minimum Window Substring |
| 15–18 | Two Pointers | Valid Palindrome, Two Sum II, 3Sum, Container With Most Water |
| 19–23 | Binary Search | Search in Rotated Sorted Array, Find Min in Rotated Sorted Array, Binary Search, Koko Eating Bananas, Time Based Key-Value Store |
| 24–25 | Intervals | Merge Intervals, Insert Interval |
| 26–28 | Linked Lists | Reverse Linked List, Linked List Cycle, Merge Two Sorted Lists |
| 29–31 | Trees | Valid BST, Level Order Traversal, LCA of BST |
| 32–33 | Graphs | Number of Islands, Clone Graph |
| 34 | Heap | Kth Largest Element |
| 35 | Dynamic Programming | Coin Change |

---

## File Naming Conventions

- **Problem descriptions:** `##-problem-name.md` (e.g., `01-two-sum.md`)
- **Solutions:** `##-problem-name.py` (e.g., `01-two-sum.py`)
- **Tests:** `test_##_problem_name.py` (e.g., `test_01_two_sum.py`)
- **Guides:** `UPPERCASE_NAME.md` in `learn/` subdirectories
- **Config:** Standard lowercase names at root
