# Claim 3 - linear and contractive nonlinear SA

**Verdict: VERIFIED.**

The linear system has a diagonal Hurwitz drift with rates in [0.7, 1.4]. The
nonlinear system uses `T_i(x) = gamma_i tanh(x_i)` with `gamma_i <= 0.65`, so
it is globally contractive and has bounded derivatives.

Under i.i.d. noise, their fitted W1 slopes are respectively 0.494 and 0.421.
Both held-out paper-rate envelopes pass, and both O(alpha) controls fail. This
replaces the earlier single-alpha threshold checks.

Evidence: `evidence/claim_3/`.
