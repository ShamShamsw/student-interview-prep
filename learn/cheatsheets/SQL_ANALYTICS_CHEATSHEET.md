# SQL Analytics Cheatsheet

> Reference for analytical SQL patterns used in data science, data engineering, and BI interviews — window functions, CTEs, time-series, cohort analysis, and more.

---

## Table of Contents

1. [Query Execution Order](#query-execution-order)
2. [Joins Reference](#joins-reference)
3. [Aggregates & GROUP BY](#aggregates--group-by)
4. [CASE WHEN — Conditional Logic](#case-when--conditional-logic)
5. [Subqueries & CTEs](#subqueries--ctes)
6. [Window Functions](#window-functions)
7. [Ranking Functions](#ranking-functions)
8. [Lead, Lag & Running Totals](#lead-lag--running-totals)
9. [Date & Time Operations](#date--time-operations)
10. [String Functions](#string-functions)
11. [NULL Handling](#null-handling)
12. [Set Operations](#set-operations)
13. [Analytics Patterns](#analytics-patterns)
14. [Performance & Indexing Notes](#performance--indexing-notes)
15. [Dialect Differences](#dialect-differences)

---

## Query Execution Order

Understanding this prevents almost every ORDER BY / WHERE / HAVING confusion.

```
FROM      → choose tables, apply JOINs
WHERE     → filter rows (before grouping; cannot use aliases or window functions)
GROUP BY  → group rows
HAVING    → filter groups (after GROUP BY; can use aggregates)
SELECT    → compute output columns, apply window functions
DISTINCT  → remove duplicate rows
ORDER BY  → sort result (can use aliases from SELECT)
LIMIT     → restrict row count
```

> **Trap:** You cannot filter on a window function result in `WHERE`. Use a subquery or CTE first.

---

## Joins Reference

```sql
-- INNER JOIN: only matching rows in both tables
SELECT e.name, d.department_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;

-- LEFT JOIN: all rows from left; NULL where no match on right
SELECT c.name, o.order_id
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;

-- Find customers who have NEVER ordered (anti-join pattern)
SELECT c.name
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.order_id IS NULL;

-- FULL OUTER JOIN: all rows from both; NULLs where no match
SELECT a.id, b.id
FROM table_a a
FULL OUTER JOIN table_b b ON a.id = b.id;

-- CROSS JOIN: every combination (cartesian product)
SELECT s.size, c.color
FROM sizes s
CROSS JOIN colors c;

-- SELF JOIN: join table to itself
-- Use case: find employees and their managers
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

---

## Aggregates & GROUP BY

```sql
-- Basic aggregates
SELECT
    department,
    COUNT(*)                          AS total_employees,
    COUNT(DISTINCT manager_id)        AS num_managers,
    SUM(salary)                       AS total_payroll,
    AVG(salary)                       AS avg_salary,
    MIN(salary)                       AS min_salary,
    MAX(salary)                       AS max_salary,
    ROUND(AVG(salary), 2)             AS avg_salary_rounded
FROM employees
GROUP BY department
HAVING COUNT(*) >= 5                  -- filter groups (not individual rows)
ORDER BY total_payroll DESC;

-- COUNT(*) vs COUNT(col)
-- COUNT(*): counts all rows including NULLs
-- COUNT(col): counts only non-NULL values in that column

-- Conditional aggregation (Excel: SUMIF, COUNTIF, AVERAGEIF)
SELECT
    department,
    COUNT(*)                                      AS total,
    COUNT(CASE WHEN salary > 80000 THEN 1 END)    AS high_earners,
    SUM(CASE WHEN gender = 'Female' THEN salary END) AS female_payroll,
    AVG(CASE WHEN region = 'West' THEN salary END)   AS avg_west_salary
FROM employees
GROUP BY department;

-- Grouping sets (multiple GROUP BY in one query)
SELECT region, department, SUM(revenue)
FROM sales
GROUP BY GROUPING SETS (
    (region, department),   -- subtotals for region + dept
    (region),               -- subtotals for region only
    ()                      -- grand total
);

-- ROLLUP (hierarchical subtotals)
SELECT year, quarter, SUM(revenue)
FROM sales
GROUP BY ROLLUP (year, quarter);

-- CUBE (all combinations of subtotals)
SELECT region, product, SUM(revenue)
FROM sales
GROUP BY CUBE (region, product);
```

---

## CASE WHEN — Conditional Logic

```sql
-- Simple CASE (like Excel IF / IFS)
SELECT
    name,
    salary,
    CASE
        WHEN salary >= 120000 THEN 'Principal'
        WHEN salary >= 85000  THEN 'Senior'
        WHEN salary >= 55000  THEN 'Mid'
        ELSE                       'Junior'
    END AS level
FROM employees;

-- CASE in aggregate (pivot rows to columns)
SELECT
    department,
    SUM(CASE WHEN quarter = 'Q1' THEN revenue ELSE 0 END) AS q1,
    SUM(CASE WHEN quarter = 'Q2' THEN revenue ELSE 0 END) AS q2,
    SUM(CASE WHEN quarter = 'Q3' THEN revenue ELSE 0 END) AS q3,
    SUM(CASE WHEN quarter = 'Q4' THEN revenue ELSE 0 END) AS q4
FROM sales
GROUP BY department;
```

---

## Subqueries & CTEs

```sql
-- Inline subquery in WHERE
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Correlated subquery (runs once per outer row — can be slow)
SELECT name, salary, department
FROM employees e
WHERE salary = (
    SELECT MAX(salary)
    FROM employees
    WHERE department = e.department   -- references outer row
);

-- ── CTEs (Common Table Expressions) ──────────────────────────
-- Cleaner alternative to subqueries; evaluated once (in most DBs)

WITH avg_by_dept AS (
    SELECT department, AVG(salary) AS avg_sal
    FROM employees
    GROUP BY department
)
SELECT e.name, e.salary, a.avg_sal,
       e.salary - a.avg_sal AS diff_from_avg
FROM employees e
JOIN avg_by_dept a ON e.department = a.department;

-- Multiple CTEs chained together
WITH
monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        SUM(amount) AS revenue
    FROM orders
    GROUP BY 1
),
prev_month AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) AS prev_revenue
    FROM monthly_revenue
)
SELECT
    month,
    revenue,
    prev_revenue,
    ROUND((revenue - prev_revenue) / prev_revenue * 100, 2) AS pct_change
FROM prev_month
ORDER BY month;

-- Recursive CTE (hierarchy traversal: org chart, BOM, file tree)
WITH RECURSIVE org_chart AS (
    -- Anchor: start with the CEO (manager_id is NULL)
    SELECT id, name, manager_id, 0 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive: join each employee to their manager
    SELECT e.id, e.name, e.manager_id, oc.depth + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT depth, name FROM org_chart ORDER BY depth, name;
```

---

## Window Functions

Window functions compute a value for each row **using a "window" of related rows** without collapsing rows (unlike GROUP BY).

```sql
-- Syntax
function_name() OVER (
    PARTITION BY col      -- optional: groups rows (like GROUP BY per window)
    ORDER BY col          -- optional: ordering within the window
    ROWS BETWEEN ...      -- optional: frame specification
)
```

```sql
-- Running total per department (no PARTITION = entire table)
SELECT
    name,
    department,
    salary,
    SUM(salary) OVER (PARTITION BY department ORDER BY hire_date) AS running_dept_total,
    AVG(salary) OVER (PARTITION BY department)                    AS dept_avg
FROM employees;

-- Compare each row to group average
SELECT
    name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department)        AS dept_avg,
    salary - AVG(salary) OVER (PARTITION BY department) AS diff_from_avg,
    salary / SUM(salary) OVER (PARTITION BY department) * 100 AS pct_of_dept
FROM employees;

-- Moving / rolling average (Excel: AVERAGE of N rows)
SELECT
    order_date,
    daily_revenue,
    AVG(daily_revenue) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW   -- 7-day rolling avg
    ) AS rolling_7d_avg
FROM daily_sales;

-- Frame clauses
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW   -- cumulative sum
ROWS BETWEEN 6 PRECEDING AND CURRENT ROW           -- rolling 7 rows
ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING           -- 3-row centered avg
ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING   -- suffix sum
```

---

## Ranking Functions

```sql
SELECT
    name,
    department,
    salary,
    ROW_NUMBER()   OVER (PARTITION BY department ORDER BY salary DESC) AS row_num,
    RANK()         OVER (PARTITION BY department ORDER BY salary DESC) AS rank,
    DENSE_RANK()   OVER (PARTITION BY department ORDER BY salary DESC) AS dense_rank,
    NTILE(4)       OVER (ORDER BY salary DESC)                         AS quartile,
    PERCENT_RANK() OVER (ORDER BY salary)                              AS pct_rank,
    CUME_DIST()    OVER (ORDER BY salary)                              AS cume_dist
FROM employees;

-- ROW_NUMBER:   unique per row — 1, 2, 3, 4
-- RANK:         ties share rank, gap after — 1, 2, 2, 4
-- DENSE_RANK:   ties share rank, no gap — 1, 2, 2, 3
-- NTILE(4):     bucket into 4 equal groups (quartiles)
-- PERCENT_RANK: (rank-1)/(rows-1) — fraction of rows below
-- CUME_DIST:    fraction of rows ≤ current row

-- ── Common pattern: top N per group ──────────────────────────
-- (Cannot use WHERE on window functions — wrap in CTE or subquery)
WITH ranked AS (
    SELECT
        name, department, salary,
        DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
    FROM employees
)
SELECT name, department, salary
FROM ranked
WHERE rnk <= 3;
```

---

## Lead, Lag & Running Totals

```sql
-- LAG: previous row's value (Excel: previous row reference)
-- LEAD: next row's value
SELECT
    order_date,
    revenue,
    LAG(revenue, 1)  OVER (ORDER BY order_date)  AS prev_day_revenue,
    LEAD(revenue, 1) OVER (ORDER BY order_date)  AS next_day_revenue,
    revenue - LAG(revenue) OVER (ORDER BY order_date) AS day_over_day_change,
    (revenue - LAG(revenue) OVER (ORDER BY order_date))
        / NULLIF(LAG(revenue) OVER (ORDER BY order_date), 0) * 100 AS pct_change
FROM daily_sales
ORDER BY order_date;

-- FIRST_VALUE / LAST_VALUE — compare to period start/end
SELECT
    month,
    revenue,
    FIRST_VALUE(revenue) OVER (ORDER BY month)                         AS first_month_rev,
    LAST_VALUE(revenue)  OVER (ORDER BY month ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) AS last_month_rev
FROM monthly_sales;

-- Cumulative sum (running total)
SELECT
    order_date,
    revenue,
    SUM(revenue) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) AS cumulative_revenue
FROM daily_sales;

-- Year-to-date by partition
SELECT
    sale_date,
    region,
    revenue,
    SUM(revenue) OVER (
        PARTITION BY region, EXTRACT(YEAR FROM sale_date)
        ORDER BY sale_date
        ROWS UNBOUNDED PRECEDING
    ) AS ytd_revenue
FROM sales;
```

---

## Date & Time Operations

> Syntax varies by database — see [Dialect Differences](#dialect-differences).

```sql
-- ── PostgreSQL ────────────────────────────────────────────────

-- Current date/time
SELECT NOW(), CURRENT_DATE, CURRENT_TIMESTAMP;

-- Truncate to period
DATE_TRUNC('month', order_date)          -- first day of month
DATE_TRUNC('quarter', order_date)
DATE_TRUNC('year', order_date)

-- Extract components
EXTRACT(YEAR FROM order_date)
EXTRACT(MONTH FROM order_date)
EXTRACT(DOW FROM order_date)             -- day of week: 0=Sun, 6=Sat
EXTRACT(WEEK FROM order_date)

-- Arithmetic
order_date + INTERVAL '7 days'
order_date - INTERVAL '1 month'
AGE(end_date, start_date)                -- difference as interval
order_date::date - hire_date::date       -- integer days difference

-- ── MySQL / BigQuery ─────────────────────────────────────────
DATE_FORMAT(order_date, '%Y-%m')         -- "2024-03"
YEAR(order_date), MONTH(order_date), DAY(order_date)
DATE_ADD(order_date, INTERVAL 7 DAY)
DATEDIFF(end_date, start_date)           -- days difference

-- ── SQLite ───────────────────────────────────────────────────
strftime('%Y-%m', order_date)            -- "2024-03"
julianday('now') - julianday(hire_date)  -- days since hire

-- ── Common analytics patterns ────────────────────────────────

-- Monthly revenue
SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS revenue
FROM orders
GROUP BY 1
ORDER BY 1;

-- Cohort: join on month of first purchase
WITH first_purchase AS (
    SELECT user_id, MIN(DATE_TRUNC('month', order_date)) AS cohort_month
    FROM orders
    GROUP BY user_id
)
SELECT
    f.cohort_month,
    DATE_TRUNC('month', o.order_date)                              AS order_month,
    COUNT(DISTINCT o.user_id)                                     AS active_users
FROM orders o
JOIN first_purchase f ON o.user_id = f.user_id
GROUP BY 1, 2
ORDER BY 1, 2;
```

---

## String Functions

```sql
-- Length & case (Excel: LEN, UPPER, LOWER, PROPER)
LENGTH(name)
UPPER(name), LOWER(name)
INITCAP(name)             -- Title Case (PostgreSQL)

-- Trim whitespace (Excel: TRIM)
TRIM(name)
LTRIM(name)               -- left only
RTRIM(name)               -- right only

-- Substring (Excel: LEFT, RIGHT, MID)
LEFT(name, 5)             -- MySQL / BigQuery
RIGHT(email, 3)
SUBSTRING(name, 2, 4)     -- start pos, length
SUBSTR(name, -4)          -- SQLite: last 4 chars

-- Concatenation (Excel: CONCATENATE / &)
CONCAT(first_name, ' ', last_name)
first_name || ' ' || last_name      -- ANSI / SQLite / PostgreSQL

-- Find position (Excel: FIND)
POSITION('@' IN email)              -- PostgreSQL
INSTR(email, '@')                   -- MySQL / SQLite
CHARINDEX('@', email)               -- SQL Server

-- Replace (Excel: SUBSTITUTE)
REPLACE(phone, '-', '')

-- Pattern matching
name LIKE 'Smith%'          -- starts with Smith
name LIKE '%son'            -- ends with son
name LIKE '%an%'            -- contains "an"
name ILIKE '%smith%'        -- case-insensitive (PostgreSQL)
name ~ '^A.*n$'             -- regex (PostgreSQL)

-- Split and extract
SPLIT_PART(email, '@', 2)   -- domain from email (PostgreSQL)
REGEXP_SUBSTR(...)           -- regex extract (BigQuery / Oracle)
```

---

## NULL Handling

```sql
-- Check for NULL
WHERE col IS NULL
WHERE col IS NOT NULL

-- Replace NULL with fallback (Excel: IFERROR / IF(ISBLANK()))
COALESCE(col, 'Unknown')          -- returns first non-NULL argument
COALESCE(col1, col2, col3, 0)     -- chain of fallbacks
IFNULL(col, 0)                    -- MySQL / SQLite shorthand
NVL(col, 0)                       -- Oracle shorthand

-- NULLIF — return NULL if equal to a value (avoid division by zero)
NULLIF(denominator, 0)
revenue / NULLIF(cost, 0)         -- safe division

-- NULL in aggregates
-- COUNT(*) includes NULLs; COUNT(col) ignores them
-- SUM, AVG, MAX, MIN all ignore NULLs automatically

-- NULL in sorting
ORDER BY col NULLS LAST           -- NULLs at end (PostgreSQL / BigQuery)
ORDER BY col NULLS FIRST

-- NULL in comparisons
-- NULL = NULL → NULL (not TRUE!) — always use IS NULL
-- col != 'x' does NOT return rows where col IS NULL
```

---

## Set Operations

```sql
-- UNION: combine results, remove duplicates (slower)
SELECT product_id FROM online_orders
UNION
SELECT product_id FROM store_orders;

-- UNION ALL: combine results, keep duplicates (faster)
SELECT 'online' AS source, product_id FROM online_orders
UNION ALL
SELECT 'store',            product_id FROM store_orders;

-- INTERSECT: rows in both result sets
SELECT customer_id FROM subscribers
INTERSECT
SELECT customer_id FROM purchasers;

-- EXCEPT / MINUS: rows in first but NOT second (anti-join)
SELECT customer_id FROM all_customers
EXCEPT
SELECT customer_id FROM churned_customers;
```

---

## Analytics Patterns

### 1. Month-over-Month Growth

```sql
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date) AS month, SUM(revenue) AS rev
    FROM orders GROUP BY 1
)
SELECT
    month,
    rev,
    LAG(rev) OVER (ORDER BY month)                                      AS prev_month,
    ROUND((rev - LAG(rev) OVER (ORDER BY month))
        / NULLIF(LAG(rev) OVER (ORDER BY month), 0) * 100, 2)           AS mom_pct
FROM monthly
ORDER BY month;
```

### 2. Cohort Retention Table

```sql
WITH cohorts AS (
    SELECT user_id, DATE_TRUNC('month', MIN(order_date)) AS cohort
    FROM orders GROUP BY user_id
),
activity AS (
    SELECT o.user_id,
           c.cohort,
           DATE_TRUNC('month', o.order_date) AS active_month,
           DATEDIFF('month', c.cohort, DATE_TRUNC('month', o.order_date)) AS period
    FROM orders o JOIN cohorts c ON o.user_id = c.user_id
)
SELECT
    cohort,
    period,
    COUNT(DISTINCT user_id)                                       AS users,
    COUNT(DISTINCT user_id) * 100.0
        / FIRST_VALUE(COUNT(DISTINCT user_id)) OVER (PARTITION BY cohort ORDER BY period) AS retention_pct
FROM activity
GROUP BY cohort, period
ORDER BY cohort, period;
```

### 3. Running 7-Day Active Users (DAU / WAU)

```sql
SELECT
    activity_date,
    COUNT(DISTINCT user_id)                                                AS dau,
    COUNT(DISTINCT user_id) OVER (
        ORDER BY activity_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    )                                                                      AS wau_approx
FROM user_activity
GROUP BY activity_date
ORDER BY activity_date;
```

### 4. Percentile Bucketing (Excel: QUARTILE / PERCENTILE)

```sql
SELECT
    employee_id,
    salary,
    NTILE(4) OVER (ORDER BY salary)                              AS salary_quartile,
    CASE NTILE(10) OVER (ORDER BY salary)
        WHEN 10 THEN 'Top 10%'
        WHEN 9  THEN 'Top 20%'
        ELSE 'Bottom 80%'
    END                                                          AS salary_tier,
    PERCENT_RANK() OVER (ORDER BY salary)                        AS salary_percentile
FROM employees;
```

### 5. Deduplication — Keep Latest Record

```sql
WITH deduped AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY email ORDER BY updated_at DESC) AS rn
    FROM users
)
SELECT * FROM deduped WHERE rn = 1;
```

### 6. Funnel Analysis

```sql
SELECT
    COUNT(DISTINCT CASE WHEN step >= 1 THEN user_id END) AS step1_visit,
    COUNT(DISTINCT CASE WHEN step >= 2 THEN user_id END) AS step2_signup,
    COUNT(DISTINCT CASE WHEN step >= 3 THEN user_id END) AS step3_add_to_cart,
    COUNT(DISTINCT CASE WHEN step >= 4 THEN user_id END) AS step4_purchase,
    ROUND(COUNT(DISTINCT CASE WHEN step >= 2 THEN user_id END) * 100.0
        / NULLIF(COUNT(DISTINCT CASE WHEN step >= 1 THEN user_id END), 0), 1) AS visit_to_signup_pct
FROM user_funnel;
```

### 7. Gap & Island Detection

```sql
-- Find consecutive date ranges (islands) per user
WITH numbered AS (
    SELECT
        user_id,
        login_date,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn,
        login_date - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) * INTERVAL '1 day') AS grp
    FROM logins
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end,
       COUNT(*) AS streak_length
FROM numbered
GROUP BY user_id, grp
ORDER BY user_id, streak_start;
```

---

## Performance & Indexing Notes

| Situation | Best Practice |
|---|---|
| Filter on a column frequently | Add an index on that column |
| Join two large tables | Ensure both join keys are indexed |
| Aggregating large tables | Materialize as a summary table or use partitioning |
| SELECT * | Specify exactly the columns you need |
| Many OR conditions | Rewrite as IN (...) or UNION ALL |
| Correlated subquery | Rewrite as JOIN or window function |
| LIKE '%prefix' | Cannot use index (leading wildcard) |
| LIKE 'prefix%' | Can use index |
| ORDER BY + LIMIT | Needs index on ORDER BY column for efficiency |

```sql
-- Check query plan (PostgreSQL)
EXPLAIN ANALYZE SELECT ...;

-- Check query plan (MySQL)
EXPLAIN SELECT ...;
```

---

## Dialect Differences

| Feature | PostgreSQL | MySQL | SQLite | BigQuery | SQL Server |
|---|---|---|---|---|---|
| Truncate date | `DATE_TRUNC('month', d)` | `DATE_FORMAT(d,'%Y-%m-01')` | `strftime('%Y-%m-01', d)` | `DATE_TRUNC(d, MONTH)` | `DATETRUNC(month, d)` |
| String concat | `\|\|` or `CONCAT()` | `CONCAT()` | `\|\|` | `CONCAT()` | `+` or `CONCAT()` |
| Regex match | `~` | `REGEXP` | none | `REGEXP_CONTAINS` | none (LIKE only) |
| Limit rows | `LIMIT n` | `LIMIT n` | `LIMIT n` | `LIMIT n` | `TOP n` |
| Auto-increment | `SERIAL` / `IDENTITY` | `AUTO_INCREMENT` | `AUTOINCREMENT` | n/a | `IDENTITY(1,1)` |
| Current timestamp | `NOW()` | `NOW()` | `datetime('now')` | `CURRENT_TIMESTAMP` | `GETDATE()` |
| String length | `LENGTH()` | `LENGTH()` | `LENGTH()` | `LENGTH()` | `LEN()` |
| Full outer join | ✓ | ✗ (simulate) | ✗ (simulate) | ✓ | ✓ |
| Window functions | ✓ | ✓ (v8+) | ✓ (v3.25+) | ✓ | ✓ |
| Recursive CTEs | ✓ | ✓ (v8+) | ✓ | ✓ | ✓ |
