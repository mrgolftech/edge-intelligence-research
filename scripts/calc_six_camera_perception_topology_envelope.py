#!/usr/bin/env python3
"""Generate six-camera PER_VIEW vs FUSED_MULTI_VIEW analysis envelope.

All profiles are BENCHMARK_BASELINE/SENSITIVITY, not project requirements.
The source-frame traffic is a one-full-read-per-consumer arithmetic equivalent,
not measured DDR or PCIe traffic.
"""

from __future__ import annotations

import csv
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "calculations" / "six-camera-perception-topology-envelope.csv"

SOURCE_FRAME_MB = 1072 * 1280 * 1.5 / 1e6
BENCH_VIEW_MB = 640 * 640 * 3 / 1e6

PROFILES = [
    ("P20-2", "PER_VIEW", 20, 2, 20, 40, 40),
    ("P20-4", "PER_VIEW", 20, 4, 20, 80, 80),
    ("P20-6", "PER_VIEW", 20, 6, 20, 120, 120),
    ("P30-2", "PER_VIEW", 30, 2, 30, 60, 60),
    ("P30-4", "PER_VIEW", 30, 4, 30, 120, 120),
    ("P30-6", "PER_VIEW", 30, 6, 30, 180, 180),
    ("F20-6", "FUSED_MULTI_VIEW", 20, 6, 20, 20, 120),
    ("F30-6", "FUSED_MULTI_VIEW", 30, 6, 30, 30, 180),
]

FIELDS = [
    "profile_id", "topology", "capture_fps", "capture_views",
    "vio_views", "vio_hz", "depth_views", "depth_hz",
    "perception_views", "perception_hz", "model_calls_s",
    "input_view_rate_s", "serial_service_budget_ms", "source_frame_mb",
    "capture_write_mb_s", "consumer_view_reads_s",
    "full_source_read_equiv_mb_s", "capture_plus_read_equiv_mb_s",
    "benchmark_input", "benchmark_input_bytes_per_view",
    "benchmark_input_payload_mb_s", "evidence_class", "notes",
]


def make_row(p):
    pid, topology, fps, pviews, phz, calls, input_views = p
    vio_views = 2
    depth_views = 2
    vio_hz = fps
    depth_hz = fps
    capture_write = 6 * fps * SOURCE_FRAME_MB
    consumer_reads = vio_views * vio_hz + depth_views * depth_hz + input_views
    read_equiv = consumer_reads * SOURCE_FRAME_MB
    total_equiv = capture_write + read_equiv
    input_payload = input_views * BENCH_VIEW_MB
    note = (
        "One-read-per-consumer analysis; model calls scale with independent views; not measured DDR/PCIe."
        if topology == "PER_VIEW"
        else "Six input views per fused update; same source-view rate as P6 at same Hz but far fewer heavier model calls; not measured DDR/PCIe."
    )
    return {
        "profile_id": pid,
        "topology": topology,
        "capture_fps": fps,
        "capture_views": 6,
        "vio_views": vio_views,
        "vio_hz": vio_hz,
        "depth_views": depth_views,
        "depth_hz": depth_hz,
        "perception_views": pviews,
        "perception_hz": phz,
        "model_calls_s": calls,
        "input_view_rate_s": input_views,
        "serial_service_budget_ms": f"{1000 / calls:.3f}",
        "source_frame_mb": f"{SOURCE_FRAME_MB:.6f}",
        "capture_write_mb_s": f"{capture_write:.6f}",
        "consumer_view_reads_s": consumer_reads,
        "full_source_read_equiv_mb_s": f"{read_equiv:.6f}",
        "capture_plus_read_equiv_mb_s": f"{total_equiv:.6f}",
        "benchmark_input": "640x640 RGB8 analysis",
        "benchmark_input_bytes_per_view": f"{BENCH_VIEW_MB:.6f}",
        "benchmark_input_payload_mb_s": f"{input_payload:.6f}",
        "evidence_class": "BENCHMARK_BASELINE",
        "notes": note,
    }


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for p in PROFILES:
            writer.writerow(make_row(p))
    print(OUT)


if __name__ == "__main__":
    main()
