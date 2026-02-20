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

# Useful methods
arr.reverse()         # O(n) - reverse in-place
arr.count(x)          # O(n) - count occurrences
arr.index(x)          # O(n) - find first index
arr.extend(other)     # O(k) - add all from other
```

### Dictionary (Hash Table)
```python
# Creation
d = {'a': 1, 'b': 2}
d = dict(a=1, b=2)
d = {}

# Common operations - Time complexity
d[key] = value        # O(1) - insert/update
d[key]                # O(1) - access (KeyError if missing)
d.get(key, default)   # O(1) - safe access with default
key in d              # O(1) - check existence
del d[key]            # O(1) - delete
len(d)                # O(1) - size

# Useful methods
d.keys()              # dict_keys view
d.values()            # dict_values view
d.items()             # dict_items view (key, value pairs)
d.pop(key, default)   # O(1) - remove and return
d.setdefault(key, default)  # O(1) - get or set default
```

### Set (Hash Set)
```python
# Creation
s = {1, 2, 3}
s = set([1, 2, 2, 3])  # {1, 2, 3}
s = set()              # Empty set (NOT {})

# Common operations - Time complexity
s.add(x)              # O(1) - add element
s.remove(x)           # O(1) - remove (KeyError if missing)
s.discard(x)          # O(1) - remove if exists
x in s                # O(1) - check membership
len(s)                # O(1) - size

# Set operations
s1 | s2               # O(len(s1) + len(s2)) - union
s1 & s2               # O(min(len(s1), len(s2))) - intersection
s1 - s2               # O(len(s1)) - difference
s1 ^ s2               # O(len(s1) + len(s2)) - symmetric difference
```

### Tuple (Immutable List)
```python
# Creation
t = (1, 2, 3)
t = 1, 2, 3           # Parentheses optional
t = tuple([1, 2, 3])

# Operations (all read-only)
t[i]                  # O(1) - access
len(t)                # O(1) - length
x in t                # O(n) - search
t.count(x)            # O(n) - count
t.index(x)            # O(n) - find index

# Use cases: dictionary keys, multiple return values, unpacking
```

### String (Immutable)
```python
# Common operations
s[i]                  # O(1) - access character
len(s)                # O(1) - length
s + t                 # O(n + m) - concatenation (creates new string)
s * n                 # O(n * len(s)) - repeat
s.split(delim)        # O(n) - split into list
delim.join(list)      # O(n) - join list into string
s.lower(), s.upper()  # O(n) - case conversion
s.strip()             # O(n) - remove whitespace
s.replace(old, new)   # O(n) - replace substring
s.startswith(prefix)  # O(k) - check prefix
s.endswith(suffix)    # O(k) - check suffix

# String is immutable - use list for building
chars = list(s)       # Convert to list
chars[0] = 'X'        # Modify
s = ''.join(chars)    # Convert back
```

---

## Collections Module

### deque (Double-Ended Queue)
```python
from collections import deque

# Creation
q = deque([1, 2, 3])

# Operations - Time complexity
q.append(x)           # O(1) - add to right
q.appendleft(x)       # O(1) - add to left
q.pop()               # O(1) - remove from right
q.popleft()           # O(1) - remove from left
q[i]                  # O(n) - random access (slow!)

# Use cases: BFS queue, sliding window
```

### Counter (Count Elements)
```python
from collections import Counter

# Creation
c = Counter([1, 2, 2, 3, 3, 3])  # Counter({3: 3, 2: 2, 1: 1})
c = Counter("hello")              # Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})

# Operations
c[key]                # O(1) - get count (0 if missing)
c.most_common(k)      # O(n log k) - top k elements
c1 + c2               # Add counts
c1 - c2               # Subtract counts (keep positive only)
```

### defaultdict (Dict with Default)
```python
from collections import defaultdict

# Creation
d = defaultdict(int)        # Default 0
d = defaultdict(list)       # Default []
d = defaultdict(set)        # Default set()

# Usage
d[key].append(value)        # No KeyError if key missing
```

---

## Heapq (Min Heap)

```python
import heapq

# Creation
heap = []
heapq.heapify(arr)    # O(n) - convert list to heap in-place

# Operations - Time complexity
heapq.heappush(heap, x)      # O(log n) - add
heapq.heappop(heap)          # O(log n) - remove and return min
heap[0]                      # O(1) - peek at min
heapq.heappushpop(heap, x)   # O(log n) - push then pop (efficient)
heapq.heapreplace(heap, x)   # O(log n) - pop then push (efficient)

# Max heap (negate values)
max_heap = []
heapq.heappush(max_heap, -x)
max_val = -heapq.heappop(max_heap)

# K largest/smallest
heapq.nlargest(k, arr)       # O(n log k)
heapq.nsmallest(k, arr)      # O(n log k)
```

---

## Common Algorithm Patterns

### Two Pointers
```python
# Pattern: Two ends moving inward
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []

# Use cases: Two Sum II, Container With Most Water, Valid Palindrome
```

### Sliding Window
```python
# Pattern: Fixed or dynamic window
def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]  # Slide window
        max_sum = max(max_sum, window_sum)
    
    return max_sum

# Use cases: Longest Substring, Max Sum Subarray, Sliding Window Maximum
```

### Binary Search
```python
# Pattern: Search in sorted array
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Template for "find first/last occurrence"
def binary_search_leftmost(arr, target):
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left

