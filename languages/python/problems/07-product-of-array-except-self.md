# 07. Product of Array Except Self

Difficulty: Medium  
Topics: array, prefix-suffix

Statement
Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all elements of `nums` except `nums[i]`.

Do not use division, and run in `O(n)` time.

Examples
- Input: `nums = [1,2,3,4]`  
  Output: `[24,12,8,6]`

Constraints
- `2 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`

Hints (optional)
- Build prefix products and suffix products.

Canonical solution
- `/languages/python/problems/solutions/07-product-of-array-except-self.py`
