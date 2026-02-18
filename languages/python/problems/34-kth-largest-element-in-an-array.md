# 34. Kth Largest Element in an Array

Difficulty: Medium  
Topics: array, heap, divide-and-conquer

Statement
Given an integer array `nums` and an integer `k`, return the `k`th largest element in the array.

Note that it is the `k`th largest element in sorted order, not the `k`th distinct element.

Examples
- Input: `nums = [3,2,1,5,6,4]`, `k = 2`  
  Output: `5`

Constraints
- `1 <= k <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

Hints (optional)
- Maintain a min-heap of size `k` while scanning values.

Canonical solution
- `/languages/python/problems/solutions/34-kth-largest-element-in-an-array.py`
