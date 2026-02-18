# 31. Lowest Common Ancestor of a Binary Search Tree

Difficulty: Medium  
Topics: tree, binary-search-tree

Statement
Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes `p` and `q` in the BST.

According to the definition of LCA: "The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has both `p` and `q` as descendants (where a node can be a descendant of itself)."

Examples
- Input: `root = [6,2,8,0,4,7,9,null,null,3,5]`, `p = 2`, `q = 8`  
  Output: `6`

Constraints
- The number of nodes in the tree is in the range `[2, 10^5]`.
- `-10^9 <= Node.val <= 10^9`
- All `Node.val` are unique.
- `p != q` and both values exist in the BST.

Hints (optional)
- Use BST ordering: go left if both targets are smaller, right if both are larger.

Canonical solution
- `/languages/python/problems/solutions/31-lowest-common-ancestor-of-a-binary-search-tree.py`
