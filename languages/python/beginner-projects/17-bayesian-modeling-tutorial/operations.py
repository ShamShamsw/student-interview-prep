"""
operations.py - Bayesian inference engine and analysis workflows
===============================================================

Implements:
    - Beta-Binomial conjugate prior update
    - Posterior summary statistics computation
    - Prior sensitivity analysis across named presets
    - Posterior predictive distribution via Monte Carlo
"""

from __future__ import annotations

import numpy as np
from scipy import stats

from models import (
    create_beta_params,
    create_inference_result,
    create_posterior_metrics,
    create_project_config,
)
from storage import save_latest_session


def load_prior_presets() -> dict:
    """Return named prior configurations for sensitivity analysis.

    Returns:
        dict: Preset name mapped to alpha, beta, and description.
    """
    return {
        "uniform": {
            "alpha": 1.0,
            "beta": 1.0,
            "description": "Uniform prior - no prior belief",
        },
        "weakly_informative": {
            "alpha": 2.0,
            "beta": 2.0,
            "description": "Weakly informative - slight fair-coin belief",
        },
        "strong_fair_coin": {
            "alpha": 10.0,
            "beta": 10.0,
            "description": "Strong fair-coin belief (p near 0.5)",
        },
        "biased_high": {
            "alpha": 5.0,
            "beta": 2.0,
            "description": "Prior belief coin is biased toward heads",
        },
        "jeffreys": {
            "alpha": 0.5,
            "beta": 0.5,
            "description": "Jeffreys prior - non-informative reference prior",
        },
    }


def compute_conjugate_posterior(
    prior_alpha: float,
    prior_beta: float,
    n_heads: int,
    n_trials: int,
) -> dict:
    """Compute the analytical Beta-Binomial conjugate posterior.

    With a Beta(alpha, beta) prior and a Binomial likelihood with n_heads
    successes in n_trials trials, the posterior is:
        Beta(alpha + n_heads, beta + n_trials - n_heads)

    Parameters:
        prior_alpha (float): Alpha parameter of Beta prior.
        prior_beta (float): Beta parameter of Beta prior.
        n_heads (int): Observed number of heads (successes).
        n_trials (int): Total number of coin flips (trials).

    Returns:
        dict: Posterior Beta distribution parameters.
    """
    post_alpha = prior_alpha + n_heads
    post_beta = prior_beta + (n_trials - n_heads)
    return create_beta_params(alpha=post_alpha, beta=post_beta, label="posterior")


def compute_posterior_metrics(
    posterior_alpha: float,
    posterior_beta: float,
    ci_level: float = 0.95,
) -> dict:
    """Compute summary statistics for a Beta posterior distribution.

    Parameters:
        posterior_alpha (float): Posterior alpha parameter.
        posterior_beta (float): Posterior beta parameter.
        ci_level (float): Credible interval probability level.

    Returns:
        dict: Posterior summary statistics.
    """
    dist = stats.beta(posterior_alpha, posterior_beta)
    mean = dist.mean()
    variance = dist.var()
    std = dist.std()

    # Mode is (alpha - 1) / (alpha + beta - 2) when both alpha, beta > 1
    if posterior_alpha > 1 and posterior_beta > 1:
        mode = (posterior_alpha - 1) / (posterior_alpha + posterior_beta - 2)
    else:
        mode = float("nan")

    lower_tail = (1.0 - ci_level) / 2.0
    ci_lower, ci_upper = dist.ppf([lower_tail, 1.0 - lower_tail])

    return create_posterior_metrics(
        mean=float(mean),
        mode=float(mode),
        variance=float(variance),
        std=float(std),
        ci_lower=float(ci_lower),
        ci_upper=float(ci_upper),
        ci_level=ci_level,
    )


