"""Presentation helpers for Project 42: Hand-Pose Sign Language Classifier."""

from typing import Any, Dict, List


def format_header() -> str:
    """Format session header banner."""
    return '=' * 70 + '\n' + '   HAND-POSE SIGN LANGUAGE CLASSIFIER\n' + '=' * 70


def format_startup_guide(config: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """Format startup configuration and historical profile."""
    recent = ', '.join(profile.get('recent_samples', [])) or 'None yet'
    lines = [
        '',
        'Configuration:',
        f"   Project type:           {config['project_type']}",
        f"   Sign vocabulary:        {', '.join(config['signs'])}",
        f"   Landmarks per hand:     {config['landmarks_per_hand']}",
        f"   Capture samples/sign:   {config['capture_samples_per_sign']}",
        f"   Training split:         {config['train_split']:.0%}",
        f"   Live demo frames:       {config['live_frames']}",
        f"   Low-confidence cutoff:  {config['low_confidence_threshold']:.2f}",
        f"   Confusion matrix:       {config['include_confusion_matrix']}",
        f"   Confidence timeline:    {config['include_confidence_timeline']}",
        f"   Max predictions report: {config['max_predictions_in_report']}",
        f"   Random seed:            {config['random_seed']}",
        '',
        'Startup:',
        '   Data directory:         data/',
        '   Outputs directory:      data/outputs/',
        (
            f"   Template library:       {profile['library_file']} "
            f"(loaded {profile['templates_available']} signs)"
        ),
        (
            f"   Run catalog:            {profile['catalog_file']} "
            f"(loaded {profile['runs_stored']} runs)"
        ),
        (
            f"   Dataset catalog:        {profile['dataset_file']} "
            f"(loaded {profile['samples_stored']} samples)"
        ),
        f"   Recent samples:         {recent}",
        '',
        '---',
    ]
    return '\n'.join(lines)


def format_prediction_table(prediction_previews: List[Dict[str, Any]]) -> str:
    """Format live prediction preview table."""
    if not prediction_previews:
        return 'No live predictions generated.'
    lines = [
        'Prediction previews:',
        '   Frame          | Expected | Predicted | Confidence | Low conf',
        '   ---------------+----------+-----------+------------+---------',
    ]
    for prediction in prediction_previews:
        lines.append(
            '   '
            f"{prediction['frame_id'][:13]:<13} | "
            f"{prediction['expected_label'][:8]:<8} | "
            f"{prediction['predicted_label'][:9]:<9} | "
            f"{prediction['confidence']:<10.2%} | "
            f"{'yes' if prediction['is_low_confidence'] else 'no'}"
        )
    return '\n'.join(lines)


def format_run_report(summary: Dict[str, Any]) -> str:
    """Format final session report."""
    artifacts = summary.get('artifacts', {})
    metrics = summary.get('metrics', {})
    lines = [
        '',
        'Session complete:',
        f"   Session ID:             {summary['session_id']}",
        f"   Signs modeled:          {summary['signs_modeled']}",
        f"   Captures generated:     {summary['captures_total']}",
        f"   Training samples:       {summary['training_samples']}",
        f"   Test samples:           {summary['test_samples']}",
        f"   Test accuracy:          {summary['test_accuracy']:.1%}",
        f"   Live frames:            {summary['live_frames']}",
        f"   Low-confidence frames:  {summary['low_confidence_frames']}",
        f"   Elapsed time:           {summary['elapsed_ms']:.2f} ms",
        '',
        (
            f"Classifier metrics: "
            f"macro_accuracy={metrics.get('macro_accuracy', 0.0):.1%} | "
            f"avg_live_confidence={metrics.get('avg_live_confidence', 0.0):.1%} | "
            f"feature_dimension={metrics.get('feature_dimension', 0)} | "
            f"classifier={metrics.get('classifier_type', 'N/A')}"
        ),
        '',
        format_prediction_table(summary.get('prediction_previews', [])),
        '',
        'Artifacts saved:',
        f"   Run record:             {artifacts.get('session_file', 'N/A')}",
        f"   Model file:             {artifacts.get('model_file', 'N/A')}",
        f"   Live inference file:    {artifacts.get('live_file', 'N/A')}",
        f"   Confusion matrix:       {artifacts.get('confusion_matrix_file', 'N/A')}",
        f"   Confidence timeline:    {artifacts.get('confidence_timeline_file', 'N/A')}",
        f"   Total captures logged:  {artifacts.get('capture_count', 0)}",
    ]
    return '\n'.join(lines)


def format_message(message: str) -> str:
    """Format a user-facing message string."""
    return f'[Project 42] {message}'
