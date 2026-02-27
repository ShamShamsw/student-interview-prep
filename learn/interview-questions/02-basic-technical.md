# Basic Technical Interview Questions

Foundational CS and programming concepts every developer should be comfortable with, regardless of role.

---

## Data Structures

1. **What is the difference between an array and a linked list?**
   _Compare: memory layout, access time, insertion/deletion cost._

2. **When would you use a hash map vs. a sorted array?**
   _Hash map: O(1) lookup, unordered. Sorted array: O(log n) search, ordered iteration._

3. **What is a stack? What is a queue? Give a real-world use case for each.**
   _Stack: undo history, call stack. Queue: task scheduling, BFS._

4. **Explain what a tree is. What makes a binary search tree special?**
   _BST property: left < node < right. Enables O(log n) search on average._

5. **What is a graph? Name two ways to represent one in code.**
   _Adjacency list vs. adjacency matrix. Trade-offs in space and lookup._

6. **What is a heap and when would you use one?**
   _Priority queue operations. Use case: finding k largest/smallest elements._

---

## Algorithms & Complexity

7. **Explain Big O notation. Why does it matter?**
   _Describes how runtime/space scales with input size. Helps compare approaches._

8. **What's the difference between O(n), O(n log n), and O(n²)?**
   _Give concrete examples: linear scan, merge sort, nested loops._

9. **Explain the difference between depth-first search and breadth-first search.**
   _DFS: go deep (stack/recursion). BFS: go wide (queue). When to use each._

10. **What is recursion? What's the risk of using it?**
    _A function calling itself. Risk: stack overflow without a base case or with deep recursion._

11. **Describe a divide-and-conquer algorithm.**
    _Merge sort: split, solve sub-problems, combine results._

12. **What is dynamic programming? How is it different from recursion?**
    _DP stores results of sub-problems to avoid recomputation. Memoization vs. tabulation._

---

## Programming Fundamentals

13. **What is the difference between a compiled language and an interpreted language?**
    _Compiled: translated to machine code ahead of time (C, Go). Interpreted: executed line by line (Python, JS)._

14. **What are value types vs. reference types?**
    _Value: holds the data (int, bool). Reference: holds a pointer to data (objects, lists)._

15. **Explain what a class is. What is an object?**
    _Class: blueprint. Object: instance of a blueprint._

16. **What is the difference between a function and a method?**
    _Method: a function that belongs to a class/object._

17. **What does "pass by value" vs. "pass by reference" mean?**
    _Value: copy is passed. Reference: pointer to original is passed._

18. **What is an exception? How do you handle one?**
    _An error that disrupts normal flow. Use try/except (Python) or try/catch (JS, Java)._

---

## Version Control & Tools

19. **What is Git? Why do developers use it?**
    _Distributed version control. Track changes, collaborate, revert mistakes._

20. **What is the difference between `git merge` and `git rebase`?**
    _Merge: creates a merge commit. Rebase: replays commits on top of another branch._

21. **What is a pull request and why is it important?**
    _A request to merge your branch. Enables code review, discussion, and CI checks._

22. **How would you resolve a merge conflict?**
    _Open the conflicted file, choose which changes to keep, test, commit._

---

## Testing

23. **What is a unit test? Why write them?**
    _Tests a single function/method in isolation. Catches regressions, documents behavior._

24. **What is the difference between unit tests, integration tests, and end-to-end tests?**
    _Unit: one function. Integration: multiple components. E2E: full user workflow._

25. **What is test-driven development (TDD)?**
    _Write the test first, watch it fail, write code to pass it, refactor._

---

## General Problem-Solving

26. **You're given a bug report with no reproduction steps. What do you do?**
    _Check logs, try to reproduce, narrow scope, add logging, bisect._

27. **How would you approach optimizing a slow function?**
    _Profile first, identify bottleneck, then optimize. Don't guess._

28. **Explain how you would design a solution before writing code.**
    _Understand requirements, sketch data flow, choose data structures, write pseudocode, then implement._

29. **What questions would you ask before starting a new feature?**
    _Requirements, edge cases, deadlines, existing code, testing expectations._

30. **How do you decide between two different approaches to a problem?**
    _Compare time/space complexity, readability, maintainability, and constraints._

---

## How to Study These

- For each question, write a 2–3 sentence answer from memory
- Then check — can you explain it to someone who doesn't code?
- If you can't explain it simply, review the concept before moving on
- Practice 3–5 questions per study session
