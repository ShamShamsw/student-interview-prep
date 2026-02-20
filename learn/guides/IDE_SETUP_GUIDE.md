````markdown
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

---

````
