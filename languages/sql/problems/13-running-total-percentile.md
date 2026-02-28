# Problem 13: Running Total & Percentile

Difficulty: Medium  
Topics: window functions, SUM() OVER, PERCENT_RANK, NTILE

---

## Statement

Write a query against the `orders` table that returns, for each completed order:

1. `order_id`, `customer_id`, `order_date`, `amount`
2. `running_total` — cumulative revenue up to and including this order (ordered by date), scoped to the customer
3. `pct_of_customer_total` — this order's amount as a % of the customer's all-time revenue
4. `revenue_quartile` — buckets each order into Q1 / Q2 / Q3 / Q4 based on amount across all orders

---

## Schema

```sql
CREATE TABLE orders (
    order_id    INT PRIMARY KEY,
    customer_id INT,
    order_date  DATE,
    amount      DECIMAL(10, 2),
    status      VARCHAR(20)
);
```

---

## Solution

```sql
SELECT
    order_id,
    customer_id,
    order_date,
    ROUND(amount, 2)                                              AS amount,

    -- Running total per customer, ordered by date
    ROUND(SUM(amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2)                                                         AS running_total,

    -- This order as % of customer's total
    ROUND(amount * 100.0 / SUM(amount) OVER (PARTITION BY customer_id), 2)
                                                                  AS pct_of_customer_total,

    -- Quartile bucket across ALL orders
    'Q' || NTILE(4) OVER (ORDER BY amount)                        AS revenue_quartile

FROM orders
WHERE status = 'completed'
ORDER BY customer_id, order_date;
```

---

## Key Concepts

- `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` — includes all rows from the start of the partition up to the current row (standard running total frame).
- `SUM() OVER (PARTITION BY customer_id)` with no ORDER BY = total for the entire customer partition (not cumulative).
- `NTILE(4)` divides all rows into 4 equal groups — works across the entire result set unless you PARTITION.
