if "Node" not in globals():

    class Node:
        def __init__(self, val=0, neighbors=None):
            self.val = val
            self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node: "Node | None") -> "Node | None":
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
