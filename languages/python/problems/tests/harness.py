from __future__ import annotations

import importlib.util
from collections import deque
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable


PROBLEMS_DIR = Path(__file__).resolve().parents[1]
SOLUTIONS_DIR = PROBLEMS_DIR / "solutions"


@lru_cache(maxsize=None)
def _load_module(problem_number: int):
    pattern = f"{problem_number:02d}-*.py"
    matches = sorted(SOLUTIONS_DIR.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"No solution file found for problem {problem_number:02d}")

    file_path = matches[0]
    module_name = f"solution_{problem_number:02d}"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to import {file_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def solution_instance(problem_number: int) -> Any:
    module = _load_module(problem_number)
    return module.Solution()


def solution_module(problem_number: int) -> Any:
    return _load_module(problem_number)


def run_method(problem_number: int, method_name: str, *args: Any, **kwargs: Any) -> Any:
    instance = solution_instance(problem_number)
    method = getattr(instance, method_name)
    return method(*args, **kwargs)


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None) -> None:
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


class GraphNode:
    def __init__(self, val: int = 0, neighbors: list["GraphNode"] | None = None) -> None:
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def build_linked_list(values: Iterable[int]) -> ListNode | None:
    head: ListNode | None = None
    tail: ListNode | None = None

    for value in values:
        node = ListNode(value)
        if head is None:
            head = node
            tail = node
        else:
            tail.next = node
            tail = node

    return head


def linked_list_to_list(head: ListNode | None) -> list[int]:
    values: list[int] = []
    current = head
    while current is not None:
        values.append(current.val)
        current = current.next
    return values


def build_cycle_linked_list(values: list[int], cycle_pos: int) -> ListNode | None:
    head = build_linked_list(values)
    if head is None or cycle_pos < 0:
        return head

    cycle_node: ListNode | None = None
    current = head
    index = 0
    while current.next is not None:
        if index == cycle_pos:
            cycle_node = current
        current = current.next
        index += 1

    if index == cycle_pos:
        cycle_node = current

    if cycle_node is not None:
        current.next = cycle_node

    return head


def build_tree(level_values: list[int | None]) -> TreeNode | None:
    if not level_values:
        return None
    if level_values[0] is None:
        return None

    root = TreeNode(level_values[0])
    queue: deque[TreeNode] = deque([root])
    index = 1

    while queue and index < len(level_values):
        node = queue.popleft()

        if index < len(level_values) and level_values[index] is not None:
            node.left = TreeNode(level_values[index])
            queue.append(node.left)
        index += 1

        if index < len(level_values) and level_values[index] is not None:
            node.right = TreeNode(level_values[index])
            queue.append(node.right)
        index += 1

    return root


def find_bst_node(root: TreeNode | None, target: int) -> TreeNode | None:
    current = root
    while current is not None:
        if current.val == target:
            return current
        if target < current.val:
            current = current.left
        else:
            current = current.right
    return None


def build_graph(adj_list: list[list[int]]) -> GraphNode | None:
    if not adj_list:
        return None

    nodes = {index + 1: GraphNode(index + 1) for index in range(len(adj_list))}
    for index, neighbors in enumerate(adj_list, start=1):
        nodes[index].neighbors = [nodes[n] for n in neighbors]

    return nodes[1]


def graph_to_adj_list(node: GraphNode | None) -> list[list[int]]:
    if node is None:
        return []

    queue = deque([node])
    visited: dict[int, GraphNode] = {}

    while queue:
        current = queue.popleft()
        if current.val in visited:
            continue
        visited[current.val] = current

        for neighbor in current.neighbors:
            if neighbor.val not in visited:
                queue.append(neighbor)

    max_val = max(visited)
    result: list[list[int]] = [[] for _ in range(max_val)]
    for value, graph_node in visited.items():
        result[value - 1] = sorted(neighbor.val for neighbor in graph_node.neighbors)

    return result


def normalize_nested_lists(values: list[list[int]]) -> list[list[int]]:
    return sorted([sorted(group) for group in values])
