#!/usr/bin/env python3
"""Screen a UAV obstacle-avoidance latency budget.

This is an engineering calculation helper, not a safety certification tool.
It deliberately requires project-specific inputs instead of shipping assumed defaults.
"""

from __future__ import annotations

import argparse
import json


def positive(name: str, value: float) -> float:
    if value <= 0:
        raise ValueError(f"{name} must be > 0")
    return value


def nonnegative(name: str, value: float) -> float:
    if value < 0:
        raise ValueError(f"{name} must be >= 0")
    return value


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--speed-mps", type=float, required=True)
    p.add_argument("--sensor-rate-hz", type=float, required=True)
    p.add_argument("--pipeline-ms", type=float, required=True,
                   help="capture-ready through perception/map/planner/command, excluding sampling wait and vehicle tracking delay")
    p.add_argument("--vehicle-delay-ms", type=float, required=True,
                   help="measured command/setpoint-to-vehicle response delay")
    p.add_argument("--detect-distance-m", type=float,
                   help="usable obstacle detection distance")
    p.add_argument("--keepout-distance-m", type=float,
                   help="required residual distance to obstacle")
    p.add_argument("--effective-decel-mps2", type=float,
                   help="only for ideal constant-deceleration screening; jerk-limited real stopping can require more distance")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    v = positive("speed", args.speed_mps)
    rate = positive("sensor rate", args.sensor_rate_hz)
    pipeline_s = nonnegative("pipeline delay", args.pipeline_ms) / 1000.0
    vehicle_s = nonnegative("vehicle delay", args.vehicle_delay_ms) / 1000.0

    sample_wait_s = 1.0 / rate  # worst-case obstacle appearance immediately after a sample
    reaction_s = sample_wait_s + pipeline_s + vehicle_s

    out = {
        "speed_mps": v,
        "sensor_rate_hz": rate,
        "worst_case_sampling_wait_ms": sample_wait_s * 1000.0,
        "pipeline_ms": args.pipeline_ms,
        "vehicle_delay_ms": args.vehicle_delay_ms,
        "reaction_before_braking_ms": reaction_s * 1000.0,
        "distance_during_sampling_m": v * sample_wait_s,
        "distance_during_pipeline_m": v * pipeline_s,
        "distance_during_vehicle_delay_m": v * vehicle_s,
        "distance_before_braking_m": v * reaction_s,
    }

    braking = None
    if args.effective_decel_mps2 is not None:
        a = positive("effective deceleration", args.effective_decel_mps2)
        braking = v * v / (2.0 * a)
        out["ideal_constant_decel_braking_m"] = braking
        out["braking_model_warning"] = (
            "Ideal constant-deceleration screening only. PX4 collision prevention uses jerk/acceleration-aware control; "
            "use measured vehicle stopping data for product decisions."
        )

    if args.keepout_distance_m is not None:
        keepout = nonnegative("keepout distance", args.keepout_distance_m)
        out["keepout_distance_m"] = keepout
        if braking is not None:
            out["screening_required_detection_distance_m"] = v * reaction_s + braking + keepout

    if args.detect_distance_m is not None:
        detect = positive("detect distance", args.detect_distance_m)
        out["detect_distance_m"] = detect
        if braking is not None and args.keepout_distance_m is not None:
            out["screening_distance_margin_m"] = detect - out["screening_required_detection_distance_m"]

    out["interpretation"] = (
        "Use P95/P99 end-to-end measured pipeline and vehicle response values. "
        "Do not substitute model inference latency for pipeline latency."
    )

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        for k, v_ in out.items():
            print(f"{k}: {v_}")


if __name__ == "__main__":
    main()
