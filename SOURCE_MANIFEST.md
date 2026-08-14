# Source manifest

This manifest records the paper snapshot, scientific source, and publication
receipts behind the current finite-contract audit.

## Paper source

| Field | Value |
| --- | --- |
| Title | Steady-State Behavior of Constant-Stepsize Stochastic Approximation: Gaussian Approximation and Tail Bounds |
| Authors | Zedong Wang; Yuyang Wang; Ijay Narang; Felix Wang; Yuzhou Wang; Siva Theja Maguluri |
| arXiv | [2602.13960v1](https://arxiv.org/abs/2602.13960) |
| PDF | [arxiv.org/pdf/2602.13960](https://arxiv.org/pdf/2602.13960) |
| OpenReview | [m4TAzup6Yc](https://openreview.net/forum?id=m4TAzup6Yc) |
| Retrieved source | https://ar5iv.labs.arxiv.org/html/2602.13960 |
| Retrieved at | 2026-07-23T16:22:07Z |
| SHA-256 | ba012ad708927c13fab0ef54d35a3b8fb693451cfae9000e430e1329ed48dcab |

The source registry preserves anchors for Assumptions 3.1–3.2, Theorems
3.1 and 4.1, Propositions 3.1–3.3 and 4.1, Assumptions 5.1–5.2, Conjectures
5.1–5.2, and Proposition 5.1:
[source_registry.json](release/hf-space-overlay/evidence/protected/source_registry.json).

## Scientific source

| Field | Value |
| --- | --- |
| Evidence Git SHA | a75d96d2fd051c33e80f1bb92870e6afb6ee42f6 |
| Judge-visible source SHA | ca71757e2505adf2d17c2dac2a12a12381db3cd3 |
| Fixed command | uv run python repro/src/verify_sgd.py |
| Environment | Python 3.12.11, NumPy 2.5.1, SciPy 1.18.0 |
| Lockfile | uv.lock |
| Hardware | local 8-core arm64 CPU; no GPU |
| Seeds | 1729, 2718, 3141, 5772 |

The evidence source uses three separable d=8 model classes, five stepsizes,
four deterministic seeds, held-out fine stepsizes, exact tail intervals, and
CSV-only independent recomputation.

## Evidence tree

The authoritative current evidence is under
.openresearch/artifacts. Each claim directory contains:

- claim_contract.json — paper result, assumptions, operationalization, and gate;
- source_audit.md — source location and hash;
- method.md — experiment construction;
- raw_metrics.csv — serialized observations;
- verdict.json — scoped verdict;
- independent_checker_output.json — independent recomputation;
- negative_control_output.json — expected failure control;
- limitations.md and EVAL.md — boundaries and execution record.

Claims 1–5 are VERIFIED_SCOPED. Claim 6 is BLOCKED after four documented
routes in .openresearch/artifacts/claim_6/routes.md.

## Publication receipt

The judge-visible remediation was published to
DineshAI/m4TAzup6Yc at revision
643bd5022b83d9c13488bbb9f4c8ec629cd795f9. The formal local run was recorded
as 3533c8cd-f080-4076-aee3-64ae49792f7f and the release receipt is
[release/published_revision.json](release/published_revision.json).

The previous judged revision remains the source of the documented 5/12 live
score. The new revision is awaiting judge evaluation; publication is not
presented as a score change.
