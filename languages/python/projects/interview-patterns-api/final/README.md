# Final: Interview Patterns API

This is the complete reference implementation for the Interview Patterns API.

## Features

- Algorithm endpoints:
  - `POST /algorithms/two-sum`
  - `POST /algorithms/valid-parentheses`
  - `POST /algorithms/top-k-frequent`
- Practice tracking endpoints:
  - `POST /practice/events`
  - `GET /practice/events`
  - `GET /practice/insights/top-topics`
  - `GET /practice/insights/minutes-pair`

## Run

From `interview-patterns-api/`:

```bash
python -m pip install -r requirements.txt
uvicorn final.app:app --reload
```

Swagger docs: `http://127.0.0.1:8000/docs`

## How this maps to interview prep

- `two_sum_indices` powers minutes-pair matching.
- `Counter` + top-k powers top-topic insights.
- Stack validation powers parentheses endpoint.

Use this implementation after completing `starter/app.py`.
