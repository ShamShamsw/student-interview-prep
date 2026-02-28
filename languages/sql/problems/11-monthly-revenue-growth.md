# Problem 11: Monthly Revenue Growth

Difficulty: Medium  
Topics: window functions, LAG, CTE, date functions

---

## Statement

You have a table of daily order transactions. Write a SQL query that returns the **month-over-month revenue growth** for each month, showing:
- month (YYYY-MM format)
- total revenue for that month
- total revenue for the previous month
- absolute revenue change
- percentage change (rounded to 2 decimal places)

Order results chronologically. The first month should show `NULL` for previous month and change columns.

---

## Schema

```sql
CREATE TABLE orders (
    order_id   INT,
    order_date DATE,
    amount     DECIMAL(10, 2)
);
```

---

## Example

**Input — orders:**

| order_id | order_date | amount |
|---|---|---|
| 1 | 2024-01-05 | 200.00 |
| 2 | 2024-01-20 | 150.00 |
| 3 | 2024-02-10 | 500.00 |
| 4 | 2024-02-28 | 100.00 |
| 5 | 2024-03-15 | 300.00 |

**Expected Output:**

| month | revenue | prev_revenue | change | pct_change |
|---|---|---|---|---|
| 2024-01 | 350.00 | NULL | NULL | NULL |
| 2024-02 | 600.00 | 350.00 | 250.00 | 71.43 |
| 2024-03 | 300.00 | 600.00 | -300.00 | -50.00 |

---

## Solution (PostgreSQL)

```sql
WITH monthly AS (
    SELECT
        TO_CHAR(order_date, 'YYYY-MM') AS month,
        SUM(amount)                    AS revenue
    FROM orders
    GROUP BY 1
)
SELECT
    month,
    ROUND(revenue, 2)                                              AS revenue,
    ROUND(LAG(revenue) OVER (ORDER BY month), 2)                  AS prev_revenue,
    ROUND(revenue - LAG(revenue) OVER (ORDER BY month), 2)        AS change,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY month))
        / NULLIF(LAG(revenue) OVER (ORDER BY month), 0) * 100,
    2)                                                             AS pct_change
FROM monthly
ORDER BY month;
```

## Solution (SQLite)

```sql
WITH monthly AS (
    SELECT
        strftime('%Y-%m', order_date) AS month,
        SUM(amount)                   AS revenue
    FROM orders
    GROUP BY 1
)
SELECT
    month,
    ROUND(revenue, 2)                                          AS revenue,
    ROUND(LAG(revenue) OVER (ORDER BY month), 2)              AS prev_revenue,
    ROUND(revenue - LAG(revenue) OVER (ORDER BY month), 2)    AS change,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY month))
        / LAG(revenue) OVER (ORDER BY month) * 100,
    2)                                                         AS pct_change
FROM monthly
ORDER BY month;
```

---

## Complexity

- Time: O(n log n) — one GROUP BY + one window pass
- Space: O(m) — m = number of distinct months

---

## Key Concepts

- Window `LAG()` looks back one row within the ordered window.
- `NULLIF(expr, 0)` prevents division-by-zero — returns NULL instead of error.
- The `ORDER BY` inside `OVER()` determines which row is "previous," not the outer `ORDER BY`.
