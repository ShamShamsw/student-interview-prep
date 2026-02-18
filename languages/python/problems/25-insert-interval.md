# 25. Insert Interval

Difficulty: Medium  
Topics: array, intervals

Statement
You are given an array of non-overlapping intervals sorted by start time and a new interval `newInterval`.

Insert `newInterval` into the intervals and merge if necessary.

Examples
- Input: `intervals = [[1,3],[6,9]]`, `newInterval = [2,5]`  
  Output: `[[1,5],[6,9]]`

Constraints
- `0 <= intervals.length <= 10^4`
- `intervals` is sorted by start and non-overlapping.
- `0 <= start <= end <= 10^5`

Hints (optional)
- Add intervals before overlap, merge overlap, then append remaining.

Canonical solution
- `/languages/python/problems/solutions/25-insert-interval.py`
