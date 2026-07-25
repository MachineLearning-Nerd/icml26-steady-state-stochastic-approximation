# Judge-visible Claim 5 evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_jv_claim_5", "created_at": "2026-07-25T06:00:00+00:00", "title": "Claim 5: Markov W1 and tail raw evidence"}
-->
## Exact contract and assumptions

The stationary finite-state refresh chain has `rho=0.55`, is uniformly
ergodic, has bounded Poisson solutions, and has known long-run variance
multiplier `(1+rho)/(1-rho)`. All three d=8 model classes are checked for both
W1 and projection tails.

Independent W1 slopes are
**0.505382**
(SGD),
**0.495829**
(linear), and
**0.558038**
(contractive). All held-out envelopes pass. The `O(alpha)` W1/tail envelopes
and the wrong i.i.d. target covariance are rejected.

### Verifier excerpt

```python
refresh_probability = 1.0 - MARKOV_RHO
long_run = (1.0 + MARKOV_RHO) / (1.0 - MARKOV_RHO)
target_variance = long_run / (2.0 * target_precision)
```

### Raw W1 output

| noise | model | alpha | d | seeds | samples/seed | W1 upper 95% | rate | normalized |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
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

### Raw tail output across all thresholds

| alpha | a | rows | max exact gap U95 | alpha^.25 sqrt(log)/a | max normalized U95 |
| --- | --- | --- | --- | --- | --- |
| 0.080000 | 1.20 | 48 | 0.036151 | 0.704344 | 0.051325 |
| 0.080000 | 0.95 | 48 | 0.036414 | 0.889697 | 0.040928 |
| 0.080000 | 0.70 | 48 | 0.036088 | 1.207446 | 0.029888 |
| 0.080000 | 0.45 | 48 | 0.035531 | 1.878250 | 0.018917 |
| 0.040000 | 1.20 | 48 | 0.024819 | 0.668630 | 0.037119 |
| 0.040000 | 0.95 | 48 | 0.027037 | 0.844585 | 0.032012 |
| 0.040000 | 0.70 | 48 | 0.026515 | 1.146223 | 0.023133 |
| 0.040000 | 0.45 | 48 | 0.026805 | 1.783013 | 0.015033 |
| 0.020000 | 1.20 | 48 | 0.022182 | 0.619836 | 0.035788 |
| 0.020000 | 0.95 | 48 | 0.023000 | 0.782951 | 0.029376 |
| 0.020000 | 0.70 | 48 | 0.022898 | 1.062576 | 0.021550 |
| 0.020000 | 0.45 | 48 | 0.022226 | 1.652897 | 0.013447 |
| 0.010000 | 1.20 | 48 | 0.014999 | 0.565512 | 0.026522 |
| 0.010000 | 0.95 | 48 | 0.015350 | 0.714331 | 0.021489 |
| 0.010000 | 0.70 | 48 | 0.015607 | 0.969449 | 0.016099 |
| 0.010000 | 0.45 | 48 | 0.019109 | 1.508031 | 0.012671 |
| 0.005000 | 1.20 | 48 | 0.010997 | 0.510071 | 0.021559 |
| 0.005000 | 0.95 | 48 | 0.012854 | 0.644300 | 0.019951 |
| 0.005000 | 0.70 | 48 | 0.014028 | 0.874407 | 0.016042 |
| 0.005000 | 0.45 | 48 | 0.015865 | 1.360188 | 0.011664 |

[Complete W1 CSV](../../evidence/claim_5/raw_metrics.csv) ·
[all 960 tail rows](../../evidence/claim_5/raw_tail_metrics.csv) ·
[independent checker JSON](../../evidence/claim_5/independent_checker_output.json) ·
[negative control JSON](../../evidence/claim_5/negative_control_output.json)

**Verdict: VERIFIED within this explicit finite contract.**
