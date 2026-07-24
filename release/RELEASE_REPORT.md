# Publication release report

**Status:** published to the existing Space; **awaiting judge**.

**Previous live judged score:** 6/12.

**Judged Space and judge head:** `847472e15337044d0adb3e636ebbcf7614f0cd34`.

**Target Space:** `DineshAI/m4TAzup6Yc` (the existing Space only).

**Published HF revision:** `887693a544629b31b7c6dc141fa321a9fcdb5948`.

## Winning evidence

- Experiment branch:
  `orx/final-additive-publication-candidate`
- Scientific Git SHA:
  `a75d96d2fd051c33e80f1bb92870e6afb6ee42f6`
- Exact-interval run:
  `900dc3d7-2e2c-4bb4-922d-feb16b446db9`
- Publication assembly Git SHA:
  `8867787f7b7927eb1ba7a07ae03498ebb9937f6e`
- Publication assembly regression:
  `a3fe8f73-2a3e-4a55-8367-aebfd951005c`
- Fixed command:
  `uv run python repro/src/verify_sgd.py`
- Exact-interval verifier wall time:
  340.377 seconds
- Publication assembly verifier wall time:
  656.085 seconds
- Publication assembly orchestrated runtime:
  12m37s
- Total formal experiment time through publication assembly:
  67m39s
- Compute:
  local 8-core arm64 CPU
- Hugging Face CPU:
  not used because local CPU was sufficient
- GPU:
  none
- Direct compute cost:
  $0

## Experiment tree

| Node | Git SHA | Main decision | Result | Runtime |
| --- | --- | --- | --- | ---: |
| Baseline: judged 1D toy reproduction | `7ab5361` | Freeze the prior environment and result | Toy baseline reproduced | 20s |
| Faithful d=8 contracts | `5cac01e` | Replace arbitrary thresholds with assumption-sensitive rate contracts | Exposed i.i.d. W1 sampling floor | 1m20s |
| High-precision i.i.d. W1 | `46216e7` | Increase only the Gaussian ensemble | All six W1 rates resolve | 14m15s |
| Durable evidence gate | `47c8401` | Add independent recomputation and corruption tests | All claim checkers pass | 20m44s |
| Reader-facing evidence | `c8788df` | Add reproducible figure generation | Scientific gate and figures pass | 10m40s |
| Exact tail intervals | `a75d96d` | Replace approximate tail intervals with exact Clopper-Pearson intervals | Scientific winner | 7m43s |
| Publication assembly | `8867787` | Add report, notebook, additive Space overlay, and release manifests | Unchanged cumulative regression passes | 12m37s |

## Claim-by-claim result

| Claim | Exact result | Core evidence | Remaining limitation |
| --- | --- | --- | --- |
| 1 | **VERIFIED** within the finite contract | Six d=8 family/noise combinations pass held-out paper-rate envelopes; slopes 0.421–0.558; six wrong O(alpha) controls fail | Finite d=8 systems do not prove the universal theorem |
| 2 | **VERIFIED** | Nonquadratic globally smooth strongly convex d=8 SGD; slope 0.539; held-out rate passes | One assumption-satisfying objective family |
| 3 | **VERIFIED** | d=8 Hurwitz linear slope 0.494 and global-contraction slope 0.421; controls fail | Separable systems |
| 4 | **VERIFIED** | 960 i.i.d. tail rows; exact 95% Clopper-Pearson bounds; held-out 0.01463 below 0.02925 calibration | Finite directions and positive thresholds |
| 5 | **VERIFIED** | Three d=8 Markov models and 960 tail rows; held-out 0.02652 below 0.07699; wrong covariance rejected | One uniformly ergodic finite-state chain |
| 6 | **BLOCKED** after four routes | Intended h=4/h=6 slopes match; literal density is rejected by 7.50x/18.05x W1 diagnostics | Proposition is conditional and internally inconsistent, so no route can satisfy every printed premise |

Every claim directory contains `claim_contract.json`, `source_audit.md`,
`method.md`, raw CSV, `verdict.json`, an independent checker result, a negative
control, runtime metadata, `EVAL.md`, and limitations. Claim 6 additionally
contains the four-route record.

