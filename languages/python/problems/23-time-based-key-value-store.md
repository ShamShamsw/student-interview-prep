# 23. Time Based Key-Value Store

Difficulty: Medium  
Topics: hash-map, binary-search, design

Statement
Design a time-based key-value data structure that supports:
- `set(key, value, timestamp)` stores the key-value pair.
- `get(key, timestamp)` returns the value with the largest timestamp less than or equal to `timestamp`.

Examples
- Input: operations on keys like `set("foo", "bar", 1)`, `get("foo", 1)`  
  Output: `"bar"`

Constraints
- `1 <= key.length, value.length <= 100`
- `1 <= timestamp <= 10^7`
- Timestamps in `set` are strictly increasing for each key.

Hints (optional)
- Store sorted timestamp lists per key and binary-search in `get`.

Canonical solution
- `/languages/python/problems/solutions/23-time-based-key-value-store.py`
