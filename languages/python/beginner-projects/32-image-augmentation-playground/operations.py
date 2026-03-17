"""
operations.py - Business logic for Project 32: Image Augmentation Playground
"""

from __future__ import annotations

from datetime import datetime
import time
from typing import Any, Callable, Dict, List, Tuple

import numpy as np

from models import (
    create_augmentation_record,
    create_evaluation_result,
    create_playground_config,
    create_run_summary,
)
from storage import (
    OUTPUTS_DIR,
    ensure_data_dirs,
    load_aug_catalog,
    load_run_catalog,
    save_aug_record,
    save_run_record,
)


def _run_id() -> str:
    """Build a compact run ID from UTC timestamp."""
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


# ── Synthetic image generators ──────────────────────────────────────────────

def _make_circle_image(
    width: int, height: int, rng: np.random.Generator, sample_id: int
) -> np.ndarray:
    """Solid circle on dark background — class 0 (red hue)."""
    img = np.zeros((height, width, 3), dtype=np.float32)
    radius = int(min(width, height) * (0.20 + 0.10 * ((sample_id * 7 + 3) % 5) / 4.0))
    cx = width // 2 + int((sample_id * 17 % 11 - 5) * width * 0.04)
    cy = height // 2 + int((sample_id * 13 % 9 - 4) * height * 0.04)
    y_grid, x_grid = np.ogrid[:height, :width]
    mask = (x_grid - cx) ** 2 + (y_grid - cy) ** 2 <= radius ** 2
    img[mask, 0] = 0.90
    img[mask, 1] = 0.10
    img[mask, 2] = 0.10
    return img


def _make_stripes_image(
    width: int, height: int, rng: np.random.Generator, sample_id: int
) -> np.ndarray:
    """Diagonal stripes — class 1 (blue hue)."""
    img = np.zeros((height, width, 3), dtype=np.float32)
    stripe_w = max(8, int(width * (0.08 + 0.04 * (sample_id % 4) / 3.0)))
    y_grid, x_grid = np.ogrid[:height, :width]
    mask = ((x_grid + y_grid) % (stripe_w * 2)) < stripe_w
    img[mask, 0] = 0.10
    img[mask, 1] = 0.10
    img[mask, 2] = 0.90
    return img


def _make_bars_image(
    width: int, height: int, rng: np.random.Generator, sample_id: int
) -> np.ndarray:
    """Horizontal bars — class 2 (green hue)."""
    img = np.zeros((height, width, 3), dtype=np.float32)
    bar_h = max(8, int(height * (0.10 + 0.04 * (sample_id % 4) / 3.0)))
    y_grid = np.arange(height)[:, None]
    mask = (y_grid % (bar_h * 2)) < bar_h
    img[np.broadcast_to(mask, (height, width)), 1] = 0.85
    img[np.broadcast_to(mask, (height, width)), 0] = 0.10
    img[np.broadcast_to(mask, (height, width)), 2] = 0.15
    return img


def _make_ring_image(
    width: int, height: int, rng: np.random.Generator, sample_id: int
) -> np.ndarray:
    """Concentric ring — class 3 (yellow hue)."""
    img = np.zeros((height, width, 3), dtype=np.float32)
    outer_r = int(min(width, height) * (0.32 + 0.06 * ((sample_id * 5 + 1) % 5) / 4.0))
    inner_r = int(outer_r * 0.55)
    cx = width // 2
    cy = height // 2
    y_grid, x_grid = np.ogrid[:height, :width]
    dist_sq = (x_grid - cx) ** 2 + (y_grid - cy) ** 2
    mask = (dist_sq <= outer_r ** 2) & (dist_sq >= inner_r ** 2)
    img[mask, 0] = 0.95
    img[mask, 1] = 0.85
    img[mask, 2] = 0.05
    return img


_GENERATORS: List[Callable] = [
    _make_circle_image,
    _make_stripes_image,
    _make_bars_image,
    _make_ring_image,
]
_CLASS_NAMES = ['circle', 'stripes', 'bars', 'ring']


def _generate_synthetic_dataset(
    config: Dict[str, Any],
) -> Tuple[np.ndarray, np.ndarray]:
    """Return (images, labels) arrays for the synthetic dataset.

    Images shape: (n_classes * num_samples, H, W, 3) float32 in [0, 1].
    Labels shape: (n_classes * num_samples,) int.
    Classes are grouped: [cls0 * n, cls1 * n, cls2 * n, cls3 * n].
    """
    rng = np.random.default_rng(config['random_seed'])
    width = config['image_width']
    height = config['image_height']
    n = config['num_samples']

    images: List[np.ndarray] = []
    labels: List[int] = []
    for class_id, gen_fn in enumerate(_GENERATORS):
        for sample_id in range(n):
            images.append(gen_fn(width, height, rng, sample_id))
            labels.append(class_id)

    return np.array(images, dtype=np.float32), np.array(labels, dtype=int)


