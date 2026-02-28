# Data Science Interview Questions

Commonly asked questions covering statistics, pandas, machine learning, SQL for data, and the data science process.

---

## Statistics & Probability

1. **What is the difference between mean, median, and mode? When would you use each?**
   _Mean: sensitive to outliers. Median: robust to outliers. Mode: for categorical data or finding the most frequent value._

2. **Explain the Central Limit Theorem (CLT). Why does it matter in practice?**
   _The distribution of sample means approaches a normal distribution as sample size grows, regardless of the population distribution. Enables confidence intervals and hypothesis tests on any data._

3. **What is the difference between standard deviation and standard error?**
   _Standard deviation measures spread within a dataset. Standard error measures how much a sample mean varies from the population mean: $SE = \sigma / \sqrt{n}$._

4. **What is a p-value? What does p < 0.05 actually mean?**
   _p-value is the probability of observing a result at least as extreme as the one obtained, assuming the null hypothesis is true. p < 0.05 means there is less than a 5% chance the result is due to random chance._

5. **What is the difference between Type I and Type II errors?**
   _Type I (false positive): reject H₀ when it is true (α). Type II (false negative): fail to reject H₀ when it is false (β). Power = 1 - β._

6. **What is correlation vs. causation? Give an example.**
   _Correlation: two variables move together. Causation: one directly causes the other. Example: ice cream sales and drowning rates are positively correlated (both driven by summer), but ice cream does not cause drowning._

7. **Explain the difference between a normal distribution and a skewed distribution.**
   _Normal: symmetric, mean = median = mode. Positive skew: long right tail, mean > median. Negative skew: long left tail, mean < median._

8. **What is A/B testing? Walk through how you would design one.**
   _Split users randomly into control (A) and treatment (B) groups. Define metric (conversion rate, etc.), set sample size based on desired power, run until significance. Analyze with a t-test or chi-squared test._

9. **What is Bayesian vs. frequentist statistics?**
   _Frequentist: probability as long-run frequency; parameters are fixed, data is random. Bayesian: probability as degree of belief; updates prior with data to get posterior. $P(\theta|D) \propto P(D|\theta) \cdot P(\theta)$._

10. **What is multicollinearity? How do you detect and handle it?**
    _When predictor variables are highly correlated. Detect with VIF (Variance Inflation Factor) or correlation matrix. Handle by removing one of the correlated features, PCA, or Ridge regression._

---

## pandas & Data Manipulation

11. **What is the difference between `loc` and `iloc`?**
    _`loc` uses label-based indexing (column names, index labels). `iloc` uses integer-based positional indexing._

12. **What is the difference between `merge` and `concat` in pandas?**
    _`merge` joins DataFrames on key columns (like SQL JOIN). `concat` stacks DataFrames vertically (rows) or horizontally (columns) by position._

13. **How would you handle missing values in a dataset?**
    _Options: drop rows/columns (`dropna`), fill with mean/median/mode (`fillna`), forward/backward fill, or impute with a model. Choice depends on amount missing and whether data is MAR/MCAR/MNAR._

14. **What is a groupby operation? How does it work internally?**
    _split-apply-combine: split data into groups, apply a function to each group, combine results. Internally builds a hash map of group keys._

15. **When would you use `apply` vs. vectorized pandas operations?**
    _Avoid `apply` when a vectorized equivalent exists — it's much slower because it loops in Python. Use vectorized: `.str`, arithmetic, `.where`, `.map`, etc. Use `apply` only for complex logic without a vectorized equivalent._

16. **Explain `pivot_table` vs `groupby`.**
    _`groupby` produces a Series/DataFrame with a multi-level index. `pivot_table` produces a 2D table with one variable as rows and another as columns — easier to read, like an Excel Pivot Table._

17. **How would you efficiently find duplicate rows?**
    ```python
    df[df.duplicated()]              # show duplicate rows
    df.drop_duplicates()             # remove them
    df.duplicated(subset=["email"])  # duplicate on specific cols
    ```

18. **What is the difference between `stack` and `melt`?**
    _`stack` moves column names into the row index (multi-level). `melt` converts wide format to long format, creating `variable` and `value` columns. `melt` is more user-friendly._

