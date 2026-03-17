# Beginner Project 32: Image Augmentation Playground

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Image augmentation pipelines, before/after visualization, metric tracking, and reproducible evaluation

---

## Why This Project?

Image augmentation is one of the most practical techniques in computer vision. It helps models generalize by exposing them to transformed versions of training data without collecting new samples.

This project teaches end-to-end augmentation workflows where you can:

- generate a deterministic synthetic image dataset,
- apply reusable augmentation pipelines (color, geometry, noise, and combined),
- compare before/after outputs in exported preview grids,
- compute quality deltas (brightness and contrast) per pipeline,
- evaluate model impact using a baseline vs augmented classifier comparison,
- export run metadata and augmentation records to JSON,
- keep historical catalogs of runs and augmentation sessions,
- inspect recent pipeline usage at startup,
- and run everything with deterministic seeds for reproducibility.

---

## Separate Repository

You can also access this project in a separate repository:

[Image Augmentation Playground Repository](https://github.com/ShamShamsw/image-augmentation-playground.git)

---

## What You Will Build

You will build an image augmentation playground that:

1. Creates synthetic RGB image classes (circle, stripes, bars, ring).
2. Defines named augmentation pipelines from composable operations.
3. Applies augmentations deterministically with a fixed random seed.
4. Exports side-by-side before/after grid images per pipeline.
5. Computes per-pipeline brightness and contrast deltas.
6. Compares classifier accuracy with and without augmentation.
7. Persists augmentation metadata records as JSON artifacts.
8. Maintains run and augmentation catalogs for historical tracking.
9. Prints a readable terminal report with pipeline and evaluation tables.
10. Produces reproducible outputs and metrics from the same configuration.

---

## Requirements

- Python 3.11+
- `numpy` (for synthetic image generation and augmentation operations)
- `matplotlib` (for rendering and exporting comparison grids)

Install with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
   IMAGE AUGMENTATION PLAYGROUND
======================================================================

Configuration:
   Project type:         image_augmentation_playground
   Image size:           256x256
   Samples per class:    8
   Classes:              4 (circle, stripes, bars, ring)
   Augmentation rounds:  3
   Color mode:           rgb
   Random seed:          42
   Export DPI:           120
   Evaluate classifier:  True

Startup:
   Data directory:       data/
   Outputs directory:    data/outputs/
   Run catalog:          data/runs.json (loaded 0 runs)
   Aug catalog:          data/augmentations.json (loaded 0 records)
   Recent pipelines:     None yet

---

Run complete:
   Run ID:               20260317_063852
   Pipelines applied:    4
   Grids exported:       4
   Elapsed time:         4824.60 ms

Augmentation pipelines:
   Pipeline            | Operations                             | Δ Brightness | Δ Contrast
   --------------------+----------------------------------------+--------------+-----------
   color_jitter        | brightness → contrast                  |    +0.0205   |    +0.0385
   geometric           | h_flip → crop_resize                   |    +0.0148   |    +0.0107
   noise_injection     | gaussian_noise → salt_pepper           |    +0.0208   |    +0.0077
   combined            | h_flip → brightness → gaussian_noise   |    +0.0292   |    +0.0289

Classifier evaluation (nearest-centroid, channel-statistic features):
   Setting              | Train samples | Test samples  | Accuracy
   ---------------------+---------------+---------------+---------
   Baseline (no aug)    |            24 |             8 |   100.0%
   Augmented (+3x aug)  |            96 |             8 |   100.0%
   Delta                |           +72 |            -- |    +0.0%

Artifacts saved:
   Run record:           data/outputs/run_20260317_063852.json
   Grid exports:         4
   Metadata exports:     4
```

---

## Run

```bash
python main.py
```
