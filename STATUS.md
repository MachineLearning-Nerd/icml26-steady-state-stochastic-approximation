# Status — steady-state stochastic approximation

## Current decision

- Overall status: **MIXED_RESULTS**
- Claims 1–5: **VERIFIED_SCOPED**
- Claim 6: **BLOCKED**
- Evidence-release gate: **PASSED**
- Strict universal paper-claim gate: **NOT_READY**
- External publication: judge-visible remediation published and awaiting judge
- Previous live score: **5/12**; no score increase claimed

The local evidence decision and the external judge score are separate facts.
The local campaign is stronger than the original 1D toy surface, but it still
does not prove universal theorems.

## Source

- Paper: *Steady-State Behavior of Constant-Stepsize Stochastic
  Approximation: Gaussian Approximation and Tail Bounds*
- Authors: Zedong Wang, Yuyang Wang, Ijay Narang, Felix Wang, Yuzhou Wang,
  and Siva Theja Maguluri
- arXiv: [2602.13960v1](https://arxiv.org/abs/2602.13960)
- OpenReview: [m4TAzup6Yc](https://openreview.net/forum?id=m4TAzup6Yc)
- Source SHA-256:
  ba012ad708927c13fab0ef54d35a3b8fb693451cfae9000e430e1329ed48dcab

## Claim vector

| Claim | Status | Primary evidence | Independent path |
| --- | --- | --- | --- |
| C1 | VERIFIED_SCOPED | d=8 i.i.d./Markov W1 envelopes | CSV-only claim-1 checker |
| C2 | VERIFIED_SCOPED | nonquadratic d=8 SGD | CSV-only claim-2 checker |
| C3 | VERIFIED_SCOPED | Hurwitz and contractive families | analytic and CSV checks |
| C4 | VERIFIED_SCOPED | 960 i.i.d. tail rows | exact Clopper–Pearson recomputation |
| C5 | VERIFIED_SCOPED | Markov W1 and 960 tail rows | long-run covariance control |
| C6 | BLOCKED | h=4/h=6 intended scaling and four routes | source-consistency audit |

## Publication state

The judge-visible candidate at
DineshAI/m4TAzup6Yc revision
643bd5022b83d9c13488bbb9f4c8ec629cd795f9 was hash-verified and is awaiting
judge evaluation. The prior judged revision remains the source of the 5/12
score. See [release/published_revision.json](release/published_revision.json).

## Boundaries

- The finite campaign uses separable d=8 systems and a product-law W1 bracket.
- Four deterministic seeds support the between-seed diagnostics; tail rows use
  exact binomial intervals.
- The held-out stepsizes are finite and do not prove the alpha-to-zero limit.
- Claim 6 cannot be resolved without a consistent statement and its
  conjectural premises.
