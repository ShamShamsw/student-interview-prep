```markdown
# Glossary (Beginner-Friendly)

## Core coding terms

- **Algorithm**: A step-by-step method to solve a problem.
- **Data structure**: A way to store and organize data (list, dict, stack, queue, tree, graph).
- **Time complexity**: How runtime grows as input grows (e.g., O(n), O(log n)).
- **Space complexity**: How memory usage grows as input grows.
- **Edge case**: Unusual input that often breaks code.
- **Refactor**: Improve code structure without changing behavior.

## Python and project terms

- **CLI**: Command-line interface app run from terminal.
- **API**: Interface where programs talk via HTTP endpoints.
- **Endpoint**: A specific API route like `/health`.
- **Validation**: Checking request/input format and constraints.
- **Test case**: One scenario that verifies expected behavior.
- **Regression**: A bug introduced into code that used to work.

## Open source workflow terms

- **Repository (repo)**: Project folder tracked by Git.
- **Branch**: A separate line of work.
- **Commit**: A saved snapshot of code changes.
- **Pull Request (PR)**: A request to merge code changes.
- **Issue**: A tracked task, bug, or feature request.
- **Maintainer**: Person responsible for reviewing and managing project contributions.

## Data science & analytics terms

- **DataFrame**: A tabular data structure with named rows and columns, like a spreadsheet in code (pandas, Spark).
- **EDA (Exploratory Data Analysis)**: Examining a dataset to summarize its characteristics before modeling.
- **Feature engineering**: Creating or transforming input variables to improve model performance.
- **Overfitting**: When a model learns training data too well and performs poorly on new data.
- **Underfitting**: When a model is too simple to capture patterns in the data (high bias).
- **Bias-variance tradeoff**: Balancing model simplicity (high bias) vs. sensitivity to training data (high variance).
- **Cross-validation**: Evaluating a model by training/testing on different folds of the data.
- **Regularization**: Adding a penalty term to prevent overfitting (L1 = Lasso, L2 = Ridge).
- **Hyperparameter**: A model setting configured before training (e.g., number of trees, learning rate).
- **Null hypothesis (H₀)**: The default assumption that there is no effect or no difference.
- **p-value**: Probability of observing the data assuming H₀ is true; < 0.05 often used to reject H₀.
- **Correlation**: A measure of how two variables move together (−1 to 1).
- **Outlier**: A data point that differs significantly from others; can skew statistics and model results.

## Data engineering terms

- **ETL**: Extract, Transform, Load — move data from source, transform it, then load to destination.
- **ELT**: Extract, Load, Transform — load raw data first, then transform inside the warehouse.
- **Data pipeline**: A series of automated steps that move and transform data.
- **DAG**: Directed Acyclic Graph — tasks with dependencies and no cycles; core concept in Airflow.
- **Idempotent**: A pipeline run multiple times with the same input produces the same output.
- **Parquet**: A columnar binary file format; faster and smaller than CSV for analytics workloads.
- **Data lake**: Storage of raw data at any scale in any format (JSON, CSV, Parquet) in object storage.
- **Data warehouse**: A structured analytical database optimized for fast SQL queries (Snowflake, BigQuery, Redshift).
- **Medallion architecture**: Bronze (raw) → Silver (cleaned) → Gold (business-ready) data layers.
- **dbt (data build tool)**: Framework for SQL-based transformations in the warehouse with versioning and testing.
- **Partition pruning**: Skipping irrelevant partitions during a query to improve performance.
- **Schema-on-read**: Data types are interpreted at query time (data lake model).
- **Schema-on-write**: Data types are enforced at load time (data warehouse model).
- **Slowly Changing Dimension (SCD)**: A dimension table that changes over time; Type 2 tracks history with new rows.
- **Star schema**: One central fact table joined to flat dimension tables; standard data warehouse design.
- **Window function**: SQL function that computes values across related rows without collapsing them (e.g., `RANK()`, `LAG()`, `SUM() OVER`).

```
