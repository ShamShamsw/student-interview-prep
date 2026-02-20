````markdown
# Python Interview Cheatsheet

Quick reference for common patterns, complexity, and data structures used in coding interviews.

## Time Complexity Cheat Sheet

| Complexity | Name | Example Operations |
|------------|------|-------------------|
| O(1) | Constant | Array access, hash table lookup, stack push/pop |
| O(log n) | Logarithmic | Binary search, balanced tree operations |
| O(n) | Linear | Array traversal, linked list traversal |
| O(n log n) | Linearithmic | Merge sort, heap sort, efficient sorting |
| O(n²) | Quadratic | Nested loops, bubble sort |
| O(n³) | Cubic | Triple nested loops |
| O(2ⁿ) | Exponential | Recursive fibonacci (naive), subset generation |
| O(n!) | Factorial | Permutations, traveling salesman (brute force) |

**Goal in interviews:** O(n log n) or better for most problems.

---

## Python Built-in Data Structures

### List (Dynamic Array)
```python
# Creation
arr = [1, 2, 3]
arr = list(range(5))  # [0, 1, 2, 3, 4]

# Common operations - Time complexity
arr.append(x)         # O(1) - add to end
arr.pop()             # O(1) - remove from end
arr.insert(i, x)      # O(n) - insert at index
arr[i]                # O(1) - access
len(arr)              # O(1) - length
x in arr              # O(n) - search
arr.sort()            # O(n log n) - in-place sort
sorted(arr)           # O(n log n) - returns new list
```

---

## Collections Module (high level)

- `deque` for O(1) pops from both ends
- `Counter` for frequency counting
- `defaultdict` for convenient grouping

---

## Common Algorithm Patterns (short)

- Two pointers: use for sorted arrays or pair-sum patterns
- Sliding window: use for contiguous subarray problems
- Binary search: template for index/search in sorted data
- DFS/BFS: graph traversal templates (recursive or stack/queue)
- DP: memoize subproblems or bottom-up table

````
