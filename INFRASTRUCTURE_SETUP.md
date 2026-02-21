# Technical Infrastructure Setup Guide

This guide helps you set up the development environment with all the technical infrastructure tools.

## Quick Start

### 1. Install Development Dependencies

```bash
# Install all development tools
pip install -r requirements-dev.txt

# Or use make command
make install-dev
```

### 2. Setup Pre-commit Hooks

Pre-commit hooks automatically format and lint your code before each commit:

```bash
# Install pre-commit hooks
pre-commit install

# Run on all files (first time)
pre-commit run --all-files

# Or use make command
make precommit
```

The hooks will automatically:
- Format code with Black
- Lint with Flake8
- Remove trailing whitespace
- Fix end-of-file issues
- Validate YAML/JSON files

### 3. Run Tests with Coverage

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=./ --cov-report=term --cov-report=html

# Or use make commands
make test
make test-cov  # Opens htmlcov/index.html after
```

### 4. Run Benchmarks

```bash
# Run only benchmark tests
pytest --benchmark-only

# Or use make command
make bench
```

### 5. Docker Development Environment

Use Docker for a consistent development environment:

```bash
# Build the container
docker compose build

# Start the container
docker compose up -d

# Connect to the container
docker compose exec dev bash

# Or use make commands
make docker-build
make docker-up
make docker-shell
```

Inside the container, all dependencies are pre-installed and ready to use.

## Available Make Commands

Run `make help` to see all available commands:

- `make install` - Install project dependencies
- `make install-dev` - Install dev dependencies + setup pre-commit
- `make test` - Run all tests
- `make test-cov` - Run tests with coverage report
- `make lint` - Run all linters
- `make format` - Auto-format code
- `make clean` - Remove build artifacts and cache
- `make bench` - Run benchmarks
- `make docker-build` - Build Docker image
- `make docker-up` - Start Docker container
- `make docker-shell` - Connect to running container
- `make precommit` - Run pre-commit on all files

## CI/CD Pipeline

The repository has several CI workflows:

### New Unified CI Workflow (`.github/workflows/ci.yml`)
- **Lint**: Runs Black, Flake8, and Ruff checks
- **Test**: Runs tests on Python 3.10, 3.11, and 3.12
- **Coverage**: Uploads coverage to Codecov
- **Benchmark**: Runs benchmark tests and saves results

### Existing Workflows
- `python-tests.yml` - Python test suite
- `yaml-lint.yml` - YAML file validation
- `notebook-checks.yml` - Jupyter notebook validation
- `actions-smoke-test.yml` - GitHub Actions validation

## Dependabot

Dependabot automatically creates PRs to update dependencies weekly for:
- Root-level pip packages
- Interview patterns API project
- Interview prep capstone project
- GitHub Actions versions

## Code Quality Tools

### Black (Code Formatter)
```bash
# Check formatting
black --check .

# Auto-format
black .
```

### Flake8 (Linter)
```bash
flake8 . --max-line-length=100
```

### Ruff (Fast Linter)
```bash
ruff check .
```

### MyPy (Type Checker)
```bash
mypy .
```

## Coverage Reports

After running tests with coverage:
- **Terminal**: Shows coverage summary
- **HTML Report**: Open `htmlcov/index.html` in browser
- **XML Report**: `coverage.xml` for CI tools

## Troubleshooting

### Pre-commit hooks fail
```bash
# Update pre-commit hooks
pre-commit autoupdate

# Clear cache and retry
pre-commit clean
pre-commit run --all-files
```

### Docker issues
```bash
# Rebuild without cache
docker compose build --no-cache

# Remove all containers and volumes
docker compose down -v
```

### Import errors in tests
The `pytest.ini` and `conftest.py` files configure the Python path. If you still see import errors:
```bash
# Install project in editable mode
pip install -e .
```

## Badge Setup

Your README badges are configured for:

```markdown
[![CI](https://github.com/ShamShamsw/student-interview-prep/actions/workflows/ci.yml/badge.svg)](https://github.com/ShamShamsw/student-interview-prep/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ShamShamsw/student-interview-prep/branch/main/graph/badge.svg)](https://codecov.io/gh/ShamShamsw/student-interview-prep)
```

For Codecov (public repos), no token needed. For private repos:
1. Go to https://codecov.io
2. Connect your GitHub repository
3. Add `CODECOV_TOKEN` to GitHub repository secrets
