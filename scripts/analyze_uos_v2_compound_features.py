#!/usr/bin/env python3
"""Validate physically expected harmonic and modulation families in UOS v2.

The target families follow the S1 paper (Wang et al., PLOS ONE, 2024):
outer-race harmonics, inner-race harmonics with shaft sidebands, and
rolling-element harmonics with cage sidebands.  Arbitrary pairwise sums and
differences are deliberately not searched.
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

from scripts.analyze_uos_v2_clipping import _channels, bearing_orders, discover_unique_files, parse_filename
from scripts.analyze_uos_v2_clipping_extended import local_envelope_prominence
from scripts.uos_v2_measurement_window import measurement_window


CARRIER_BANDS_HZ = ((2000, 7000), (7000, 10000), (10000, 11200))


def _write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    names = fieldnames or (list(rows[0]) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=names, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fault_tokens(label: str) -> set[str]:
    return set(label.split("+"))


def compound_targets(bearing: str, shaft_hz: float) -> list[dict]:
    orders = bearing_orders(bearing)
    ftf = orders["FTF"] * shaft_hz
    bpfo = orders["BPFO"] * shaft_hz
    bpfi = orders["BPFI"] * shaft_hz
    bsf = orders["BSF"] * shaft_hz
    rows = [
        {"target": "1X", "family": "rotation", "component": "ROT", "frequency_hz": shaft_hz},
        {"target": "FTF", "family": "cage", "component": "CAGE", "frequency_hz": ftf},
    ]
    for harmonic in (1, 2, 3):
        rows.append({"target": f"BPFO_{harmonic}x", "family": "outer_harmonic", "component": "OR",
                     "frequency_hz": harmonic * bpfo})
        rows.append({"target": f"BPFI_{harmonic}x", "family": "inner_harmonic", "component": "IR",
                     "frequency_hz": harmonic * bpfi})
        rows.append({"target": f"BSF_{harmonic}x", "family": "rolling_harmonic", "component": "B",
                     "frequency_hz": harmonic * bsf})
        for sign, text in ((-1, "minus"), (1, "plus")):
            inner_sideband = harmonic * bpfi + sign * shaft_hz
            rolling_sideband = harmonic * bsf + sign * ftf
            if inner_sideband > 0:
                rows.append({"target": f"BPFI_{harmonic}x_{text}_1X", "family": "inner_shaft_sideband",
                             "component": "IR", "frequency_hz": inner_sideband})
            if rolling_sideband > 0:
                rows.append({"target": f"BSF_{harmonic}x_{text}_FTF", "family": "rolling_cage_sideband",
                             "component": "B", "frequency_hz": rolling_sideband})
    for row in rows:
        alternatives = [other for other in rows if other is not row and other["component"] != row["component"]]
        nearest = min(alternatives, key=lambda other: abs(other["frequency_hz"] - row["frequency_hz"]))
        distance = abs(nearest["frequency_hz"] - row["frequency_hz"])
        search_half_width = max(0.5, 0.01 * row["frequency_hz"])
        row["nearest_other_family_target"] = nearest["target"]
        row["nearest_other_family_distance_hz"] = distance
        row["overlaps_other_family_search_window"] = "Yes" if distance <= search_half_width else "No"
    return rows


def component_expected(fault_label: str, component: str) -> bool:
    return component in fault_tokens(fault_label)


def load_one_x(path: Path) -> dict[str, float]:
    with path.open(encoding="utf-8") as handle:
        return {row["file"]: float(row["consensus_hz"]) for row in csv.DictReader(handle)}


def analyse(data_root: Path, one_x_csv: Path, output_dir: Path) -> list[dict]:
    one_x = load_one_x(one_x_csv)
    rows: list[dict] = []
    files = discover_unique_files(data_root)
    for number, item in enumerate(files, 1):
        meta = parse_filename(item.path)
        if meta["bearing"] not in ("30204", "6204", "N204", "NJ204"):
            continue
        shaft_hz = one_x.get(str(item.path), float(meta["rpm"]) / 60.0)
        targets = compound_targets(meta["bearing"], shaft_hz)
        with TdmsFile.open(item.path) as tdms:
            for channel_index, channel in enumerate(_channels(tdms)):
                fs = 1.0 / float(channel.properties["wf_increment"])
                window = measurement_window(len(channel), fs, meta["bearing"])
                count = min(window.end_sample - window.start_sample, int(round(10 * fs)))
                values = np.asarray(channel[window.start_sample:window.start_sample + count], dtype=np.float64)
                values -= np.mean(values)
                for low, high in CARRIER_BANDS_HZ:
                    sos = signal.butter(4, (low, high), btype="bandpass", fs=fs, output="sos")
                    envelope = np.abs(signal.hilbert(signal.sosfiltfilt(sos, values)))
                    freq, psd = signal.welch(envelope, fs=fs, nperseg=len(envelope), noverlap=0,
                                             scaling="spectrum")
                    amplitude = np.sqrt(psd)
                    for target in targets:
                        observed, prominence = local_envelope_prominence(
                            freq, amplitude, target["frequency_hz"])
                        rows.append({
                            "file": str(item.path), **meta, "channel": f"CH{channel_index}",
                            "excerpt_start_s": window.start_s, "excerpt_duration_s": count / fs,
                            "shaft_hz_candidate": shaft_hz, "carrier_band_hz": f"{low}-{high}",
                            **target, "expected_for_label": "Yes" if component_expected(meta["fault"], target["component"]) else "No",
                            "observed_peak_hz": observed, "local_prominence_db": prominence,
                            "at_least_15_db": "Yes" if prominence >= 15 else "No",
                        })
        print(f"compound {number}/{len(files)}: {item.path}", flush=True)
    _write_csv(output_dir / "compound_feature_validation_10s.csv", rows)
    return rows


def summarize_conditions(rows: list[dict], output_dir: Path) -> list[dict]:
    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        if row["component"] not in ("IR", "OR", "B") or row["expected_for_label"] != "Yes":
            continue
        key = tuple(row[name] for name in ("bearing", "rpm", "fault", "carrier_band_hz", "target", "family", "component"))
        grouped[key].append(row)
    output = []
    names = ("bearing", "rpm", "fault", "carrier_band_hz", "target", "family", "component")
    for key, members in sorted(grouped.items()):
        values = np.array([float(row["local_prominence_db"]) for row in members])
        detected = values >= 15
        output.append({**dict(zip(names, key)), "channels": len(members),
                       "detected_channels": int(np.count_nonzero(detected)),
                       "detection_rate_pct": 100 * float(np.mean(detected)),
                       "median_prominence_db": float(np.median(values)),
                       "q25_prominence_db": float(np.quantile(values, 0.25)),
                       "q75_prominence_db": float(np.quantile(values, 0.75))})
    _write_csv(output_dir / "compound_feature_condition_summary.csv", output)
    return output


def paired_single_compound(rows: list[dict], output_dir: Path) -> tuple[list[dict], list[dict]]:
    """Compare 30204/1600 compounds with matched rotor/channel single faults."""
    eligible = [row for row in rows if row["bearing"] == "30204" and row["rpm"] == "1600"]
    lookup = {(row["rotor"], row["fault"], row["channel"], row["carrier_band_hz"], row["target"]): row
              for row in eligible}
    baseline = {"IR": "IR", "OR": "OR", "B": "B"}
    detail = []
    compounds = ("IR+B", "IR+OR", "OR+B", "IR+OR+B")
    for row in eligible:
        component = row["component"]
        if component not in baseline or row["fault"] not in compounds or not component_expected(row["fault"], component):
            continue
        key = (row["rotor"], baseline[component], row["channel"], row["carrier_band_hz"], row["target"])
        single = lookup.get(key)
        if single is None:
            continue
        single_db = float(single["local_prominence_db"])
        compound_db = float(row["local_prominence_db"])
        detail.append({"bearing": "30204", "rpm": 1600, "rotor": row["rotor"],
                       "channel": row["channel"], "carrier_band_hz": row["carrier_band_hz"],
                       "component": component, "target": row["target"], "family": row["family"],
                       "overlaps_other_family_search_window": row["overlaps_other_family_search_window"],
                       "nearest_other_family_target": row["nearest_other_family_target"],
                       "single_fault": baseline[component], "compound_fault": row["fault"],
                       "single_prominence_db": single_db, "compound_prominence_db": compound_db,
                       "delta_compound_minus_single_db": compound_db - single_db,
                       "single_at_least_15_db": "Yes" if single_db >= 15 else "No",
                       "compound_at_least_15_db": "Yes" if compound_db >= 15 else "No"})
    _write_csv(output_dir / "single_compound_feature_comparison.csv", detail)

    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for row in detail:
        key = tuple(row[name] for name in ("carrier_band_hz", "component", "target", "family",
                                           "overlaps_other_family_search_window", "nearest_other_family_target",
                                           "single_fault", "compound_fault"))
        grouped[key].append(row)
    summary = []
    names = ("carrier_band_hz", "component", "target", "family",
             "overlaps_other_family_search_window", "nearest_other_family_target",
             "single_fault", "compound_fault")
    for key, members in sorted(grouped.items()):
        single = np.array([row["single_prominence_db"] for row in members])
        compound = np.array([row["compound_prominence_db"] for row in members])
        delta = compound - single
        summary.append({**dict(zip(names, key)), "paired_channels": len(members),
                        "single_detection_rate_pct": 100 * float(np.mean(single >= 15)),
                        "compound_detection_rate_pct": 100 * float(np.mean(compound >= 15)),
                        "single_median_db": float(np.median(single)),
                        "compound_median_db": float(np.median(compound)),
                        "median_delta_db": float(np.median(delta)),
                        "increased_over_3db": int(np.count_nonzero(delta > 3)),
                        "decreased_over_3db": int(np.count_nonzero(delta < -3)),
                        "within_plus_minus_3db": int(np.count_nonzero(np.abs(delta) <= 3))})
    _write_csv(output_dir / "single_compound_feature_comparison_summary.csv", summary)
    return detail, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--one-x-csv", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    rows = analyse(args.data_root, args.one_x_csv, args.output_dir)
    summarize_conditions(rows, args.output_dir)
    paired_single_compound(rows, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
