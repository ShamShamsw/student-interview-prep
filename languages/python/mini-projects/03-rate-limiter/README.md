# Mini-Project 03: Rate Limiter

**Time:** 1–2 hours  
**Difficulty:** Medium  
**Concepts:** Sliding window algorithm, time-based logic, decorators, OOP

---

## Objective

Build a rate limiter that restricts how many times a function (or API endpoint) can be called within a time window. This is a classic system design concept — building it makes the interview question much easier to answer.

## Requirements

Implement these rate limiting algorithms:

### 1. Fixed Window Counter

```python
limiter = FixedWindowLimiter(max_requests=5, window_seconds=60)

limiter.allow("user_123")  # True (1/5)
limiter.allow("user_123")  # True (2/5)
# ... 3 more calls ...
limiter.allow("user_123")  # False (limit reached)
limiter.allow("user_456")  # True (different user, separate counter)
```

### 2. Sliding Window Log

```python
limiter = SlidingWindowLimiter(max_requests=5, window_seconds=60)

# Keeps a log of timestamps, counting only those within the last 60 seconds
limiter.allow("user_123")  # True
```

### 3. Decorator

```python
@rate_limit(max_calls=3, period_seconds=10)
def send_email(to, subject):
    print(f"Sending email to {to}")

send_email("a@b.com", "Hi")  # Works
send_email("a@b.com", "Hi")  # Works
send_email("a@b.com", "Hi")  # Works
send_email("a@b.com", "Hi")  # Raises RateLimitExceeded
```

## Approach

### Fixed Window
- Store a dict mapping `(user, window_start)` → count
- Window start = `int(current_time / window_seconds) * window_seconds`
- If count < max_requests, increment and allow

### Sliding Window
- Store a dict mapping `user` → list of timestamps
- On each request, remove timestamps older than `now - window_seconds`
- If remaining count < max_requests, add timestamp and allow

## Hints

<details>
<summary>Hint 1: Getting current time</summary>

```python
import time
now = time.time()  # Returns float (seconds since epoch)
```
</details>

<details>
<summary>Hint 2: Making it testable</summary>

Inject the time source so you can control it in tests:
```python
class SlidingWindowLimiter:
    def __init__(self, max_requests, window_seconds, time_func=None):
        self._time_func = time_func or time.time
```
</details>

<details>
<summary>Hint 3: Decorator pattern</summary>

```python
import functools

def rate_limit(max_calls, period_seconds):
    limiter = SlidingWindowLimiter(max_calls, period_seconds)
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not limiter.allow("global"):
                raise RateLimitExceeded(f"Rate limit: {max_calls} calls per {period_seconds}s")
            return func(*args, **kwargs)
        return wrapper
    return decorator
```
</details>

## Tests to Write

```python
def test_allows_within_limit():
    limiter = FixedWindowLimiter(max_requests=3, window_seconds=60)
    assert limiter.allow("user1") is True
    assert limiter.allow("user1") is True
    assert limiter.allow("user1") is True

def test_blocks_over_limit():
    limiter = FixedWindowLimiter(max_requests=2, window_seconds=60)
    limiter.allow("user1")
    limiter.allow("user1")
    assert limiter.allow("user1") is False

def test_separate_users():
    limiter = FixedWindowLimiter(max_requests=1, window_seconds=60)
    assert limiter.allow("user1") is True
    assert limiter.allow("user2") is True  # different user

def test_window_reset():
    fake_time = [100.0]
    limiter = SlidingWindowLimiter(
        max_requests=2, window_seconds=10,
        time_func=lambda: fake_time[0]
    )
    limiter.allow("user1")
    limiter.allow("user1")
    assert limiter.allow("user1") is False

    fake_time[0] = 111.0  # advance past window
    assert limiter.allow("user1") is True

def test_decorator_raises():
    @rate_limit(max_calls=1, period_seconds=60)
    def my_func():
        return "ok"

    assert my_func() == "ok"
    with pytest.raises(RateLimitExceeded):
        my_func()
```

## Stretch Goals

1. Implement a **Token Bucket** algorithm (constant rate, allows bursts)
2. Add a `retry_after` property that tells the caller how many seconds to wait
3. Build a simple Flask/FastAPI middleware that uses your rate limiter
4. Store rate limit state in Redis instead of in-memory (for distributed systems)
