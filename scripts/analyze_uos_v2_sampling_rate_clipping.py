#!/usr/bin/env python3
"""Compare UOS v2 clipping at 12.8, 17.0667, and 25.6 kS/s.

Only N204, 1600 RPM, IR+OR+B files are included.  Raw TDMS files are never
modified.  After the first 60 s idle interval, exactly 3,072,000 samples are
used: 240 s at 12.8 kHz, 180 s at 17.0667 kHz, and 120 s at 25.6 kHz.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
from nptdms import TdmsFile
from scipy import signal

from scripts.analyze_uos_v2_clipping import _channels, parse_filename
from scripts.analyze_uos_v2_clipping_extended import (
    RAILS_G,
    collapse_events,
    estimate_one_x,
    rail_indices,
)
from scripts.uos_v2_measurement_window import MeasurementWindow


TARGET_RATES_HZ = (12800.0, 13107200.0 / (256.0 * 3.0), 25600.0)
TARGET_ROTORS = ("H", "L", "M3", "U3")
COMMON_BAND_CUTOFF_HZ = 5500.0
NI_MASTER_TIMEBASE_HZ = 13_107_200.0
EQUAL_ANALYSIS_SAMPLES = 3_072_000


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    names = list(rows[0]) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=names, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _rate_label(rate_hz: float) -> str:
    if math.isclose(rate_hz, 12800.0, abs_tol=0.1):
        return "12.8 kHz"
    if math.isclose(rate_hz, 13107200.0 / (256.0 * 3.0), abs_tol=0.1):
        return "17.0667 kHz"
    if math.isclose(rate_hz, 25600.0, abs_tol=0.1):
        return "25.6 kHz"
    return f"{rate_hz / 1000.0:.4f} kHz"


def sampling_rate_measurement_window(total_samples: int, fs: float) -> MeasurementWindow:
    """Return the user-confirmed equal-sample interval after 60 s idle."""

    start_s = 60.0
    start_sample = int(round(start_s * fs))
    end_sample = start_sample + EQUAL_ANALYSIS_SAMPLES
    if end_sample > total_samples:
        raise ValueError(
            f"recording is too short: fs={fs}, total_samples={total_samples}, required={end_sample}"
        )
    duration_s = EQUAL_ANALYSIS_SAMPLES / fs
    return MeasurementWindow(
        start_sample=start_sample,
        end_sample=end_sample,
        start_s=start_s,
        end_s=start_s + duration_s,
        duration_s=duration_s,
        policy="discard_first_60s_keep_next_3072000_samples",
    )


def discover_files(data_root: Path) -> list[Path]:
    selected = []
    for path in data_root.rglob("*.tdms"):
        meta = parse_filename(path)
        if (
            meta["bearing"] == "N204"
            and meta["rpm"] == "1600"
            and meta["fault"] == "IR+OR+B"
            and meta["rotor"] in TARGET_ROTORS
            and meta["fs"] != "Unknown"
            and any(math.isclose(float(meta["fs"]), rate, abs_tol=0.1) for rate in TARGET_RATES_HZ)
        ):
            selected.append(path)
    return sorted(selected, key=str)


def distribution_metrics(values: np.ndarray, prefix: str) -> dict[str, float]:
    absolute = np.abs(np.asarray(values, dtype=np.float64))
    rms = float(np.sqrt(np.mean(np.asarray(values, dtype=np.float64) ** 2)))
    p99, p999, p9999 = np.quantile(absolute, (0.99, 0.999, 0.9999))
    return {
        f"{prefix}_rms_g": rms,
        f"{prefix}_p99_abs_g": float(p99),
        f"{prefix}_p99_9_abs_g": float(p999),
        f"{prefix}_p99_99_abs_g": float(p9999),
        f"{prefix}_peak_abs_g": float(np.max(absolute)),
    }


def analyse(data_root: Path, output_dir: Path) -> tuple[list[dict], list[dict], list[dict]]:
    files = discover_files(data_root)
    if len(files) != 12:
        raise ValueError(f"expected 12 N204 comparison files, found {len(files)}")

    channel_rows: list[dict] = []
    file_rows: list[dict] = []
    for number, path in enumerate(files, 1):
        meta = parse_filename(path)
        with TdmsFile.open(path) as tdms:
            channels = _channels(tdms)
            properties = dict(tdms["Test Information"].properties) if "Test Information" in tdms else {}
            fs_values = [1.0 / float(channel.properties["wf_increment"]) for channel in channels]
            if max(fs_values) - min(fs_values) > 1e-6:
                raise ValueError(f"channels do not share a sampling rate: {path}")
            fs = fs_values[0]
            window = sampling_rate_measurement_window(len(channels[0]), fs)
            requested_metadata = float(properties.get("Test_properties~SamplingRate", "nan"))
            requested_filename = float(meta["fs"])
            divider_n = int(round(NI_MASTER_TIMEBASE_HZ / (256.0 * fs)))
            native_formula_hz = NI_MASTER_TIMEBASE_HZ / (256.0 * divider_n)
            per_file = []
            for channel_index, channel in enumerate(channels):
                raw = np.asarray(channel[window.start_sample:window.end_sample], dtype=np.float64)
                centered = raw - np.mean(raw)
                exact_rail = rail_indices(raw, channel_index)
                events = collapse_events(exact_rail)
                above_50 = int(np.count_nonzero(np.abs(raw) > 50.0))
                sensitivity = float(channel.properties.get("NI_SensorSensitivity", math.nan))
                voltage_limit_candidates = int(np.count_nonzero(np.abs(raw * sensitivity) >= 5.10))
                sos = signal.butter(4, COMMON_BAND_CUTOFF_HZ, btype="lowpass", fs=fs, output="sos")
                common_band = signal.sosfiltfilt(sos, centered)
                one_x = estimate_one_x(centered, fs, 1600.0)
                row = {
                    "file": str(path),
                    "rotor": meta["rotor"],
                    "fault": meta["fault"],
                    "bearing": meta["bearing"],
                    "rpm_nominal": 1600,
                    "channel": f"CH{channel_index}",
                    "requested_rate_filename_hz": requested_filename,
                    "requested_rate_metadata_hz": requested_metadata,
                    "actual_rate_hz": fs,
                    "rate_label": _rate_label(fs),
                    "ni_divider_n": divider_n,
                    "native_formula_hz": native_formula_hz,
                    "actual_minus_native_formula_hz": fs - native_formula_hz,
                    "metadata_rate_error_hz": fs - requested_metadata,
                    "nyquist_hz": fs / 2.0,
                    "approx_alias_free_bandwidth_hz": 0.45 * fs,
                    "source_duration_s": len(channel) / fs,
                    "analysis_start_s": window.start_s,
                    "analysis_end_s": window.end_s,
                    "analysis_duration_s": window.duration_s,
                    "analysis_samples": len(raw),
                    "sensitivity_v_per_g": sensitivity,
                    "minimum_g": float(np.min(raw)),
                    "maximum_g": float(np.max(raw)),
                    "samples_over_50g": above_50,
                    "samples_over_50g_per_million": 1_000_000.0 * above_50 / len(raw),
                    "samples_abs_voltage_at_least_5p10v": voltage_limit_candidates,
                    "samples_abs_voltage_at_least_5p10v_per_million": (
                        1_000_000.0 * voltage_limit_candidates / len(raw)
                    ),
                    "exact_rail_samples": len(exact_rail),
                    "exact_rail_samples_per_million": 1_000_000.0 * len(exact_rail) / len(raw),
                    "exact_rail_events": len(events),
                    "exact_rail_events_per_minute": len(events) / (window.duration_s / 60.0),
                    "has_exact_rail": "Yes" if len(exact_rail) else "No",
                    **distribution_metrics(centered, "raw"),
                    **distribution_metrics(common_band, "common_0_5p5khz"),
                    "one_x_candidate_hz": one_x["candidate_hz"],
                    "one_x_candidate_rpm": one_x["candidate_rpm"],
                    "one_x_local_ratio_db": one_x["local_ratio_db"],
                }
                channel_rows.append(row)
                per_file.append(row)

            file_rows.append({
                "file": str(path),
                "rotor": meta["rotor"],
                "rate_label": _rate_label(fs),
                "actual_rate_hz": fs,
                "source_duration_s": per_file[0]["source_duration_s"],
                "analysis_start_s": window.start_s,
                "analysis_end_s": window.end_s,
                "channels": len(per_file),
                "channels_with_exact_rail": sum(row["has_exact_rail"] == "Yes" for row in per_file),
                "exact_rail_samples": sum(int(row["exact_rail_samples"]) for row in per_file),
                "exact_rail_events": sum(int(row["exact_rail_events"]) for row in per_file),
                "samples_over_50g": sum(int(row["samples_over_50g"]) for row in per_file),
                "samples_abs_voltage_at_least_5p10v": sum(
                    int(row["samples_abs_voltage_at_least_5p10v"]) for row in per_file
                ),
                "maximum_raw_peak_g": max(float(row["raw_peak_abs_g"]) for row in per_file),
                "median_one_x_rpm": float(np.median([float(row["one_x_candidate_rpm"]) for row in per_file])),
            })
        print(f"sampling-rate clipping {number}/{len(files)}: {path}", flush=True)

    summary_rows = summarize(channel_rows, file_rows)
    _write_csv(output_dir / "sampling_rate_channel_metrics.csv", channel_rows)
    _write_csv(output_dir / "sampling_rate_file_metrics.csv", file_rows)
    _write_csv(output_dir / "sampling_rate_summary.csv", summary_rows)
    return channel_rows, file_rows, summary_rows


def summarize(channel_rows: list[dict], file_rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in channel_rows:
        grouped[row["rate_label"]].append(row)
    summary_rows = []
    for rate_label, rows in sorted(grouped.items(), key=lambda item: float(item[1][0]["actual_rate_hz"])):
        rate = float(rows[0]["actual_rate_hz"])
        matching_files = [row for row in file_rows if row["rate_label"] == rate_label]
        total_samples = sum(int(row["analysis_samples"]) for row in rows)
        rail_samples = sum(int(row["exact_rail_samples"]) for row in rows)
        rail_events = sum(int(row["exact_rail_events"]) for row in rows)
        above_50 = sum(int(row["samples_over_50g"]) for row in rows)
        voltage_limit_candidates = sum(int(row["samples_abs_voltage_at_least_5p10v"]) for row in rows)
        total_channel_minutes = sum(float(row["analysis_duration_s"]) / 60.0 for row in rows)
        summary_rows.append({
            "rate_label": rate_label,
            "actual_rate_hz": rate,
            "ni_divider_n": rows[0]["ni_divider_n"],
            "nyquist_hz": rate / 2.0,
            "approx_alias_free_bandwidth_hz": 0.45 * rate,
            "files": len(matching_files),
            "channels": len(rows),
            "files_with_exact_rail": sum(int(row["exact_rail_samples"]) > 0 for row in matching_files),
            "channels_with_exact_rail": sum(row["has_exact_rail"] == "Yes" for row in rows),
            "exact_rail_samples": rail_samples,
            "exact_rail_samples_per_million": 1_000_000.0 * rail_samples / total_samples,
            "exact_rail_events": rail_events,
            "exact_rail_events_per_channel_minute": rail_events / total_channel_minutes,
            "samples_over_50g": above_50,
            "samples_over_50g_per_million": 1_000_000.0 * above_50 / total_samples,
            "samples_abs_voltage_at_least_5p10v": voltage_limit_candidates,
            "samples_abs_voltage_at_least_5p10v_per_million": (
                1_000_000.0 * voltage_limit_candidates / total_samples
            ),
            "median_raw_peak_g": float(np.median([float(row["raw_peak_abs_g"]) for row in rows])),
            "maximum_raw_peak_g": max(float(row["raw_peak_abs_g"]) for row in rows),
            "median_raw_p99_99_g": float(np.median([float(row["raw_p99_99_abs_g"]) for row in rows])),
            "median_raw_rms_g": float(np.median([float(row["raw_rms_g"]) for row in rows])),
            "median_common_0_5p5khz_peak_g": float(np.median(
                [float(row["common_0_5p5khz_peak_abs_g"]) for row in rows]
            )),
            "median_common_0_5p5khz_p99_99_g": float(np.median(
                [float(row["common_0_5p5khz_p99_99_abs_g"]) for row in rows]
            )),
            "median_common_0_5p5khz_rms_g": float(np.median(
                [float(row["common_0_5p5khz_rms_g"]) for row in rows]
            )),
            "median_one_x_candidate_rpm": float(np.median(
                [float(row["one_x_candidate_rpm"]) for row in rows]
            )),
            "minimum_one_x_candidate_rpm": min(float(row["one_x_candidate_rpm"]) for row in rows),
            "maximum_one_x_candidate_rpm": max(float(row["one_x_candidate_rpm"]) for row in rows),
        })
    return summary_rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    analyse(args.data_root, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
