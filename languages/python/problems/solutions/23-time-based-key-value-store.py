from collections import defaultdict
from typing import Dict, List, Tuple


class TimeMap:
    def __init__(self) -> None:
        self.data: Dict[str, List[Tuple[int, str]]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.data[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        values = self.data.get(key, [])

        left = 0
        right = len(values) - 1
        result = ""

        while left <= right:
            middle = (left + right) // 2
            time, text = values[middle]

            if time <= timestamp:
                result = text
                left = middle + 1
            else:
                right = middle - 1

        return result