# Use cases: Binary Search, Search Rotated Array, Find Peak Element
```

### DFS (Depth-First Search)
```python
# Pattern: Recursive traversal
def dfs(node, visited):
    if node in visited:
        return
    visited.add(node)
    
    # Process node
    
    for neighbor in node.neighbors:
        dfs(neighbor, visited)

# Iterative with stack
def dfs_iterative(start):
    stack = [start]
    visited = set()
    
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        
        # Process node
        
        for neighbor in node.neighbors:
            if neighbor not in visited:
                stack.append(neighbor)

# Use cases: Number of Islands, Clone Graph, Path Finding
```

### BFS (Breadth-First Search)
```python
from collections import deque

# Pattern: Level-by-level traversal
def bfs(start):
    queue = deque([start])
    visited = {start}
    
    while queue:
        node = queue.popleft()
        
        # Process node
        
        for neighbor in node.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# With levels (for tree level-order)
def bfs_levels(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result

# Use cases: Binary Tree Level Order, Shortest Path, Word Ladder
```

### Dynamic Programming
```python
# Pattern: Bottom-up with memoization
def fib(n):
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]

# Space-optimized (only need last 2 values)
def fib_optimized(n):
    if n <= 1:
        return n
    
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current
    
    return prev1

# Use cases: Coin Change, Longest Increasing Subsequence, House Robber
```

---

## Useful Built-in Functions

```python
# Math
min(a, b, c)          # Minimum
max(a, b, c)          # Maximum
abs(x)                # Absolute value
pow(x, y)             # x to the power y
divmod(a, b)          # (a // b, a % b)

# Iterables
sum(arr)              # Sum of elements
any(arr)              # True if any element is truthy
all(arr)              # True if all elements are truthy
enumerate(arr)        # Iterator of (index, value) pairs
zip(a, b)             # Iterator of pairs from two iterables
reversed(arr)         # Reverse iterator
sorted(arr)           # New sorted list
map(func, arr)        # Apply function to all elements
filter(func, arr)     # Keep elements where func returns True

# Type conversions
int(x)                # Convert to integer
str(x)                # Convert to string
list(x)               # Convert to list
set(x)                # Convert to set
ord('A')              # Character to ASCII (65)
chr(65)               # ASCII to character ('A')
```

---

## Common Edge Cases to Test

```python
# Arrays/Lists
[]                    # Empty
[1]                   # Single element
[1, 1, 1]             # All duplicates
[-1, 0, 1]            # Mixed positive/negative

# Strings
""                    # Empty
"a"                   # Single character
"   "                 # Only whitespace
"aaa"                 # All same character

# Numbers
0                     # Zero
-1                    # Negative
2**31 - 1             # Max 32-bit int
float('inf')          # Infinity

# Binary tree
None                  # Empty tree
# Single node         # Just root
# Unbalanced          # All left or all right

# Graphs
# Disconnected        # Multiple components
# Cycle               # Has cycle
# Single node         # No edges
```

---

## Python Tricks for Interviews

```python
# List comprehension
squares = [x**2 for x in range(10)]
evens = [x for x in range(10) if x % 2 == 0]

# Dict comprehension
char_count = {ch: s.count(ch) for ch in set(s)}

# Multiple assignment
a, b = b, a           # Swap
a = b = c = 0         # Initialize multiple

# Ternary operator
max_val = a if a > b else b

# Unpacking
first, *middle, last = [1, 2, 3, 4, 5]  # first=1, middle=[2,3,4], last=5

# Negative indexing
arr[-1]               # Last element
arr[-2]               # Second to last

# Slicing
arr[start:end:step]
arr[::-1]             # Reverse array
arr[::2]              # Every other element

# Initialization
arr = [0] * n         # [0, 0, 0, ..., 0] (n times)
matrix = [[0] * cols for _ in range(rows)]  # 2D array

# Infinity
float('inf')          # Positive infinity
float('-inf')         # Negative infinity

# String to list and back
chars = list(s)       # "hello" -> ['h', 'e', 'l', 'l', 'o']
s = ''.join(chars)    # ['h', 'i'] -> "hi"
```

---

## When to Use Each Data Structure

| Need | Use |
|------|-----|
| Fast lookup by key | dict or set |
| Track frequencies | Counter |
| Maintain sorted order | heapq or sorted list |
| FIFO queue | deque (use as queue) |
| LIFO stack | list (append/pop) or deque |
| Both ends access | deque |
| Sliding window | deque |
| Graph adjacency | dict of lists |
| Tree node | class with left/right |
| Undo/redo | two stacks |

---

## Quick Debugging

```python
# Print with label
print(f"arr: {arr}")

# Print type
print(type(x))

# Print all attributes
print(dir(obj))

# Interactive debugging
import pdb; pdb.set_trace()  # Pause here

# Assert for testing
assert len(arr) > 0, "Array should not be empty"
```

---

## Complexity Goal by Problem Type

| Problem Type | Target Time | Target Space |
|--------------|-------------|--------------|
| Two Sum family | O(n) | O(n) |
| Binary Search | O(log n) | O(1) |
| Sorting required | O(n log n) | O(1) or O(n) |
| Matrix traversal | O(rows * cols) | O(1) or O(rows * cols) |
| Tree traversal | O(n) | O(h) recursion stack |
| Graph BFS/DFS | O(V + E) | O(V) |
| Dynamic Programming | O(n²) or better | O(n) |

---

This cheatsheet covers 80% of what you need for coding interviews. Keep it handy during practice sessions!
