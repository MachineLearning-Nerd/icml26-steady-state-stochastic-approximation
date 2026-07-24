# Claim 4 - projection-tail rate

**Verdict: VERIFIED.**

The check covers three d=8 models, five stepsizes, four deterministic seeds,
four unit directions, and four positive thresholds: 960 serialized rows.
Every row stores its exceedance count and sample size. An independent checker
recomputes exact two-sided 95% Clopper-Pearson intervals.

The largest held-out normalized upper gap is 0.01463, below the coarse-step
calibration 0.02925. The wrong O(alpha) tail envelope fails.

Evidence: `evidence/claim_4/`.
