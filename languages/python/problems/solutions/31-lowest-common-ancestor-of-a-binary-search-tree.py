class Solution:
    def lowestCommonAncestor(self, root, p, q):
        current = root

        while current is not None:
            if p.val < current.val and q.val < current.val:
                current = current.left
            elif p.val > current.val and q.val > current.val:
                current = current.right
            else:
                return current

        return None
