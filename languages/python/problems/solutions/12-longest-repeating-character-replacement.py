class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        counts = {}
        left = 0
        max_count = 0
        best = 0

        for right, char in enumerate(s):
            counts[char] = counts.get(char, 0) + 1
            max_count = max(max_count, counts[char])

            while (right - left + 1) - max_count > k:
                left_char = s[left]
                counts[left_char] -= 1
                left += 1

            best = max(best, right - left + 1)

        return best
