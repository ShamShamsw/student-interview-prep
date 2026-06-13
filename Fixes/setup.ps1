#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Automated setup script for student-interview-prep repository
.DESCRIPTION
    This script installs all dependencies, configures pre-commit hooks,
    and verifies the development environment is ready to use.
.EXAMPLE
    .\setup.ps1
#>

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "🚀 Student Interview Prep Setup" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "📋 Step 1/5: Checking Python version..." -ForegroundColor Yellow
$pythonVersion = & python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✓ $pythonVersion found" -ForegroundColor Green
    
    # Check if Python 3.10+
    if ($pythonVersion -match "Python 3\.(\d+)") {
        $minorVersion = [int]$matches[1]
        if ($minorVersion -ge 10) {
            Write-Host "   ✓ Python version is 3.10 or higher" -ForegroundColor Green
        } else {
            Write-Host "   ⚠ Warning: Python 3.10+ recommended" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "   ✗ Python not found. Please install Python 3.10+ first." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Install development dependencies
Write-Host "📦 Step 2/5: Installing development dependencies..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip --quiet
    python -m pip install -r requirements-dev.txt --quiet
    Write-Host "   ✓ Development dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Failed to install dependencies" -ForegroundColor Red
    Write-Host "   Run manually: pip install -r requirements-dev.txt" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Install project dependencies
Write-Host "📚 Step 3/5: Installing project dependencies..." -ForegroundColor Yellow
$projectDirs = @(
    "languages\python\projects\interview-patterns-api",
    "languages\python\projects\interview-prep-capstone"
)

foreach ($dir in $projectDirs) {
    $reqFile = Join-Path $dir "requirements.txt"
    if (Test-Path $reqFile) {
        try {
            python -m pip install -r $reqFile --quiet
            Write-Host "   ✓ Installed: $dir" -ForegroundColor Green
        } catch {
            Write-Host "   ⚠ Warning: Failed to install $dir dependencies" -ForegroundColor Yellow
        }
    }
}
Write-Host ""

# Setup pre-commit hooks
Write-Host "🔧 Step 4/5: Setting up pre-commit hooks..." -ForegroundColor Yellow
try {
    $null = & pre-commit --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        pre-commit install | Out-Null
        Write-Host "   ✓ Pre-commit hooks installed" -ForegroundColor Green
        Write-Host "   ℹ Running initial formatting (this may take a moment)..." -ForegroundColor Cyan
        pre-commit run --all-files 2>&1 | Out-Null
        Write-Host "   ✓ Initial code formatting complete" -ForegroundColor Green
    }
} catch {
    Write-Host "   ⚠ Pre-commit setup skipped" -ForegroundColor Yellow
}
Write-Host ""

# Verify setup
Write-Host "✅ Step 5/5: Verifying installation..." -ForegroundColor Yellow
Write-Host ""
python scripts\verify_setup.py
Write-Host ""

# Success message
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "✨ Setup Complete!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎯 Quick Commands:" -ForegroundColor Cyan
Write-Host "   • Run tests:          " -NoNewline -ForegroundColor White
Write-Host "pytest" -ForegroundColor Yellow
Write-Host "   • Test with coverage: " -NoNewline -ForegroundColor White
Write-Host "pytest --cov=./ --cov-report=html" -ForegroundColor Yellow
Write-Host "   • Format code:        " -NoNewline -ForegroundColor White
Write-Host "black ." -ForegroundColor Yellow
Write-Host "   • Lint code:          " -NoNewline -ForegroundColor White
Write-Host "ruff check ." -ForegroundColor Yellow
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   • Quick Start:        " -NoNewline -ForegroundColor White
Write-Host "QUICKSTART.md" -ForegroundColor Yellow
Write-Host "   • All Commands:       " -NoNewline -ForegroundColor White
Write-Host "COMMANDS_REFERENCE.md" -ForegroundColor Yellow
Write-Host "   • Repository Map:     " -NoNewline -ForegroundColor White
Write-Host "REPOSITORY_STRUCTURE.md" -ForegroundColor Yellow
Write-Host "   • Full Setup Guide:   " -NoNewline -ForegroundColor White
Write-Host "INFRASTRUCTURE_SETUP.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎓 Start Learning:" -ForegroundColor Cyan
Write-Host "   • For Beginners:      " -NoNewline -ForegroundColor White
Write-Host "learn\guides\BEGINNER_START_HERE.md" -ForegroundColor Yellow
Write-Host "   • Learning Path:      " -NoNewline -ForegroundColor White
Write-Host "learn\paths\LEARNING_PATH.md" -ForegroundColor Yellow
Write-Host "   • First Problem:      " -NoNewline -ForegroundColor White
Write-Host "languages\python\problems\01-two-sum.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Tip: Pre-commit hooks will run automatically before each commit!" -ForegroundColor Yellow
Write-Host "💡 Tip: Type 'pytest' to run your first test!" -ForegroundColor Yellow
Write-Host ""