# ── Augmentation operations ──────────────────────────────────────────────────

def _aug_horizontal_flip(img: np.ndarray, **_: Any) -> np.ndarray:
    return np.fliplr(img)


def _aug_brightness(
    img: np.ndarray, factor: float = 1.30, **_: Any
) -> np.ndarray:
    return np.clip(img * factor, 0.0, 1.0)


def _aug_contrast(
    img: np.ndarray, factor: float = 1.25, **_: Any
) -> np.ndarray:
    mean = float(img.mean())
    return np.clip((img - mean) * factor + mean, 0.0, 1.0)


def _aug_gaussian_noise(
    img: np.ndarray, sigma: float = 0.05, rng: Any = None, **_: Any
) -> np.ndarray:
    rng = rng if rng is not None else np.random.default_rng()
    return np.clip(
        img + rng.normal(0.0, sigma, img.shape).astype(np.float32),
        0.0,
        1.0,
    )


def _aug_salt_pepper(
    img: np.ndarray, density: float = 0.025, rng: Any = None, **_: Any
) -> np.ndarray:
    rng = rng if rng is not None else np.random.default_rng()
    mask = rng.random(img.shape[:2])
    result = img.copy()
    result[mask < density / 2] = 0.0
    result[mask > 1.0 - density / 2] = 1.0
    return result


def _bilinear_resize(img: np.ndarray, out_h: int, out_w: int) -> np.ndarray:
    """Resize img (H, W, C) float32 to (out_h, out_w, C) using bilinear interpolation."""
    in_h, in_w = img.shape[:2]
    src_y = np.arange(out_h, dtype=np.float64) * (in_h / out_h)
    src_x = np.arange(out_w, dtype=np.float64) * (in_w / out_w)

    y0 = np.clip(np.floor(src_y).astype(int), 0, in_h - 1)
    y1 = np.clip(y0 + 1, 0, in_h - 1)
    x0 = np.clip(np.floor(src_x).astype(int), 0, in_w - 1)
    x1 = np.clip(x0 + 1, 0, in_w - 1)

    yf = (src_y - y0)[:, None, None].astype(np.float32)   # (out_h, 1, 1)
    xf = (src_x - x0)[None, :, None].astype(np.float32)   # (1, out_w, 1)

    result = (
        img[y0][:, x0] * (1.0 - yf) * (1.0 - xf)
        + img[y0][:, x1] * (1.0 - yf) * xf
        + img[y1][:, x0] * yf * (1.0 - xf)
        + img[y1][:, x1] * yf * xf
    )
    return result.astype(img.dtype)


def _aug_crop_resize(
    img: np.ndarray, scale: float = 0.85, rng: Any = None, **_: Any
) -> np.ndarray:
    rng = rng if rng is not None else np.random.default_rng()
    h, w = img.shape[:2]
    ch = max(1, int(h * scale))
    cw = max(1, int(w * scale))
    y0 = int(rng.integers(0, h - ch + 1))
    x0 = int(rng.integers(0, w - cw + 1))
    cropped = img[y0: y0 + ch, x0: x0 + cw]
    return _bilinear_resize(cropped, h, w)


# ── Pipeline definitions ─────────────────────────────────────────────────────

_PIPELINES: Dict[str, List[Tuple[Callable[..., np.ndarray], Dict[str, Any]]]] = {
    'color_jitter': [
        (_aug_brightness, {'factor': 1.30}),
        (_aug_contrast, {'factor': 1.25}),
    ],
    'geometric': [
        (_aug_horizontal_flip, {}),
        (_aug_crop_resize, {'scale': 0.85}),
    ],
    'noise_injection': [
        (_aug_gaussian_noise, {'sigma': 0.05}),
        (_aug_salt_pepper, {'density': 0.025}),
    ],
    'combined': [
        (_aug_horizontal_flip, {}),
        (_aug_brightness, {'factor': 1.20}),
        (_aug_gaussian_noise, {'sigma': 0.04}),
    ],
}

_PIPELINE_LABELS: Dict[str, str] = {
    'color_jitter': 'brightness \u2192 contrast',
    'geometric': 'h_flip \u2192 crop_resize',
    'noise_injection': 'gaussian_noise \u2192 salt_pepper',
    'combined': 'h_flip \u2192 brightness \u2192 gaussian_noise',
}


