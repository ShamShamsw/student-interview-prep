```markdown
# student-interview-prep

[![CI](https://github.com/ShamShamsw/student-interview-prep/actions/workflows/ci.yml/badge.svg)](https://github.com/ShamShamsw/student-interview-prep/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ShamShamsw/student-interview-prep/branch/main/graph/badge.svg)](https://codecov.io/gh/ShamShamsw/student-interview-prep)
[![Python Tests](https://github.com/ShamShamsw/student-interview-prep/actions/workflows/python-tests.yml/badge.svg)](https://github.com/ShamShamsw/student-interview-prep/actions/workflows/python-tests.yml)
[![YAML Lint](https://github.com/ShamShamsw/student-interview-prep/actions/workflows/yaml-lint.yml/badge.svg)](https://github.com/ShamShamsw/student-interview-prep/actions/workflows/yaml-lint.yml)

[![Contribute](https://img.shields.io/badge/contribute-Guide-blue.svg)](CONTRIBUTING.md)
> A comprehensive, beginner-friendly repository for technical interview preparation with 35+ coding problems, practical projects, and guided learning paths.

---

## 🚀 Quick Start (5 Minutes)

> 👋 **First time here?** Check out [WELCOME.md](WELCOME.md) to choose your learning path!

### 1. Clone & Setup
```powershell
# Clone the repository
git clone https://github.com/ShamShamsw/student-interview-prep.git
cd student-interview-prep

# Run automated setup (installs dependencies, configures tools)
.\setup.ps1
```

### 2. Start Learning
```powershell
# Run your first test
pytest languages/python/problems/tests/test_01_two_sum.py

# View the problem
# Open: languages/python/problems/01-two-sum.md
```

### 3. Track Progress
- Use the [Learning Path Checklist](learn/paths/LEARNING_PATH_CHECKLIST.md) to track completed problems
- Follow the [8-Week Learning Path](learn/paths/LEARNING_PATH.md) for structured progression

📖 **New here?** Start with these guides:
- [QUICKSTART.md](QUICKSTART.md) - Complete setup in 5 minutes
- [REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md) - Find your way around
- [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md) - All commands you'll need

---

## 📚 What's Inside

### 💻 Coding Problems (35+)
- **Arrays & Hashing**: Two Sum, Valid Anagram, Group Anagrams, Top K Elements
- **Two Pointers**: Valid Palindrome, 3Sum, Container With Most Water
- **Sliding Window**: Longest Substring, Permutation in String
- **Binary Search**: Search Rotated Array, Koko Eating Bananas
- **Linked Lists**: Reverse List, Detect Cycle, Merge Lists
- **Trees & Graphs**: Valid BST, Level Order Traversal, Number of Islands
- **Dynamic Programming**: Coin Change, Kth Largest Element

📁 Location: [`languages/python/problems/`](languages/python/problems/)

### 🏗️ Practical Projects
- **Interview Patterns API**: REST API demonstrating algorithm patterns
- **Interview Prep Capstone**: Full-stack interview tracking application
- **Sample Todo App**: Best practices demonstration
- **Study Session Tracker**: Time management tool

📁 Location: [`languages/python/projects/`](languages/python/projects/)

### 📖 Learning Resources
- [Beginner's Start Guide](learn/guides/BEGINNER_START_HERE.md) - 2-week daily plan for newcomers
- [Learning Path](learn/paths/LEARNING_PATH.md) - 8-week and 12-week structured tracks
- [Python Cheatsheet](learn/cheatsheets/PYTHON_CHEATSHEET.md) - Time complexity & common patterns
- [Interview Questions](learn/guides/INTERVIEW_QUESTIONS.md) - Behavioral & technical prep
- [Mock Interview Guide](learn/guides/MOCK_INTERVIEW_GUIDE.md) - Practice like the real thing
- [System Design Basics](learn/guides/SYSTEM_DESIGN_BASICS.md) - Architecture fundamentals
- [Glossary](learn/resources/GLOSSARY.md) - Technical terms explained simply

---

## ✨ Interactive Features (NEW!)

### 🎨 Algorithm Visualizer
Watch algorithms come to life with step-by-step visual animations!

```bash
# Web-based visualizer (open in browser)
open visualizer.html

