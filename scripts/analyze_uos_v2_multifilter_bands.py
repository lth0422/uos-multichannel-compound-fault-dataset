#!/usr/bin/env python3
"""Compare five established IIR families on UOS v2 >50 g triple-fault channels."""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
from nptdms import TdmsFile
from scipy import signal

from scripts.analyze_uos_v2_clipping import _channels
from scripts.analyze_uos_v2_clipping_extended import local_envelope_prominence
from scripts.analyze_uos_v2_compound_features import compound_targets


FILTERS = ("butter", "cheby1", "cheby2", "ellip", "bessel")
CUTOFF_SCENARIOS_HZ = (2000.0, 7000.0, 10000.0, 11500.0)
BANDS = (
    ("B1_0_2k", 0.0, 2000.0, "lowpass"),
    ("B2_2_7k", 2000.0, 7000.0, "bandpass"),
    ("B3_7_10k", 7000.0, 10000.0, "bandpass"),
    ("B4_10_11p5k", 10000.0, 11500.0, "bandpass"),
    ("B5_11p5_12p8k", 11500.0, math.nan, "highpass"),
)


def _write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    names = fields or (list(rows[0]) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=names, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def design_sos(filter_name: str, band: tuple, fs: float, order: int = 4) -> np.ndarray:
    _, low, high, kind = band
    wn = high if kind == "lowpass" else (low if kind == "highpass" else (low, high))
    kwargs = {"N": order, "Wn": wn, "btype": kind, "fs": fs, "output": "sos"}
    if filter_name == "butter": return signal.butter(**kwargs)
    if filter_name == "cheby1": return signal.cheby1(rp=0.5, **kwargs)
    if filter_name == "cheby2": return signal.cheby2(rs=40, **kwargs)
    if filter_name == "ellip": return signal.ellip(rp=0.5, rs=40, **kwargs)
    if filter_name == "bessel": return signal.bessel(norm="phase", **kwargs)
    raise ValueError(f"Unsupported filter: {filter_name}")


def select_channels(scan_csv: Path) -> list[dict]:
    with scan_csv.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return [row for row in rows
            if row["bearing_filename"] in ("30204", "6204", "N204")
            and row["rpm_filename"] in ("1400", "1600")
            and row["fault_filename"] == "IR+OR+B"
            and (float(row["max_g"]) > 50 or float(row["min_g"]) < -50)]


def centered_excerpt(values: np.ndarray, fs: float, duration_s: float = 10.0) -> tuple[np.ndarray, int, int]:
    length = min(len(values), int(round(duration_s * fs)))
    peak_index = int(np.argmax(np.abs(values)))
    start = min(max(0, peak_index - length // 2), len(values) - length)
    excerpt = np.asarray(values[start:start + length], dtype=np.float64)
    excerpt -= np.mean(excerpt)
    return excerpt, start, peak_index


def analyse(
    data_root: Path, scan_csv: Path, one_x_csv: Path, output_dir: Path
) -> tuple[list[dict], list[dict], list[dict]]:
    selected = select_channels(scan_csv)
    with one_x_csv.open(encoding="utf-8") as handle:
        one_x = {row["file"]: float(row["consensus_hz"]) for row in csv.DictReader(handle)}
    by_file: dict[str, list[dict]] = defaultdict(list)
    for row in selected: by_file[row["file"]].append(row)
    metrics: list[dict] = []
    envelope_rows: list[dict] = []
    cutoff_rows: list[dict] = []
    for number, (file_name, channel_specs) in enumerate(sorted(by_file.items()), 1):
        path = Path(file_name)
        with TdmsFile.open(path) as tdms:
            channels = _channels(tdms)
            for spec in channel_specs:
                channel_index = int(spec["channel_index"])
                channel = channels[channel_index]
                fs = 1.0 / float(channel.properties["wf_increment"])
                raw = np.asarray(channel[:], dtype=np.float64)
                excerpt, start, peak_index = centered_excerpt(raw, fs)
                shaft_hz = one_x.get(file_name, float(spec["rpm_filename"]) / 60.0)
                targets = compound_targets(spec["bearing_filename"], shaft_hz)
                raw_rms = float(np.sqrt(np.mean(excerpt * excerpt)))
                common = {
                    "file": file_name, "bearing": spec["bearing_filename"], "rpm": spec["rpm_filename"],
                    "rotor": spec["rotor_filename"], "fault": spec["fault_filename"],
                    "channel": spec["channel"], "sampling_rate_hz": fs,
                    "excerpt_start_s": start / fs, "excerpt_duration_s": len(excerpt) / fs,
                    "raw_global_peak_index": peak_index, "raw_global_peak_abs_g": float(np.max(np.abs(raw))),
                    "raw_excerpt_rms_g": raw_rms, "raw_n_at_rail": spec["n_at_rail"],
                }
                for filter_name in FILTERS:
                    for cutoff_hz in CUTOFF_SCENARIOS_HZ:
                        scenario = (f"LPF_{cutoff_hz:g}", 0.0, cutoff_hz, "lowpass")
                        sos = design_sos(filter_name, scenario, fs)
                        retained = signal.sosfiltfilt(sos, excerpt)
                        retained_abs = np.abs(retained)
                        retained_rms = float(np.sqrt(np.mean(retained * retained)))
                        cutoff_rows.append({
                            **common,
                            "filter": filter_name,
                            "order_single_pass": 4,
                            "application": "sosfiltfilt_zero_phase",
                            "cutoff_hz": cutoff_hz,
                            "removed_nominal_range_hz": f">{cutoff_hz:g}",
                            "retained_nominal_range_hz": f"0-{cutoff_hz:g}",
                            "retained_peak_abs_g": float(np.max(retained_abs)),
                            "retained_p99_9_abs_g": float(np.quantile(retained_abs, 0.999)),
                            "retained_p99_99_abs_g": float(np.quantile(retained_abs, 0.9999)),
                            "retained_rms_g": retained_rms,
                            "retained_energy_pct_of_raw_excerpt": (
                                100 * retained_rms * retained_rms / max(raw_rms * raw_rms, 1e-30)
                            ),
                            "retained_peak_over_50g": "Yes" if np.max(retained_abs) > 50 else "No",
                            "interpretation": "post_clipping_hypothetical_lowpass_output",
                        })
                    for band in BANDS:
                        band_name, low, high, kind = band
                        sos = design_sos(filter_name, band, fs)
                        filtered = signal.sosfiltfilt(sos, excerpt)
                        abs_values = np.abs(filtered)
                        rms = float(np.sqrt(np.mean(filtered * filtered)))
                        metrics.append({
                            **common, "filter": filter_name, "order_single_pass": 4,
                            "application": "sosfiltfilt_zero_phase", "cheby1_rp_db": 0.5 if filter_name == "cheby1" else "NA",
                            "cheby2_rs_db": 40 if filter_name == "cheby2" else "NA",
                            "ellip_rp_db": 0.5 if filter_name == "ellip" else "NA",
                            "ellip_rs_db": 40 if filter_name == "ellip" else "NA",
                            "bessel_norm": "phase" if filter_name == "bessel" else "NA",
                            "band": band_name, "low_hz": low,
                            "high_hz": fs / 2 if kind == "highpass" else high,
                            "band_peak_abs_g": float(np.max(abs_values)),
                            "band_p99_9_abs_g": float(np.quantile(abs_values, 0.999)),
                            "band_p99_99_abs_g": float(np.quantile(abs_values, 0.9999)),
                            "band_rms_g": rms, "band_energy_pct_of_raw_excerpt": 100 * rms * rms / max(raw_rms * raw_rms, 1e-30),
                            "band_peak_over_50g": "Yes" if np.max(abs_values) > 50 else "No",
                            "physical_interpretation": "DAQ_transition_diagnostic_only" if band_name.startswith("B5") else
                                ("sensor_outside_nominal_range" if band_name.startswith("B4") else "in_sensor_nominal_range"),
                        })
                        if band_name.startswith("B5"):
                            continue
                        env = np.abs(signal.hilbert(filtered))
                        freq, psd = signal.welch(env, fs=fs, nperseg=len(env), noverlap=0, scaling="spectrum")
                        amplitude = np.sqrt(psd)
                        for target in targets:
                            if target["component"] not in ("IR", "OR", "B"):
                                continue
                            observed, prominence = local_envelope_prominence(freq, amplitude, target["frequency_hz"])
                            envelope_rows.append({
                                **common, "filter": filter_name, "band": band_name,
                                **target, "observed_peak_hz": observed,
                                "local_prominence_db": prominence,
                                "at_least_15_db": "Yes" if prominence >= 15 else "No",
                            })
        print(f"multifilter {number}/{len(by_file)}: {file_name}", flush=True)
    _write_csv(output_dir / "multifilter_band_metrics.csv", metrics)
    _write_csv(output_dir / "multifilter_envelope_features.csv", envelope_rows)
    _write_csv(output_dir / "multifilter_cutoff_scenarios.csv", cutoff_rows)
    return metrics, envelope_rows, cutoff_rows


def summarize_cutoff_scenarios(cutoff_rows: list[dict], output_dir: Path) -> list[dict]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in cutoff_rows:
        groups[(row["filter"], float(row["cutoff_hz"]))].append(row)
    summary = []
    for (filter_name, cutoff_hz), rows in sorted(groups.items()):
        peaks = np.array([float(row["retained_peak_abs_g"]) for row in rows], dtype=float)
        summary.append({
            "filter": filter_name,
            "cutoff_hz": cutoff_hz,
            "removed_nominal_range_hz": f">{cutoff_hz:g}",
            "channels": len(rows),
            "retained_peak_over_50g_channels": int(np.count_nonzero(peaks > 50)),
            "retained_peak_at_most_50g_channels": int(np.count_nonzero(peaks <= 50)),
            "median_retained_peak_g": float(np.median(peaks)),
            "max_retained_peak_g": float(np.max(peaks)),
        })
    _write_csv(output_dir / "multifilter_cutoff_scenario_summary.csv", summary)

    channel_groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in cutoff_rows:
        channel_groups[(row["file"], row["channel"], float(row["cutoff_hz"]))].append(row)
    consensus_rows = []
    for (file_name, channel, cutoff_hz), rows in sorted(channel_groups.items()):
        first = rows[0]
        over = sorted(row["filter"] for row in rows if float(row["retained_peak_abs_g"]) > 50)
        peaks = [float(row["retained_peak_abs_g"]) for row in rows]
        consensus_rows.append({
            "file": file_name,
            "bearing": first["bearing"],
            "rpm": first["rpm"],
            "rotor": first["rotor"],
            "fault": first["fault"],
            "channel": channel,
            "cutoff_hz": cutoff_hz,
            "filters_over_50g_count": len(over),
            "filters_over_50g": "+".join(over) if over else "None",
            "majority_at_least_3_of_5": "Yes" if len(over) >= 3 else "No",
            "minimum_filtered_peak_g": min(peaks),
            "maximum_filtered_peak_g": max(peaks),
        })
    _write_csv(output_dir / "multifilter_cutoff_consensus_channels.csv", consensus_rows)

    consensus_summary = []
    for cutoff_hz in sorted({float(row["cutoff_hz"]) for row in consensus_rows}):
        rows = [row for row in consensus_rows if float(row["cutoff_hz"]) == cutoff_hz]
        vote_counts = {votes: sum(int(row["filters_over_50g_count"]) == votes for row in rows) for votes in range(6)}
        consensus_summary.append({
            "cutoff_hz": cutoff_hz,
            "channels": len(rows),
            "majority_at_least_3_of_5_channels": sum(row["majority_at_least_3_of_5"] == "Yes" for row in rows),
            **{f"exactly_{votes}_filters_over_50g_channels": vote_counts[votes] for votes in range(6)},
        })
    _write_csv(output_dir / "multifilter_cutoff_consensus_summary.csv", consensus_summary)
    return summary


def summarize(metrics: list[dict], envelope_rows: list[dict], output_dir: Path) -> tuple[list[dict], list[dict]]:
    metric_groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in metrics: metric_groups[(row["filter"], row["band"])].append(row)
    metric_summary = []
    for (filter_name, band), rows in sorted(metric_groups.items()):
        peaks = np.array([row["band_peak_abs_g"] for row in rows], dtype=float)
        rms = np.array([row["band_rms_g"] for row in rows], dtype=float)
        metric_summary.append({"filter": filter_name, "band": band, "channels": len(rows),
                               "peak_over_50g_channels": int(np.count_nonzero(peaks > 50)),
                               "median_peak_g": float(np.median(peaks)), "max_peak_g": float(np.max(peaks)),
                               "median_rms_g": float(np.median(rms)),
                               "median_energy_pct": float(np.median(
                                   [float(row["band_energy_pct_of_raw_excerpt"]) for row in rows]))})
    _write_csv(output_dir / "multifilter_band_summary.csv", metric_summary)

    env_groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in envelope_rows:
        if row["overlaps_other_family_search_window"] == "No":
            env_groups[(row["filter"], row["band"], row["target"], row["component"])].append(row)
    env_summary = []
    for (filter_name, band, target, component), rows in sorted(env_groups.items()):
        values = np.array([row["local_prominence_db"] for row in rows], dtype=float)
        env_summary.append({"filter": filter_name, "band": band, "target": target, "component": component,
                            "channels": len(rows), "detected_channels": int(np.count_nonzero(values >= 15)),
                            "detection_rate_pct": 100 * float(np.mean(values >= 15)),
                            "median_prominence_db": float(np.median(values))})
    _write_csv(output_dir / "multifilter_envelope_summary.csv", env_summary)

    component_groups: dict[tuple, dict[tuple[str, str], list[float]]] = defaultdict(lambda: defaultdict(list))
    for row in envelope_rows:
        if row["overlaps_other_family_search_window"] == "No":
            group = (row["filter"], row["band"], row["component"])
            channel_key = (row["file"], row["channel"])
            component_groups[group][channel_key].append(float(row["local_prominence_db"]))
    component_summary = []
    for (filter_name, band, component), channels in sorted(component_groups.items()):
        strongest = np.array([max(values) for values in channels.values()], dtype=float)
        component_summary.append({
            "filter": filter_name,
            "band": band,
            "component": component,
            "channels": len(strongest),
            "channels_with_any_nonoverlap_target_at_least_15_db": int(np.count_nonzero(strongest >= 15)),
            "detection_rate_pct": 100 * float(np.mean(strongest >= 15)),
            "median_strongest_prominence_db": float(np.median(strongest)),
        })
    _write_csv(output_dir / "multifilter_component_summary.csv", component_summary)
    return metric_summary, env_summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--scan-csv", type=Path, required=True)
    parser.add_argument("--one-x-csv", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    metrics, envelope, cutoff_rows = analyse(args.data_root, args.scan_csv, args.one_x_csv, args.output_dir)
    summarize(metrics, envelope, args.output_dir)
    summarize_cutoff_scenarios(cutoff_rows, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
