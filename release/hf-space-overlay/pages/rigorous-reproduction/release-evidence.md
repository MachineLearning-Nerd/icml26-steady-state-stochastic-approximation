# Release evidence

## Immutable judged baseline

- Space: `DineshAI/m4TAzup6Yc`
- Judged revision: `847472e15337044d0adb3e636ebbcf7614f0cd34`
- Previous live score: 6/12
- Protected paths: 17/17 remain in the virtual candidate tree
- Existing claim, evidence, and conclusion pages: unchanged

Only `logbook.json` is updated to append this new navigation branch. No
existing page or evidence file is deleted or overwritten.

## Reproducibility

- Paper source SHA-256:
  `ba012ad708927c13fab0ef54d35a3b8fb693451cfae9000e430e1329ed48dcab`
- Evidence Git SHA:
  `a75d96d2fd051c33e80f1bb92870e6afb6ee42f6`
- Fixed command: `uv run python repro/src/verify_sgd.py`
- Formal experiment runtime through the exact-interval winner: 55m02s
- Final verifier wall time at that winner: 340.377 seconds
- Hardware: local 8-core arm64 CPU
- GPU and paid remote compute: none

The upload manifest, old/new subset check, and exact text allowlist are part of
the repository release record. Publication does not itself change the score;
only a later live judge can do that.
