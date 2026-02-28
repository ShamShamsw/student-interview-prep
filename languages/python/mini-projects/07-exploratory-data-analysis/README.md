````markdown
# Mini-Project 07: Exploratory Data Analysis (EDA)

**Time:** 1.5–2.5 hours  
**Difficulty:** Beginner–Medium  
**Concepts:** pandas, statistics, matplotlib, seaborn, data cleaning, feature relationships

---

## Objective

Conduct a full Exploratory Data Analysis on a real-world-style dataset. EDA is the first step in any data science project and the most common coding exercise in data science interviews — you will describe the data, clean it, find patterns, and form hypotheses.

---

## Dataset

We use a fictional but realistic **HR Dataset** covering employee information. Generate it with the script below, or attach your own CSV.

```python
# generate_hr_data.py
import numpy as np
import pandas as pd

np.random.seed(0)
n = 500

departments = ["Engineering", "Marketing", "Sales", "HR", "Product", "Finance"]
education   = ["High School", "Bachelor's", "Master's", "PhD"]

data = {
    "employee_id":     range(1001, 1001 + n),
    "age":             np.random.randint(22, 62, n),
    "gender":          np.random.choice(["Male", "Female", "Non-binary"], n, p=[0.50, 0.45, 0.05]),
    "education":       np.random.choice(education, n, p=[0.10, 0.55, 0.28, 0.07]),
    "department":      np.random.choice(departments, n),
    "years_at_company":np.random.randint(0, 20, n),
    "hours_per_week":  np.round(np.clip(np.random.normal(42, 7, n), 20, 80), 1),
    "salary":          None,  # computed below
    "performance_score": np.random.choice([1, 2, 3, 4, 5], n, p=[0.05, 0.15, 0.40, 0.30, 0.10]),
    "satisfaction":    np.random.choice([1, 2, 3, 4, 5], n),
    "left_company":    np.random.choice([0, 1], n, p=[0.78, 0.22]),
}
df = pd.DataFrame(data)

# Salary based on education + years + noise
base = {"High School": 40000, "Bachelor's": 58000, "Master's": 75000, "PhD": 95000}
df["salary"] = (
    df["education"].map(base)
    + df["years_at_company"] * 1500
    + df["performance_score"] * 3000
    + np.random.normal(0, 8000, n)
).clip(30000, 180000).round(-2)

# Introduce some missing values (realistic)
df.loc[df.sample(20).index, "satisfaction"] = np.nan
df.loc[df.sample(10).index, "salary"]       = np.nan

df.to_csv("hr_data.csv", index=False)
print(f"Saved {n} rows.")
```

---

## EDA Checklist

A complete EDA covers these six stages. Work through them in order.

---

### Stage 1 — Load & First Look

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted")
df = pd.read_csv("hr_data.csv")

# TODO: Answer all of the following:
print(df.shape)          # How many employees? How many features?
print(df.dtypes)         # What are the data types?
print(df.head(10))       # Does the data look reasonable?
print(df.tail(5))        # Any oddities at the end?
print(df.describe())     # What are the ranges? Any obvious anomalies?
print(df.nunique())      # How many unique values per column?
```

**Guiding questions:**
- What does each row represent?
- What is the target variable you might want to predict?
- Are the column types correct (e.g., is `age` numeric)?

---

### Stage 2 — Missing Value Analysis

```python
# TODO: Produce a missing value summary
missing = df.isna().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_summary = pd.DataFrame({"count": missing, "pct": missing_pct})
print(missing_summary[missing_summary["count"] > 0])

# TODO: Visualize missingness with a heatmap
plt.figure(figsize=(12, 4))
sns.heatmap(df.isna(), cbar=False, yticklabels=False, cmap="viridis")
plt.title("Missing Value Map")
plt.show()

# TODO: Decide on a strategy for each missing column:
# - Drop if < 1% missing?
# - Fill numeric with median?
# - Fill categorical with mode?
# Document your choices as comments.
```

---

### Stage 3 — Univariate Analysis (one variable at a time)

#### Numeric columns

```python
numeric_cols = ["age", "years_at_company", "hours_per_week", "salary", "performance_score", "satisfaction"]

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
for ax, col in zip(axes.flat, numeric_cols):
    sns.histplot(df[col].dropna(), kde=True, ax=ax, bins=25)
    ax.set_title(col)
    ax.set_xlabel("")
plt.tight_layout()
plt.savefig("univariate_numeric.png", dpi=120)
plt.show()

# TODO: For each numeric column note:
# - Is it normally distributed, right-skewed, left-skewed, bimodal?
# - Are there outliers (values > 3 standard deviations from mean)?
```

#### Categorical columns

```python
cat_cols = ["gender", "education", "department"]

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, col in zip(axes, cat_cols):
    counts = df[col].value_counts()
    ax.bar(counts.index, counts.values)
    ax.set_title(f"Distribution of {col}")
    ax.tick_params(axis="x", rotation=30)
