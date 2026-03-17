# Beginner Project 43: Sorting Algorithm Education Visualizer

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Instrumented quicksort, mergesort, and heapsort demos with empirical runtime and operation-count visualization

---

## Why This Project?

Sorting algorithms are one of the first places where computer science becomes visible: the same input list can be transformed by very different strategies, and those strategies show up both in the animation of the data and in the measured cost of the work. This project turns that idea into a small reproducible lab where students can inspect step-by-step behavior and then compare each algorithm with real benchmark data.

This project teaches end-to-end sorting visualization concepts where you can:

- load or auto-seed a reusable lesson-array library for common ordering patterns,
- run instrumented quicksort, mergesort, and heapsort on the same demo array,
- capture storyboard frames that show how each algorithm transforms the array over time,
- count comparisons, writes, swaps, and recursion or heap depth during execution,
- benchmark multiple algorithms over increasing array sizes with repeatable random trials,
- compare runtime growth empirically instead of only discussing Big-O notation abstractly,
- compare primitive-operation growth across input sizes,
- export trace bundles and benchmark bundles to JSON for later inspection,
- render a storyboard image that places sampled sort states side by side,
- render a runtime chart across benchmark sizes,
- render an operations chart across benchmark sizes,
- persist historical run summaries for repeatable auditing,
- and print a readable terminal report with algorithm previews and artifact paths.

---

## Separate Repository

You can also access this project in a separate repository:

[sorting algorithm education visualizer Repository](sorting-algorithm-education-visualizer.git)

---

## What You Will Build

You will build a sorting algorithm education visualizer that:

1. Loads lesson arrays from `data/array_sets.json` (or seeds a starter set of 4 arrays).
2. Selects a deterministic demo array for the main storyboard lesson.
3. Runs quicksort, mergesort, and heapsort on identical input values.
4. Captures step frames with active indices and explanatory notes during execution.
5. Tracks comparisons, writes, swaps, and maximum depth for each algorithm.
6. Samples storyboard frames so each algorithm can be compared side by side.
7. Benchmarks every algorithm across multiple array sizes and repeated trials.
8. Saves a runtime chart of average elapsed time versus input size.
9. Saves an operations chart of average primitive operations versus input size.
10. Persists a trace bundle, benchmark bundle, and run summary under `data/outputs/`.
11. Maintains an array library and run catalog for history and auditing.

---

## Requirements

- Python 3.11+
- `matplotlib`

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
   SORTING ALGORITHM EDUCATION VISUALIZER
======================================================================

Configuration:
   Project type:           sorting_algorithm_education_visualizer
   Algorithms:             Quick Sort, Merge Sort, Heap Sort
   Demo array:             lesson_random_12
   Benchmark sizes:        16, 32, 64, 96, 128
   Trials per size:        3
   Storyboard frames:      6
   Storyboard plot:        True
   Runtime chart:          True
   Operations chart:       True
   Max algorithms report:  3
   Random seed:            42

Startup:
   Data directory:         data/
   Outputs directory:      data/outputs/
   Array library:          data/array_sets.json (loaded 0 arrays)
   Run catalog:            data/runs.json (loaded 0 runs)
   Recent runs:            None yet

---

Session complete:
   Session ID:             20260317_211936
   Arrays available:       4
   Demo array:             lesson_random_12 (12 items)
   Algorithms run:         3
   Benchmark points:       45
   Elapsed time:           964.64 ms

Lesson metrics: fastest_algorithm=Quick Sort | fastest_runtime_ms=0.10749 | lowest_demo_ops=Quick Sort (76) | largest_array_size=128

Algorithm previews:
   Algorithm  | Time (ms) | Comparisons | Writes | Swaps | Depth | Sorted
   -----------+-----------+-------------+--------+-------+-------+--------
   Quick Sort | 0.2532    | 37          | 26     | 13    | 6     | yes
   Merge Sort | 0.1292    | 32          | 44     | 0     | 5     | yes
   Heap Sort  | 0.1042    | 51          | 66     | 33    | 4     | yes

Artifacts saved:
   Session record:         data/outputs/run_20260317_211936.json
   Trace bundle:           data/outputs/trace_20260317_211936.json
   Benchmark file:         data/outputs/benchmark_20260317_211936.json
   Storyboard plot:        data/outputs/storyboard_20260317_211936.png
   Runtime chart:          data/outputs/runtime_20260317_211936.png
   Operations chart:       data/outputs/operations_20260317_211936.png
```

---

## Run

```bash
python main.py
```
