from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows = len(grid)
        cols = len(grid[0])
        count = 0

        def dfs(row: int, col: int) -> None:
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return
            if grid[row][col] != "1":
                return

            grid[row][col] = "0"
            dfs(row + 1, col)
            dfs(row - 1, col)
            dfs(row, col + 1)
            dfs(row, col - 1)

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == "1":
                    count += 1
                    dfs(row, col)

        return count
