"""
models.py - Data models for Bayesian Modeling Tutorial
======================================================

Defines:
    - Model configuration for Beta-Binomial inference
    - Prior and posterior parameter containers
    - Inference results and posterior metrics
"""

from datetime import datetime


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp.

    Returns:
        str: Timestamp string with trailing Z.
    """
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def create_project_config(
    n_trials: int = 50,
    n_heads: int = 30,
    prior_alpha: float = 1.0,
    prior_beta: float = 1.0,
    n_posterior_samples: int = 10000,
    seed: int = 42,
) -> dict:
    """Create the default runtime configuration for Bayesian inference.

    Parameters:
        n_trials (int): Total number of coin flips observed.
        n_heads (int): Number of heads observed.
        prior_alpha (float): Alpha parameter of Beta prior.
        prior_beta (float): Beta parameter of Beta prior.
        n_posterior_samples (int): Number of samples to draw from posterior.
        seed (int): Random seed for reproducibility.

    Returns:
        dict: Configuration dictionary.
    """
    return {
        "n_trials": n_trials,
        "n_heads": n_heads,
        "prior_alpha": prior_alpha,
        "prior_beta": prior_beta,
        "n_posterior_samples": n_posterior_samples,
        "seed": seed,
        "created_at": _utc_timestamp(),
    }


def create_beta_params(alpha: float, beta: float, label: str = "") -> dict:
    """Create a Beta distribution parameter container.

    Parameters:
        alpha (float): Alpha (success) concentration parameter.
        beta (float): Beta (failure) concentration parameter.
        label (str): Optional human-readable label.

    Returns:
        dict: Beta distribution parameters.
    """
    return {
        "alpha": alpha,
        "beta": beta,
        "label": label,
    }


def create_posterior_metrics(
    mean: float,
    mode: float,
    variance: float,
    std: float,
    ci_lower: float,
    ci_upper: float,
    ci_level: float,
) -> dict:
    """Create a summary of posterior distribution statistics.

    Parameters:
        mean (float): Posterior mean.
        mode (float): Posterior mode (MAP estimate).
        variance (float): Posterior variance.
        std (float): Posterior standard deviation.
        ci_lower (float): Lower credible interval bound.
        ci_upper (float): Upper credible interval bound.
        ci_level (float): Credible interval probability level (e.g. 0.95).

    Returns:
        dict: Posterior summary statistics.
    """
    return {
        "mean": mean,
        "mode": mode,
        "variance": variance,
        "std": std,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "ci_level": ci_level,
    }


def create_inference_result(
    config: dict,
    prior_params: dict,
    posterior_params: dict,
    metrics: dict,
) -> dict:
    """Create a complete inference result.

    Parameters:
        config (dict): Original inference configuration.
        prior_params (dict): Prior Beta distribution parameters.
        posterior_params (dict): Posterior Beta distribution parameters.
        metrics (dict): Computed posterior statistics.

    Returns:
        dict: Complete inference result.
    """
    return {
        "config": config,
        "prior": prior_params,
        "posterior": posterior_params,
        "metrics": metrics,
        "completed_at": _utc_timestamp(),
    }
