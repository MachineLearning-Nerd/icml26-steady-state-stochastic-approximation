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
        {row["direction"] for row in rows} == required_directions
        and {float(row["threshold"]) for row in rows} == required_thresholds
        and {float(row["alpha"]) for row in rows} == required_alphas
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
    result = coverage and rate_matches and holdout
    return result, {
        "coverage_pass": coverage,
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
