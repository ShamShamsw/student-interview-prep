from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        best = 0

        while left < right:
            width = right - left
            area = width * min(height[left], height[right])
            best = max(best, area)

            if height[left] <= height[right]:
                left += 1
            else:
                right -= 1

        return best
