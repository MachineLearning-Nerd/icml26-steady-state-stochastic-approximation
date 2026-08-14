# Branch audit

## Final branch vocabulary

The final remote contains twelve purpose-based branches:

| Final branch | Historical source ref | Responsibility |
| --- | --- | --- |
| main | master | Canonical reader-facing surface |
| baseline/judged-1d | orx/baseline-judged-1d-toy-reproduction | Historical 1D judged baseline |
| docs/reader-facing | orx/reader-facing-report-notebook-and-release-candid | Report and notebook checkpoint |
| research/faithful-d8 | orx/faithful-d-8-separable-w1-contracts | Initial faithful d=8 contracts |
| research/high-precision-w1 | orx/high-precision-iid-w1-floor-removal | High-precision W1 ensemble |
| release/durable-evidence | orx/durable-evidence-freeze-and-release-gate | Durable evidence gate |
| release/final-evidence | orx/final-additive-publication-candidate | Exact-tail final evidence |
| release/publication-assembly | orx/publication-assembly-and-final-regression | Publication assembly |
| audit/final-approval | orx/final-approval-report-freeze | Final approval metadata audit |
| release/awaiting-judge | orx/published-receipt-and-awaiting-judge-mirror | Earlier publication receipt |
| research/judge-visible-d8 | orx/judge-visible-d-8-code-and-raw-evidence | Full d=8 judge-visible evidence |
| release/published-receipt | orx/published-judge-visible-remediation-receipt | Current publication receipt |

Historical refs are shown for provenance only and are not part of the final
remote vocabulary.

## Identity policy

All approved commits use:

```text
MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>
```

The history cleanup covers every commit reachable from the twelve final
branches. No co-author or tool-signature lines are added.

## Required remote invariants

- Owner: MachineLearning-Nerd
- Repository: icml26-steady-state-stochastic-approximation
- Default branch: main
- Public branch count: 12
- Legacy refs absent: master, all orx/* refs
- README, STATUS, SOURCE_MANIFEST, AUDIT_REPORT, and publication_gate.json
  are present on main
- Every final branch is pushed and readable

## Remote verification

Verified on 2026-08-14 against the GitHub remote:

- `HEAD` points to `main`
- `main` tip: `24ed73998c9d2a6b7659e3e827f90a1631ce1862`
- `git ls-remote --heads origin` returns exactly twelve branches
- `master` and every `orx/*` ref are absent
- All reachable commit authors and committers are
  `MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>`
