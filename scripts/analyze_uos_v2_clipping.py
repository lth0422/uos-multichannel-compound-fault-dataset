#!/usr/bin/env python3
"""Audit clipping in UOS v2 TDMS recordings without modifying raw data."""

from __future__ import annotations

import argparse
import csv
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from nptdms import TdmsFile
from scipy import signal

try:
    from scripts.uos_v2_measurement_window import measurement_window
except ModuleNotFoundError:  # Support direct execution: python scripts/analyze_uos_v2_clipping.py
    from uos_v2_measurement_window import measurement_window


CHANNEL_RE = re.compile(r"Channel\s+(\d+)$")
FILE_RE = re.compile(
    r"(?P<rotor>H|L|M[123]|U[123])_(?P<fault>H|IR|OR|B|IR\+B|IR\+OR|OR\+B|IR\+OR\+B)_"
    r"(?P<fs>\d+(?:_\d+)?)_(?P<bearing>6204|30204|N204|NJ204)_(?P<rpm>\d+)\.tdms$"
)
LPF_CUTOFFS_HZ = (3000, 5000, 7000, 9000, 10000, 11000)
ENVELOPE_BANDS_HZ = ((2000, 7000), (7000, 10000), (10000, 11200))
BEARING_GEOMETRY = {
    # UOS v1 original dataset paper, p. 6, Table 2.
    "6204": {"pitch_mm": 34.57, "element_mm": 7.94, "angle_deg": 0.0, "count": 8},
    "N204": {"pitch_mm": 34.0, "element_mm": 7.50, "angle_deg": 0.0, "count": 11},
    "NJ204": {"pitch_mm": 34.0, "element_mm": 7.50, "angle_deg": 0.0, "count": 11},
    "30204": {"pitch_mm": 35.8, "element_mm": 6.20, "angle_deg": 12.6, "count": 15},
}


@dataclass(frozen=True)
class LogicalFile:
    path: Path
    duplicate_paths: tuple[Path, ...]


def discover_unique_files(root: Path) -> list[LogicalFile]:
    """Collapse byte-identical candidates represented by equal name and size.

    The caller should independently hash candidate duplicates before deletion.
    This function only prevents obvious copied paths from biasing an audit.
    """

    groups: dict[tuple[str, int], list[Path]] = defaultdict(list)
    for path in root.rglob("*.tdms"):
        groups[(path.name, path.stat().st_size)].append(path)
    output = []
    for paths in groups.values():
        paths.sort(key=lambda p: (len(p.parts), str(p)))
        output.append(LogicalFile(paths[0], tuple(paths[1:])))
    return sorted(output, key=lambda item: str(item.path))


def parse_filename(path: Path) -> dict[str, str]:
    match = FILE_RE.fullmatch(path.name)
    if match is None:
        return {"rotor": "Unknown", "fault": "Unknown", "fs": "Unknown", "bearing": "Unknown", "rpm": "Unknown"}
    parsed = match.groupdict()
    parsed["fs"] = parsed["fs"].replace("_", ".")
    return parsed


def bearing_orders(model: str) -> dict[str, float]:
    geometry = BEARING_GEOMETRY[model]
    ratio = geometry["element_mm"] / geometry["pitch_mm"] * math.cos(math.radians(geometry["angle_deg"]))
    count = geometry["count"]
    return {
        "FTF": 0.5 * (1.0 - ratio),
        "BSF": geometry["pitch_mm"] / (2.0 * geometry["element_mm"]) * (1.0 - ratio**2),
        "BPFO": count / 2.0 * (1.0 - ratio),
        "BPFI": count / 2.0 * (1.0 + ratio),
    }


def bearing_frequencies(model: str, rpm: float) -> dict[str, float]:
    shaft_hz = rpm / 60.0
    return {name: order * shaft_hz for name, order in bearing_orders(model).items()}


