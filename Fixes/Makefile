.PHONY: help install install-dev test test-cov lint format clean docker-build docker-up docker-down bench

help:  ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

install:  ## Install project dependencies
	pip install -r requirements-dev.txt
	cd languages/python/projects/interview-patterns-api && pip install -r requirements.txt
	cd languages/python/projects/interview-prep-capstone && pip install -r requirements.txt

install-dev:  ## Install development dependencies and setup pre-commit
	pip install -r requirements-dev.txt
	pre-commit install
	@echo "Pre-commit hooks installed!"

test:  ## Run all tests
	pytest

test-cov:  ## Run tests with coverage report
	pytest --cov=./ --cov-report=term --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

lint:  ## Run linters (black check, flake8, ruff)
	black --check .
	flake8 . --count --max-line-length=100 --statistics
	ruff check .

format:  ## Auto-format code with black
	black .
	@echo "Code formatted!"

clean:  ## Remove build artifacts, cache files, and coverage reports
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete
	@echo "Cleaned build artifacts and cache files!"

bench:  ## Run benchmark tests
	pytest --benchmark-only

docker-build:  ## Build Docker development environment
	docker compose build

docker-up:  ## Start Docker development environment
	docker compose up -d
	@echo "Development container started. Run 'make docker-shell' to connect."

docker-down:  ## Stop Docker development environment
	docker compose down

docker-shell:  ## Open shell in running Docker container
	docker compose exec dev bash

precommit:  ## Run pre-commit hooks on all files
	pre-commit run --all-files
