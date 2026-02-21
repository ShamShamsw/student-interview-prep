from collections import Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not t or not s:
            return ""

        need = Counter(t)
        window = {}
        have = 0
        required = len(need)

        result_left = 0
        result_right = float("inf")
        left = 0

        for right, char in enumerate(s):
            window[char] = window.get(char, 0) + 1

            if char in need and window[char] == need[char]:
                have += 1

            while have == required:
                if (right - left) < (result_right - result_left):
                    result_left, result_right = left, right

                left_char = s[left]
                window[left_char] -= 1
                if left_char in need and window[left_char] < need[left_char]:
                    have -= 1
                left += 1

        if result_right == float("inf"):
            return ""

        return s[result_left:result_right + 1]