plt.tight_layout()
plt.show()

# TODO: What percentage of employees are in each department?
# (Hint: df["department"].value_counts(normalize=True) * 100)
```

---

### Stage 4 — Bivariate Analysis (pairs of variables)

```python
# TODO: Produce and interpret all of the following:

# 4a. Correlation matrix of numeric features
plt.figure(figsize=(9, 7))
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Correlation Matrix")
plt.show()

# 4b. Salary vs. years_at_company scatter
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="years_at_company", y="salary", hue="education", alpha=0.6)
plt.title("Salary vs. Years at Company by Education")
plt.show()

# 4c. Salary by department box plot
plt.figure(figsize=(10, 5))
order = df.groupby("department")["salary"].median().sort_values(ascending=False).index
sns.boxplot(data=df, x="department", y="salary", order=order)
plt.title("Salary Distribution by Department")
plt.xticks(rotation=30)
plt.show()

# 4d. Attrition (left_company) by department — stacked bar
attrition = df.groupby("department")["left_company"].mean() * 100
attrition.sort_values().plot.barh(title="Attrition Rate (%) by Department")
plt.xlabel("Attrition Rate (%)")
plt.show()

# 4e. Performance score vs. satisfaction — violin plot
sns.violinplot(data=df, x="performance_score", y="satisfaction")
plt.title("Satisfaction Distribution by Performance Score")
plt.show()
```

**Guiding questions after each chart:**
- Is there a clear trend?
- Does it match your intuition? If not, why might that be?
- Which variables seem most related to `left_company`?

---

### Stage 5 — Multivariate Analysis

```python
# TODO: Pair plot — shows all pairwise relationships at once
subset = df[["age", "salary", "years_at_company", "satisfaction", "left_company"]].dropna()
sns.pairplot(subset, hue="left_company", plot_kws={"alpha": 0.4})
plt.suptitle("Pair Plot: Employee Features by Attrition", y=1.02)
plt.show()

# TODO: GroupBy analysis — salary by department AND education level
pivot = df.groupby(["department", "education"])["salary"].mean().unstack()
plt.figure(figsize=(12, 6))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="Blues")
plt.title("Average Salary by Department × Education")
plt.show()

# TODO: Compare hours_per_week for employees who left vs. stayed
sns.histplot(data=df, x="hours_per_week", hue="left_company", kde=True, bins=30)
plt.title("Hours per Week: Stayed vs. Left")
plt.show()
```

---

### Stage 6 — Outlier Detection

```python
# TODO: Detect outliers using the IQR method for salary and hours_per_week

def flag_outliers(series: pd.Series) -> pd.Series:
    Q1, Q3 = series.quantile(0.25), series.quantile(0.75)
    IQR = Q3 - Q1
    return (series < Q1 - 1.5 * IQR) | (series > Q3 + 1.5 * IQR)

df["salary_outlier"]          = flag_outliers(df["salary"].dropna())
df["hours_per_week_outlier"]  = flag_outliers(df["hours_per_week"])

print(f"Salary outliers:    {df['salary_outlier'].sum()}")
print(f"Hours outliers:     {df['hours_per_week_outlier'].sum()}")

# Box plots for visual verification
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
df["salary"].plot.box(ax=ax1, title="Salary (with outliers marked)")
df["hours_per_week"].plot.box(ax=ax2, title="Hours per Week")
plt.tight_layout()
plt.show()
```

---

## Deliverable: EDA Summary Report

After completing all stages, write a short Markdown summary (`eda_summary.md`) answering:

1. **Dataset overview** — size, features, target variable.
2. **Data quality** — missing values, their impact, and handling strategy.
3. **Key distributions** — which features are skewed? Any surprising shapes?
4. **Top 3 correlations** with the target variable (`left_company`).
5. **Main findings** — two or three hypotheses you'd test next.
6. **Potential issues** — class imbalance? Outliers? Confounders?

---

## Expected Output Files

```
07-exploratory-data-analysis/
├── generate_hr_data.py
├── eda.py               (or eda.ipynb)
├── hr_data.csv          (generated)
├── univariate_numeric.png
├── eda_summary.md
└── (any other charts you saved)
```

---

## Stretch Goals

- Conduct a t-test to check if salary differs significantly between genders.
- Build a correlation heatmap using only employees who left the company.
- Fit a simple Logistic Regression to predict `left_company` using the features you identified as important.
- Use `pandas_profiling` / `ydata-profiling` to generate an automated HTML EDA report.
````
