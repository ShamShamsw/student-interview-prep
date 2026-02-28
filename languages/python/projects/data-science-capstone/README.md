````markdown
# Project: Data Science Capstone — End-to-End ML Pipeline

**Estimated Time:** 6–10 hours (spread across multiple sessions)  
**Difficulty:** Intermediate  
**Concepts:** EDA, feature engineering, model training, evaluation, interpretation, reporting

---

## Overview

Build a complete, production-style data science pipeline from raw data to a deployable model and a stakeholder report. This project mirrors what a data analyst or junior data scientist would deliver in a real job.

You will work through:

1. Business problem framing
2. Data ingestion and validation
3. Exploratory data analysis
4. Feature engineering
5. Model training and selection
6. Model evaluation and interpretation
7. A written summary report

---

## Business Problem

> **Predicting Employee Attrition**
>
> The HR department wants to understand why employees leave and identify at-risk employees before they quit. A 10-percentage-point reduction in attrition would save the company approximately $1.2 M per year in hiring and training costs.
>
> **Goal:** Build a binary classification model that predicts whether an employee will leave (`left_company = 1`) within the next performance cycle.

---

## Dataset

Use the HR dataset from Mini-Project 07, or generate a fresh one:

```bash
python generate_hr_data.py   # same script as 07-exploratory-data-analysis
```

---

## Project Structure

```
data-science-capstone/
├── data/
│   └── hr_data.csv
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_modeling.ipynb
├── src/
│   ├── __init__.py
│   ├── features.py          # feature engineering functions
│   ├── model.py             # training and evaluation code
│   └── report.py            # generate summary tables and charts
├── outputs/
│   ├── eda_charts/
│   ├── model_results.json
│   └── final_report.md
├── requirements.txt
└── README.md
```

---

## Step-by-Step Instructions

---

### Step 1 — Business Understanding & Baseline

Before writing a single line of code, answer these questions in `outputs/final_report.md`:

- What does success look like? (metric: F1? Recall? AUC?)
- What is the cost of a false negative vs. a false positive?
  - False negative: employee is predicted to stay but leaves → no intervention → lose employee.
  - False positive: employee is predicted to leave but stays → unnecessary HR intervention.
- What is the naive baseline? (predict "stays" for everyone → accuracy = attrition rate)
- What features do you have access to before the employee leaves?

---

### Step 2 — Data Ingestion & Validation

```python
# src/features.py  (start here, add to it throughout)
import pandas as pd
import numpy as np

def load_and_validate(path: str) -> pd.DataFrame:
    """Load CSV and run basic data quality checks."""
    df = pd.read_csv(path)

    # TODO: Assert expected columns exist
    expected_cols = [
        "employee_id", "age", "gender", "education", "department",
        "years_at_company", "hours_per_week", "salary",
        "performance_score", "satisfaction", "left_company",
    ]
    missing_cols = set(expected_cols) - set(df.columns)
    assert not missing_cols, f"Missing columns: {missing_cols}"

    # TODO: Assert no duplicate employee_ids
    assert df["employee_id"].is_unique, "Duplicate employee IDs found"

    # TODO: Assert target variable is binary
    assert set(df["left_company"].dropna().unique()).issubset({0, 1})

    print(f"Loaded {len(df)} rows. All checks passed.")
    return df
```

---

### Step 3 — Exploratory Data Analysis

Complete the same EDA stages as Mini-Project 07, but focus specifically on the **target variable**:

```python
# notebooks/01_eda.ipynb

# 3a. Class balance
print(df["left_company"].value_counts(normalize=True) * 100)
# If heavily imbalanced (>80/20), note it — you will handle it in modeling.

# 3b. For each feature: compare distributions for left=0 vs left=1
for col in ["age", "salary", "years_at_company", "hours_per_week", "satisfaction"]:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 3))
    df.groupby("left_company")[col].plot.hist(bins=25, alpha=0.6, ax=ax1, legend=True)
    ax1.set_title(f"{col} — histogram by attrition")
    df.boxplot(column=col, by="left_company", ax=ax2)
    ax2.set_title(f"{col} — box plot by attrition")
    plt.tight_layout()
    plt.savefig(f"outputs/eda_charts/{col}_by_attrition.png")
    plt.show()

# 3c. Attrition rate per category
for col in ["department", "education", "gender"]:
    rates = df.groupby(col)["left_company"].mean().sort_values(ascending=False)
    rates.plot.barh(title=f"Attrition Rate by {col}")
    plt.xlabel("Attrition Rate")
    plt.tight_layout()
    plt.savefig(f"outputs/eda_charts/attrition_by_{col}.png")
    plt.show()
```

---

### Step 4 — Feature Engineering

```python
# src/features.py  (continued)

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create all model features from raw data."""
    df = df.copy()

    # TODO: Fill missing values
    df["satisfaction"] = df["satisfaction"].fillna(df["satisfaction"].median())
    df["salary"] = df["salary"].fillna(df["salary"].median())

    # TODO: Encode categoricals
    # Education — ordinal (has natural order)
    edu_order = {"High School": 0, "Bachelor's": 1, "Master's": 2, "PhD": 3}
    df["education_num"] = df["education"].map(edu_order)

    # Department, gender — one-hot encode
    df = pd.get_dummies(df, columns=["department", "gender"], drop_first=True)

    # TODO: Create new features
    df["salary_per_year"]        = df["salary"] / df["years_at_company"].clip(lower=1)
    df["is_overworked"]          = (df["hours_per_week"] > 50).astype(int)
    df["low_satisfaction"]       = (df["satisfaction"] <= 2).astype(int)
    df["high_performer"]         = (df["performance_score"] >= 4).astype(int)
    df["tenure_group"]           = pd.cut(
        df["years_at_company"],
        bins=[-1, 2, 5, 10, 100],
        labels=["<2yr", "2-5yr", "5-10yr", "10+yr"],
    ).astype(str)
    df = pd.get_dummies(df, columns=["tenure_group"], drop_first=True)

    # TODO: Drop columns not used in model
    drop_cols = ["employee_id", "education", "left_company"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors="ignore")

    return df
```

