# Claim 2 - smooth strongly convex SGD

**Verdict: VERIFIED.**

The committed d=8 objective is coordinate-separable with

`f_i(x) = q_i x^2 / 2 + s_i (1 - cos(x))`, where `q_i > s_i > 0`.

It is globally smooth, strongly convex, nonquadratic, and has bounded third
derivatives. The observed W1 slope is 0.539. The paper-rate held-out envelope
passes, while the identically calibrated O(alpha) negative control fails.

Evidence: `evidence/claim_2/`.
