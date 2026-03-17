# Beginner Project 20: Image Segmentation Interactive Demo

**Time:** 3-5 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** semantic segmentation fundamentals, encoder-decoder training dynamics, IoU and Dice monitoring, and qualitative mask inspection

---

## Why This Project?

Image segmentation is a core computer vision task where each pixel is classified into a region (foreground/background or semantic classes).
This project gives you a practical beginner workflow where you can:

- build a full segmentation pipeline end-to-end with only NumPy,
- train a compact encoder-decoder style model on synthetic grayscale images,
- track important segmentation metrics like IoU, Dice, and pixel accuracy,
- visualize predicted masks against ground-truth masks,
- and save reproducible run artifacts for analysis.

---

## Separate Repository

You can also access this project in a separate repository:

[image segmentation interactive demo Repository](https://github.com/ShamShamsw/image-segmentation-interactive-demo.git)

---

## What You Will Build

You will build a command-line image segmentation demo that:

1. Generates a synthetic 32x32 grayscale dataset with circles and rectangles plus noise.
2. Builds a lightweight encoder-decoder style neural network in NumPy.
3. Trains the model with binary cross-entropy for foreground/background mask prediction.
4. Evaluates validation performance each epoch with IoU, Dice score, and pixel accuracy.
5. Tracks epoch-level train and validation losses throughout training.
6. Saves visual artifacts (loss curves, quality trend, and prediction sample grid).
7. Persists a complete session summary to JSON for reproducibility.

---

## Requirements

- Python 3.11+
- `numpy`
- `matplotlib`
- `seaborn`

Install with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
   IMAGE SEGMENTATION INTERACTIVE DEMO - NUMPY ENCODER-DECODER
======================================================================

Configuration:
   Image size: 32x32 (grayscale)
   Train samples: 800
   Validation samples: 200
   Hidden dimension: 128
   Bottleneck dimension: 48
   Epochs: 160
   Batch size: 32
   Learning rate: 0.08
   Snapshot interval: every 20 epochs
   Random seed: 42

Dataset profile:
   Name: Synthetic 32x32 grayscale shapes
   Description: Mixed circles and rectangles with additive noise
   Pixel range: (0.0, 1.0)
   Mask labels: (0, 1)

Session behavior:
   1) Generate synthetic grayscale images with binary masks.
   2) Train a tiny encoder-decoder to predict segmentation masks.
   3) Track train/validation BCE loss each epoch.
   4) Track IoU, Dice score, and pixel accuracy on validation data.
   5) Save learning plots and segmentation prediction panels.

Session summary:
   Status: completed
   Training epochs: 160
   Final train loss: 0.0618
   Final validation loss: 0.0644
   Mean IoU (last 20 epochs): 0.915
   Max IoU observed: 0.923
   Final Dice score: 0.958
   Final pixel accuracy: 0.976
   Final sample statistics:
      Predicted foreground ratio: 0.187
      Ground-truth foreground ratio: 0.191
      Samples visualized: 12
   Saved plots: data/runs/segmentation_losses.png, data/runs/segmentation_quality.png
   Saved sample grid: data/runs/segmentation_samples_grid.png
Saved run artifact: data/runs/latest_segmentation_demo.json
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
