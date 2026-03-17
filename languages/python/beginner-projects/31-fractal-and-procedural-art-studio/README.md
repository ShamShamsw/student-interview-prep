# Beginner Project 31: Fractal And Procedural Art Studio

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Fractal rendering, procedural noise synthesis, image export pipelines, and metadata tracking

---

## Why This Project?

Fractals and procedural textures are core techniques in creative coding, data art, and game visuals. This project helps you understand how deterministic math rules produce rich visual structures and how to turn those outputs into reusable artifacts with metadata.

This project teaches computational art workflows where you can:

- generate Mandelbrot fractals from complex-plane iteration,
- create Julia sets by varying complex constants,
- synthesize layered procedural textures using value-noise octaves,
- normalize and color-map generated scalar fields,
- export rendered images at configurable resolution and DPI,
- record per-artwork quality statistics (contrast, intensity, escape behavior),
- persist artwork metadata and run summaries to JSON,
- inspect historical catalogs of generated artwork,
- tune generation parameters for very different visual styles,
- and build a reproducible CLI art pipeline with deterministic seeds.

---

## Separate Repository

You can also access this project in a separate repository:

[Fractal And Procedural Art Studio Rep sitory](https://github.com/ShamShamsw/fractal-and-procedural-art-studio.git)

---

## What You Will Build

You will build a fractal and procedural art studio that:

1. Creates Mandelbrot-set visualizations using iterative escape-time computation.
2. Renders Julia-set variations from configurable complex constants.
3. Generates layered procedural cloud textures using octave-based value noise.
4. Normalizes generated scalar fields into display-ready image data.
5. Exports each generated artwork to PNG with a configurable colormap.
6. Tracks artwork-level metrics (contrast, intensity, and escape behavior).
7. Persists artwork metadata records to JSON files per render.
8. Maintains run and artwork catalogs for historical browsing.
9. Prints a readable terminal gallery preview for each session.
10. Produces reproducible outputs using fixed random seeds and parameter snapshots.

---

## Requirements

- Python 3.11+
- `numpy` (for vectorized fractal/noise computation)
- `matplotlib` (for rendering and image export)

Install with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
   FRACTAL AND PROCEDURAL ART STUDIO
======================================================================

Configuration:
   Project type:         fractal_procedural_art
   Canvas size:          900x600
   Max iterations:       220
   Color map:            magma
   Julia constant:       -0.800 +0.156i
   Noise octaves:        5
   Noise scale:          3.50
   Random seed:          42
   Export DPI:           140

Startup:
   Data directory:       data/
   Outputs directory:    data/outputs/
   Run catalog:          data/runs.json (loaded 0 runs)
   Artwork catalog:      data/artworks.json (loaded 0 artworks)
   Recent styles:        None yet

---

Run complete:
   Run ID:               20260316_234210
   Artworks created:     3
   Elapsed time:         974.84 ms

Generated gallery:
   #  | Style              | Contrast | Image File
   ---+--------------------+----------+--------------------------------------
    1 | mandelbrot         | 0.2841   | data/outputs/art_mandelbrot_20260316_234210.png
    2 | julia              | 0.2974   | data/outputs/art_julia_20260316_234210.png
    3 | procedural_clouds  | 0.1738   | data/outputs/art_procedural_clouds_20260316_234210.png

Artifacts saved:
   Run record:           data/outputs/run_20260316_234210.json
   Image exports:        3
   Metadata exports:     3
```

---

## Run

```bash
python main.py
```
