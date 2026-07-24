# Claim 1 - Gaussian approximation under i.i.d. and Markov noise

**Verdict: VERIFIED within the explicit finite experimental contract.**

Theorems 3.1 and 4.1 state a Wasserstein upper rate of
sqrt(alpha) log(1/alpha) for the centered-scaled stationary law. Six faithful
d=8 combinations (three model classes under two noise types) pass held-out
paper-rate envelopes. Their fitted W1 slopes range from 0.421 to 0.558.

Every deliberately faster O(alpha) envelope fails under the same calibration
protocol. This directly answers the prior judge's concerns about a
nonmonotone, four-point 1D check and an arbitrary fixed threshold.

Evidence: `evidence/claim_1/`.
