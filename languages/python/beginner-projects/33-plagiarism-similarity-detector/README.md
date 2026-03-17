# Beginner Project 33: Plagiarism Similarity Detector

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** semantic document similarity, pairwise risk scoring, nearest-neighbor analysis, and cluster discovery

---

## Why This Project?

Plagiarism detection is not only exact text matching. In real submissions, copied content is often paraphrased, reordered, or partially rewritten. This project demonstrates how to compare documents semantically using vector-based representations, then convert those signals into practical review artifacts.

This project teaches end-to-end document similarity workflows where you can:

- load or auto-generate a reusable local corpus,
- tokenize and vectorize text into deterministic TF-IDF embeddings,
- compute full pairwise cosine similarity matrices,
- compare semantic and lexical overlap for each document pair,
- flag potentially suspicious pairs by configurable thresholds,
- create nearest-neighbor summaries per document,
- group related documents via threshold-based clustering,
- persist run summaries and analysis records to JSON,
- inspect recent high-risk matches at startup,
- and rerun with deterministic settings for reproducible outputs.

---

## Separate Repository

You can also access this project in a separate repository:

[Plagiarism Similarity Detector Repository](https://github.com/ShamShamsw/plagiarism-similarity-detector.git)

---

## What You Will Build

You will build a plagiarism similarity detector that:

1. Loads a document corpus from `data/documents.json` (or seeds a starter corpus).
2. Normalizes and tokenizes document text with configurable token rules.
3. Builds deterministic TF-IDF embeddings with optional bigrams.
4. Computes a full cosine similarity matrix across all documents.
5. Produces pairwise semantic and lexical similarity scores.
6. Flags suspicious pairs by similarity threshold and risk level.
7. Generates per-document nearest-neighbor similarity reports.
8. Clusters related documents using threshold graph components.
9. Persists catalogs and run artifacts for historical analysis.
10. Prints a readable terminal report with pair, neighbor, and cluster tables.

---

## Requirements

- Python 3.11+
- `numpy` (for TF-IDF vectors, cosine similarity, and matrix operations)

Install with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
   PLAGIARISM SIMILARITY DETECTOR
======================================================================

Configuration:
   Project type:         plagiarism_similarity_detector
   Embedding method:     tfidf (unigram + optional bigram)
   Similarity threshold: 0.12
   Cluster threshold:    0.12
   Include bigrams:      True
   Min token length:     2
   Random seed:          42
   Max pairs in report:  8

Startup:
   Data directory:       data/
   Outputs directory:    data/outputs/
   Document corpus:      data/documents.json (loaded 8 docs)
   Run catalog:          data/runs.json (loaded 0 runs)
   Analysis catalog:     data/analyses.json (loaded 0 records)
   Recent high-risk:     None yet

---

Run complete:
   Run ID:               20260317_070246
   Documents processed:  8
   Pairs compared:       28
   Flagged pairs:        3
   Clusters found:       3
   Elapsed time:         585.47 ms

Corpus metrics: vocab=277 | mean_sim=0.1582 | median_pair=0.0205 | max_pair=0.2764

Top pair similarities:
   Pair                                | Semantic | Lexical  | Risk
   ------------------------------------+----------+----------+---------
   doc_003:doc_004                     |  0.2764  |  0.3929  | critical
   doc_001:doc_002                     |  0.1637  |  0.2258  | high
   doc_007:doc_008                     |  0.1238  |  0.1818  | medium

Nearest-neighbor report:
   Document ID | Most similar document | Score
   ------------+-----------------------+--------
   doc_003     | doc_004               | 0.2764
   doc_001     | doc_002               | 0.1637
   doc_007     | doc_008               | 0.1238

Cluster summary:
   Cluster      | Size | Avg similarity | Member preview
   -------------+------+----------------+------------------------------
   cluster_01   |    2 |    0.1637      | doc_001, doc_002
   cluster_02   |    2 |    0.2764      | doc_003, doc_004
   cluster_03   |    2 |    0.1238      | doc_007, doc_008

Artifacts saved:
   Run record:           data/outputs/run_20260317_070246.json
   Similarity matrix:    data/outputs/similarity_matrix_20260317_070246.json
   Pair report:          data/outputs/pairs_20260317_070246.json
   Cluster report:       data/outputs/clusters_20260317_070246.json
   Metadata exports:     3
```

---

## Run

```bash
python main.py
```
