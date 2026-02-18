# Problem Test Harness (Pytest)

This folder provides a reusable test harness for solution files in `../solutions/`.

What it includes:
- `harness.py` — dynamic loader and shared builders for linked lists, trees, and graphs.
- `test_core_algorithms.py` — tests for array/string/binary-search/interval/DP problems.
- `test_design_and_structures.py` — tests for design, linked-list, tree, and graph problems.

## Run tests

From repo root:

```bash
python -m pytest languages/python/problems/tests -q
```

Or with your Windows launcher alias:

```bash
python3.12 -m pytest languages/python/problems/tests -q
```

## Extend the harness

When you add a new solution file:
1. Add or reuse helpers in `harness.py`.
2. Add test coverage in one of the test files.
3. Keep tests deterministic and focused on constraints in the markdown statement.
