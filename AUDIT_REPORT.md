# Claim audit

## Decision

The evidence-release gate passes for the committed finite contracts. Claims
1–5 are VERIFIED_SCOPED. Claim 6 is BLOCKED. The overall repository status is
MIXED_RESULTS and the strict universal paper-claim gate is NOT_READY.

The independent checker parses serialized CSV evidence rather than importing
the simulator. The historical root outputs/verdict.json is retained for
lineage; it reports the earlier 1D toy run and is not the authoritative
current d=8 decision.

## Claim-by-claim audit

| Claim | Target | Producer | Independent check | Result | Boundary |
| --- | --- | --- | --- | --- | --- |
| C1 | Gaussian Wasserstein rate for i.i.d. and Markov noise | repro/src/research_campaign.py plus verify_claim_artifacts.py --claim 1 | repro/src/independent_check.py --claim 1 | VERIFIED_SCOPED; six d=8 model/noise families pass held-out envelopes; slopes 0.421–0.558 | Finite d=8 separable systems and a rigorous product-law W1 bracket |
| C2 | Smooth strongly convex SGD rate | research_campaign.py SGD family and claim-2 verifier | independent CSV parser for claim 2 | VERIFIED_SCOPED; nonquadratic d=8 slope 0.539; paper-rate holdout passes and O(alpha) control fails | One committed objective and bounded skew noise |
| C3 | Hurwitz linear and contractive nonlinear SA | research_campaign.py linear/tanh families and claim-3 verifier | independent CSV parser plus analytic checks | VERIFIED_SCOPED; linear slope 0.494 and contractive slope 0.421 | Diagonal d=8 matrix and gamma_i tanh(x_i) family |
| C4 | Projection-tail and Berry–Esseen behavior | research_campaign.py tail rows and claim-4 verifier | exact Clopper–Pearson recomputation from serialized counts | VERIFIED_SCOPED; 960 i.i.d. rows and wrong O(alpha) control fails | Four directions, four thresholds, five stepsizes |
| C5 | Markovian extension | research_campaign.py refresh-chain route and claim-5 verifier | independent W1/tail parser and covariance control | VERIFIED_SCOPED; all three model classes and 960 Markov tail rows pass | Product of eight finite-state refresh chains with rho=0.55 |
| C6 | Gibbs limit near flat convex minima | research_campaign.py and the four routes in claim_6/routes.md | claim-6 source and route audits | BLOCKED; intended h=4/h=6 scaling is supported, exact printed proposition is not | Unresolved conjectural premises and conflicting printed formulas |

## Claim 6 blocker

The evidence supports the intended alpha^(1/h) scaling, but no VERIFIED
verdict is allowed because:

1. Proposition 5.1 is conditional on Conjectures 5.1–5.2, which remain open.
2. Conjecture 5.2 prints drift -y^h while the scaling argument and Appendix E
   use -y^(h-1).
3. The proposition's density coefficient differs from Appendix E by
   (h-1)!.
4. The literal-density route finds a mismatch but cannot call it a complete
   falsification while the printed premises do not define one consistent
   model.

## Integrity checks

- The paper-source SHA matches the source registry and claim source audits.
- Claims 1–5 have claim contracts, raw CSV, independent checks, and negative
  controls.
- The formal publication candidate was re-downloaded and its approved paths
  were hash-checked.
- No universal theorem is represented as proved by the finite campaign.
- The prior live score is reported separately from the local evidence result.

## Status vocabulary

| Status | Meaning |
| --- | --- |
| VERIFIED_SCOPED | Finite machine contract and independent checks pass within stated scope |
| BLOCKED | Required source, premise, or consistency condition prevents a defensible verdict |
| FALSIFIED | A contract-level counterexample satisfies the stated premises and breaks the target |
| NOT_READY | Evidence is insufficient for the stronger universal claim |

## Reproduction entrypoint

```bash
uv sync --frozen
uv run python repro/src/verify_sgd.py
```
