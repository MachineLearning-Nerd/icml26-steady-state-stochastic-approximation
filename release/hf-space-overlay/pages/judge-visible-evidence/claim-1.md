# Judge-visible Claim 1 evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_jv_claim_1", "created_at": "2026-07-25T06:00:00+00:00", "title": "Claim 1: d=8 W1 raw evidence"}
-->
## Exact contract and assumptions

Theorems 3.1 and 4.1 predict
`W1(L(Y_alpha), N(0,Sigma_Y)) <= U sqrt(alpha) log(1/alpha)`.
The finite contract uses all three assumption-satisfying d=8 systems, i.i.d.
and uniformly ergodic finite-state Markov noise, five stepsizes, four seeds,
and 32,768 retained samples per seed. Three coarse stepsizes calibrate one
constant; two fine stepsizes are held out. The Euclidean W1 upper bound is the
sum of exact coordinate W1 values for the separable product law.

### Independently recomputed rate results

| family | log-log slope | calibration | held-out normalized U95 | pass |
| --- | --- | --- | --- | --- |
| iid:contractive | 0.421126 | 0.550056 | 0.236694, 0.245720 | True |
| iid:linear | 0.494044 | 0.516095 | 0.185389, 0.200105 | True |
| iid:sgd | 0.539014 | 0.548727 | 0.176787, 0.185279 | True |
| markov:contractive | 0.558038 | 2.594676 | 0.879497, 0.805749 | True |
| markov:linear | 0.495829 | 1.968783 | 0.747651, 0.665724 | True |
| markov:sgd | 0.505382 | 1.989277 | 0.726508, 0.652047 | True |

The deliberately too-fast `O(alpha)` envelope fails for all six families.

### Verifier excerpt

```python
coord = coordinate_w1(model_samples, target_var)
record = {
    "w1_lower": float(np.max(coord)),
    "w1_upper": float(np.sum(coord)),
}
calibrator = 1.50 * float(np.max(ratios[:3]))
holdout_pass = bool(np.all(ratios[3:] <= calibrator))
```

### Raw W1 output

| noise | model | alpha | d | seeds | samples/seed | W1 upper 95% | rate | normalized |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| iid | sgd | 0.08 | 8 | 4 | 32768 | 0.261334 | 0.714384 | 0.365818 |
| iid | linear | 0.08 | 8 | 4 | 32768 | 0.245793 | 0.714384 | 0.344063 |
| iid | contractive | 0.08 | 8 | 4 | 32768 | 0.261968 | 0.714384 | 0.366704 |
| iid | sgd | 0.04 | 8 | 4 | 32768 | 0.158972 | 0.643775 | 0.246937 |
| iid | linear | 0.04 | 8 | 4 | 32768 | 0.155256 | 0.643775 | 0.241165 |
| iid | contractive | 0.04 | 8 | 4 | 32768 | 0.176719 | 0.643775 | 0.274504 |
| iid | sgd | 0.02 | 8 | 4 | 32768 | 0.106925 | 0.553244 | 0.193269 |
| iid | linear | 0.02 | 8 | 4 | 32768 | 0.108294 | 0.553244 | 0.195745 |
| iid | contractive | 0.02 | 8 | 4 | 32768 | 0.144976 | 0.553244 | 0.262048 |
| iid | sgd | 0.01 | 8 | 4 | 32768 | 0.081413 | 0.460517 | 0.176787 |
| iid | linear | 0.01 | 8 | 4 | 32768 | 0.085375 | 0.460517 | 0.185389 |
| iid | contractive | 0.01 | 8 | 4 | 32768 | 0.109001 | 0.460517 | 0.236694 |
| iid | sgd | 0.005 | 8 | 4 | 32768 | 0.069415 | 0.374648 | 0.185279 |
| iid | linear | 0.005 | 8 | 4 | 32768 | 0.074969 | 0.374648 | 0.200105 |
| iid | contractive | 0.005 | 8 | 4 | 32768 | 0.092058 | 0.374648 | 0.245720 |
| markov | sgd | 0.08 | 8 | 4 | 32768 | 0.947405 | 0.714384 | 1.326185 |
| markov | linear | 0.08 | 8 | 4 | 32768 | 0.937645 | 0.714384 | 1.312522 |
| markov | contractive | 0.08 | 8 | 4 | 32768 | 1.235730 | 0.714384 | 1.729784 |
| markov | sgd | 0.04 | 8 | 4 | 32768 | 0.657415 | 0.643775 | 1.021186 |
| markov | linear | 0.04 | 8 | 4 | 32768 | 0.657839 | 0.643775 | 1.021845 |
| markov | contractive | 0.04 | 8 | 4 | 32768 | 0.856015 | 0.643775 | 1.329681 |
| markov | sgd | 0.02 | 8 | 4 | 32768 | 0.473663 | 0.553244 | 0.856156 |
| markov | linear | 0.02 | 8 | 4 | 32768 | 0.474858 | 0.553244 | 0.858316 |
| markov | contractive | 0.02 | 8 | 4 | 32768 | 0.615898 | 0.553244 | 1.113250 |
| markov | sgd | 0.01 | 8 | 4 | 32768 | 0.334569 | 0.460517 | 0.726508 |
| markov | linear | 0.01 | 8 | 4 | 32768 | 0.344306 | 0.460517 | 0.747651 |
| markov | contractive | 0.01 | 8 | 4 | 32768 | 0.405024 | 0.460517 | 0.879497 |
| markov | sgd | 0.005 | 8 | 4 | 32768 | 0.244288 | 0.374648 | 0.652047 |
| markov | linear | 0.005 | 8 | 4 | 32768 | 0.249412 | 0.374648 | 0.665724 |
| markov | contractive | 0.005 | 8 | 4 | 32768 | 0.301872 | 0.374648 | 0.805749 |

[Complete raw CSV](../../evidence/claim_1/raw_metrics.csv) ·
[independent checker JSON](../../evidence/claim_1/independent_checker_output.json) ·
[negative control JSON](../../evidence/claim_1/negative_control_output.json) ·
[claim contract](../../evidence/claim_1/claim_contract.json)

**Verdict: VERIFIED within this explicit finite contract.**
