# Beginner Project 09: NLP Text Summarizer Demo

**Time:** 3-5 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** NLP preprocessing, extractive vs abstractive summarization, and quality comparison

---

## Why This Project?

Summarization is one of the most useful NLP tasks in real-world applications. This project helps you build a practical comparison workflow between two approaches:

- extractive summarization (selecting key original sentences),
- abstractive summarization (generating shorter paraphrased text).

In this project you will:

- prepare source text,
- generate summaries with both methods,
- compare quality and compression,
- and explain trade-offs clearly.

---

## Separate Repository

You can also access this project in a separate repository:

[NLP text summarizer demo Repository](https://github.com/ShamShamsw/nlp-text-summarizer-demo.git)

---

## The Importance of Comments

This project introduces **comparison-focused comments**. Your comments should explain:

- why each summarization method was chosen,
- why specific metrics were used,
- and what limitations exist in each approach.

Example:

```python
# Extractive summaries preserve original wording, which often improves
# factual reliability but can reduce flow between selected sentences.
```

Example:

```python
# Overlap-based metrics are useful for quick comparison, but they do not
# fully capture readability or factual correctness.
```

---

## Requirements

Build a command-line summarization workflow that supports:

1. Loading text from a file or built-in sample documents.
2. Basic preprocessing and sentence segmentation.
3. Extractive summary generation.
4. Abstractive summary generation (with fallback when model is unavailable).
5. Quality comparison using simple overlap/length metrics.
6. Saving run artifacts (summaries and metadata).

### Example session

```
=======================================================
            NLP TEXT SUMMARIZER DEMO - COMPARISON RUN
=======================================================

Loaded documents: 1
Source words: 640

Generating extractive summary...
Generating abstractive summary...

Comparison metrics:
   Extractive words: 128
   Abstractive words: 102
   Extractive overlap: 0.61
   Abstractive overlap: 0.49

Saved artifact:
   data/runs/latest_summary_run.json

Done.
```

---

## STOP - Plan Before You Code

Spend 20-30 minutes planning.

### Planning Question 1: Input Design

- What source text format will you support first?
- How will you handle empty or very short input?
- What text length is realistic for a first version?

### Planning Question 2: Extractive Strategy

- How will sentence importance be scored?
- How many sentences should be included in the summary?
- How will you preserve sentence order for readability?

### Planning Question 3: Abstractive Strategy

- Which model/API will you use?
- What fallback behavior will you use if model dependencies are missing?
- How will you keep run time manageable for beginners?

### Planning Question 4: Evaluation Choices

- Which metrics will you compute and why?
- How will you compare compression ratio between methods?
- What limitations should be documented in comments?

### Planning Question 5: Build Order

Suggested order:

1. `storage.py`
2. `models.py`
3. `operations.py`
4. `display.py`
5. `main.py`

---

## Step-by-Step Instructions

### Step 1: Build storage.py

Create safe JSON save/load helpers for run artifacts in `data/runs/`.

### Step 2: Build models.py

Add constructors for run config, summary outputs, and metric objects.

### Step 3: Build operations.py

Implement pipeline functions:

- load text,
- preprocess and split sentences,
- generate extractive summary,
- generate abstractive summary,
- compute comparison metrics,
- persist run artifact.

### Step 4: Build display.py

Create formatting functions for:

- header,
- summary output sections,
- metric comparison,
- final report.

### Step 5: Build main.py

Keep main as a thin orchestrator that calls operations and display.

---

## Comment Checklist

- [ ] Module docstring in all 5 Python files
- [ ] Every function has docstring with Parameters and Returns
- [ ] At least 5 comments explain why a choice was made
- [ ] Fallback behavior is documented clearly
- [ ] Metric limitations are documented
- [ ] `if __name__ == "__main__"` guard includes explanation

---

## Reflect on What You Learned

Write 2-3 sentences for each audience at the bottom of `main.py`:

- Friend: what summarization does in plain language
- Employer: workflow and engineering skills you practiced
- Professor: technical explanation of extractive vs abstractive comparison

---

## Stretch Goals

1. Add support for summarizing multiple documents together.
2. Add optional ROUGE scoring for deeper comparison.
3. Export a markdown summary report to `outputs/`.
4. Add a simple UI mode for interactive testing.