def write_frequency_table(output_dir: Path) -> list[dict]:
    rows = []
    for model in ("6204", "N204", "30204"):
        orders = bearing_orders(model)
        for rpm in (600, 1400, 1600):
            frequencies = bearing_frequencies(model, rpm)
            for name in ("FTF", "BSF", "BPFO", "BPFI"):
                rows.append({"bearing": model, "rpm": rpm, "component": name,
                             "order_x": orders[name], "frequency_hz": frequencies[name],
                             "source": "UOS v1 original paper p. 6 Table 2 + classical bearing equations"})
    _write_csv(output_dir / "expected_bearing_frequencies.csv", rows)
    return rows


def _channels(tdms: TdmsFile):
    channels = [channel for group in tdms.groups() for channel in group.channels()]
    channels.sort(key=lambda c: int(CHANNEL_RE.search(c.name).group(1)) if CHANNEL_RE.search(c.name) else 999)
    return channels


def _max_run(indices: np.ndarray) -> tuple[int, int, float]:
    if len(indices) == 0:
        return 0, 0, 0.0
    starts = np.r_[0, np.flatnonzero(np.diff(indices) > 1) + 1]
    ends = np.r_[starts[1:], len(indices)]
    lengths = ends - starts
    return len(lengths), int(np.max(lengths)), float(np.mean(lengths))


def _block_baselines(values: np.ndarray, fs: float) -> np.ndarray:
    n = int(round(fs))
    usable = len(values) // n * n
    if usable == 0:
        return np.array([], dtype=float)
    # Median is deliberately used: sparse, one-sided bearing impacts can move a
    # one-second mean by several g without indicating an IEPE baseline shift.
    return np.median(values[:usable].reshape(-1, n), axis=1)


def _zero_shift_screen(block_means: np.ndarray) -> tuple[str, float]:
    """Conservative screen, not a calibrated IEPE overload test.

    Flag a persistent mean step only when adjacent 1 s means change by >0.1 g
    and the next three blocks remain displaced in the same direction.
    """

    if len(block_means) < 5:
        return "not_tested", math.nan
    steps = np.diff(block_means)
    largest = float(np.max(np.abs(steps)))
    for i, step in enumerate(steps[:-3]):
        if abs(step) <= 0.1:
            continue
        before = block_means[max(0, i - 2) : i + 1]
        after = block_means[i + 1 : i + 4]
        if abs(float(np.median(after) - np.median(before))) > 0.1:
            return "suspect", largest
    return "pass", largest


