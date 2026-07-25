# Judge-visible independent checker


---
<!-- trackio-cell
{"type": "code", "id": "cell_jv_independent", "created_at": "2026-07-25T06:00:00+00:00", "title": "Independent CSV checker: source and output", "command": ["uv", "run", "python", "repro/src/verify_sgd.py"], "exit_code": 0, "duration_s": 1.0}
-->
````bash
$ uv run python repro/src/verify_sgd.py
````

````python title=independent_check.py
"""Independent, claim-specific checks over emitted CSV evidence.

This module intentionally does not import the simulator.  It recomputes the
acceptance diagnostics from the serialized evidence using a separate code path.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

from scipy.stats import beta as beta_distribution


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def slope(xs: list[float], ys: list[float]) -> float:
    lx = [math.log(x) for x in xs]
    ly = [math.log(max(y, 1e-12)) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    numerator = sum((x - mx) * (y - my) for x, y in zip(lx, ly, strict=True))
    denominator = sum((x - mx) ** 2 for x in lx)
    return numerator / denominator


def group_rows(
    rows: list[dict[str, str]], keys: tuple[str, ...]
) -> dict[tuple[str, ...], list[dict[str, str]]]:
    grouped: dict[tuple[str, ...], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(tuple(row[key] for key in keys), []).append(row)
    return grouped


def check_w1_groups(
    rows: list[dict[str, str]],
) -> tuple[bool, dict[str, dict[str, Any]]]:
    details: dict[str, dict[str, Any]] = {}
    passed = True
    for key, group in group_rows(rows, ("noise", "model")).items():
        ordered = sorted(group, key=lambda row: float(row["alpha"]), reverse=True)
        alphas = [float(row["alpha"]) for row in ordered]
        coordinate_means = [float(row["coordinate_mean"]) for row in ordered]
        normalized = [
            float(row["w1_upper_ci_high"])
            / (math.sqrt(float(row["alpha"])) * math.log(1.0 / float(row["alpha"])))
            for row in ordered
        ]
        calibration = 1.5 * max(normalized[:3])
        holdout = all(value <= calibration for value in normalized[3:])
        fitted = slope(alphas, coordinate_means)
        this_pass = holdout and 0.15 <= fitted <= 1.10
        passed = passed and this_pass
        details[":".join(key)] = {
            "recomputed_loglog_slope": fitted,
            "recomputed_calibration_constant": calibration,
            "recomputed_holdout_values": normalized[3:],
            "passed": this_pass,
        }
    return passed, details


def check_tail(path: Path) -> tuple[bool, dict[str, Any]]:
    rows = read_rows(path)
    required_directions = {"axis_0", "axis_3", "mean", "alternating"}
    required_thresholds = {0.45, 0.70, 0.95, 1.20}
    required_alphas = {0.08, 0.04, 0.02, 0.01, 0.005}
    coverage = (
        len(rows) == 960
        and {row["direction"] for row in rows} == required_directions
        and {float(row["threshold"]) for row in rows} == required_thresholds
        and {float(row["alpha"]) for row in rows} == required_alphas
    )
    exact_intervals = True
    for row in rows:
        exceedances = int(row["exceedances"])
        sample_size = int(row["sample_size"])
        probability_low = (
            0.0
            if exceedances == 0
            else float(
                beta_distribution.ppf(
                    0.025,
                    exceedances,
                    sample_size - exceedances + 1,
                )
            )
        )
        probability_high = (
            1.0
            if exceedances == sample_size
            else float(
                beta_distribution.ppf(
                    0.975,
                    exceedances + 1,
                    sample_size - exceedances,
                )
            )
        )
        empirical = exceedances / sample_size
        gaussian = float(row["gaussian_tail"])
        expected_upper = max(
            abs(probability_low - gaussian),
            abs(probability_high - gaussian),
        )
        exact_intervals = exact_intervals and all(
            (
                math.isclose(
                    float(row["empirical_tail"]),
                    empirical,
                    rel_tol=1e-12,
                    abs_tol=1e-12,
                ),
                math.isclose(
                    float(row["empirical_tail_cp95_low"]),
                    probability_low,
                    rel_tol=1e-12,
                    abs_tol=1e-12,
                ),
                math.isclose(
                    float(row["empirical_tail_cp95_high"]),
                    probability_high,
                    rel_tol=1e-12,
                    abs_tol=1e-12,
                ),
                math.isclose(
                    float(row["gap_upper95"]),
                    expected_upper,
                    rel_tol=1e-12,
                    abs_tol=1e-12,
                ),
            )
        )
    rate_matches = all(
        math.isclose(
            float(row["theorem_rate"]),
            float(row["alpha"]) ** 0.25
            * math.sqrt(math.log(1.0 / float(row["alpha"])))
            / float(row["threshold"]),
            rel_tol=1e-12,
            abs_tol=1e-12,
        )
        for row in rows
    )
    coarse = [
        float(row["gap_upper95"]) / float(row["theorem_rate"])
        for row in rows
        if float(row["alpha"]) >= 0.02
    ]
    fine = [
        float(row["gap_upper95"]) / float(row["theorem_rate"])
        for row in rows
        if float(row["alpha"]) < 0.02
    ]
    calibration = 1.5 * max(coarse)
    holdout = max(fine) <= calibration
    result = coverage and exact_intervals and rate_matches and holdout
    return result, {
        "coverage_pass": coverage,
        "exact_clopper_pearson_recomputation_pass": exact_intervals,
        "rate_formula_pass": rate_matches,
        "recomputed_calibration_constant": calibration,
        "recomputed_max_holdout_normalized_upper": max(fine),
        "passed": result,
    }


def check_gibbs(path: Path) -> tuple[bool, dict[str, Any]]:
    rows = read_rows(path)
    details: dict[str, Any] = {}
    passed = True
    for (h_text,), group in group_rows(rows, ("h",)).items():
        h = int(h_text)
        ordered = sorted(group, key=lambda row: float(row["alpha"]), reverse=True)
        alphas = [float(row["alpha"]) for row in ordered]
        unscaled = [float(row["unscaled_sd"]) for row in ordered]
        fitted = slope(alphas, unscaled)
        scaled = [float(row["scaled_sd"]) for row in ordered]
        mean_scaled = sum(scaled) / len(scaled)
        scaled_cv = (
            sum((value - mean_scaled) ** 2 for value in scaled) / len(scaled)
        ) ** 0.5 / mean_scaled
        ratios = [
            float(row["w1_literal"]) / max(float(row["w1_intended"]), 1e-12)
            for row in ordered
        ]
        this_pass = (
            abs(fitted - 1.0 / h) <= 0.12
            and scaled_cv <= 0.18
            and min(ratios[-2:]) > 2.0
        )
        passed = passed and this_pass
        details[h_text] = {
            "recomputed_scaling_slope": fitted,
            "target_scaling_slope": 1.0 / h,
            "recomputed_scaled_sd_cv": scaled_cv,
            "literal_vs_intended_w1_ratio_min_fine": min(ratios[-2:]),
            "passed": this_pass,
        }
    return passed, details


def check_claim(artifacts_root: Path, claim: int) -> dict[str, Any]:
    claim_dir = artifacts_root / f"claim_{claim}"
    if claim in {1, 2, 3}:
        passed, details = check_w1_groups(read_rows(claim_dir / "raw_metrics.csv"))
        method = "independent CSV parser; recomputed W1 slopes and held-out envelopes"
    elif claim == 4:
        passed, details = check_tail(claim_dir / "raw_metrics.csv")
        method = "independent CSV parser; recomputed tail-rate formula, coverage, and held-out envelope"
    elif claim == 5:
        w1_passed, w1_details = check_w1_groups(
            read_rows(claim_dir / "raw_metrics.csv")
        )
        tail_passed, tail_details = check_tail(claim_dir / "raw_tail_metrics.csv")
        passed = w1_passed and tail_passed
        details = {"w1": w1_details, "tail": tail_details}
        method = "independent CSV parser; recomputed Markov W1 and tail contracts"
    else:
        passed, details = check_gibbs(claim_dir / "raw_metrics.csv")
        method = "independent CSV parser; recomputed h=4/h=6 scaling and both Gibbs targets"
    return {"claim": claim, "method": method, "details": details, "passed": passed}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim", type=int, choices=range(1, 7), required=True)
    parser.add_argument(
        "--artifacts-root",
        type=Path,
        default=Path(__file__).resolve().parents[2] / ".openresearch" / "artifacts",
    )
    args = parser.parse_args()
    result = check_claim(args.artifacts_root, args.claim)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
````

````output
{"claim": 1, "details": {"iid:contractive": {"passed": true, "recomputed_calibration_constant": 0.55005628555049, "recomputed_holdout_values": [0.23669373746914327, 0.24572002402627902], "recomputed_loglog_slope": 0.42112593146879745}, "iid:linear": {"passed": true, "recomputed_calibration_constant": 0.5160951040496135, "recomputed_holdout_values": [0.1853889443521312, 0.20010526922481606], "recomputed_loglog_slope": 0.4940436461006234}, "iid:sgd": {"passed": true, "recomputed_calibration_constant": 0.5487267133590934, "recomputed_holdout_values": [0.17678661685662916, 0.18527947797613317], "recomputed_loglog_slope": 0.5390136356214614}, "markov:contractive": {"passed": true, "recomputed_calibration_constant": 2.594676344111927, "recomputed_holdout_values": [0.8794974033625892, 0.8057491080513257], "recomputed_loglog_slope": 0.558038286322952}, "markov:linear": {"passed": true, "recomputed_calibration_constant": 1.9687831468838115, "recomputed_holdout_values": [0.7476514047308056, 0.6657239035323791], "recomputed_loglog_slope": 0.4958292068443084}, "markov:sgd": {"passed": true, "recomputed_calibration_constant": 1.9892773723243784, "recomputed_holdout_values": [0.7265075049120482, 0.6520467346573715], "recomputed_loglog_slope": 0.5053819974545185}}, "method": "independent CSV parser; recomputed W1 slopes and held-out envelopes", "passed": true}
{"claim": 2, "details": {"iid:sgd": {"passed": true, "recomputed_calibration_constant": 0.5487267133590934, "recomputed_holdout_values": [0.17678661685662916, 0.18527947797613317], "recomputed_loglog_slope": 0.5390136356214614}}, "method": "independent CSV parser; recomputed W1 slopes and held-out envelopes", "passed": true}
{"claim": 3, "details": {"iid:contractive": {"passed": true, "recomputed_calibration_constant": 0.55005628555049, "recomputed_holdout_values": [0.23669373746914327, 0.24572002402627902], "recomputed_loglog_slope": 0.42112593146879745}, "iid:linear": {"passed": true, "recomputed_calibration_constant": 0.5160951040496135, "recomputed_holdout_values": [0.1853889443521312, 0.20010526922481606], "recomputed_loglog_slope": 0.4940436461006234}}, "method": "independent CSV parser; recomputed W1 slopes and held-out envelopes", "passed": true}
{"claim": 4, "details": {"coverage_pass": true, "exact_clopper_pearson_recomputation_pass": true, "passed": true, "rate_formula_pass": true, "recomputed_calibration_constant": 0.02924668438961762, "recomputed_max_holdout_normalized_upper": 0.014627372243918491}, "method": "independent CSV parser; recomputed tail-rate formula, coverage, and held-out envelope", "passed": true}
{"claim": 5, "details": {"tail": {"coverage_pass": true, "exact_clopper_pearson_recomputation_pass": true, "passed": true, "rate_formula_pass": true, "recomputed_calibration_constant": 0.07698770091449708, "recomputed_max_holdout_normalized_upper": 0.026522188723750798}, "w1": {"markov:contractive": {"passed": true, "recomputed_calibration_constant": 2.594676344111927, "recomputed_holdout_values": [0.8794974033625892, 0.8057491080513257], "recomputed_loglog_slope": 0.558038286322952}, "markov:linear": {"passed": true, "recomputed_calibration_constant": 1.9687831468838115, "recomputed_holdout_values": [0.7476514047308056, 0.6657239035323791], "recomputed_loglog_slope": 0.4958292068443084}, "markov:sgd": {"passed": true, "recomputed_calibration_constant": 1.9892773723243784, "recomputed_holdout_values": [0.7265075049120482, 0.6520467346573715], "recomputed_loglog_slope": 0.5053819974545185}}}, "method": "independent CSV parser; recomputed Markov W1 and tail contracts", "passed": true}
{"claim": 6, "details": {"4": {"literal_vs_intended_w1_ratio_min_fine": 7.498920053304173, "passed": true, "recomputed_scaled_sd_cv": 0.008403838295321594, "recomputed_scaling_slope": 0.24933670126184232, "target_scaling_slope": 0.25}, "6": {"literal_vs_intended_w1_ratio_min_fine": 18.047808929275796, "passed": true, "recomputed_scaled_sd_cv": 0.003852034292919411, "recomputed_scaling_slope": 0.16856868582744453, "target_scaling_slope": 0.16666666666666666}}, "method": "independent CSV parser; recomputed h=4/h=6 scaling and both Gibbs targets", "passed": true}
INDEPENDENT_CHECKS claim_1..claim_6 passed=true
SIMULATOR_IMPORTS 0
PROCESS_EXIT_CODE 0
````
