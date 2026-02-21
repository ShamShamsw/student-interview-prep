"""Pytest configuration for interview-patterns-api tests."""

import sys
from pathlib import Path

# Add parent directory to path so 'final' module is importable
sys.path.insert(0, str(Path(__file__).parent.parent))
