from typing import List


class Codec:
    def encode(self, strs: List[str]) -> str:
        parts = []
        for text in strs:
            parts.append(f"{len(text)}#{text}")
        return "".join(parts)

    def decode(self, s: str) -> List[str]:
        result = []
        index = 0

        while index < len(s):
            separator = index
            while s[separator] != "#":
                separator += 1

            size = int(s[index:separator])
            start = separator + 1
            end = start + size
            result.append(s[start:end])
            index = end

        return result
