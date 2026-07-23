"""Independent exit-code checker for committed/generated claim artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim", type=int, choices=range(1, 7), required=True)
    args = parser.parse_args()
    claim_dir = ROOT / ".openresearch" / "artifacts" / f"claim_{args.claim}"
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
    print(f"CLAIM_{args.claim}_CHECK PASS verdict={status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
