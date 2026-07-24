# Claim 5 - Markov-noise extensions

**Verdict: VERIFIED.**

All three d=8 model classes use a stationary finite-state refresh chain with
rho=0.55. Its long-run variance multiplier is analytically
`(1 + rho) / (1 - rho)`.

The fitted W1 slopes are 0.558, 0.496, and 0.505. The Markov tail evidence
contains 960 rows; its largest held-out normalized exact-interval upper gap is
0.02652, below calibration 0.07699. Both the wrong O(alpha) rate and a
deliberate i.i.d.-covariance substitution are rejected.

Evidence: `evidence/claim_5/`.
