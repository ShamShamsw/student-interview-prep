# 14. Minimum Window Substring

Difficulty: Hard  
Topics: string, sliding-window, hash-map

Statement
Given strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window.

If there is no such substring, return an empty string.

Examples
- Input: `s = "ADOBECODEBANC"`, `t = "ABC"`  
  Output: `"BANC"`

Constraints
- `1 <= s.length, t.length <= 10^5`

Hints (optional)
- Expand and contract a window while tracking required counts.

Canonical solution
- `/languages/python/problems/solutions/14-minimum-window-substring.py`
