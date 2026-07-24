# Claim-by-claim reproduction of steady-state stochastic approximation

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-m4TAzup6Yc-sgd-steady-state/blob/master/notebooks/sgd_steady_state_reproduction.py)

This repository tests the Gaussian-approximation, projection-tail, Markov-noise,
and flat-minimum claims in
[arXiv:2602.13960](https://arxiv.org/abs/2602.13960). The previous judged
logbook earned **6/12** from 1D toy checks. The new cumulative suite uses three
assumption-satisfying d=8 model classes, five stepsizes, four deterministic
seeds, held-out rate envelopes, exact Clopper–Pearson tail intervals,
independent CSV recomputation, and controls designed to fail.

Claims 1–5 are **VERIFIED within their explicit finite experimental contracts**.
Claim 6 is **BLOCKED** after four routes because the printed proposition is
conditional on unresolved conjectures and is inconsistent with its own
Appendix-E target. These verdicts do not prove universal theorems, and the live
score remains **6/12** until a judge evaluates a future approved Space revision.

The paper predicts a
\(\sqrt{\alpha}\log(1/\alpha)\) Gaussian Wasserstein upper rate. Observed fitted
slopes across six d=8 model/noise families range from **0.421 to 0.558**; every
held-out paper-rate envelope passes and every deliberately too-fast
\(O(\alpha)\) envelope fails. For the conditional flat-minimum result, observed
standard-deviation slopes are **0.24934** for h=4 versus paper scaling 0.25 and
**0.16857** for h=6 versus 1/6, but source inconsistencies prevent an exact
Claim 6 verdict.

All formal runs used the local 8-core arm64 CPU, one repository `.venv`, and
the same pinned `uv` command. No GPU or Hugging Face compute was used; direct
compute cost was $0. The experiment is narrower than the universal theorems:
it uses separable d=8 systems and a rigorous product-law W1 bracket rather than
an exact high-dimensional optimal-transport solve.

- [Illustrated technical report](reports/sgd-steady-state-reproduction/report.md)
- [Self-contained marimo tutorial](notebooks/sgd_steady_state_reproduction.py)
- [Durable claim evidence](.openresearch/artifacts/README.md)

## Experiment log

| Branch/experiment | Purpose or change | Exact run command | Assessment/outcome | Compute |
| --- | --- | --- | --- | --- |
| `master` | Public landing page and approved publication surface | Not run as an experiment (publication surface) | Presentation only | None |
| [Judged 1D baseline](https://github.com/MachineLearning-Nerd/icml26-repro-m4TAzup6Yc-sgd-steady-state/tree/orx/baseline-judged-1d-toy-reproduction) | Freeze the prior 1D checks | `uv run python repro/src/verify_sgd.py` | Reproduces the toy baseline | Local CPU, 20s |
| [Faithful d=8 contracts](https://github.com/MachineLearning-Nerd/icml26-repro-m4TAzup6Yc-sgd-steady-state/tree/orx/faithful-d-8-separable-w1-contracts) | Add assumption-satisfying models, rate contracts, and controls | `uv run python repro/src/verify_sgd.py` | Exposed an i.i.d. W1 sampling floor | Local CPU, 1m20s |
| [High-precision W1](https://github.com/MachineLearning-Nerd/icml26-repro-m4TAzup6Yc-sgd-steady-state/tree/orx/high-precision-iid-w1-floor-removal) | Increase only the Gaussian stationary ensemble | `uv run python repro/src/verify_sgd.py` | Resolves all six W1 slopes and controls | Local CPU, 14m15s |
| [Durable evidence gate](https://github.com/MachineLearning-Nerd/icml26-repro-m4TAzup6Yc-sgd-steady-state/tree/orx/durable-evidence-freeze-and-release-gate) | Add claim-specific independent checks and mutation tests | `uv run python repro/src/verify_sgd.py` | Six independent checks and 12 failure tests pass | Local CPU, 20m44s |
| [Exact tail intervals](https://github.com/MachineLearning-Nerd/icml26-repro-m4TAzup6Yc-sgd-steady-state/tree/orx/final-additive-publication-candidate) | Replace approximate tail uncertainty with exact binomial intervals | `uv run python repro/src/verify_sgd.py` | Claims 1–5 VERIFIED; Claim 6 BLOCKED | Local CPU, 7m43s |
| [Publication assembly](https://github.com/MachineLearning-Nerd/icml26-repro-m4TAzup6Yc-sgd-steady-state/tree/orx/publication-assembly-and-final-regression) | Add report, notebook, and additive text-only release candidate | `uv run python repro/src/verify_sgd.py` | Unchanged cumulative regression passes | Local CPU, 12m37s |

## Run locally

```bash
uv sync --frozen
uv run python repro/src/verify_sgd.py
```

To explore the already-embedded results without rerunning the formal
experiment:

```bash
uv run marimo edit notebooks/sgd_steady_state_reproduction.py
uv run marimo run notebooks/sgd_steady_state_reproduction.py
```
