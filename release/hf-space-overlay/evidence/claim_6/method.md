# Method — Claim 6

For `f(x)=x^h/h`, simulate the scaled recursion directly with effective Euler
step `delta=alpha^(2-2/h)`. Test `h=4` and `h=6`, four alpha values, and four
seeds. Fit the standard deviation of unscaled `X` against alpha, measure the
coefficient of variation after `alpha^(1/h)` scaling, and compute W1 against
both the intended Appendix-E Gibbs quantiles and the literal main-text density.
The wrong square-root scaling is a negative control.
