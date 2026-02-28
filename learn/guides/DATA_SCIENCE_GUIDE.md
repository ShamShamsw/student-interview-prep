# Data Science Notes — Concepts, Formulas & Mental Models

> Concise reference notes on statistical foundations, machine learning theory, and the data science process. Designed for interview preparation and concept review.

---

## Table of Contents

1. [The Data Science Process](#the-data-science-process)
2. [Statistics Foundations](#statistics-foundations)
3. [Probability Fundamentals](#probability-fundamentals)
4. [Distributions Quick Reference](#distributions-quick-reference)
5. [Hypothesis Testing](#hypothesis-testing)
6. [Machine Learning Overview](#machine-learning-overview)
7. [Model Evaluation Metrics](#model-evaluation-metrics)
8. [Key Algorithms](#key-algorithms)
9. [Feature Engineering Techniques](#feature-engineering-techniques)
10. [Data Cleaning Workflow](#data-cleaning-workflow)
11. [Common Traps & Mistakes](#common-traps--mistakes)
12. [Recommended Libraries & Tools](#recommended-libraries--tools)

---

## The Data Science Process

```
Business Problem
      ↓
Data Collection & Ingestion
      ↓
Exploratory Data Analysis (EDA)
      ↓
Data Cleaning & Preprocessing
      ↓
Feature Engineering
      ↓
Model Selection & Training
      ↓
Model Evaluation & Tuning
      ↓
Interpretation & Communication
      ↓
Deployment & Monitoring
```

### At each stage, ask:
- **Business Problem:** What decision will this analysis support? How will success be measured?
- **Data:** Where did it come from? Is it representative? What's missing?
- **EDA:** What is the distribution of the target? Which features correlate with it?
- **Cleaning:** How will I handle missing values, outliers, duplicates?
- **Features:** Can domain knowledge create better predictors than raw columns?
- **Modeling:** Does my evaluation metric match the business goal?
- **Deployment:** How often will the model retrain? Who monitors for drift?

---

## Statistics Foundations

### Central Tendency

| Measure | Formula | When to use |
|---|---|---|
| Mean | $\bar{x} = \frac{1}{n}\sum x_i$ | Symmetric distributions, no extreme outliers |
| Median | Middle value when sorted | Skewed distributions, outliers present |
| Mode | Most frequent value | Categorical data, discrete counts |

### Spread

| Measure | Formula | Notes |
|---|---|---|
| Variance | $s^2 = \frac{\sum(x_i - \bar{x})^2}{n-1}$ | Squared units |
| Std Dev | $s = \sqrt{s^2}$ | Same units as data |
| IQR | $Q_3 - Q_1$ | Robust to outliers |
| Range | $\max - \min$ | Sensitive to outliers |

### Shape

- **Skewness > 0 (right skew):** Long right tail → mean > median (income, house prices)
- **Skewness < 0 (left skew):** Long left tail → mean < median (age at death)
- **Kurtosis:** Excess peakedness/fatness of tails. Normal = 0 (excess kurtosis).

### The Empirical Rule (Normal Distribution)

| Range | % of data |
|---|---|
| $\bar{x} \pm 1\sigma$ | ~68% |
| $\bar{x} \pm 2\sigma$ | ~95% |
| $\bar{x} \pm 3\sigma$ | ~99.7% |

---

## Probability Fundamentals

**Conditional probability:**
$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}$$

**Bayes' theorem:**
$$P(A \mid B) = \frac{P(B \mid A) \cdot P(A)}{P(B)}$$

**Independence:** $P(A \cap B) = P(A) \cdot P(B)$ — knowing B tells you nothing about A.

**Expected value:** $E[X] = \sum x_i \cdot P(x_i)$

**Law of Large Numbers:** As sample size grows, the sample mean converges to the population mean.

**Central Limit Theorem:** For large enough $n$, the distribution of sample means is approximately normal:
$$\bar{X} \sim N\!\left(\mu,\, \frac{\sigma^2}{n}\right)$$

---

## Distributions Quick Reference

| Distribution | Use Case | Key Parameters |
|---|---|---|
| Normal / Gaussian | Heights, errors, many natural phenomena | $\mu$, $\sigma$ |
| Bernoulli | Single binary trial (coin flip) | $p$ |
| Binomial | # successes in n binary trials | $n$, $p$ |
| Poisson | # events in a fixed interval (rare events) | $\lambda$ (rate) |
| Exponential | Time between Poisson events | $\lambda$ |
| Uniform | Random number in [a, b] | $a$, $b$ |
| Log-Normal | Data that is normal after log transform (salaries, stock prices) | $\mu$, $\sigma$ of log |

---

## Hypothesis Testing

### Procedure

1. State $H_0$ (null) and $H_a$ (alternative).
2. Choose significance level $\alpha$ (usually 0.05).
3. Collect data and compute test statistic.
4. Calculate p-value (probability of data this extreme given $H_0$ is true).
5. If $p < \alpha$: reject $H_0$. Otherwise: fail to reject.

### Common Tests

| Situation | Test |
|---|---|
| Compare means of 2 groups | Independent t-test |
| Compare means of paired samples | Paired t-test |
| Compare means of 3+ groups | ANOVA |
| Compare proportions (2 groups) | Chi-squared test |
| Test correlation | Pearson / Spearman correlation |
| Non-parametric mean comparison | Mann-Whitney U |

### Confidence Intervals

A 95% CI means: if we repeated the experiment 100 times, approximately 95 of those intervals would contain the true parameter.

$$\text{CI} = \bar{x} \pm z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}$$

### Error Types

| | $H_0$ True | $H_0$ False |
|---|---|---|
| Reject $H_0$ | **Type I Error** ($\alpha$) | Correct (Power) |
| Fail to reject | Correct | **Type II Error** ($\beta$) |

- **Power** = $1 - \beta$ = probability of detecting a real effect.
- Increase power by: larger sample size, larger effect size, higher $\alpha$.

---

## Machine Learning Overview

### Problem Types

| Problem | Output | Examples |
|---|---|---|
| Binary Classification | 0 or 1 | Spam detection, churn prediction |
| Multi-class Classification | One of K classes | Digit recognition, disease diagnosis |
| Regression | Continuous number | House price, temperature |
| Clustering | Group labels | Customer segments, topic modeling |
| Dimensionality Reduction | Lower-dim representation | PCA, UMAP, t-SNE |

### The Bias-Variance Tradeoff

$$\text{Total Error} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Noise}$$

- **High bias:** Underfitting — model too simple, misses patterns.
- **High variance:** Overfitting — model too complex, memorizes noise.
- **Goal:** Minimize total error on unseen data.

### Regularization

| Method | Penalty | Effect |
|---|---|---|
| L1 (Lasso) | $\lambda \sum |w_i|$ | Sparse weights; built-in feature selection |
| L2 (Ridge) | $\lambda \sum w_i^2$ | Shrinks all weights; handles multicollinearity |
| Elastic Net | Mix of L1 and L2 | Best of both |

### Gradient Descent

$$w \leftarrow w - \alpha \frac{\partial L}{\partial w}$$

- $\alpha$ = learning rate  
- **Batch GD:** uses all data per step — stable but slow.
- **SGD:** uses one sample per step — noisy but fast.
- **Mini-batch GD:** uses a batch (32–256) — best of both worlds.

---

## Model Evaluation Metrics

### Classification

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$

$$\text{Precision} = \frac{TP}{TP + FP} \qquad \text{Recall} = \frac{TP}{TP + FN}$$

$$F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

- **AUC-ROC:** Area under the ROC curve. 0.5 = random, 1.0 = perfect.
- **Log Loss:** Penalizes confident wrong predictions. Lower is better.

**When to use which metric:**
- Balanced classes + equal costs → Accuracy
- Imbalanced classes → F1 or AUC
- Cost of FP ≠ cost of FN → Tune threshold on the ROC or Precision-Recall curve

### Regression

$$\text{MAE} = \frac{1}{n}\sum|y_i - \hat{y}_i| \qquad \text{MSE} = \frac{1}{n}\sum(y_i - \hat{y}_i)^2$$

$$\text{RMSE} = \sqrt{\text{MSE}} \qquad R^2 = 1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2}$$

- **RMSE** is in the same units as the target; more sensitive to outliers than MAE.
- **R²** = fraction of variance explained by the model. 1.0 = perfect, 0 = just predict the mean.
- **MAPE** = Mean Absolute Percentage Error — useful when comparing across scales.

---

## Key Algorithms

### Linear Regression
- **Assumption:** Linear relationship between features and target.
- **Loss:** MSE
- **Output:** Continuous prediction.
- **Pros:** Interpretable, fast.
- **Cons:** Sensitive to outliers, assumes linearity and normal residuals.

### Logistic Regression
- Uses sigmoid function to map output to [0, 1] probability.
- **Loss:** Log loss (binary cross-entropy)
- **Pros:** Probabilistic output, fast, interpretable coefficients.
- **Cons:** Cannot learn non-linear boundaries without feature engineering.

### Decision Tree
- Recursively splits on the feature + threshold that maximally reduces impurity (Gini or Entropy).
- **Pros:** Interpretable, handles non-linearity, no scaling needed.
- **Cons:** Overfits easily; unstable (small data changes → very different tree).

### Random Forest
- Ensemble of many decision trees trained on bootstrap samples with random feature subsets.
- Final prediction = majority vote (classification) or average (regression).
- **Pros:** Reduces variance, handles non-linearity, gives feature importances, robust to outliers.
- **Cons:** Less interpretable than a single tree, slow to predict on large forests.

### Gradient Boosting (XGBoost, LightGBM, CatBoost)
- Trains trees sequentially, each fitting the residuals of the previous model.
- **Pros:** Often best in-class on tabular data, handles mixed types, fast with LightGBM.
- **Cons:** Many hyperparameters, can overfit, slower to train than Random Forest.

### K-Nearest Neighbors (KNN)
- Predict by majority vote (or average) of the k nearest training points.
- **Pros:** No training required (lazy learner), simple.
- **Cons:** Slow at prediction on large datasets, sensitive to feature scaling and irrelevant features.

### K-Means Clustering
- Iteratively assign points to the nearest of k centroids, update centroids to cluster means.
- **Choose k:** Elbow method (plot inertia vs. k), silhouette score.
- **Limitations:** Assumes spherical clusters, sensitive to initialization and outliers, must specify k.

### Principal Component Analysis (PCA)
- Projects data onto directions of maximum variance.
- **Use when:** Many correlated features; want to visualize high-dim data; reduce dimensionality before modeling.
- Explained variance ratio tells you how much information each component captures.

---

## Feature Engineering Techniques

| Technique | When to use | Example |
|---|---|---|
| Log transform | Right-skewed numeric | `log(salary)` to normalize distribution |
| Binning / Bucketization | Convert continuous to ordinal | Age → "18-25", "26-35",... |
| One-hot encoding | Low-cardinality categoricals | `department` → boolean columns |
| Target encoding | High-cardinality categoricals | Replace category with mean target value |
| Interaction features | When features multiply effects | `salary * years = career_value` |
| Date decomposition | Date/time columns | Extract year, month, day-of-week, quarter |
| Lag/Lead features | Time series | Previous month's value |
| Rolling statistics | Time series | 7-day rolling mean |
| Polynomial features | Non-linear relationships | $x^2$, $x_1 \cdot x_2$ |
| Normalization/Scaling | Algorithms sensitive to scale | StandardScaler, MinMaxScaler |

---

## Data Cleaning Workflow

```
1. Load data
2. Inspect (shape, dtypes, head, describe)
3. Missing values
   a. Count per column
   b. Assess pattern (MCAR / MAR / MNAR)
   c. Strategy: drop / fill / model
4. Duplicates
   a. Exact duplicates → drop
   b. Near-duplicates → investigate
5. Outliers
   a. Detect: IQR, Z-score, box plots
   b. Strategy: remove, cap (winsorize), keep (document)
6. Type corrections
   a. Parse dates, convert codes to categories, fix string/numeric mix
7. Consistency
   a. Standardize casing, spelling variations, unit mismatches
8. Validation
   a. Assert business rules hold (no negative quantities, date makes sense)
```

### Missing Data Mechanisms

| Mechanism | Description | Appropriate Response |
|---|---|---|
| MCAR (Missing Completely At Random) | Missingness unrelated to any variable | Any imputation method; drop if < 5% |
| MAR (Missing At Random) | Missingness related to observed variables | Model-based imputation |
| MNAR (Missing Not At Random) | Missingness related to the missing value itself | Rethink data collection; use domain knowledge |

---

## Common Traps & Mistakes

### 1. Data Leakage
**Mistake:** Using future or target-related information as a feature.  
**Fix:** Build features only from data available at prediction time. Fit all preprocessing (scalers, encoders) on train only.

### 2. Evaluating on Training Data
**Mistake:** Reporting training accuracy as model performance.  
**Fix:** Always evaluate on a held-out test set (or use cross-validation).

### 3. Ignoring Class Imbalance
**Mistake:** 95% accuracy on a dataset where 95% of instances are negative ≠ good model.  
**Fix:** Use F1, AUC, or PR-AUC. Consider resampling (SMOTE) or `class_weight="balanced"`.

### 4. p-Hacking
**Mistake:** Running many hypothesis tests and only reporting the significant ones.  
**Fix:** Pre-register your analysis plan. Apply Bonferroni correction when testing multiple hypotheses: $\alpha' = \alpha / m$.

### 5. Correlation ≠ Causation
**Mistake:** Building a "causal" story from correlational data.  
**Fix:** Use careful language. Establish causation only with randomized experiments (A/B tests) or valid causal inference methods (DiD, IV, RD).

### 6. Wrong Evaluation Metric
**Mistake:** Using RMSE for a business problem that cares about direction (went up/down), or accuracy for an imbalanced problem.  
**Fix:** Define the metric that matches the actual business cost before modeling.

### 7. Forgetting to Reset Index after Filter/Groupby
```python
# Bad — index is discontinuous after filtering
df_filtered = df[df["region"] == "West"]

# Safe — reset so iloc still works intuitively
df_filtered = df[df["region"] == "West"].reset_index(drop=True)
```

### 8. Applying the Scaler to the Whole Dataset Before Splitting
```python
# BAD — scaler learns from the test set (data leakage)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test = train_test_split(X_scaled)

# CORRECT
X_train, X_test = train_test_split(X)
X_train_s = scaler.fit_transform(X_train)   # fit on train only
X_test_s  = scaler.transform(X_test)        # apply transformation to test
```

---

## Recommended Libraries & Tools

| Library | Purpose | Install |
|---|---|---|
| `pandas` | Data manipulation | `pip install pandas` |
| `numpy` | Numerical operations | `pip install numpy` |
| `matplotlib` | Plotting (low-level) | `pip install matplotlib` |
| `seaborn` | Statistical charts (high-level) | `pip install seaborn` |
| `scikit-learn` | Classical ML algorithms | `pip install scikit-learn` |
| `xgboost` | Gradient boosting | `pip install xgboost` |
| `lightgbm` | Fast gradient boosting | `pip install lightgbm` |
| `statsmodels` | Statistical tests, OLS with p-values | `pip install statsmodels` |
| `scipy` | Scientific computing, distributions | `pip install scipy` |
| `shap` | Model explainability | `pip install shap` |
| `imbalanced-learn` | SMOTE, resampling | `pip install imbalanced-learn` |
| `plotly` | Interactive charts | `pip install plotly` |
| `streamlit` | ML web dashboards | `pip install streamlit` |
| `ydata-profiling` | Automated EDA reports | `pip install ydata-profiling` |
| `openpyxl` | Read/write Excel files | `pip install openpyxl` |
| `polars` | Fast alternative to pandas | `pip install polars` |
