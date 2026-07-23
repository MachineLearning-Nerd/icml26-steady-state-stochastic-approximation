# Source audit — Claim 6

Proposition 5.1 is at `S5.Thmproposition1` and is explicitly conditional on
Assumptions 5.1–5.2 and **Conjectures** 5.1–5.2. Section 6 says completing those
conjectures is future work.

There are material source conflicts:

- Conjecture 5.2 displays drift `-y^h`, implying a potential of order `h+1`,
  while Proposition 5.1 and the intended scaling require drift `-y^(h-1)`.
- Proposition 5.1 prints density
  `exp[-2 f^(h)(x*) y^h / (h E xi^2)]`; Appendix E uses the coefficient
  `2 f^(h)(x*)/h!`, differing by `(h-1)!`.
- Conjecture 5.1 states an unscaled moment bound, while Appendix E invokes
  bounded moments of the scaled law.

Accordingly, the exact proposition is not silently replaced by the corrected
Appendix-E interpretation.
