"""
operations.py - Business logic for Project 31: Fractal And Procedural Art Studio
"""

from __future__ import annotations

from datetime import datetime
import time
from typing import Any, Dict, List, Tuple

import numpy as np

from models import create_artwork_metadata, create_run_summary, create_studio_config
from storage import (
    OUTPUTS_DIR,
    ensure_data_dirs,
    load_artwork_catalog,
    load_run_catalog,
    save_artwork_record,
    save_run_record,
)


def _run_id() -> str:
    """Build a compact run ID from UTC timestamp."""
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def _normalize(values: np.ndarray) -> np.ndarray:
    min_value = float(values.min())
    max_value = float(values.max())
    if max_value - min_value < 1e-12:
        return np.zeros_like(values, dtype=float)
    return (values - min_value) / (max_value - min_value)


def _generate_mandelbrot(config: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, float]]:
    width = config['canvas_width']
    height = config['canvas_height']
    max_iter = config['max_iterations']

    x = np.linspace(-2.25, 0.8, width)
    y = np.linspace(-1.3, 1.3, height)
    c = x[None, :] + 1j * y[:, None]

    z = np.zeros_like(c)
    escaped = np.zeros(c.shape, dtype=bool)
    escape_time = np.full(c.shape, max_iter, dtype=int)

    for iteration in range(max_iter):
        active = ~escaped
        if not np.any(active):
            break
        z[active] = z[active] * z[active] + c[active]
        newly_escaped = (np.abs(z) > 2.0) & active
        escape_time[newly_escaped] = iteration
        escaped |= newly_escaped

    values = _normalize(escape_time.astype(float))
    stats = {
        'escape_ratio': float(escaped.mean()),
        'avg_escape_iter': float(escape_time.mean()),
        'contrast': float(values.std()),
    }
    return values, stats


def _generate_julia(config: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, float]]:
    width = config['canvas_width']
    height = config['canvas_height']
    max_iter = config['max_iterations']
    constant = complex(config['julia_real'], config['julia_imag'])

    x = np.linspace(-1.8, 1.8, width)
    y = np.linspace(-1.2, 1.2, height)
    z = x[None, :] + 1j * y[:, None]

    escaped = np.zeros(z.shape, dtype=bool)
    escape_time = np.full(z.shape, max_iter, dtype=int)

    for iteration in range(max_iter):
        active = ~escaped
        if not np.any(active):
            break
        z[active] = z[active] * z[active] + constant
        newly_escaped = (np.abs(z) > 2.0) & active
        escape_time[newly_escaped] = iteration
        escaped |= newly_escaped

    values = _normalize(escape_time.astype(float))
    stats = {
        'escape_ratio': float(escaped.mean()),
        'avg_escape_iter': float(escape_time.mean()),
        'contrast': float(values.std()),
    }
    return values, stats


def _value_noise_2d(width: int, height: int, scale: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    grid_x = max(2, int(width / (80 * scale)) + 2)
    grid_y = max(2, int(height / (80 * scale)) + 2)
    grid = rng.random((grid_y, grid_x))

    xs = np.linspace(0, grid_x - 1, width)
    ys = np.linspace(0, grid_y - 1, height)
    xi = np.floor(xs).astype(int)
    yi = np.floor(ys).astype(int)
    xf = xs - xi
    yf = ys - yi

    xi1 = np.clip(xi + 1, 0, grid_x - 1)
    yi1 = np.clip(yi + 1, 0, grid_y - 1)

    output = np.empty((height, width), dtype=float)
    for row in range(height):
        g00 = grid[yi[row], xi]
        g10 = grid[yi[row], xi1]
        g01 = grid[yi1[row], xi]
        g11 = grid[yi1[row], xi1]

        row_top = g00 * (1.0 - xf) + g10 * xf
        row_bottom = g01 * (1.0 - xf) + g11 * xf
        output[row] = row_top * (1.0 - yf[row]) + row_bottom * yf[row]
    return output


def _generate_procedural_clouds(config: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, float]]:
    width = config['canvas_width']
    height = config['canvas_height']
    octaves = config['noise_octaves']
    scale = config['noise_scale']
    seed = config['random_seed']

    amplitude = 1.0
    frequency = 1.0
    total_amplitude = 0.0
    texture = np.zeros((height, width), dtype=float)

    for octave in range(octaves):
        octave_noise = _value_noise_2d(
            width=width,
            height=height,
            scale=scale / frequency,
            seed=seed + octave * 97,
        )
        texture += octave_noise * amplitude
        total_amplitude += amplitude
        amplitude *= 0.55
        frequency *= 1.95

    texture = texture / max(total_amplitude, 1e-9)

    y_gradient = np.linspace(0.25, 1.0, height)[:, None]
    x_wave = (np.sin(np.linspace(0.0, 6.0 * np.pi, width))[None, :] + 1.0) * 0.11
    procedural = _normalize(texture * y_gradient + x_wave)

    stats = {
        'mean_intensity': float(procedural.mean()),
        'variance': float(procedural.var()),
        'contrast': float(procedural.std()),
    }
    return procedural, stats


