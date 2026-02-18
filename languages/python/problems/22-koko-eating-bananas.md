# 22. Koko Eating Bananas

Difficulty: Medium  
Topics: array, binary-search

Statement
Koko loves bananas. There are `n` piles where `piles[i]` is the number of bananas in pile `i`.

She can decide her eating speed `k` bananas per hour. Each hour, she chooses one pile and eats up to `k` bananas from it.

Return the minimum integer `k` so she can eat all bananas within `h` hours.

Examples
- Input: `piles = [3,6,7,11]`, `h = 8`  
  Output: `4`

Constraints
- `1 <= piles.length <= 10^4`
- `piles.length <= h <= 10^9`
- `1 <= piles[i] <= 10^9`

Hints (optional)
- Binary-search the speed and check feasibility.

Canonical solution
- `/languages/python/problems/solutions/22-koko-eating-bananas.py`