## Judge criticisms answered

The candidate replaces the earlier 1D, 2,000–3,000-sample, arbitrary-threshold
checks with:

- three faithful d=8 model classes under both i.i.d. and Markov noise;
- five stepsizes and four deterministic seeds;
- 32,768 retained states per seed and stepsize;
- coarse-step calibration with two held-out fine stepsizes;
- explicit wrong-rate and wrong-covariance controls;
- exact binomial confidence intervals for projection tails;
- simulator-independent recomputation from serialized CSV;
- nonzero exit behavior for every failed contract;
- 12 verifier mutation tests, all of which reject corrupted evidence.

No toy result is relabeled as full-scale. The report explicitly limits the
conclusions to the committed finite experimental contracts.

## Source and baseline provenance

- Paper HTML:
  `https://ar5iv.labs.arxiv.org/html/2602.13960`
- Retrieval:
  2026-07-23 with an explicit browser User-Agent
- Paper SHA-256:
  `ba012ad708927c13fab0ef54d35a3b8fb693451cfae9000e430e1329ed48dcab`
- Baseline repository SHA:
  `598e7084fae9935b26a2cb68b4daa0a74aab0066`
- Live verdict selection:
  `space_id == "DineshAI/m4TAzup6Yc"`
- Verdict dataset revision:
  `047e821a412e22da0c6fa8a4b9b78a3ca9096dbf`
- Exact judged Space:
  `DineshAI/m4TAzup6Yc@847472e15337044d0adb3e636ebbcf7614f0cd34`

The theorem and proposition anchors, assumptions, domains, and quantifiers are
recorded in each `source_audit.md` and in
`.openresearch/protected/source_registry.json`.

## Commands

Startup and source audit:

```bash
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx project view b4caaa09-e6ff-4cdd-9c8a-7d1e5870458d
orx runs b4caaa09-e6ff-4cdd-9c8a-7d1e5870458d
git branch -a
git rev-parse HEAD
git status --short
df -h .
env | cut -d= -f1 | sort
curl -L -A "OpenResearch-Reproduction/1.0" https://ar5iv.labs.arxiv.org/html/2602.13960
hf download ICML-2026-agent-repro/verdicts --repo-type dataset --revision 047e821a412e22da0c6fa8a4b9b78a3ca9096dbf
hf download DineshAI/m4TAzup6Yc --repo-type space --revision 847472e15337044d0adb3e636ebbcf7614f0cd34
```

Environment and formal runs:

```bash
uv sync --frozen
uv run python repro/src/verify_sgd.py
orx exp run <experiment-id> --backend local
orx exp wait <experiment-id> --interval 300 --timeout 480
orx logs <run-id> --bytes 1000000
```

The fixed Python command is identical on every node; the experiment IDs and
run IDs are recorded in the OpenResearch tree and the table above.

Candidate validation:

```bash
uv run marimo check notebooks/sgd_steady_state_reproduction.py
uv run python release/verify_candidate.py --judged-dir /tmp/orx-judged-space-847472e-candidate
git diff --check
git status --short
git rev-parse HEAD
git ls-remote origin
```

The approved 76-path text transaction was committed through the Hugging Face
commit API with the previous judged revision as its required parent.

## Reader-facing artifacts

- Illustrated report:
  `reports/sgd-steady-state-reproduction/report.md`
- Report figures:
  `reports/sgd-steady-state-reproduction/images/`
- Self-contained tutorial:
  `notebooks/sgd_steady_state_reproduction.py`
- Durable evidence:
  `.openresearch/artifacts/`
- Space overlay:
  `release/hf-space-overlay/`
- Upload allowlist:
  `release/hf_upload_allowlist.txt`
- Upload SHA-256 manifest:
  `release/hf_upload_manifest.sha256`
- Old/new subset proof:
  `release/old_new_subset_check.json`

## Protected logbook subset check

The verifier passes with:

- 17/17 protected old paths present;
- 16/16 old paths other than `logbook.json` byte-identical;
- all five previous navigation children preserved in order;
- only `logbook.json` replaced, solely to append the new branch;
- 75 additive paths;
- 92 paths in the virtual candidate;
- 15/15 navigation targets present;
- 76/76 overlay paths valid UTF-8 with text-only suffixes;
- no configured secret-like pattern detected.