def _write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows and fieldnames is None:
        return
    names = fieldnames or list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=names, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def scan_files(files: list[LogicalFile], output_dir: Path) -> tuple[list[dict], list[dict], dict[int, tuple[float, float]]]:
    provisional: list[dict] = []
    candidate_counts: dict[int, dict[str, Counter]] = defaultdict(lambda: {"pos": Counter(), "neg": Counter()})

    for number, item in enumerate(files, 1):
        metadata = parse_filename(item.path)
        with TdmsFile.open(item.path) as tdms:
            props = dict(tdms["Test Information"].properties) if "Test Information" in tdms else {}
            for channel in _channels(tdms):
                fs = 1.0 / float(channel.properties["wf_increment"])
                window = measurement_window(len(channel), fs, metadata["bearing"])
                values = np.asarray(channel[window.start_sample:window.end_sample], dtype=np.float64)
                match = CHANNEL_RE.search(channel.name)
                ch = int(match.group(1)) if match else -1
                candidate_counts[ch]
                sensitivity = float(channel.properties.get("NI_SensorSensitivity", math.nan))
                voltage = values * sensitivity
                candidate_idx = np.flatnonzero(np.abs(voltage) >= 5.10)
                for value in values[candidate_idx]:
                    candidate_counts[ch]["pos" if value > 0 else "neg"][float(value)] += 1
                means = _block_baselines(values, fs)
                zero_state, largest_step = _zero_shift_screen(means)
                provisional.append({
                    "file": str(item.path), "channel": f"CH{ch}", "channel_index": ch,
                    "bearing_filename": metadata["bearing"], "rpm_filename": metadata["rpm"],
                    "rotor_filename": metadata["rotor"], "fault_filename": metadata["fault"],
                    "bearing_metadata": props.get("Test_properties~BearingType", "Unknown"),
                    "rpm_metadata": props.get("Test_properties~RPM", "Unknown"),
                    "rotor_metadata": props.get("Test_properties~RotorFaultType", "Unknown"),
                    "fault_metadata": props.get("Test_properties~BearingFaultType", "Unknown"),
                    "sampling_rate_hz": fs,
                    "source_samples": len(channel), "source_duration_s": len(channel) / fs,
                    "analysis_start_sample": window.start_sample, "analysis_end_sample": window.end_sample,
                    "analysis_start_s": window.start_s, "analysis_end_s": window.end_s,
                    "analysis_window_policy": window.policy,
                    "samples": len(values), "duration_s": len(values) / fs,
                    "sensitivity_v_per_g": sensitivity, "min_g": float(np.min(values)), "max_g": float(np.max(values)),
                    "n_above_50g": int(np.count_nonzero(np.abs(values) > 50.0)),
                    "candidate_indices": candidate_idx, "candidate_values": values[candidate_idx],
                    "zero_shift_screen": zero_state, "largest_1s_median_step_g": largest_step,
                    "duplicate_copy_count": len(item.duplicate_paths),
                })
        print(f"scan {number}/{len(files)}: {item.path}", flush=True)

    rails: dict[int, tuple[float, float]] = {}
    rail_rows: list[dict] = []
    for ch in sorted(candidate_counts):
        pos = candidate_counts[ch]["pos"].most_common(1)
        neg = candidate_counts[ch]["neg"].most_common(1)
        pos_value = pos[0][0] if pos and pos[0][1] >= 2 else math.nan
        neg_value = neg[0][0] if neg and neg[0][1] >= 2 else math.nan
        rails[ch] = (neg_value, pos_value)
        sensitivities = [r["sensitivity_v_per_g"] for r in provisional if r["channel_index"] == ch]
        sensitivity = float(np.median(sensitivities))
        rail_rows.append({
            "channel": f"CH{ch}", "sensitivity_v_per_g": sensitivity,
            "rail_neg_g": neg_value, "rail_pos_g": pos_value,
            "rail_neg_v": neg_value * sensitivity, "rail_pos_v": pos_value * sensitivity,
            "negative_exact_count": neg[0][1] if neg else 0, "positive_exact_count": pos[0][1] if pos else 0,
        })

    channel_rows: list[dict] = []
    masks_dir = output_dir / "masks"
    masks_dir.mkdir(parents=True, exist_ok=True)
    masks_by_file: dict[str, dict[str, np.ndarray]] = defaultdict(dict)
    for row in provisional:
        neg, pos = rails[row["channel_index"]]
        values = row.pop("candidate_values")
        indices = row.pop("candidate_indices")
        selected = np.zeros(len(indices), dtype=bool)
        if math.isfinite(neg): selected |= values == neg
        if math.isfinite(pos): selected |= values == pos
        rail_indices = indices[selected] + int(row["analysis_start_sample"])
        events, max_run, mean_run = _max_run(rail_indices)
        row.update({"n_at_rail": len(rail_indices), "n_rail_events": events, "max_rail_run": max_run,
                    "mean_rail_run": mean_run, "rail_ratio_pct": len(rail_indices) / row["samples"] * 100.0})
        if len(rail_indices) == 0:
            tier = "A"
        elif max_run <= 2 and row["zero_shift_screen"] == "pass":
            tier = "B"
        else:
            tier = "C"
        row["usability_tier"] = tier
        channel_rows.append(row)
        if len(rail_indices):
            masks_by_file[row["file"]][row["channel"]] = rail_indices.astype(np.int64)

    for file_name, channel_indices in masks_by_file.items():
        safe = Path(file_name).stem
        np.savez_compressed(masks_dir / f"{safe}_rail_indices.npz", **channel_indices)

    _write_csv(output_dir / "clipping_scan_channel.csv", channel_rows)
    _write_csv(output_dir / "rail_values.csv", rail_rows)
    return channel_rows, rail_rows, rails


