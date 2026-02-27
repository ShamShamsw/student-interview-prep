# 10. Managers With At Least 5 Reports

**Difficulty:** Medium  
**Topics:** Self-join, GROUP BY, HAVING

---

## Problem

Write a SQL query to find managers who have at least 5 direct reports. Return the manager's name and the number of people they manage.

## Schema

```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    manager_id INTEGER REFERENCES employees(id)
);
```

## Sample Data

```sql
INSERT INTO employees (id, name, department, manager_id) VALUES
(1, 'Alice', 'Engineering', NULL),       -- CEO, no manager
(2, 'Bob', 'Engineering', 1),
(3, 'Charlie', 'Engineering', 1),
(4, 'Diana', 'Engineering', 1),
(5, 'Eve', 'Engineering', 1),
(6, 'Frank', 'Engineering', 1),
(7, 'Grace', 'Marketing', 1),            -- Alice manages 6 people
(8, 'Hank', 'Marketing', 7),
(9, 'Ivy', 'Marketing', 7),
(10, 'Jack', 'Sales', 2),
(11, 'Kara', 'Sales', 2);
```

## Expected Output

| manager_name | report_count |
|-------------|-------------|
| Alice | 6 |

---

## Solution 1: Self-Join

```sql
SELECT m.name AS manager_name, COUNT(*) AS report_count
FROM employees e
JOIN employees m ON e.manager_id = m.id
GROUP BY m.id, m.name
HAVING COUNT(*) >= 5
ORDER BY report_count DESC;
```

## Solution 2: Subquery

```sql
SELECT e.name AS manager_name, sub.report_count
FROM employees e
JOIN (
    SELECT manager_id, COUNT(*) AS report_count
    FROM employees
    WHERE manager_id IS NOT NULL
    GROUP BY manager_id
    HAVING COUNT(*) >= 5
) sub ON e.id = sub.manager_id
ORDER BY sub.report_count DESC;
```

## Explanation

- **Solution 1** joins the table to itself — each employee row (`e`) is matched to its manager row (`m`). Then we group by manager and count how many employees report to them. `HAVING >= 5` filters to managers with at least 5 reports.
- **Solution 2** first finds all manager IDs with 5+ reports as a subquery, then joins back to get the manager's name. Some find this more readable.
- The self-join pattern is common in hierarchical data (org charts, category trees, threaded comments). Whenever a table references itself via a foreign key, expect self-join questions.

## Follow-Up Questions

1. How would you find ALL levels of reports (not just direct reports)? (Hint: recursive CTE)
2. How would you find managers whose reports span more than one department?
3. What index would you add to speed this query up?
