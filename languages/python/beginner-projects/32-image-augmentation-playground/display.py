"""
display.py - Presentation helpers for Project 32: Image Augmentation Playground
"""

from typing import Any, Dict, List


def format_header() -> str:
    """Format session header banner."""
    return (
        "=" * 70
        + "\n"
        + "   IMAGE AUGMENTATION PLAYGROUND\n"
        + "=" * 70
    )


def format_startup_guide(config: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """Format startup configuration and historical profile."""
    recent = ', '.join(profile.get('recent_pipelines', [])) or 'None yet'
    lines = [
        '',
        'Configuration:',
        f"   Project type:         {config['project_type']}",
        f"   Image size:           {config['image_width']}x{config['image_height']}",
        f"   Samples per class:    {config['num_samples']}",
        '   Classes:              4 (circle, stripes, bars, ring)',
        f"   Augmentation rounds:  {config['augmentation_rounds']}",
        f"   Color mode:           {config['color_mode']}",
        f"   Random seed:          {config['random_seed']}",
        f"   Export DPI:           {config['export_dpi']}",
        f"   Evaluate classifier:  {config['evaluate_classifier']}",
        '',
        'Startup:',
        '   Data directory:       data/',
        '   Outputs directory:    data/outputs/',
        f"   Run catalog:          {profile['catalog_file']} (loaded {profile['runs_stored']} runs)",
        f"   Aug catalog:          {profile['aug_catalog_file']} (loaded {profile['augs_stored']} records)",
        f'   Recent pipelines:     {recent}',
        '',
        '---',
    ]
    return '\n'.join(lines)


def format_pipeline_table(pipeline_previews: List[Dict[str, Any]]) -> str:
    """Format augmentation pipeline results as a comparison table."""
    if not pipeline_previews:
        return 'No pipelines applied.'
    lines = [
        'Augmentation pipelines:',
        '   Pipeline            | Operations                             | \u0394 Brightness | \u0394 Contrast',
        '   --------------------+----------------------------------------+--------------+-----------',
    ]
    for item in pipeline_previews:
        lines.append(
            '   '
            f"{item['pipeline_name'][:20]:<20}| "
            f"{item['operations_label'][:38]:<38} | "
            f"   {item['delta_brightness']:+.4f}   | "
            f"   {item['delta_contrast']:+.4f}"
        )
    return '\n'.join(lines)


def format_evaluation_report(evaluation: Dict[str, Any]) -> str:
    """Format classifier evaluation comparison table."""
    if not evaluation:
        return ''
    n_train_base = evaluation.get('dataset_size_baseline', 0)
    n_train_aug = evaluation.get('dataset_size_augmented', 0)
    n_test = evaluation.get('test_size', 0)
    base_acc = evaluation.get('baseline_accuracy', 0.0) * 100
    aug_acc = evaluation.get('augmented_accuracy', 0.0) * 100
    delta_acc = evaluation.get('accuracy_delta', 0.0) * 100
    delta_train = n_train_aug - n_train_base

    rounds = int(round(n_train_aug / max(n_train_base, 1))) - 1
    aug_label = f'Augmented (+{rounds}x aug)'

    def _row(setting: str, train: str, test: str, acc_str: str) -> str:
        return f"   {setting:<21}| {train:>13} | {test:>13} | {acc_str}"

    lines = [
        '',
        'Classifier evaluation (nearest-centroid, channel-statistic features):',
        '   Setting              | Train samples | Test samples  | Accuracy',
        '   ---------------------+---------------+---------------+---------',
        _row('Baseline (no aug)', str(n_train_base), str(n_test), f"  {base_acc:>5.1f}%"),
        _row(aug_label, str(n_train_aug), str(n_test), f"  {aug_acc:>5.1f}%"),
        _row('Delta', f'+{delta_train}', '--', f"  {delta_acc:>+5.1f}%"),
    ]
    return '\n'.join(lines)


def format_run_report(summary: Dict[str, Any]) -> str:
    """Format final run report."""
    artifacts = summary.get('artifacts', {})
    grid_files = artifacts.get('grid_files', [])
    metadata_files = artifacts.get('metadata_files', [])
    lines = [
        '',
        'Run complete:',
        f"   Run ID:               {summary['run_id']}",
        f"   Pipelines applied:    {summary['pipelines_applied']}",
        f"   Grids exported:       {summary['grids_exported']}",
        f"   Elapsed time:         {summary['elapsed_ms']:.2f} ms",
        '',
        format_pipeline_table(summary.get('pipeline_previews', [])),
        format_evaluation_report(summary.get('evaluation', {})),
        '',
        'Artifacts saved:',
        f"   Run record:           {artifacts.get('run_file', 'N/A')}",
        f"   Grid exports:         {len(grid_files)}",
        f"   Metadata exports:     {len(metadata_files)}",
    ]
    return '\n'.join(lines)


def format_message(message: str) -> str:
    """Format a user-facing message string."""
    return f'[Project 32] {message}'

