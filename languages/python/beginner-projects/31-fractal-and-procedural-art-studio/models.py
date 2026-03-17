"""
models.py - Data models for Project 31: Fractal And Procedural Art Studio
"""

from datetime import datetime
from typing import Any, Dict, List


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string."""
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def create_studio_config(
    canvas_width: int = 900,
    canvas_height: int = 600,
    max_iterations: int = 220,
    color_map: str = "magma",
    julia_real: float = -0.8,
    julia_imag: float = 0.156,
    noise_octaves: int = 5,
    noise_scale: float = 3.5,
    random_seed: int = 42,
    export_dpi: int = 140,
) -> Dict[str, Any]:
    """Create a validated fractal/procedural art configuration record."""
    width = max(320, int(canvas_width))
    height = max(240, int(canvas_height))
    return {
        "project_type": "fractal_procedural_art",
        "canvas_width": width,
        "canvas_height": height,
        "max_iterations": max(30, int(max_iterations)),
        "color_map": color_map.strip() or "magma",
        "julia_real": float(julia_real),
        "julia_imag": float(julia_imag),
        "noise_octaves": max(1, int(noise_octaves)),
        "noise_scale": max(0.5, float(noise_scale)),
        "random_seed": int(random_seed),
        "export_dpi": max(72, int(export_dpi)),
        "created_at": _utc_timestamp(),
    }


def create_artwork_metadata(
    artwork_id: str,
    title: str,
    style: str,
    width: int,
    height: int,
    generator: str,
    parameters: Dict[str, Any],
    statistics: Dict[str, float],
    image_file: str,
) -> Dict[str, Any]:
    """Create a persisted artwork metadata record."""
    return {
        "artwork_id": artwork_id,
        "title": title,
        "style": style,
        "resolution": f"{int(width)}x{int(height)}",
        "generator": generator,
        "parameters": parameters,
        "statistics": statistics,
        "image_file": image_file,
        "created_at": _utc_timestamp(),
    }


def create_run_summary(
    run_id: str,
    artworks_created: int,
    elapsed_ms: float,
    artifacts: Dict[str, str],
    gallery_preview: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Create a final run summary for reporting and persistence."""
    return {
        "run_id": run_id,
        "artworks_created": int(artworks_created),
        "elapsed_ms": float(elapsed_ms),
        "artifacts": artifacts,
        "gallery_preview": gallery_preview,
        "finished_at": _utc_timestamp(),
    }


def create_record(**kwargs: Any) -> Dict[str, Any]:
    """Backwards-compatible generic record factory."""
    return dict(kwargs)
