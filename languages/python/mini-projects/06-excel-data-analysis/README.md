````markdown
# Mini-Project 06: Excel-Style Data Analysis with pandas

**Time:** 1.5–2 hours  
**Difficulty:** Beginner–Medium  
**Concepts:** pandas, data cleaning, groupby, pivot tables, merge, visualization

---

## Objective

Re-create common Excel workflows — filters, pivot tables, VLOOKUP, charts — entirely in Python using pandas and Matplotlib. By the end you will be comfortable trading a spreadsheet for a reproducible, scriptable analysis.

---

## Dataset

Use the included synthetic `sales_data.csv` file or generate it with the setup script below. It simulates 1 year of retail transactions.

**Columns:**

| Column | Description |
|---|---|
| `order_id` | Unique order identifier |
| `date` | Transaction date (YYYY-MM-DD) |
| `customer_id` | Customer identifier |
| `product` | Product name |
| `category` | Product category (Electronics, Clothing, Food, Home) |
| `region` | Sales region (North, South, East, West) |
| `quantity` | Units sold |
| `unit_price` | Price per unit in USD |
| `discount_pct` | Discount percentage (0–30) |

**Generate the dataset:**

```python
# generate_data.py
import numpy as np
import pandas as pd

np.random.seed(42)
n = 2000

categories = ["Electronics", "Clothing", "Food", "Home"]
products = {
    "Electronics": ["Laptop", "Headphones", "Tablet", "Keyboard"],
    "Clothing":    ["T-Shirt", "Jeans", "Jacket", "Shoes"],
    "Food":        ["Coffee", "Tea", "Snacks", "Vitamins"],
    "Home":        ["Lamp", "Pillow", "Blanket", "Candle"],
}
price_ranges = {
    "Electronics": (50, 1200),
    "Clothing":    (15, 200),
    "Food":        (5, 40),
    "Home":        (10, 150),
}

category_col = np.random.choice(categories, n)
product_col  = [np.random.choice(products[c]) for c in category_col]
price_col    = [
    round(np.random.uniform(*price_ranges[c]), 2)
    for c in category_col
]

df = pd.DataFrame({
    "order_id":     range(1001, 1001 + n),
    "date":         pd.to_datetime(
        np.random.choice(pd.date_range("2024-01-01", "2024-12-31"), n)
    ),
    "customer_id":  np.random.randint(1, 201, n),
    "product":      product_col,
    "category":     category_col,
    "region":       np.random.choice(["North", "South", "East", "West"], n),
    "quantity":     np.random.randint(1, 10, n),
    "unit_price":   price_col,
    "discount_pct": np.random.choice([0, 5, 10, 15, 20, 25, 30], n),
})

df.to_csv("sales_data.csv", index=False)
print(f"Saved {n} rows to sales_data.csv")
```

---

## Tasks

Complete each task and save the analysis to `analysis.py` (or a Jupyter notebook).

---

### Task 1 — Load & Inspect (Excel: Open Workbook)

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("sales_data.csv", parse_dates=["date"])

# TODO: Answer these questions using pandas:
# 1. How many rows and columns?
# 2. What are the data types of each column?
# 3. Are there any missing values?
# 4. What is the date range of the data?
# 5. How many unique customers are there?
```

---

### Task 2 — Add Computed Columns (Excel: Formula Columns)

```python
# TODO: Add these columns to df:
# 1. "revenue"         = quantity * unit_price * (1 - discount_pct / 100)
# 2. "month"           = month number extracted from date
# 3. "month_name"      = month name ("January", "February", ...)
# 4. "quarter"         = "Q1", "Q2", "Q3", or "Q4"
# 5. "revenue_tier"    = "Low" (<100), "Medium" (100–500), "High" (>500)
#                        (Hint: use pd.cut or np.select)
```

---

### Task 3 — Filter Rows (Excel: AutoFilter)

```python
# TODO: Create the following filtered DataFrames:
# 1. Orders from the "Electronics" category
# 2. Orders in Q4 (October–December)
# 3. Orders with a discount > 15%
# 4. Orders from the "West" region with revenue > $500
# 5. Orders for customers who bought more than once
#    (Hint: groupby customer_id, count orders, filter)
```

---

### Task 4 — Sort and Rank (Excel: Sort & RANK)

```python
# TODO:
# 1. Sort the DataFrame by revenue descending — show top 10
# 2. Add a "revenue_rank" column (rank 1 = highest revenue)
# 3. Add a "rank_in_category" column (rank within each category)
#    (Hint: df.groupby("category")["revenue"].rank(ascending=False))
```

---

### Task 5 — Aggregation & GroupBy (Excel: SUMIF / COUNTIF / AVERAGEIF)

```python
# TODO: Using groupby, compute:
# 1. Total revenue per category
# 2. Average order value per region
# 3. Number of orders per month
# 4. Top 5 products by total revenue
# 5. Revenue summary table: mean, sum, count, max per category × region
#    (Hint: use .agg() with a dict of functions)
```

---

### Task 6 — Pivot Table (Excel: Insert → Pivot Table)

```python
# TODO: Build this pivot table:
#   Rows    = region
#   Columns = quarter
#   Values  = total revenue (sum)
#   Include grand totals (margins=True)

