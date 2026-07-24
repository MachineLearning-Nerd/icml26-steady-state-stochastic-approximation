# Rigorous claim-by-claim reproduction

The original pages in this Space are preserved as the evidence judged at
revision `847472e15337044d0adb3e636ebbcf7614f0cd34`. They contain the earlier 1D
toy study that received 6/12. This additive section records a new
rate-sensitive campaign without rewriting that history.

## Outcome

| Claim | Evidence verdict |
| --- | --- |
| 1 - Gaussian W1 under i.i.d. and Markov noise | **VERIFIED** within the committed finite contract |
| 2 - Smooth strongly convex SGD | **VERIFIED** |
| 3 - Hurwitz linear and contractive nonlinear SA | **VERIFIED** |
| 4 - Projection-tail rate | **VERIFIED** |
| 5 - Markov extensions | **VERIFIED** |
| 6 - Flat convex minima | **BLOCKED** after four routes |

The live judged score remains **6/12** until the live judge evaluates a
published revision. Experimental verification of a finite contract is not a
proof of a universally quantified theorem.

## Headline evidence

Across six d=8 model/noise combinations, the fitted W1 slopes are
0.421, 0.494, 0.539, 0.558, 0.496, and 0.505. Each paper-rate envelope,
calibrated only on three coarse stepsizes, passes at two held-out fine
stepsizes. The deliberately too-fast O(alpha) control fails in all six cases.

Projection-tail checks serialize 960 rows for i.i.d. noise and 960 for Markov
noise. An independent parser reconstructs exact two-sided 95%
Clopper-Pearson intervals from the exceedance counts.

The complete text evidence is under `evidence/claim_1/` through
`evidence/claim_6/`.
