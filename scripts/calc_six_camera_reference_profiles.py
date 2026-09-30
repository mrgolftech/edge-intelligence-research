#!/usr/bin/env python3
"""Generate six-camera reference workload profiles.

These profiles are arithmetic transforms of public reference systems/datasets.
They are NOT product requirements for the six-camera UAV case.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/calculations/six-camera-reference-profiles.csv"

PROFILES = [
    {
        "profile_id": "R1_EUROC_6EQ",
        "basis": "EuRoC MAV stereo images",
        "reference_camera_count": 2,
        "equivalent_camera_count": 6,
        "width": 752,
        "height": 480,
        "fps": 20,
        "role": "VIO/MAV low-resolution reference",
        "source_url": "https://projects.asl.ethz.ch/datasets/euroc-mav/",
        "evidence_note": "Official EuRoC: stereo WVGA monochrome, 2x20 FPS, IMU 200 Hz. Six-camera result is arithmetic scaling only.",
    },
    {
        "profile_id": "R2_TUMVI_6EQ",
        "basis": "TUM VI stereo images",
        "reference_camera_count": 2,
        "equivalent_camera_count": 6,
        "width": 1024,
        "height": 1024,
        "fps": 20,
        "role": "VIO high-resolution grayscale reference",
        "source_url": "https://cvg.cit.tum.de/data/datasets/visual-inertial-dataset",
        "evidence_note": "Official TUM VI: stereo 1024x1024 @20 Hz, IMU 200 Hz, hardware synchronized. Six-camera result is arithmetic scaling only.",
    },
    {
        "profile_id": "R3_NUSCENES_6CAM",
        "basis": "nuScenes six-camera sensor suite",
        "reference_camera_count": 6,
        "equivalent_camera_count": 6,
        "width": 1600,
        "height": 900,
        "fps": 12,
        "role": "native six-camera perception reference",
        "source_url": "https://www.nuscenes.org/tutorials/nuscenes_tutorial.html",
        "evidence_note": "nuScenes has six cameras; sample metadata is 1600x900; official data-collection note states cameras run at 12 Hz.",
    },
    {
        "profile_id": "R4_NOVA_HAWK_6EQ_30",
        "basis": "NVIDIA Hawk stereo module operating point",
        "reference_camera_count": 1,
        "equivalent_camera_count": 6,
        "width": 1920,
        "height": 1200,
        "fps": 30,
        "role": "robotics multi-camera 30 Hz reference",
        "source_url": "https://nvidia-isaac-ros.github.io/getting_started/sensors/hawk_setup.html",
        "evidence_note": "Current Isaac ROS Hawk setup publishes left/right raw streams at 1920x1200@30. One Hawk is a stereo module with two imagers; six-camera result is per-image-stream arithmetic scaling, not six Hawk modules.",
    },
    {
        "profile_id": "R5_NOVA_HAWK_6EQ_60",
        "basis": "NVIDIA Hawk stereo module sensor capability",
        "reference_camera_count": 1,
        "equivalent_camera_count": 6,
        "width": 1920,
        "height": 1200,
        "fps": 60,
        "role": "robotics high-rate stress reference",
        "source_url": "https://nvidia-isaac-ros.github.io/nova/getting_started/platforms/adapting_nova.html",
        "evidence_note": "Nova supports Hawk stereo cameras at 1920x1200, 60 FPS. Six-camera result is per-image-stream arithmetic scaling, not a measured six-camera benchmark.",
    },
]

# bpp=24 is an in-memory RGB888 representation scenario, not a sensor-wire claim.
BPP_SCENARIOS = [
    (8, "1-byte/pixel payload sensitivity"),
    (10, "10-bit packed-equivalent arithmetic"),
    (12, "12-bit packed-equivalent arithmetic"),
    (16, "2-byte/pixel / 16-bit representation"),
    (24, "RGB888 in-memory representation sensitivity"),
]

FIELDS = [
    "profile_id", "basis", "reference_camera_count", "equivalent_camera_count",
    "width", "height", "fps", "pixel_rate_mp_s", "bpp_scenario",
    "payload_gbps", "payload_MBps", "role", "source_url", "evidence_note"
]


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for p in PROFILES:
        pixel_rate = p["equivalent_camera_count"] * p["width"] * p["height"] * p["fps"]
        for bpp, bpp_note in BPP_SCENARIOS:
            payload_bps = pixel_rate * bpp
            rows.append({
                "profile_id": p["profile_id"],
                "basis": p["basis"],
                "reference_camera_count": p["reference_camera_count"],
                "equivalent_camera_count": p["equivalent_camera_count"],
                "width": p["width"],
                "height": p["height"],
                "fps": p["fps"],
                "pixel_rate_mp_s": f"{pixel_rate / 1e6:.5f}",
                "bpp_scenario": f"{bpp} ({bpp_note})",
                "payload_gbps": f"{payload_bps / 1e9:.5f}",
                "payload_MBps": f"{payload_bps / 8 / 1e6:.5f}",
                "role": p["role"],
                "source_url": p["source_url"],
                "evidence_note": p["evidence_note"],
            })

    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