The published revision was then redownloaded and independently checked:

- 92/92 remote paths accounted for;
- 17/17 protected old paths present;
- 16/16 old non-navigation paths byte-identical;
- 76/76 approved uploaded paths match the SHA-256 manifest.

## Exact Hugging Face upload allowlist

Only the following text paths are authorized for the proposed upload:

```text
evidence/README.md
evidence/claim_1/EVAL.md
evidence/claim_1/claim_contract.json
evidence/claim_1/independent_checker_output.json
evidence/claim_1/limitations.md
evidence/claim_1/method.md
evidence/claim_1/negative_control_output.json
evidence/claim_1/raw_metrics.csv
evidence/claim_1/runtime.json
evidence/claim_1/source_audit.md
evidence/claim_1/verdict.json
evidence/claim_2/EVAL.md
evidence/claim_2/claim_contract.json
evidence/claim_2/independent_checker_output.json
evidence/claim_2/limitations.md
evidence/claim_2/method.md
evidence/claim_2/negative_control_output.json
evidence/claim_2/raw_metrics.csv
evidence/claim_2/runtime.json
evidence/claim_2/source_audit.md
evidence/claim_2/verdict.json
evidence/claim_3/EVAL.md
evidence/claim_3/claim_contract.json
evidence/claim_3/independent_checker_output.json
evidence/claim_3/limitations.md
evidence/claim_3/method.md
evidence/claim_3/negative_control_output.json
evidence/claim_3/raw_metrics.csv
evidence/claim_3/runtime.json
evidence/claim_3/source_audit.md
evidence/claim_3/verdict.json
evidence/claim_4/EVAL.md
evidence/claim_4/claim_contract.json
evidence/claim_4/independent_checker_output.json
evidence/claim_4/limitations.md
evidence/claim_4/method.md
evidence/claim_4/negative_control_output.json
evidence/claim_4/raw_metrics.csv
evidence/claim_4/runtime.json
evidence/claim_4/source_audit.md
evidence/claim_4/verdict.json
evidence/claim_5/EVAL.md
evidence/claim_5/claim_contract.json
evidence/claim_5/independent_checker_output.json
evidence/claim_5/limitations.md
evidence/claim_5/method.md
evidence/claim_5/negative_control_output.json
evidence/claim_5/raw_metrics.csv
evidence/claim_5/raw_tail_metrics.csv
evidence/claim_5/runtime.json
evidence/claim_5/source_audit.md
evidence/claim_5/verdict.json
evidence/claim_6/EVAL.md
evidence/claim_6/claim_contract.json
evidence/claim_6/independent_checker_output.json
evidence/claim_6/limitations.md
evidence/claim_6/method.md
evidence/claim_6/negative_control_output.json
evidence/claim_6/raw_metrics.csv
evidence/claim_6/routes.md
evidence/claim_6/runtime.json
evidence/claim_6/source_audit.md
evidence/claim_6/verdict.json
evidence/protected/judged_space_847472e_manifest.sha256
evidence/protected/source_registry.json
evidence/verifier_selftest.json
logbook.json
pages/rigorous-reproduction/claim-1.md
pages/rigorous-reproduction/claim-2.md
pages/rigorous-reproduction/claim-3.md
pages/rigorous-reproduction/claim-4.md
pages/rigorous-reproduction/claim-5.md
pages/rigorous-reproduction/claim-6.md
pages/rigorous-reproduction/method.md
pages/rigorous-reproduction/page.md
pages/rigorous-reproduction/release-evidence.md
```

The exact SHA-256 of each upload path is in
`release/hf_upload_manifest.sha256`. Existing binary assets are neither
uploaded nor deleted.

## Publication record

The user approved the exact action described above. The existing Space was
updated at revision `887693a544629b31b7c6dc141fa321a9fcdb5948`, the remote
tree passed the hash and subset checks, and the release is marked
`awaiting_judge`. The exact receipt is in `release/published_revision.json`.

Publication is not evidence of a score change. The score remains 6/12 unless
and until the live judge publishes a new verdict.
