# 📁 Repository Structure

Clear overview of the repository organization and where to find things.

```
student-interview-prep/
│
├── 📚 learn/                          # All learning materials
│   ├── guides/                        # Step-by-step guides
│   │   ├── BEGINNER_START_HERE.md    # Start here if new to coding!
│   │   ├── FAQ.md                     # Frequently asked questions
│   │   ├── IDE_SETUP_GUIDE.md        # Setup VS Code/PyCharm
│   │   ├── INTERVIEW_QUESTIONS.md    # Common interview questions
│   │   ├── MOCK_INTERVIEW_GUIDE.md   # Practice interviews
│   │   └── SYSTEM_DESIGN_BASICS.md   # Architecture fundamentals
│   │
│   ├── paths/                         # Structured learning tracks
│   │   ├── LEARNING_PATH.md          # 8-week & 12-week plans
│   │   └── LEARNING_PATH_CHECKLIST.md # Track your progress
│   │
│   ├── checklists/                    # Progress tracking
│   │   └── WEEKLY_CONFIDENCE_CHECK.md
│   │
│   ├── cheatsheets/                   # Quick references
│   │   └── PYTHON_CHEATSHEET.md      # Time complexity & patterns
│   │
│   └── resources/                     # Additional materials
│       ├── GLOSSARY.md                # Technical terms explained
│       └── EXTERNAL_RESOURCES.md      # Curated external links
│
├── 💻 languages/python/               # Python-specific content
│   ├── problems/                      # 35+ coding problems
│   │   ├── 01-two-sum.md             # Problem descriptions
│   │   ├── 02-valid-parentheses.md
│   │   ├── ...                        # 03-35 more problems
│   │   │
│   │   ├── solutions/                 # Solutions to problems
│   │   │   ├── 01-two-sum.py
│   │   │   ├── 02-valid-parentheses.py
│   │   │   └── ...
│   │   │
│   │   └── tests/                     # Test files
│   │       ├── test_01_two_sum.py
│   │       ├── test_02_valid_parentheses.py
│   │       └── harness.py             # Test utilities
│   │
│   └── projects/                      # Practical projects
│       ├── interview-patterns-api/    # REST API project
│       ├── interview-prep-capstone/   # Full-stack app
│       ├── sample-to-do-app/          # Best practices demo
│       └── study-session-tracker/     # Time tracking tool
│
├── 🔧 .github/                        # GitHub configuration
│   ├── workflows/                     # CI/CD pipelines
│   │   ├── ci.yml                     # Main CI workflow
│   │   ├── python-tests.yml           # Python tests
│   │   ├── yaml-lint.yml              # YAML validation
│   │   └── actions-smoke-test.yml     # Actions validation
│   │
│   ├── ISSUE_TEMPLATE/                # Issue templates
│   ├── PULL_REQUEST_TEMPLATE.md       # PR template
│   └── dependabot.yml                 # Automated updates
│
├── 🐳 docker/                         # Docker configuration
│   └── Dockerfile                     # Dev environment image
│
├── 📝 scripts/                        # Utility scripts
│   ├── verify_setup.py                # Environment verification
│   └── create_python_problem_issues.ps1
│
├── 📋 Configuration Files
│   ├── .pre-commit-config.yaml        # Pre-commit hooks
│   ├── .gitignore                     # Git ignore rules
│   ├── .dockerignore                  # Docker ignore rules
│   ├── .yamllint                      # YAML linting config
│   ├── pytest.ini                     # Pytest configuration
│   ├── ruff.toml                      # Ruff linter config
│   ├── docker-compose.yml             # Docker Compose setup
│   ├── Makefile                       # Make commands
│   ├── requirements-dev.txt           # Dev dependencies
│   └── setup.ps1                      # Automated setup script
│
└── 📖 Documentation
    ├── README.md                      # Main entry point (start here!)
    ├── QUICKSTART.md                  # 5-minute setup guide
    ├── COMMANDS_REFERENCE.md          # All available commands
    ├── INFRASTRUCTURE_SETUP.md        # Detailed dev setup
    ├── REPOSITORY_STRUCTURE.md        # This file!
    ├── CONTRIBUTING.md                # Contribution guide
    ├── CODE_OF_CONDUCT.md             # Community standards
    ├── CHANGELOG.md                   # Version history
    ├── ROADMAP_Version2.md            # Future plans
    └── LICENSE_Version2.txt           # MIT License
```

---

## 🗺️ Quick Navigation

### I want to...

#### Learn to Code
- 👉 Start: [learn/guides/BEGINNER_START_HERE.md](learn/guides/BEGINNER_START_HERE.md)
- 📅 Follow: [learn/paths/LEARNING_PATH.md](learn/paths/LEARNING_PATH.md)
- ✅ Track: [learn/paths/LEARNING_PATH_CHECKLIST.md](learn/paths/LEARNING_PATH_CHECKLIST.md)

#### Practice Problems
- 📁 Browse: [languages/python/problems/](languages/python/problems/)
- 🧪 Test: `pytest languages/python/problems/tests/test_01_two_sum.py`
- 💡 Solutions: [languages/python/problems/solutions/](languages/python/problems/solutions/)

#### Build Projects
- 🏗️ Projects: [languages/python/projects/](languages/python/projects/)
- 🌐 API Project: [languages/python/projects/interview-patterns-api/](languages/python/projects/interview-patterns-api/)
- 📱 Capstone: [languages/python/projects/interview-prep-capstone/](languages/python/projects/interview-prep-capstone/)

