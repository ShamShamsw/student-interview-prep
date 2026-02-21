"""
Quick setup verification script for student-interview-prep repository.
Run this after installing dependencies to verify your environment is ready.
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.10 or higher."""
    print("🐍 Checking Python version...")
    major, minor = sys.version_info[:2]
    if major == 3 and minor >= 10:
        print(f"   ✓ Python {major}.{minor} is supported")
        return True
    else:
        print(f"   ✗ Python {major}.{minor} is not supported (need 3.10+)")
        return False


def check_package(package_name, import_name=None):
    """Check if a package is installed."""
    if import_name is None:
        import_name = package_name
    try:
        __import__(import_name)
        print(f"   ✓ {package_name} installed")
        return True
    except ImportError:
        print(f"   ✗ {package_name} not installed")
        return False


def check_precommit():
    """Check if pre-commit is installed and configured."""
    print("\n🔧 Checking pre-commit setup...")
    try:
        result = subprocess.run(
            ["pre-commit", "--version"], capture_output=True, text=True, check=True
        )
        print(f"   ✓ pre-commit installed: {result.stdout.strip()}")

        # Check if hooks are installed
        git_hooks = Path(".git/hooks/pre-commit")
        if git_hooks.exists():
            print("   ✓ pre-commit hooks are installed")
            return True
        else:
            print("   ⚠ pre-commit installed but hooks not configured")
            print("     Run: pre-commit install")
            return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("   ✗ pre-commit not installed")
        return False


def check_files():
    """Check if required configuration files exist."""
    print("\n📄 Checking configuration files...")
    files = [
        ".pre-commit-config.yaml",
        ".gitignore",
        "pytest.ini",
        "ruff.toml",
        ".yamllint",
        "requirements-dev.txt",
        "docker-compose.yml",
        "Makefile",
    ]

    all_exist = True
    for file in files:
        if Path(file).exists():
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} missing")
            all_exist = False

    return all_exist


def main():
    print("=" * 60)
    print("🚀 Student Interview Prep - Setup Verification")
    print("=" * 60)

    checks = []

    # Check Python version
    checks.append(check_python_version())

    # Check essential packages
    print("\n📦 Checking core packages...")
    checks.append(check_package("pytest"))
    checks.append(check_package("pytest-cov", "pytest_cov"))
    checks.append(check_package("black"))
    checks.append(check_package("ruff"))
    checks.append(check_package("flake8"))

    # Check pre-commit
    checks.append(check_precommit())

    # Check configuration files
    checks.append(check_files())

    # Summary
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ All checks passed! Your environment is ready.")
        print("\n📚 Next steps:")
        print("   1. Run 'make test' to run all tests")
        print("   2. Run 'make test-cov' to see coverage report")
        print("   3. Check INFRASTRUCTURE_SETUP.md for more details")
    else:
        print("⚠️  Some checks failed. Please install missing dependencies:")
        print("\n   pip install -r requirements-dev.txt")
        print("   pre-commit install")
        print("\n   Or use: make install-dev")
    print("=" * 60)


if __name__ == "__main__":
    main()
