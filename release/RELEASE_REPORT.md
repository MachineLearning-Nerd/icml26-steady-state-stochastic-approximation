# Publication release report

**Status:** published to the existing Space; **awaiting judge**.

**Previous live judged score:** 5/12.

**Current judge head:** `887693a544629b31b7c6dc141fa321a9fcdb5948`.

**Published HF head:** `643bd5022b83d9c13488bbb9f4c8ec629cd795f9`.

**Target Space:** `DineshAI/m4TAzup6Yc` (the existing Space only).

No score increase is claimed. The live judge has not evaluated the published
HF revision.

## Why the prior revision received 5/12

The 2026-07-24 verdict selected by
`space_id == "DineshAI/m4TAzup6Yc"` rated Claims 1–5 `toy` and Claim 6
`inconclusive`. The common criticism was that the visible implementation was
the original 1D, 2,000–3,000-sample simulation with arbitrary thresholds.

The rigorous d=8 evidence already existed in the Space, but Trackio's compact
agent reader serialized its plain-Markdown subtree as `No cells`. The judge
therefore could not see executable d=8 code or raw output. The remediation
adds a real 10-cell Trackio page containing the formal source, raw W1 and tail
tables, independent checker output, and negative controls.

## Winning evidence

- Experiment branch:
  `orx/judge-visible-d-8-code-and-raw-evidence`
- Candidate Git SHA:
  `ca71757e2505adf2d17c2dac2a12a12381db3cd3`
- Formal run:
  `3533c8cd-f080-4076-aee3-64ae49792f7f`
- Fixed command:
  `uv run python repro/src/verify_sgd.py`
- Formal orchestrated runtime:
  13m33s
- Compute:
  local 8-core arm64 CPU
- Hugging Face CPU:
  not used because local CPU was sufficient
- GPU:
  none
- Direct compute cost:
  $0

## Claim-by-claim result and forecast

The scientific verdicts are finite-contract results, not universal theorem
proofs. The conservative projected total remains **9–10/12**, and the
best-supported possible score is **10/12 as a forecast**, not a judge result.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 1 | 2 | HIGH | VERIFIED | Six d=8 i.i.d./Markov model families, five stepsizes, held-out rate envelopes, and wrong-rate controls; finite separable systems remain narrower than the theorem |
| 2 | 1 | 2 | HIGH | VERIFIED | Smooth strongly convex nonquadratic d=8 SGD; slope 0.539; held-out paper-rate envelope passes and O(alpha) fails |
| 3 | 1 | 2 | HIGH | VERIFIED | d=8 Hurwitz and globally contractive systems; slopes 0.494 and 0.421; held-out envelopes and controls pass |
| 4 | 1 | 2 | HIGH | VERIFIED | 960 i.i.d. tail rows, exact Clopper–Pearson intervals, four thresholds, exact paper rate, and wrong-rate rejection |
| 5 | 1 | 2 | HIGH | VERIFIED | Three d=8 Markov systems plus 960 tail rows; wrong i.i.d. covariance and wrong rate both rejected |
| 6 | 0 | 0 | HIGH | BLOCKED | Four materially different routes found unresolved conjectures and inconsistent printed drift/density; no valid exact verification or falsification |

Only the live judge can change the current 5/12.

## Judge criticisms answered

The published reader-visible cells replace the evidence basis criticized by
the judge with:

- three assumption-satisfying d=8 model classes under i.i.d. and Markov noise;
- five stepsizes and four deterministic seeds;
- 32,768 retained states per seed and stepsize for Claims 1–5;
- three coarse calibration steps and two held-out fine steps;
- empirical slopes and explicit paper-rate normalization;
- exact two-sided 95% Clopper–Pearson projection-tail intervals;
- 960 tail rows for Claim 4 and 960 Markov tail rows for Claim 5;
- simulator-independent recomputation from serialized CSV;
- six negative controls and 12 mutation tests that all reject corruption;
- a 985-line attached formal verifier source visible to the agent reader.

No toy result is described as full-scale.

## Published transaction

The user approved exactly 17 text paths. A Hugging Face commit API transaction
used `887693a544629b31b7c6dc141fa321a9fcdb5948` as the required parent and
created:

`643bd5022b83d9c13488bbb9f4c8ec629cd795f9`

