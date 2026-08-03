#!/usr/bin/env python3
"""Create compact figures from committed UOS v2 clipping CSV results."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def relevant_target(fault: str, target: str) -> bool:
    tokens = fault.split("+")
    return ((target == "BPFI" and "IR" in tokens) or
            (target == "BPFO" and "OR" in tokens) or
            (target == "BSF" and "B" in tokens))


def plot_results(results: Path, figures: Path) -> None:
    korean_fonts = [font.name for font in font_manager.fontManager.ttflist if "NanumGothic" in font.name]
    if korean_fonts:
        plt.rcParams["font.family"] = korean_fonts[0]
    plt.rcParams["axes.unicode_minus"] = False
    figures.mkdir(parents=True, exist_ok=True)
    scan = read_csv(results / "clipping_scan_file.csv")
    events = read_csv(results / "rail_event_cross_channel.csv")
    bands = read_csv(results / "band_metrics_10s.csv")
    envelope = read_csv(results / "envelope_validation_10s.csv")
    rpm_rows = read_csv(results / "one_x_candidates.csv")

    # Figure 1: clipping and shortcut risk.
    fault_order = ["H", "IR", "OR", "B", "IR+B", "IR+OR", "OR+B", "IR+OR+B"]
    totals, clipped = [], []
    for fault in fault_order:
        rows = [r for r in scan if r["fault"] == fault]
        totals.append(len(rows))
        clipped.append(sum(int(r["n_at_rail_all_channels"]) > 0 for r in rows))
    event_counter = Counter(int(r["other_channels_above_own_p999"]) for r in events)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    x = np.arange(len(fault_order))
    axes[0].bar(x, totals, color="#d9d9d9", label="전체 파일")
    axes[0].bar(x, clipped, color="#c0392b", label="ADC 포화 포함 파일")
    axes[0].set_xticks(x, fault_order, rotation=35, ha="right")
    axes[0].set_ylabel("파일 수")
    axes[0].set_title("베어링 결함 조합별 ADC 포화 파일")
    axes[0].legend()
    keys = range(4)
    axes[1].bar(keys, [event_counter[k] for k in keys], color="#4472c4")
    axes[1].set_xticks(list(keys))
    axes[1].set_xlabel("±1 ms 이내 동시에 크게 반응한 다른 채널 수")
    axes[1].set_ylabel("ADC 포화 사건 수")
    axes[1].set_title("ADC 포화 시점의 다른 채널 반응")
    fig.tight_layout()
    fig.savefig(figures / "clipping_risk_dashboard.png", dpi=180)
    plt.close(fig)

    # Figure 2: retained band information and envelope validation.
    clipped_map = {r["file"]: int(r["n_at_rail_all_channels"]) > 0 for r in scan}
    band_order = ["0.5-2000", "2000-7000", "7000-10000", "10000-11200"]
    medians = {state: [] for state in (False, True)}
    for state in (False, True):
        for band in band_order:
            values = [float(r["band_energy_pct_of_centered_raw"]) for r in bands
                      if r["band_hz"] == band and clipped_map[r["file"]] == state]
            medians[state].append(float(np.median(values)))

    detections: dict[tuple[str, str], list[bool]] = defaultdict(list)
    for row in envelope:
        if row["target"] in ("BPFO", "BPFI", "BSF") and relevant_target(row["fault"], row["target"]):
            detections[(row["target"], row["band_hz"])].append(row["at_least_15_db"] == "Yes")

    unique_rpm = {}
    for row in rpm_rows:
        unique_rpm[row["file"]] = (float(row["nominal_rpm"]), float(row["consensus_rpm"]))

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    x = np.arange(len(band_order)); width = 0.36
    axes[0].bar(x - width / 2, medians[False], width, label="ADC 포화 없음", color="#70ad47")
    axes[0].bar(x + width / 2, medians[True], width, label="ADC 포화 있음", color="#c0392b")
    axes[0].set_xticks(x, ["0.5-2k", "2-7k", "7-10k", "10-11.2k"])
    axes[0].set_ylabel("원신호 대비 대역 에너지 중앙값(%)")
    axes[0].set_title("주파수 대역별 에너지 중앙값")
    axes[0].legend()

    targets = ["BPFO", "BPFI", "BSF"]
    carrier_bands = ["2000-7000", "7000-10000", "10000-11200"]
    matrix = np.array([[100 * np.mean(detections[(target, band)]) for band in carrier_bands]
                       for target in targets])
    image = axes[1].imshow(matrix, vmin=0, vmax=100, cmap="Blues", aspect="auto")
    axes[1].set_xticks(range(3), ["2-7k", "7-10k", "10-11.2k"])
    axes[1].set_yticks(range(3), targets)
    axes[1].set_title("레이블에 포함된 결함주파수 검출률(15 dB 이상, %)")
    for i in range(3):
        for j in range(3):
            axes[1].text(j, i, f"{matrix[i,j]:.0f}", ha="center", va="center")
    fig.colorbar(image, ax=axes[1], fraction=0.046)

    nominal = [x[0] for x in unique_rpm.values()]
    estimated = [x[1] for x in unique_rpm.values()]
    axes[2].scatter(nominal, estimated, s=18, alpha=0.65)
    axes[2].plot([550, 1650], [550, 1650], "k--", linewidth=1)
    axes[2].set_xlim(550, 1650); axes[2].set_ylim(550, 1650)
    axes[2].set_xlabel("설정 회전수(RPM)")
    axes[2].set_ylabel("진동 신호에서 추정한 1× 회전수(RPM)")
    axes[2].set_title("설정 회전수와 진동 기반 추정값 비교")
    fig.tight_layout()
    fig.savefig(figures / "physical_signal_dashboard.png", dpi=180)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--figures", type=Path, required=True)
    args = parser.parse_args()
    plot_results(args.results, args.figures)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
