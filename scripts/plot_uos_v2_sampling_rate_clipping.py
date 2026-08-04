#!/usr/bin/env python3
"""Create concise figures for the UOS v2 sampling-rate clipping comparison."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np


RATE_ORDER = ("12.8 kHz", "17.0667 kHz", "25.6 kHz")
ROTOR_ORDER = ("H", "L", "M3", "U3")


def _read(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _font() -> None:
    candidates = [font.name for font in font_manager.fontManager.ttflist if "NanumGothic" in font.name]
    if candidates:
        plt.rcParams["font.family"] = candidates[0]
    plt.rcParams["axes.unicode_minus"] = False


def _annotate_bars(axis, bars, decimals: int = 1) -> None:
    for bar in bars:
        value = bar.get_height()
        axis.text(bar.get_x() + bar.get_width() / 2, value, f"{value:.{decimals}f}",
                  ha="center", va="bottom", fontsize=9)


def plot(results_dir: Path, figures_dir: Path) -> tuple[Path, Path, Path]:
    _font()
    figures_dir.mkdir(parents=True, exist_ok=True)
    summary = _read(results_dir / "sampling_rate_summary.csv")
    files = _read(results_dir / "sampling_rate_file_metrics.csv")
    channels = _read(results_dir / "sampling_rate_channel_metrics.csv")
    summary_by_rate = {row["rate_label"]: row for row in summary}

    actual_khz = [float(summary_by_rate[label]["actual_rate_hz"]) / 1000.0 for label in RATE_ORDER]
    alias_free_khz = [
        float(summary_by_rate[label]["approx_alias_free_bandwidth_hz"]) / 1000.0 for label in RATE_ORDER
    ]
    x = np.arange(len(RATE_ORDER))
    fig, axis = plt.subplots(figsize=(9.2, 5.2), constrained_layout=True)
    bars_actual = axis.bar(x - 0.18, actual_khz, width=0.36, label="TDMS 실제 sampling rate")
    bars_band = axis.bar(x + 0.18, alias_free_khz, width=0.36, label="근사 alias-free bandwidth (0.45×fs)")
    _annotate_bars(axis, bars_actual, 4)
    _annotate_bars(axis, bars_band, 2)
    axis.set_xticks(x, RATE_ORDER)
    axis.set_ylabel("주파수(kHz)")
    axis.set_title("요청값과 실제 TDMS sampling rate 확인")
    axis.legend()
    axis.grid(axis="y", alpha=0.25)
    rate_output = figures_dir / "sampling_rate_verification.png"
    fig.savefig(rate_output, dpi=180)
    plt.close(fig)

    rail_channels = np.zeros((len(ROTOR_ORDER), len(RATE_ORDER)))
    rail_events = np.zeros_like(rail_channels)
    for row in files:
        i = ROTOR_ORDER.index(row["rotor"])
        j = RATE_ORDER.index(row["rate_label"])
        rail_channels[i, j] = float(row["channels_with_exact_rail"])
        rail_events[i, j] = float(row["exact_rail_events"])
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.9), constrained_layout=True)
    for axis, values, title, cmap in (
        (axes[0], rail_channels, "ADC rail이 발생한 채널 수 (파일당 4채널)", "Reds"),
        (axes[1], rail_events, "유효 구간의 ADC rail 사건 수", "Oranges"),
    ):
        image = axis.imshow(values, aspect="auto", cmap=cmap)
        axis.set_xticks(range(len(RATE_ORDER)), RATE_ORDER)
        axis.set_yticks(range(len(ROTOR_ORDER)), ROTOR_ORDER)
        axis.set_xlabel("sampling rate")
        axis.set_ylabel("로터 조건")
        axis.set_title(title)
        for i in range(values.shape[0]):
            for j in range(values.shape[1]):
                axis.text(j, i, f"{values[i, j]:.0f}", ha="center", va="center")
        fig.colorbar(image, ax=axis, fraction=0.046, pad=0.04)
    fig.suptitle("N204 · 1600 RPM · IR+OR+B · 공회전 제외 · rate별 3,072,000표본", fontsize=14)
    clipping_output = figures_dir / "clipping_by_sampling_rate.png"
    fig.savefig(clipping_output, dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(14.5, 5.0), constrained_layout=True)
    measures = (
        ("raw_peak_abs_g", "원신호 절대 peak", "g"),
        ("raw_p99_99_abs_g", "원신호 p99.99", "g"),
        ("common_0_5p5khz_p99_99_abs_g", "공통 0–5.5 kHz p99.99", "g"),
    )
    for axis, (field, title, unit) in zip(axes, measures):
        values = [
            [float(row[field]) for row in channels if row["rate_label"] == label]
            for label in RATE_ORDER
        ]
        axis.boxplot(values, labels=RATE_ORDER, showfliers=True)
        axis.set_title(title)
        axis.set_ylabel(unit)
        axis.grid(axis="y", alpha=0.25)
    fig.suptitle("채널별 진폭 분포 비교 · 각 sampling rate당 16채널 기록", fontsize=14)
    amplitude_output = figures_dir / "amplitude_distribution_by_sampling_rate.png"
    fig.savefig(amplitude_output, dpi=180)
    plt.close(fig)
    return rate_output, clipping_output, amplitude_output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--figures-dir", type=Path, required=True)
    args = parser.parse_args()
    plot(args.results_dir, args.figures_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
