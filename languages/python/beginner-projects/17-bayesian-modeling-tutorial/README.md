# Beginner Project 17: Bayesian Modeling Tutorial

**Time:** 3-5 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Bayesian inference, conjugate prior updates, posterior analysis, prior sensitivity analysis, and posterior predictive distributions

---

## Why This Project?

Understanding how to update beliefs from evidence is a foundational skill in statistics and machine learning.
This project gives you a practical beginner workflow where you can:

- specify prior beliefs about an unknown probability using a Beta distribution,
- update those beliefs analytically after observing coin-flip data (Beta-Binomial conjugate model),
- summarize the posterior with credible intervals and MAP estimates,
- compare how different priors influence the posterior through sensitivity analysis,
- and generate posterior predictive distributions to forecast future observations.

---

## Separate Repository

You can also access this project in a separate repository:

[bayesian-modeling-tutorial Repository](https://github.com/ShamShamsw/Bayesian-modeling-tutorial.git)

---

## What You Will Build

You will build a command-line Bayesian inference tool that:

1. Accepts observed coin-flip data (total flips and number of heads) as configuration.
2. Defines a Beta prior distribution over the unknown coin-bias probability p.
3. Computes the analytical conjugate posterior using the Beta-Binomial model.
4. Summarizes the posterior with the mean, mode (MAP), standard deviation, and 95% credible interval.
5. Runs a prior sensitivity analysis across five named priors (uniform, weakly informative, strong fair-coin, biased, and Jeffreys).
6. Generates a posterior predictive distribution for future coin flips via Monte Carlo sampling.
7. Saves the complete inference session to JSON for reproducibility.

---

## Requirements

- Python 3.11+
- `numpy`
- `scipy`
- `matplotlib`
- `seaborn`

Install with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
  BAYESIAN MODELING TUTORIAL - BETA-BINOMIAL COIN INFERENCE
======================================================================

Configuration:
  Observed flips:   50 total (30 heads, 20 tails)
  Maximum likelihood estimate (p): 0.600
  Prior: Beta(1.0, 1.0)
  Posterior samples: 10000
  Random seed: 42

Available prior presets for sensitivity analysis:
  - uniform: Beta(1.0, 1.0) - Uniform prior - no prior belief
  - weakly_informative: Beta(2.0, 2.0) - Weakly informative - slight fair-coin belief
  - strong_fair_coin: Beta(10.0, 10.0) - Strong fair-coin belief (p near 0.5)
  - biased_high: Beta(5.0, 2.0) - Prior belief coin is biased toward heads
  - jeffreys: Beta(0.5, 0.5) - Jeffreys prior - non-informative reference prior

Session behavior:
  1) Specify prior Beta distribution for coin-flip probability p.
  2) Compute analytical conjugate posterior after observing data.
  3) Summarize posterior: mean, mode, 95% credible interval.
  4) Run prior sensitivity analysis across named presets.
  5) Generate posterior predictive distribution for future flips.

Session summary:
  Status: completed
  Data: 50 flips, 30 heads
  Posterior: Beta(31.0, 21.0)
  Posterior mean: 0.5962
  Posterior mode (MAP): 0.6000
  Posterior std: 0.0674
  95% credible interval: [0.4611, 0.7242]
  Prior sensitivity analysis: 5 priors tested
    uniform               : mean=0.5962  95%CI=[0.4611, 0.7242]
    weakly_informative    : mean=0.5926  95%CI=[0.4600, 0.7186]
    strong_fair_coin      : mean=0.5714  95%CI=[0.4548, 0.6842]
    biased_high           : mean=0.6140  95%CI=[0.4855, 0.7350]
    jeffreys              : mean=0.5980  95%CI=[0.4617, 0.7270]
  Posterior predictive (20 future flips):
    Expected heads: 12.0 +/- 2.5
    95% predictive interval: [7, 17]
  Saved plots: data/runs/prior_posterior.png, data/runs/sensitivity.png
Saved run artifact: data/runs/latest_bayesian_inference.json
```

---

## Build Order

Follow this order for clean architecture:

1. `storage.py`
2. `models.py`
3. `operations.py`
4. `display.py`
5. `main.py`

---