def summarize_files(channel_rows: list[dict], output_dir: Path) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in channel_rows: grouped[row["file"]].append(row)
    output = []
    for file_name, rows in sorted(grouped.items()):
        labels_match = all(
            str(row[a]) == str(row[b])
            for row in rows
            for a, b in (("bearing_filename", "bearing_metadata"), ("rpm_filename", "rpm_metadata"),
                         ("rotor_filename", "rotor_metadata"), ("fault_filename", "fault_metadata"))
        )
        output.append({
            "file": file_name, "bearing": rows[0]["bearing_filename"], "rpm": rows[0]["rpm_filename"],
            "rotor": rows[0]["rotor_filename"], "fault": rows[0]["fault_filename"],
            "source_duration_s": rows[0]["source_duration_s"],
            "analysis_start_s": rows[0]["analysis_start_s"],
            "analysis_end_s": rows[0]["analysis_end_s"],
            "analysis_duration_s": rows[0]["duration_s"],
            "analysis_window_policy": rows[0]["analysis_window_policy"],
            "samples_all_channels": sum(r["samples"] for r in rows),
            "n_above_50g_all_channels": sum(r["n_above_50g"] for r in rows),
            "n_at_rail_all_channels": sum(r["n_at_rail"] for r in rows),
            "rail_ratio_pct": sum(r["n_at_rail"] for r in rows) / sum(r["samples"] for r in rows) * 100.0,
            "max_rail_run": max(r["max_rail_run"] for r in rows),
            "zero_shift_suspect_channels": sum(r["zero_shift_screen"] == "suspect" for r in rows),
            "usability_tier": max((r["usability_tier"] for r in rows), key=lambda x: "ABC".index(x)),
            "filename_metadata_match": "Yes" if labels_match else "No",
        })
    _write_csv(output_dir / "clipping_scan_file.csv", output)
    manifest_fields = [
        "file", "bearing", "rpm", "rotor", "fault", "source_duration_s",
        "analysis_start_s", "analysis_end_s", "analysis_duration_s", "analysis_window_policy",
    ]
    manifest_rows = []
    for row in output:
        manifest_row = {name: row[name] for name in manifest_fields}
        for name in ("source_duration_s", "analysis_start_s", "analysis_end_s", "analysis_duration_s"):
            manifest_row[name] = round(float(manifest_row[name]), 6)
        manifest_rows.append(manifest_row)
    _write_csv(
        output_dir / "analysis_window_manifest.csv",
        manifest_rows,
        manifest_fields,
    )
    return output


def select_lpf_files(files: list[LogicalFile]) -> list[LogicalFile]:
    desired = [
        ("N204", "1600", "M3", "IR+OR+B"), ("N204", "1600", "H", "IR+OR+B"),
        ("30204", "1600", "H", "IR+OR+B"), ("6204", "1600", "L", "IR+OR+B"),
        ("30204", "1400", "L", "IR+OR+B"), ("30204", "600", "H", "IR+OR+B"),
        ("30204", "1600", "H", "H"), ("30204", "1600", "L", "IR+B"),
    ]
    lookup = {(m["bearing"], m["rpm"], m["rotor"], m["fault"]): f for f in files if (m := parse_filename(f.path))["bearing"] != "Unknown"}
    return [lookup[key] for key in desired if key in lookup]


