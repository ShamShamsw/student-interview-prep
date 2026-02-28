# Problem 12: Cohort Retention Rate

Difficulty: Hard  
Topics: CTEs, window functions, self-join, date arithmetic, GROUP BY

---

## Statement

You have an `orders` table of customer transactions. Write a SQL query that computes a **cohort retention table** showing, for each monthly cohort of new customers, what percentage remained active (placed at least one order) in each of the following months (periods 0–4).

- **Cohort** = the month a customer placed their first ever order.
- **Period 0** = the cohort month itself (always 100%).
- **Period n** = n months after the cohort month.

Return: `cohort_month`, `period`, `cohort_size`, `active_users`, `retention_pct`.

---

## Schema

```sql
CREATE TABLE orders (
    order_id    INT,
    customer_id INT,
    order_date  DATE,
    amount      DECIMAL(10, 2)
);
```

---

## Solution (PostgreSQL)

```sql
WITH first_order AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', MIN(order_date))::DATE AS cohort_month
    FROM orders
    GROUP BY customer_id
),
cohort_size AS (
    SELECT cohort_month, COUNT(*) AS size
    FROM first_order
    GROUP BY cohort_month
),
activity AS (
    SELECT
        f.cohort_month,
        o.customer_id,
        DATE_PART('year', AGE(DATE_TRUNC('month', o.order_date), f.cohort_month)) * 12
        + DATE_PART('month', AGE(DATE_TRUNC('month', o.order_date), f.cohort_month)) AS period
    FROM orders o
    JOIN first_order f ON o.customer_id = f.customer_id
    WHERE DATE_TRUNC('month', o.order_date) >= f.cohort_month
)
SELECT
    a.cohort_month,
    a.period::INT                                             AS period,
    cs.size                                                   AS cohort_size,
    COUNT(DISTINCT a.customer_id)                             AS active_users,
    ROUND(COUNT(DISTINCT a.customer_id) * 100.0 / cs.size, 1) AS retention_pct
FROM activity a
JOIN cohort_size cs ON a.cohort_month = cs.cohort_month
WHERE a.period <= 4
GROUP BY a.cohort_month, a.period, cs.size
ORDER BY a.cohort_month, a.period;
```

---

## Example Output

| cohort_month | period | cohort_size | active_users | retention_pct |
|---|---|---|---|---|
| 2024-01-01 | 0 | 120 | 120 | 100.0 |
| 2024-01-01 | 1 | 120 | 72 | 60.0 |
| 2024-01-01 | 2 | 120 | 50 | 41.7 |
| 2024-02-01 | 0 | 95 | 95 | 100.0 |
| 2024-02-01 | 1 | 95 | 52 | 54.7 |

---

## Visualization in Python

```python
import pandas as pd, seaborn as sns, matplotlib.pyplot as plt

pivot = df.pivot_table(index="cohort_month", columns="period", values="retention_pct")
plt.figure(figsize=(10, 6))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="Blues", vmin=0, vmax=100)
plt.title("Cohort Retention Heatmap (%)")
plt.tight_layout()
plt.show()
```

---

## Key Concepts

- First compute `first_order` month per customer (determines cohort).
- `AGE()` or integer arithmetic computes months between dates.
- `COUNT(DISTINCT customer_id)` per cohort+period gives active users.
- Divide by cohort size for retention %.
- Period 0 = always 100% (the cohort definition month).