# Terminal visualizer
python scripts/visualize.py two-sum --array "[2,7,11,15]" --target 9
python scripts/visualize.py binary-search --array "[1,2,3,4,5]" --target 3
python scripts/visualize.py merge-sort --array "[5,2,8,1,9]"
```

### 📊 Progress Tracker
Beautiful visual progress tracking with achievements and streaks!

```bash
# View your progress
python scripts/progress_tracker.py

# Detailed breakdown by topic
python scripts/progress_tracker.py --detailed

# Mark a problem complete
python scripts/progress_tracker.py --mark-complete 01-two-sum
```

**Features:**
- 📈 Visual progress bars by difficulty and topic
- 🔥 Streak tracking (current & best)
- 🏆 Achievement system with unlockable badges
- 📅 Recent activity history

### ⭐ Daily Challenge System
Get personalized daily coding challenges using spaced repetition!

```bash
# Get today's challenge
python scripts/daily_challenge.py

# Challenge by difficulty
python scripts/daily_challenge.py --difficulty Easy

# Challenge by topic
python scripts/daily_challenge.py --topic arrays

# Complete a challenge
python scripts/daily_challenge.py --complete 01-two-sum --success
```

**Smart Algorithm:**
- Uses spaced repetition for optimal review timing
- Prioritizes problems you haven't mastered
- Adapts to your success rate
- Never repeats the same problem too soon

### 🏆 Achievement System
Unlock achievements as you progress!

```bash
# View all achievements
python scripts/achievements.py

# See what's next
python scripts/achievements.py --next

# Export your badges
python scripts/achievements.py --export badges.md
```

**Achievement Types:**
- 🌟 Milestone achievements (1st, 5th, 10th, 20th, all problems)
- 🔥 Streak achievements (3, 7, 30, 100 days)
- 🎯 Topic mastery (complete all in a category)
- ⚡ Speed challenges

### 💡 Interactive Hint System
Get progressive hints without spoiling the solution!

```bash
# Get first hint
python scripts/hints.py 01-two-sum

# Get specific level hint
python scripts/hints.py 35-coin-change --level 3

# Show all hints
python scripts/hints.py 15-valid-palindrome --all
```

**5-Level Hint System:**
1. Conceptual hint (what to think about)
2. Approach hint (general strategy)
3. Data structure hint (what to use)
4. Implementation hint (how to code it)
5. Complexity hint (time/space targets)

### 📊 Code Quality Analyzer
Get detailed analysis of your solutions!

```bash
# Analyze a solution
python scripts/analyze_code.py languages/python/problems/solutions/01-two-sum.py

# Analyze all solutions
python scripts/analyze_code.py languages/python/problems/solutions/ --all

# Detailed analysis
python scripts/analyze_code.py solutions/35-coin-change.py --detailed
```

**Analyzes:**
- ⚡ Time & space complexity
- 📈 Cyclomatic complexity
- 🎨 Code style & readability
- 📚 Documentation coverage
- ✨ Best practices compliance
- 🎯 Overall quality score (0-100)

### 🌐 Multi-Language Support
Now supporting JavaScript in addition to Python!

```bash
# Python (existing)
cd languages/python
pytest

