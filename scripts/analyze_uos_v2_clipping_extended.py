#!/usr/bin/env python3
"""Current-data-only analyses for the UOS v2 clipping investigation.

The outputs distinguish observations from interpretations.  In particular,
the vibration-derived 1x candidate is not treated as tachometer ground truth.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from nptdms import TdmsFile
from scipy import signal

from scripts.analyze_uos_v2_clipping import (
    _channels,
    bearing_orders,
    discover_unique_files,
    parse_filename,
)


RAILS_G = {
    # Exact repeated values recovered by the exhaustive base scan.
    0: (-53.129211775684645, 53.14191454931536),
    1: (-50.655637040792065, 50.67458878321781),
    2: (math.nan, 51.62331855642786),
    3: (math.nan, math.nan),
}
BANDS_HZ = ((0.5, 2000), (2000, 7000), (7000, 10000), (10000, 11200))


def _write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    names = fieldnames or (list(rows[0]) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=names, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def collapse_events(indices: np.ndarray) -> np.ndarray:
    """Return the first sample of each contiguous rail run."""
    indices = np.asarray(indices, dtype=np.int64)
    if not len(indices):
        return indices
    return indices[np.r_[True, np.diff(indices) > 1]]


def rail_indices(values: np.ndarray, channel_index: int) -> np.ndarray:
    neg, pos = RAILS_G[channel_index]
    mask = np.zeros(len(values), dtype=bool)
    if math.isfinite(neg):
        mask |= values == neg
    if math.isfinite(pos):
        mask |= values == pos
    return np.flatnonzero(mask)


def estimate_one_x(values: np.ndarray, fs: float, nominal_rpm: float) -> dict[str, float]:
    """Estimate a vibration-derived 1x candidate near nominal shaft speed.

    At most 30 seconds are uniformly decimated to approximately 1 kS/s.  The
    local spectral maximum and its prominence over a nearby median are saved.
    This is a candidate, not a measured RPM, because no tachometer is present.
    """
    max_samples = min(len(values), int(round(30 * fs)))
    x = np.asarray(values[:max_samples], dtype=np.float64)
    x -= np.mean(x)
    q = max(1, int(fs // 1024))
    if q > 1:
        x = signal.resample_poly(x, 1, q)
        fs_eff = fs / q
    else:
        fs_eff = fs
    nperseg = min(len(x), int(round(16 * fs_eff)))
    freq, psd = signal.welch(x, fs=fs_eff, nperseg=nperseg,
                             noverlap=nperseg // 2, detrend="constant")
    nominal_hz = nominal_rpm / 60.0
    search = (freq >= nominal_hz * 0.90) & (freq <= nominal_hz * 1.10)
    if not np.any(search):
        return {"candidate_hz": math.nan, "candidate_rpm": math.nan,
                "local_ratio_db": math.nan, "resolution_hz": math.nan}
    selected = np.flatnonzero(search)
    peak_i = selected[np.argmax(psd[selected])]
    near = (freq >= nominal_hz * 0.75) & (freq <= nominal_hz * 1.25)
    exclude = np.abs(freq - freq[peak_i]) <= max(0.25, 2 * (freq[1] - freq[0]))
    background = psd[near & ~exclude]
    ratio = 10 * np.log10(max(psd[peak_i], 1e-30) / max(float(np.median(background)), 1e-30))
    return {"candidate_hz": float(freq[peak_i]), "candidate_rpm": float(freq[peak_i] * 60),
            "local_ratio_db": float(ratio), "resolution_hz": float(freq[1] - freq[0])}


def consensus_one_x(channel_estimates: list[dict]) -> dict[str, float | str]:
    usable = [r for r in channel_estimates if math.isfinite(r["candidate_hz"])]
    if not usable:
        return {"consensus_hz": math.nan, "consensus_rpm": math.nan,
                "channel_spread_rpm": math.nan, "confidence": "Unresolved"}
    rpm = np.array([r["candidate_rpm"] for r in usable])
    ratio = np.array([r["local_ratio_db"] for r in usable])
    median = float(np.median(rpm))
    spread = float(np.max(rpm) - np.min(rpm))
    agreeing = int(np.count_nonzero(np.abs(rpm - median) <= 15.0))
    confidence = "High" if agreeing >= 3 and spread <= 30 and np.median(ratio) >= 10 else (
        "Medium" if agreeing >= 2 and np.median(ratio) >= 6 else "Low")
    return {"consensus_hz": median / 60.0, "consensus_rpm": median,
            "channel_spread_rpm": spread, "confidence": confidence}


def phase_concentration(event_samples: np.ndarray, fs: float, frequency_hz: float) -> tuple[float, float]:
    """Return circular concentration R and Rayleigh large-sample p approximation."""
    if len(event_samples) < 3 or not math.isfinite(frequency_hz):
        return math.nan, math.nan
    phase = np.mod(2 * np.pi * frequency_hz * event_samples / fs, 2 * np.pi)
    r = float(abs(np.mean(np.exp(1j * phase))))
    n = len(phase)
    p = min(1.0, math.exp(-n * r * r) * (1 + (2 * n * r * r - r**4 * n) / (4 * n)))
    return r, p


def local_envelope_prominence(freq: np.ndarray, amplitude: np.ndarray, target_hz: float) -> tuple[float, float]:
    """Peak frequency and local amplitude prominence using fixed relative rules."""
    peak_half_width = max(0.5, 0.01 * target_hz)
    bg_inner = max(2.0, 0.02 * target_hz)
    bg_outer = max(10.0, 0.10 * target_hz)
    peak = np.abs(freq - target_hz) <= peak_half_width
    background = (np.abs(freq - target_hz) >= bg_inner) & (np.abs(freq - target_hz) <= bg_outer)
    if not np.any(peak) or not np.any(background):
        return math.nan, math.nan
    indices = np.flatnonzero(peak)
    selected = indices[np.argmax(amplitude[indices])]
    ratio = 20 * np.log10(max(amplitude[selected], 1e-15) /
                          max(float(np.median(amplitude[background])), 1e-15))
    return float(freq[selected]), float(ratio)


def analyse_files(data_root: Path, output_dir: Path) -> tuple[list[dict], list[dict], list[dict]]:
    files = discover_unique_files(data_root)
    rpm_rows: list[dict] = []
    event_rows: list[dict] = []
    periodicity_rows: list[dict] = []

    for number, item in enumerate(files, 1):
        meta = parse_filename(item.path)
        if meta["rpm"] == "Unknown":
            continue
        nominal_rpm = float(meta["rpm"])
        with TdmsFile.open(item.path) as tdms:
            channels = _channels(tdms)
            arrays = [np.asarray(ch[:], dtype=np.float64) for ch in channels]
            fs = 1.0 / float(channels[0].properties["wf_increment"])
            estimates = []
            for ch_i, values in enumerate(arrays):
                estimate = estimate_one_x(values, fs, nominal_rpm)
                estimates.append(estimate)
                rpm_rows.append({"file": str(item.path), **meta, "channel": f"CH{ch_i}",
                                 "nominal_rpm": nominal_rpm, **estimate})
            consensus = consensus_one_x(estimates)
            for row in rpm_rows[-len(arrays):]:
                row.update(consensus)

            # Event-level cross-channel response.  A response means exceeding
            # that channel's own 99.9th absolute-amplitude percentile within
            # +/-1 ms; it is not called simultaneous clipping.
            thresholds = [float(np.quantile(np.abs(x), 0.999)) for x in arrays]
            file_events: dict[int, np.ndarray] = {}
            for source_ch, values in enumerate(arrays):
                events = collapse_events(rail_indices(values, source_ch))
                file_events[source_ch] = events
                half = max(1, int(round(0.001 * fs)))
                for event_n, index in enumerate(events):
                    response_count = 0
                    response_ratios = []
                    for target_ch, target in enumerate(arrays):
                        lo, hi = max(0, index - half), min(len(target), index + half + 1)
                        local_peak = float(np.max(np.abs(target[lo:hi])))
                        ratio = local_peak / max(thresholds[target_ch], 1e-12)
                        if target_ch != source_ch:
                            response_count += ratio >= 1.0
                            response_ratios.append(ratio)
                    event_rows.append({"file": str(item.path), **meta, "source_channel": f"CH{source_ch}",
                                       "event_number": event_n, "sample_index": int(index),
                                       "time_s": index / fs, "other_channels_above_own_p999": response_count,
                                       "max_other_channel_p999_ratio": max(response_ratios, default=math.nan),
                                       "window_ms": 1.0})

                if len(events):
                    shaft = float(consensus["consensus_hz"])
                    targets = {"1X": shaft}
                    if meta["bearing"] in ("6204", "N204", "NJ204", "30204"):
                        targets.update({name: order * shaft for name, order in bearing_orders(meta["bearing"]).items()})
                    for name, target in targets.items():
                        r, p = phase_concentration(events, fs, target)
                        periodicity_rows.append({"file": str(item.path), **meta,
                                                 "source_channel": f"CH{source_ch}", "rail_events": len(events),
                                                 "one_x_confidence": consensus["confidence"],
                                                 "target": name, "target_hz": target,
                                                 "phase_concentration_r": r, "rayleigh_p_approx": p})
        print(f"extended {number}/{len(files)}: {item.path}", flush=True)

    _write_csv(output_dir / "one_x_candidates.csv", rpm_rows)
    _write_csv(output_dir / "rail_event_cross_channel.csv", event_rows)
    _write_csv(output_dir / "rail_event_periodicity.csv", periodicity_rows)
    return rpm_rows, event_rows, periodicity_rows


def clipping_label_association(scan_csv: Path, output_dir: Path) -> list[dict]:
    """Tabulate clipping prevalence by metadata; this is not a classifier."""
    with scan_csv.open(encoding="utf-8") as handle:
        source = list(csv.DictReader(handle))
    dimensions = ("bearing", "rpm", "rotor", "fault")
    rows = []
    for dimension in dimensions:
        grouped: dict[str, list[dict]] = defaultdict(list)
        for row in source:
            grouped[row[dimension]].append(row)
        for value, members in sorted(grouped.items()):
            clipped = sum(float(row["n_at_rail_all_channels"]) > 0 for row in members)
            rows.append({"dimension": dimension, "value": value, "files": len(members),
                         "files_with_rail": clipped, "prevalence_pct": 100 * clipped / len(members),
                         "rail_samples": sum(int(row["n_at_rail_all_channels"]) for row in members)})
    _write_csv(output_dir / "clipping_label_association.csv", rows)
    return rows


def band_and_envelope_analysis(data_root: Path, rpm_csv: Path, output_dir: Path) -> tuple[list[dict], list[dict]]:
    """Analyse a fixed first 10 s excerpt from every logical recording/channel."""
    with rpm_csv.open(encoding="utf-8") as handle:
        consensus = {row["file"]: float(row["consensus_hz"]) for row in csv.DictReader(handle)}
    band_rows: list[dict] = []
    envelope_rows: list[dict] = []
    files = discover_unique_files(data_root)
    for number, item in enumerate(files, 1):
        meta = parse_filename(item.path)
        shaft = consensus.get(str(item.path), float(meta["rpm"]) / 60)
        targets = {name: order * shaft for name, order in bearing_orders(meta["bearing"]).items()}
        with TdmsFile.open(item.path) as tdms:
            for ch_i, channel in enumerate(_channels(tdms)):
                fs = 1.0 / float(channel.properties["wf_increment"])
                count = min(len(channel), int(round(10 * fs)))
                x = np.asarray(channel[:count], dtype=np.float64)
                x -= np.mean(x)
                total_ms = float(np.mean(x * x))
                for low, high in BANDS_HZ:
                    sos = signal.butter(4, (low, high), btype="bandpass", fs=fs, output="sos")
                    filtered = signal.sosfiltfilt(sos, x)
                    band_ms = float(np.mean(filtered * filtered))
                    common = {"file": str(item.path), **meta, "channel": f"CH{ch_i}",
                              "excerpt_start_s": 0, "excerpt_duration_s": count / fs,
                              "band_hz": f"{low:g}-{high:g}", "band_rms_g": math.sqrt(band_ms),
                              "band_energy_pct_of_centered_raw": 100 * band_ms / max(total_ms, 1e-30)}
                    band_rows.append(common)
                    if low < 2000:
                        continue
                    envelope = np.abs(signal.hilbert(filtered))
                    nperseg = min(len(envelope), int(round(10 * fs)))
                    freq, psd = signal.welch(envelope, fs=fs, nperseg=nperseg,
                                             noverlap=0, scaling="spectrum")
                    amplitude = np.sqrt(psd)
                    for target_name, target_hz in targets.items():
                        observed, prominence = local_envelope_prominence(freq, amplitude, target_hz)
                        envelope_rows.append({**common, "target": target_name, "expected_hz": target_hz,
                                              "observed_peak_hz": observed,
                                              "local_prominence_db": prominence,
                                              "at_least_15_db": "Yes" if prominence >= 15 else "No"})
        print(f"band-envelope {number}/{len(files)}: {item.path}", flush=True)
    _write_csv(output_dir / "band_metrics_10s.csv", band_rows)
    _write_csv(output_dir / "envelope_validation_10s.csv", envelope_rows)
    return band_rows, envelope_rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--scan-csv", type=Path, required=True)
    parser.add_argument("--skip-band-envelope", action="store_true")
    parser.add_argument("--only-band-envelope", action="store_true")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if not args.only_band_envelope:
        analyse_files(args.data_root, args.output_dir)
        clipping_label_association(args.scan_csv, args.output_dir)
    if not args.skip_band_envelope:
        band_and_envelope_analysis(args.data_root, args.output_dir / "one_x_candidates.csv", args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