---

### Step 5 — Model Training & Selection

```python
# src/model.py
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score,
    classification_report, confusion_matrix,
)
import matplotlib.pyplot as plt
import seaborn as sns


def train_and_evaluate(X: pd.DataFrame, y: pd.Series, output_path: str = "outputs/model_results.json"):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    models = {
        "LogisticRegression": LogisticRegression(class_weight="balanced", max_iter=500),
        "RandomForest":       RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42),
        "GradientBoosting":   GradientBoostingClassifier(n_estimators=200, random_state=42),
    }

    results = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for name, model in models.items():
        X_fit = X_train_s if name == "LogisticRegression" else X_train.values
        X_eval = X_test_s if name == "LogisticRegression" else X_test.values

        # Cross-validated AUC
        cv_auc = cross_val_score(model, X_fit, y_train, cv=cv, scoring="roc_auc").mean()

        # Train and evaluate on test set
        model.fit(X_fit, y_train)
        y_pred = model.predict(X_eval)
        y_prob = model.predict_proba(X_eval)[:, 1]

        results[name] = {
            "cv_auc":   round(float(cv_auc), 4),
            "test_auc": round(float(roc_auc_score(y_test, y_prob)), 4),
            "f1":       round(float(f1_score(y_test, y_pred)), 4),
            "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        }
        print(f"\n{name}:")
        print(classification_report(y_test, y_pred))

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print("\nResults saved to", output_path)
    return results, models
```

---

### Step 6 — Model Interpretation

```python
# notebooks/03_modeling.ipynb  (after training RandomForest)

# 6a. Feature importance
rf = models["RandomForest"]
importance = pd.Series(rf.feature_importances_, index=X.columns)
importance.nlargest(15).sort_values().plot.barh(figsize=(8, 6))
plt.title("Top 15 Feature Importances (Random Forest)")
plt.tight_layout()
plt.savefig("outputs/feature_importance.png")
plt.show()

# 6b. Confusion matrix heatmap
cm = confusion_matrix(y_test, rf.predict(X_test))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Stayed", "Left"],
            yticklabels=["Stayed", "Left"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix — Random Forest")
plt.savefig("outputs/confusion_matrix.png")
plt.show()

# 6c. ROC curves for all models
from sklearn.metrics import roc_curve
plt.figure(figsize=(7, 6))
for name, model in models.items():
    X_eval = X_test_s if name == "LogisticRegression" else X_test.values
    y_prob = model.predict_proba(X_eval)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)
    plt.plot(fpr, tpr, label=f"{name} (AUC={auc:.3f})")
plt.plot([0,1],[0,1],"--", color="gray", label="Random")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curves")
plt.legend()
plt.savefig("outputs/roc_curves.png")
plt.show()
```

---

### Step 7 — Final Report

Complete `outputs/final_report.md` using this template:

```markdown
# Employee Attrition Prediction — Final Report

## Executive Summary
[2–3 sentences: what was built, best AUC, key finding]

## Data
- Source: HR dataset (500 employees, 11 features)
- Attrition rate: X% (class imbalance: Y:Z ratio)
- Missing values handled: ...

## Key EDA Findings
1. ...
2. ...
3. ...

## Feature Engineering
New features created:
- `salary_per_year` — proxy for compensation relative to tenure
- `is_overworked` — hours > 50/week
- ...

## Model Results

| Model | CV AUC | Test AUC | F1 | Accuracy |
|---|---|---|---|---|
| Logistic Regression | ... | ... | ... | ... |
| Random Forest | ... | ... | ... | ... |
| Gradient Boosting | ... | ... | ... | ... |

**Best model:** [name] with Test AUC = [value]

## Top Predictors of Attrition
1. [feature] — [interpretation]
2. [feature] — [interpretation]
3. [feature] — [interpretation]

## Business Recommendations
1. ...
2. ...
3. ...

## Limitations & Next Steps
- Dataset is synthetic — validate with real data before deployment.
- Class imbalance could be further addressed with SMOTE.
- Next: deploy model as a REST API (FastAPI) for HR dashboard integration.
```

---

## Evaluation Rubric

| Criterion | Points |
|---|---|
| Data loading & validation passes | 10 |
| EDA covers all 6 stages | 20 |
| Feature engineering (≥4 new features) | 15 |
| At least 2 models trained and compared | 20 |
| ROC + confusion matrix produced | 10 |
| Feature importance chart | 10 |
| Final report is complete and coherent | 15 |
| **Total** | **100** |

---

## Stretch Goals

- **Hyperparameter tuning:** Use `GridSearchCV` or `RandomizedSearchCV` to tune the best model.
- **SHAP explanations:** Install `shap` and generate a SHAP summary plot and a force plot for one individual prediction.
- **SMOTE:** Use `imbalanced-learn`'s `SMOTE` to handle class imbalance and compare results.
- **Deploy:** Wrap the trained model in a FastAPI endpoint that accepts employee JSON and returns a churn probability.
- **Dashboard:** Build a Streamlit dashboard that shows the EDA charts interactively.
````
