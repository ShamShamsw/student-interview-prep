# Interview Patterns API (FastAPI)

Build a small API that applies interview algorithms to realistic practice data.

## Project objective

Create an API that can:
- Run algorithm endpoints (`two-sum`, `valid-parentheses`, `top-k-frequent`)
- Track practice events (`topic`, `minutes`, `difficulty`)
- Generate insights (top practiced topics and matching minute-pair targets)

## Prerequisites

- Python 3.10+
- Basic API familiarity
- `pip` for dependency install

## Estimated time

90-150 minutes

## Learning outcomes

By the end, you should be able to:
- Build and run a FastAPI service
- Reuse algorithm patterns in product-like API logic
- Validate request data with Pydantic models
- Organize starter vs final project implementations

## Project structure

- `starter/` — partially implemented API with TODOs
- `final/` — complete reference API
- `tests/` — permanent endpoint test suite (pytest)
- `walkthrough.ipynb` — build sequence and validation plan
- `requirements.txt` — project dependencies

## Quick start

From `interview-patterns-api/`:

```bash
python -m pip install -r requirements.txt
uvicorn final.app:app --reload
```

Open docs at:
- `http://127.0.0.1:8000/docs`

Run tests:

```bash
python -m pytest tests -q
```

## Suggested workflow

1. Start from `starter/README.md`.
2. Implement TODO algorithm functions in `starter/app.py`.
3. Run API and verify endpoints in Swagger.
4. Compare with `final/app.py`.
5. Review `walkthrough.ipynb`.
