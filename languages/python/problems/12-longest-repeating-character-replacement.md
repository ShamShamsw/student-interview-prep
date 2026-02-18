# 12. Longest Repeating Character Replacement

Difficulty: Medium  
Topics: string, sliding-window

Statement
Given a string `s` and an integer `k`, you can replace at most `k` characters. Return the length of the longest substring containing the same letter after replacements.

Examples
- Input: `s = "ABAB"`, `k = 2`  
  Output: `4`

Constraints
- `1 <= s.length <= 10^5`
- `s` consists of uppercase English letters.
- `0 <= k <= s.length`

Hints (optional)
- Track the most frequent character count in the window.

Canonical solution
- `/languages/python/problems/solutions/12-longest-repeating-character-replacement.py`
