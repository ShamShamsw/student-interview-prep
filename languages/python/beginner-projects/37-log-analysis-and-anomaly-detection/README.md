# Beginner Project 37: Log Analysis And Anomaly Detection

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Common-log parsing, rule-based anomaly scoring, and persistent security-oriented run analytics

---

## Why This Project?

Production systems generate large volumes of HTTP logs, but raw log lines are hard to inspect manually. This project demonstrates how to turn semi-structured web logs into actionable anomaly reports using a deterministic parser, lightweight feature engineering, and explainable scoring rules.

This project teaches end-to-end log monitoring workflow concepts where you can:

- load or auto-generate a reusable local log library,
- parse Common Log Format style records into structured events,
- flag malformed lines that fail schema validation,
- compute request-level features like off-hours access, burst traffic, and suspicious paths,
- detect repeated auth failures and server-error clusters by IP,
- score anomalies with human-readable supporting evidence,
- export parsed logs and anomaly reports to JSON,
- generate a text timeline view for rapid terminal inspection,
- persist run summaries and per-anomaly metadata to JSON,
- track recent anomalies and historical run catalogs,
- and print a readable terminal report with preview rows and export paths.

---

## Separate Repository

You can also access this project in a separate repository:

[Image Annotation Tool For Detection Repository](https://github.com/ShamShamsw/log-analysis-and-anomaly-detection.git)

---


## What You Will Build

You will build a log analysis and anomaly detection tool that:

1. Loads a log library from `data/library.json` (or seeds a starter set).
2. Parses Common Log Format style records into structured request events.
3. Detects malformed lines that do not match the expected schema.
4. Builds request features including minute buckets, off-hours flags, and suspicious-path markers.
5. Scores events for unusual behavior using explainable rule-based heuristics.
6. Identifies burst request patterns, repeated auth failures, suspicious probes, and server error spikes.
7. Exports parsed request events to JSON for downstream tooling.
8. Exports anomaly records with evidence and severity scores.
9. Produces a plain-text timeline summary with status and anomaly counts.
10. Persists per-anomaly metadata and run summaries for history and auditing.

---

## Requirements

- Python 3.11+
- No external dependencies - the parser and anomaly engine use stdlib only.

---

## Example Session

```text
======================================================================
   LOG ANALYSIS AND ANOMALY DETECTION
======================================================================

Configuration:
   Project type:         log_analysis_and_anomaly_detection
   Analyzer engine:     common-log parser + rule scoring (stdlib only)
   Top patterns:         6
   Score threshold:      3.0
   Include timeline:     True
   Include IP summary:   True
   Include path summary: True
   Max anomalies report: 10
   Random seed:          42

Startup:
   Data directory:       data/
   Outputs directory:    data/outputs/
   Log library:          data/library.json (loaded 18 log lines)
   Run catalog:          data/runs.json (loaded 0 runs)
   Anomaly catalog:      data/anomalies.json (loaded 0 records)
   Recent anomalies:     None yet

---

Run complete:
   Run ID:               20260317_190458
   Log lines processed:  18
   Parsed events:        17
   Anomalies detected:   10
   Unique IPs:           12
   Elapsed time:         219.88 ms

Dataset metrics: error_rate=47.1% | server_error_rate=23.5% | offhours_share=5.9% | peak_minute_volume=4 | max_score=9.0

Anomaly previews:
   ID      | Time                 | IP              | Type                     | Score | Evidence
   --------+----------------------+-----------------+--------------------------+-------+------------------------------
   anm_001 |                      | unknown         | malformed_log_entry      |   9.0 | log line did not match expec
   anm_007 | 2026-03-17T08:04:01+ | 192.0.2.55      | server_error_spike       |   7.0 | 5xx response observed (500)
   anm_003 | 2026-03-17T08:02:10+ | 203.0.113.77    | repeated_auth_failures   |   6.0 | multiple authentication fail

Artifacts saved:
   Run record:           data/outputs/run_20260317_190458.json
   Parsed export:        data/outputs/parsed_20260317_190458.json
   Anomaly export:       data/outputs/anomalies_20260317_190458.json
   Timeline export:      data/outputs/timeline_20260317_190458.txt
   Metadata exports:     10
```

---

## Run

```bash
python main.py
```
