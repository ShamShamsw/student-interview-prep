import math
from typing import List


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        left = 1
        right = max(piles)
        answer = right

        while left <= right:
            middle = (left + right) // 2
            hours = sum(math.ceil(pile / middle) for pile in piles)

            if hours <= h:
                answer = middle
                right = middle - 1
            else:
                left = middle + 1

        return answer
