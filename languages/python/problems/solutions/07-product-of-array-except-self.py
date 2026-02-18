from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        length = len(nums)
        result = [1] * length

        prefix = 1
        for index in range(length):
            result[index] = prefix
            prefix *= nums[index]

        suffix = 1
        for index in range(length - 1, -1, -1):
            result[index] *= suffix
            suffix *= nums[index]

        return result
