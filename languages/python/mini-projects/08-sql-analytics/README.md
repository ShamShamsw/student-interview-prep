````markdown
# Mini-Project 08: SQL Analytics — In-Database Analysis

**Time:** 2–3 hours  
**Difficulty:** Medium  
**Concepts:** SQL window functions, CTEs, aggregations, cohort analysis, SQLite, Python + SQL

---

## Objective

Write real analytical SQL against a local SQLite database — the same patterns used in data analyst and data engineering interviews. You will practice every major analytics SQL pattern: window functions, cohort analysis, funnels, and running totals, using Python to load data and execute queries.

---

## Setup

```python
# setup.py — run once to create the database
import sqlite3
import numpy as np
import pandas as pd

np.random.seed(7)
conn = sqlite3.connect("ecommerce.db")

# ── Customers ────────────────────────────────────────────────
customers = pd.DataFrame({
    "customer_id": range(1, 501),
    "name":        [f"Customer_{i}" for i in range(1, 501)],
    "region":      np.random.choice(["North", "South", "East", "West"], 500),
    "signup_date": pd.to_datetime(
        np.random.choice(pd.date_range("2022-01-01", "2023-12-31"), 500)
    ).strftime("%Y-%m-%d"),
    "segment":     np.random.choice(["Retail", "Wholesale", "Online"], 500, p=[0.5, 0.2, 0.3]),
})

# ── Products ─────────────────────────────────────────────────
products = pd.DataFrame({
    "product_id":  range(1, 51),
    "product_name":[f"Product_{i}" for i in range(1, 51)],
    "category":    np.random.choice(["Electronics", "Clothing", "Food", "Home"], 50),
    "unit_price":  np.round(np.random.uniform(5, 500, 50), 2),
})

# ── Orders ───────────────────────────────────────────────────
n_orders = 3000
orders = pd.DataFrame({
    "order_id":    range(10001, 10001 + n_orders),
    "customer_id": np.random.randint(1, 501, n_orders),
    "product_id":  np.random.randint(1, 51, n_orders),
    "order_date":  pd.to_datetime(
        np.random.choice(pd.date_range("2023-01-01", "2024-12-31"), n_orders)
    ).strftime("%Y-%m-%d"),
    "quantity":    np.random.randint(1, 10, n_orders),
    "status":      np.random.choice(["completed", "refunded", "pending"], n_orders, p=[0.85, 0.10, 0.05]),
})
orders["revenue"] = (
    orders["product_id"].map(products.set_index("product_id")["unit_price"]) * orders["quantity"]
).round(2)

# ── Events / Funnel ──────────────────────────────────────────
events_rows = []
for cid in np.random.choice(range(1, 501), 400, replace=False):
    events_rows.append((cid, "viewed",    "2024-01-15", np.random.choice([True, False])))
    if np.random.rand() > 0.3:
        events_rows.append((cid, "added_to_cart", "2024-01-15", np.random.choice([True, False])))
    if np.random.rand() > 0.5:
        events_rows.append((cid, "checkout",      "2024-01-15", np.random.choice([True, False])))
    if np.random.rand() > 0.6:
        events_rows.append((cid, "purchased",     "2024-01-15", np.random.choice([True, False])))

events = pd.DataFrame(events_rows, columns=["customer_id", "event_type", "event_date", "is_mobile"])

# Write to SQLite
customers.to_sql("customers", conn, if_exists="replace", index=False)
products.to_sql("products",   conn, if_exists="replace", index=False)
orders.to_sql("orders",       conn, if_exists="replace", index=False)
events.to_sql("events",       conn, if_exists="replace", index=False)
conn.close()
print("Database created: ecommerce.db")
print(f"  customers: {len(customers)}, products: {len(products)}, orders: {len(orders)}, events: {len(events)}")
```

---

## How to Run Queries

