#!/usr/bin/env python3
"""Summarize and plot the Task B low-pass sweep."""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np


CUTOFFS = (3000, 5000, 7000, 9000, 10000, 11000)


def _write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def interpret_row(row: dict) -> dict:
    peaks = {cutoff: float(row[f"lpf_{cutoff}_peak_abs_g"]) for cutoff in CUTOFFS}
    descending = (11000, 10000, 9000, 7000, 5000, 3000)
    drops = {(high, low): peaks[high] - peaks[low] for high, low in zip(descending[:-1], descending[1:])}
    interval, largest_drop = max(drops.items(), key=lambda item: item[1])
    branch = "L3" if peaks[7000] >= 50 else ("L2" if peaks[10000] >= 50 else "L1")
    # A negative drop indicates filter-reconstruction overshoot or cancellation;
    # it is reported rather than forced into a monotonic physical interpretation.
    negative_steps = sum(value < 0 for value in drops.values())
    return {
        "file": row["file"], "bearing": row["bearing"], "rpm": row["rpm"],
        "rotor": row["rotor"], "fault": row["fault"], "channel": row["channel"],
        "raw_peak_abs_g": float(row["raw_peak_abs_g"]),
        **{f"peak_{cutoff}_hz_g": peaks[cutoff] for cutoff in CUTOFFS},
        "task_b_branch": branch,
        "largest_positive_drop_interval_hz": f"{interval[0]}->{interval[1]}",
        "largest_positive_drop_g": largest_drop,
        "negative_or_overshoot_steps": negative_steps,
        "task_b_caution": "post-clipping_filter_reconstruction" if negative_steps else "none_observed",
    }


def plot(input_csv: Path, output_csv: Path, figures_dir: Path) -> list[dict]:
    with input_csv.open(encoding="utf-8") as handle:
        source = list(csv.DictReader(handle))
    rows = [interpret_row(row) for row in source]
    _write_csv(output_csv, rows)
    figures_dir.mkdir(parents=True, exist_ok=True)
    fonts = [font.name for font in font_manager.fontManager.ttflist if "NanumGothic" in font.name]
    if fonts: plt.rcParams["font.family"] = fonts[0]
    plt.rcParams["axes.unicode_minus"] = False
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows: grouped[row["file"]].append(row)
    for file_name, members in grouped.items():
        members.sort(key=lambda row: row["channel"])
        fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True)
        for axis, row in zip(axes.flat, members):
            y = [row[f"peak_{cutoff}_hz_g"] for cutoff in CUTOFFS]
            axis.plot(np.array(CUTOFFS) / 1000, y, marker="o", linewidth=2)
            axis.axhline(50, color="#c0392b", linestyle="--", linewidth=1, label="50 g 기준")
            axis.set_title(f"{row['channel'].replace('Channel ', 'CH')} · {row['task_b_branch']}")
            axis.grid(alpha=0.25)
            axis.set_ylabel("저역통과 후 절대 최대값(g)")
            axis.legend(loc="best")
        for axis in axes[-1]: axis.set_xlabel("저역통과 차단주파수(kHz)")
        first = members[0]
        fig.suptitle(f"Task B · {first['bearing']} · {first['rpm']} RPM · 로터 {first['rotor']} · 베어링 {first['fault']}")
        fig.tight_layout(rect=(0, 0, 1, 0.96))
        safe = Path(file_name).stem
        fig.savefig(figures_dir / f"task_b_{safe}.png", dpi=170)
        plt.close(fig)
    return rows


def combine_task_b_c(task_b_rows: list[dict], compound_csv: Path, output_csv: Path) -> list[dict]:
    with compound_csv.open(encoding="utf-8") as handle:
        features = list(csv.DictReader(handle))
    lookup: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for row in features:
        if (row["expected_for_label"] == "Yes" and row["component"] in ("IR", "OR", "B")
                and row["overlaps_other_family_search_window"] == "No"):
            lookup[(row["file"], row["channel"], row["carrier_band_hz"])].append(row)
    band_for_branch = {"L1": "10000-11200", "L2": "7000-10000", "L3": "2000-7000"}
    output = []
    for row in task_b_rows:
        channel = row["channel"].replace("Channel ", "CH")
        branch = row["task_b_branch"]
        selected_band = band_for_branch[branch]
        selected = lookup.get((row["file"], channel, selected_band), [])
        control = lookup.get((row["file"], channel, "2000-7000"), [])
        top = max(selected, key=lambda item: float(item["local_prominence_db"]), default=None)
        control_top = max(control, key=lambda item: float(item["local_prominence_db"]), default=None)
        applicable = float(row["raw_peak_abs_g"]) >= 50
        output.append({**row, "task_b_applicable_raw_peak_at_least_50g": "Yes" if applicable else "No",
                       "task_b_indicated_carrier_band_hz": selected_band,
                       "task_c_status": "Not applicable" if not selected else
                           ("M+ (expanded family)" if any(float(item["local_prominence_db"]) >= 15 for item in selected)
                            else "M- (expanded family)"),
                       "task_c_top_target": top["target"] if top else "None",
                       "task_c_top_prominence_db": float(top["local_prominence_db"]) if top else math.nan,
                       "control_2_7khz_status": "Not applicable" if not control else
                           ("M+ (expanded family)" if any(float(item["local_prominence_db"]) >= 15 for item in control)
                            else "M- (expanded family)"),
                       "control_2_7khz_top_target": control_top["target"] if control_top else "None",
                       "control_2_7khz_top_prominence_db": float(control_top["local_prominence_db"]) if control_top else math.nan})
    _write_csv(output_csv, output)
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--figures-dir", type=Path, required=True)
    parser.add_argument("--compound-csv", type=Path)
    parser.add_argument("--combined-output-csv", type=Path)
    args = parser.parse_args()
    rows = plot(args.input_csv, args.output_csv, args.figures_dir)
    if args.compound_csv and args.combined_output_csv:
        combine_task_b_c(rows, args.compound_csv, args.combined_output_csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