19. **How do you efficiently join a large dataset without running out of memory?**
    _Use chunked reading (`chunksize` in `read_csv`), merge on indexed columns, use Parquet format, or switch to Dask/Polars/Spark for data that doesn't fit in RAM._

20. **What are the different types of SQL joins and their pandas equivalents?**

    | SQL JOIN | pandas `how=` |
    |---|---|
    | INNER JOIN | `"inner"` |
    | LEFT JOIN | `"left"` |
    | RIGHT JOIN | `"right"` |
    | FULL OUTER JOIN | `"outer"` |

---

## Machine Learning Concepts

21. **What is the bias-variance tradeoff?**
    _Bias: error from wrong assumptions (underfitting). Variance: error from sensitivity to training data fluctuations (overfitting). As model complexity increases, bias decreases and variance increases. Goal: find the sweet spot._

22. **What is overfitting? How do you detect and prevent it?**
    _Model performs well on training data but poorly on new data. Detect: large gap between train and validation accuracy. Prevent: more data, regularization (L1/L2), dropout, early stopping, cross-validation._

23. **Explain regularization. What is the difference between L1 and L2?**
    _Regularization adds a penalty to the loss function to constrain model complexity._
    - _L1 (Lasso): penalty = $\lambda \sum |w_i|$. Drives some weights to zero — built-in feature selection._
    - _L2 (Ridge): penalty = $\lambda \sum w_i^2$. Shrinks all weights but rarely to zero._

24. **What is cross-validation? Why is it better than a single train/test split?**
    _k-fold CV: split data into k folds, train k models each leaving one fold out for validation, average scores. More reliable estimate of generalization performance; uses all data for both training and validation._

25. **What is precision vs. recall? When do you optimize for each?**
    $$\text{Precision} = \frac{TP}{TP + FP} \qquad \text{Recall} = \frac{TP}{TP + FN}$$
    _Optimize precision when false positives are costly (spam filter). Optimize recall when false negatives are costly (cancer detection)._

26. **What is the F1 score?**
    $$F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$
    _Harmonic mean of precision and recall. Useful when classes are imbalanced._

27. **What is the difference between classification and regression?**
    _Classification: predict a discrete label (spam/not spam, disease/no disease). Regression: predict a continuous numeric value (house price, temperature)._

28. **Explain how a decision tree works.**
    _Recursively splits data on the feature + threshold that maximizes information gain (or minimizes Gini impurity). At each node, pick the best split; stop when a stopping criterion is met (max depth, min samples)._

29. **What is the difference between a Random Forest and Gradient Boosting?**
    _Random Forest: trains many deep trees in parallel on bootstrap samples; averages predictions (bagging). Gradient Boosting (XGBoost, LightGBM): trains shallow trees sequentially, each correcting the previous tree's residuals (boosting)._

30. **What is the curse of dimensionality?**
    _As the number of features grows, data becomes increasingly sparse and distances become meaningless. Models need exponentially more data to generalize. Mitigate with feature selection, PCA, or other dimensionality reduction._

31. **Explain PCA (Principal Component Analysis).**
    _Finds orthogonal directions (principal components) of maximum variance in the data. Projects high-dimensional data into fewer dimensions. Components are linear combinations of original features, ordered by variance explained._

32. **What is gradient descent? How does the learning rate affect it?**
    _Iteratively move in the direction of steepest loss decrease: $w \leftarrow w - \alpha \nabla_w L$. Too high a learning rate: overshoots, diverges. Too low: converges slowly._

33. **What is a confusion matrix?**
    _2×2 table for binary classification showing: True Positive, False Positive, False Negative, True Negative. Foundation for precision, recall, F1, accuracy metrics._

34. **Explain k-means clustering. What are its limitations?**
    _Assigns each point to the nearest of k centroids, updates centroids to means of assigned points, repeats until convergence. Limitations: must specify k, sensitive to initialization, assumes spherical clusters, affected by outliers._

35. **What is the ROC curve and AUC?**
    _ROC (Receiver Operating Characteristic): plots True Positive Rate vs. False Positive Rate at every threshold. AUC (Area Under Curve): probability that model ranks a random positive higher than a random negative. AUC = 0.5 is random; AUC = 1.0 is perfect._

