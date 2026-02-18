# 19. Search in Rotated Sorted Array

Difficulty: Medium  
Topics: array, binary-search

Statement
There is an integer array `nums` sorted in ascending order and then rotated at an unknown pivot.

Given `nums` and `target`, return the index of `target` if it exists, otherwise return `-1`.

Examples
- Input: `nums = [4,5,6,7,0,1,2]`, `target = 0`  
  Output: `4`

Constraints
- `1 <= nums.length <= 5000`
- `-10^4 <= nums[i], target <= 10^4`
- All values in `nums` are unique.

Hints (optional)
- In each binary-search step, one side is always sorted.

Canonical solution
- `/languages/python/problems/solutions/19-search-in-rotated-sorted-array.py`