The exact revision was redownloaded and independently verified:

- 17/17 approved upload hashes match;
- 92/92 protected judged paths remain present;
- 91/91 protected paths other than `logbook.json` are byte-identical;
- `logbook.json` is the only existing path replaced;
- the final Space contains 108 paths;
- the live Trackio reader reports `judge-visible-evidence` with 10 cells;
- the formal source payload contains 985 attached lines.

## Exact upload allowlist

```text
evidence/judge-visible/judge_verdict.json
evidence/judge-visible/source/independent_check.py
evidence/judge-visible/source/research_campaign.py
evidence/judge-visible/source/verify_claim_artifacts.py
evidence/judge-visible/source/verify_sgd.py
evidence/protected/judged_space_887693a_manifest.sha256
logbook.json
pages/judge-visible-evidence/claim-1.md
pages/judge-visible-evidence/claim-2.md
pages/judge-visible-evidence/claim-3.md
pages/judge-visible-evidence/claim-4.md
pages/judge-visible-evidence/claim-5.md
pages/judge-visible-evidence/claim-6.md
pages/judge-visible-evidence/controls.md
pages/judge-visible-evidence/formal-run.md
pages/judge-visible-evidence/independent-check.md
pages/judge-visible-evidence/page.md
```

The per-path SHA-256 values are in `release/hf_upload_manifest.sha256`.

## Reproducibility and provenance

- Paper:
  `https://arxiv.org/abs/2602.13960`
- Paper HTML:
  `https://ar5iv.labs.arxiv.org/html/2602.13960`
- Retrieved:
  2026-07-23 with explicit User-Agent
- Paper SHA-256:
  `ba012ad708927c13fab0ef54d35a3b8fb693451cfae9000e430e1329ed48dcab`
- Baseline Git SHA:
  `598e7084fae9935b26a2cb68b4daa0a74aab0066`
- Current verdict selection:
  `space_id == "DineshAI/m4TAzup6Yc"`
- Previous exact judged Space:
  `DineshAI/m4TAzup6Yc@887693a544629b31b7c6dc141fa321a9fcdb5948`

The theorem anchors, assumptions, domains, quantifiers, finite contracts,
limitations, and four Claim 6 routes are recorded under
`.openresearch/artifacts/`.

## Commands

Formal reproduction:

```bash
uv sync --frozen
uv run python repro/src/verify_sgd.py
orx exp run 054b5f47-c5ff-44d3-8e6c-98a6f1c0d963 --backend local
orx exp wait 054b5f47-c5ff-44d3-8e6c-98a6f1c0d963 --timeout 480
orx logs 3533c8cd-f080-4076-aee3-64ae49792f7f
```

Candidate and publication verification:

```bash
uv run python release/verify_candidate.py --judged-dir /tmp/orx-space-887693a-IFwVgH
shasum -a 256 -c release/hf_upload_manifest.sha256
hf download DineshAI/m4TAzup6Yc --repo-type space --revision 643bd5022b83d9c13488bbb9f4c8ec629cd795f9
uv run trackio logbook read --path DineshAI/m4TAzup6Yc pages
uv run trackio logbook read --path DineshAI/m4TAzup6Yc page judge-visible-evidence
uv run trackio logbook read --path DineshAI/m4TAzup6Yc cell cell_jv_formal_run --full
git diff --check
git status --short
git ls-remote origin refs/heads/master
```

## Reader-facing artifacts

- Illustrated report:
  `reports/sgd-steady-state-reproduction/report.md`
- Self-contained tutorial:
  `notebooks/sgd_steady_state_reproduction.py`
- Durable evidence:
  `.openresearch/artifacts/`
- Published Space overlay:
  `release/hf-space-overlay/`
- Upload allowlist:
  `release/hf_upload_allowlist.txt`
- Upload manifest:
  `release/hf_upload_manifest.sha256`
- Old/new subset proof:
  `release/old_new_subset_check.json`
- Immutable publication receipt:
  `release/published_revision.json`

## Awaiting judge

The existing Space is updated and the exact published text paths are mirrored
in the Git history. This release is marked **awaiting judge**. The current
score remains **5/12** unless and until a live verdict for
`643bd5022b83d9c13488bbb9f4c8ec629cd795f9` is produced.