---

## Feature Engineering

36. **What is feature engineering? Give three examples.**
    _Creating new variables from raw data to improve model performance._
    - _Extracting month/weekday from a date column_
    - _Binning age into "young/middle/senior" categories_
    - _Computing interaction terms: `price_per_sqft = price / sqft`_

37. **How do you handle categorical features?**
    _Low cardinality: one-hot encoding (`pd.get_dummies`). High cardinality: target encoding, embedding, or frequency encoding to avoid dimensionality explosion._

38. **Why does feature scaling matter? Which algorithms require it?**
    _Scaling ensures no feature dominates due to different ranges. Required by: KNN, SVM, PCA, logistic regression, neural networks. Not required by: tree-based models (Random Forest, XGBoost)._

39. **What is target leakage? How do you prevent it?**
    _Including information in features that wouldn't be available at prediction time. Example: using `claim_status` to predict insurance fraud when the claim is already processed. Prevent by thinking through the timeline carefully and building features only from data available at prediction time._

---

## SQL for Data Science

40. **Write a query to find the top 3 salaries per department.**
    ```sql
    SELECT department, name, salary
    FROM (
        SELECT
            department,
            name,
            salary,
            RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
        FROM employees
    ) ranked
    WHERE rnk <= 3;
    ```

41. **What is the difference between RANK(), DENSE_RANK(), and ROW_NUMBER()?**
    - _`ROW_NUMBER()`: unique sequential number, no ties._
    - _`RANK()`: ties get the same rank, next rank skips (1, 2, 2, 4)._
    - _`DENSE_RANK()`: ties get same rank, no gap (1, 2, 2, 3)._

42. **How would you calculate month-over-month revenue growth in SQL?**
    ```sql
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) AS prev_revenue,
        (revenue - LAG(revenue) OVER (ORDER BY month))
            / LAG(revenue) OVER (ORDER BY month) * 100 AS pct_change
    FROM monthly_revenue;
    ```

43. **Explain CTEs and when to use them.**
    _Common Table Expressions define a named temporary result set within a query. Use them to break complex queries into readable steps, replace subqueries for clarity, or reference the same subquery multiple times._

44. **What is the difference between WHERE and HAVING?**
    _WHERE filters rows before grouping. HAVING filters groups after GROUP BY._

---

## Data Science Process

45. **What are the steps you follow when approaching a new data science problem?**
    1. Understand the business problem and define success metrics.
    2. Gather and load the data; understand its source and limitations.
    3. Exploratory Data Analysis (EDA): distributions, missing values, correlations.
    4. Feature engineering and preprocessing.
    5. Select and train models; tune hyperparameters.
    6. Evaluate on hold-out set; compare to baseline.
    7. Deploy and monitor for drift.

46. **How do you handle an imbalanced dataset?**
    _Resampling: oversample minority class (SMOTE), undersample majority class. Algorithm-level: use `class_weight="balanced"`, adjust decision threshold, use precision-recall curve instead of accuracy._

47. **What is data leakage? Give an example.**
    _When information from outside the training period/scope leaks into the model input. Example: normalizing features using the mean/std of the entire dataset (including test set) before splitting. Correct: fit scaler on train, transform train and test separately._

48. **How would you explain a model's predictions to a non-technical stakeholder?**
    _Use SHAP values to show feature contributions to individual predictions. Show simple charts: "model ranked salary and experience as the top drivers." Avoid jargon — translate confidence scores to plain risk tiers._

49. **What is the difference between supervised, unsupervised, and reinforcement learning?**
    - _Supervised: labeled training data, predict outputs from inputs (classification, regression)._
    - _Unsupervised: no labels, find hidden structure (clustering, dimensionality reduction)._
    - _Reinforcement: an agent takes actions and receives rewards; learns policy via trial and error._

50. **What metrics would you use to evaluate a recommendation system?**
    _Precision@K, Recall@K, NDCG (Normalized Discounted Cumulative Gain), MAP (Mean Average Precision). Online: click-through rate, session length, conversion rate._
