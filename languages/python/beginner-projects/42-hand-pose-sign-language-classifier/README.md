# Beginner Project 42: Hand-Pose Sign Language Classifier

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Synthetic hand-landmark capture, nearest-centroid sign classification, held-out evaluation, and scripted live inference visualization

---

## Why This Project?

Hand-pose recognition sits at the intersection of computer vision, geometry, and machine learning. Even when you remove the complexity of a live webcam feed, the underlying workflow is still valuable: you need a repeatable landmark representation, a dataset capture loop, a training step, an evaluation step, and an inference path that behaves like a real-time classifier.

This project teaches end-to-end sign classification concepts where you can:

- seed a reusable sign-template library for a small hand-sign vocabulary,
- generate deterministic synthetic hand-landmark captures for each target sign,
- normalize 21-point landmark sets into stable geometry-based feature vectors,
- split the captured dataset into train and test partitions per sign,
- train a pure-Python nearest-centroid classifier on extracted landmark features,
- evaluate classifier quality with per-sign accuracy and a confusion matrix,
- run a scripted live-inference demo over noisy synthetic frames,
- flag low-confidence predictions using a configurable confidence threshold,
- render a confusion-matrix heatmap for held-out sign predictions,
- render a confidence timeline for the simulated live demo,
- export model and live-inference artifacts to JSON,
- and persist historical runs and captured samples for repeatable auditing.

---

## Separate Repository

You can also access this project in a separate repository:

[quiz game Repository](https://github.com/ShamShamsw/hand-pose-sign-language-classifier.git)

---

## What You Will Build

You will build a hand-pose sign language classifier that:

1. Loads sign templates from `data/sign_templates.json` (or seeds a starter set of 5 signs).
2. Simulates dataset capture mode by generating 24 augmented landmark samples per sign.
3. Extracts normalized geometric features from 21 hand landmarks per sample.
4. Splits the dataset into deterministic training and test partitions.
5. Trains a pure-Python nearest-centroid classifier over the captured features.
6. Evaluates held-out accuracy across the supported sign vocabulary.
7. Tracks per-sign performance and confusion-matrix counts.
8. Runs a scripted live-inference demo over 12 noisy synthetic frames.
9. Flags low-confidence live predictions using a configurable threshold.
10. Saves a confusion matrix plot and a live-confidence timeline under `data/outputs/`.
11. Persists a model bundle, live-inference bundle, run summary, and captured dataset catalog for future sessions.

---

## Requirements

- Python 3.11+
- `matplotlib`

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
   HAND-POSE SIGN LANGUAGE CLASSIFIER
======================================================================

Configuration:
   Project type:           hand_pose_sign_classifier
   Sign vocabulary:        A, B, C, L, Y
   Landmarks per hand:     21
   Capture samples/sign:   24
   Training split:         75%
   Live demo frames:       12
   Low-confidence cutoff:  0.58
   Confusion matrix:       True
   Confidence timeline:    True
   Max predictions report: 8
   Random seed:            42

Startup:
   Data directory:         data/
   Outputs directory:      data/outputs/
   Template library:       data/sign_templates.json (loaded 0 signs)
   Run catalog:            data/runs.json (loaded 0 runs)
   Dataset catalog:        data/dataset.json (loaded 0 samples)
   Recent samples:         None yet

---

Session complete:
   Session ID:             20260317_210350
   Signs modeled:          5
   Captures generated:     120
   Training samples:       90
   Test samples:           30
   Test accuracy:          100.0%
   Live frames:            12
   Low-confidence frames:  1
   Elapsed time:           630.19 ms

Classifier metrics: macro_accuracy=100.0% | avg_live_confidence=65.7% | feature_dimension=77 | classifier=nearest_centroid

Prediction previews:
   Frame          | Expected | Predicted | Confidence | Low conf
   ---------------+----------+-----------+------------+---------
   live_001       | A        | A         | 58.04%     | no
   live_002       | B        | B         | 65.36%     | no
   live_003       | C        | C         | 65.46%     | no
   live_004       | L        | L         | 58.28%     | no
   live_005       | Y        | Y         | 77.86%     | no
   live_006       | L        | L         | 72.64%     | no
   live_007       | C        | C         | 63.49%     | no
   live_008       | B        | B         | 71.62%     | no

Artifacts saved:
   Run record:             data/outputs/run_20260317_210350.json
   Model file:             data/outputs/model_20260317_210350.json
   Live inference file:    data/outputs/live_inference_20260317_210350.json
   Confusion matrix:       data/outputs/confusion_matrix_20260317_210350.png
   Confidence timeline:    data/outputs/confidence_timeline_20260317_210350.png
   Total captures logged:  120
```

---

## Run

```bash
python main.py
```
