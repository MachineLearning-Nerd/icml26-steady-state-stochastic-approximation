# Judge-visible Claim 3 evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_jv_claim_3", "created_at": "2026-07-25T06:00:00+00:00", "title": "Claim 3: linear and nonlinear SA raw evidence"}
-->
## Exact contract and assumptions

The linear drift is diagonal Hurwitz with rates 0.7--1.4. The nonlinear map is
`T_i(x)=gamma_i tanh(x_i)` with `gamma_i <= 0.65`, hence globally contractive.
Both use bounded centered skew innovations in d=8.

The independent slopes are
**0.494044** (linear)
and **0.421126**
(nonlinear). Both paper-rate holdouts pass; both `O(alpha)` controls fail.

### Raw output at all five stepsizes

| noise | model | alpha | d | seeds | samples/seed | W1 upper 95% | rate | normalized |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| iid | linear | 0.08 | 8 | 4 | 32768 | 0.245793 | 0.714384 | 0.344063 |
| iid | contractive | 0.08 | 8 | 4 | 32768 | 0.261968 | 0.714384 | 0.366704 |
| iid | linear | 0.04 | 8 | 4 | 32768 | 0.155256 | 0.643775 | 0.241165 |
| iid | contractive | 0.04 | 8 | 4 | 32768 | 0.176719 | 0.643775 | 0.274504 |
| iid | linear | 0.02 | 8 | 4 | 32768 | 0.108294 | 0.553244 | 0.195745 |
| iid | contractive | 0.02 | 8 | 4 | 32768 | 0.144976 | 0.553244 | 0.262048 |
| iid | linear | 0.01 | 8 | 4 | 32768 | 0.085375 | 0.460517 | 0.185389 |
| iid | contractive | 0.01 | 8 | 4 | 32768 | 0.109001 | 0.460517 | 0.236694 |
| iid | linear | 0.005 | 8 | 4 | 32768 | 0.074969 | 0.374648 | 0.200105 |
| iid | contractive | 0.005 | 8 | 4 | 32768 | 0.092058 | 0.374648 | 0.245720 |

[Complete raw CSV](../../evidence/claim_3/raw_metrics.csv) ·
[independent checker JSON](../../evidence/claim_3/independent_checker_output.json) ·
[negative control JSON](../../evidence/claim_3/negative_control_output.json) ·
[claim contract](../../evidence/claim_3/claim_contract.json)

**Verdict: VERIFIED within this explicit finite contract.**
