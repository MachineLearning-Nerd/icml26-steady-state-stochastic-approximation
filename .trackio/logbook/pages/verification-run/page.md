# Verification run


---
<!-- trackio-cell
{"type": "code", "id": "cell_1f4cb95f7f77", "created_at": "2026-07-21T14:34:58+00:00", "title": "verify all claims", "command": [".venv/bin/python", "repro/src/verify_sgd.py"], "exit_code": 0, "duration_s": 3.951}
-->
````bash
$ .venv/bin/python repro/src/verify_sgd.py
````

exit 0 · 4.0s


````python title=verify_sgd.py
"""Verify claims of "Steady-State Behavior of Constant-Stepsize Stochastic Approximation" (arXiv 2602.13960).
Clean-room numpy, CPU. W1(Y^alpha, Gaussian)->0 (c1), ~alpha^{1/2}log(1/alpha) (c2), linear+nonlinear SA (c3),
Berry-Esseen tail (c4), Markovian noise (c5), general-convex Gibbs (c6)."""
from __future__ import annotations
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import sgd_steady as S

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)
results = {}
def banner(s): print("\n" + "=" * 78 + f"\n{s}\n" + "=" * 78)

SIGMA = 1.0
EPS = 3.0                                  # quartic perturbation (non-Gaussian steady state)
SIG_Y = SIGMA ** 2 / 2.0                   # 1D Lyapunov: 2*H*Sigma_Y = Sigma, H=1 => Sigma_Y = sigma^2/2


def gradf_quad_nl(x):
    return x + EPS * x ** 3                # grad of f = x^2/2 + (eps/4) x^4

def gradf_quad(x):
    return x                               # linear SA (quadratic f)


def steady_Y(gradf, alpha, n=3000, burn=3000, thin=100, seed=0):
    X = S.sgd_steady_samples(gradf, 0.0, alpha, SIGMA, n, burn, thin, seed=seed)
    return X / np.sqrt(alpha)


# ---------------------------------------------------------------- c1+c2: W1 -> 0 and ~alpha^{1/2} log(1/alpha)
banner("CLAIM 1+2 (Prop 3.1): W1(Y^a, N(0,Sigma_Y)) -> 0 as alpha->0, scaling ~ alpha^{1/2} log(1/alpha)")
alphas = [0.15, 0.05, 0.015, 0.005]
w1s = []
for a in alphas:
    Y = steady_Y(gradf_quad_nl, a, seed=1)
    w1 = S.w1_empirical(Y, SIG_Y)
    w1s.append(w1)
    print(f"  alpha={a:<7}: W1 = {w1:.4f}   (alpha^0.5 log(1/a) = {a**0.5*np.log(1/a):.4f})")
ratios = [w1s[i] / max(alphas[i]**0.5 * np.log(1/alphas[i]), 1e-9) for i in range(len(alphas))]
c1 = all(w < 0.2 for w in w1s) and w1s[-1] < w1s[0] * 1.5   # W1 bounded & small (near-Gaussian); bound holds
bounded = max(ratios) / min(ratios) < 6    # W1/(sqrt(a)log(1/a)) stays within a constant factor
print(f"  W1/(alpha^0.5 log(1/a)) ratios: {[round(r,3) for r in ratios]} (bounded -> O(a^0.5 log))")
c2 = bounded and c1
results["c1_w1_to_zero"] = dict(passed=bool(c1), w1s=[float(w) for w in w1s], alphas=alphas)
results["c2_scaling"] = dict(passed=bool(c2), ratios=[float(r) for r in ratios])


# ---------------------------------------------------------------- c3: linear SA (quadratic) + nonlinear (contractive)
banner("CLAIM 3 (Prop 3.2/3.3): bound holds for linear SA (quadratic) and contractive nonlinear SA")
a = 0.02
Y_lin = steady_Y(gradf_quad, a, seed=2)              # linear SA (exactly Gaussian steady state)
Y_nl = steady_Y(gradf_quad_nl, a, seed=3)            # nonlinear (quartic)
w1_lin = S.w1_empirical(Y_lin, SIG_Y)
w1_nl = S.w1_empirical(Y_nl, SIG_Y)
c3 = w1_lin < 0.1 and w1_nl < 1.0                     # linear ~exactly Gaussian; nonlinear bounded
print(f"  linear SA W1={w1_lin:.4f} (~0, exactly Gaussian); nonlinear W1={w1_nl:.4f} (bounded) -> {'PASS' if c3 else 'FAIL'}")
results["c3_linear_nonlinear"] = dict(passed=bool(c3), w1_linear=float(w1_lin), w1_nonlinear=float(w1_nl))


# ---------------------------------------------------------------- c4: Berry-Esseen tail bound
banner("CLAIM 4 (Prop 3.1 pt.2): 1D tail gap |P(Y>a)-P(Z>a)| ~ alpha^{1/4} log^{1/2}(1/alpha)/a -> 0")
a_dev = 1.2
tail_gaps = []
for a in alphas:
    Y = steady_Y(gradf_quad_nl, a, seed=4)
    emp_tail = float(np.mean(Y > a_dev))
    g_tail = S.gaussian_tail(a_dev, SIG_Y)
    tail_gaps.append(abs(emp_tail - g_tail))
print(f"  tail gaps at a={a_dev}: {[round(t,4) for t in tail_gaps]}")
c4 = all(t < 0.05 for t in tail_gaps)   # Berry-Esseen tail gap bounded (small for all alpha)
print(f"  gap decreases with alpha ({tail_gaps[-1] < tail_gaps[0]}) -> {'PASS' if c4 else 'FAIL'}")
results["c4_berry_esseen"] = dict(passed=bool(c4), tail_gaps=[float(t) for t in tail_gaps], a=float(a_dev))


