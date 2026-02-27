# 03. Department Highest Salary

**Difficulty:** Medium  
**Topics:** JOIN, subquery

---

## Problem

Write a SQL query to find the employee with the highest salary in each department. If there's a tie, return all employees with the maximum salary.

## Schema

```sql
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    salary INTEGER NOT NULL,
    department_id INTEGER REFERENCES departments(id)
);
```

## Sample Data

```sql
INSERT INTO departments (id, name) VALUES
(1, 'Engineering'), (2, 'Marketing'), (3, 'Sales');

INSERT INTO employees (id, name, salary, department_id) VALUES
(1, 'Alice', 85000, 1),
(2, 'Bob', 45000, 2),
(3, 'Charlie', 92000, 1),
(4, 'Diana', 55000, 3),
(5, 'Eve', 45000, 2),
(6, 'Frank', 78000, 1),
(7, 'Grace', 55000, 3);
```

## Expected Output

| department | employee | salary |
|-----------|----------|--------|
| Engineering | Charlie | 92000 |
| Marketing | Bob | 45000 |
| Marketing | Eve | 45000 |
| Sales | Diana | 55000 |
| Sales | Grace | 55000 |

---

## Solution 1: Subquery

```sql
SELECT d.name AS department, e.name AS employee, e.salary
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE e.salary = (
    SELECT MAX(e2.salary)
    FROM employees e2
    WHERE e2.department_id = e.department_id
)
ORDER BY e.salary DESC, d.name;
```

## Solution 2: Window Function

```sql
WITH ranked AS (
    SELECT
        d.name AS department,
        e.name AS employee,
        e.salary,
        RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS rnk
    FROM employees e
    JOIN departments d ON e.department_id = d.id
)
SELECT department, employee, salary
FROM ranked
WHERE rnk = 1
ORDER BY salary DESC, department;
```

## Explanation

- **Solution 1** uses a correlated subquery — for each employee, it checks if their salary equals the max salary in their department. Handles ties naturally.
- **Solution 2** uses `RANK()` which assigns the same rank to tied values (both get rank 1), then filters to rank 1. Generally preferred in interviews because it's more readable and extensible (easy to change to "top 3" by filtering `rnk <= 3`).

## Follow-Up Questions

1. How would you find the top 3 salaries per department?
2. What's the difference between `RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()` here?
