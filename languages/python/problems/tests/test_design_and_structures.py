from __future__ import annotations

from harness import (
    GraphNode,
    build_cycle_linked_list,
    build_graph,
    build_linked_list,
    build_tree,
    find_bst_node,
    graph_to_adj_list,
    linked_list_to_list,
    normalize_nested_lists,
    solution_instance,
    solution_module,
)


def test_10_encode_decode_strings_round_trip() -> None:
    module = solution_module(10)
    codec = module.Codec()
    values = ["lint", "", "code", "#hash"]
    encoded = codec.encode(values)
    decoded = codec.decode(encoded)
    assert decoded == values


def test_23_time_map() -> None:
    module = solution_module(23)
    time_map = module.TimeMap()

    time_map.set("foo", "bar", 1)
    assert time_map.get("foo", 1) == "bar"
    assert time_map.get("foo", 3) == "bar"

    time_map.set("foo", "bar2", 4)
    assert time_map.get("foo", 4) == "bar2"
    assert time_map.get("foo", 5) == "bar2"


def test_26_reverse_linked_list() -> None:
    head = build_linked_list([1, 2, 3, 4, 5])
    result = solution_instance(26).reverseList(head)
    assert linked_list_to_list(result) == [5, 4, 3, 2, 1]


def test_27_linked_list_cycle() -> None:
    head = build_cycle_linked_list([3, 2, 0, -4], cycle_pos=1)
    assert solution_instance(27).hasCycle(head) is True


def test_28_merge_two_sorted_lists() -> None:
    left = build_linked_list([1, 2, 4])
    right = build_linked_list([1, 3, 4])
    merged = solution_instance(28).mergeTwoLists(left, right)
    assert linked_list_to_list(merged) == [1, 1, 2, 3, 4, 4]


def test_29_valid_binary_search_tree() -> None:
    root = build_tree([2, 1, 3])
    assert solution_instance(29).isValidBST(root) is True

    invalid_root = build_tree([5, 1, 4, None, None, 3, 6])
    assert solution_instance(29).isValidBST(invalid_root) is False


def test_30_binary_tree_level_order_traversal() -> None:
    root = build_tree([3, 9, 20, None, None, 15, 7])
    result = solution_instance(30).levelOrder(root)
    assert result == [[3], [9, 20], [15, 7]]


def test_31_lowest_common_ancestor_bst() -> None:
    root = build_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    p = find_bst_node(root, 2)
    q = find_bst_node(root, 8)
    lca = solution_instance(31).lowestCommonAncestor(root, p, q)
    assert lca.val == 6


def test_32_number_of_islands() -> None:
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert solution_instance(32).numIslands(grid) == 3


def test_33_clone_graph() -> None:
    module = solution_module(33)
    module.Node = GraphNode

    source = build_graph([[2, 4], [1, 3], [2, 4], [1, 3]])
    clone = module.Solution().cloneGraph(source)

    assert clone is not source
    assert normalize_nested_lists(graph_to_adj_list(clone)) == normalize_nested_lists(
        graph_to_adj_list(source)
    )
