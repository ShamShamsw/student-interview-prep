# 35. Coin Change

Difficulty: Medium  
Topics: dynamic-programming, array

Statement
You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.

Return the fewest number of coins needed to make up that amount. If that amount cannot be made up by any combination of the coins, return `-1`.

Examples
- Input: `coins = [1,2,5]`, `amount = 11`  
  Output: `3`

Constraints
- `1 <= coins.length <= 12`
- `1 <= coins[i] <= 2^31 - 1`
- `0 <= amount <= 10^4`

Hints (optional)
- Use bottom-up DP where `dp[x]` stores minimum coins to make amount `x`.

Canonical solution
- `/languages/python/problems/solutions/35-coin-change.py`
