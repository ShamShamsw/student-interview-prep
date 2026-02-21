class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        need = [0] * 26
        have = [0] * 26
        offset = ord("a")

        for char in s1:
            need[ord(char) - offset] += 1

        window = len(s1)
        for index, char in enumerate(s2):
            have[ord(char) - offset] += 1

            if index >= window:
                left_char = s2[index - window]
                have[ord(left_char) - offset] -= 1

            if have == need:
                return True

        return False
