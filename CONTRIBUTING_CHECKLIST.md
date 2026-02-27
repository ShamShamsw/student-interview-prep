# Quick CONTRIBUTING Checklist

This short checklist includes exact commands to get a development environment ready and run tests locally.

## Python (POSIX / macOS / WSL)

- Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

- Install development dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

- Run tests (repo root):

```bash
pytest
```

## Python (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pytest
```

## JavaScript

- Install dependencies and run tests/lint:

```bash
cd languages/javascript
npm ci
npm run lint
npm test
```

## Using Docker (dev container)

Start a dev container with source mounted:

```bash
docker-compose up --build
# then open a shell in the `dev` container
docker exec -it student-interview-prep-dev /bin/bash
```

## Notes & Tips

- Starter/`starter/` folders are exercises — complete them locally and run the tests in that folder.
- If CI fails, reproduce locally with the same Python version used in CI: `python -V`.
- For dependency pinning, consider using a lockfile or `pip-tools`/`poetry` for reproducible installs.