def apply_pipeline(
    img: np.ndarray, name: str, rng: np.random.Generator
) -> np.ndarray:
    """Apply a named augmentation pipeline to a single image."""
    steps = _PIPELINES.get(name, [])
    result = img.copy()
    for fn, kwargs in steps:
        result = fn(result, rng=rng, **kwargs)
    return result


def compute_image_stats(img: np.ndarray) -> Dict[str, float]:
    """Compute per-image quality statistics."""
    brightness = float(img.mean())
    contrast = float(img.std())
    gy = float(np.abs(np.diff(img, axis=0)).mean())
    gx = float(np.abs(np.diff(img, axis=1)).mean())
    return {
        'mean_brightness': brightness,
        'contrast': contrast,
        'edge_density': (gx + gy) / 2.0,
    }


# ── Grid export ──────────────────────────────────────────────────────────────

def _save_comparison_grids(
    originals: List[np.ndarray],
    augmented_sets: Dict[str, List[np.ndarray]],
    run_id: str,
    config: Dict[str, Any],
) -> List[str]:
    """Save one before/after comparison PNG per pipeline."""
    grid_files: List[str] = []
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return grid_files

    num_samples = min(4, len(originals))
    for pipe_name, aug_images in augmented_sets.items():
        n_cols = num_samples * 2
        fig, axes = plt.subplots(
            1, n_cols, figsize=(n_cols * 2.6, 3.0), squeeze=False
        )
        ax_row = axes[0]
        for sample_idx in range(num_samples):
            ax_orig = ax_row[sample_idx * 2]
            ax_aug = ax_row[sample_idx * 2 + 1]
            ax_orig.imshow(originals[sample_idx], vmin=0.0, vmax=1.0)
            ax_orig.set_title(f'Original {_CLASS_NAMES[sample_idx]}', fontsize=7)
            ax_orig.axis('off')
            ax_aug.imshow(aug_images[sample_idx], vmin=0.0, vmax=1.0)
            ax_aug.set_title(f'Augmented', fontsize=7)
            ax_aug.axis('off')
        fig.suptitle(
            f'Pipeline: {pipe_name}  |  {_PIPELINE_LABELS[pipe_name]}', fontsize=9
        )
        plt.tight_layout()
        out_path = OUTPUTS_DIR / f'grid_{pipe_name}_{run_id}.png'
        plt.savefig(out_path, dpi=config['export_dpi'], bbox_inches='tight')
        plt.close()
        grid_files.append(str(out_path))

    return grid_files


# ── Classifier evaluation ─────────────────────────────────────────────────────

def _extract_features(img: np.ndarray) -> np.ndarray:
    """Extract channel-statistic feature vector from image."""
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    return np.array(
        [r.mean(), r.std(), g.mean(), g.std(), b.mean(), b.std()],
        dtype=np.float32,
    )


def _nearest_centroid_accuracy(
    train_imgs: np.ndarray,
    train_labels: np.ndarray,
    test_imgs: np.ndarray,
    test_labels: np.ndarray,
) -> float:
    """Train nearest-centroid classifier and return accuracy on test set."""
    classes = np.unique(train_labels)
    centroids: Dict[int, np.ndarray] = {}
    for c in classes:
        mask = train_labels == c
        feats = np.array([_extract_features(img) for img in train_imgs[mask]])
        centroids[int(c)] = feats.mean(axis=0)

    correct = 0
    for img, label in zip(test_imgs, test_labels):
        feat = _extract_features(img)
        pred = min(centroids, key=lambda c: float(np.linalg.norm(feat - centroids[c])))
        if pred == int(label):
            correct += 1
    return correct / len(test_labels) if len(test_labels) > 0 else 0.0


def _evaluate_classifier(
    images: np.ndarray,
    labels: np.ndarray,
    config: Dict[str, Any],
    rng: np.random.Generator,
) -> Dict[str, Any]:
    """Compare nearest-centroid accuracy with and without augmentation."""
    n_classes = len(_GENERATORS)
    n_per_class = config['num_samples']
    train_per_class = max(1, int(n_per_class * 0.75))

    train_idx: List[int] = []
    test_idx: List[int] = []
    for c in range(n_classes):
        class_idx = np.where(labels == c)[0]
        train_idx.extend(class_idx[:train_per_class].tolist())
        test_idx.extend(class_idx[train_per_class:].tolist())

    train_imgs = images[train_idx]
    train_labels = labels[train_idx]
    test_imgs = images[test_idx]
    test_labels = labels[test_idx]

    baseline_acc = _nearest_centroid_accuracy(
        train_imgs, train_labels, test_imgs, test_labels
    )

    aug_imgs: List[np.ndarray] = list(train_imgs)
    aug_labels: List[int] = list(train_labels)
    for _ in range(config['augmentation_rounds']):
        for img, lbl in zip(train_imgs, train_labels):
            aug_imgs.append(apply_pipeline(img, 'combined', rng))
            aug_labels.append(int(lbl))

    aug_imgs_arr = np.array(aug_imgs, dtype=np.float32)
    aug_labels_arr = np.array(aug_labels, dtype=int)
    augmented_acc = _nearest_centroid_accuracy(
        aug_imgs_arr, aug_labels_arr, test_imgs, test_labels
    )

    return create_evaluation_result(
        classifier='nearest-centroid',
        baseline_accuracy=baseline_acc,
        augmented_accuracy=augmented_acc,
        dataset_size_baseline=len(train_idx),
        dataset_size_augmented=len(aug_imgs),
        test_size=len(test_idx),
    )


