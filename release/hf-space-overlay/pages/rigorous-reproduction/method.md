# Method and release gate

## Fixed execution contract

- Command: `uv run python repro/src/verify_sgd.py`
- Environment: Python 3.12.11, NumPy 2.5.1, SciPy 1.18.0
- Seeds: 1729, 2718, 3141, 5772
- Compute: local 8-core arm64 CPU
- GPU use: none
- Hugging Face compute: none
- Direct compute cost: $0
- Evidence SHA: `a75d96d2fd051c33e80f1bb92870e6afb6ee42f6`
- Exact-interval run: `900dc3d7-2e2c-4bb4-922d-feb16b446db9`

All experiment nodes inherit the same command and one locked repository-level
uv environment. Variants are committed code changes rather than command-line
knobs.

## Experimental systems

The campaign uses three separable d=8 systems:

1. globally smooth, strongly convex, nonquadratic SGD;
2. linear SA with a diagonal Hurwitz matrix;
3. nonlinear SA with a globally contractive tanh map.

The i.i.d. innovation is a bounded, centered, variance-one skew two-point law.
The Markov innovation is a stationary finite-state refresh chain with
rho=0.55, known long-run variance, uniform ergodicity, and bounded Poisson
solutions.

For each of five stepsizes, each seed retains 4,096 stationary chains in eight
separated batches. The product-law coordinate W1 values yield a rigorous
bracket on Euclidean multivariate W1; the upper bracket is used for acceptance.

## Failure-sensitive evidence

An independent checker imports no simulator code and reconstructs the claim
contracts from raw CSV. Negative controls use deliberately wrong O(alpha)
rates or the wrong Markov covariance. The release self-test mutates every
claim's verdict and independent-check status; all 12 corruptions exit nonzero.

Source conditions, exact quantifiers, deviations, and limitations are recorded
inside each claim evidence directory.
