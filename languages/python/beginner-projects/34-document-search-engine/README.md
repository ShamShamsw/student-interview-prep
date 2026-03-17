# Beginner Project 34: Document Search Engine

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** corpus indexing, TF-IDF retrieval, hybrid ranking, and persistent search analytics

---

## Why This Project?

A search engine is one of the most practical systems you can build with Python and data structures. It combines text normalization, vector scoring, ranking logic, and reusable persistence patterns. This project turns those pieces into a complete local retrieval workflow.

This project teaches end-to-end search workflows where you can:

- load or auto-generate a reusable local document corpus,
- normalize and tokenize query/document text consistently,
- build deterministic TF-IDF vectors for document indexing,
- score query-to-document relevance with cosine similarity,
- blend semantic and lexical overlap into one ranking score,
- filter low-confidence matches with configurable thresholds,
- return top-k ranked results for each query,
- persist run summaries and result records to JSON,
- inspect recent successful matches at startup,
- and rerun with deterministic settings for reproducible outputs.

---

## Separate Repository

You can also access this project in a separate repository:

[document search engine Repository](https://github.com/ShamShamsw/document-search-engine.git)

---

## What You Will Build

You will build a document search engine that:

1. Loads a corpus from `data/documents.json` (or seeds a starter set).
2. Loads a query batch from `data/queries.json` (or seeds sample queries).
3. Normalizes and tokenizes text with configurable token rules.
4. Builds deterministic TF-IDF document embeddings with optional bigrams.
5. Vectorizes each query into the same TF-IDF feature space.
6. Computes semantic query-to-document cosine similarity scores.
7. Adds lexical overlap scoring and blends both signals into ranking.
8. Filters by minimum score and returns top-k results per query.
9. Persists per-result metadata and run summaries for history.
10. Prints a readable terminal report with query and ranking tables.

---

## Requirements

- Python 3.11+
- `numpy` (for TF-IDF vectors, cosine scoring, and matrix operations)

Install with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
   DOCUMENT SEARCH ENGINE
======================================================================

Configuration:
   Project type:         document_search_engine
   Retrieval model:      tfidf semantic + lexical blend
   Top-k results:        4
   Minimum score:        0.10
   Include bigrams:      True
   Min token length:     2
   Semantic weight:      0.80
   Lexical weight:       0.20
   Random seed:          42

Startup:
   Data directory:       data/
   Outputs directory:    data/outputs/
   Document corpus:      data/documents.json (loaded 8 docs)
   Query set:            data/queries.json (loaded 4 queries)
   Run catalog:          data/runs.json (loaded 0 runs)
   Search catalog:       data/searches.json (loaded 0 records)
   Recent results:       None yet

---

Run complete:
   Run ID:               20260317_081500
   Documents indexed:    8
   Queries executed:     4
   Results returned:     9
   Elapsed time:         347.22 ms

Index metrics: vocab=311 | mean_score=0.2218 | min_score=0.1114 | max_score=0.5962

Query summary:
   Query ID | Top document | Top score
   ---------+--------------+----------
   q_001    | doc_006      | 0.5962
   q_002    | doc_007      | 0.5201
   q_003    | doc_002      | 0.4817
   q_004    | doc_008      | 0.4429

Top blended matches:
   Query   | Rank | Document ID | Blended | Semantic | Lexical
   --------+------+-------------+---------+----------+--------
   q_001   |    1 | doc_006     | 0.5962 | 0.7104   | 0.1396
   q_002   |    1 | doc_007     | 0.5201 | 0.6338   | 0.0654
   q_003   |    1 | doc_002     | 0.4817 | 0.5712   | 0.1235
   q_004   |    1 | doc_008     | 0.4429 | 0.5093   | 0.1765

Artifacts saved:
   Run record:           data/outputs/run_20260317_081500.json
   Index snapshot:       data/outputs/index_20260317_081500.json
   Results report:       data/outputs/results_20260317_081500.json
   Metadata exports:     9
```

---

## Run

```bash
python main.py
```
