# Final: Interview Prep Platform Capstone

This folder represents the target quality bar for your capstone backend implementation.

## What final includes

- layered API/service/repository organization (kept lightweight for learning)
- attempt tracking and progress analytics
- recommendation generation from weakness signals
- study plan endpoint patterns
- tests and clear behavior expectations

## Run final reference

```bash
python -m pip install -r ../requirements.txt
uvicorn app:app --reload
```

## Compare checklist

When comparing your starter build to final:
- Are handlers thin and logic extracted?
- Are edge cases tested?
- Are recommendations deterministic?
- Are response shapes consistent?