def run_prior_sensitivity(config: dict, presets: dict) -> list[dict]:
    """Run inference under multiple named priors and return comparison results.

    Parameters:
        config (dict): Base inference configuration.
        presets (dict): Named prior presets from load_prior_presets().

    Returns:
        list[dict]: Inference result for each prior preset.
    """
    results = []
    for preset_name, preset_info in presets.items():
        prior_params = create_beta_params(
            alpha=preset_info["alpha"],
            beta=preset_info["beta"],
            label=preset_name,
        )
        posterior_params = compute_conjugate_posterior(
            prior_alpha=preset_info["alpha"],
            prior_beta=preset_info["beta"],
            n_heads=config["n_heads"],
            n_trials=config["n_trials"],
        )
        metrics = compute_posterior_metrics(
            posterior_alpha=posterior_params["alpha"],
            posterior_beta=posterior_params["beta"],
        )
        result = create_inference_result(
            config=config,
            prior_params=prior_params,
            posterior_params=posterior_params,
            metrics=metrics,
        )
        result["preset_name"] = preset_name
        result["preset_description"] = preset_info["description"]
        results.append(result)

    return results


def generate_posterior_predictive(
    posterior_alpha: float,
    posterior_beta: float,
    future_trials: int = 20,
    n_samples: int = 10000,
    rng: np.random.Generator | None = None,
) -> dict:
    """Sample from the posterior predictive distribution.

    Draws p from the posterior Beta distribution, then simulates future
    coin flips from Binomial(future_trials, p).

    Parameters:
        posterior_alpha (float): Posterior alpha parameter.
        posterior_beta (float): Posterior beta parameter.
        future_trials (int): Number of future coin flips to predict.
        n_samples (int): Number of Monte Carlo samples.
        rng (np.random.Generator | None): Random generator for reproducibility.

    Returns:
        dict: Posterior predictive summary statistics.
    """
    if rng is None:
        rng = np.random.default_rng()

    p_samples = rng.beta(posterior_alpha, posterior_beta, size=n_samples)
    count_samples = rng.binomial(future_trials, p_samples)

    return {
        "future_trials": future_trials,
        "n_samples": n_samples,
        "predicted_mean_heads": float(np.mean(count_samples)),
        "predicted_std": float(np.std(count_samples)),
        "predicted_95ci_lower": float(np.percentile(count_samples, 2.5)),
        "predicted_95ci_upper": float(np.percentile(count_samples, 97.5)),
    }


def run_core_flow(config: dict | None = None) -> dict:
    """Execute the main Bayesian inference workflow.

    Parameters:
        config (dict | None): Override default configuration. If None, uses default.

    Returns:
        dict: Session summary with inference results and metadata.
    """
    if config is None:
        config = create_project_config()

    rng = np.random.default_rng(config.get("seed", 42))

    # Define prior from config
    prior_params = create_beta_params(
        alpha=config["prior_alpha"],
        beta=config["prior_beta"],
        label="prior",
    )

    # Compute analytical conjugate posterior
    posterior_params = compute_conjugate_posterior(
        prior_alpha=config["prior_alpha"],
        prior_beta=config["prior_beta"],
        n_heads=config["n_heads"],
        n_trials=config["n_trials"],
    )

    # Compute posterior summary statistics
    metrics = compute_posterior_metrics(
        posterior_alpha=posterior_params["alpha"],
        posterior_beta=posterior_params["beta"],
    )

    # Build base result
    base_result = create_inference_result(
        config=config,
        prior_params=prior_params,
        posterior_params=posterior_params,
        metrics=metrics,
    )

    # Run prior sensitivity analysis
    presets = load_prior_presets()
    sensitivity_results = run_prior_sensitivity(config, presets)

    # Posterior predictive
    predictive = generate_posterior_predictive(
        posterior_alpha=posterior_params["alpha"],
        posterior_beta=posterior_params["beta"],
        future_trials=20,
        n_samples=config.get("n_posterior_samples", 10000),
        rng=rng,
    )

    # Build session summary
    session_summary = {
        "status": "completed",
        "config": config,
        "base_result": base_result,
        "sensitivity_results": sensitivity_results,
        "posterior_predictive": predictive,
    }

    # Persist results
    save_latest_session(session_summary)

    return session_summary