# ── Profile loader ────────────────────────────────────────────────────────────

def load_playground_profile() -> Dict[str, Any]:
    """Return startup profile built from previously saved catalogs."""
    runs = load_run_catalog()
    augs = load_aug_catalog()
    recent_pipelines = [
        item.get('pipeline_name', '')
        for item in augs[-8:]
        if item.get('pipeline_name')
    ]
    return {
        'catalog_file': 'data/runs.json',
        'aug_catalog_file': 'data/augmentations.json',
        'runs_stored': len(runs),
        'augs_stored': len(augs),
        'recent_pipelines': sorted(set(recent_pipelines)),
    }


# ── Core flow ─────────────────────────────────────────────────────────────────

def run_core_flow() -> Dict[str, Any]:
    """Run one complete augmentation session and return a run summary."""
    ensure_data_dirs()
    config = create_playground_config()
    rng = np.random.default_rng(config['random_seed'])

    run_id = _run_id()
    started = time.perf_counter()

    images, labels = _generate_synthetic_dataset(config)

    # One representative sample per class (first sample of each class)
    n = config['num_samples']
    original_samples = [images[class_id * n] for class_id in range(len(_GENERATORS))]

    pipeline_names = list(_PIPELINES.keys())
    augmented_sets: Dict[str, List[np.ndarray]] = {}
    pipeline_previews: List[Dict[str, Any]] = []
    metadata_files: List[str] = []

    for pipe_name in pipeline_names:
        pipe_rng = np.random.default_rng(
            config['random_seed'] + abs(hash(pipe_name)) % 10_000
        )
        aug_samples = [
            apply_pipeline(img, pipe_name, pipe_rng) for img in original_samples
        ]
        augmented_sets[pipe_name] = aug_samples

        orig_stats_list = [compute_image_stats(img) for img in original_samples]
        aug_stats_list = [compute_image_stats(img) for img in aug_samples]
        avg_orig = {
            k: float(np.mean([s[k] for s in orig_stats_list]))
            for k in orig_stats_list[0]
        }
        avg_aug = {
            k: float(np.mean([s[k] for s in aug_stats_list]))
            for k in aug_stats_list[0]
        }

        record = create_augmentation_record(
            aug_id=f'{pipe_name}_{run_id}',
            pipeline_name=pipe_name,
            operations=_PIPELINE_LABELS[pipe_name].split(' \u2192 '),
            original_stats=avg_orig,
            augmented_stats=avg_aug,
            grid_file='',
        )
        pipeline_previews.append(
            {
                'pipeline_name': pipe_name,
                'operations_label': _PIPELINE_LABELS[pipe_name],
                'delta_brightness': avg_aug['mean_brightness'] - avg_orig['mean_brightness'],
                'delta_contrast': avg_aug['contrast'] - avg_orig['contrast'],
            }
        )
        metadata_files.append(save_aug_record(record))

    grid_files = _save_comparison_grids(original_samples, augmented_sets, run_id, config)

    evaluation: Dict[str, Any] = {}
    if config['evaluate_classifier']:
        evaluation = _evaluate_classifier(images, labels, config, rng)

    elapsed_ms = (time.perf_counter() - started) * 1000.0

    artifacts: Dict[str, Any] = {
        'run_file': str(OUTPUTS_DIR / f'run_{run_id}.json'),
        'grid_files': grid_files,
        'metadata_files': metadata_files,
    }

    summary = create_run_summary(
        run_id=run_id,
        pipelines_applied=len(pipeline_names),
        grids_exported=len(grid_files),
        elapsed_ms=elapsed_ms,
        artifacts=artifacts,
        pipeline_previews=pipeline_previews,
        evaluation=evaluation,
    )

    save_run_record(summary)
    return summary

