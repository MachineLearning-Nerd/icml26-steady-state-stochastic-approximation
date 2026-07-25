# Judge-visible controls


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_jv_controls", "created_at": "2026-07-25T06:00:00+00:00", "title": "Negative controls and mutation tests"}
-->
## Failure-sensitive checks

| claim | negative-control result |
| --- | --- |
| claim_1 | {"control": "O(alpha) W1 envelope across all six iid/Markov families", "detected_as_wrong": true, "expected_to_pass": false, "observed_families_passing": 0} |
| claim_2 | {"control": "O(alpha) W1 envelope for iid smooth strongly convex SGD", "control_pass": false, "expected_to_pass": false} |
| claim_3 | {"control": "O(alpha) W1 envelope for iid linear and contractive SA", "control_passes": {"contractive": false, "linear": false}, "expected_to_pass": false} |
| claim_4 | {"control": "O(alpha) projection-tail envelope", "control_pass": false, "expected_to_pass": false} |
| claim_5 | {"controls": {"O(alpha)_Markov_tail_envelope": {"control_pass": false, "expected_to_pass": false}, "iid_covariance_substituted_for_long_run_covariance": {"control_pass": false, "expected_to_pass": false}}} |
| claim_6 | {"controls": {"literal_main_text_density": {"expected_to_match": false, "rejected": true}, "wrong_sqrt_scaling": {"expected_to_stabilize": false, "rejected": true}}} |

The mutation suite changes every verdict and every independent-check status in
a temporary artifact copy. All 12 corruptions return nonzero:
`passed=true`.

[Full mutation output](../../evidence/verifier_selftest.json) ·
[formal verifier source](../../evidence/judge-visible/source/research_campaign.py) ·
[independent checker source](../../evidence/judge-visible/source/independent_check.py)
