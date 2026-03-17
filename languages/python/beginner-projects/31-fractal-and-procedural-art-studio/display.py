"""
display.py - Presentation helpers for Project 31: Fractal And Procedural Art Studio
"""

from typing import Any, Dict, List


def format_header() -> str:
    """Format session header banner."""
    return (
        "=" * 70
        + "\n"
        + "   FRACTAL AND PROCEDURAL ART STUDIO\n"
        + "=" * 70
    )


def format_startup_guide(config: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """Format startup configuration and historical profile."""
    recent_styles = ', '.join(profile.get('recent_styles', [])) or 'None yet'
    lines = [
        '',
        'Configuration:',
        f"   Project type:         {config['project_type']}",
        f"   Canvas size:          {config['canvas_width']}x{config['canvas_height']}",
        f"   Max iterations:       {config['max_iterations']}",
        f"   Color map:            {config['color_map']}",
        f"   Julia constant:       {config['julia_real']:+.3f} {config['julia_imag']:+.3f}i",
        f"   Noise octaves:        {config['noise_octaves']}",
        f"   Noise scale:          {config['noise_scale']:.2f}",
        f"   Random seed:          {config['random_seed']}",
        f"   Export DPI:           {config['export_dpi']}",
        '',
        'Startup:',
        '   Data directory:       data/',
        '   Outputs directory:    data/outputs/',
        f"   Run catalog:          {profile['catalog_file']} (loaded {profile['runs_stored']} runs)",
        f"   Artwork catalog:      {profile['art_catalog_file']} (loaded {profile['artworks_stored']} artworks)",
        f'   Recent styles:        {recent_styles}',
        '',
        '---',
    ]
    return '\n'.join(lines)


def format_gallery_preview(gallery_preview: List[Dict[str, Any]]) -> str:
    """Format compact artwork preview table."""
    if not gallery_preview:
        return 'No artworks generated.'

    lines = [
        'Generated gallery:',
        '   #  | Style              | Contrast | Image File',
        '   ---+--------------------+----------+--------------------------------------',
    ]
    for index, item in enumerate(gallery_preview, start=1):
        lines.append(
            '   '
            f"{index:>2} | "
            f"{item['style'][:18]:<18} | "
            f"{float(item.get('contrast', 0.0)):.4f}   | "
            f"{item['image_file']}"
        )
    return '\n'.join(lines)


def format_run_report(summary: Dict[str, Any]) -> str:
    """Format final run report."""
    lines = [
        '',
        'Run complete:',
        f"   Run ID:               {summary['run_id']}",
        f"   Artworks created:     {summary['artworks_created']}",
        f"   Elapsed time:         {summary['elapsed_ms']:.2f} ms",
        '',
        format_gallery_preview(summary.get('gallery_preview', [])),
        '',
        'Artifacts saved:',
        f"   Run record:           {summary['artifacts'].get('run_file', 'N/A')}",
        f"   Image exports:        {len(summary['artifacts'].get('image_files', []))}",
        f"   Metadata exports:     {len(summary['artifacts'].get('metadata_files', []))}",
    ]
    return '\n'.join(lines)


def format_message(message: str) -> str:
    """Format a user-facing message string."""
    return f'[Project 31] {message}'
