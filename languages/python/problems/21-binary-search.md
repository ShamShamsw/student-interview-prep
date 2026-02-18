# 21. Binary Search

Difficulty: Easy  
Topics: array, binary-search

Statement
Given a sorted array `nums` and an integer `target`, return the index of `target` if it exists; otherwise return `-1`.

You must write an algorithm with `O(log n)` runtime complexity.

Examples
- Input: `nums = [-1,0,3,5,9,12]`, `target = 9`  
  Output: `4`

Constraints
- `1 <= nums.length <= 10^4`
- `-10^4 < nums[i], target < 10^4`
- `nums` contains unique values sorted ascending.

Hints (optional)
- Maintain `left` and `right` pointers and update by midpoint comparisons.

Canonical solution
- `/languages/python/problems/solutions/21-binary-search.py`
