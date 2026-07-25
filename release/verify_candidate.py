#!/usr/bin/env python3
"""Prepare and verify the additive, text-only Hugging Face Space candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
RELEASE = REPO / "release"
OVERLAY = RELEASE / "hf-space-overlay"
PROTECTED_MANIFEST = (
    REPO / ".openresearch/protected/judged_space_887693a_manifest.sha256"
)
ALLOWLIST = RELEASE / "hf_upload_allowlist.txt"
UPLOAD_MANIFEST = RELEASE / "hf_upload_manifest.sha256"
SUBSET_REPORT = RELEASE / "old_new_subset_check.json"
SPACE_ID = "DineshAI/m4TAzup6Yc"
JUDGED_REVISION = "887693a544629b31b7c6dc141fa321a9fcdb5948"
TEXT_SUFFIXES = {".csv", ".json", ".md", ".py", ".sha256", ".txt"}
SECRET_PATTERNS = {
    "huggingface_token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "github_classic_token": re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    "github_fine_grained_token": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private_key_header": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_protected_manifest() -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in PROTECTED_MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        digest, path = line.split(maxsplit=1)
        entries[path.strip()] = digest
    return entries


def overlay_files() -> dict[str, Path]:
    return {
        path.relative_to(OVERLAY).as_posix(): path
        for path in sorted(OVERLAY.rglob("*"))
        if path.is_file()
    }


def navigation_files(node: dict[str, object]) -> set[str]:
    found = {str(node["file"])}
    for child in node.get("children", []):
        found.update(navigation_files(child))
    return found


def candidate_state(judged_dir: Path) -> tuple[dict[str, object], list[str]]:
    failures: list[str] = []
    expected_old = read_protected_manifest()
    overlay = overlay_files()

    for relative, expected_hash in expected_old.items():
        path = judged_dir / relative
        if not path.is_file():
            failures.append(f"missing judged path: {relative}")
        elif sha256(path) != expected_hash:
            failures.append(f"judged hash mismatch: {relative}")

    for relative, path in overlay.items():
        if path.suffix.lower() not in TEXT_SUFFIXES:
            failures.append(f"non-text overlay suffix: {relative}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append(f"non-UTF-8 overlay file: {relative}")
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                failures.append(f"secret-like {label} pattern in: {relative}")

    judged_logbook = json.loads((judged_dir / "logbook.json").read_text())
    candidate_logbook = json.loads((OVERLAY / "logbook.json").read_text())
    if candidate_logbook.get("space_id") != SPACE_ID:
        failures.append("candidate logbook has the wrong space_id")
    old_children = judged_logbook["root"]["children"]
    new_children = candidate_logbook["root"]["children"]
    if new_children[: len(old_children)] != old_children:
        failures.append("candidate navigation does not preserve judged children")
    if candidate_logbook.get("revision") != judged_logbook.get("revision"):
        failures.append("candidate unexpectedly rewrites the judged revision field")

    old_paths = set(expected_old)
    overlay_paths = set(overlay)
    virtual_paths = old_paths | overlay_paths
    missing_old = sorted(old_paths - virtual_paths)
    if missing_old:
        failures.append(f"old paths absent from virtual candidate: {missing_old}")
    missing_navigation = sorted(
        navigation_files(candidate_logbook["root"]) - virtual_paths
    )
    if missing_navigation:
        failures.append(f"navigation targets absent: {missing_navigation}")

    changed_old: list[str] = []
    unchanged_old: set[str] = set()
    for relative, expected_hash in expected_old.items():
        if relative == "logbook.json":
            continue
        candidate_path = overlay.get(relative, judged_dir / relative)
        if candidate_path.is_file() and sha256(candidate_path) == expected_hash:
            unchanged_old.add(relative)
        else:
            changed_old.append(relative)
    if changed_old:
        failures.append(f"protected judged paths changed: {changed_old}")
    upload_paths = sorted(
        {"logbook.json"} | (overlay_paths - old_paths)
    )
    report: dict[str, object] = {
        "status": "PASS" if not failures else "FAIL",
        "space_id": SPACE_ID,
        "judged_revision": JUDGED_REVISION,
        "protected_old_path_count": len(old_paths),
        "protected_old_paths_present": len(old_paths - set(missing_old)),
        "unchanged_old_paths_except_logbook": len(unchanged_old),
        "expected_unchanged_old_paths_except_logbook": len(old_paths) - 1,
        "overlay_text_path_count": len(overlay_paths),
        "new_additive_path_count": len(overlay_paths - old_paths),
        "virtual_candidate_path_count": len(virtual_paths),
        "navigation_target_count": len(navigation_files(candidate_logbook["root"])),
        "missing_old_paths": missing_old,
        "missing_navigation_targets": missing_navigation,
        "old_pages_and_evidence_unchanged": len(unchanged_old) == len(old_paths) - 1,
        "only_existing_path_replaced": sorted(
            relative
            for relative in old_paths & overlay_paths
            if relative == "logbook.json"
            or sha256(overlay[relative]) != expected_old[relative]
        ),
        "failures": failures,
    }
    return report, upload_paths


def generated_allowlist(paths: list[str]) -> str:
    return "".join(f"{path}\n" for path in paths)


def generated_manifest(paths: list[str]) -> str:
    return "".join(f"{sha256(OVERLAY / path)}  {path}\n" for path in paths)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--judged-dir", type=Path, required=True)
    parser.add_argument(
        "--prepare",
        action="store_true",
        help="write the exact allowlist, SHA-256 manifest, and subset report",
    )
    args = parser.parse_args()

    report, paths = candidate_state(args.judged_dir.resolve())
    allowlist_text = generated_allowlist(paths)
    manifest_text = generated_manifest(paths)

    if args.prepare:
        ALLOWLIST.write_text(allowlist_text, encoding="utf-8")
        UPLOAD_MANIFEST.write_text(manifest_text, encoding="utf-8")
        SUBSET_REPORT.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    else:
        if not ALLOWLIST.is_file() or ALLOWLIST.read_text() != allowlist_text:
            report["failures"].append("upload allowlist is missing or stale")
        if not UPLOAD_MANIFEST.is_file() or UPLOAD_MANIFEST.read_text() != manifest_text:
            report["failures"].append("upload SHA-256 manifest is missing or stale")
        if not SUBSET_REPORT.is_file():
            report["failures"].append("old/new subset report is missing")
        report["status"] = "PASS" if not report["failures"] else "FAIL"

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
