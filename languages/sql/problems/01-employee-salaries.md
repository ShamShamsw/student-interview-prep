# 01. Employee Salaries

**Difficulty:** Easy  
**Topics:** SELECT, WHERE, ORDER BY

---

## Problem

Write a SQL query to find all employees who earn more than $50,000 per year. Return their name, department, and salary, ordered by salary descending.

## Schema

```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary INTEGER NOT NULL,
    hire_date DATE NOT NULL
);
```

## Sample Data

```sql
INSERT INTO employees (id, name, department, salary, hire_date) VALUES
(1, 'Alice', 'Engineering', 85000, '2022-03-15'),
(2, 'Bob', 'Marketing', 45000, '2021-06-01'),
(3, 'Charlie', 'Engineering', 92000, '2020-01-10'),
(4, 'Diana', 'Sales', 55000, '2023-01-20'),
(5, 'Eve', 'Marketing', 48000, '2022-09-05'),
(6, 'Frank', 'Engineering', 78000, '2021-11-30'),
(7, 'Grace', 'Sales', 62000, '2020-07-15');
```

## Expected Output

| name | department | salary |
|------|-----------|--------|
| Charlie | Engineering | 92000 |
| Alice | Engineering | 85000 |
| Frank | Engineering | 78000 |
| Grace | Sales | 62000 |
| Diana | Sales | 55000 |

---

## Solution

```sql
SELECT name, department, salary
FROM employees
WHERE salary > 50000
ORDER BY salary DESC;
```

## Explanation

- `WHERE salary > 50000` filters to only rows matching the condition
- `ORDER BY salary DESC` sorts the results from highest to lowest
- This is a simple table scan — for large tables, an index on `salary` would speed this up

## Follow-Up Questions

1. How would you also show each employee's rank within their department?
2. What happens if you need employees earning more than the company average? (Hint: subquery)
