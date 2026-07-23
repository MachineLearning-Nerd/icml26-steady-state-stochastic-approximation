# Method — Claim 1

Use eight independent coordinates with bounded, centered, variance-one skew
two-point noise. For Markov noise, each coordinate is a stationary two-state
refresh chain with autocorrelation `rho^m`; their product is finite-state and
uniformly ergodic. Five alpha values and four deterministic seeds are used.

For product laws under Euclidean cost,
`max_i W1_i <= W1_d <= sum_i W1_i`. Coordinate W1 values use empirical and
Gaussian quantiles. A constant is calibrated only on the three coarsest alpha
values and checked on two held-out smaller values. A separate Gaussian
linear-SA calculation uses the exact finite-alpha covariance and `W1 <= W2`.