# JavaScript (NEW!)
cd languages/javascript
npm install
npm test
```

---

## 🛠️ For Developers

### Requirements
- Python 3.10+
- Git
- (Optional) Docker for containerized development

### Development Tools Included
- ✅ **Pre-commit hooks**: Auto-format with Black, lint with Flake8/Ruff
- ✅ **Test coverage**: pytest with coverage reporting
- ✅ **CI/CD**: GitHub Actions workflows
- ✅ **Dependabot**: Automated dependency updates
- ✅ **Docker environment**: Consistent development setup
- ✅ **Makefile commands**: Common tasks simplified

📖 Full setup guide: [INFRASTRUCTURE_SETUP.md](INFRASTRUCTURE_SETUP.md)

### Common Commands
```powershell
# Run tests
pytest

# Run with coverage
pytest --cov=./ --cov-report=html

# Format code
black .

# Lint code
ruff check .

# Verify environment
python scripts/verify_setup.py
```

---

## 🎯 Learning Paths

### Path 1: Complete Beginner (12 weeks)
1. Start with [BEGINNER_START_HERE.md](learn/guides/BEGINNER_START_HERE.md)
2. Follow [Learning Path - Beginner Track](learn/paths/LEARNING_PATH.md)
3. Complete Easy problems (01-15)
4. Build sample todo app
5. Weekly confidence checks

### Path 2: Interview Ready (8 weeks)
1. Review [Python Cheatsheet](learn/cheatsheets/PYTHON_CHEATSHEET.md)
2. Follow [Learning Path - Fast Track](learn/paths/LEARNING_PATH.md)
3. Complete all 35 problems
4. Practice [Mock Interviews](learn/guides/MOCK_INTERVIEW_GUIDE.md)
5. Study [System Design](learn/guides/SYSTEM_DESIGN_BASICS.md)

### Path 3: Self-Paced
1. Browse [problems directory](languages/python/problems/)
2. Pick problems by topic (arrays, trees, graphs, etc.)
3. Check [Learning Checklist](learn/paths/LEARNING_PATH_CHECKLIST.md)
4. Build practical projects

---

---

## 🤝 Contributing

We welcome contributions! See:
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Community standards
- [ROADMAP_Version2.md](ROADMAP_Version2.md) - Future plans

> Quick start: copy a problem template from `languages/python/problems/templates/PROBLEM_TEMPLATE.md`, add a solution in `languages/python/problems/solutions/` and tests in `languages/python/problems/tests/`, run `pre-commit run --all-files` and `pytest`, then open a PR.

### Ways to Contribute
- 🐛 Report bugs or issues
- 💡 Suggest new problems or improvements
- 📝 Improve documentation
- ✨ Add new features or solutions
- 🎨 Enhance learning materials

---

## 📊 Repository Stats

- **35+ Coding Problems** across multiple topics (Python + JavaScript)
- **4 Practical Projects** with real-world applications
- **15+ Learning Guides** and resources
- **100% Test Coverage** for solutions
- **CI/CD Pipeline** with automated testing
- **7 Interactive Tools** (Progress Tracker, Daily Challenge, Achievements, Visualizer, Hints, Code Analyzer, Multi-language)
- **2 Languages Supported** (Python & JavaScript)

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE_Version2.txt](LICENSE_Version2.txt) for details.

---

## 🆘 Getting Help

- **Setup Guide**: [QUICKSTART.md](QUICKSTART.md) - Get started in 5 minutes
- **Repository Map**: [REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md) - Navigate the repo
- **All Commands**: [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md) - Complete command reference
- **Quick Answers**: [FAQ.md](learn/guides/FAQ.md) - Common questions
- **Technical Terms**: [GLOSSARY.md](learn/resources/GLOSSARY.md) - Definitions
- **IDE Setup**: [IDE_SETUP_GUIDE.md](learn/guides/IDE_SETUP_GUIDE.md) - Configure your editor
- **Questions**: Open an issue on GitHub

---

## 🎉 Ready to Start?

1. **Run setup**: `.\setup.ps1`
2. **Read the quickstart**: [QUICKSTART.md](QUICKSTART.md)
3. **Choose your path**: Pick from the learning paths above
4. **Start coding**: Open a problem and begin!

Happy coding and good luck with your interviews! 🚀

```