pivot = pd.pivot_table(
    df,
    values=???
    index=???
    columns=???
    aggfunc=???
    fill_value=0,
    margins=True,
    margins_name="Grand Total",
)
print(pivot.round(2))
```

---

### Task 7 — VLOOKUP: Enrich with Customer Data (Excel: VLOOKUP)

```python
# Simulate a customer lookup table
customers = pd.DataFrame({
    "customer_id": range(1, 201),
    "customer_name": [f"Customer_{i}" for i in range(1, 201)],
    "segment": np.random.choice(["Retail", "Wholesale", "Online"], 200),
    "signup_year": np.random.choice([2019, 2020, 2021, 2022, 2023], 200),
})

# TODO:
# 1. Left-join df with customers on "customer_id"
# 2. Compute total revenue per customer segment
# 3. Find the average order size for Wholesale vs Retail customers
```

---

### Task 8 — Rolling Averages & Trends (Excel: Moving Average)

```python
# TODO:
# 1. Group orders by date and sum revenue → daily_revenue Series
# 2. Compute a 7-day rolling average of daily revenue
# 3. Compute month-over-month revenue and pct change
# 4. Plot daily revenue with the 7-day rolling average overlaid
```

---

### Task 9 — Charts (Excel: Insert Chart)

Produce these four charts in a single 2×2 figure:

```python
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Sales Dashboard — 2024", fontsize=16)

# Chart 1 (top-left): Monthly revenue bar chart
# Chart 2 (top-right): Revenue by category (horizontal bar)
# Chart 3 (bottom-left): Revenue distribution histogram
# Chart 4 (bottom-right): Region × Category heatmap
#   Hint for heatmap: pivot → sns.heatmap(annot=True, fmt=".0f")

plt.tight_layout()
plt.savefig("sales_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
```

---

### Task 10 — Export Report (Excel: Save As)

```python
# TODO: Write df to a multi-sheet Excel workbook:
# Sheet 1: "Raw Data"    — the full cleaned DataFrame
# Sheet 2: "Pivot"       — the region × quarter pivot table
# Sheet 3: "Top 20"      — top 20 orders by revenue

with pd.ExcelWriter("sales_report.xlsx", engine="openpyxl") as writer:
    ???
```

---

## Expected Output

After completing all tasks, your workspace should contain:

```
06-excel-data-analysis/
├── generate_data.py
├── analysis.py          (or analysis.ipynb)
├── sales_data.csv       (generated)
├── sales_dashboard.png  (generated)
└── sales_report.xlsx    (generated)
```

---

## Solution Hints

<details>
<summary>Task 2 — Revenue tier using pd.cut</summary>

```python
df["revenue_tier"] = pd.cut(
    df["revenue"],
    bins=[0, 100, 500, float("inf")],
    labels=["Low", "Medium", "High"],
)
```
</details>

<details>
<summary>Task 5 — Multiple aggregations</summary>

```python
df.groupby(["category", "region"])["revenue"].agg(
    mean="mean", total="sum", orders="count", max_order="max"
).round(2)
```
</details>

<details>
<summary>Task 8 — Daily revenue and rolling average</summary>

```python
daily = df.groupby("date")["revenue"].sum().sort_index()
daily_rolling = daily.rolling(window=7).mean()

ax.plot(daily.index, daily, alpha=0.4, label="Daily")
ax.plot(daily_rolling.index, daily_rolling, linewidth=2, label="7-day avg")
ax.legend()
```
</details>

<details>
<summary>Task 10 — Multi-sheet Excel export</summary>

```python
with pd.ExcelWriter("sales_report.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Raw Data", index=False)
    pivot.to_excel(writer, sheet_name="Pivot")
    df.nlargest(20, "revenue").to_excel(writer, sheet_name="Top 20", index=False)
```
</details>

---

## Stretch Goals

- Add a "profit_margin" column assuming cost = unit_price × 0.6.
- Find the customer lifetime value (CLV) — total revenue per customer.
- Build a simple forecasting model: fit a linear trend to monthly revenue and predict the next 3 months.
- Use `plotly.express` to make the charts interactive.
````
