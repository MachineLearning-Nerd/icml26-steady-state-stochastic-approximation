# Judge-visible Claim 4 evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_jv_claim_4", "created_at": "2026-07-25T06:00:00+00:00", "title": "Claim 4: exact 1/a tail-rate raw evidence"}
-->
## Exact contract and assumptions

The exact paper rate is checked as
`gap <= C alpha^(1/4) sqrt(log(1/alpha)) / a`, not by a fixed cutoff.
Coverage is 3 models x 5 stepsizes x 4 seeds x 4 unit projections x 4 positive
thresholds = **960 rows**. Each row stores the exceedance count and sample
size. The independent parser reconstructs exact two-sided 95%
Clopper--Pearson intervals and the rate formula.

- coverage: **True**
- exact interval recomputation: **True**
- exact `alpha^(1/4) sqrt(log)/a` formula: **True**
- coarse calibration: **0.029247**
- max held-out normalized U95: **0.014627**
- wrong `O(alpha)` tail envelope: **rejected**

### Verifier excerpt

```python
probability_low = beta_distribution.ppf(
    0.025, exceedances, sample_size - exceedances + 1
)
probability_high = beta_distribution.ppf(
    0.975, exceedances + 1, sample_size - exceedances
)
upper95 = max(abs(probability_low - gaussian), abs(probability_high - gaussian))
rate = alpha**0.25 * math.sqrt(math.log(1.0 / alpha)) / threshold
```

### Raw threshold-by-stepsize output

| alpha | a | rows | max exact gap U95 | alpha^.25 sqrt(log)/a | max normalized U95 |
| --- | --- | --- | --- | --- | --- |
| 0.080000 | 1.20 | 48 | 0.013401 | 0.704344 | 0.019027 |
| 0.080000 | 0.95 | 48 | 0.017347 | 0.889697 | 0.019498 |
| 0.080000 | 0.70 | 48 | 0.019647 | 1.207446 | 0.016272 |
| 0.080000 | 0.45 | 48 | 0.016427 | 1.878250 | 0.008746 |
| 0.040000 | 1.20 | 48 | 0.009306 | 0.668630 | 0.013919 |
| 0.040000 | 0.95 | 48 | 0.011980 | 0.844585 | 0.014184 |
| 0.040000 | 0.70 | 48 | 0.014682 | 1.146223 | 0.012809 |
| 0.040000 | 0.45 | 48 | 0.013572 | 1.783013 | 0.007612 |
| 0.020000 | 1.20 | 48 | 0.008440 | 0.619836 | 0.013617 |
| 0.020000 | 0.95 | 48 | 0.012408 | 0.782951 | 0.015848 |
| 0.020000 | 0.70 | 48 | 0.014066 | 1.062576 | 0.013238 |
| 0.020000 | 0.45 | 48 | 0.015317 | 1.652897 | 0.009267 |
| 0.010000 | 1.20 | 48 | 0.007575 | 0.565512 | 0.013395 |
| 0.010000 | 0.95 | 48 | 0.008107 | 0.714331 | 0.011349 |
| 0.010000 | 0.70 | 48 | 0.009536 | 0.969449 | 0.009837 |
| 0.010000 | 0.45 | 48 | 0.011925 | 1.508031 | 0.007908 |
| 0.005000 | 1.20 | 48 | 0.007461 | 0.510071 | 0.014627 |
| 0.005000 | 0.95 | 48 | 0.007939 | 0.644300 | 0.012321 |
| 0.005000 | 0.70 | 48 | 0.009491 | 0.874407 | 0.010854 |
| 0.005000 | 0.45 | 48 | 0.011188 | 1.360188 | 0.008225 |

[All 960 raw rows](../../evidence/claim_4/raw_metrics.csv) ·
[independent checker JSON](../../evidence/claim_4/independent_checker_output.json) ·
[negative control JSON](../../evidence/claim_4/negative_control_output.json) ·
[claim contract](../../evidence/claim_4/claim_contract.json)

**Verdict: VERIFIED within this explicit finite contract.**
