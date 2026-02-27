# 09. Nth Highest Salary

**Difficulty:** Medium  
**Topics:** Window functions, parameterized query

---

## Problem

Write a SQL query (or function) to find the Nth highest **distinct** salary from the `employees` table. If there is no Nth highest salary, return `NULL`.

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
(5, 'Eve', 65000),
(6, 'Frank', 78000),
(7, 'Grace', 105000);
```

## Expected Output (N = 3)

| nth_highest_salary |
|-------------------|
| 85000 |

Distinct salaries ranked: 105000 (1st), 92000 (2nd), 85000 (3rd), 78000 (4th), 65000 (5th)

---

## Solution 1: DENSE_RANK Window Function

```sql
SELECT salary AS nth_highest_salary
FROM (
    SELECT
        DISTINCT salary,
        DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
) ranked
WHERE rnk = 3;  -- Replace 3 with N
```

## Solution 2: LIMIT/OFFSET

```sql
SELECT (
    SELECT DISTINCT salary
    FROM employees
    ORDER BY salary DESC
    LIMIT 1 OFFSET 2  -- OFFSET is N-1
) AS nth_highest_salary;
```

## Solution 3: PostgreSQL Function

```sql
CREATE OR REPLACE FUNCTION nth_highest_salary(n INT)
RETURNS TABLE(salary INT) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT e.salary
    FROM employees e
    ORDER BY e.salary DESC
    LIMIT 1 OFFSET n - 1;
END;
$$ LANGUAGE plpgsql;

-- Usage:
SELECT * FROM nth_highest_salary(3);
```

## Explanation

- **Solution 1** ranks distinct salaries and picks the one with rank = N. Using `DISTINCT` before ranking ensures tied salaries don't affect the rank count.
- **Solution 2** sorts distinct salaries and skips N-1 rows. The outer subquery wrapper ensures NULL is returned (instead of empty result set) when N exceeds the number of distinct salaries.
- **Solution 3** encapsulates the logic in a reusable function — some interview problems specifically ask you to write this as a function.

**Common interview trap:** Forgetting to handle duplicates. If two employees earn 92000, that's still only one distinct salary level. Use `DISTINCT` or `DENSE_RANK`.

## Follow-Up Questions

1. How would you return the names of employees earning the Nth highest salary?
2. What's the time complexity of each approach? Which scales better?
3. How would you find the Nth highest salary per department?