#### Prepare for Interviews
- 💬 Questions: [learn/guides/INTERVIEW_QUESTIONS.md](learn/guides/INTERVIEW_QUESTIONS.md)
- 🎭 Mock Interviews: [learn/guides/MOCK_INTERVIEW_GUIDE.md](learn/guides/MOCK_INTERVIEW_GUIDE.md)
- 🏛️ System Design: [learn/guides/SYSTEM_DESIGN_BASICS.md](learn/guides/SYSTEM_DESIGN_BASICS.md)
- 📖 Cheatsheet: [learn/cheatsheets/PYTHON_CHEATSHEET.md](learn/cheatsheets/PYTHON_CHEATSHEET.md)

#### Setup Development Environment
- 🚀 Quick Setup: [QUICKSTART.md](QUICKSTART.md)
- 🔧 Full Setup: [INFRASTRUCTURE_SETUP.md](INFRASTRUCTURE_SETUP.md)
- 📝 Commands: [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md)
- ✅ Verify: `python scripts/verify_setup.py`

#### Contribute
- 🤝 Guidelines: [CONTRIBUTING.md](CONTRIBUTING.md)
- 📜 Code of Conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- 🗺️ Roadmap: [ROADMAP_Version2.md](ROADMAP_Version2.md)

---

## 📊 Problem Categories

Problems are organized by topic and difficulty:

### Arrays & Hashing (01-10)
- Two Sum, Valid Anagram, Contains Duplicate
- Group Anagrams, Top K Frequent Elements
- Product of Array Except Self, Encode/Decode Strings

### Sliding Window (11-14)
- Longest Substring Without Repeating Characters
- Longest Repeating Character Replacement
- Permutation in String, Minimum Window Substring

### Two Pointers (15-18)
- Valid Palindrome, Two Sum II
- 3Sum, Container With Most Water

### Binary Search (19-23)
- Search in Rotated Sorted Array
- Find Minimum in Rotated Sorted Array
- Binary Search, Koko Eating Bananas
- Time Based Key-Value Store

### Intervals (24-25)
- Merge Intervals, Insert Interval

### Linked Lists (26-28)
- Reverse Linked List, Linked List Cycle
- Merge Two Sorted Lists

### Trees (29-31)
- Valid Binary Search Tree
- Binary Tree Level Order Traversal
- Lowest Common Ancestor of BST

### Graphs (32-33)
- Number of Islands, Clone Graph

### Heap/Priority Queue (34)
- Kth Largest Element in an Array

### Dynamic Programming (35)
- Coin Change

---

## 🎯 File Naming Conventions

### Problems
- **Description**: `##-problem-name.md` (e.g., `01-two-sum.md`)
- **Solution**: `##-problem-name.py` (e.g., `01-two-sum.py`)
- **Test**: `test_##_problem_name.py` (e.g., `test_01_two_sum.py`)

### Guides
- Markdown files in `learn/guides/`
- UPPERCASE names (e.g., `BEGINNER_START_HERE.md`)

### Configuration
- Standard names (`.gitignore`, `pytest.ini`, etc.)
- Lowercase with hyphens (e.g., `docker-compose.yml`)

---

## 🔍 Search Tips

### Find a specific problem
```powershell
# By number
Get-ChildItem -Path languages\python\problems -Filter "01-*"

# By name
Get-ChildItem -Path languages\python\problems -Filter "*two-sum*"
```

### Find all tests
```powershell
Get-ChildItem -Path . -Filter "test_*.py" -Recurse
```

### Search for code patterns
```powershell
# Find all functions
Select-String -Path .\languages\python\**\*.py -Pattern "^def "

# Find specific algorithm
Select-String -Path .\**\*.py -Pattern "binary.?search"
```

---

## 📱 Mobile-Friendly Access

Viewing on mobile? Here are the most important files:

1. **[README.md](README.md)** - Start here
2. **[QUICKSTART.md](QUICKSTART.md)** - Setup guide
3. **[BEGINNER_START_HERE.md](learn/guides/BEGINNER_START_HERE.md)** - Learning guide
4. **[LEARNING_PATH.md](learn/paths/LEARNING_PATH.md)** - Study plan
5. **[PYTHON_CHEATSHEET.md](learn/cheatsheets/PYTHON_CHEATSHEET.md)** - Quick reference

---

## 🚀 Getting Started Paths

Choose your path based on experience:

```
Complete Beginner
    → README.md
    → setup.ps1
    → learn/guides/BEGINNER_START_HERE.md
    → learn/paths/LEARNING_PATH.md (12-week track)
    → languages/python/problems/01-two-sum.md

Some Python Experience
    → README.md
    → setup.ps1
    → languages/python/problems/ (browse problems)
    → learn/guides/INTERVIEW_QUESTIONS.md
    → learn/paths/LEARNING_PATH.md (8-week track)

Interview Prep Mode
    → README.md
    → setup.ps1
    → learn/cheatsheets/PYTHON_CHEATSHEET.md
    → learn/guides/MOCK_INTERVIEW_GUIDE.md
    → languages/python/problems/ (all problems)
    → learn/guides/SYSTEM_DESIGN_BASICS.md

Developer/Contributor
    → README.md
    → setup.ps1
    → INFRASTRUCTURE_SETUP.md
    → COMMANDS_REFERENCE.md
    → CONTRIBUTING.md
```

---

**Next**: Return to [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md)
