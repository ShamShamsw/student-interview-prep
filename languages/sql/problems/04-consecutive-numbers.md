# 04. Consecutive Numbers

**Difficulty:** Medium  
**Topics:** Self-join, LAG/LEAD window functions

---

## Problem

Write a SQL query to find all numbers that appear at least three times consecutively in the `logs` table.

## Schema

```sql
CREATE TABLE logs (
    id INTEGER PRIMARY KEY,
    num INTEGER NOT NULL
);
```

## Sample Data

```sql
INSERT INTO logs (id, num) VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 2),
(5, 1),
(6, 2),
(7, 2),
(8, 2),
(9, 3);
```

## Expected Output

| consecutive_num |
|----------------|
| 1 |
| 2 |

---

## Solution 1: Self-Join

```sql
SELECT DISTINCT l1.num AS consecutive_num
FROM logs l1
JOIN logs l2 ON l1.id = l2.id - 1
JOIN logs l3 ON l2.id = l3.id - 1
WHERE l1.num = l2.num AND l2.num = l3.num;
```

## Solution 2: Window Functions (LAG/LEAD)

```sql
SELECT DISTINCT num AS consecutive_num
FROM (
    SELECT
        num,
        LAG(num, 1) OVER (ORDER BY id) AS prev_num,
        LEAD(num, 1) OVER (ORDER BY id) AS next_num
    FROM logs
) t
WHERE num = prev_num AND num = next_num;
```

## Explanation

- **Solution 1** joins the table to itself three times, linking consecutive IDs. If all three rows have the same `num`, we found a streak of 3. `DISTINCT` removes duplicates (e.g., 1 appears in rows 1,2,3 — the join would match it multiple times).
- **Solution 2** uses `LAG` (look at previous row) and `LEAD` (look at next row) to peek at neighboring values without a join. Cleaner and more efficient.
- Both assume `id` is sequential with no gaps. In production, you might need to use `ROW_NUMBER()` to handle gaps.

## Follow-Up Questions

1. What if `id` values have gaps? How would you modify the query?
2. How would you generalize this to find numbers appearing N times consecutively?
