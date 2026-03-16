# Beginner Project 07: Handwritten Digit Recognizer (MNIST)

**Time:** 2.5-4.5 hours  
**Difficulty:** Beginner+  
**Focus:** Intro machine learning workflow, model evaluation, misclassification analysis, and explaining performance clearly

---

## Why This Project?

This is your first end-to-end machine learning project in this track. You will:

- load and inspect a real dataset,
- train a baseline classifier,
- evaluate results with multiple metrics,
- and explain where the model fails.

The goal is not to build the most accurate model. The goal is to learn the workflow and document your reasoning.

---

## Separate Repository

You can also access this project in a separate repository:

[quiz game Repository](https://github.com/ShamShamsw/quiz-game.git)

---

## The Importance of Comments

This project introduces **evaluation-focused comments**. In ML code, comments should explain:

- why you chose a model,
- why you used a metric,
- and what the errors mean.

Example:

```python
# We start with LogisticRegression because it is fast, interpretable,
# and gives us a strong baseline before trying more complex models.
model = LogisticRegression(max_iter=1000)
```

Another example:

```python
# Accuracy alone can hide weak spots, so we also compute per-class
# precision/recall to see which digits are commonly confused.
report = classification_report(y_true, y_pred, output_dict=True)
```

---

## Requirements

Build a command-line MNIST digit recognizer pipeline that supports:

1. Loading a digit dataset (`sklearn.datasets.load_digits` is recommended baseline).
2. Splitting data into train and test sets.
3. Training a baseline classifier.
4. Evaluating with:
    - accuracy,
    - confusion matrix,
    - per-class precision/recall/F1.
5. Finding common misclassifications.
6. Saving run artifacts (metrics and metadata).
7. Printing a readable summary report.

### Example session

```
=======================================================
         HANDWRITTEN DIGIT RECOGNIZER - BASELINE RUN
=======================================================

Loading dataset...
Dataset loaded: 1797 samples, 64 features, 10 classes

Splitting data (test_size=0.2, random_state=42)...
Training baseline model (Logistic Regression)...

Evaluation:
   Accuracy: 0.9639

Top confusion pairs:
   8 -> 1 : 3 samples
   9 -> 4 : 2 samples
   3 -> 5 : 2 samples

Run artifacts saved to:
   data/runs/latest_run.json

Done.
```

---

## STOP - Plan Before You Code

Spend 20-30 minutes planning first.

### Planning Question 1: Dataset and Features

- Which dataset loader will you use and why?
- What are the feature dimensions?
- What does each label represent?

### Planning Question 2: Baseline Model Choice

- Which baseline model will you start with?
- Why this model before more advanced models?
- What hyperparameters will you set explicitly?

### Planning Question 3: Evaluation Strategy

- Which metrics will you report and why?
- How will you inspect per-class performance?
- How will you identify common error patterns?

### Planning Question 4: Artifact Tracking

- What files should be saved after each run?
- What metadata is needed for reproducibility?
   - random seed
   - train/test split settings
   - model name and parameters

### Planning Question 5: Build Order

Suggested order:

1. `storage.py` (run artifact save/load)
2. `models.py` (config/result object builders)
3. `operations.py` (data load, train, evaluate)
4. `display.py` (formatted reports)
5. `main.py` (orchestration and menu/runner)

Test after each step.

---

## Step-by-Step Instructions

### Step 1: Build storage.py first

Create helpers to save and load JSON run summaries in `data/runs/`.

### Step 2: Build models.py

Add constructors for:

- run configuration,
- training result summary,
- confusion pair summary entries.

### Step 3: Build operations.py

Implement core workflow functions:

- load dataset,
- split,
- train baseline,
- evaluate,
- extract top misclassification pairs,
- persist summary.

### Step 4: Build display.py

Create formatting functions for:

- header/banner,
- metric summary,
- confusion pair table,
- final run report.

### Step 5: Build main.py

Make `main.py` a thin controller that calls operations and display.

---

## Comment Checklist

- [ ] Module docstring in all 5 Python files
- [ ] Every function has Parameters/Returns in docstring
- [ ] At least 5 comments explain why decisions were made
- [ ] Metrics are justified in comments
- [ ] Misclassification analysis logic is explained in comments
- [ ] `if __name__ == "__main__"` guard includes an explanation comment

---

## Reflect on What You Learned

Write 2-3 sentences for each audience at the bottom of `main.py`:

- Friend: what the project does in plain language
- Employer: what engineering skills you practiced
- Professor: technical explanation of evaluation pipeline and error analysis

---

## Stretch Goals

1. Compare two baseline models and report side-by-side metrics.
2. Save sample misclassified images to `outputs/`.
3. Add cross-validation for more reliable baseline estimates.
4. Add a lightweight inference mode for single-image prediction.
