#!/usr/bin/env python3
"""Define the user-confirmed UOS v2 measurement interval without editing raw files."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MeasurementWindow:
    start_sample: int
    end_sample: int
    start_s: float
    end_s: float
    duration_s: float
    policy: str


def measurement_window(total_samples: int, fs: float, bearing: str) -> MeasurementWindow:
    """Return the two-minute measurement interval after the idle period.

    User-confirmed acquisition procedure (2026-08-03):
    - ordinary recordings: discard the first 60 s and retain 60--180 s;
    - 30204 recordings longer than 7 min: discard the first 300 s and retain
      300--420 s;
    - discard everything after the retained two-minute interval.
    """

    if total_samples <= 0 or fs <= 0:
        raise ValueError("total_samples and fs must be positive")
    source_duration_s = total_samples / fs
    long_30204 = bearing == "30204" and source_duration_s > 420.0
    start_s = 300.0 if long_30204 else 60.0
    duration_s = 120.0
    start_sample = int(round(start_s * fs))
    end_sample = start_sample + int(round(duration_s * fs))
    if end_sample > total_samples:
        raise ValueError(
            f"recording is too short for policy: bearing={bearing}, "
            f"source_duration_s={source_duration_s:.3f}, required_end_s={start_s + duration_s:.3f}"
        )
    policy = "discard_first_300s_keep_next_120s" if long_30204 else "discard_first_60s_keep_next_120s"
    return MeasurementWindow(
        start_sample=start_sample,
        end_sample=end_sample,
        start_s=start_s,
        end_s=start_s + duration_s,
        duration_s=duration_s,
        policy=policy,
    )