```python
# query_runner.py
import sqlite3
import pandas as pd

def query(sql: str, db: str = "ecommerce.db") -> pd.DataFrame:
    """Execute SQL and return a DataFrame."""
    with sqlite3.connect(db) as conn:
        return pd.read_sql_query(sql, conn)

# Example
df = query("SELECT * FROM customers LIMIT 5")
print(df)
```

---

## Tasks

### Task 1 — Schema Exploration

```sql
-- 1a. How many rows in each table?
-- 1b. What is the date range of orders?
-- 1c. What fraction of orders are completed vs refunded vs pending?
-- 1d. Which product category has the highest average unit price?

-- Starter for 1c:
SELECT status, COUNT(*) AS cnt,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS pct
FROM orders
GROUP BY status
ORDER BY cnt DESC;
```

---

### Task 2 — Aggregation (SUMIF / COUNTIF in SQL)

```sql
-- 2a. Total revenue and number of completed orders per region
--     (join orders → customers, filter status = 'completed')

-- 2b. Top 10 products by total revenue (completed orders only)

-- 2c. Monthly revenue for 2024 — include months with zero orders
--     (Hint: generate month series in Python, left join SQL results)

-- 2d. Revenue per customer segment per quarter
```

---

### Task 3 — Window Functions

```sql
-- 3a. Rank customers by total revenue (all time) — show top 20
WITH customer_revenue AS (
    SELECT customer_id, SUM(revenue) AS total_rev
    FROM orders WHERE status = 'completed'
    GROUP BY customer_id
)
SELECT
    customer_id,
    total_rev,
    RANK() OVER (ORDER BY total_rev DESC)       AS revenue_rank,
    ROUND(
        total_rev * 100.0 / SUM(total_rev) OVER (),
    2)                                          AS pct_of_total_revenue
FROM customer_revenue
ORDER BY revenue_rank
LIMIT 20;

-- 3b. For each order, show the customer's cumulative spend up to that order date
--     (running total per customer, ordered by order_date)

-- 3c. Add a column: revenue compared to department average (diff from avg)
--     (use AVG() OVER PARTITION BY category)

-- 3d. 3-order moving average of daily revenue in 2024
```

---

### Task 4 — Ranking & Top-N Per Group

```sql
-- 4a. Top 3 products by revenue within each category
--     (Use DENSE_RANK() OVER PARTITION BY category)

-- 4b. Second highest revenue customer per region

-- 4c. For each month, the single best-selling product (by quantity)

-- Starter for 4a:
WITH ranked AS (
    SELECT
        p.category,
        p.product_name,
        SUM(o.revenue) AS total_revenue,
        DENSE_RANK() OVER (
            PARTITION BY p.category
            ORDER BY SUM(o.revenue) DESC
        ) AS rnk
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    WHERE o.status = 'completed'
    GROUP BY p.category, p.product_name
)
SELECT category, product_name, total_revenue, rnk
FROM ranked
WHERE rnk <= 3
ORDER BY category, rnk;
```

---

### Task 5 — Month-over-Month Growth

```sql
-- 5a. Monthly revenue with MoM change and MoM % change
WITH monthly AS (
    SELECT
        strftime('%Y-%m', order_date) AS month,
        SUM(revenue)                  AS revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY 1
),
with_lag AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) AS prev_revenue
    FROM monthly
)
SELECT
    month,
    ROUND(revenue, 2)                                                            AS revenue,
    ROUND(prev_revenue, 2)                                                       AS prev_revenue,
    ROUND(revenue - prev_revenue, 2)                                             AS mom_change,
    ROUND((revenue - prev_revenue) * 100.0 / prev_revenue, 2)                   AS mom_pct_change
FROM with_lag
ORDER BY month;

-- 5b. Year-over-year revenue comparison: 2023 vs 2024 per region
-- 5c. Rolling 3-month revenue per region
```

---

### Task 6 — Cohort Retention

