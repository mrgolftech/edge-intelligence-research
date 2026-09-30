#!/usr/bin/env python3
"""Reproduce C2 Visual Autonomy reference/sensitivity envelope CSV.

This script intentionally separates:
- REFERENCE: public-system facts or arithmetic equivalents;
- SENSITIVITY: project geometry with hypothetical rates;
- STRESS: engineering stress points.

It does not define project requirements.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


OUT = Path(__file__).resolve().parents[1] / "data" / "calculations" / "c2-visual-autonomy-reference-envelope.csv"


@dataclass(frozen=True)
class Profile:
    profile_id: str
    profile_class: str
    source_system: str
    relation_to_source: str
    camera_count: int
    width: int
    height: int
    fps: float
    representation: str
    bytes_per_pixel: float
    evidence_type: str
    source_url: str
    notes: str


PROFILES = [
    Profile(
        "R-NU-6C12", "REFERENCE", "nuScenes", "native six-camera",
        6, 1600, 900, 12, "RGB888 analysis representation", 3.0, "REF",
        "https://www.nuscenes.org/tutorials/nuscenes_tutorial.html",
        "Native 6-camera dataset anchor; RGB888 is an analysis representation, not vehicle RAW/DDR traffic.",
    ),
    Profile(
        "R-TUMVI-6EQ20", "REFERENCE", "TUM VI",
        "six-stream arithmetic equivalent of stereo source",
        6, 1024, 1024, 20, "GRAY16 analysis representation", 2.0, "REF+CALC",
        "https://cvg.cit.tum.de/data/datasets/visual-inertial-dataset",
        "TUM VI is stereo, not six-camera; six streams are arithmetic scaling only.",
    ),
    Profile(
        "R-HAWK-6EQ30", "REFERENCE", "NVIDIA Hawk",
        "six-stream arithmetic equivalent of 1920x1200@30 stream",
        6, 1920, 1200, 30, "RGB888 analysis representation", 3.0, "REF+CALC",
        "https://nvidia-isaac-ros.github.io/getting_started/sensors/hawk_setup.html",
        "Hawk is stereo; six streams are arithmetic scaling only. RGB888 is a sensitivity representation.",
    ),
    Profile(
        "S-OBS-6C20", "SENSITIVITY", "project observed downstream mode",
        "project geometry with hypothetical rate",
        6, 1072, 1280, 20, "NV12", 1.5, "PROJECT_OBS+CALC", "",
        "20Hz is sensitivity only; actual project FPS remains unconfirmed.",
    ),
    Profile(
        "S-OBS-6C30", "SENSITIVITY", "project observed downstream mode",
        "project geometry with hypothetical rate",
        6, 1072, 1280, 30, "NV12", 1.5, "PROJECT_OBS+CALC", "",
        "30Hz is sensitivity only; actual project FPS remains unconfirmed.",
    ),
    Profile(
        "STRESS-OBS-6C60", "STRESS", "project observed downstream mode",
        "project geometry stress point",
        6, 1072, 1280, 60, "NV12", 1.5, "ENGINEERING_STRESS", "",
        "60Hz is an engineering stress point, not a product requirement.",
    ),
]


FIELDS = [
    "profile_id", "profile_class", "source_system", "relation_to_source",
    "camera_count", "width", "height", "fps", "representation",
    "bytes_per_pixel", "pixel_rate_mp_s", "image_plane_mb_s",
    "frame_period_ms", "one_frame_set_mb", "queue_depth_4_mb",
    "evidence_type", "source_url", "notes",
]


def row(p: Profile) -> dict[str, object]:
    pixels_per_second = p.camera_count * p.width * p.height * p.fps
    one_frame_set_mb = p.camera_count * p.width * p.height * p.bytes_per_pixel / 1e6
    return {
        "profile_id": p.profile_id,
        "profile_class": p.profile_class,
        "source_system": p.source_system,
        "relation_to_source": p.relation_to_source,
        "camera_count": p.camera_count,
        "width": p.width,
        "height": p.height,
        "fps": int(p.fps) if float(p.fps).is_integer() else p.fps,
        "representation": p.representation,
        "bytes_per_pixel": p.bytes_per_pixel,
        "pixel_rate_mp_s": f"{pixels_per_second / 1e6:.6f}",
        "image_plane_mb_s": f"{pixels_per_second * p.bytes_per_pixel / 1e6:.6f}",
        "frame_period_ms": f"{1000.0 / p.fps:.3f}",
        "one_frame_set_mb": f"{one_frame_set_mb:.6f}",
        "queue_depth_4_mb": f"{one_frame_set_mb * 4:.6f}",
        "evidence_type": p.evidence_type,
        "source_url": p.source_url,
        "notes": p.notes,
    }


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for p in PROFILES:
            writer.writerow(row(p))
    print(OUT)


if __name__ == "__main__":
    main()
