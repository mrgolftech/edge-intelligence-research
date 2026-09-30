#!/usr/bin/env python3
"""Validate evidence-oriented CSV tables.

This script intentionally checks evidence completeness, not whether a platform is "good".
"""

from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

TABLES = {
    ROOT / "data/product-specs/platform-facts.csv": [
        "vendor", "product_name", "product_type", "evidence_ids",
        "evidence_status", "source_url", "notes"
    ],
    ROOT / "data/benchmarks/public-platform-benchmarks.csv": [
        "benchmark_id", "vendor", "platform", "workload", "benchmark_type",
        "model_or_node", "input", "host", "throughput", "source_url",
        "evidence_status", "limitations"
    ],
    ROOT / "data/calculations/six-camera-reference-profiles.csv": [
        "profile_id", "basis", "equivalent_camera_count", "width", "height",
        "fps", "pixel_rate_mp_s", "bpp_scenario", "payload_gbps",
        "payload_MBps", "source_url", "evidence_note"
    ],
    ROOT / "data/calculations/avoidance-timing-fact-anchors.csv": [
        "anchor_id", "source_type", "source_name", "speed_mps",
        "evidence_status", "source_url", "limitations"
    ],
    ROOT / "data/calculations/six-camera-observed-mode-sensitivity.csv": [
        "profile_id", "camera_count", "width", "height", "format",
        "fps_scenario", "six_stream_pixel_rate_mp_s",
        "six_stream_memory_payload_MBps", "status", "notes"
    ],
}

ALLOWED_EVIDENCE_TOKENS = {
    "SPEC", "REF", "CASE", "BENCH", "PAPER", "DEMO",
    "VENDOR_BENCH", "PARTNER_BENCH", "HISTORICAL_REF", "INFER", "GAP", "HOST"
}


def split_status(value: str) -> list[str]:
    return [x.strip() for x in value.replace("/", "+").split("+") if x.strip()]


def validate_table(path: Path, required: list[str]) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing file: {path.relative_to(ROOT)}"]

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        for col in required:
            if col not in fields:
                errors.append(f"{path.name}: missing column {col}")

        for lineno, row in enumerate(reader, start=2):
            for col in required:
                if not (row.get(col) or "").strip():
                    errors.append(f"{path.name}:{lineno}: empty required field {col}")

            if "source_url" in fields:
                urls = [u.strip() for u in (row.get("source_url") or "").split("|") if u.strip()]
                if not urls or any(not u.startswith(("http://", "https://")) for u in urls):
                    errors.append(f"{path.name}:{lineno}: invalid source_url")

            status = row.get("evidence_status") or ""
            unknown = [x for x in split_status(status) if x not in ALLOWED_EVIDENCE_TOKENS]
            if unknown:
                errors.append(
                    f"{path.name}:{lineno}: unknown evidence token(s): {', '.join(unknown)}"
                )

            if path.name == "public-platform-benchmarks.csv":
                if row.get("evidence_status") in {"BENCH", "VENDOR_BENCH"}:
                    if not (row.get("input") or "").strip():
                        errors.append(f"{path.name}:{lineno}: benchmark missing input")
                    if not (row.get("host") or "").strip():
                        errors.append(f"{path.name}:{lineno}: benchmark missing host")

    return errors


def main() -> int:
    errors: list[str] = []
    for path, required in TABLES.items():
        errors.extend(validate_table(path, required))

    if errors:
        print("Evidence table validation FAILED")
        for e in errors:
            print(f"- {e}")
        return 1

    print("Evidence table validation PASSED")
    for path in TABLES:
        print(f"- {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
