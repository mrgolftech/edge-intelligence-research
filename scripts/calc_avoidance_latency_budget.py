#!/usr/bin/env python3
"""Screen or invert a UAV obstacle-avoidance latency budget.

This is an engineering calculation helper, not a safety certification tool.
Project-specific dynamics and measured vehicle response are required for decisions.
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
    p.add_argument("--pipeline-ms", type=float,
                   help="measured/assumed capture-ready through perception/map/planner/command")
    p.add_argument("--vehicle-delay-ms", type=float, required=True,
                   help="measured command/setpoint-to-vehicle response delay")
    p.add_argument("--detect-distance-m", type=float,
                   help="usable obstacle detection distance")
    p.add_argument("--keepout-distance-m", type=float,
                   help="required residual distance to obstacle")

    braking = p.add_mutually_exclusive_group()
    braking.add_argument("--measured-maneuver-distance-m", type=float,
                         help="measured/validated braking or turning distance; preferred")
    braking.add_argument("--effective-decel-mps2", type=float,
                         help="ideal constant-deceleration screening only; not preferred for product decisions")

    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    v = positive("speed", args.speed_mps)
    rate = positive("sensor rate", args.sensor_rate_hz)
    vehicle_s = nonnegative("vehicle delay", args.vehicle_delay_ms) / 1000.0
    sample_wait_s = 1.0 / rate

    maneuver = None
    maneuver_source = None
    if args.measured_maneuver_distance_m is not None:
        maneuver = nonnegative("measured maneuver distance", args.measured_maneuver_distance_m)
        maneuver_source = "measured_or_validated"
    elif args.effective_decel_mps2 is not None:
        a = positive("effective deceleration", args.effective_decel_mps2)
        maneuver = v * v / (2.0 * a)
        maneuver_source = "ideal_constant_deceleration_screening"

    out = {
        "speed_mps": v,
        "sensor_rate_hz": rate,
        "worst_case_sampling_wait_ms": sample_wait_s * 1000.0,
        "vehicle_delay_ms": args.vehicle_delay_ms,
        "distance_during_sampling_m": v * sample_wait_s,
        "distance_during_vehicle_delay_m": v * vehicle_s,
    }

    if maneuver is not None:
        out["maneuver_distance_m"] = maneuver
        out["maneuver_distance_source"] = maneuver_source
        if maneuver_source != "measured_or_validated":
            out["braking_model_warning"] = (
                "Ideal constant-deceleration screening only. Real multirotor stopping/turning is jerk-, attitude-, "
                "controller- and thrust-limited. Prefer measured or validated maneuver distance."
            )

    if args.pipeline_ms is not None:
        pipeline_s = nonnegative("pipeline delay", args.pipeline_ms) / 1000.0
        reaction_s = sample_wait_s + pipeline_s + vehicle_s
        out.update({
            "pipeline_ms": args.pipeline_ms,
            "reaction_before_maneuver_ms": reaction_s * 1000.0,
            "distance_during_pipeline_m": v * pipeline_s,
            "distance_before_maneuver_m": v * reaction_s,
        })

        if args.keepout_distance_m is not None and maneuver is not None:
            keepout = nonnegative("keepout distance", args.keepout_distance_m)
            out["keepout_distance_m"] = keepout
            out["screening_required_detection_distance_m"] = keepout + maneuver + v * reaction_s

    # Inverse budget: derive how much time remains for the compute/data pipeline.
    if (
        args.detect_distance_m is not None
        and args.keepout_distance_m is not None
        and maneuver is not None
    ):
        detect = positive("detect distance", args.detect_distance_m)
        keepout = nonnegative("keepout distance", args.keepout_distance_m)
        usable_reaction_distance = detect - keepout - maneuver
        max_reaction_s = usable_reaction_distance / v
        max_pipeline_s = max_reaction_s - sample_wait_s - vehicle_s

        out.update({
            "detect_distance_m": detect,
            "keepout_distance_m": keepout,
            "distance_available_for_sampling_pipeline_vehicle_m": usable_reaction_distance,
            "max_reaction_time_before_maneuver_ms": max_reaction_s * 1000.0,
            "max_pipeline_ms": max_pipeline_s * 1000.0,
            "pipeline_budget_feasible": max_pipeline_s > 0,
        })

        if max_pipeline_s <= 0:
            out["infeasible_reason"] = (
                "No positive compute/data pipeline budget remains after sampling wait, vehicle response, "
                "keep-out distance and maneuver distance. More TOPS alone cannot fix this screening case."
            )

    out["interpretation"] = (
        "Use P95/P99 measured Frame Age and vehicle response for acceptance. "
        "Do not substitute model inference latency or average FPS for closed-loop latency."
    )

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        for k, value in out.items():
            print(f"{k}: {value}")


if __name__ == "__main__":
    main()
