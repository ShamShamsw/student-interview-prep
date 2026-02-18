class Solution:
    def cloneGraph(self, node):
        if node is None:
            return None

        copies = {}

        def dfs(current):
            if current in copies:
                return copies[current]

            clone = Node(current.val)
            copies[current] = clone

            for neighbor in current.neighbors:
                clone.neighbors.append(dfs(neighbor))

            return clone

        return dfs(node)
