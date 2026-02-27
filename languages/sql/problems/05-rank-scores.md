# 05. Rank Scores

**Difficulty:** Medium  
**Topics:** Window functions, DENSE_RANK

---

## Problem

Write a SQL query to rank scores in a table. The ranking should be dense (no gaps between ranks). If two scores are the same, they should have the same rank.

## Schema

```sql
CREATE TABLE scores (
    id INTEGER PRIMARY KEY,
    score DECIMAL(5, 2) NOT NULL
);
```

## Sample Data

```sql
INSERT INTO scores (id, score) VALUES
(1, 3.50),
(2, 3.65),
(3, 4.00),
(4, 3.85),
(5, 4.00),
(6, 3.65);
```

## Expected Output

| score | rank |
|-------|------|
| 4.00 | 1 |
| 4.00 | 1 |
| 3.85 | 2 |
| 3.65 | 3 |
| 3.65 | 3 |
| 3.50 | 4 |

---

## Solution

```sql
SELECT
    score,
    DENSE_RANK() OVER (ORDER BY score DESC) AS rank
FROM scores
ORDER BY score DESC;
```

## Explanation

- `DENSE_RANK()` assigns the same rank to identical values and leaves no gaps in the sequence (4.00 → rank 1, 3.85 → rank 2, not rank 3)
- The difference between the three ranking functions:

| Function | 4.00, 4.00, 3.85 would get... | Use when |
|----------|-------------------------------|----------|
| `ROW_NUMBER()` | 1, 2, 3 | You need unique sequential numbers (no ties) |
| `RANK()` | 1, 1, 3 | Ties get same rank, but next rank skips (gap) |
| `DENSE_RANK()` | 1, 1, 2 | Ties get same rank, no gaps |

- `OVER (ORDER BY score DESC)` defines the window — rank by score from highest to lowest

## Without Window Functions (for older SQL versions)

```sql
SELECT
    s.score,
    (SELECT COUNT(DISTINCT s2.score) FROM scores s2 WHERE s2.score >= s.score) AS rank
FROM scores s
ORDER BY s.score DESC;
```

This counts how many distinct scores are ≥ the current score, which produces the same result as `DENSE_RANK`.

## Follow-Up Questions

1. How would you get the top 3 ranked scores only?
2. What changes if you want `RANK()` behavior instead of `DENSE_RANK()`?