def _save_art_image(
    values: np.ndarray,
    run_id: str,
    style_slug: str,
    title: str,
    color_map: str,
    export_dpi: int,
) -> str:
    image_path = OUTPUTS_DIR / f'art_{style_slug}_{run_id}.png'
    try:
        import matplotlib.pyplot as plt
    except Exception:
        fallback_path = OUTPUTS_DIR / f'art_{style_slug}_{run_id}.txt'
        fallback_path.write_text(
            'Matplotlib is unavailable.\n'
            f'Style: {style_slug}\n'
            f'Min: {values.min():.6f}\n'
            f'Max: {values.max():.6f}\n'
            f'Mean: {values.mean():.6f}\n',
            encoding='utf-8',
        )
        return str(fallback_path)

    height, width = values.shape
    plt.figure(figsize=(width / 120, height / 120))
    plt.imshow(values, cmap=color_map, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.tight_layout(pad=0)
    plt.savefig(image_path, dpi=export_dpi, bbox_inches='tight', pad_inches=0)
    plt.close()
    return str(image_path)


def load_studio_profile() -> Dict[str, Any]:
    """Build startup profile from previously saved runs and artworks."""
    runs = load_run_catalog()
    artworks = load_artwork_catalog()
    recent_styles = [item.get('style', '') for item in artworks[-8:] if item.get('style')]
    return {
        'catalog_file': 'data/runs.json',
        'art_catalog_file': 'data/artworks.json',
        'runs_stored': len(runs),
        'artworks_stored': len(artworks),
        'recent_styles': sorted(set(recent_styles)),
    }


def run_core_flow() -> Dict[str, Any]:
    """Generate a full artwork run and return a run summary."""
    ensure_data_dirs()
    config = create_studio_config()

    run_id = _run_id()
    started = time.perf_counter()

    generators = [
        (
            'mandelbrot',
            'Mandelbrot Basin',
            _generate_mandelbrot,
            {
                'plane_x': [-2.25, 0.8],
                'plane_y': [-1.3, 1.3],
                'max_iterations': config['max_iterations'],
            },
        ),
        (
            'julia',
            'Julia Drift',
            _generate_julia,
            {
                'constant': [config['julia_real'], config['julia_imag']],
                'max_iterations': config['max_iterations'],
            },
        ),
        (
            'procedural_clouds',
            'Procedural Cloudfield',
            _generate_procedural_clouds,
            {
                'noise_octaves': config['noise_octaves'],
                'noise_scale': config['noise_scale'],
                'seed': config['random_seed'],
            },
        ),
    ]

    gallery_preview: List[Dict[str, Any]] = []
    metadata_files: List[str] = []
    image_files: List[str] = []

    for index, (style, title, generator, params) in enumerate(generators, start=1):
        values, stats = generator(config)
        image_file = _save_art_image(
            values=values,
            run_id=run_id,
            style_slug=style,
            title=title,
            color_map=config['color_map'],
            export_dpi=config['export_dpi'],
        )

        artwork_id = f"{run_id}_{index:02d}_{style}"
        metadata = create_artwork_metadata(
            artwork_id=artwork_id,
            title=title,
            style=style,
            width=config['canvas_width'],
            height=config['canvas_height'],
            generator=generator.__name__,
            parameters=params,
            statistics={k: round(float(v), 6) for k, v in stats.items()},
            image_file=image_file,
        )
        metadata_file = save_artwork_record(metadata)

        image_files.append(image_file)
        metadata_files.append(metadata_file)
        gallery_preview.append(
            {
                'title': title,
                'style': style,
                'image_file': image_file,
                'contrast': metadata['statistics'].get('contrast', 0.0),
            }
        )

    elapsed_ms = (time.perf_counter() - started) * 1000.0
    summary = create_run_summary(
        run_id=run_id,
        artworks_created=len(gallery_preview),
        elapsed_ms=elapsed_ms,
        artifacts={
            'image_files': image_files,
            'metadata_files': metadata_files,
        },
        gallery_preview=gallery_preview,
    )
    summary['config'] = config

    run_file = save_run_record(summary)
    summary['artifacts']['run_file'] = run_file
    return summary
