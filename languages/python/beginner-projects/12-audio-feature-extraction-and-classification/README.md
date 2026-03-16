# Beginner Project 12: Audio Feature Extraction And Classification

**Time:** 3-5 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** MFCC/chroma feature engineering, synthetic audio labeling, and classifier evaluation

---

## Why This Project?

Audio ML becomes much easier when you can control the signal source and inspect extracted features.
This project gives you a practical beginner workflow where you can:

- generate labeled audio clips with reproducible variation,
- extract MFCC and chroma features plus key spectral statistics,
- train and evaluate a baseline classifier,
- and save reproducible run artifacts for comparison.

---

## Separate Repository

You can also access this project in a separate repository:

[quiz game Repository](https://github.com/ShamShamsw/audio-features-extraction-and-classification.git)

---

## Separate Repository

This project is currently maintained in this monorepo.

---

## What You Will Build

You will build a command-line audio classification demo that:

1. Generates synthetic clips for low, mid, and high tone classes.
2. Extracts MFCC/chroma features and spectral summary metrics per clip.
3. Builds a feature matrix and train/test split with stratification.
4. Trains a RandomForest baseline classifier.
5. Computes accuracy and a confusion matrix on held-out test data.
6. Saves run metadata and recent feature records to JSON.

---

## Requirements

- Python 3.11+
- `numpy`
- `librosa`
- `scikit-learn`
- `soundfile`

Install with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
   AUDIO FEATURE EXTRACTION AND CLASSIFICATION - MFCC + CHROMA + ML
======================================================================

Configuration:
   Sample rate: 22050 Hz
   Clip duration: 2.0 seconds
   Samples per label: 24
   MFCC count: 13
   FFT window: 2048
   Hop length: 512
   Test split: 0.25

Synthetic labels:
   - low_tone (160.0 Hz): low-frequency harmonic tone with mild broadband noise
   - mid_tone (440.0 Hz): mid-frequency steady tone plus a weak overtone
   - high_tone (880.0 Hz): high-frequency tone profile with sharper spectral centroid

Run summary:
   Status: completed
   Total samples: 72
   Train/Test split: 54/18
   Feature vector size: 28
   Accuracy: 0.9444
   Confusion matrix (rows=true, cols=pred):
      labels: high_tone, low_tone, mid_tone
      high_tone: [6, 0, 0]
      low_tone: [0, 6, 0]
      mid_tone: [1, 0, 5]
Saved run artifact: data/runs/latest_audio_classification_run.json
```

---

## Build Order

Follow this order for clean architecture:

1. `storage.py`
2. `models.py`
3. `operations.py`
4. `display.py`
5. `main.py`

---

## File Responsibilities

- `storage.py`: handles run artifact persistence in `data/runs/`.
- `models.py`: creates consistent record payloads for config, label specs, extracted features, and summaries.
- `operations.py`: synthetic audio generation, feature extraction, model training, and evaluation.
- `display.py`: formats a readable CLI banner, startup guide, and run summary.
- `main.py`: thin orchestration entry point.

---

## Suggested Reflection Prompts

Add answers in your own notes after running the project:

- Which features separated classes most clearly in your runs?
- How did accuracy change when you modified noise level or clip duration?
- What are limits of synthetic data when preparing for real-world audio classification?

---

## Stretch Goals

1. Load real audio clips from folders instead of generating synthetic samples.
2. Add mel-spectrogram statistics and compare feature importance.
3. Compare RandomForest to SVM and logistic regression baselines.
4. Save misclassified test examples to a CSV review report.