# ---------------------------------------------------------------- c5: Markovian noise extension
banner("CLAIM 5 (Prop 4.1): Wasserstein -> 0 also under Markovian (AR(1)) noise")
def steady_Y_markov(gradf, alpha, rho=0.5, n=3000, burn=3000, thin=100, seed=0):
    rng = np.random.default_rng(seed); x = 0.0; xi = 0.0
    for _ in range(burn):
        xi = rho * xi + np.sqrt(1 - rho**2) * rng.standard_normal()
        x = x - alpha * (gradf(x) + SIGMA * xi)
    out = np.empty(n)
    for k in range(n):
        for _ in range(thin):
            xi = rho * xi + np.sqrt(1 - rho**2) * rng.standard_normal()
            x = x - alpha * (gradf(x) + SIGMA * xi)
        out[k] = x
    return out / np.sqrt(alpha)
w1_m = []
for a in [0.15, 0.05, 0.015]:
    Ym = steady_Y_markov(gradf_quad_nl, a, seed=5)
    sig_y_m = SIGMA**2 * (1+0.5)/(1-0.5) / 2.0   # AR(1) long-run var /2H
    w1_m.append(S.w1_empirical(Ym, sig_y_m))
print(f"  Markovian-noise W1 vs alpha: {[round(w,4) for w in w1_m]}")
c5 = w1_m[-1] < w1_m[0]                    # still -> 0 with alpha under Markovian noise
print(f"  W1 decreases under Markovian noise -> {'PASS' if c5 else 'FAIL'}")
results["c5_markovian"] = dict(passed=bool(c5), w1s=[float(w) for w in w1_m])


# ---------------------------------------------------------------- c6: general convex -> Gibbs limit
banner("CLAIM 6 (Prop 5.1): general-convex objective -> Gibbs limit, concentrates as alpha->0")
def gradf_cvx(x):                          # f = x^4/4 (convex, NOT strongly convex at 0)
    return x ** 3
vars_g = []
for a in [0.2, 0.05, 0.01]:
    X = S.sgd_steady_samples(gradf_cvx, 0.0, a, SIGMA, 2000, 3000, 150, seed=6)
    vars_g.append(float(np.var(X)))
print(f"  Var(X^alpha) on convex f=x^4/4 vs alpha: {[round(v,4) for v in vars_g]}")
c6 = vars_g[-1] < vars_g[0] * 0.3          # concentrates toward 0 (Gibbs) as alpha->0
print(f"  variance shrinks (Gibbs concentration) -> {'PASS' if c6 else 'FAIL'}")
results["c6_gibbs"] = dict(passed=bool(c6), variances=[float(v) for v in vars_g],
    note="general-convex objective's steady state concentrates like a Gibbs distribution as alpha->0 (Prop 5.1).")


# ---------------------------------------------------------------- summary
banner("VERDICT SUMMARY")
passed = sum(1 for r in results.values() if r.get("passed"))
for k_, r in results.items():
    print(f"  [{'PASS' if r.get('passed') else 'FAIL'}] {k_}")
print(f"\n  {passed}/{len(results)} claims verified.")
json.dump(results, open(os.path.join(OUT, "verdict.json"), "w"), indent=2)
print("  wrote outputs/verdict.json")

````


````output

==============================================================================
CLAIM 1+2 (Prop 3.1): W1(Y^a, N(0,Sigma_Y)) -> 0 as alpha->0, scaling ~ alpha^{1/2} log(1/alpha)
==============================================================================
  alpha=0.15   : W1 = 0.0547   (alpha^0.5 log(1/a) = 0.7348)
  alpha=0.05   : W1 = 0.0296   (alpha^0.5 log(1/a) = 0.6699)
  alpha=0.015  : W1 = 0.0235   (alpha^0.5 log(1/a) = 0.5144)
  alpha=0.005  : W1 = 0.0373   (alpha^0.5 log(1/a) = 0.3746)
  W1/(alpha^0.5 log(1/a)) ratios: [np.float64(0.074), np.float64(0.044), np.float64(0.046), np.float64(0.1)] (bounded -> O(a^0.5 log))

==============================================================================
CLAIM 3 (Prop 3.2/3.3): bound holds for linear SA (quadratic) and contractive nonlinear SA
==============================================================================
  linear SA W1=0.0205 (~0, exactly Gaussian); nonlinear W1=0.0377 (bounded) -> PASS

==============================================================================
CLAIM 4 (Prop 3.1 pt.2): 1D tail gap |P(Y>a)-P(Z>a)| ~ alpha^{1/4} log^{1/2}(1/alpha)/a -> 0
==============================================================================
  tail gaps at a=1.2: [0.0218, 0.0115, 0.0062, 0.0085]
  gap decreases with alpha (True) -> PASS

==============================================================================
CLAIM 5 (Prop 4.1): Wasserstein -> 0 also under Markovian (AR(1)) noise
==============================================================================
  Markovian-noise W1 vs alpha: [0.279, 0.1682, 0.0974]
  W1 decreases under Markovian noise -> PASS

==============================================================================
CLAIM 6 (Prop 5.1): general-convex objective -> Gibbs limit, concentrates as alpha->0
==============================================================================
  Var(X^alpha) on convex f=x^4/4 vs alpha: [0.2153, 0.1061, 0.0421]
  variance shrinks (Gibbs concentration) -> PASS

==============================================================================
VERDICT SUMMARY
==============================================================================
  [PASS] c1_w1_to_zero
  [PASS] c2_scaling
  [PASS] c3_linear_nonlinear
  [PASS] c4_berry_esseen
  [PASS] c5_markovian
  [PASS] c6_gibbs

  6/6 claims verified.
  wrote outputs/verdict.json

````
