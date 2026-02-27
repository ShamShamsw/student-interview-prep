# 06. Rising Temperature

**Difficulty:** Easy  
**Topics:** Self-join, DATE functions

---

## Problem

Write a SQL query to find all dates where the temperature was higher than the previous day's temperature.

## Schema

```sql
CREATE TABLE weather (
    id INTEGER PRIMARY KEY,
    record_date DATE NOT NULL,
    temperature INTEGER NOT NULL
);
```

## Sample Data

```sql
INSERT INTO weather (id, record_date, temperature) VALUES
(1, '2024-01-01', 30),
(2, '2024-01-02', 35),
(3, '2024-01-03', 32),
(4, '2024-01-04', 38),
(5, '2024-01-05', 36),
(6, '2024-01-06', 40);
```

## Expected Output

| id | record_date | temperature |
|----|-------------|-------------|
| 2 | 2024-01-02 | 35 |
| 4 | 2024-01-04 | 38 |
| 6 | 2024-01-06 | 40 |

---

## Solution 1: Self-Join

```sql
SELECT w1.id, w1.record_date, w1.temperature
FROM weather w1
JOIN weather w2 ON w1.record_date = w2.record_date + INTERVAL '1 day'
WHERE w1.temperature > w2.temperature;
```

## Solution 2: LAG Window Function

```sql
SELECT id, record_date, temperature
FROM (
    SELECT
        id,
        record_date,
        temperature,
        LAG(temperature) OVER (ORDER BY record_date) AS prev_temp
    FROM weather
) t
WHERE temperature > prev_temp;
```

## Explanation

- **Solution 1** joins each day to the previous day using `date + INTERVAL '1 day'`. Note: syntax varies by database — PostgreSQL uses `+ INTERVAL '1 day'`, MySQL uses `DATE_ADD`, SQLite uses `DATE(record_date, '+1 day')`.
- **Solution 2** uses `LAG(temperature) OVER (ORDER BY record_date)` to get yesterday's temperature without a join. More portable and arguably cleaner.
- Both handle the first day correctly — there's no "previous day" so it's automatically excluded (NULL comparison returns false).

## Follow-Up Questions

1. How would you find dates where the temperature rose for 3 consecutive days?
2. What if there are gaps in the dates (missing days)? How does each solution handle that?
