from collections import defaultdict
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)

        for value in strs:
            key = tuple(sorted(value))
            groups[key].append(value)

        return list(groups.values())
