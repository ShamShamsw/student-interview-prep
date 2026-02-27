# 08. Customers Who Never Order

**Difficulty:** Easy  
**Topics:** LEFT JOIN, IS NULL

---

## Problem

Write a SQL query to find all customers who have never placed an order.

## Schema

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    amount DECIMAL(10, 2) NOT NULL,
    order_date DATE NOT NULL
);
```

## Sample Data

```sql
INSERT INTO customers (id, name) VALUES
(1, 'Alice'), (2, 'Bob'), (3, 'Charlie'), (4, 'Diana'), (5, 'Eve');

INSERT INTO orders (id, customer_id, amount, order_date) VALUES
(101, 1, 50.00, '2024-01-15'),
(102, 3, 75.50, '2024-01-20'),
(103, 1, 30.00, '2024-02-01'),
(104, 5, 120.00, '2024-02-10');
```

## Expected Output

| name |
|------|
| Bob |
| Diana |

---

## Solution 1: LEFT JOIN + IS NULL

```sql
SELECT c.name
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;
```

## Solution 2: NOT EXISTS

```sql
SELECT c.name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.id
);
```

## Solution 3: NOT IN

```sql
SELECT name
FROM customers
WHERE id NOT IN (
    SELECT DISTINCT customer_id
    FROM orders
    WHERE customer_id IS NOT NULL
);
```

## Explanation

- **Solution 1** LEFT JOINs customers to orders — customers with no orders have NULL in all order columns. We filter for those NULLs.
- **Solution 2** checks for each customer whether any matching order exists. `NOT EXISTS` is often the most readable.
- **Solution 3** gets all customer IDs that appear in orders and excludes them. **Careful:** if `customer_id` can be NULL in orders, `NOT IN` behaves unexpectedly — `NOT IN (1, 2, NULL)` returns nothing! Always add `WHERE customer_id IS NOT NULL`.

**Performance:** On large tables, `NOT EXISTS` and `LEFT JOIN + IS NULL` usually perform similarly and often better than `NOT IN`. Most databases optimize them to the same plan, but `NOT IN` can cause issues with NULLs and large subqueries.

## Follow-Up Questions

1. How would you find customers who ordered only once?
2. What's the performance difference between these three approaches on a table with 10 million rows?
