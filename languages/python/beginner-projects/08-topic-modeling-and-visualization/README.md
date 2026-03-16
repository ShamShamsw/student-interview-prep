# Beginner Project 08: Topic Modeling And Visualization

**Time:** 2.5-4.5 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Text preprocessing, unsupervised topic discovery, and making model output interpretable

---

## Why This Project?

Most beginner ML projects are supervised (you already know the labels). Topic modeling is different: it finds hidden structure in text without explicit labels.

In this project you will:

- prepare a text corpus,
- run topic models,
- compare topic quality,
- and present topics clearly enough for a non-technical reader.

---

## Separate Repository

You can also access this project in a separate repository:

[topic modeling and visulaization Repository](https://github.com/ShamShamsw/topic-modeling-and-visualization.git)

---

## The Importance of Comments

This project introduces **interpretability comments**. Your comments should explain:

- why you chose a vectorizer setup,
- why you chose the number of topics,
- and how to read the resulting topic-word lists.

Example:

```python
# We remove very common terms with max_df so topics are driven by
# domain words, not generic words that appear in almost every document.
vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words="english")
```

Example:

```python
# NMF is often easier to interpret on TF-IDF-like features, while LDA
# gives a probabilistic topic mixture. We run both for comparison.
```

---

## Requirements

Build a command-line topic modeling workflow that supports:

1. Loading a text corpus from file or built-in sample documents.
2. Preprocessing text (basic cleaning, stop words handling).
3. Vectorizing documents.
4. Training both NMF and LDA topic models.
5. Extracting top words per topic.
6. Showing a per-document dominant topic summary.
7. Saving run artifacts (topics and metadata).

### Example session

```
=======================================================
         TOPIC MODELING AND VISUALIZATION - RUN
=======================================================

Loaded documents: 40
Vectorized shape: (40, 520)

Training models with 5 topics...

Top NMF topics:
   Topic 0: model, training, accuracy, dataset, feature
   Topic 1: market, revenue, customer, growth, product

Top LDA topics:
   Topic 0: policy, government, public, law, rights
   Topic 1: game, team, season, score, player

Saved artifact:
   data/runs/latest_topics.json

Done.
```

---

## STOP - Plan Before You Code

Spend 20-30 minutes planning.

### Planning Question 1: Corpus Design

- Where does text come from?
- How many documents are needed for a meaningful run?
- What text quality issues do you expect?

### Planning Question 2: Preprocessing Choices

- What normalization steps will you apply?
- Which stop words strategy will you use?
- Should you keep numbers/punctuation?

### Planning Question 3: Modeling Choices

- How many topics will you start with?
- Why run NMF and LDA both?
- How will you compare interpretability?

### Planning Question 4: Output Interpretation

- How will you display top words per topic?
- How will you map a document to a dominant topic?
- What caveats should be explained in comments?

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

Create safe JSON save/load helpers for topic artifacts in `data/runs/`.

### Step 2: Build models.py

Add constructors for run config, topic objects, and run summary objects.

### Step 3: Build operations.py

Implement pipeline functions:

- load corpus,
- vectorize,
- train NMF and LDA,
- extract top words,
- compute dominant topic per document,
- persist summary.

### Step 4: Build display.py

Create formatting functions for:

- header,
- topic tables,
- dominant topic summary,
- final report.

### Step 5: Build main.py

Keep main as a thin orchestrator that calls operations and display.

---

## Comment Checklist

- [ ] Module docstring in all 5 Python files
- [ ] Every function has docstring with Parameters and Returns
- [ ] At least 5 comments explain why a choice was made
- [ ] Topic count choice is justified in comments
- [ ] Limitations of topic modeling are documented
- [ ] `if __name__ == "__main__"` guard includes explanation

---

## Reflect on What You Learned

Write 2-3 sentences for each audience at the bottom of `main.py`:

- Friend: what topic modeling does in plain language
- Employer: workflow and engineering skills you practiced
- Professor: technical explanation of vectorization and unsupervised modeling

---

## Stretch Goals

1. Add coherence-based topic count tuning.
2. Export topic-word charts to `outputs/`.
3. Add pyLDAvis output export for interactive inspection.
4. Add custom stop-word management per domain.
