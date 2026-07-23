# Source audit — Claim 3

Audited source: `https://ar5iv.labs.arxiv.org/html/2602.13960`, retrieved with
the explicit User-Agent recorded in `.openresearch/protected/source_registry.json`
at `2026-07-23T16:22:07Z`; source SHA-256
`ba012ad708927c13fab0ef54d35a3b8fb693451cfae9000e430e1329ed48dcab`.

Proposition 3.2 is at `S3.Thmproposition2`, under iid Assumption 3.1 and the
Hurwitz Assumption 3.4. Proposition 3.3 is at `S3.Thmproposition3`, under
Assumption 3.5: global strict contraction in a weighted Euclidean norm and
bounded component Hessians. The old quartic SGD example did not establish this
contractivity condition; the tanh operator used here does.
