from __future__ import annotations

from harness import normalize_nested_lists, run_method


def test_01_two_sum() -> None:
    result = run_method(1, "twoSum", [2, 7, 11, 15], 9)
    assert result == [0, 1]


def test_02_valid_parentheses() -> None:
    assert run_method(2, "isValid", "()[]{}") is True
    assert run_method(2, "isValid", "([)]") is False


def test_03_merge_sorted_arrays() -> None:
    nums1 = [1, 2, 3, 0, 0, 0]
    run_method(3, "merge", nums1, 3, [2, 5, 6], 3)
    assert nums1 == [1, 2, 2, 3, 5, 6]


def test_04_best_time_to_buy_and_sell_stock() -> None:
    assert run_method(4, "maxProfit", [7, 1, 5, 3, 6, 4]) == 5


def test_05_contains_duplicate() -> None:
    assert run_method(5, "containsDuplicate", [1, 2, 3, 1]) is True
    assert run_method(5, "containsDuplicate", [1, 2, 3, 4]) is False


def test_06_valid_anagram() -> None:
    assert run_method(6, "isAnagram", "anagram", "nagaram") is True
    assert run_method(6, "isAnagram", "rat", "car") is False


def test_07_product_of_array_except_self() -> None:
    assert run_method(7, "productExceptSelf", [1, 2, 3, 4]) == [24, 12, 8, 6]


def test_08_group_anagrams() -> None:
    result = run_method(8, "groupAnagrams", ["eat", "tea", "tan", "ate", "nat", "bat"])
    assert normalize_nested_lists(result) == normalize_nested_lists(
        [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
    )


def test_09_top_k_frequent() -> None:
    result = run_method(9, "topKFrequent", [1, 1, 1, 2, 2, 3], 2)
    assert set(result) == {1, 2}


def test_11_longest_substring_without_repeating_characters() -> None:
    assert run_method(11, "lengthOfLongestSubstring", "abcabcbb") == 3


def test_12_longest_repeating_character_replacement() -> None:
    assert run_method(12, "characterReplacement", "AABABBA", 1) == 4


def test_13_permutation_in_string() -> None:
    assert run_method(13, "checkInclusion", "ab", "eidbaooo") is True
    assert run_method(13, "checkInclusion", "ab", "eidboaoo") is False


def test_14_minimum_window_substring() -> None:
    assert run_method(14, "minWindow", "ADOBECODEBANC", "ABC") == "BANC"


def test_15_valid_palindrome() -> None:
    assert run_method(15, "isPalindrome", "A man, a plan, a canal: Panama") is True
    assert run_method(15, "isPalindrome", "race a car") is False


def test_16_two_sum_ii() -> None:
    assert run_method(16, "twoSum", [2, 7, 11, 15], 9) == [1, 2]


def test_17_three_sum() -> None:
    result = run_method(17, "threeSum", [-1, 0, 1, 2, -1, -4])
    assert normalize_nested_lists(result) == normalize_nested_lists([[-1, -1, 2], [-1, 0, 1]])


def test_18_container_with_most_water() -> None:
    assert run_method(18, "maxArea", [1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49


def test_19_search_in_rotated_sorted_array() -> None:
    assert run_method(19, "search", [4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert run_method(19, "search", [4, 5, 6, 7, 0, 1, 2], 3) == -1


def test_20_find_minimum_in_rotated_sorted_array() -> None:
    assert run_method(20, "findMin", [3, 4, 5, 1, 2]) == 1


def test_21_binary_search() -> None:
    assert run_method(21, "search", [-1, 0, 3, 5, 9, 12], 9) == 4
    assert run_method(21, "search", [-1, 0, 3, 5, 9, 12], 2) == -1


def test_22_koko_eating_bananas() -> None:
    assert run_method(22, "minEatingSpeed", [3, 6, 7, 11], 8) == 4


def test_24_merge_intervals() -> None:
    assert run_method(24, "merge", [[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]


def test_25_insert_interval() -> None:
    result = run_method(25, "insert", [[1, 3], [6, 9]], [2, 5])
    assert result == [[1, 5], [6, 9]]


def test_34_kth_largest_element_in_array() -> None:
    assert run_method(34, "findKthLargest", [3, 2, 1, 5, 6, 4], 2) == 5


def test_35_coin_change() -> None:
    assert run_method(35, "coinChange", [1, 2, 5], 11) == 3
    assert run_method(35, "coinChange", [2], 3) == -1
