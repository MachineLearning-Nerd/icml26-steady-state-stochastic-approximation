# Claim 6 verification routes

## Exact contract shared by all routes

Proposition 5.1 (`S5.Thmproposition1`) states, in one dimension and for even
`h`, that **conditional on Assumptions 5.1–5.2 and Conjectures 5.1–5.2**, there
are finite constants `U_5` and `alpha_5>0` such that for every
`alpha in (0,alpha_5)`,

`d_W((X^(alpha)-x*)/alpha^(1/h), Y) <= U_5 alpha^(1/h)`.

The source is the explicitly User-Agent-retrieved ar5iv HTML at
`https://ar5iv.labs.arxiv.org/html/2602.13960`, retrieved
`2026-07-23T16:22:07Z`, SHA-256
`ba012ad708927c13fab0ef54d35a3b8fb693451cfae9000e430e1329ed48dcab`.
The exact source registry is `.openresearch/protected/source_registry.json`.

## Route 1 — source-logic and quantifier audit

- Interpretation: treat every printed premise, formula, and quantifier
  literally.
- Method: compare Assumptions 5.1–5.2, Conjectures 5.1–5.2, Proposition 5.1,
  Appendix E, and Section 6 in the retrieved source.
- Command/source path: `orx paper 2602.13960 --full` plus the hashed ar5iv
  source above.
- Result: the proposition is conditional on two unproved conjectures; Section
  6 explicitly leaves them for future work. Conjecture 5.2 prints drift
  `-y^h`, whereas the scaling and Appendix E use `-y^(h-1)`. The proposition's
  density coefficient differs from Appendix E by `(h-1)!`.
- Resolution: this route blocks a strict verification and prevents replacing
  the printed result with a corrected nearby claim.

## Route 2 — scaling-exponent experiment

- Interpretation: test the rate component intended by the proposition,
  independently of the disputed target-density coefficient.
- Method: for `f(x)=x^h/h`, run `h=4` and `h=6`, four stepsizes, four
  deterministic seeds, and fit the standard deviation of unscaled `X` against
  `alpha`. The square-root scaling is a negative control.
- Exact fixed command: `uv run python repro/src/verify_sgd.py`.
- Result: observed slopes are `0.2493367` for `h=4` (target `0.25`) and
  `0.1685687` for `h=6` (target `1/6`). Correctly scaled standard-deviation
  coefficients of variation are below `0.009`; the square-root control does
  not stabilize.
- Resolution: substantial support for the intended `alpha^(1/h)` scaling, but
  it cannot prove the conjectural premises for the full objective class.

## Route 3 — distributional target discrimination

- Interpretation: compare the literal Proposition 5.1 density and the
  Appendix-E density as distinct candidate claims.
- Method: compute exact generalized-Gaussian quantiles for both candidates and
  measure empirical Wasserstein-1 distance using the same fixed run. A separate
  CSV parser recomputes the fine-stepsize ratios.
- Exact fixed command: `uv run python repro/src/verify_sgd.py`.
- Result: at the two fine stepsizes, the literal target is at least `7.50x`
  farther than the Appendix-E target for `h=4` and `18.05x` farther for `h=6`.
  The literal-density negative control is rejected.
- Resolution: the data discriminate strongly in favor of the intended
  Appendix-E law, but this is evidence about a corrected interpretation, not a
  verification of the exact printed proposition.

## Route 4 — exact-statement falsification attempt

- Restated domain and assumptions: one-dimensional constant-stepsize SA,
  even `h`, Assumptions 5.1–5.2, Conjectures 5.1–5.2, and every sufficiently
  small `alpha`.
- Counterexample sought: `f(x)=x^h/h` with `h in {4,6}` and bounded centered
  variance-one skew noise. These models satisfy the explicit smoothness,
  convexity, growth, and noise conditions and sharply reject the literal
  displayed density while matching the Appendix-E density.
- Independent check: `uv run python repro/src/independent_check.py --claim 6`
  recomputes both scaling exponents and the literal-versus-intended W1
  separation solely from serialized CSV evidence.
- Negative controls: the wrong square-root scaling and literal target density
  are both required to be rejected; the artifact verifier exits nonzero when
  either rejection record is corrupted.
- Why falsification did not succeed: a valid falsification must satisfy every
  premise. The printed Conjecture 5.2 and the proposition/Appendix-E dynamics
  do not define one consistent premise set, and the conjectures themselves are
  unproved. Treating the intended corrected dynamics as a premise would
  falsify the printed density, but would no longer test the exact printed
  conjunction.
- Verdict after route 4: **BLOCKED**, not FALSIFIED. An author erratum fixing
  the drift, density coefficient, and moment statement—or a proof under one
  explicit corrected formulation—would unblock a strict verdict.
