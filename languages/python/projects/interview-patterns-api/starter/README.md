# Starter: Interview Patterns API

This starter API connects interview algorithms to practical usage.

## Implement TODO functions in `app.py`

- `two_sum_indices`
- `is_valid_parentheses`
- `top_k_frequent`
- `top_practiced_topics`
- `find_minutes_pair`

## Setup

From `interview-patterns-api/`:

```bash
python -m pip install -r requirements.txt
uvicorn starter.app:app --reload
```

Open docs at `http://127.0.0.1:8000/docs`.

## Suggested endpoint checks

1. `POST /practice/events` several times.
2. `GET /practice/insights/top-topics?k=2`
3. `GET /practice/insights/minutes-pair?target=75`
4. `POST /algorithms/two-sum`
5. `POST /algorithms/valid-parentheses`
6. `POST /algorithms/top-k-frequent`

## Success criteria

- API starts with no runtime errors.
- All algorithm endpoints return expected outputs.
- Practice insight endpoints use same algorithm patterns.
- Error handling returns clear 400/404 responses.
