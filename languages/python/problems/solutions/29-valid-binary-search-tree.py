class Solution:
    def isValidBST(self, root) -> bool:
        def dfs(node, lower, upper):
            if node is None:
                return True
            if not (lower < node.val < upper):
                return False
            return dfs(node.left, lower, node.val) and dfs(node.right, node.val, upper)

        return dfs(root, float("-inf"), float("inf"))
