# 🚀 Quick Start Guide

Get up and running in 5 minutes or less!

## ⚡ One-Command Setup

```powershell
# Windows PowerShell
.\setup.ps1
```

```bash
# Linux/Mac
chmod +x setup.ps1
./setup.ps1
```

That's it! The script will:
- ✅ Check your Python version
- ✅ Install all dependencies
- ✅ Configure pre-commit hooks
- ✅ Verify your environment

---

## 📋 Manual Setup (if needed)

### 1. Install Dependencies

```powershell
pip install -r requirements-dev.txt
```

### 2. Setup Pre-commit Hooks

```powershell
pre-commit install
pre-commit run --all-files
```

### 3. Verify Installation

```powershell
python scripts/verify_setup.py
```

---

## 🎯 Common Tasks

### Run Tests

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=./ --cov-report=html

# View coverage report
# Open: htmlcov/index.html
```

### Format & Lint Code

```powershell
# Auto-format code
black .

# Check code quality
ruff check .

# Fix auto-fixable issues
ruff check . --fix

# Run all linters
flake8 .
```

### Work on Problems

```powershell
# Navigate to problems directory
cd languages/python/problems

# Run a specific problem's tests
pytest tests/test_01_two_sum.py

# Run all problem tests
pytest tests/
```

### Work on Projects

```powershell
# Interview Patterns API
cd languages/python/projects/interview-patterns-api
pytest tests/

# Interview Prep Capstone
cd languages/python/projects/interview-prep-capstone
pytest tests/
```

---

## 🐳 Docker Environment (Optional)

If you prefer a containerized environment:

```powershell
# Build and start container
docker compose up -d

# Connect to container
docker compose exec dev bash

# Inside container, everything is pre-installed!
pytest
black .
```

---

## 📚 Learning Path

### For Beginners
1. Read the [Beginner's Guide](../learn/guides/BEGINNER_START_HERE.md)
2. Follow the [Learning Path](../learn/paths/LEARNING_PATH.md)
3. Use the [Python Cheatsheet](../learn/cheatsheets/PYTHON_CHEATSHEET.md)

### For Interview Prep
1. Start with [Easy Problems](../languages/python/problems/)
2. Review [Interview Questions](../learn/guides/INTERVIEW_QUESTIONS.md)
3. Practice [Mock Interviews](../learn/guides/MOCK_INTERVIEW_GUIDE.md)
4. Study [System Design](../learn/guides/SYSTEM_DESIGN_BASICS.md)

---

## 🔧 Troubleshooting

### Python Not Found
```powershell
# Check Python installation
python --version

# Or try
python3 --version

# Install from: https://www.python.org/downloads/
```

### Permission Errors on Windows
```powershell
# Run PowerShell as Administrator, then:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Pre-commit Fails
```powershell
# Update hooks
pre-commit autoupdate

# Clear cache
pre-commit clean
pre-commit run --all-files
```

### Import Errors in Tests
```powershell
# Make sure you're in the project root
cd c:\path\to\student-interview-prep

# Reinstall in development mode
pip install -e .
```

### Need More Commands?
📖 See [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md) for comprehensive command guide

---

## 💡 Pro Tips

1. **Use pre-commit hooks**: They automatically format code before commits
2. **Check coverage**: Aim for >80% test coverage on your solutions
3. **Run benchmarks**: Use `pytest --benchmark-only` to test performance
4. **Read error messages**: pytest provides helpful hints for failing tests
5. **Use the glossary**: Check [GLOSSARY.md](../learn/resources/GLOSSARY.md) for terms

---

## 🆘 Need Help?

- 📖 Full documentation: [INFRASTRUCTURE_SETUP.md](INFRASTRUCTURE_SETUP.md)
- ❓ Common questions: [FAQ.md](../learn/guides/FAQ.md)
- 🐛 Found a bug? Check [CONTRIBUTING.md](../CONTRIBUTING.md)
- 💬 Questions? Open an issue on GitHub

---

## ✅ You're Ready!

Your environment is now set up. Happy coding! 🎉

**Next**: Choose a problem from [languages/python/problems/](../languages/python/problems/) and start practicing!
