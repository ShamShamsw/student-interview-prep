# IDE Setup Guide

Get your development environment configured for the best learning experience.

## Recommended: Visual Studio Code

VS Code is free, lightweight, and has excellent Python support.

### Install VS Code

1. Download from [code.visualstudio.com](https://code.visualstudio.com/)
2. Run the installer
3. Launch VS Code

### Essential Extensions

Install these extensions (click Extensions icon in sidebar or press `Ctrl+Shift+X`):

#### 1. Python (by Microsoft)
- Official Python support
- IntelliSense, linting, debugging
- Install: Search "Python" → Install

#### 2. Pylance (by Microsoft)
- Fast language server
- Better code completion
- Install: Search "Pylance" → Install

#### 3. Black Formatter (by Microsoft)
- Auto-format Python code
- Matches repository style
- Install: Search "Black Formatter" → Install

### Recommended Extensions

#### 4. Error Lens
- Shows errors inline (very helpful for beginners)
- Install: Search "Error Lens" → Install

#### 5. autoDocstring
- Generate docstrings automatically
- Install: Search "autoDocstring" → Install

#### 6. GitLens
- Enhanced Git features
- See code history inline
- Install: Search "GitLens" → Install

#### 7. Jupyter (by Microsoft)
- If you want to use notebooks
- Install: Search "Jupyter" → Install

### VS Code Settings

Create or edit your settings (`Ctrl+,` or File → Preferences → Settings):

**settings.json** (click "Open Settings (JSON)" in top right):

```json
{
  "python.defaultInterpreterPath": "python",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.rulers": [88],
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": [
    "."
  ],
  "[python]": {
    "editor.tabSize": 4,
    "editor.insertSpaces": true
  }
}
```

### Workspace Setup

Open this repository as a workspace:
1. File → Open Folder
2. Navigate to `student-interview-prep`
3. Click "Select Folder"

### Python Interpreter Selection

1. Press `Ctrl+Shift+P` (Command Palette)
2. Type "Python: Select Interpreter"
3. Choose Python 3.10 or newer
4. VS Code will show the version in the bottom left

### Running Code

**Option 1: Run in Terminal**
1. Open integrated terminal: `` Ctrl+` ``
2. Navigate to file directory
3. Run: `python filename.py`

**Option 2: Run Button**
1. Open a Python file
2. Click the ▶ button in top right
3. Output appears in terminal

### Running Tests

**Option 1: Test Explorer**
1. Click Testing icon in sidebar (beaker icon)
2. VS Code discovers tests automatically
3. Click ▶ next to any test to run

**Option 2: Terminal**
```bash
pytest languages/python/problems/tests/test_core_algorithms.py
```

### Debugging

1. Set a breakpoint (click left of line number)
2. Press `F5` or Run → Start Debugging
3. Choose "Python File"
4. Step through with `F10` (step over), `F11` (step into)

---

## Alternative: PyCharm

PyCharm Community Edition is a full-featured IDE.

### Install PyCharm

1. Download from [jetbrains.com/pycharm/download](https://www.jetbrains.com/pycharm/download/)
2. Choose **Community Edition** (free)
3. Run installer

### Project Setup

1. Open PyCharm
2. Open → Navigate to `student-interview-prep`
3. PyCharm will detect it's a Python project

### Configure Interpreter

1. File → Settings (or PyCharm → Preferences on Mac)
2. Project: student-interview-prep → Python Interpreter
3. Click gear icon → Add
4. Choose System Interpreter → Python 3.10+
5. Apply

### Install Packages

PyCharm will prompt to install requirements. Or install manually:
1. Terminal (bottom of window)
2. Run: `pip install pytest black flake8`

### Running Tests

1. Right-click `tests/` folder
2. "Run pytest in tests"
3. Results appear in bottom panel

### Code Formatting

1. Settings → Tools → Black
2. Enable "Format on save"
3. Or use `Ctrl+Alt+L` to format manually

---

## Command Line Only (Minimalist)

If you prefer working in terminal with a text editor:

### Editor Choices
- **Vim/Neovim**: Powerful but steep learning curve
- **nano**: Simple, built-in on most systems
- **Sublime Text**: Fast, lightweight GUI

### Essential Tools

Install these command-line tools:

```bash
# Install Python packages
pip install pytest black flake8 ipython

# Verify installations
python --version      # Should be 3.10+
pytest --version
black --version
flake8 --version
```

### Workflow

```bash
# Edit code
nano languages/python/problems/solutions/01-two-sum.py

# Run code
python languages/python/problems/solutions/01-two-sum.py

# Format code
black languages/python/problems/solutions/01-two-sum.py

# Check style
flake8 languages/python/problems/solutions/01-two-sum.py

# Run tests
pytest languages/python/problems/tests/
```

### IPython (Interactive Python)

```bash
# Launch
ipython

# Load and test functions
In [1]: from solutions.two_sum import two_sum
In [2]: two_sum([2, 7, 11, 15], 9)
Out[2]: [0, 1]

# Exit
In [3]: exit
```

---

## Git Setup

### Install Git

**Windows**: Download from [git-scm.com](https://git-scm.com/)  
**Mac**: `brew install git` or Xcode Command Line Tools  
**Linux**: `sudo apt install git` (Ubuntu/Debian)

### Configure Git

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Basic Workflow

```bash
# Clone repository (if not already)
git clone https://github.com/ShamShamsw/student-interview-prep.git
cd student-interview-prep

# Create a branch for your work
git checkout -b my-solutions

# After making changes
git add .
git commit -m "Solve problem 01: two sum"

# Push to your fork (if contributing)
git push origin my-solutions
```

### VS Code Git Integration

- Source Control icon in sidebar (third from top)
- Stage changes by clicking `+` next to files
- Write commit message and click ✓
- Push/pull with sync button

---

## Python Virtual Environment (Optional but Recommended)

Keep project dependencies isolated.

### Create Virtual Environment

```bash
# In repository root
python -m venv venv
```

### Activate

**Windows**:
```bash
venv\Scripts\activate
```

**Mac/Linux**:
```bash
source venv/bin/activate
```

You'll see `(venv)` in your terminal prompt.

### Install Packages

```bash
pip install pytest black flake8
```

### Deactivate

```bash
deactivate
```

### VS Code Auto-Activation

VS Code can activate venv automatically:
1. Create `.vscode/settings.json` in repository root
2. Add:
```json
{
  "python.terminal.activateEnvironment": true
}
```

---

## Code Formatting (Black)

This repository uses Black for consistent Python style.

### Format Files

```bash
# Format one file
black languages/python/problems/solutions/01-two-sum.py

# Format all Python files
black languages/python/
```

### VS Code Auto-Format

With settings from above, files format on save automatically.

Or press `Shift+Alt+F` to format current file manually.

---

## Linting (Flake8)

Catch common errors before running code.

### Check Files

```bash
# Check one file
flake8 languages/python/problems/solutions/01-two-sum.py

# Check all Python files
flake8 languages/python/
```

### VS Code Integration

With Python extension, flake8 warnings appear as squiggly underlines.

Hover over them for explanation and quick fixes.

---

## Troubleshooting

### "python: command not found"

**Windows**: Make sure Python is in PATH during installation  
**Mac/Linux**: Use `python3` instead of `python`

### Extensions not working in VS Code

1. Reload window: `Ctrl+Shift+P` → "Reload Window"
2. Check Python interpreter is selected (bottom left)
3. Reinstall extension if needed

### Tests not discovered

1. Make sure pytest is installed: `pip install pytest`
2. Check VS Code testing settings (see settings.json above)
3. Reload window
4. Check terminal for error messages

### Import errors in tests

Make sure you're running tests from the correct directory:
```bash
cd languages/python/problems
python -m pytest tests/
```

---

## Performance Tips

### VS Code Performance
- Disable unused extensions
- Exclude large folders from search:
  ```json
  "files.exclude": {
    "**/.git": true,
    "**/__pycache__": true,
    "**/*.pyc": true
  }
  ```

### Terminal Performance
- Use virtual environments to install only needed packages
- Clear pytest cache: `pytest --cache-clear`

---

## Next Steps

1. Install VS Code and extensions OR your preferred IDE
2. Clone the repository if you haven't
3. Open repository as workspace/project
4. Verify Python interpreter is 3.10+
5. Install pytest: `pip install pytest`
6. Run a test to verify setup: `pytest languages/python/problems/tests/test_core_algorithms.py`

If everything passes, you're ready to start coding! Head to [BEGINNER_START_HERE.md](BEGINNER_START_HERE.md) for your first problem.