```sql
-- 6. Build a cohort table:
--    Row   = cohort month (month of first order)
--    Column = months since first order (0, 1, 2, ...)
--    Value = % of cohort still active (placed an order)

-- Step 1: first order month per customer
WITH first_order AS (
    SELECT customer_id,
           strftime('%Y-%m', MIN(order_date)) AS cohort_month
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
),
-- Step 2: all (customer, month) order activity
activity AS (
    SELECT DISTINCT
        o.customer_id,
        f.cohort_month,
        strftime('%Y-%m', o.order_date) AS active_month,
        -- period: months since cohort start
        (
            (strftime('%Y', o.order_date) - strftime('%Y', f.cohort_month || '-01')) * 12
            + strftime('%m', o.order_date) - strftime('%m', f.cohort_month || '-01')
        ) AS period
    FROM orders o
    JOIN first_order f ON o.customer_id = f.customer_id
    WHERE o.status = 'completed'
),
-- Step 3: count per cohort per period
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT customer_id) AS cohort_customers
    FROM first_order
    GROUP BY cohort_month
)
SELECT
    a.cohort_month,
    a.period,
    COUNT(DISTINCT a.customer_id)                              AS active_customers,
    c.cohort_customers,
    ROUND(COUNT(DISTINCT a.customer_id) * 100.0 / c.cohort_customers, 1) AS retention_pct
FROM activity a
JOIN cohort_size c ON a.cohort_month = c.cohort_month
WHERE a.period <= 6
GROUP BY a.cohort_month, a.period
ORDER BY a.cohort_month, a.period;
```

---

### Task 7 — Funnel Analysis

```sql
-- 7. Compute conversion rates at each funnel step for the events table

SELECT
    COUNT(DISTINCT CASE WHEN event_type = 'viewed'       THEN customer_id END) AS step1_viewed,
    COUNT(DISTINCT CASE WHEN event_type = 'added_to_cart' THEN customer_id END) AS step2_cart,
    COUNT(DISTINCT CASE WHEN event_type = 'checkout'     THEN customer_id END) AS step3_checkout,
    COUNT(DISTINCT CASE WHEN event_type = 'purchased'    THEN customer_id END) AS step4_purchased,
    ROUND(COUNT(DISTINCT CASE WHEN event_type = 'added_to_cart' THEN customer_id END) * 100.0
        / COUNT(DISTINCT CASE WHEN event_type = 'viewed' THEN customer_id END), 1) AS view_to_cart_pct,
    ROUND(COUNT(DISTINCT CASE WHEN event_type = 'purchased' THEN customer_id END) * 100.0
        / COUNT(DISTINCT CASE WHEN event_type = 'viewed' THEN customer_id END), 1) AS overall_conversion_pct
FROM events;

-- 7b. Compare funnel conversion for mobile vs desktop users
```

---

### Task 8 — Deduplication & Data Quality

```sql
-- 8a. Check: are there any customers with more than one order on the same day for the same product?
SELECT customer_id, product_id, order_date, COUNT(*) AS cnt
FROM orders
GROUP BY customer_id, product_id, order_date
HAVING cnt > 1;

-- 8b. Find customers in orders who don't exist in the customers table
SELECT DISTINCT o.customer_id
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- 8c. What percentage of customers have placed more than 5 orders?
```

---

## Expected Outputs

| Task | What to verify |
|---|---|
| 1c | Three status rows summing to 100% |
| 3a | 20 rows ranked 1–20 |
| 4a | ≤3 rows per category |
| 5a | MoM NULLs on first row; realistic % changes |
| 6 | Period 0 retention = 100% for every cohort |
| 7 | step1 > step2 > step3 > step4 |

---

## Stretch Goals

- Visualize the cohort retention table as a heatmap using seaborn.
- Build a Python function `run_report(db, start_date, end_date)` that generates all 8 tasks and writes them to a multi-sheet Excel file.
- Rewrite the same queries using **pandas** and compare outputs.
- Port the SQLite database to PostgreSQL and test dialect differences.
- Add a `reviews` table (1–5 star ratings) and compute average rating per product and per category.
````
