"""
display.py - Output formatting for Bayesian Modeling Tutorial
=============================================================

Provides:
    - CLI banners and headers
    - Configuration display
    - Inference result formatting
    - Session report generation
"""


def format_header() -> str:
    """Return the CLI banner for this project.

    Returns:
        str: User-facing banner string.
    """
    return (
        "=" * 70
        + "\n"
        + "  BAYESIAN MODELING TUTORIAL - BETA-BINOMIAL COIN INFERENCE\n"
        + "=" * 70
    )


def format_startup_guide(config: dict, presets: dict) -> str:
    """Return startup guidance shown before inference begins.

    Parameters:
        config (dict): Runtime configuration.
        presets (dict): Named prior presets.

    Returns:
        str: Multi-line startup guide.
    """
    observed_tails = config["n_trials"] - config["n_heads"]
    mle = config["n_heads"] / config["n_trials"] if config["n_trials"] > 0 else 0.0

    lines = [
        "",
        "Configuration:",
        f"  Observed flips:   {config['n_trials']} total "
        f"({config['n_heads']} heads, {observed_tails} tails)",
        f"  Maximum likelihood estimate (p): {mle:.3f}",
        f"  Prior: Beta({config['prior_alpha']}, {config['prior_beta']})",
        f"  Posterior samples: {config.get('n_posterior_samples', 10000)}",
        f"  Random seed: {config.get('seed', 42)}",
        "",
        "Available prior presets for sensitivity analysis:",
    ]

    for preset_name, preset_info in presets.items():
        a = preset_info["alpha"]
        b = preset_info["beta"]
        desc = preset_info["description"]
        lines.append(f"  - {preset_name}: Beta({a}, {b}) - {desc}")

    lines.extend(
        [
            "",
            "Session behavior:",
            "  1) Specify prior Beta distribution for coin-flip probability p.",
            "  2) Compute analytical conjugate posterior after observing data.",
            "  3) Summarize posterior: mean, mode, 95% credible interval.",
            "  4) Run prior sensitivity analysis across named presets.",
            "  5) Generate posterior predictive distribution for future flips.",
        ]
    )
    return "\n".join(lines)


def _format_posterior_metrics(metrics: dict) -> list[str]:
    """Return readable posterior statistics.

    Parameters:
        metrics (dict): Computed posterior summary statistics.

    Returns:
        list[str]: Formatted metric lines.
    """
    if not metrics:
        return ["  Posterior metrics: no data"]

    ci_pct = int(metrics.get("ci_level", 0.95) * 100)
    mode_val = metrics.get("mode", float("nan"))
    mode_str = f"{mode_val:.4f}" if mode_val == mode_val else "N/A"

    return [
        f"  Posterior mean: {metrics['mean']:.4f}",
        f"  Posterior mode (MAP): {mode_str}",
        f"  Posterior std: {metrics['std']:.4f}",
        f"  {ci_pct}% credible interval: [{metrics['ci_lower']:.4f}, {metrics['ci_upper']:.4f}]",
    ]


def _format_sensitivity_summary(sensitivity_results: list[dict]) -> list[str]:
    """Return formatted summary of prior sensitivity results.

    Parameters:
        sensitivity_results (list[dict]): Results from prior sensitivity analysis.

    Returns:
        list[str]: Summary lines.
    """
    if not sensitivity_results:
        return ["  Prior sensitivity: not performed"]

    lines = [f"  Prior sensitivity analysis: {len(sensitivity_results)} priors tested"]
    for result in sensitivity_results:
        name = result.get("preset_name", "unknown")
        mean = result.get("metrics", {}).get("mean", float("nan"))
        ci_lo = result.get("metrics", {}).get("ci_lower", float("nan"))
        ci_hi = result.get("metrics", {}).get("ci_upper", float("nan"))
        lines.append(
            f"    {name:22s}: mean={mean:.4f}  95%CI=[{ci_lo:.4f}, {ci_hi:.4f}]"
        )
    return lines


def _format_predictive_summary(predictive: dict) -> list[str]:
    """Return formatted posterior predictive summary.

    Parameters:
        predictive (dict): Posterior predictive simulation results.

    Returns:
        list[str]: Summary lines.
    """
    if not predictive:
        return ["  Posterior predictive: not computed"]

    return [
        f"  Posterior predictive ({predictive['future_trials']} future flips):",
        f"    Expected heads: {predictive['predicted_mean_heads']:.1f}"
        f" +/- {predictive['predicted_std']:.1f}",
        f"    95% predictive interval: [{predictive['predicted_95ci_lower']:.0f},"
        f" {predictive['predicted_95ci_upper']:.0f}]",
    ]


def format_run_report(summary: dict) -> str:
    """Return formatted session report for display.

    Parameters:
        summary (dict): Complete session summary.

    Returns:
        str: Formatted multi-line report.
    """
    lines = ["", "Session summary:"]
    lines.append(f"  Status: {summary.get('status', 'unknown')}")

    config = summary.get("config", {})
    lines.append(
        f"  Data: {config.get('n_trials', 0)} flips, "
        f"{config.get('n_heads', 0)} heads"
    )

    base_result = summary.get("base_result", {})
    metrics = base_result.get("metrics", {})
    post = base_result.get("posterior", {})

    if post:
        lines.append(
            f"  Posterior: Beta({post.get('alpha', 0):.1f}, {post.get('beta', 0):.1f})"
        )
    lines.extend(_format_posterior_metrics(metrics))

    sensitivity = summary.get("sensitivity_results", [])
    lines.extend(_format_sensitivity_summary(sensitivity))

    predictive = summary.get("posterior_predictive", {})
    lines.extend(_format_predictive_summary(predictive))

    lines.extend(
        [
            "  Saved plots: data/runs/prior_posterior.png, data/runs/sensitivity.png",
            "Saved run artifact: data/runs/latest_bayesian_inference.json",
            "",
        ]
    )

    return "\n".join(lines)


def format_message(message: str) -> str:
    """Format a user-facing message string.

    Parameters:
        message (str): Raw message text.

    Returns:
        str: Prefixed message string.
    """
    return f"[Bayesian] {message}"
