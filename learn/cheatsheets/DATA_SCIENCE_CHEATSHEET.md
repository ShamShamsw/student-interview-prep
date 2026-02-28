# Data Science Cheatsheet — Python (pandas / NumPy / Matplotlib)

> Quick-reference for pandas, NumPy, Matplotlib, and scikit-learn — with Excel equivalents wherever applicable.

---

## Table of Contents

1. [Setup & Imports](#setup--imports)
2. [Loading Data — Excel vs pandas](#loading-data--excel-vs-pandas)
3. [Viewing & Inspecting Data](#viewing--inspecting-data)
4. [Column & Row Selection](#column--row-selection)
5. [Filtering Rows](#filtering-rows)
6. [Sorting](#sorting)
7. [Adding & Modifying Columns](#adding--modifying-columns)
8. [Aggregation & GroupBy](#aggregation--groupby)
9. [Pivot Tables](#pivot-tables)
10. [VLOOKUP / Merge / Join](#vlookup--merge--join)
11. [Handling Missing Data](#handling-missing-data)
12. [String Operations](#string-operations)
13. [Date & Time](#date--time)
14. [Reshaping Data](#reshaping-data)
15. [NumPy Essentials](#numpy-essentials)
16. [Matplotlib & Seaborn — Charting](#matplotlib--seaborn--charting)
17. [Descriptive Statistics](#descriptive-statistics)
18. [scikit-learn Quick Reference](#scikit-learn-quick-reference)
19. [Common Interview Patterns](#common-interview-patterns)
20. [Complexity & Performance Notes](#complexity--performance-notes)

---

## Setup & Imports

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
```

---

## Loading Data — Excel vs pandas

| Excel Action | pandas Equivalent |
|---|---|
| Open .xlsx file | `pd.read_excel("file.xlsx")` |
| Open .csv file | `pd.read_csv("file.csv")` |
| Open specific sheet | `pd.read_excel("file.xlsx", sheet_name="Sheet2")` |
| Save as .xlsx | `df.to_excel("output.xlsx", index=False)` |
| Save as .csv | `df.to_csv("output.csv", index=False)` |

```python
# Read CSV with options
df = pd.read_csv(
    "sales.csv",
    parse_dates=["date"],      # auto-parse date columns
    dtype={"zip_code": str},   # force column types
    na_values=["N/A", "--"],   # treat these as NaN
    skiprows=2,                # skip header junk
    nrows=1000,                # only load first 1000 rows
)

# Read multiple sheets at once → dict of DataFrames
sheets = pd.read_excel("report.xlsx", sheet_name=None)
df_jan = sheets["January"]
df_feb = sheets["February"]
```

---

## Viewing & Inspecting Data

| Excel Action | pandas Equivalent |
|---|---|
| Scroll to see data | `df.head(10)` / `df.tail(5)` |
| Row & column count | `df.shape` |
| Column names | `df.columns.tolist()` |
| Data types per col | `df.dtypes` |
| Summary statistics | `df.describe()` |
| Count non-nulls | `df.info()` |

```python
df.head()           # first 5 rows
df.tail()           # last 5 rows
df.sample(5)        # 5 random rows
df.shape            # (rows, cols)
df.columns          # Index of column names
df.dtypes           # dtype per column
df.info()           # non-null counts + dtypes
df.describe()       # count, mean, std, min/max, quartiles
df.describe(include="all")  # include non-numeric cols
df.nunique()        # unique value count per column
df.value_counts()   # frequency table (Series)
```

---

## Column & Row Selection

| Excel Action | pandas Equivalent |
|---|---|
| Select column B | `df["name"]` or `df.name` |
| Select columns B:D | `df[["name","age","city"]]` |
| Select row 3 | `df.iloc[2]` |
| Select rows 1–5 | `df.iloc[0:5]` |
| Cell at row 3, col B | `df.iloc[2, 1]` or `df.at[2, "name"]` |

```python
# Single column → Series
df["salary"]

# Multiple columns → DataFrame
df[["name", "salary", "department"]]

# Row by label index
df.loc[5]              # row where index == 5
df.loc[5, "salary"]    # specific cell

# Row by integer position
df.iloc[0]             # first row
df.iloc[-1]            # last row
df.iloc[0:3, 1:4]      # slice rows 0-2, cols 1-3

# Rename columns
df = df.rename(columns={"Sal": "salary", "Dept": "department"})

# Drop columns
df = df.drop(columns=["unnecessary_col", "temp"])
```

---

## Filtering Rows

| Excel Action | pandas Equivalent |
|---|---|
| Filter by value | `df[df["age"] > 30]` |
| Filter multiple conditions | `df[(df["age"] > 30) & (df["dept"] == "Sales")]` |
| Filter by list | `df[df["city"].isin(["NYC", "LA"])]` |
| Exclude values | `df[~df["city"].isin(["NYC", "LA"])]` |
| Text contains | `df[df["name"].str.contains("Smith")]` |

```python
# Single condition
df[df["salary"] >= 75000]

# AND condition (use & not 'and')
df[(df["salary"] >= 75000) & (df["department"] == "Engineering")]

# OR condition (use | not 'or')
df[(df["salary"] < 40000) | (df["salary"] > 120000)]

# isin — like FILTER with a list
df[df["region"].isin(["West", "South"])]

# NOT isin
df[~df["region"].isin(["West", "South"])]

# query() — more readable for complex filters
df.query("salary >= 75000 and department == 'Engineering'")

# Filter nulls
df[df["email"].isna()]         # rows where email is missing
df[df["email"].notna()]        # rows where email is present
```

---

## Sorting

| Excel Action | pandas Equivalent |
|---|---|
| Sort A→Z by col | `df.sort_values("name")` |
| Sort Z→A by col | `df.sort_values("salary", ascending=False)` |
| Sort by multiple cols | `df.sort_values(["dept", "salary"], ascending=[True, False])` |

```python
df.sort_values("salary")                                   # ascending
df.sort_values("salary", ascending=False)                  # descending
df.sort_values(["dept", "salary"], ascending=[True, False])# multi-col
df.sort_values("date", na_position="last")                 # NaNs at end
df.sort_index()                                            # sort by index
```

---

## Adding & Modifying Columns

| Excel Action | pandas Equivalent |
|---|---|
| New formula column | `df["bonus"] = df["salary"] * 0.10` |
| IF formula | `df["level"] = np.where(df["salary"] > 80000, "Senior", "Junior")` |
| IFS / nested IF | `pd.cut()` or `np.select()` |

```python
# Simple calculation
df["annual_bonus"] = df["salary"] * 0.10

# Conditional column — Excel IF()
df["level"] = np.where(df["salary"] > 80000, "Senior", "Junior")

# Multi-condition — Excel IFS()
conditions = [
    df["salary"] >= 120000,
    df["salary"] >= 80000,
    df["salary"] >= 50000,
]
choices = ["Principal", "Senior", "Mid"]
df["level"] = np.select(conditions, choices, default="Junior")

# Excel ROUND()
df["salary_rounded"] = df["salary"].round(-3)   # round to nearest 1000

# Apply a custom function
def categorize(val):
    if val > 100:
        return "high"
    elif val > 50:
        return "medium"
    return "low"

df["category"] = df["score"].apply(categorize)

# Vectorized string concat
df["full_name"] = df["first_name"] + " " + df["last_name"]
```

---

## Aggregation & GroupBy

| Excel Action | pandas Equivalent |
|---|---|
| SUM of column | `df["sales"].sum()` |
| AVERAGE of column | `df["sales"].mean()` |
| COUNT rows | `len(df)` or `df.shape[0]` |
| COUNTIF | `(df["dept"] == "Sales").sum()` |
| SUMIF | `df.loc[df["dept"] == "Sales", "revenue"].sum()` |
| AVERAGEIF | `df.loc[df["dept"] == "Sales", "revenue"].mean()` |
| Group & aggregate | `df.groupby("dept")["revenue"].sum()` |

```python
# Basic aggregation
df["revenue"].sum()
df["revenue"].mean()
df["revenue"].median()
df["revenue"].std()
df["revenue"].min()
df["revenue"].max()

# GroupBy — like Excel SUMIF/AVERAGEIF/COUNTIF
df.groupby("department")["salary"].mean()
df.groupby("department")["salary"].sum()
df.groupby("department")["employee_id"].count()

# Multiple aggregations at once
df.groupby("department").agg(
    avg_salary=("salary", "mean"),
    total_headcount=("employee_id", "count"),
    max_salary=("salary", "max"),
    min_salary=("salary", "min"),
)

# GroupBy multiple columns
df.groupby(["department", "region"])["revenue"].sum().reset_index()

# Value counts — like COUNTIF for all values
df["department"].value_counts()
df["department"].value_counts(normalize=True)  # as percentages
```

---

## Pivot Tables

| Excel Action | pandas Equivalent |
|---|---|
| Insert Pivot Table | `pd.pivot_table(df, ...)` |
| Pivot (wide format) | `df.pivot(index, columns, values)` |

```python
# Excel-style Pivot Table
pivot = pd.pivot_table(
    df,
    values="revenue",           # what to aggregate
    index="region",             # rows
    columns="quarter",          # columns
    aggfunc="sum",              # SUM, mean, count, etc.
    fill_value=0,               # replace NaN with 0
    margins=True,               # add Grand Total row/col
    margins_name="Grand Total",
)

# Pivot (simple reshape — no aggregation, needs unique index)
wide = df.pivot(index="date", columns="product", values="sales")

# Cross-tabulation — count occurrences
pd.crosstab(df["department"], df["region"])
pd.crosstab(df["department"], df["region"], normalize="index")  # row %
```

---

## VLOOKUP / Merge / Join

| Excel Action | pandas Equivalent |
|---|---|
| VLOOKUP | `df.merge(lookup_df, on="key", how="left")` |
| XLOOKUP | `df.merge(lookup_df, on="key", how="left")` |
| Inner join | `df.merge(other, on="id", how="inner")` |
| Left join | `df.merge(other, on="id", how="left")` |
| Right join | `df.merge(other, on="id", how="right")` |
| Full outer join | `df.merge(other, on="id", how="outer")` |
| Stack rows vertically | `pd.concat([df1, df2])` |

```python
# VLOOKUP equivalent — left join on key
employees = pd.DataFrame({
    "emp_id": [1, 2, 3],
    "name": ["Alice", "Bob", "Carol"],
})
departments = pd.DataFrame({
    "emp_id": [1, 2, 4],
    "department": ["Eng", "Marketing", "Sales"],
})

result = employees.merge(departments, on="emp_id", how="left")
#   emp_id   name department
#        1  Alice        Eng
#        2    Bob  Marketing
#        3  Carol        NaN

# Merge on different column names
df.merge(lookup, left_on="dept_code", right_on="code")

# Merge on multiple keys
df.merge(other, on=["company_id", "year"])

# Stack DataFrames vertically — like copy-paste rows
combined = pd.concat([df_q1, df_q2, df_q3, df_q4], ignore_index=True)
```

---

## Handling Missing Data

```python
# Detect missing values
df.isna()               # boolean mask
df.isna().sum()         # count per column
df.isna().sum() / len(df)  # proportion missing

# Drop rows/columns with missing values
df.dropna()                          # drop any row with NaN
df.dropna(subset=["salary"])         # drop only if salary is NaN
df.dropna(axis=1, thresh=0.9*len(df))# drop cols >10% missing

# Fill missing values
df["salary"].fillna(df["salary"].median())
df["name"].fillna("Unknown")
df.fillna(method="ffill")    # forward fill (carry previous value)
df.fillna(method="bfill")    # backward fill

# Fill per column with a dict
df.fillna({"salary": 0, "email": "noemail@example.com"})

# Replace specific values
df.replace({"N/A": np.nan, "?": np.nan})
df["status"].replace({"Y": True, "N": False})
```

---

## String Operations

| Excel Action | pandas Equivalent |
|---|---|
| UPPER / LOWER | `df["name"].str.upper()` / `.str.lower()` |
| LEFT(x, n) | `df["name"].str[:n]` |
| RIGHT(x, n) | `df["name"].str[-n:]` |
| LEN | `df["name"].str.len()` |
| TRIM | `df["name"].str.strip()` |
| FIND / SEARCH | `df["name"].str.find("Smith")` |
| SUBSTITUTE | `df["name"].str.replace("Corp", "Inc")` |
| CONCATENATE | `df["first"] + " " + df["last"]` |
| Text to Columns | `df["name"].str.split(",", expand=True)` |

```python
df["name"].str.upper()
df["name"].str.lower()
df["name"].str.title()
df["name"].str.strip()          # remove leading/trailing whitespace
df["name"].str.len()
df["name"].str[:5]              # first 5 chars
df["name"].str[-4:]             # last 4 chars
df["name"].str.contains("Inc")  # boolean mask
df["name"].str.startswith("A")
df["name"].str.endswith("LLC")
df["name"].str.replace("Corp", "Inc", regex=False)
df["name"].str.split(",", expand=True)   # split into cols
df["email"].str.extract(r"@(.+)\.")      # regex extract domain
```

---

## Date & Time

| Excel Action | pandas Equivalent |
|---|---|
| TODAY() | `pd.Timestamp.today()` |
| YEAR(date) | `df["date"].dt.year` |
| MONTH(date) | `df["date"].dt.month` |
| DAY(date) | `df["date"].dt.day` |
| DATEDIF | `(df["end"] - df["start"]).dt.days` |
| WEEKDAY | `df["date"].dt.day_name()` |

```python
# Parse dates when loading
df["date"] = pd.to_datetime(df["date"])

# Extract components
df["year"]    = df["date"].dt.year
df["month"]   = df["date"].dt.month
df["day"]     = df["date"].dt.day
df["weekday"] = df["date"].dt.day_name()   # "Monday", "Tuesday", ...
df["quarter"] = df["date"].dt.quarter

# Date arithmetic
df["tenure_days"] = (pd.Timestamp.today() - df["hire_date"]).dt.days
df["tenure_years"] = df["tenure_days"] / 365.25

# Date ranges
pd.date_range("2024-01-01", "2024-12-31", freq="MS")  # monthly start
pd.date_range("2024-01-01", periods=52, freq="W")      # 52 weeks

# Resample time series (group by time period)
df.set_index("date").resample("M")["revenue"].sum()    # monthly totals
df.set_index("date").resample("Q")["revenue"].mean()   # quarterly avg
```

---

## Reshaping Data

```python
# Wide → Long (like Excel "Unpivot Columns" in Power Query)
long = df.melt(
    id_vars=["name", "department"],       # keep these cols
    value_vars=["Q1", "Q2", "Q3", "Q4"], # melt these
    var_name="quarter",
    value_name="revenue",
)

# Long → Wide (reverse of melt)
wide = long.pivot_table(
    index=["name", "department"],
    columns="quarter",
    values="revenue",
).reset_index()

# Stack / Unstack (multi-level index manipulation)
df.stack()    # moves column level to row index
df.unstack()  # moves row index level to column
```

---

## NumPy Essentials

```python
# Array creation
arr = np.array([1, 2, 3, 4, 5])
zeros = np.zeros((3, 4))           # 3×4 matrix of zeros
ones = np.ones((2, 3))             # 2×3 matrix of ones
eye = np.eye(3)                    # 3×3 identity matrix
rng = np.arange(0, 10, 2)         # [0, 2, 4, 6, 8]
linspace = np.linspace(0, 1, 5)   # [0.0, 0.25, 0.5, 0.75, 1.0]

# Random numbers
np.random.seed(42)                 # reproducibility
np.random.rand(3, 4)               # uniform [0, 1)
np.random.randn(3, 4)              # standard normal
np.random.randint(0, 100, (3, 4)) # random integers

# Math operations (vectorized — much faster than Python loops)
arr * 2
arr ** 2
np.sqrt(arr)
np.log(arr)
np.exp(arr)

# Aggregations
arr.sum()
arr.mean()
arr.std()
arr.min()
arr.max()
arr.argmin()   # index of minimum
arr.argmax()   # index of maximum

# Shape manipulation
arr.reshape(2, 5)
arr.flatten()
np.transpose(matrix)   # or matrix.T

# Boolean indexing (same as pandas)
arr[arr > 3]           # [4, 5]
np.where(arr > 3, arr, 0)  # conditional replace

# Linear algebra
np.dot(A, B)           # matrix multiplication
np.linalg.inv(A)       # matrix inverse
np.linalg.det(A)       # determinant
eigenvalues, eigenvectors = np.linalg.eig(A)
```

---

## Matplotlib & Seaborn — Charting

| Excel Chart Type | Matplotlib / Seaborn Equivalent |
|---|---|
| Bar chart | `df["col"].plot.bar()` / `sns.barplot()` |
| Line chart | `df.plot.line()` / `sns.lineplot()` |
| Scatter chart | `df.plot.scatter(x, y)` / `sns.scatterplot()` |
| Histogram | `df["col"].plot.hist()` / `sns.histplot()` |
| Box chart | `df.plot.box()` / `sns.boxplot()` |
| Heatmap | `sns.heatmap(df.corr())` |

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Line chart
axes[0, 0].plot(df["date"], df["revenue"], color="steelblue", linewidth=2)
axes[0, 0].set_title("Revenue Over Time")
axes[0, 0].set_xlabel("Date")
axes[0, 0].set_ylabel("Revenue ($)")

# Bar chart
dept_revenue = df.groupby("department")["revenue"].sum()
axes[0, 1].bar(dept_revenue.index, dept_revenue.values, color="salmon")
axes[0, 1].set_title("Revenue by Department")
axes[0, 1].tick_params(axis="x", rotation=45)

# Scatter plot
axes[1, 0].scatter(df["experience_years"], df["salary"], alpha=0.5)
axes[1, 0].set_title("Salary vs Experience")

# Histogram
axes[1, 1].hist(df["salary"], bins=20, edgecolor="black")
axes[1, 1].set_title("Salary Distribution")

plt.tight_layout()
plt.savefig("report.png", dpi=150, bbox_inches="tight")
plt.show()

# ── Seaborn (higher-level, better defaults) ──────────────────
sns.set_theme(style="whitegrid")

# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(numeric_only=True), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Matrix")

# Distribution with KDE
sns.histplot(df["salary"], kde=True, bins=30)

# Box plot (shows outliers)
sns.boxplot(data=df, x="department", y="salary")

# Pair plot (scatter matrix — all numeric pairs)
sns.pairplot(df[["salary", "experience_years", "age", "score"]])
```

---

## Descriptive Statistics

```python
# Summary statistics
df.describe()                                  # numeric only
df.describe(include="object")                  # string/categorical

# Individual statistics
df["salary"].mean()
df["salary"].median()
df["salary"].mode()[0]                         # mode (most frequent)
df["salary"].std()                             # standard deviation
df["salary"].var()                             # variance
df["salary"].skew()                            # skewness
df["salary"].kurt()                            # kurtosis
df["salary"].quantile([0.25, 0.5, 0.75])      # quartiles

# Correlation
df.corr(numeric_only=True)                     # correlation matrix
df["salary"].corr(df["experience_years"])      # single pair

# Outlier detection via IQR
Q1 = df["salary"].quantile(0.25)
Q3 = df["salary"].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df["salary"] < Q1 - 1.5*IQR) | (df["salary"] > Q3 + 1.5*IQR)]
```

---

## scikit-learn Quick Reference

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report,
    mean_squared_error, r2_score,
)

# ── Preprocessing ────────────────────────────────────────────
# Encode categorical columns
le = LabelEncoder()
df["dept_encoded"] = le.fit_transform(df["department"])

# One-hot encode (like Excel "convert to boolean columns")
dummies = pd.get_dummies(df["department"], prefix="dept", drop_first=True)
df = pd.concat([df, dummies], axis=1)

# Scale numeric features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

# ── Train / Test Split ───────────────────────────────────────
X = df[["experience_years", "education_level", "age"]]
y = df["salary"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Linear Regression ────────────────────────────────────────
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(f"R²:   {r2_score(y_test, y_pred):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
print("Coefficients:", dict(zip(X.columns, model.coef_)))

# ── Classification ───────────────────────────────────────────
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

# Feature importance
importance = pd.Series(clf.feature_importances_, index=X.columns)
importance.sort_values().plot.barh(title="Feature Importance")

# ── Cross Validation ─────────────────────────────────────────
scores = cross_val_score(clf, X, y, cv=5, scoring="accuracy")
print(f"CV Accuracy: {scores.mean():.4f} ± {scores.std():.4f}")
```

---

## Common Interview Patterns

### 1. Find top N per group (Excel: LARGE + FILTER)
```python
# Top 3 earners per department
df.groupby("department").apply(
    lambda g: g.nlargest(3, "salary")
).reset_index(drop=True)
```

### 2. Running total (Excel: cumulative SUM)
```python
df["cumulative_revenue"] = df["revenue"].cumsum()
df["rolling_7day_avg"]   = df["revenue"].rolling(window=7).mean()
```

### 3. Percentage of total
```python
df["pct_of_total"] = df["revenue"] / df["revenue"].sum() * 100
# Within each group (Excel: SUMIF / total)
df["pct_in_dept"] = df.groupby("department")["revenue"].transform(
    lambda x: x / x.sum() * 100
)
```

### 4. Rank within group (Excel: RANK)
```python
df["rank_overall"] = df["salary"].rank(ascending=False)
df["rank_in_dept"] = df.groupby("department")["salary"].rank(
    ascending=False, method="dense"
)
```

### 5. Lag / Lead (Excel: offset reference)
```python
df["prev_month_revenue"] = df["revenue"].shift(1)   # lag 1
df["next_month_revenue"] = df["revenue"].shift(-1)  # lead 1
df["mom_change"]         = df["revenue"].diff()     # month-over-month
df["mom_pct_change"]     = df["revenue"].pct_change() * 100
```

### 6. Conditional aggregation (Excel: SUMIFS)
```python
# Total revenue for Engineering dept in Q1
mask = (df["department"] == "Engineering") & (df["quarter"] == "Q1")
df.loc[mask, "revenue"].sum()
```

---

## Complexity & Performance Notes

| Operation | Complexity | Notes |
|---|---|---|
| `df[col]` | O(1) | Direct lookup |
| `df.loc[mask]` | O(n) | Scans rows |
| `df.merge()` | O(n + m) | Hash join |
| `df.groupby().agg()` | O(n) | Single pass |
| `df.sort_values()` | O(n log n) | TimSort |
| `pd.pivot_table()` | O(n log n) | GroupBy + sort |

**Performance tips:**
- Use vectorized operations instead of `.apply()` + Python loops when possible.
- Use `df.query()` for readable filters — comparable speed to boolean masks.
- Specify `dtype` when reading CSVs to avoid expensive type inference.
- Use `category` dtype for low-cardinality string columns (saves memory, speeds up groupby).
- Use `df.to_parquet()` instead of CSV for large files — much faster read/write.

```python
# Convert string cols with few unique values to category
df["department"] = df["department"].astype("category")

# Faster IO for big datasets
df.to_parquet("data.parquet", index=False)
df = pd.read_parquet("data.parquet")
```
