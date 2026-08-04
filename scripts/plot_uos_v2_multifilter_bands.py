#!/usr/bin/env python3
"""Plot the UOS v2 multi-filter band and envelope sensitivity summaries."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LogNorm
import numpy as np


FILTERS = ("butter", "cheby1", "cheby2", "ellip", "bessel")
BANDS = ("B1_0_2k", "B2_2_7k", "B3_7_10k", "B4_10_11p5k", "B5_11p5_12p8k")
FILTER_LABELS = ("Butterworth", "Chebyshev I", "Chebyshev II", "Elliptic", "Bessel")
BAND_LABELS = ("0–2", "2–7", "7–10", "10–11.5", "11.5–12.8")
CUTOFFS = (11500.0, 10000.0, 7000.0, 2000.0)
CUTOFF_LABELS = ("원신호", "LPF 11.5", "LPF 10", "LPF 7", "LPF 2")


def _font() -> None:
    fonts = [font.name for font in font_manager.fontManager.ttflist if "NanumGothic" in font.name]
    if fonts:
        plt.rcParams["font.family"] = fonts[0]
    plt.rcParams["axes.unicode_minus"] = False


def _read(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _matrix(rows: list[dict], value: str, *, component: str | None = None) -> np.ndarray:
    lookup = {(row["filter"], row["band"]): float(row[value]) for row in rows
              if component is None or row.get("component") == component}
    return np.array([[lookup[(filter_name, band)] for band in BANDS[:4 if component else 5]]
                     for filter_name in FILTERS], dtype=float)


def _channel_median_matrix(rows: list[dict], channel: str) -> np.ndarray:
    """Return per-filter, per-band median peaks for one acquisition channel."""
    values: dict[tuple[str, str], list[float]] = {
        (filter_name, band): [] for filter_name in FILTERS for band in BANDS
    }
    for row in rows:
        if row["channel"] == channel:
            values[(row["filter"], row["band"])].append(float(row["band_peak_abs_g"]))
    missing = [key for key, peaks in values.items() if not peaks]
    if missing:
        raise ValueError(f"Missing {channel} filter/band rows: {missing}")
    return np.array([
        [float(np.median(values[(filter_name, band)])) for band in BANDS]
        for filter_name in FILTERS
    ])


def _annotated_heatmap(axis, values: np.ndarray, columns: tuple[str, ...], title: str,
                       colorbar_label: str, fmt: str, cmap: str,
                       row_labels: tuple[str, ...] = FILTER_LABELS):
    image = axis.imshow(values, cmap=cmap, aspect="auto")
    axis.set_xticks(range(len(columns)), columns)
    axis.set_yticks(range(len(row_labels)), row_labels)
    axis.set_xlabel("주파수 구간(kHz)")
    axis.set_title(title)
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            text_color = "white" if values[i, j] > (np.nanmin(values) + np.nanmax(values)) / 2 else "black"
            axis.text(j, i, format(values[i, j], fmt), ha="center", va="center", color=text_color, fontsize=9)
    colorbar = axis.figure.colorbar(image, ax=axis, fraction=0.046, pad=0.04)
    colorbar.set_label(colorbar_label)
    return image


def plot(results_dir: Path, figures_dir: Path) -> tuple[Path, Path, Path, Path]:
    _font()
    figures_dir.mkdir(parents=True, exist_ok=True)
    band_rows = _read(results_dir / "multifilter_band_summary.csv")
    band_metric_rows = _read(results_dir / "multifilter_band_metrics.csv")
    component_rows = _read(results_dir / "multifilter_component_summary.csv")
    total_channels = int(float(band_rows[0]["channels"]))

    counts = _matrix(band_rows, "peak_over_50g_channels")
    ch0_median_peak = _channel_median_matrix(band_metric_rows, "CH0")
    ch1_median_peak = _channel_median_matrix(band_metric_rows, "CH1")
    fig, axes = plt.subplots(1, 3, figsize=(21, 5.4), constrained_layout=True)
    _annotated_heatmap(
        axes[0], counts, BAND_LABELS,
        f"필터 후 최대 절대값이 50 g를 넘은 채널 수 (전체 {total_channels}개)",
        "채널 수", ".0f", "Reds",
    )
    _annotated_heatmap(
        axes[1], ch0_median_peak, BAND_LABELS,
        "CH0: 필터 후 최대 절대값의 중앙값", "CH0 중앙값(g)", ".1f", "Blues",
    )
    _annotated_heatmap(
        axes[2], ch1_median_peak, BAND_LABELS,
        "CH1: 필터 후 최대 절대값의 중앙값", "CH1 중앙값(g)", ".1f", "Blues",
    )
    fig.suptitle("IR+OR+B · 1400/1600 RPM · 원신호 ±50 g 초과 채널의 필터 민감도", fontsize=14)
    band_output = figures_dir / "multifilter_band_peak_summary.png"
    fig.savefig(band_output, dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.4), constrained_layout=True)
    for axis, component, label in zip(axes, ("IR", "OR", "B"), ("내륜(IR)", "외륜(OR)", "볼·롤러(B)")):
        rates = _matrix(component_rows, "detection_rate_pct", component=component)
        _annotated_heatmap(
            axis, rates, BAND_LABELS[:4],
            f"{label}: 비중첩 후보 중 하나 이상 검출", "검출 채널 비율(%)", ".1f", "YlGnBu",
        )
    fig.suptitle(
        f"포락선 스펙트럼 결함 계열 검출률 · 국소 돌출도 15 dB 이상 · 전체 {total_channels}개 채널",
        fontsize=14,
    )
    envelope_output = figures_dir / "multifilter_envelope_detection_summary.png"
    fig.savefig(envelope_output, dpi=180)
    plt.close(fig)

    cutoff_rows = _read(results_dir / "multifilter_cutoff_scenario_summary.csv")
    consensus_rows = _read(results_dir / "multifilter_cutoff_consensus_summary.csv")
    cutoff_lookup = {
        (row["filter"], float(row["cutoff_hz"])): float(row["retained_peak_over_50g_channels"])
        for row in cutoff_rows
    }
    per_filter_counts = [
        [float(total_channels)] + [cutoff_lookup[(filter_name, cutoff)] for cutoff in CUTOFFS]
        for filter_name in FILTERS
    ]
    consensus_lookup = {
        float(row["cutoff_hz"]): float(row["majority_at_least_3_of_5_channels"])
        for row in consensus_rows
    }
    scenario_counts = np.array(
        per_filter_counts + [[float(total_channels)] + [consensus_lookup[cutoff] for cutoff in CUTOFFS]]
    )
    fig, axis = plt.subplots(figsize=(10.5, 5.8), constrained_layout=True)
    _annotated_heatmap(
        axis,
        scenario_counts,
        CUTOFF_LABELS,
        "고주파 성분을 단계적으로 감쇠했을 때 50 g를 넘는 채널 수",
        "50 g 초과 채널 수",
        ".0f",
        "OrRd",
        FILTER_LABELS + ("필터 3/5 이상 동의",),
    )
    axis.set_xlabel("가상 저역통과 시나리오")
    fig.suptitle(
        f"IR+OR+B · 1400/1600 RPM · 측정구간 원신호 ±50 g 초과 {total_channels}채널",
        fontsize=14,
    )
    cutoff_output = figures_dir / "multifilter_cutoff_scenario_summary.png"
    fig.savefig(cutoff_output, dpi=180)
    plt.close(fig)

    histogram_rows = [
        row for row in _read(results_dir / "multifilter_band_g_histogram.csv")
        if row["filter"] == "butter" and row["bearing"] == "All" and row["rpm"] == "All"
    ]
    histogram_bins = []
    for row in histogram_rows:
        if row["band"] == BANDS[0]:
            histogram_bins.append((float(row["bin_low_g"]), row["abs_g_bin"]))
    histogram_bins = [label for _, label in sorted(histogram_bins)]
    histogram_lookup = {
        (row["band"], row["abs_g_bin"]): float(row["sample_pct"])
        for row in histogram_rows
    }
    histogram_pct = np.array([
        [histogram_lookup[(band, label)] for label in histogram_bins]
        for band in BANDS
    ])

    fig, axes = plt.subplots(1, 2, figsize=(18, 6.2), constrained_layout=True)
    positive = histogram_pct[histogram_pct > 0]
    minimum = max(float(np.min(positive)) if len(positive) else 1e-9, 1e-9)
    image = axes[0].imshow(
        np.ma.masked_less_equal(histogram_pct, 0),
        aspect="auto",
        cmap="YlOrRd",
        norm=LogNorm(vmin=minimum, vmax=max(float(np.max(histogram_pct)), minimum)),
    )
    axes[0].set_xticks(range(len(histogram_bins)), histogram_bins, rotation=55, ha="right")
    axes[0].set_yticks(range(len(BAND_LABELS)), BAND_LABELS)
    axes[0].set_xlabel("필터 출력의 절대 가속도 구간(g)")
    axes[0].set_ylabel("주파수 구간(kHz)")
    axes[0].set_title("120초 전체 표본의 절대 g 분포")
    colorbar = fig.colorbar(image, ax=axes[0], fraction=0.046, pad=0.04)
    colorbar.set_label("전체 표본 비율(%, 로그 색상)")

    thresholds = (10.0, 20.0, 30.0, 40.0, 50.0)
    bin_lows = np.array([float(label.split("-")[0]) for label in histogram_bins])
    for band, label in zip(BANDS, BAND_LABELS):
        row = histogram_pct[BANDS.index(band)]
        exceedance = np.array(
            [float(np.sum(row[bin_lows >= threshold])) for threshold in thresholds], dtype=float
        )
        exceedance[exceedance <= 0] = np.nan
        axes[1].plot(thresholds, exceedance, marker="o", label=f"{label} kHz")
    axes[1].set_yscale("log")
    axes[1].set_xlabel("절대 가속도 기준(g)")
    axes[1].set_ylabel("기준 초과 표본 비율(%)")
    axes[1].set_title("대역별 큰 진폭 표본의 꼬리 분포")
    axes[1].grid(True, which="both", alpha=0.3)
    axes[1].legend()
    fig.suptitle(
        f"Butterworth 필터 · 공회전 제외 120초 · 원신호 ±50 g 초과 {total_channels}채널",
        fontsize=14,
    )
    distribution_output = figures_dir / "multifilter_band_g_distribution.png"
    fig.savefig(distribution_output, dpi=180)
    plt.close(fig)
    return band_output, envelope_output, cutoff_output, distribution_output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--figures-dir", type=Path, required=True)
    args = parser.parse_args()
    plot(args.results_dir, args.figures_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
