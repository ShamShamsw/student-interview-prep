# 02. Duplicate Emails

**Difficulty:** Easy  
**Topics:** GROUP BY, HAVING

---

## Problem

Write a SQL query to find all email addresses that appear more than once in the `users` table.

## Schema

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL
);
```

## Sample Data

```sql
INSERT INTO users (id, email, name) VALUES
(1, 'alice@example.com', 'Alice Smith'),
(2, 'bob@example.com', 'Bob Jones'),
(3, 'alice@example.com', 'Alice Johnson'),
(4, 'charlie@example.com', 'Charlie Brown'),
(5, 'bob@example.com', 'Bob Williams'),
(6, 'bob@example.com', 'Bob Davis');
```

## Expected Output

| email | count |
|-------|-------|
| bob@example.com | 3 |
| alice@example.com | 2 |

---

## Solution

```sql
SELECT email, COUNT(*) AS count
FROM users
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY count DESC;
```

## Explanation

- `GROUP BY email` collapses all rows with the same email into one group
- `COUNT(*)` counts how many rows are in each group
- `HAVING COUNT(*) > 1` filters to only groups with duplicates (you can't use `WHERE` here because the aggregation hasn't happened yet when `WHERE` runs)
- The key distinction: `WHERE` filters rows BEFORE grouping, `HAVING` filters groups AFTER grouping

## Follow-Up Questions

1. How would you delete the duplicate rows, keeping only the one with the lowest `id`?
2. What's the difference between `HAVING` and `WHERE`? Why can't you use `WHERE` here?
