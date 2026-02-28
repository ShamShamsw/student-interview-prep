# SQL Interview Prep

Structured query language practice for technical interviews — from basic SELECTs to advanced window functions and query optimization.

## Why SQL Matters in Interviews

SQL appears in backend, data engineering, fullstack, and even some frontend interviews. Employers test it because:
- Every production application stores data — you'll interact with databases constantly
- SQL skills reveal how you think about data relationships and efficiency
- Many "algorithmic" problems have elegant SQL solutions

## Current Problems

| # | Problem | Difficulty | Topics |
|---|---------|------------|--------|
| 01 | [Employee Salaries](problems/01-employee-salaries.md) | Easy | SELECT, WHERE, ORDER BY |
| 02 | [Duplicate Emails](problems/02-duplicate-emails.md) | Easy | GROUP BY, HAVING |
| 03 | [Department Highest Salary](problems/03-department-highest-salary.md) | Medium | JOIN, subquery |
| 04 | [Consecutive Numbers](problems/04-consecutive-numbers.md) | Medium | Self-join, LAG/LEAD |
| 05 | [Rank Scores](problems/05-rank-scores.md) | Medium | Window functions, DENSE_RANK |
| 06 | [Rising Temperature](problems/06-rising-temperature.md) | Easy | Self-join, DATE functions |
| 07 | [Second Highest Salary](problems/07-second-highest-salary.md) | Medium | Subquery, LIMIT/OFFSET, NULL handling |
| 08 | [Customers Who Never Order](problems/08-customers-who-never-order.md) | Easy | LEFT JOIN, IS NULL |
| 09 | [Nth Highest Salary](problems/09-nth-highest-salary.md) | Medium | Window functions, parameterized query |
| 10 | [Managers With At Least 5 Reports](problems/10-managers-with-reports.md) | Medium | Self-join, GROUP BY, HAVING |
| 11 | [Monthly Revenue Growth](problems/11-monthly-revenue-growth.md) | Medium | LAG, CTE, date functions, MoM % |
| 12 | [Cohort Retention Rate](problems/12-cohort-retention.md) | Hard | CTE, date arithmetic, retention analysis |
| 13 | [Running Total & Percentile](problems/13-running-total-percentile.md) | Medium | SUM OVER, NTILE, PERCENT_RANK |
| 14 | [Funnel Conversion Rates](problems/14-funnel-conversion.md) | Medium | Conditional aggregation, CASE WHEN |

## How to Practice

You can practice these problems using any of these tools:

1. **SQLite** (simplest — comes with Python):
   ```bash
   python -c "import sqlite3; print('SQLite is available')"
   sqlite3 practice.db < setup.sql
   ```

2. **PostgreSQL** (recommended for interview realism):
   ```bash
   psql -U postgres -f setup.sql
   ```

3. **Online playgrounds**:
   - [DB Fiddle](https://www.db-fiddle.com/)
   - [SQLite Online](https://sqliteonline.com/)
   - [LeetCode Database Problems](https://leetcode.com/problemset/database/)

## Key SQL Concepts for Interviews

### Must-Know (Every Interview)
- `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`
- `JOIN` types: INNER, LEFT, RIGHT, FULL OUTER
- `GROUP BY` + aggregate functions (`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`)
- `HAVING` (filtering groups)
- Subqueries (correlated and uncorrelated)

### Frequently Tested
- `DISTINCT`, `UNION` vs `UNION ALL`
- `CASE WHEN` expressions
- `NULL` handling (`IS NULL`, `COALESCE`, `IFNULL`)
- `EXISTS` vs `IN`
- Date/time functions

### Advanced (Senior / Data Roles)
- Window functions: `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD`
- CTEs (Common Table Expressions) with `WITH`
- Self-joins
- `EXPLAIN` / query plans
- Indexing strategies

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md). Each SQL problem should include:
1. Problem description and sample data
2. Expected output
3. At least one solution with explanation
4. Complexity discussion (what indexes would help?)
