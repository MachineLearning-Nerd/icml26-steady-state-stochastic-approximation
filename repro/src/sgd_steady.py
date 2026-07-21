"""Clean-room constant-stepsize SGD steady-state, from
"Steady-State Behavior of Constant-Stepsize Stochastic Approximation" (arXiv 2602.13960). numpy, CPU.

Recursion (3.4): X_{t+1} = X_t - alpha * grad_f(X_t) - alpha * sigma * xi_t.
Steady state X^(alpha); centered-scaled Y^(alpha) = (X^(alpha) - x*) / sqrt(alpha).
Proposition 3.1: Y^(alpha) -> Y ~ N(0, Sigma_Y),  Sigma_Y solves H Sigma_Y + Sigma_Y H = Sigma (noise cov),
  with dW(Y^(alpha), Y) <= U1 * alpha^{1/2} * log(1/alpha)  (3.6)
  and Berry-Esseen tail |P(<Y^a,zeta>>a) - P(Z_zeta>a)| <= U1' alpha^{1/4} log^{1/2}(1/alpha) / a  (3.7).
"""
from __future__ import annotations
import numpy as np


def sgd_steady_samples(gradf, xstar, alpha, sigma, n_samples, burn_in, thin, seed=0):
    """Run constant-stepsize SGD; collect steady-state samples of X (subsampled every `thin` after burn-in)."""
    rng = np.random.default_rng(seed)
    x = 0.0
    for _ in range(burn_in):
        x = x - alpha * (gradf(x) + sigma * rng.standard_normal())
    out = np.empty(n_samples)
    for k in range(n_samples):
        for _ in range(thin):
            x = x - alpha * (gradf(x) + sigma * rng.standard_normal())
        out[k] = x
    return out


def w1_empirical(Y, var):
    """1D Wasserstein-1 = integral |empirical_CDF(Y) - Gaussian_CDF| dx. No inverse-CDF needed."""
    from math import erf, sqrt
    ys = np.sort(Y)
    sd = sqrt(max(var, 1e-12))
    xs = np.linspace(min(ys.min(), -6 * sd), max(ys.max(), 6 * sd), 400)
    emp_cdf = np.searchsorted(ys, xs, side="right") / len(ys)
    g_cdf = np.array([0.5 * (1 + erf(x / (sqrt(2) * sd))) for x in xs])
    return float(np.mean(np.abs(emp_cdf - g_cdf)) * (xs[-1] - xs[0]))


def gaussian_tail(a, var):
    """P(N(0,var) > a)."""
    from math import erf, sqrt
    return 0.5 * (1 - erf(a / np.sqrt(2 * var)))
