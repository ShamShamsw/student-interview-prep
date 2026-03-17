# Beginner Project 39: Interactive Optimization Visualizer

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Linear and nonlinear optimization, solver convergence inspection, and persistent visualization artifacts

---

## Why This Project?

Optimization is one of the most practical ways to turn business or engineering goals into concrete decisions. This project demonstrates how to define objective functions, enforce constraints, run deterministic solvers, and visualize why a chosen solution is optimal or near-optimal.

This project teaches end-to-end optimization workflow concepts where you can:

- load or auto-generate a reusable local optimization problem library,
- solve a constrained linear programming problem with an exact solver,
- solve a constrained nonlinear problem with iterative numerical optimization,
- inspect variable values, objective scores, and constraint slack values,
- track convergence history from solver callbacks,
- generate a feasible-region plot for the linear problem,
- generate a convergence plot for the nonlinear problem,
- generate a contour-and-path visualization of the nonlinear search route,
- export solution bundles and per-solution metadata to JSON,
- persist run summaries and historical solution catalogs,
- and print a readable terminal report with preview rows and export paths.

---

## Separate Repository

You can also access this project in a separate repository:

[quiz game Repository](https://github.com/ShamShamsw/interactive-optimization-visualizer.git)

---

## What You Will Build

You will build an optimization visualizer that:

1. Loads optimization problem definitions from `data/problems.json` (or seeds a starter set).
2. Includes at least one linear and one nonlinear optimization example.
3. Defines objective functions, bounds, and constraints in a readable JSON-backed format.
4. Solves the linear problem with `scipy.optimize.linprog`.
5. Solves the nonlinear problem with `scipy.optimize.minimize` using constrained optimization.
6. Tracks solver progress and objective history for iterative inspection.
7. Computes and exports variable assignments, objective values, and constraint slack values.
8. Saves a feasible-region plot for the linear program.
9. Saves a convergence plot for the nonlinear optimization run.
10. Saves a contour plot showing the nonlinear solver path.
11. Persists per-solution metadata and run summaries for history and auditing.

---

## Requirements

- Python 3.11+
- `matplotlib`
- `scipy`

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
   INTERACTIVE OPTIMIZATION VISUALIZER
======================================================================

Configuration:
   Project type:         interactive_optimization_visualizer
   Solver stack:         scipy.optimize + matplotlib
   Linear grid points:   220
   Max nonlinear iters:  60
   Feasible region plot: True
   Convergence plot:     True
   Path contour plot:    True
   Max sols in report:   6
   Random seed:          42

Startup:
   Data directory:       data/
   Outputs directory:    data/outputs/
   Problem library:      data/problems.json (loaded 2 problems)
   Run catalog:          data/runs.json (loaded 0 runs)
   Solution catalog:     data/solutions.json (loaded 0 records)
   Recent solutions:     None yet

---

Run complete:
   Run ID:               20260317_194303
   Problems loaded:      2
   Solutions generated:  2
   Successful solves:    2
   Elapsed time:         1428.53 ms

Dataset metrics: success_rate=100.0% | mean_iterations=3.0 | best_linear_objective=36.000 | best_nonlinear_objective=0.086

Solution previews:
   ID      | Problem                      | Kind      | Objective | Iters | Status
   --------+------------------------------+-----------+-----------+-------+----------------
   sol_001 | Production Mix Linear Progra | linear    |    36.000 |     0 | optimal
   sol_002 | Rippled Nonlinear Design Sea | nonlinear |     0.086 |     6 | optimal

Artifacts saved:
   Run record:           data/outputs/run_20260317_194303.json
   Bundle export:        data/outputs/solutions_20260317_194303.json
   Feasible region plot: data/outputs/feasible_region_20260317_194303.png
   Convergence plot:     data/outputs/convergence_20260317_194303.png
   Path contour plot:    data/outputs/path_contour_20260317_194303.png
   Metadata exports:     2
```

---

## Run

```bash
python main.py
```
