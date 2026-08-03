#!/usr/bin/env python3
"""Plot matched single-versus-compound feature changes for 30204/1600 RPM."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np


def plot(summary_csv: Path, output_png: Path) -> None:
    with summary_csv.open(encoding="utf-8") as handle:
        source = list(csv.DictReader(handle))
    source = [row for row in source if row["carrier_band_hz"] == "2000-7000"]
    fonts = [font.name for font in font_manager.fontManager.ttflist if "NanumGothic" in font.name]
    if fonts: plt.rcParams["font.family"] = fonts[0]
    plt.rcParams["axes.unicode_minus"] = False
    components = ("IR", "OR", "B")
    compounds = {"IR": ("IR+B", "IR+OR", "IR+OR+B"),
                 "OR": ("OR+B", "IR+OR", "IR+OR+B"),
                 "B": ("IR+B", "OR+B", "IR+OR+B")}
    fig, axes = plt.subplots(1, 3, figsize=(21, 9), constrained_layout=True)
    for axis, component in zip(axes, components):
        rows = [row for row in source if row["component"] == component]
        targets = sorted({row["target"] for row in rows})
        cols = compounds[component]
        matrix = np.full((len(targets), len(cols)), np.nan)
        detection = np.full_like(matrix, np.nan)
        overlap = np.zeros_like(matrix, dtype=bool)
        for i, target in enumerate(targets):
            for j, compound in enumerate(cols):
                match = next((row for row in rows if row["target"] == target and row["compound_fault"] == compound), None)
                if match:
                    matrix[i, j] = float(match["median_delta_db"])
                    detection[i, j] = float(match["compound_detection_rate_pct"])
                    overlap[i, j] = match["overlaps_other_family_search_window"] == "Yes"
        image = axis.imshow(matrix, vmin=-15, vmax=15, cmap="coolwarm", aspect="auto")
        labels = [target + ("*" if any(overlap[i]) else "") for i, target in enumerate(targets)]
        axis.set_yticks(range(len(targets)), labels, fontsize=8)
        axis.set_xticks(range(len(cols)), cols, rotation=35, ha="right")
        axis.set_title(f"{component} 계열 · 복합 조건값 - 단일 조건값")
        axis.set_xlabel("복합 베어링 결함")
        for i in range(len(targets)):
            for j in range(len(cols)):
                if np.isfinite(matrix[i, j]):
                    axis.text(j, i, f"{matrix[i,j]:+.1f}\n({detection[i,j]:.0f}%)",
                              ha="center", va="center", fontsize=7,
                              color="white" if abs(matrix[i,j]) > 8 else "black")
    axes[0].set_ylabel("검사 주파수 · *는 다른 결함 계열과 탐색 창 중첩")
    cbar = fig.colorbar(image, ax=axes, fraction=0.02, pad=0.02)
    cbar.set_label("복합 결함 prominence - 대응 단일 결함 prominence(dB)")
    fig.suptitle("30204 · 1600 RPM · 동일 로터·채널 짝 비교 · 2–7 kHz 포락선\n괄호: 복합 조건의 15 dB 이상 검출률")
    output_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_png, dpi=180)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary-csv", type=Path, required=True)
    parser.add_argument("--output-png", type=Path, required=True)
    args = parser.parse_args(); plot(args.summary_csv, args.output_png); return 0


if __name__ == "__main__":
    raise SystemExit(main())
