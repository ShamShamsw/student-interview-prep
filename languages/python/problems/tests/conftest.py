"""Pytest configuration for core algorithms and data structures tests."""

import sys
from pathlib import Path

# Add this directory to path so 'harness' module is importable
sys.path.insert(0, str(Path(__file__).parent))
