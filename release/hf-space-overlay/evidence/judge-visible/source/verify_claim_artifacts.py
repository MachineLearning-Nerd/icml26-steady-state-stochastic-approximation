"""Independent exit-code checker for committed/generated claim artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from independent_check import check_claim


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim", type=int, choices=range(1, 7), required=True)
    parser.add_argument(
        "--artifacts-root",
        type=Path,
        default=ROOT / ".openresearch" / "artifacts",
    )
    args = parser.parse_args()
    claim_dir = args.artifacts_root / f"claim_{args.claim}"
    verdict = json.loads((claim_dir / "verdict.json").read_text(encoding="utf-8"))
    required = [
        "claim_contract.json",
        "source_audit.md",
        "method.md",
        "raw_metrics.csv",
        "independent_checker_output.json",
        "negative_control_output.json",
        "runtime.json",
        "EVAL.md",
        "limitations.md",
    ]
    if args.claim == 6:
        required.append("routes.md")
    missing = [name for name in required if not (claim_dir / name).is_file()]
    if missing:
        print(f"CLAIM_{args.claim}_CHECK FAIL missing={missing}")
        return 1
    status = verdict.get("verdict")
    if status not in {"VERIFIED", "FALSIFIED", "BLOCKED"}:
        print(f"CLAIM_{args.claim}_CHECK FAIL invalid_verdict={status!r}")
        return 1
    raw = (claim_dir / "raw_metrics.csv").read_text(encoding="utf-8")
    if raw.count("\n") < 2:
        print(f"CLAIM_{args.claim}_CHECK FAIL empty_raw_metrics")
        return 1
    independent = json.loads(
        (claim_dir / "independent_checker_output.json").read_text(encoding="utf-8")
    )
    if independent.get("claim") != args.claim or independent.get("passed") is not True:
        print(f"CLAIM_{args.claim}_CHECK FAIL independent_checker")
        return 1
    recomputed = check_claim(args.artifacts_root, args.claim)
    if recomputed.get("passed") is not True:
        print(f"CLAIM_{args.claim}_CHECK FAIL recomputed_raw_evidence")
        return 1
    controls = json.loads(
        (claim_dir / "negative_control_output.json").read_text(encoding="utf-8")
    )
    if args.claim == 1:
        controls_pass = (
            controls.get("expected_to_pass") is False
            and controls.get("observed_families_passing") == 0
            and controls.get("detected_as_wrong") is True
        )
    elif args.claim in {2, 4}:
        controls_pass = (
            controls.get("expected_to_pass") is False
            and controls.get("control_pass") is False
        )
    elif args.claim == 3:
        control_passes = controls.get("control_passes", {})
        controls_pass = (
            controls.get("expected_to_pass") is False
            and control_passes == {"linear": False, "contractive": False}
        )
    elif args.claim == 5:
        claim_controls = controls.get("controls", {})
        controls_pass = (
            len(claim_controls) == 2
            and all(
                record.get("expected_to_pass") is False
                and record.get("control_pass") is False
                for record in claim_controls.values()
            )
        )
    else:
        claim_controls = controls.get("controls", {})
        controls_pass = (
            claim_controls.get("literal_main_text_density", {}).get("rejected")
            is True
            and claim_controls.get("wrong_sqrt_scaling", {}).get("rejected")
            is True
        )
    if not controls_pass:
        print(f"CLAIM_{args.claim}_CHECK FAIL negative_control")
        return 1
    print(f"CLAIM_{args.claim}_CHECK PASS verdict={status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
