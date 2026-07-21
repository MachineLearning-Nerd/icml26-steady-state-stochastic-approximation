# Claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_b9360ece0c79", "created_at": "2026-07-21T14:34:52+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. Theorem 3.1 (i.i.d. noise) and Theorem 4.1 (Markovian noise) bound the Wasserstein distance between the centered-scaled steady state Y^(α) = (X^(α) − x*)/√α and its Gaussian limit N(0, Σ_Y) by U√α log(1/α) (Theorems 3.1 and 4.1).
2. Proposition 3.1 establishes an explicit non-asymptotic Wasserstein bound of order O(α^{1/2} log(1/α)) for constant-stepsize SGD on smooth, strongly convex objectives (Proposition 3.1).
3. Propositions 3.2 and 3.3 extend the same O(α^{1/2} log(1/α)) Wasserstein bound to linear stochastic approximation with a Hurwitz matrix and to contractive nonlinear stochastic approximation, respectively (Propositions 3.2 and 3.3, Section 3.2.2, Section 3.2.3).
4. For one-dimensional projections, the paper derives a non-uniform Berry-Esseen-type tail bound |P(⟨Y^(α),ζ⟩ > a) − P(Z_ζ > a)| ≤ C_d α^{1/4} log^{1/2}(1/α) / a, which improves as the deviation level a grows (Section 4).
5. Proposition 4.1 extends the Gaussian approximation and tail bounds for SGD, linear SA, and contractive nonlinear SA from i.i.d. noise to Markovian noise (Proposition 4.1, Section 4).
6. Proposition 5.1 shows a different convergence rate of order α^{1/h} for constant-stepsize SA applied to general convex objectives with Gibbs-type limiting distributions (Proposition 5.1, Section 5).
