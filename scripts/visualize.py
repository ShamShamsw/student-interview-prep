#!/usr/bin/env python3
"""Algorithm Visualizer for Interview Prep.

Provides step-by-step visualization of common algorithms.

Supported algorithms:
- Two Sum (hash table approach)
- Binary Search
- Merge Sort
- Quick Sort
- BFS/DFS traversal
- Dynamic Programming patterns

Usage:
    python scripts/visualize.py two-sum --array "[2,7,11,15]" --target 9
    python scripts/visualize.py binary-search --array "[1,2,3,4,5]" --target 3
    python scripts/visualize.py merge-sort --array "[5,2,8,1,9]"
    python scripts/visualize.py bfs --graph "{'A':['B','C'],'B':['D'],'C':['D'],'D':[]}" --start A
"""

from __future__ import annotations

import ast
import json
import time
from typing import Any

# Color codes
COLORS = {
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "reset": "\033[0m",
}


def colorize(text: str, color: str) -> str:
    """Apply color to text."""
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"


def pause(delay: float = 0.8) -> None:
    """Pause for visualization."""
    time.sleep(delay)


class AlgorithmVisualizer:
    """Visualize algorithm execution step-by-step."""

    def __init__(self, delay: float = 0.8):
        """Initialize visualizer."""
        self.delay = delay
        self.step_count = 0
    
    def print_step(self, description: str) -> None:
        """Print a step with counter."""
        self.step_count += 1
        print(colorize(f"\n📍 Step {self.step_count}: {description}", "cyan"))
        pause(self.delay)
    
    def print_array(
        self,
        array: list[Any],
        highlight: list[int] | None = None,
        label: str = "",
    ) -> None:
        """Print array with optional highlighting."""
        if label:
            print(f"   {label}: ", end="")
        else:
            print("   ", end="")
        
        for i, val in enumerate(array):
            if highlight and i in highlight:
                print(colorize(f"[{val}]", "yellow"), end=" ")
            else:
                print(colorize(f" {val} ", "dim"), end=" ")
        print()
    
    def visualize_two_sum(self, nums: list[int], target: int) -> None:
        """Visualize Two Sum algorithm using hash table."""
        print(colorize("\n🎯 TWO SUM VISUALIZATION", "bold"))
        print("=" * 60)
        print(f"\nInput: nums = {nums}, target = {target}")
        print(f"\nGoal: Find two indices where nums[i] + nums[j] = {target}")
        
        self.print_step("Initialize empty hash table to store seen numbers")
        seen = {}
        print(f"   seen = {{}}")
        
        self.print_step("Iterate through array")
        
        for i, num in enumerate(nums):
            self.print_step(f"Check index {i}, value = {num}")
            self.print_array(nums, highlight=[i], label="Array")
            
            complement = target - num
            print(f"   Complement needed: {target} - {num} = {complement}")
            
            if complement in seen:
                self.print_step(f"✅ Found! {complement} at index {seen[complement]}, {num} at index {i}")
                print(colorize(f"   Answer: [{seen[complement]}, {i}]", "green"))
                print(f"   Verification: {nums[seen[complement]]} + {nums[i]} = {target}")
                return
            
            seen[num] = i
            print(f"   Store: seen[{num}] = {i}")
            print(f"   seen = {seen}")
        
        print(colorize("\n❌ No solution found", "red"))
    
    def visualize_binary_search(self, nums: list[int], target: int) -> None:
        """Visualize Binary Search algorithm."""
        print(colorize("\n🎯 BINARY SEARCH VISUALIZATION", "bold"))
        print("=" * 60)
        print(f"\nInput: nums = {nums}, target = {target}")
        print(f"\nGoal: Find index of {target} in sorted array")
        
        left, right = 0, len(nums) - 1
        
        self.print_step("Initialize pointers: left = 0, right = len(nums) - 1")
        print(f"   left = {left}, right = {right}")
        
        while left <= right:
            mid = (left + right) // 2
            
            self.print_step(f"Calculate mid = (left + right) // 2 = {mid}")
            self.print_array(nums, highlight=[left, mid, right], label="Array")
            print(f"   left = {left}, mid = {mid}, right = {right}")
            print(f"   nums[mid] = {nums[mid]}")
            
            if nums[mid] == target:
                self.print_step(f"✅ Found! Target {target} at index {mid}")
                print(colorize(f"   Answer: {mid}", "green"))
                return
            elif nums[mid] < target:
                self.print_step(f"nums[mid] ({nums[mid]}) < target ({target}), search right half")
                left = mid + 1
                print(f"   Update: left = {left}")
            else:
                self.print_step(f"nums[mid] ({nums[mid]}) > target ({target}), search left half")
                right = mid - 1
                print(f"   Update: right = {right}")
        
        print(colorize(f"\n❌ Target {target} not found in array", "red"))
    
    def visualize_merge_sort(self, nums: list[int]) -> None:
        """Visualize Merge Sort algorithm."""
        print(colorize("\n🎯 MERGE SORT VISUALIZATION", "bold"))
        print("=" * 60)
        print(f"\nInput: nums = {nums}")
        print(f"\nGoal: Sort array using divide-and-conquer")
        
        def merge_sort_helper(arr: list[int], level: int = 0) -> list[int]:
            indent = "  " * level
            
            if len(arr) <= 1:
                print(f"{indent}Base case: {arr}")
                return arr
            
            mid = len(arr) // 2
            self.print_step(f"Divide array at mid = {mid}")
            print(f"{indent}Left:  {arr[:mid]}")
            print(f"{indent}Right: {arr[mid:]}")
            
            left = merge_sort_helper(arr[:mid], level + 1)
            right = merge_sort_helper(arr[mid:], level + 1)
            
            self.print_step(f"Merge {left} and {right}")
            result = []
            i = j = 0
            
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            
            result.extend(left[i:])
            result.extend(right[j:])
            
            print(f"{indent}Result: {result}")
            return result
        
        sorted_arr = merge_sort_helper(nums)
        print(colorize(f"\n✅ Final sorted array: {sorted_arr}", "green"))
    
    def visualize_bfs(self, graph: dict[str, list[str]], start: str) -> None:
        """Visualize BFS traversal."""
        print(colorize("\n🎯 BREADTH-FIRST SEARCH VISUALIZATION", "bold"))
        print("=" * 60)
        print(f"\nGraph: {graph}")
        print(f"Start node: {start}")
        print(f"\nGoal: Visit all nodes using BFS (level-by-level)")
        
        from collections import deque
        
        self.print_step("Initialize queue with start node")
        queue = deque([start])
        visited = {start}
        
        print(f"   queue = {list(queue)}")
        print(f"   visited = {visited}")
        
        order = []
        
        while queue:
            self.print_step("Dequeue node from front")
            node = queue.popleft()
            order.append(node)
            
            print(f"   Current node: {colorize(node, 'yellow')}")
            print(f"   queue = {list(queue)}")
            print(f"   visited = {visited}")
            
            neighbors = graph.get(node, [])
            self.print_step(f"Check neighbors of {node}: {neighbors}")
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    print(f"   ➕ Add {neighbor} to queue")
                    queue.append(neighbor)
                    visited.add(neighbor)
                else:
                    print(f"   ⏭️  {neighbor} already visited, skip")
            
            print(f"   queue = {list(queue)}")
            print(f"   visited = {visited}")
        
        print(colorize(f"\n✅ BFS order: {' → '.join(order)}", "green"))
    
    def visualize_dfs(self, graph: dict[str, list[str]], start: str) -> None:
        """Visualize DFS traversal."""
        print(colorize("\n🎯 DEPTH-FIRST SEARCH VISUALIZATION", "bold"))
        print("=" * 60)
        print(f"\nGraph: {graph}")
        print(f"Start node: {start}")
        print(f"\nGoal: Visit all nodes using DFS (go deep first)")
        
        self.print_step("Initialize stack with start node")
        stack = [start]
        visited = set()
        order = []
        
        print(f"   stack = {stack}")
        print(f"   visited = {visited}")
        
        while stack:
            self.print_step("Pop node from stack")
            node = stack.pop()
            
            if node in visited:
                print(f"   {node} already visited, skip")
                continue
            
            visited.add(node)
            order.append(node)
            
            print(f"   Current node: {colorize(node, 'yellow')}")
            print(f"   visited = {visited}")
            
            neighbors = graph.get(node, [])
            self.print_step(f"Add neighbors of {node}: {neighbors}")
            
            for neighbor in reversed(neighbors):  # Reverse to maintain left-to-right order
                if neighbor not in visited:
                    print(f"   ➕ Push {neighbor} to stack")
                    stack.append(neighbor)
            
            print(f"   stack = {stack}")
        
        print(colorize(f"\n✅ DFS order: {' → '.join(order)}", "green"))
    
    def visualize_sliding_window(self, s: str, k: int) -> None:
        """Visualize sliding window technique."""
        print(colorize("\n🎯 SLIDING WINDOW VISUALIZATION", "bold"))
        print("=" * 60)
        print(f"\nInput: s = '{s}', k = {k}")
        print(f"\nGoal: Find max sum of any subarray of size {k}")
        
        if len(s) < k:
            print(colorize("\n❌ Array too small for window size", "red"))
            return
        
        # Convert string to numbers for demo
        nums = [ord(c) for c in s]
        
        self.print_step(f"Initialize window of size {k}")
        window_sum = sum(nums[:k])
        max_sum = window_sum
        
        print(f"   Window: {nums[:k]}")
        print(f"   Sum: {window_sum}")
        
        for i in range(k, len(nums)):
            self.print_step(f"Slide window to position {i-k+1}")
            
            # Remove leftmost element
            removed = nums[i - k]
            added = nums[i]
            
            print(f"   Remove: {removed}")
            print(f"   Add: {added}")
            
            window_sum = window_sum - removed + added
            max_sum = max(max_sum, window_sum)
            
            print(f"   Window: {nums[i-k+1:i+1]}")
            print(f"   Sum: {window_sum}")
            print(f"   Max so far: {max_sum}")
        
        print(colorize(f"\n✅ Maximum window sum: {max_sum}", "green"))


