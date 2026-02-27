# Mini-Project 01: LRU Cache

**Time:** 1–1.5 hours  
**Difficulty:** Medium  
**Concepts:** Hash map, doubly linked list, OOP, time complexity

---

## Objective

Build a Least Recently Used (LRU) Cache that supports `get` and `put` operations in O(1) time.

This is one of the most commonly asked interview design problems. Building it from scratch is the best way to understand it.

## Requirements

Implement a class `LRUCache` with:

```python
class LRUCache:
    def __init__(self, capacity: int):
        """Initialize the cache with a positive capacity."""
        pass

    def get(self, key: int) -> int:
        """Return the value if key exists, otherwise return -1.
        Mark the key as recently used."""
        pass

    def put(self, key: int, value: int) -> None:
        """Insert or update the value for the key.
        If the cache is at capacity, evict the least recently used item first."""
        pass
```

## Example Usage

```python
cache = LRUCache(2)  # capacity = 2

cache.put(1, 10)     # cache: {1: 10}
cache.put(2, 20)     # cache: {1: 10, 2: 20}
cache.get(1)         # returns 10, cache: {2: 20, 1: 10} (1 is now most recent)
cache.put(3, 30)     # evicts key 2, cache: {1: 10, 3: 30}
cache.get(2)         # returns -1 (not found)
cache.put(4, 40)     # evicts key 1, cache: {3: 30, 4: 40}
cache.get(1)         # returns -1 (evicted)
cache.get(3)         # returns 30
cache.get(4)         # returns 40
```

## Approach

You need two data structures working together:

1. **Hash map** (dict) — maps key → node for O(1) lookup
2. **Doubly linked list** — maintains order from least recently used (head) to most recently used (tail)

When you `get` a key: look it up in the hash map, move the node to the tail (most recent).  
When you `put` a key: add to tail. If over capacity, remove from head (least recent) and delete from hash map.

## Hints

<details>
<summary>Hint 1: Node structure</summary>

Create a `Node` class with `key`, `value`, `prev`, and `next` attributes. You need the key stored in the node so you can remove it from the hash map when evicting.
</details>

<details>
<summary>Hint 2: Sentinel nodes</summary>

Use dummy head and tail nodes to avoid null checks. Always insert between `dummy_head` and `dummy_tail`. This simplifies the linked list logic dramatically.
</details>

<details>
<summary>Hint 3: Helper methods</summary>

Write two private helpers: `_remove(node)` removes a node from the list, and `_add_to_tail(node)` adds a node right before the dummy tail. Then "move to most recent" is just `_remove` + `_add_to_tail`.
</details>

## Tests to Write

```python
def test_basic_get_and_put():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1

def test_eviction():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)  # evicts key 1
    assert cache.get(1) == -1

def test_update_existing_key():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(1, 10)  # update value
    assert cache.get(1) == 10

def test_get_refreshes_recency():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.get(1)       # 1 is now most recent
    cache.put(3, 3)    # should evict 2, not 1
    assert cache.get(2) == -1
    assert cache.get(1) == 1

def test_capacity_one():
    cache = LRUCache(1)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == -1
    assert cache.get(2) == 2
```

## Stretch Goals

1. Add a `__repr__` method that shows the cache contents in order from least to most recently used
2. Add a `size()` method and a `clear()` method
3. Make it thread-safe using `threading.Lock`
4. Add TTL (time-to-live) support — entries expire after N seconds
