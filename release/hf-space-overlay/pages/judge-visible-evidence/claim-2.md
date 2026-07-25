# Judge-visible Claim 2 evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_jv_claim_2", "created_at": "2026-07-25T06:00:00+00:00", "title": "Claim 2: d=8 SGD raw evidence"}
-->
## Exact contract and assumptions

The d=8 nonquadratic objective has coordinate gradients
`q_i x_i + s_i sin(x_i)`, with `q_i > s_i > 0`. It is globally smooth,
strongly convex, and has bounded third derivatives. Innovations are bounded,
centered, variance one, and skew.

Independent recomputation gives slope
**0.539014**. The
paper-rate envelope passes both held-out stepsizes; the identically calibrated
`O(alpha)` envelope fails.

### Raw output at every stepsize

| noise | model | alpha | d | seeds | samples/seed | W1 upper 95% | rate | normalized |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| iid | sgd | 0.08 | 8 | 4 | 32768 | 0.261334 | 0.714384 | 0.365818 |
| iid | sgd | 0.04 | 8 | 4 | 32768 | 0.158972 | 0.643775 | 0.246937 |
| iid | sgd | 0.02 | 8 | 4 | 32768 | 0.106925 | 0.553244 | 0.193269 |
| iid | sgd | 0.01 | 8 | 4 | 32768 | 0.081413 | 0.460517 | 0.176787 |
| iid | sgd | 0.005 | 8 | 4 | 32768 | 0.069415 | 0.374648 | 0.185279 |

[Complete raw CSV](../../evidence/claim_2/raw_metrics.csv) ·
[independent checker JSON](../../evidence/claim_2/independent_checker_output.json) ·
[negative control JSON](../../evidence/claim_2/negative_control_output.json) ·
[claim contract](../../evidence/claim_2/claim_contract.json)

**Verdict: VERIFIED within this explicit finite contract.**
