# 33. Clone Graph

Difficulty: Medium  
Topics: graph, depth-first-search, breadth-first-search, hash-map

Statement
Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph.

Each node contains a value and a list of its neighbors.

Examples
- Input: `adjList = [[2,4],[1,3],[2,4],[1,3]]`  
  Output: `[[2,4],[1,3],[2,4],[1,3]]`

Constraints
- The number of nodes in the graph is in the range `[0, 100]`.
- `1 <= Node.val <= 100`
- `Node.val` is unique for each node.
- There are no repeated edges and no self-loops.

Hints (optional)
- Use a map from original node to cloned node while traversing.

Canonical solution
- `/languages/python/problems/solutions/33-clone-graph.py`
