# 📝 Commands Reference

Quick reference for all common development commands. Copy and paste as needed!

---

## 🚀 Initial Setup

```powershell
# Automated setup (recommended)
.\setup.ps1

# Or manual setup
pip install -r requirements-dev.txt
pre-commit install
python scripts\verify_setup.py
```

---

## 🧪 Testing

### Run Tests

```powershell
# Run all tests
pytest

# Run tests in a specific directory
pytest languages\python\problems\tests

# Run a specific test file
pytest languages\python\problems\tests\test_01_two_sum.py

# Run tests matching a pattern
pytest -k "two_sum"

# Run tests with specific marker
pytest -m "not slow"

# Verbose output
pytest -v

# Stop after first failure
pytest -x

# Show 10 slowest tests
pytest --durations=10
```

### Coverage

```powershell
# Run tests with coverage
pytest --cov=languages --cov-report=term

# Generate HTML coverage report
pytest --cov=languages --cov-report=html
# Open: htmlcov\index.html

# Generate coverage for specific module
pytest --cov=languages\python\problems --cov-report=term-missing
```

### Benchmarks

```powershell
# Run only benchmark tests
pytest --benchmark-only

# Run benchmarks and save results
pytest --benchmark-only --benchmark-json=benchmark.json

# Compare benchmarks
pytest --benchmark-compare
```

---

## 🎨 Code Formatting & Linting

### Black (Formatter)

```powershell
# Check if code needs formatting
black --check .

# Auto-format all code
black .

# Format specific file
black languages\python\problems\solutions\01-two-sum.py

# Show what would be formatted (dry run)
black --diff .
```

### Ruff (Fast Linter)

```powershell
# Check all files
ruff check .

# Auto-fix issues
ruff check . --fix

# Check specific file
ruff check languages\python\problems\solutions\01-two-sum.py

# Show all violations (even passed)
ruff check . --verbose
```

### Flake8 (Linter)

```powershell
# Lint all files
flake8 .

# Lint specific directory
flake8 languages\python\problems

# Show statistics
flake8 . --statistics --count

# Lint with custom line length
flake8 . --max-line-length=100
```

### MyPy (Type Checker)

```powershell
# Type check all files
mypy .

# Type check specific module
mypy languages\python\problems

# Strict mode
mypy --strict languages\python\problems\solutions
```

---

## 🔧 Pre-commit Hooks

```powershell
# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files

# Run on staged files only
pre-commit run

# Run specific hook
pre-commit run black

# Update hook versions
pre-commit autoupdate

# Uninstall hooks
pre-commit uninstall

# Clear cache
pre-commit clean
```

---

## 🐳 Docker

### Basic Commands

```powershell
# Build container
docker compose build

# Start container (detached)
docker compose up -d

# View logs
docker compose logs

# Stop container
docker compose down

# Rebuild and start
docker compose up -d --build
```

### Working Inside Container

```powershell
# Connect to running container
docker compose exec dev bash

# Inside container, run commands:
pytest
black .
ruff check .
python languages\python\problems\solutions\01-two-sum.py
```

### Container Management

```powershell
# List running containers
docker ps

# Remove all stopped containers
docker compose down -v

# Rebuild without cache
docker compose build --no-cache

# View container resource usage
docker stats
```

---

## 📦 Dependency Management

```powershell
# Install/update all dependencies
pip install -r requirements-dev.txt

# Install project dependencies
pip install -r languages\python\projects\interview-patterns-api\requirements.txt
pip install -r languages\python\projects\interview-prep-capstone\requirements.txt

# Update pip itself
python -m pip install --upgrade pip

# List installed packages
pip list

# Show outdated packages
pip list --outdated

# Create requirements file from environment
pip freeze > requirements.txt

# Install package in editable mode
pip install -e .
```

---

## 🔍 Code Navigation

```powershell
# View directory structure
tree /F

# Find Python files
Get-ChildItem -Path . -Filter *.py -Recurse

# Search for text in files
Select-String -Path .\**\*.py -Pattern "def two_sum"

# Count lines of code
(Get-Content .\languages\python\problems\solutions\*.py | Measure-Object -Line).Lines
```

---

## 📊 Git Commands

```powershell
# Check status
git status

# Add all changes
git add .

# Commit (pre-commit hooks will run)
git commit -m "Your message"

# Push to remote
git push

# Create new branch
git checkout -b feature/new-problem

# View commit history
git log --oneline

# Show changes
git diff

# Stash changes
git stash
git stash pop
```

---

## 🧹 Cleanup

```powershell
# Remove Python cache files
Get-ChildItem -Path . -Filter "__pycache__" -Recurse | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Filter "*.pyc" -Recurse | Remove-Item -Force

# Remove test artifacts
Remove-Item -Path .pytest_cache -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path htmlcov -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path .coverage -Force -ErrorAction SilentlyContinue

# Remove build artifacts
Remove-Item -Path build -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path dist -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Filter "*.egg-info" -Recurse | Remove-Item -Recurse -Force

# Complete cleanup (all of the above)
.\scripts\clean.ps1  # If you create this helper script
```

---

## 🛠️ Utility Commands

```powershell
# Verify setup
python scripts\verify_setup.py

# Check Python version
python --version

# Check which Python is being used
Get-Command python | Format-List *

# Launch Python REPL
python

# Run a Python file
python languages\python\problems\solutions\01-two-sum.py

# Launch IPython (enhanced REPL)
ipython

# View Python path
python -c "import sys; print('\n'.join(sys.path))"
```

---

## 📈 Performance & Profiling

```powershell
# Time a command
Measure-Command { pytest }

# Profile Python code
python -m cProfile -s cumulative your_script.py

# Line profiler (if installed)
kernprof -l -v your_script.py

# Memory profiler (if installed)
python -m memory_profiler your_script.py
```

---

## 🆘 Troubleshooting Commands

```powershell
# Check if port is in use
Test-NetConnection -ComputerName localhost -Port 8000

# Kill process on port
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process

# Fix permissions (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Reinstall corrupted package
pip uninstall package-name
pip install package-name

# Clear pip cache
pip cache purge

# Diagnose import issues
python -c "import sys; import pprint; pprint.pprint(sys.path)"
```

---

## 💡 Pro Tips

### Aliases (add to PowerShell profile)

```powershell
# Edit your PowerShell profile
notepad $PROFILE

# Add these aliases:
Set-Alias -Name py -Value python
Set-Alias -Name ipy -Value ipython
Function Test-All { pytest --cov=languages --cov-report=html }
Set-Alias -Name ta -Value Test-All
Function Format-Code { black . }
Set-Alias -Name fmt -Value Format-Code
```

### Quick Test Loop

```powershell
# Watch for changes and re-run tests (requires pytest-watch)
pip install pytest-watch
ptw -- --cov=languages
```

### Combined Commands

```powershell
# Format, lint, and test in one command
black . ; ruff check . --fix ; pytest

# Full quality check
pre-commit run --all-files ; pytest --cov=languages
```

---

## 📚 Learn More

- **Full Documentation**: See [INFRASTRUCTURE_SETUP.md](INFRASTRUCTURE_SETUP.md)
- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
- **FAQ**: See [learn/guides/FAQ.md](learn/guides/FAQ.md)
