# 32. Number of Islands

Difficulty: Medium  
Topics: graph, depth-first-search, breadth-first-search, matrix

Statement
Given an `m x n` 2D binary grid `grid` where `'1'` represents land and `'0'` represents water, return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.

Examples
- Input: `grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]`  
  Output: `3`

Constraints
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 300`
- `grid[i][j]` is `'0'` or `'1'`

Hints (optional)
- Traverse every cell; when you find unvisited land, flood-fill it and increment count.

Canonical solution
- `/languages/python/problems/solutions/32-number-of-islands.py`
