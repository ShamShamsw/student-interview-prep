# Starter: Interview Prep Platform Capstone

This starter is intentionally incomplete. Build it sprint-by-sprint using the docs in `../docs/`.

## Starter objectives

Implement the platform in layers:
1. API routes
2. service logic
3. repositories
4. tests

## Minimum endpoints to build

- `GET /health`
- `POST /attempts`
- `GET /progress/{user_id}`
- `GET /recommendations/{user_id}`
- `POST /study-plan/{user_id}`

## Sprint usage

Follow `../docs/02-sprint-plan-agile.md` and avoid building all features at once.

## Run

```bash
python -m pip install -r ../requirements.txt
uvicorn app:app --reload
```

## Completion target

By capstone completion, your starter branch should be transformed into a stable production-style MVP with tests and CI passing.
