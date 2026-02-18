# 29. Valid Binary Search Tree

Difficulty: Medium  
Topics: tree, depth-first-search, binary-search-tree

Statement
Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as:
- The left subtree contains only nodes with keys strictly less than the node's key.
- The right subtree contains only nodes with keys strictly greater than the node's key.
- Both subtrees must also be binary search trees.

Examples
- Input: `root = [2,1,3]`  
  Output: `true`

Constraints
- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-2^31 <= Node.val <= 2^31 - 1`

Hints (optional)
- Track allowed `(low, high)` bounds while traversing.

Canonical solution
- `/languages/python/problems/solutions/29-valid-binary-search-tree.py`