def lpf_sweep(files: list[LogicalFile], output_dir: Path) -> list[dict]:
    rows = []
    for item in select_lpf_files(files):
        meta = parse_filename(item.path)
        with TdmsFile.open(item.path) as tdms:
            for channel in _channels(tdms):
                fs = 1.0 / float(channel.properties["wf_increment"])
                window = measurement_window(len(channel), fs, meta["bearing"])
                values = np.asarray(channel[window.start_sample:window.end_sample], dtype=np.float64)
                centered = values - np.mean(values)
                row = {"file": str(item.path), "bearing": meta["bearing"], "rpm": meta["rpm"],
                       "rotor": meta["rotor"], "fault": meta["fault"], "channel": channel.name,
                       "analysis_start_s": window.start_s, "analysis_end_s": window.end_s,
                       "raw_peak_abs_g": float(np.max(np.abs(centered)))}
                for cutoff in LPF_CUTOFFS_HZ:
                    sos = signal.butter(8, cutoff, btype="lowpass", fs=fs, output="sos")
                    filtered = signal.sosfiltfilt(sos, centered)
                    row[f"lpf_{cutoff}_peak_abs_g"] = float(np.max(np.abs(filtered)))
                p7, p10 = row["lpf_7000_peak_abs_g"], row["lpf_10000_peak_abs_g"]
                row["branch"] = "L3" if p7 >= 50 else ("L2" if p10 >= 50 else "L1")
                rows.append(row)
        print(f"lpf: {item.path}", flush=True)
    _write_csv(output_dir / "lpf_sweep.csv", rows)
    return rows


def _local_ratio_db(freq: np.ndarray, amp: np.ndarray, target: float) -> tuple[float, float]:
    peak_mask = np.abs(freq - target) <= 1.0
    background = (np.abs(freq - target) >= 2.0) & (np.abs(freq - target) <= 10.0)
    if not np.any(peak_mask) or not np.any(background): return math.nan, math.nan
    idx = np.flatnonzero(peak_mask)[np.argmax(amp[peak_mask])]
    return float(freq[idx]), float(20 * np.log10(max(amp[idx], 1e-15) / max(np.median(amp[background]), 1e-15)))


def envelope_check(files: list[LogicalFile], output_dir: Path) -> list[dict]:
    rows = []
    for item in select_lpf_files(files):
        meta = parse_filename(item.path)
        if meta["bearing"] not in BEARING_GEOMETRY:
            continue
        targets = bearing_frequencies(meta["bearing"], float(meta["rpm"]))
        with TdmsFile.open(item.path) as tdms:
            for channel in _channels(tdms):
                fs = 1.0 / float(channel.properties["wf_increment"])
                window = measurement_window(len(channel), fs, meta["bearing"])
                values = np.asarray(channel[window.start_sample:window.end_sample], dtype=np.float64)
                centered = values - np.mean(values)
                for low, high in ENVELOPE_BANDS_HZ:
                    sos = signal.butter(4, (low, high), btype="bandpass", fs=fs, output="sos")
                    env = np.abs(signal.hilbert(signal.sosfiltfilt(sos, centered)))
                    nperseg = min(len(env), int(round(4 * fs)))
                    freq, power = signal.welch(env, fs=fs, nperseg=nperseg, noverlap=nperseg // 2, scaling="spectrum")
                    amp = np.sqrt(power)
                    for fault_name, target in targets.items():
                        peak_hz, ratio = _local_ratio_db(freq, amp, target)
                        rows.append({"file": str(item.path), "bearing": meta["bearing"], "rpm": meta["rpm"], "rotor": meta["rotor"],
                                     "fault_label": meta["fault"], "channel": channel.name,
                                     "analysis_start_s": window.start_s, "analysis_end_s": window.end_s,
                                     "carrier_band_hz": f"{low}-{high}", "target": fault_name,
                                     "expected_hz": target, "observed_peak_hz": peak_hz,
                                     "local_ratio_db": ratio, "m_plus_15db": "Yes" if ratio >= 15 else "No"})
        print(f"envelope: {item.path}", flush=True)
    _write_csv(output_dir / "envelope_check.csv", rows)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--skip-lpf", action="store_true")
    args = parser.parse_args()
    files = discover_unique_files(args.data_root)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_frequency_table(args.output_dir)
    duplicates = [{"kept": str(f.path), "duplicate": str(p)} for f in files for p in f.duplicate_paths]
    _write_csv(args.output_dir / "duplicate_candidates.csv", duplicates, ["kept", "duplicate"])
    channel_rows, _, _ = scan_files(files, args.output_dir)
    summarize_files(channel_rows, args.output_dir)
    if not args.skip_lpf:
        lpf_sweep(files, args.output_dir)
        envelope_check(files, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
