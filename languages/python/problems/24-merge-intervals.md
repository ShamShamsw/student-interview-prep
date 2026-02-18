# 24. Merge Intervals

Difficulty: Medium  
Topics: array, sorting, intervals

Statement
Given an array of intervals where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals and return an array of the non-overlapping intervals covering all input intervals.

Examples
- Input: `intervals = [[1,3],[2,6],[8,10],[15,18]]`  
  Output: `[[1,6],[8,10],[15,18]]`

Constraints
- `1 <= intervals.length <= 10^4`
- `0 <= start_i <= end_i <= 10^4`

Hints (optional)
- Sort by start time, then merge greedily.

Canonical solution
- `/languages/python/problems/solutions/24-merge-intervals.py`
