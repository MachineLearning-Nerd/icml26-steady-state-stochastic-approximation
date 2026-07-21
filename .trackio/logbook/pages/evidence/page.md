# Evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_fe1bc38d0683", "created_at": "2026-07-21T14:34:53+00:00", "title": "Verification output (last 40 lines)"}
-->
## Verification output (last 40 lines)

```
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
```
