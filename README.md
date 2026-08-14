# ICML 2026 reproduction: Steady-State Stochastic Approximation

This repository is an independent, source-pinned audit of
[*Steady-State Behavior of Constant-Stepsize Stochastic Approximation:
Gaussian Approximation and Tail Bounds*](https://arxiv.org/abs/2602.13960)
by Zedong Wang, Yuyang Wang, Ijay Narang, Felix Wang, Yuzhou Wang, and Siva
Theja Maguluri.

## Current status

- Overall evidence status: **MIXED_RESULTS**.
- Finite claim vector: Claims 1–5 are **VERIFIED_SCOPED**; Claim 6 is
  **BLOCKED**.
- Evidence-release gate: **PASSED**.
- Strict universal paper-claim gate: **NOT_READY**.
- External state: the judge-visible remediation was published to
  DineshAI/m4TAzup6Yc at revision
  643bd5022b83d9c13488bbb9f4c8ec629cd795f9, and is awaiting judge
  evaluation. The previous live score is **5/12**; no score increase is
  claimed for the new revision.

The finite verdicts describe explicit machine contracts. They do not prove
the paper's universal theorems. Claim 6 is intentionally not upgraded to
VERIFIED_SCOPED: the proposition is conditional on unresolved conjectures,
and its printed drift and density conflict with the scaling argument and
Appendix E.

## Paper

- Official record: [arXiv:2602.13960v1](https://arxiv.org/abs/2602.13960)
- [Official PDF](https://arxiv.org/pdf/2602.13960)
- OpenReview identifier: [m4TAzup6Yc](https://openreview.net/forum?id=m4TAzup6Yc)
- Authors: Zedong Wang, Yuyang Wang, Ijay Narang, Felix Wang, Yuzhou Wang,
  and Siva Theja Maguluri

The paper studies constant-stepsize stochastic approximation after it reaches
steady state. It gives fixed-stepsize, non-asymptotic Gaussian-approximation
bounds in Wasserstein distance for i.i.d. and Markovian noise, applies them to
SGD, linear SA, and contractive nonlinear SA, derives projection-tail bounds,
and studies a Gibbs-type limit near flat convex minima.

## Claim ledger

| Claim | Paper target | How the claim is produced | Result |
| --- | --- | --- | --- |
| C1 | Theorems 3.1 and 4.1: the centered/scaled steady state is within an O(sqrt(alpha) log(1/alpha)) Wasserstein envelope | repro/src/research_campaign.py generates six assumption-satisfying d=8 model/noise families; verify_claim_artifacts.py --claim 1 validates held-out envelopes; independent_check.py recomputes from CSV | **VERIFIED_SCOPED** — all i.i.d. and Markov family envelopes pass; fitted slopes range 0.421–0.558 |
| C2 | Proposition 3.1: smooth strongly convex nonquadratic SGD | The committed separable objective f_i(x)=q_i x²/2+s_i(1-cos x) is simulated with bounded skew noise; claim artifacts and the CSV-only checker validate the rate and wrong-rate control | **VERIFIED_SCOPED** — d=8 SGD slope 0.539; paper-rate holdout passes and the O(alpha) control fails |
| C3 | Propositions 3.2–3.3: Hurwitz linear SA and contractive nonlinear SA | research_campaign.py instantiates diagonal Hurwitz and gamma_i tanh(x_i) systems; analytic assumption checks, Gaussian linear reference, and independent CSV checks run through the claim verifier | **VERIFIED_SCOPED** — slopes 0.494 and 0.421; both held-out envelopes and controls pass |
| C4 | Projection-tail inequalities and Proposition 4.1's non-uniform Berry–Esseen behavior | Four directions, four thresholds, five stepsizes, three i.i.d. model families, and exact Clopper–Pearson intervals are serialized; the checker recomputes all tail gaps | **VERIFIED_SCOPED** — 960 i.i.d. rows; the wrong O(alpha) tail envelope fails |
| C5 | Proposition 4.1 under Markovian noise | A product of eight stationary two-state refresh chains with rho=0.55 supplies bounded Markov noise; long-run covariance, W1, tail rows, and the i.i.d.-covariance negative control are checked | **VERIFIED_SCOPED** — 960 Markov tail rows and all three model classes pass; the covariance substitution control fails |
| C6 | Proposition 5.1: alpha^(1/h) Gibbs approximation for general convex objectives | Four independent routes test h=4/h=6 scaling, correct Gibbs normalization, the literal density, and the Appendix-E density; all routes are documented in .openresearch/artifacts/claim_6/routes.md | **BLOCKED** — intended scaling is supported, but the exact proposition is conjectural and source-inconsistent |

## Evidence and claim boundaries

The authoritative finite evidence is under
[.openresearch/artifacts](.openresearch/artifacts). Each claim directory
contains its contract, source audit, method, raw CSV, verdict, runtime,
independent checker, negative control, and limitations.

- [Claim audit](AUDIT_REPORT.md) explains each producer, checker, result, and
  boundary.
- [Source manifest](SOURCE_MANIFEST.md) records the paper snapshot, hashes,
  environment, seeds, and release receipts.
- [Output provenance](outputs/README.md) distinguishes the historical toy
  output from the current d=8 campaign.
- [Branch audit](BRANCH_AUDIT.md) records the final branch vocabulary and
  verified remote invariants.

## Reproduce

Use the locked Python environment:

```bash
uv sync --frozen
uv run python repro/src/verify_sgd.py
```

The command regenerates the campaign artifacts, runs independent claim
parsers and negative controls, and rebuilds the report assets. To inspect the
embedded tutorial without rerunning the campaign:

```bash
uv run marimo edit notebooks/sgd_steady_state_reproduction.py
uv run marimo run notebooks/sgd_steady_state_reproduction.py
```

## Branch guide

The final public branch vocabulary is purpose-based. Historical names are
retained below only as provenance; they are not final remote refs.

| Final branch | Historical source | Purpose |
| --- | --- | --- |
| [main](https://github.com/MachineLearning-Nerd/icml26-steady-state-stochastic-approximation/tree/main) | master | Canonical README, reports, status, release metadata, and tutorial |
| [baseline/judged-1d](https://github.com/MachineLearning-Nerd/icml26-steady-state-stochastic-approximation/tree/baseline/judged-1d) | orx/baseline-judged-1d-toy-reproduction | Historical 1D judged baseline |
| [docs/reader-facing](https://github.com/MachineLearning-Nerd/icml26-steady-state-stochastic-approximation/tree/docs/reader-facing) | orx/reader-facing-report-notebook-and-release-candid | Reader-facing report and notebook checkpoint |
| [research/faithful-d8](https://github.com/MachineLearning-Nerd/icml26-steady-state-stochastic-approximation/tree/research/faithful-d8) | orx/faithful-d-8-separable-w1-contracts | Initial faithful d=8 contracts |
| [research/high-precision-w1](https://github.com/MachineLearning-Nerd/icml26-steady-state-stochastic-approximation/tree/research/high-precision-w1) | orx/high-precision-iid-w1-floor-removal | High-precision W1 ensemble |
| [release/durable-evidence](https://github.com/MachineLearning-Nerd/icml26-steady-state-stochastic-approximation/tree/release/durable-evidence) | orx/durable-evidence-freeze-and-release-gate | Durable evidence and mutation gate |
| [release/final-evidence](https://github.com/MachineLearning-Nerd/icml26-steady-state-stochastic-approximation/tree/release/final-evidence) | orx/final-additive-publication-candidate | Exact-tail final evidence checkpoint |
| [release/publication-assembly](https://github.com/MachineLearning-Nerd/icml26-steady-state-stochastic-approximation/tree/release/publication-assembly) | orx/publication-assembly-and-final-regression | Report and text-only publication assembly |
| [audit/final-approval](https://github.com/MachineLearning-Nerd/icml26-steady-state-stochastic-approximation/tree/audit/final-approval) | orx/final-approval-report-freeze | Final approval and release metadata audit |
| [release/awaiting-judge](https://github.com/MachineLearning-Nerd/icml26-steady-state-stochastic-approximation/tree/release/awaiting-judge) | orx/published-receipt-and-awaiting-judge-mirror | Earlier published receipt and judge state |
| [research/judge-visible-d8](https://github.com/MachineLearning-Nerd/icml26-steady-state-stochastic-approximation/tree/research/judge-visible-d8) | orx/judge-visible-d-8-code-and-raw-evidence | Full d=8 source and raw evidence visible to the judge |
| [release/published-receipt](https://github.com/MachineLearning-Nerd/icml26-steady-state-stochastic-approximation/tree/release/published-receipt) | orx/published-judge-visible-remediation-receipt | Current published revision receipt |

main is the reader-facing surface. Research branches are development
checkpoints; release branches are evidence/publication checkpoints.

## Repository map

- repro/src/research_campaign.py — scientific campaign and claim artifact
  producer.
- repro/src/verify_claim_artifacts.py — claim-specific contract verifier.
- repro/src/independent_check.py — simulator-independent CSV checker.
- repro/src/verify_sgd.py — locked end-to-end entrypoint.
- .openresearch/artifacts/ — durable claim evidence and limitations.
- reports/sgd-steady-state-reproduction/ — illustrated technical report.
- release/ — publication allowlist, receipt, and candidate verifier.
- .trackio/logbook/ — reader-facing experiment log.

## Citation

```bibtex
@article{wang2026steadystate,
  title   = {Steady-State Behavior of Constant-Stepsize Stochastic
             Approximation: Gaussian Approximation and Tail Bounds},
  author  = {Wang, Zedong and Wang, Yuyang and Narang, Ijay and
             Wang, Felix and Wang, Yuzhou and Maguluri, Siva Theja},
  journal = {arXiv preprint arXiv:2602.13960},
  year    = {2026},
  url     = {https://arxiv.org/abs/2602.13960}
}
```

## Thank you

Thank you to Zedong Wang, Yuyang Wang, Ijay Narang, Felix Wang, Yuzhou Wang,
and Siva Theja Maguluri for making this work available for independent study.
This repository is maintained by MachineLearning-Nerd as a transparent
reproduction audit and is not affiliated with or endorsed by the authors.
