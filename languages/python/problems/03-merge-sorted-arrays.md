# 03. Merge Sorted Arrays

Difficulty: Easy  
Topics: array, two-pointers

Statement
You are given two integer arrays `nums1` and `nums2`, sorted in non-decreasing order, and two integers `m` and `n`.

Merge `nums2` into `nums1` as one sorted array in-place.

Examples
- Input: `nums1 = [1,2,3,0,0,0]`, `m = 3`, `nums2 = [2,5,6]`, `n = 3`  
  Output: `[1,2,2,3,5,6]`

Constraints
- `nums1.length == m + n`
- `0 <= m, n <= 200`
- `-10^9 <= nums1[i], nums2[i] <= 10^9`

Hints (optional)
- Fill from the end of `nums1` using two pointers.

Canonical solution
- `/languages/python/problems/solutions/03-merge-sorted-arrays.py`
