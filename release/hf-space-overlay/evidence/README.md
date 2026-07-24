# Claim evidence layout

The fixed command `uv run python repro/src/verify_sgd.py` regenerates the raw
CSV/JSON evidence, executes the independent and negative-control checks, writes
each claim's `EVAL.md`, and returns nonzero if a numeric Claim 1–5 contract
fails. The log prints every generated text artifact with a SHA-256 digest
because OpenResearch local mode retains logs as the evidence channel.

The paper source is ar5iv HTML SHA-256
`ba012ad708927c13fab0ef54d35a3b8fb693451cfae9000e430e1329ed48dcab`,
retrieved 2026-07-23 with an explicit User-Agent. The exact judged Space
revision and source registry are preserved under `.openresearch/protected/`.
