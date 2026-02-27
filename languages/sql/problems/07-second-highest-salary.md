# 07. Second Highest Salary

**Difficulty:** Medium  
**Topics:** Subquery, LIMIT/OFFSET, NULL handling

---

## Problem

Write a SQL query to find the second highest salary from the `employees` table. If there is no second highest salary (e.g., all salaries are the same), return `NULL`.

## Schema

```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    salary INTEGER NOT NULL
);
```

## Sample Data

```sql
INSERT INTO employees (id, name, salary) VALUES
(1, 'Alice', 85000),
(2, 'Bob', 92000),
(3, 'Charlie', 78000),
(4, 'Diana', 92000),
(5, 'Eve', 65000);
```

## Expected Output

| second_highest_salary |
|----------------------|
| 85000 |

---

## Solution 1: Subquery with DISTINCT

```sql
SELECT MAX(salary) AS second_highest_salary
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

## Solution 2: LIMIT/OFFSET

```sql
SELECT (
    SELECT DISTINCT salary
    FROM employees
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
) AS second_highest_salary;
```

## Solution 3: DENSE_RANK

```sql
SELECT salary AS second_highest_salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
) t
WHERE rnk = 2
LIMIT 1;
```

## Explanation

- **Solution 1** finds the max salary, then finds the max salary that's less than that. Naturally returns NULL if all salaries are the same.
- **Solution 2** gets distinct salaries sorted descending and skips the first one. Wrapping it in a subquery ensures NULL is returned if there's no second value (without the outer SELECT, you'd get an empty result set instead of NULL).
- **Solution 3** ranks salaries and picks rank 2. Most generalizable — easy to change to Nth highest.
- The tricky edge case interviewers watch for: what happens when there's only one distinct salary? Solutions 1 and 2 both correctly return NULL.

## Follow-Up Questions

1. How would you generalize this to the Nth highest salary?
2. What's the difference between getting an empty result set vs. a row containing NULL?