def main() -> None:
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Visualize algorithm execution")
    parser.add_argument("algorithm", choices=[
        "two-sum", "binary-search", "merge-sort", "bfs", "dfs", "sliding-window"
    ], help="Algorithm to visualize")
    parser.add_argument("--array", type=str, help="Input array (JSON format)")
    parser.add_argument("--target", type=int, help="Target value")
    parser.add_argument("--graph", type=str, help="Graph (JSON format)")
    parser.add_argument("--start", type=str, help="Start node for graph traversal")
    parser.add_argument("--delay", type=float, default=0.8, help="Delay between steps (seconds)")
    parser.add_argument("--k", type=int, help="Window size for sliding window")
    
    args = parser.parse_args()
    
    visualizer = AlgorithmVisualizer(delay=args.delay)
    
    try:
        if args.algorithm == "two-sum":
            if not args.array or args.target is None:
                print("Error: --array and --target required for two-sum")
                return
            nums = json.loads(args.array)
            visualizer.visualize_two_sum(nums, args.target)
        
        elif args.algorithm == "binary-search":
            if not args.array or args.target is None:
                print("Error: --array and --target required for binary-search")
                return
            nums = json.loads(args.array)
            visualizer.visualize_binary_search(sorted(nums), args.target)
        
        elif args.algorithm == "merge-sort":
            if not args.array:
                print("Error: --array required for merge-sort")
                return
            nums = json.loads(args.array)
            visualizer.visualize_merge_sort(nums)
        
        elif args.algorithm == "bfs":
            if not args.graph or not args.start:
                print("Error: --graph and --start required for bfs")
                return
            graph = ast.literal_eval(args.graph)
            visualizer.visualize_bfs(graph, args.start)
        
        elif args.algorithm == "dfs":
            if not args.graph or not args.start:
                print("Error: --graph and --start required for dfs")
                return
            graph = ast.literal_eval(args.graph)
            visualizer.visualize_dfs(graph, args.start)
        
        elif args.algorithm == "sliding-window":
            if not args.array or not args.k:
                print("Error: --array and --k required for sliding-window")
                return
            s = json.loads(args.array)
            visualizer.visualize_sliding_window(str(s), args.k)
    
    except Exception as e:
        print(colorize(f"\n❌ Error: {e}", "red"))
        print("\nExample usage:")
        print('  python scripts/visualize.py two-sum --array "[2,7,11,15]" --target 9')


if __name__ == "__main__":
    main()
