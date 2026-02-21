# Python Interview Cheatsheet

> Comprehensive quick-reference for Python syntax, data structures, algorithms, and coding-interview patterns.

---

## Table of Contents

1. [Time & Space Complexity](#time--space-complexity)
2. [Python Basics](#python-basics)
3. [Strings](#strings)
4. [Lists (Dynamic Arrays)](#lists-dynamic-arrays)
5. [Tuples](#tuples)
6. [Dictionaries (Hash Maps)](#dictionaries-hash-maps)
7. [Sets](#sets)
8. [Stacks & Queues](#stacks--queues)
9. [Heaps / Priority Queues](#heaps--priority-queues)
10. [Collections Module](#collections-module)
11. [Linked Lists](#linked-lists)
12. [Trees & Binary Search Trees](#trees--binary-search-trees)
13. [Graphs](#graphs)
14. [Sorting Algorithms](#sorting-algorithms)
15. [Binary Search](#binary-search)
16. [Two Pointers](#two-pointers)
17. [Sliding Window](#sliding-window)
18. [Recursion & Backtracking](#recursion--backtracking)
19. [Dynamic Programming](#dynamic-programming)
20. [Bit Manipulation](#bit-manipulation)
21. [Math & Number Theory](#math--number-theory)
22. [String Algorithms](#string-algorithms)
23. [Intervals](#intervals)
24. [Tries (Prefix Trees)](#tries-prefix-trees)
25. [Union-Find (Disjoint Set)](#union-find-disjoint-set)
26. [Monotonic Stack / Queue](#monotonic-stack--queue)
27. [Topological Sort](#topological-sort)
28. [Shortest Path Algorithms](#shortest-path-algorithms)
29. [Comprehensions & Generators](#comprehensions--generators)
30. [Useful Built-in Functions](#useful-built-in-functions)
31. [Itertools Module](#itertools-module)
32. [Functools Module](#functools-module)
33. [Bisect Module](#bisect-module)
34. [Regular Expressions](#regular-expressions)
35. [Object-Oriented Python](#object-oriented-python)
36. [Error Handling](#error-handling)
37. [File I/O](#file-io)
38. [Type Hints](#type-hints)
39. [Common Interview Gotchas](#common-interview-gotchas)
40. [Complexity Reference Table](#complexity-reference-table)

---

## Time & Space Complexity

| Complexity | Name | Example Operations |
|------------|------|-------------------|
| O(1) | Constant | Array access, hash lookup, stack push/pop |
| O(log n) | Logarithmic | Binary search, balanced BST ops |
| O(n) | Linear | Array traversal, linear search |
| O(n log n) | Linearithmic | Merge sort, heap sort, Tim sort |
| O(n²) | Quadratic | Nested loops, bubble/selection/insertion sort |
| O(n³) | Cubic | Triple nested loops, naive matrix multiply |
| O(2ⁿ) | Exponential | Subsets, naive recursive Fibonacci |
| O(n!) | Factorial | Permutations, brute-force TSP |

**Interview target:** aim for O(n log n) or better. If you're writing O(n²), ask yourself if a hash map or sort can improve it.

### Space Complexity Rules of Thumb

- Recursion: O(depth) for call stack
- Hash map / set of n items: O(n)
- 2D DP table: O(n × m)
- In-place sort (e.g., quicksort): O(log n) stack space
- BFS queue can hold up to O(n) nodes

---

## Python Basics

### Variables & Assignment

```python
x = 10              # int
y = 3.14            # float
name = "Alice"      # str
is_valid = True     # bool
nothing = None      # NoneType

# Multiple assignment
a, b, c = 1, 2, 3
a, b = b, a         # swap without temp variable

# Augmented assignment
x += 5   # x = x + 5
x -= 2   # x = x - 2
x *= 3   # x = x * 3
x //= 2  # x = x // 2 (floor division)
x **= 2  # x = x ** 2 (power)
x %= 3   # x = x % 3 (modulo)
```

### Numeric Types

```python
# Integers have arbitrary precision in Python
big = 10**100                   # no overflow!
hex_val = 0xFF                  # 255
bin_val = 0b1010                # 10
oct_val = 0o17                  # 15

# Float operations
float('inf')                    # positive infinity
float('-inf')                   # negative infinity
float('nan')                    # not a number
import math
math.isnan(float('nan'))        # True
math.isinf(float('inf'))       # True
math.floor(3.7)                 # 3
math.ceil(3.2)                  # 4
round(3.14159, 2)               # 3.14

# Division
7 / 2      # 3.5 (true division)
7 // 2     # 3   (floor division)
-7 // 2    # -4  (floors toward negative infinity!)
7 % 2      # 1   (modulo)
divmod(7, 2)  # (3, 1) → (quotient, remainder)
```

### Comparison & Logic

```python
# Comparison operators
==  !=  <  >  <=  >=

# Identity vs equality
a is b      # same object in memory
a == b      # same value

# Chained comparisons
1 < x < 10          # True if x in (1, 10)
a <= b <= c          # True if a ≤ b ≤ c

# Logical operators
and  or  not
# Short-circuit: `a and b` returns a if falsy, else b
#                `a or b`  returns a if truthy, else b

# Falsy values: None, False, 0, 0.0, '', [], {}, set(), tuple()
# Everything else is truthy
```

### Control Flow

```python
# if / elif / else
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")

# Ternary expression
result = "even" if x % 2 == 0 else "odd"

# for loop
for i in range(5):        # 0, 1, 2, 3, 4
    pass
for i in range(2, 8):     # 2, 3, 4, 5, 6, 7
    pass
for i in range(0, 10, 2): # 0, 2, 4, 6, 8
    pass
for i in range(10, 0, -1):# 10, 9, ..., 1
    pass

# for-else (else runs if loop completes without break)
for item in arr:
    if item == target:
        break
else:
    print("target not found")

# while loop
while condition:
    pass

# while-else
while stack:
    node = stack.pop()
else:
    print("stack empty")

# enumerate & zip
for i, val in enumerate(arr):           # index + value
    pass
for i, val in enumerate(arr, start=1):  # 1-indexed
    pass
for a, b in zip(list1, list2):          # parallel iteration
    pass
for a, b, c in zip(l1, l2, l3):        # three lists at once
    pass
```

### Functions

```python
def greet(name: str, greeting: str = "Hello") -> str:
    """Return a greeting string."""
    return f"{greeting}, {name}!"

# *args and **kwargs
def func(*args, **kwargs):
    # args is a tuple of positional args
    # kwargs is a dict of keyword args
    pass

# Lambda (anonymous function)
square = lambda x: x ** 2
add = lambda a, b: a + b

# Functions are first-class objects
fns = [abs, len, sum]
result = fns[0](-5)  # 5
```

---

## Strings

```python
s = "hello world"

# Indexing & slicing
s[0]          # 'h'
s[-1]         # 'd'
s[0:5]        # 'hello'
s[:5]         # 'hello'
s[6:]         # 'world'
s[::-1]       # 'dlrow olleh' (reversed)
s[::2]        # 'hlowrd' (every other char)

# Strings are IMMUTABLE
# s[0] = 'H'  # TypeError!

# Common methods
s.upper()                   # 'HELLO WORLD'
s.lower()                   # 'hello world'
s.capitalize()              # 'Hello world'
s.title()                   # 'Hello World'
s.strip()                   # remove leading/trailing whitespace
s.lstrip()                  # remove leading whitespace
s.rstrip()                  # remove trailing whitespace
s.split()                   # ['hello', 'world']
s.split(',')                # split by delimiter
'-'.join(['a', 'b', 'c'])   # 'a-b-c'
s.replace('hello', 'hi')    # 'hi world'
s.find('world')             # 6 (index, -1 if not found)
s.index('world')            # 6 (raises ValueError if not found)
s.count('l')                # 3
s.startswith('hello')       # True
s.endswith('world')         # True
s.isalpha()                 # False (has space)
s.isdigit()                 # False
s.isalnum()                 # False
s.islower()                 # True (for alphabetic chars)

# String formatting
name, age = "Alice", 30
f"Name: {name}, Age: {age}"              # f-string (preferred)
"Name: {}, Age: {}".format(name, age)    # .format()
f"{3.14159:.2f}"                          # '3.14'
f"{42:08b}"                               # '00101010' (binary, 8 chars)
f"{1000000:,}"                            # '1,000,000'

# Character operations
ord('A')     # 65  (char → ASCII int)
chr(65)      # 'A' (int → char)
ord('a')     # 97
ord('0')     # 48

# String ↔ list conversion
list("abc")              # ['a', 'b', 'c']
''.join(['a', 'b', 'c'])  # 'abc'

# Checking character types
c.isalpha()    # letter?
c.isdigit()    # digit?
c.isalnum()    # letter or digit?
c.isspace()    # whitespace?
c.isupper()    # uppercase?
c.islower()    # lowercase?
```

### String Complexity

| Operation | Time |
|-----------|------|
| Index `s[i]` | O(1) |
| Slice `s[a:b]` | O(b − a) |
| Concatenation `s + t` | O(len(s) + len(t)) |
| `in` substring check | O(n × m) worst |
| `s.join(list)` | O(total length) |
| `s.split()` | O(n) |
| `s.replace()` | O(n) |

> **Tip:** Repeated string concatenation in a loop is O(n²). Use `''.join(parts)` instead.

---

## Lists (Dynamic Arrays)

```python
# Creation
arr = [1, 2, 3, 4, 5]
arr = list(range(10))           # [0, 1, ..., 9]
arr = [0] * 10                  # [0, 0, 0, ..., 0]
matrix = [[0] * cols for _ in range(rows)]  # 2D list (correct way!)
# WRONG: [[0]*cols]*rows  ← all rows share same reference!

# Indexing & slicing
arr[0]           # first
arr[-1]          # last
arr[1:4]         # [1, 2, 3]
arr[::-1]        # reversed copy
arr[::2]         # every other element

# Modification
arr.append(6)            # O(1) amortized — add to end
arr.pop()                # O(1) — remove & return last
arr.pop(0)               # O(n) — remove & return first (slow!)
arr.insert(i, val)       # O(n) — insert at index i
arr.extend([7, 8])       # O(k) — append iterable
arr.remove(val)          # O(n) — remove first occurrence
del arr[i]               # O(n) — delete by index
arr[i] = val             # O(1) — set by index

# Searching & counting
val in arr               # O(n) — membership test
arr.index(val)           # O(n) — first index of val (ValueError if absent)
arr.count(val)           # O(n) — count occurrences

# Sorting
arr.sort()                       # O(n log n) — in-place, ascending
arr.sort(reverse=True)           # in-place, descending
arr.sort(key=lambda x: x[1])    # sort by custom key
sorted(arr)                      # returns new sorted list
sorted(arr, key=abs)             # sort by absolute value

# Other useful operations
arr.reverse()            # O(n) — in-place reverse
arr.copy()               # O(n) — shallow copy
arr2 = arr[:]            # O(n) — shallow copy via slice
min(arr)                 # O(n)
max(arr)                 # O(n)
sum(arr)                 # O(n)
len(arr)                 # O(1)

# Unpacking
first, *rest = [1, 2, 3, 4]     # first=1, rest=[2,3,4]
*rest, last = [1, 2, 3, 4]      # rest=[1,2,3], last=4
first, *mid, last = [1,2,3,4]   # first=1, mid=[2,3], last=4

# List as stack
stack = []
stack.append(1)    # push
stack.pop()        # pop (LIFO)
stack[-1]          # peek
```

### 2D List / Matrix Patterns

```python
rows, cols = 3, 4

# Create 2D matrix
matrix = [[0] * cols for _ in range(rows)]

# Iterate 2D matrix
for r in range(rows):
    for c in range(cols):
        val = matrix[r][c]

# 4-directional neighbors
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
for dr, dc in directions:
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols:
        # process matrix[nr][nc]
        pass

# 8-directional neighbors
directions_8 = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

# Transpose a matrix
transposed = list(zip(*matrix))  # returns list of tuples
transposed = [list(row) for row in zip(*matrix)]  # list of lists

# Rotate 90° clockwise
rotated = [list(row) for row in zip(*matrix[::-1])]

# Flatten 2D → 1D
flat = [val for row in matrix for val in row]
```

---

## Tuples

```python
t = (1, 2, 3)
t = tuple([1, 2, 3])  # from list
t = (1,)               # single-element tuple (need trailing comma!)
a, b, c = t            # unpacking

# Immutable — cannot modify after creation
# t[0] = 5  # TypeError

# Use as dict keys or set elements (hashable, unlike lists)
point_set = {(0, 0), (1, 2), (3, 4)}
graph = {(0, 0): 'start'}

# Named tuples (more readable)
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
p.x, p.y  # 3, 4
```

---

## Dictionaries (Hash Maps)

```python
# Creation
d = {'a': 1, 'b': 2, 'c': 3}
d = dict(a=1, b=2, c=3)
d = dict([(k, v) for k, v in pairs])
d = {x: x**2 for x in range(5)}     # dict comprehension

# Access
d['a']             # 1 (KeyError if missing)
d.get('a')         # 1 (None if missing)
d.get('z', 0)      # 0 (default value if missing)

# Modification
d['d'] = 4                # set / update — O(1) avg
del d['a']                # delete key — O(1) avg
d.pop('b')                # remove & return value — O(1)
d.pop('z', None)          # remove with default if missing
d.setdefault('e', 5)      # set if key doesn't exist, return value
d.update({'f': 6, 'g': 7})  # merge another dict

# Iteration
for key in d:                   # iterate keys
    pass
for key in d.keys():            # explicit keys
    pass
for val in d.values():          # iterate values
    pass
for key, val in d.items():      # iterate key-value pairs
    pass

# Membership
'a' in d        # O(1) average — check key exists
'x' not in d    # True

# Useful patterns
# Frequency counter
freq = {}
for char in s:
    freq[char] = freq.get(char, 0) + 1

# Group by key
groups = {}
for item in items:
    key = get_key(item)
    groups.setdefault(key, []).append(item)

# Merge dicts (Python 3.9+)
merged = d1 | d2        # d2 values override d1
d1 |= d2                # in-place merge

# Ordered iteration (Python 3.7+): insertion order preserved
```

### Dictionary Complexity

| Operation | Average | Worst |
|-----------|---------|-------|
| Get/Set/Delete | O(1) | O(n) |
| `key in dict` | O(1) | O(n) |
| Iteration | O(n) | O(n) |

---

## Sets

```python
# Creation
s = {1, 2, 3}
s = set([1, 2, 2, 3])   # {1, 2, 3} — duplicates removed
s = set()                # empty set (NOT {} — that's a dict!)

# Modification
s.add(4)                 # O(1)
s.remove(2)              # O(1) — KeyError if missing
s.discard(2)             # O(1) — no error if missing
s.pop()                  # remove & return arbitrary element
s.clear()                # remove all

# Membership
2 in s                   # O(1) average

# Set operations
a | b       # union
a & b       # intersection
a - b       # difference (in a but not b)
a ^ b       # symmetric difference (in a or b but not both)
a <= b      # subset check
a >= b      # superset check
a < b       # proper subset

# Set comprehension
squares = {x**2 for x in range(10)}

# Frozenset — immutable, hashable (can be used as dict key)
fs = frozenset([1, 2, 3])
```

---

## Stacks & Queues

### Stack (LIFO)

```python
# Use a list as a stack
stack = []
stack.append(1)      # push — O(1)
stack.append(2)
stack.pop()          # pop → 2 — O(1)
top = stack[-1]      # peek — O(1)
len(stack) == 0      # empty check
```

### Queue (FIFO)

```python
from collections import deque

queue = deque()
queue.append(1)      # enqueue (right) — O(1)
queue.append(2)
queue.popleft()      # dequeue (left) → 1 — O(1)
front = queue[0]     # peek front — O(1)
len(queue) == 0      # empty check

# DON'T use list for queue — list.pop(0) is O(n)!
```

### Deque (Double-ended Queue)

```python
from collections import deque

dq = deque([1, 2, 3])
dq.append(4)         # add right — O(1)
dq.appendleft(0)     # add left — O(1)
dq.pop()             # remove right — O(1)
dq.popleft()         # remove left — O(1)
dq[0]                # peek left
dq[-1]               # peek right
dq.rotate(1)         # rotate right by 1
dq.rotate(-1)        # rotate left by 1

# Fixed-size deque (auto-drops oldest)
dq = deque(maxlen=3)
dq.append(1)  # [1]
dq.append(2)  # [1, 2]
dq.append(3)  # [1, 2, 3]
dq.append(4)  # [2, 3, 4] — 1 was dropped
```

---

## Heaps / Priority Queues

```python
import heapq

# Python heapq is a MIN-HEAP
nums = [3, 1, 4, 1, 5, 9]
heapq.heapify(nums)              # O(n) — convert list to heap in-place

heapq.heappush(nums, 2)          # O(log n) — push
smallest = heapq.heappop(nums)   # O(log n) — pop smallest
peek = nums[0]                   # O(1) — peek at smallest

# Push and pop in one operation
val = heapq.heappushpop(nums, 6) # push 6, pop smallest — O(log n)
val = heapq.heapreplace(nums, 6) # pop smallest, push 6 — O(log n)

# Find k largest / smallest
heapq.nlargest(3, nums)          # [9, 5, 4]
heapq.nsmallest(3, nums)         # [1, 1, 2]

# MAX-HEAP trick: negate values
max_heap = []
heapq.heappush(max_heap, -val)       # push
largest = -heapq.heappop(max_heap)   # pop largest

# Heap with tuples (sorted by first element, then second, etc.)
heap = []
heapq.heappush(heap, (priority, item))
heapq.heappush(heap, (1, "low"))
heapq.heappush(heap, (3, "high"))
_, item = heapq.heappop(heap)  # gets "low"

# CUSTOM OBJECTS: wrap comparable items or use (priority, counter, obj)
counter = 0
heapq.heappush(heap, (priority, counter, obj))
counter += 1  # ensures FIFO for equal priorities
```

### Heap Complexity

| Operation | Time |
|-----------|------|
| heapify | O(n) |
| push | O(log n) |
| pop | O(log n) |
| peek (heap[0]) | O(1) |
| nlargest/nsmallest(k) | O(n log k) |

---

## Collections Module

```python
from collections import Counter, defaultdict, deque, OrderedDict, namedtuple

# ─── Counter ───
c = Counter("abracadabra")
# Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
c = Counter([1, 1, 2, 3, 3, 3])
# Counter({3: 3, 1: 2, 2: 1})

c.most_common(2)        # [(3, 3), (1, 2)]
c['a']                  # 5 (returns 0 for missing keys, not KeyError)
c.update("aaa")         # add counts
c.subtract("a")         # subtract counts
c.total()               # total of all counts (Python 3.10+)
list(c.elements())      # iterator of elements repeated by count

# Counter arithmetic
c1 + c2                 # add counts
c1 - c2                 # subtract (keeps only positive)
c1 & c2                 # min of each count (intersection)
c1 | c2                 # max of each count (union)

# ─── defaultdict ───
dd = defaultdict(int)       # default value 0
dd = defaultdict(list)      # default value []
dd = defaultdict(set)       # default value set()
dd = defaultdict(lambda: float('inf'))

# Frequency counter
freq = defaultdict(int)
for x in data:
    freq[x] += 1

# Group items
groups = defaultdict(list)
for word in words:
    key = tuple(sorted(word))
    groups[key].append(word)

# ─── OrderedDict ── (maintains insertion order, has move_to_end)
od = OrderedDict()
od['a'] = 1
od['b'] = 2
od.move_to_end('a')           # move 'a' to end
od.move_to_end('b', last=False)  # move 'b' to front
od.popitem()                   # pop last item
od.popitem(last=False)         # pop first item
# Useful for LRU cache implementation

# ─── namedtuple ───
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
p.x, p.y   # 1, 2
p._asdict() # {'x': 1, 'y': 2}
```

---

## Linked Lists

```python
# Node definition
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# ─── Traversal ───
def traverse(head):
    curr = head
    while curr:
        print(curr.val)
        curr = curr.next

# ─── Reverse a linked list ───
def reverse(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev  # new head

# ─── Detect cycle (Floyd's algorithm) ───
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

# ─── Find cycle start ───
def find_cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None   # no cycle
    slow = head
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow

# ─── Find middle node ───
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow  # middle (right-middle for even length)

# ─── Merge two sorted lists ───
def merge(l1, l2):
    dummy = curr = ListNode(0)
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next

# ─── Dummy head pattern ───
# Use when the head might change (deletion, insertion at front)
dummy = ListNode(0)
dummy.next = head
# ... operations ...
return dummy.next
```

---

## Trees & Binary Search Trees

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# ─── DFS Traversals ───

# Inorder (Left, Root, Right) — gives sorted order for BST
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

# Iterative inorder
def inorder_iterative(root):
    result, stack = [], []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result

# Preorder (Root, Left, Right)
def preorder(root):
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)

# Iterative preorder
def preorder_iterative(root):
    if not root:
        return []
    result, stack = [], [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result

# Postorder (Left, Right, Root)
def postorder(root):
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]

# ─── BFS (Level Order) ───
from collections import deque

def level_order(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result

# ─── Tree height / max depth ───
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# ─── Validate BST ───
def is_valid_bst(root, lo=float('-inf'), hi=float('inf')):
    if not root:
        return True
    if not (lo < root.val < hi):
        return False
    return (is_valid_bst(root.left, lo, root.val) and
            is_valid_bst(root.right, root.val, hi))

# ─── Lowest Common Ancestor (BST) ───
def lca_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root

# ─── Lowest Common Ancestor (Binary Tree) ───
def lca(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right:
        return root
    return left or right

# ─── Serialize / Deserialize (BFS) ───
def serialize(root):
    if not root:
        return ""
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node:
            result.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append("null")
    return ",".join(result)

def deserialize(data):
    if not data:
        return None
    vals = data.split(",")
    root = TreeNode(int(vals[0]))
    queue = deque([root])
    i = 1
    while queue:
        node = queue.popleft()
        if vals[i] != "null":
            node.left = TreeNode(int(vals[i]))
            queue.append(node.left)
        i += 1
        if vals[i] != "null":
            node.right = TreeNode(int(vals[i]))
            queue.append(node.right)
        i += 1
    return root
```

---

## Graphs

```python
# ─── Representations ───

# Adjacency list (most common in interviews)
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)   # undirected

# Adjacency list (simple dict)
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A'],
    'D': ['B'],
}

# Adjacency matrix
n = 5
adj = [[0] * n for _ in range(n)]
adj[0][1] = 1   # edge from 0 to 1
adj[1][0] = 1   # undirected

# Edge list
edges = [(0, 1), (1, 2), (2, 3)]

# Weighted adjacency list
graph = defaultdict(list)
for u, v, w in weighted_edges:
    graph[u].append((v, w))

# ─── BFS ───
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# BFS shortest path (unweighted)
def shortest_path(graph, start, end):
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        node, path = queue.popleft()
        if node == end:
            return path
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return []  # no path

# ─── DFS (Recursive) ───
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited

# ─── DFS (Iterative) ───
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
    return visited

# ─── Number of connected components ───
def count_components(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    visited = set()
    count = 0
    for node in range(n):
        if node not in visited:
            dfs(graph, node, visited)
            count += 1
    return count

# ─── Detect cycle in undirected graph (DFS) ───
def has_cycle_undirected(graph, n):
    visited = set()
    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        return False
    for node in range(n):
        if node not in visited:
            if dfs(node, -1):
                return True
    return False

# ─── Detect cycle in directed graph (DFS with coloring) ───
def has_cycle_directed(graph, n):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    def dfs(node):
        color[node] = GRAY
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return True   # back edge → cycle
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        color[node] = BLACK
        return False
    return any(color[i] == WHITE and dfs(i) for i in range(n))

# ─── Number of Islands (grid BFS) ───
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                # BFS to mark connected land
                queue = deque([(r, c)])
                grid[r][c] = '0'
                while queue:
                    row, col = queue.popleft()
                    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                            grid[nr][nc] = '0'
                            queue.append((nr, nc))
    return count
```

---

## Sorting Algorithms

```python
# ─── Built-in (TimSort — hybrid merge + insertion sort) ───
arr.sort()                          # in-place — O(n log n)
sorted(arr)                         # new list — O(n log n)
sorted(arr, key=lambda x: -x)      # descending
sorted(arr, key=lambda x: (x[0], -x[1]))  # multi-key sort

# Stable sort: equal elements maintain their relative order
# Python's sort is STABLE

# ─── Merge Sort ───
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
# Time: O(n log n) | Space: O(n) | Stable

# ─── Quick Sort ───
import random

def quick_sort(arr, lo=0, hi=None):
    if hi is None:
        hi = len(arr) - 1
    if lo < hi:
        pivot_idx = partition(arr, lo, hi)
        quick_sort(arr, lo, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, hi)

def partition(arr, lo, hi):
    pivot_idx = random.randint(lo, hi)
    arr[pivot_idx], arr[hi] = arr[hi], arr[pivot_idx]
    pivot = arr[hi]
    i = lo
    for j in range(lo, hi):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i
# Time: O(n log n) avg, O(n²) worst | Space: O(log n) | Not stable

# ─── Quick Select (kth smallest) ───
def quick_select(arr, k):
    """Find k-th smallest element (0-indexed)."""
    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    if k < len(left):
        return quick_select(left, k)
    elif k < len(left) + len(mid):
        return pivot
    else:
        return quick_select(right, k - len(left) - len(mid))
# Time: O(n) average, O(n²) worst

# ─── Counting Sort (for small integer ranges) ───
def counting_sort(arr, max_val):
    count = [0] * (max_val + 1)
    for x in arr:
        count[x] += 1
    result = []
    for val, cnt in enumerate(count):
        result.extend([val] * cnt)
    return result
# Time: O(n + k) where k = range | Space: O(k)

# ─── Bucket Sort ───
def bucket_sort(arr, num_buckets=10):
    if not arr:
        return arr
    min_val, max_val = min(arr), max(arr)
    bucket_range = (max_val - min_val) / num_buckets + 1
    buckets = [[] for _ in range(num_buckets)]
    for x in arr:
        idx = int((x - min_val) / bucket_range)
        buckets[idx].append(x)
    result = []
    for bucket in buckets:
        result.extend(sorted(bucket))
    return result
# Time: O(n + k) average | Space: O(n + k)
```

### Sorting Comparison

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Tim Sort (Python) | O(n) | O(n log n) | O(n log n) | O(n) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes |
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |

---

## Binary Search

```python
# ─── Classic binary search ───
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2    # avoid overflow (habit from other languages)
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1  # not found

# ─── Leftmost insertion point (bisect_left) ───
def bisect_left(arr, target):
    """First index where target could be inserted to keep sorted order.
       = index of first element >= target."""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo

# ─── Rightmost insertion point (bisect_right) ───
def bisect_right(arr, target):
    """First index AFTER any existing entries of target.
       = index of first element > target."""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo

# ─── First occurrence of target ───
def first_occurrence(arr, target):
    idx = bisect_left(arr, target)
    if idx < len(arr) and arr[idx] == target:
        return idx
    return -1

# ─── Last occurrence of target ───
def last_occurrence(arr, target):
    idx = bisect_right(arr, target) - 1
    if idx >= 0 and arr[idx] == target:
        return idx
    return -1

# ─── Binary search on answer (minimization) ───
def binary_search_on_answer(lo, hi):
    """Find the minimum value that satisfies condition."""
    while lo < hi:
        mid = (lo + hi) // 2
        if condition(mid):
            hi = mid          # mid might be answer, search left
        else:
            lo = mid + 1      # mid doesn't work, go right
    return lo

# ─── Binary search on answer (maximization) ───
def binary_search_max(lo, hi):
    """Find the maximum value that satisfies condition."""
    while lo < hi:
        mid = (lo + hi + 1) // 2   # round up to avoid infinite loop
        if condition(mid):
            lo = mid           # mid works, try larger
        else:
            hi = mid - 1       # mid doesn't work, go left
    return lo

# ─── Binary search on floats ───
def binary_search_float(lo, hi, eps=1e-9):
    while hi - lo > eps:
        mid = (lo + hi) / 2
        if condition(mid):
            hi = mid
        else:
            lo = mid
    return lo
```

---

## Two Pointers

```python
# ─── Pattern 1: Opposite ends (sorted array) ───
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        total = arr[left] + arr[right]
        if total == target:
            return [left, right]
        elif total < target:
            left += 1
        else:
            right -= 1
    return []

# ─── Pattern 2: Same direction (fast & slow) ───
# Remove duplicates in-place
def remove_duplicates(arr):
    if not arr:
        return 0
    slow = 0
    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]
    return slow + 1

# ─── Pattern 3: Three pointers (3Sum) ───
def three_sum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]:
            continue  # skip duplicates
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left+1]:
                    left += 1
                while left < right and nums[right] == nums[right-1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return result

# ─── Pattern 4: Palindrome check ───
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

# ─── Container with most water ───
def max_area(heights):
    left, right = 0, len(heights) - 1
    best = 0
    while left < right:
        area = min(heights[left], heights[right]) * (right - left)
        best = max(best, area)
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return best
```

---

## Sliding Window

```python
# ─── Fixed-size window ───
def max_sum_subarray(arr, k):
    """Max sum of subarray of size k."""
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]  # slide: add right, remove left
        max_sum = max(max_sum, window_sum)
    return max_sum

# ─── Variable-size window (shrink from left) ───
def min_subarray_len(target, arr):
    """Minimum length subarray with sum >= target."""
    left = 0
    curr_sum = 0
    min_len = float('inf')
    for right in range(len(arr)):
        curr_sum += arr[right]
        while curr_sum >= target:
            min_len = min(min_len, right - left + 1)
            curr_sum -= arr[left]
            left += 1
    return min_len if min_len != float('inf') else 0

# ─── Longest substring without repeating characters ───
def length_of_longest_substring(s):
    char_index = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        char_index[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len

# ─── Minimum window substring ───
from collections import Counter

def min_window(s, t):
    need = Counter(t)
    missing = len(t)
    left = 0
    start, end = 0, float('inf')
    for right, char in enumerate(s):
        if need[char] > 0:
            missing -= 1
        need[char] -= 1
        while missing == 0:
            if right - left < end - start:
                start, end = left, right
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return s[start:end + 1] if end != float('inf') else ""

# ─── Sliding window with Counter (permutation check) ───
def check_inclusion(s1, s2):
    """Check if any permutation of s1 exists in s2."""
    if len(s1) > len(s2):
        return False
    need = Counter(s1)
    window = Counter(s2[:len(s1)])
    if window == need:
        return True
    for i in range(len(s1), len(s2)):
        window[s2[i]] += 1
        old = s2[i - len(s1)]
        window[old] -= 1
        if window[old] == 0:
            del window[old]
        if window == need:
            return True
    return False
```

---

## Recursion & Backtracking

```python
# ─── Template: Backtracking ───
def backtrack(candidates, path, result):
    if is_solution(path):
        result.append(path[:])  # append a COPY
        return
    for candidate in candidates:
        if is_valid(candidate, path):
            path.append(candidate)        # choose
            backtrack(candidates, path, result)  # explore
            path.pop()                    # un-choose (backtrack)

# ─── Subsets ───
def subsets(nums):
    result = []
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return result

# ─── Subsets with duplicates ───
def subsets_with_dup(nums):
    nums.sort()
    result = []
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i-1]:
                continue  # skip duplicates
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return result

# ─── Permutations ───
def permutations(nums):
    result = []
    def backtrack(path, remaining):
        if not remaining:
            result.append(path[:])
            return
        for i in range(len(remaining)):
            path.append(remaining[i])
            backtrack(path, remaining[:i] + remaining[i+1:])
            path.pop()
    backtrack([], nums)
    return result

# ─── Permutations (in-place swap) ───
def permute(nums):
    result = []
    def backtrack(start):
        if start == len(nums):
            result.append(nums[:])
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]
    backtrack(0)
    return result

# ─── Combination Sum (can reuse elements) ───
def combination_sum(candidates, target):
    result = []
    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        if remaining < 0:
            return
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # i, not i+1 (reuse)
            path.pop()
    backtrack(0, [], target)
    return result

# ─── N-Queens ───
def solve_n_queens(n):
    result = []
    cols = set()
    diag1 = set()   # row - col
    diag2 = set()   # row + col

    def backtrack(row, board):
        if row == n:
            result.append(["".join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board[row][col] = 'Q'
            backtrack(row + 1, board)
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    board = [['.' for _ in range(n)] for _ in range(n)]
    backtrack(0, board)
    return result
```

---

## Dynamic Programming

```python
# ─── Template: Top-Down (Memoization) ───
from functools import lru_cache

@lru_cache(maxsize=None)
def dp(state):
    if base_case(state):
        return base_value
    return recurrence(state)

# Or with a dict:
memo = {}
def dp(state):
    if state in memo:
        return memo[state]
    if base_case(state):
        return base_value
    memo[state] = recurrence(state)
    return memo[state]

# ─── Template: Bottom-Up (Tabulation) ───
def dp_bottom_up(n):
    dp = [0] * (n + 1)
    dp[0] = base_value
    for i in range(1, n + 1):
        dp[i] = recurrence(dp, i)
    return dp[n]

# ─── Fibonacci ───
# Top-down
@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

# Bottom-up
def fib(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# Space-optimized
def fib(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# ─── Climbing Stairs ───
def climb_stairs(n):
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

# ─── Coin Change (minimum coins) ───
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

# ─── 0/1 Knapsack ───
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i-1][w]  # skip item
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - weights[i-1]] + values[i-1])
    return dp[n][capacity]

# Space-optimized 0/1 Knapsack (1D)
def knapsack_optimized(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for i in range(len(weights)):
        for w in range(capacity, weights[i] - 1, -1):  # reverse!
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]

# ─── Longest Common Subsequence ───
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

# ─── Longest Increasing Subsequence ───
def lis(nums):
    """O(n²) DP approach."""
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

# O(n log n) approach using patience sorting
import bisect
def lis_fast(nums):
    tails = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)

# ─── Edit Distance ───
def edit_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # delete
                    dp[i][j-1],    # insert
                    dp[i-1][j-1]   # replace
                )
    return dp[m][n]

# ─── Maximum Subarray (Kadane's) ───
def max_subarray(nums):
    max_sum = curr_sum = nums[0]
    for num in nums[1:]:
        curr_sum = max(num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)
    return max_sum

# ─── House Robber ───
def rob(nums):
    if not nums:
        return 0
    if len(nums) <= 2:
        return max(nums)
    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    for i in range(2, len(nums)):
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    return dp[-1]

# ─── Unique Paths (grid) ───
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]

# ─── Word Break ───
def word_break(s, word_dict):
    word_set = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[len(s)]
```

### DP Decision Framework

| Problem Type | State | Recurrence Pattern |
|-------------|-------|-------------------|
| Linear sequence | `dp[i]` | depends on `dp[i-1]`, `dp[i-2]` |
| Two sequences | `dp[i][j]` | depends on `dp[i-1][j-1]`, etc. |
| Knapsack | `dp[i][w]` | take or skip item |
| Interval | `dp[i][j]` | partition into subintervals |
| Tree | `dp[node]` | depends on children |
| Bitmask | `dp[mask]` | toggle bits in mask |

---

## Bit Manipulation

```python
# ─── Basic operations ───
a & b     # AND
a | b     # OR
a ^ b     # XOR
~a        # NOT (bitwise complement)
a << n    # left shift (multiply by 2^n)
a >> n    # right shift (divide by 2^n)

# ─── Common tricks ───
n & 1               # check if odd (last bit)
n & (n - 1)         # remove lowest set bit
n & (-n)            # isolate lowest set bit
bin(n).count('1')   # count set bits (popcount)

# Check if power of 2
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

# Count set bits
def count_bits(n):
    count = 0
    while n:
        n &= (n - 1)    # clear lowest set bit
        count += 1
    return count

# Get i-th bit
def get_bit(n, i):
    return (n >> i) & 1

# Set i-th bit
def set_bit(n, i):
    return n | (1 << i)

# Clear i-th bit
def clear_bit(n, i):
    return n & ~(1 << i)

# Toggle i-th bit
def toggle_bit(n, i):
    return n ^ (1 << i)

# ─── XOR tricks ───
a ^ 0 = a          # XOR with 0 → identity
a ^ a = 0          # XOR with self → 0
a ^ b ^ a = b      # XOR is self-inverse

# Find single number (all others appear twice)
def single_number(nums):
    result = 0
    for n in nums:
        result ^= n
    return result

# ─── Bitmask DP (subsets of n items) ───
# Iterate over all subsets of n items
for mask in range(1 << n):        # 0 to 2^n - 1
    for i in range(n):
        if mask & (1 << i):       # item i is in subset
            pass

# Iterate over all submasks of a mask
submask = mask
while submask:
    # process submask
    submask = (submask - 1) & mask
```

---

## Math & Number Theory

```python
import math

# ─── GCD & LCM ───
math.gcd(12, 8)               # 4
math.lcm(12, 8)               # 24 (Python 3.9+)
# Or: lcm = a * b // gcd(a, b)

# GCD of a list
from functools import reduce
reduce(math.gcd, [12, 8, 16])  # 4

# ─── Primes ───
# Check if prime
def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Sieve of Eratosthenes
def sieve(n):
    """Return list of primes up to n."""
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, n + 1, i):
                is_p[j] = False
    return [i for i in range(2, n + 1) if is_p[i]]

# ─── Factorization ───
def prime_factors(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

# ─── Modular arithmetic ───
(a + b) % m == ((a % m) + (b % m)) % m
(a * b) % m == ((a % m) * (b % m)) % m
pow(base, exp, mod)  # fast modular exponentiation — O(log exp)

# Modular inverse (when mod is prime)
# a^(-1) mod p = pow(a, p-2, p)    (Fermat's little theorem)

# ─── Combinations & permutations ───
math.comb(n, k)         # C(n, k) — Python 3.8+
math.perm(n, k)         # P(n, k) — Python 3.8+
math.factorial(n)       # n!

# ─── Useful formulas ───
# Sum 1..n = n*(n+1)/2
# Sum of squares 1²..n² = n*(n+1)*(2n+1)/6
# Arithmetic series: n*(first + last)/2
# Geometric series: a*(r^n - 1)/(r - 1)

# ─── Fibonacci formula ───
# F(n) ≈ φ^n / √5 where φ = (1+√5)/2

# ─── Euclidean distance ───
math.dist([x1, y1], [x2, y2])     # Python 3.8+
# Or: ((x2-x1)**2 + (y2-y1)**2) ** 0.5

# ─── Integer square root ───
import math
math.isqrt(16)    # 4  (Python 3.8+)
```

---

## String Algorithms

```python
# ─── KMP (Knuth-Morris-Pratt) Pattern Matching ───
def kmp_search(text, pattern):
    """Find all occurrences of pattern in text. O(n + m)."""
    def build_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            elif length:
                length = lps[length - 1]
            else:
                i += 1
        return lps

    lps = build_lps(pattern)
    result = []
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == len(pattern):
            result.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and text[i] != pattern[j]:
            if j:
                j = lps[j - 1]
            else:
                i += 1
    return result

# ─── Rabin-Karp (Rolling Hash) ───
def rabin_karp(text, pattern):
    """Find pattern in text using rolling hash. O(n + m) avg."""
    MOD = 10**9 + 7
    BASE = 256
    n, m = len(text), len(pattern)
    if m > n:
        return []

    # Compute hash of pattern and first window
    p_hash = t_hash = 0
    power = pow(BASE, m - 1, MOD)
    for i in range(m):
        p_hash = (p_hash * BASE + ord(pattern[i])) % MOD
        t_hash = (t_hash * BASE + ord(text[i])) % MOD

    result = []
    for i in range(n - m + 1):
        if p_hash == t_hash and text[i:i+m] == pattern:
            result.append(i)
        if i < n - m:
            t_hash = ((t_hash - ord(text[i]) * power) * BASE + ord(text[i + m])) % MOD
    return result

# ─── Longest Palindromic Substring (expand from center) ───
def longest_palindrome(s):
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return s[l+1:r]

    result = ""
    for i in range(len(s)):
        odd = expand(i, i)
        even = expand(i, i + 1)
        result = max(result, odd, even, key=len)
    return result

# ─── Check if two strings are anagrams ───
def is_anagram(s, t):
    return Counter(s) == Counter(t)
    # Or: return sorted(s) == sorted(t)
```

---

## Intervals

```python
# ─── Merge overlapping intervals ───
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

# ─── Insert interval ───
def insert_interval(intervals, new):
    result = []
    i = 0
    # Add all intervals that end before new starts
    while i < len(intervals) and intervals[i][1] < new[0]:
        result.append(intervals[i])
        i += 1
    # Merge overlapping intervals
    while i < len(intervals) and intervals[i][0] <= new[1]:
        new[0] = min(new[0], intervals[i][0])
        new[1] = max(new[1], intervals[i][1])
        i += 1
    result.append(new)
    # Add remaining intervals
    result.extend(intervals[i:])
    return result

# ─── Check if two intervals overlap ───
def overlaps(a, b):
    return a[0] <= b[1] and b[0] <= a[1]

# ─── Interval scheduling (max non-overlapping) ───
def max_non_overlapping(intervals):
    intervals.sort(key=lambda x: x[1])  # sort by end time
    count = 0
    end = float('-inf')
    for start, finish in intervals:
        if start >= end:
            count += 1
            end = finish
    return count
```

---

## Tries (Prefix Trees)

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        """Return True if exact word exists."""
        node = self._find(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        """Return True if any word starts with prefix."""
        return self._find(prefix) is not None

    def _find(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

# Usage
trie = Trie()
trie.insert("apple")
trie.search("apple")     # True
trie.search("app")       # False
trie.starts_with("app")  # True
```

---

## Union-Find (Disjoint Set)

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n   # number of connected components

    def find(self, x):
        """Find root with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """Union by rank. Returns True if x and y were in different sets."""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.count -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)

# Usage
uf = UnionFind(10)
uf.union(0, 1)
uf.union(1, 2)
uf.connected(0, 2)   # True
uf.count              # 8 components remaining

# Common applications:
# - Number of connected components
# - Detect cycles in undirected graph
# - Kruskal's MST
# - Accounts merge
```

---

## Monotonic Stack / Queue

```python
# ─── Next Greater Element ───
def next_greater_element(nums):
    """For each element, find the next element that is greater."""
    n = len(nums)
    result = [-1] * n
    stack = []  # stores indices, values are decreasing
    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            result[stack.pop()] = nums[i]
        stack.append(i)
    return result

# ─── Daily Temperatures ───
def daily_temperatures(temps):
    """Days until a warmer temperature."""
    n = len(temps)
    result = [0] * n
    stack = []
    for i in range(n):
        while stack and temps[i] > temps[stack[-1]]:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
    return result

# ─── Largest Rectangle in Histogram ───
def largest_rectangle(heights):
    stack = []  # stores indices
    max_area = 0
    heights.append(0)  # sentinel
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    heights.pop()  # remove sentinel
    return max_area

# ─── Sliding Window Maximum (monotonic deque) ───
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()   # stores indices, values are decreasing
    result = []
    for i, num in enumerate(nums):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # Remove smaller elements (they'll never be the max)
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

---

## Topological Sort

```python
from collections import deque, defaultdict

# ─── Kahn's Algorithm (BFS-based) ───
def topological_sort(num_nodes, edges):
    """Returns topological order or empty list if cycle exists."""
    graph = defaultdict(list)
    in_degree = [0] * num_nodes
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    queue = deque([i for i in range(num_nodes) if in_degree[i] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == num_nodes else []  # empty → cycle!

# ─── DFS-based topological sort ───
def topological_sort_dfs(num_nodes, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * num_nodes
    order = []
    has_cycle = False

    def dfs(node):
        nonlocal has_cycle
        color[node] = GRAY
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                has_cycle = True
                return
            if color[neighbor] == WHITE:
                dfs(neighbor)
        color[node] = BLACK
        order.append(node)

    for i in range(num_nodes):
        if color[i] == WHITE:
            dfs(i)

    return order[::-1] if not has_cycle else []

# Use cases:
# - Course schedule / prerequisites
# - Build systems (dependency resolution)
# - Task scheduling
```

---

## Shortest Path Algorithms

```python
import heapq
from collections import defaultdict, deque

# ─── Dijkstra's Algorithm (non-negative weights) ───
def dijkstra(graph, start):
    """graph: {node: [(neighbor, weight), ...]}"""
    dist = {start: 0}
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, float('inf')):
            continue
        for v, w in graph[u]:
            new_dist = d + w
            if new_dist < dist.get(v, float('inf')):
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))
    return dist
# Time: O((V + E) log V)

# ─── Bellman-Ford (handles negative weights) ───
def bellman_ford(n, edges, start):
    """edges: [(u, v, w), ...]"""
    dist = [float('inf')] * n
    dist[start] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    # Check for negative cycle
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return None  # negative cycle exists
    return dist
# Time: O(V * E)

# ─── BFS shortest path (unweighted) ───
def bfs_shortest(graph, start, end):
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        node, dist = queue.popleft()
        if node == end:
            return dist
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1  # unreachable

# ─── Floyd-Warshall (all pairs shortest path) ───
def floyd_warshall(n, edges):
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = w
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist
# Time: O(V³) | Space: O(V²)

# ─── Minimum Spanning Tree (Kruskal's) ───
def kruskal(n, edges):
    """edges: [(weight, u, v), ...]"""
    edges.sort()
    uf = UnionFind(n)
    mst_weight = 0
    mst_edges = []
    for w, u, v in edges:
        if uf.union(u, v):
            mst_weight += w
            mst_edges.append((u, v, w))
    return mst_weight, mst_edges
```

---

## Comprehensions & Generators

```python
# ─── List comprehension ───
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
flat = [x for row in matrix for x in row]       # flatten
pairs = [(x, y) for x in range(3) for y in range(3)]

# ─── Dict comprehension ───
sq_dict = {x: x**2 for x in range(5)}
inv = {v: k for k, v in d.items()}                # invert dict
filtered = {k: v for k, v in d.items() if v > 0}

# ─── Set comprehension ───
unique_lens = {len(word) for word in words}

# ─── Generator expression (lazy, memory efficient) ───
gen = (x**2 for x in range(1000000))   # no list in memory
total = sum(x**2 for x in range(1000000))

# ─── Generator function ───
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

gen = fibonacci()
next(gen)   # 0
next(gen)   # 1
next(gen)   # 1

# Take first n from generator
from itertools import islice
first_10 = list(islice(fibonacci(), 10))

# ─── Walrus operator := (Python 3.8+) ───
# Assign and use in the same expression
while (line := input()) != "quit":
    print(line)

filtered = [y for x in data if (y := expensive(x)) > threshold]
```

---

## Useful Built-in Functions

```python
# ─── Iteration ───
map(func, iterable)          # apply func to each item (lazy)
filter(func, iterable)       # keep items where func is truthy (lazy)
zip(iter1, iter2)            # pair elements (stops at shortest)
zip(*matrix)                 # transpose
enumerate(iterable, start=0) # (index, value) pairs
reversed(sequence)           # reverse iterator
sorted(iterable, key=None, reverse=False)

# ─── Aggregation ───
sum(iterable, start=0)
min(iterable)  /  min(a, b)
max(iterable)  /  max(a, b)
all(iterable)       # True if all truthy (or empty)
any(iterable)       # True if any truthy
len(collection)

# ─── Type conversion ───
int("42")            # 42
int("1010", 2)       # 10 (binary to int)
float("3.14")        # 3.14
str(42)              # "42"
list(range(5))       # [0, 1, 2, 3, 4]
tuple([1, 2, 3])     # (1, 2, 3)
set([1, 2, 2, 3])    # {1, 2, 3}
bool(0)              # False
chr(65)              # 'A'
ord('A')             # 65
bin(10)              # '0b1010'
hex(255)             # '0xff'
oct(8)               # '0o10'

# ─── Other useful builtins ───
abs(-5)              # 5
round(3.14159, 2)    # 3.14
pow(2, 10)           # 1024
pow(2, 10, 1000)     # 24 (modular exponentiation)
divmod(17, 5)        # (3, 2)
isinstance(x, int)   # type check
isinstance(x, (int, float))  # multiple types
id(obj)              # memory address (identity)
hash(obj)            # hash value (immutable objects only)
type(obj)            # type of object

# ─── Sorting complex objects ───
from operator import itemgetter, attrgetter
sorted(pairs, key=itemgetter(1))         # sort by index 1
sorted(objects, key=attrgetter('name'))  # sort by attribute
sorted(data, key=lambda x: (x[0], -x[1]))  # multi-key
```

---

## Itertools Module

```python
import itertools

# ─── Combinatoric iterators ───
itertools.product('AB', repeat=2)
# AA, AB, BA, BB (Cartesian product)

itertools.permutations('ABC', 2)
# AB, AC, BA, BC, CA, CB

itertools.combinations('ABCD', 2)
# AB, AC, AD, BC, BD, CD

itertools.combinations_with_replacement('ABC', 2)
# AA, AB, AC, BB, BC, CC

# ─── Infinite iterators ───
itertools.count(10, 2)         # 10, 12, 14, 16, ...
itertools.cycle('ABC')         # A, B, C, A, B, C, ...
itertools.repeat(5, 3)         # 5, 5, 5

# ─── Terminating iterators ───
itertools.chain([1,2], [3,4])  # 1, 2, 3, 4
itertools.chain.from_iterable([[1,2], [3,4]])  # 1, 2, 3, 4

itertools.islice(range(100), 5, 10)  # 5, 6, 7, 8, 9

itertools.accumulate([1,2,3,4])      # 1, 3, 6, 10 (running sum)
itertools.accumulate([1,2,3,4], max) # 1, 2, 3, 4 (running max)

itertools.groupby(sorted(data), key=func)
# Group consecutive elements with same key

itertools.zip_longest([1,2], [3,4,5], fillvalue=0)
# (1,3), (2,4), (0,5)

itertools.starmap(pow, [(2,3), (3,2)])  # 8, 9

itertools.takewhile(lambda x: x < 5, [1,3,5,2])  # 1, 3
itertools.dropwhile(lambda x: x < 5, [1,3,5,2])  # 5, 2

# ─── Flatten nested lists ───
flat = list(itertools.chain.from_iterable(nested))

# ─── Pairwise (Python 3.10+) ───
itertools.pairwise('ABCD')  # AB, BC, CD

# ─── Pairwise for older Python ───
def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)
```

---

## Functools Module

```python
from functools import lru_cache, cache, reduce, partial, cmp_to_key

# ─── Memoization ───
@lru_cache(maxsize=None)    # unbounded cache
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)

@cache    # Python 3.9+ (shorthand for lru_cache(maxsize=None))
def expensive(x, y):
    return x ** y

# ─── reduce (fold) ───
from functools import reduce
reduce(lambda a, b: a + b, [1, 2, 3, 4])  # 10
reduce(lambda a, b: a * b, [1, 2, 3, 4])  # 24

# ─── partial (preset arguments) ───
from functools import partial
double = partial(lambda x, y: x * y, 2)
double(5)  # 10

# ─── Custom comparator for sorting ───
from functools import cmp_to_key

def compare(a, b):
    # return negative if a < b, 0 if equal, positive if a > b
    return a - b

sorted(arr, key=cmp_to_key(compare))

# Useful example: largest number from digits
def compare_nums(a, b):
    if a + b > b + a:
        return -1
    elif a + b < b + a:
        return 1
    return 0

nums = ["3", "30", "34", "5", "9"]
nums.sort(key=cmp_to_key(compare_nums))
# Result: ["9", "5", "34", "3", "30"] → "9534330"
```

---

## Bisect Module

```python
import bisect

arr = [1, 3, 5, 7, 9]

# Find insertion point (maintains sorted order)
bisect.bisect_left(arr, 5)    # 2 (leftmost position for 5)
bisect.bisect_right(arr, 5)   # 3 (rightmost position for 5)
bisect.bisect(arr, 5)         # same as bisect_right

# Insert into sorted list
bisect.insort_left(arr, 4)    # arr = [1, 3, 4, 5, 7, 9]
bisect.insort_right(arr, 4)   # arr = [1, 3, 4, 4, 5, 7, 9]

# ─── Useful patterns ───
# Find index of target in sorted array
def index(arr, target):
    i = bisect.bisect_left(arr, target)
    if i != len(arr) and arr[i] == target:
        return i
    return -1

# Count occurrences in sorted array
def count(arr, target):
    left = bisect.bisect_left(arr, target)
    right = bisect.bisect_right(arr, target)
    return right - left

# Find floor (largest element ≤ target)
def floor(arr, target):
    i = bisect.bisect_right(arr, target) - 1
    return arr[i] if i >= 0 else None

# Find ceiling (smallest element ≥ target)
def ceiling(arr, target):
    i = bisect.bisect_left(arr, target)
    return arr[i] if i < len(arr) else None

# Use with key function (Python 3.10+)
bisect.bisect_left(arr, target, key=lambda x: x[0])
```

---

## Regular Expressions

```python
import re

# ─── Basic matching ───
re.search(r'pattern', text)     # first match anywhere
re.match(r'pattern', text)      # match at start only
re.fullmatch(r'pattern', text)  # match entire string
re.findall(r'pattern', text)    # all non-overlapping matches
re.finditer(r'pattern', text)   # iterator of match objects

# ─── Common patterns ───
r'\d'       # digit [0-9]
r'\D'       # non-digit
r'\w'       # word char [a-zA-Z0-9_]
r'\W'       # non-word char
r'\s'       # whitespace
r'\S'       # non-whitespace
r'\b'       # word boundary
r'.'        # any char except newline
r'^'        # start of string
r'$'        # end of string

# Quantifiers
r'a*'       # 0 or more
r'a+'       # 1 or more
r'a?'       # 0 or 1
r'a{3}'     # exactly 3
r'a{2,4}'   # 2 to 4

# Groups
r'(abc)'    # capturing group
r'(?:abc)'  # non-capturing group
r'(?P<name>abc)'  # named group

# ─── Substitution ───
re.sub(r'pattern', 'replacement', text)
re.sub(r'(\w+)', lambda m: m.group(1).upper(), text)

# ─── Split ───
re.split(r'[,;\s]+', "a,b; c  d")  # ['a', 'b', 'c', 'd']

# ─── Compile for reuse ───
pattern = re.compile(r'\d+')
pattern.findall("abc 123 def 456")  # ['123', '456']
```

---

## Object-Oriented Python

```python
# ─── Basic class ───
class Animal:
    species_count = 0   # class variable

    def __init__(self, name, sound):
        self.name = name       # instance variable
        self.sound = sound
        Animal.species_count += 1

    def speak(self):
        return f"{self.name} says {self.sound}!"

    def __repr__(self):
        return f"Animal({self.name!r}, {self.sound!r})"

    def __str__(self):
        return f"{self.name} the animal"

    def __eq__(self, other):
        return isinstance(other, Animal) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.name < other.name    # enables sorting

# ─── Inheritance ───
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Woof")
        self.breed = breed

    def speak(self):    # override
        return f"{self.name} barks: {self.sound}!"

# ─── Properties ───
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        return 3.14159 * self._radius ** 2

# ─── Class methods & static methods ───
class MyClass:
    count = 0

    @classmethod
    def from_string(cls, s):
        """Alternative constructor."""
        return cls(int(s))

    @staticmethod
    def is_valid(x):
        """Utility — doesn't access instance or class."""
        return x > 0

# ─── Dataclasses (Python 3.7+) ───
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float
    label: str = "origin"

    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5

@dataclass(frozen=True)    # immutable, hashable
class FrozenPoint:
    x: float
    y: float

@dataclass(order=True)     # generates comparison methods
class Student:
    sort_index: float = field(init=False, repr=False)
    name: str
    gpa: float
    def __post_init__(self):
        self.sort_index = -self.gpa   # sort by GPA descending

# ─── Abstract Base Classes ───
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h
    def perimeter(self):
        return 2 * (self.w + self.h)

# ─── Dunder (magic) methods reference ───
# __init__       constructor
# __del__        destructor
# __repr__       developer-facing string
# __str__        user-facing string
# __len__        len(obj)
# __getitem__    obj[key]
# __setitem__    obj[key] = value
# __contains__   item in obj
# __iter__       iter(obj)
# __next__       next(obj)
# __call__       obj()
# __eq__         ==
# __ne__         !=
# __lt__         <
# __le__         <=
# __gt__         >
# __ge__         >=
# __add__        +
# __sub__        -
# __mul__        *
# __hash__       hash(obj)
# __bool__       bool(obj)
# __enter__      context manager enter
# __exit__       context manager exit
```

---

## Error Handling

```python
# ─── try / except / else / finally ───
try:
    result = risky_operation()
except ValueError as e:
    print(f"Value error: {e}")
except (TypeError, KeyError):
    print("Type or key error")
except Exception as e:
    print(f"Unexpected: {e}")
else:
    print("No exception occurred")
finally:
    cleanup()   # always runs

# ─── Raise exceptions ───
raise ValueError("Invalid input")
raise RuntimeError("Something went wrong")

# ─── Custom exceptions ───
class CustomError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

# ─── Assert (debugging only — disabled with -O flag) ───
assert x > 0, "x must be positive"

# ─── Context managers ───
# Ensure cleanup with 'with' statement
with open('file.txt') as f:
    data = f.read()

# Custom context manager
from contextlib import contextmanager

@contextmanager
def timer():
    import time
    start = time.time()
    yield
    print(f"Elapsed: {time.time() - start:.2f}s")

with timer():
    heavy_computation()
```

---

## File I/O

```python
# ─── Reading ───
with open('file.txt', 'r') as f:
    content = f.read()          # entire file as string
    lines = f.readlines()       # list of lines
    for line in f:              # iterate line by line (memory efficient)
        process(line.strip())

# ─── Writing ───
with open('file.txt', 'w') as f:   # overwrite
    f.write("Hello\n")
with open('file.txt', 'a') as f:   # append
    f.write("World\n")

# ─── JSON ───
import json
data = json.loads('{"key": "value"}')     # string → dict
json_str = json.dumps(data, indent=2)     # dict → string
with open('data.json', 'r') as f:
    data = json.load(f)                   # file → dict
with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)          # dict → file

# ─── CSV ───
import csv
with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)    # list of strings

with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Age'])
    writer.writerows([['Alice', 30], ['Bob', 25]])

# ─── Path handling ───
from pathlib import Path
p = Path('folder') / 'subfolder' / 'file.txt'
p.exists()
p.is_file()
p.is_dir()
p.read_text()
p.write_text("content")
p.stem       # filename without extension
p.suffix     # extension
p.parent     # parent directory
list(p.parent.glob('*.txt'))  # all .txt files
```

---

## Type Hints

```python
from typing import (
    List, Dict, Set, Tuple, Optional, Union,
    Callable, Iterator, Generator, Any
)

# Basic types (Python 3.9+ can use builtin names directly)
def greet(name: str) -> str:
    return f"Hello, {name}"

# Container types
def process(items: list[int]) -> dict[str, int]:         # 3.9+
    pass
def process(items: List[int]) -> Dict[str, int]:         # <3.9
    pass

# Optional (can be None)
def find(arr: list[int], target: int) -> Optional[int]:  # int | None
    pass

# Union types
def parse(data: Union[str, bytes]) -> dict:   # <3.10
    pass
def parse(data: str | bytes) -> dict:         # 3.10+
    pass

# Callable
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# Type aliases
Matrix = list[list[float]]
Graph = dict[int, list[int]]

def shortest_path(graph: Graph, start: int) -> dict[int, int]:
    pass
```

---

## Common Interview Gotchas

```python
# 1. Mutable default arguments — DANGER
def bad(lst=[]):       # same list object every call!
    lst.append(1)
    return lst
# bad() → [1], bad() → [1, 1] ← BUG

def good(lst=None):    # correct pattern
    if lst is None:
        lst = []
    lst.append(1)
    return lst

# 2. Shallow vs deep copy
import copy
a = [[1, 2], [3, 4]]
b = a[:]               # shallow copy — inner lists shared!
c = copy.deepcopy(a)   # deep copy — fully independent

# 3. Integer comparison
a = 256
b = 256
a is b    # True (Python caches -5 to 256)
a = 257
b = 257
a is b    # May be False! Use == for value comparison

# 4. Modifying list while iterating
# BAD:
for item in lst:
    if condition(item):
        lst.remove(item)   # skips elements!
# GOOD:
lst = [item for item in lst if not condition(item)]

# 5. Creating 2D lists
# WRONG: [[0]*n]*m  — all rows are the SAME list!
# RIGHT: [[0]*n for _ in range(m)]

# 6. Global vs local scope
x = 10
def func():
    # x += 1  # UnboundLocalError!
    pass
def func():
    global x   # need this to modify global
    x += 1

# 7. Dictionary iteration order
# Python 3.7+: insertion order guaranteed
# Older: use OrderedDict

# 8. Float precision
0.1 + 0.2 == 0.3          # False!
abs(0.1 + 0.2 - 0.3) < 1e-9  # True — use epsilon comparison

# 9. String immutability
s = "hello"
# s[0] = 'H'  # TypeError
s = 'H' + s[1:]  # create new string

# 10. Pass by assignment (not pass by reference)
def modify(lst):
    lst.append(4)    # modifies original (same object)
    lst = [1, 2, 3]  # rebinds local variable only
```

---

## Complexity Reference Table

### Python Built-in Operations

| Structure | Operation | Average | Worst |
|-----------|-----------|---------|-------|
| **list** | index `[i]` | O(1) | O(1) |
| | append | O(1) | O(1) amort. |
| | pop last | O(1) | O(1) |
| | pop(i) / insert(i) | O(n) | O(n) |
| | `x in list` | O(n) | O(n) |
| | sort | O(n log n) | O(n log n) |
| | slice `[a:b]` | O(b-a) | O(b-a) |
| | extend(k items) | O(k) | O(k) |
| **dict** | get / set / del | O(1) | O(n) |
| | `key in dict` | O(1) | O(n) |
| | iteration | O(n) | O(n) |
| **set** | add / remove / `in` | O(1) | O(n) |
| | union / intersection | O(m+n) | O(m+n) |
| **deque** | append / pop (both ends) | O(1) | O(1) |
| | index `[i]` | O(n) | O(n) |
| **heapq** | push / pop | O(log n) | O(log n) |
| | heapify | O(n) | O(n) |
| **str** | concat `+` | O(n+m) | O(n+m) |
| | `in` (substring) | O(nm) | O(nm) |
| | join | O(total len) | O(total len) |

### Algorithm Complexities

| Algorithm | Time | Space |
|-----------|------|-------|
| Binary Search | O(log n) | O(1) |
| BFS / DFS | O(V + E) | O(V) |
| Dijkstra | O((V+E) log V) | O(V) |
| Bellman-Ford | O(V × E) | O(V) |
| Floyd-Warshall | O(V³) | O(V²) |
| Topological Sort | O(V + E) | O(V) |
| Union-Find (with optimizations) | O(α(n)) ≈ O(1) | O(n) |
| Merge Sort | O(n log n) | O(n) |
| Quick Sort | O(n log n) avg | O(log n) |
| Quick Select | O(n) avg | O(1) |
| Counting Sort | O(n + k) | O(k) |
| Trie insert/search | O(L) | O(Σ × L) |
| KMP string match | O(n + m) | O(m) |

---

> **Remember:** In interviews, always clarify constraints first, think aloud, and start with brute force before optimizing. Test your code with edge cases: empty input, single element, duplicates, negative numbers, and very large inputs.
