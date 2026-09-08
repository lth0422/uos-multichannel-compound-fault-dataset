#!/usr/bin/env python3
"""Create one CH0 envelope-spectrum figure for every file in a validation run."""

from __future__ import annotations

import argparse
import csv
import math
from itertools import combinations
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.lines import Line2D
from nptdms import TdmsFile
from PIL import Image
from scipy import signal

try:
    from scripts.analyze_uos_v2_clipping import _channels, bearing_orders
    from scripts.validate_uos_v2_acquisition import COMPONENT_LABEL, ROTOR_ORDER, fault_components, spectrum_amplitude
except ModuleNotFoundError:  # Direct execution from scripts/.
    from analyze_uos_v2_clipping import _channels, bearing_orders
    from validate_uos_v2_acquisition import COMPONENT_LABEL, ROTOR_ORDER, fault_components, spectrum_amplitude


COMPONENT_LINESTYLE = {"IR": "--", "OR": "-.", "B": ":"}
COMPONENT_KOREAN = {"IR": "내륜", "OR": "외륜", "B": "롤러"}

_KOREAN_FONTS = [font.name for font in font_manager.fontManager.ttflist if "NanumGothic" in font.name]
if _KOREAN_FONTS:
    plt.rcParams.update({"font.family": _KOREAN_FONTS[0], "axes.unicode_minus": False})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def pairwise_interaction_targets(components: set[str], base_hz: dict[str, float]) -> list[dict]:
    """Return first-order sum/difference candidates for compound bearing faults."""
    rows = []
    ordered = [component for component in ("IR", "OR", "B") if component in components]
    for left, right in combinations(ordered, 2):
        left_label = COMPONENT_LABEL[left]
        right_label = COMPONENT_LABEL[right]
        rows.extend([
            {
                "label": f"|{left_label}-{right_label}|",
                "frequency_hz": abs(base_hz[left] - base_hz[right]),
                "kind": "difference",
            },
            {
                "label": f"{left_label}+{right_label}",
                "frequency_hz": base_hz[left] + base_hz[right],
                "kind": "sum",
            },
        ])
    return rows


def reference_targets(bearing: str, fault: str, shaft_hz: float) -> tuple[list[dict], list[dict]]:
    orders = bearing_orders(bearing)
    components = fault_components(fault)
    base_hz = {
        "IR": orders["BPFI"] * shaft_hz,
        "OR": orders["BPFO"] * shaft_hz,
        "B": orders["BSF"] * shaft_hz,
    }
    primary = [{"label": "1X", "frequency_hz": shaft_hz, "component": "ROT", "harmonic": 1}]
    for component in ("IR", "OR", "B"):
        if component not in components:
            continue
        for harmonic in (1, 2, 3):
            primary.append({
                "label": f"{COMPONENT_LABEL[component]} {harmonic}X",
                "frequency_hz": base_hz[component] * harmonic,
                "component": component,
                "harmonic": harmonic,
            })
    return primary, pairwise_interaction_targets(components, base_hz)


def canonical_image_name(row: dict[str, str]) -> str:
    return (
        f"{int(float(row['rpm'])):04d}rpm_{row['rotor']}_{row['fault']}"
        f"_R{int(float(row.get('repeat') or 1))}_CH0.png"
    )


def load_envelope_spectrum(
    path: Path,
    start_s: float,
    duration_s: float,
    carrier_low_hz: float,
    carrier_high_hz: float,
) -> tuple[np.ndarray, np.ndarray, float]:
    with TdmsFile.open(path) as tdms:
        channel = _channels(tdms)[0]
        fs = 1.0 / float(channel.properties["wf_increment"])
        start = int(round(start_s * fs))
        end = start + int(round(duration_s * fs))
        if end > len(channel):
            raise ValueError(f"120초 분석 구간이 부족함: {path}")
        values = np.asarray(channel[start:end], dtype=np.float64)
    safe_upper = 0.45 * fs
    if carrier_high_hz > safe_upper:
        raise ValueError(f"carrier 상한 {carrier_high_hz:g} Hz가 alias-free 근사 상한 {safe_upper:g} Hz를 넘음")
    sos = signal.butter(4, (carrier_low_hz, carrier_high_hz), btype="bandpass", fs=fs, output="sos")
    envelope = np.abs(signal.hilbert(signal.sosfiltfilt(sos, values)))
    frequency, amplitude = spectrum_amplitude(envelope, fs, segment_s=8.0)
    return frequency, amplitude, fs


def plot_one(
    frequency: np.ndarray,
    amplitude: np.ndarray,
    primary: list[dict],
    interactions: list[dict],
    row: dict[str, str],
    output_path: Path,
    carrier_band: tuple[float, float],
    x_max_hz: float,
) -> None:
    mask = (frequency > 0) & (frequency <= x_max_hz)
    scale = float(np.max(amplitude[mask])) if np.any(mask) else 1.0
    normalized = amplitude / max(scale, np.finfo(float).eps)
    fig, ax = plt.subplots(figsize=(12, 5.8), constrained_layout=True)
    ax.plot(frequency[mask], normalized[mask], color="#1565c0", linewidth=0.9)
    for target in primary:
        component = target["component"]
        style = "-" if component == "ROT" else COMPONENT_LINESTYLE[component]
        width = 1.6 if component == "ROT" else 1.0
        ax.axvline(target["frequency_hz"], color="#c62828", linestyle=style, linewidth=width, alpha=0.9)
    for target in interactions:
        ax.axvline(target["frequency_hz"], color="#7b1fa2", linestyle=(0, (2, 2)), linewidth=0.8, alpha=0.7)
    ax.set_xlim(0, x_max_hz)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("포락선 주파수 (Hz)")
    ax.set_ylabel("정규화 포락선 스펙트럼 (최댓값=1)")
    ax.set_title(
        f"{row['bearing']} · {row['fault']} · {row['rotor']} · {int(float(row['rpm']))} RPM · CH0\n"
        f"{carrier_band[0] / 1000:g}–{carrier_band[1] / 1000:g} kHz 대역 · 원파일 60–180초"
    )
    ax.grid(True, alpha=0.22)
    handles = [
        Line2D([0], [0], color="#1565c0", label="포락선 FFT"),
        Line2D([0], [0], color="#c62828", linestyle="-", label="회전주파수 1X"),
    ]
    for component in ("IR", "OR", "B"):
        if component in fault_components(row["fault"]):
            handles.append(Line2D(
                [0], [0], color="#c62828", linestyle=COMPONENT_LINESTYLE[component],
                label=f"{COMPONENT_LABEL[component]} ({COMPONENT_KOREAN[component]}) 1–3차",
            ))
    if interactions:
        handles.append(Line2D([0], [0], color="#7b1fa2", linestyle=(0, (2, 2)), label="합·차 주파수 후보"))
    ax.legend(handles=handles, loc="upper right", fontsize=8, ncol=2)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=170)
    plt.close(fig)


def make_contact_sheet(image_paths: list[Path], output_path: Path) -> None:
    columns, thumb_size = 4, (420, 210)
    rows = math.ceil(len(image_paths) / columns)
    sheet = Image.new("RGB", (columns * thumb_size[0], rows * thumb_size[1]), "white")
    for index, path in enumerate(image_paths):
        with Image.open(path) as source:
            image = source.convert("RGB")
            image.thumbnail(thumb_size)
            x = (index % columns) * thumb_size[0] + (thumb_size[0] - image.width) // 2
            y = (index // columns) * thumb_size[1] + (thumb_size[1] - image.height) // 2
            sheet.paste(image, (x, y))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=90)


def run(source_run: Path, output_dir: Path, carrier_band: tuple[float, float]) -> list[dict]:
    manifest = read_csv(source_run / "results" / "input_manifest.csv")
    detail = read_csv(source_run / "results" / "frequency_detection_detail.csv")
    shaft_by_file = {
        row["file"]: float(row["expected_hz"])
        for row in detail
        if row["channel"] == "CH0" and row["method"] == "raw FFT" and row["component"] == "ROT"
    }
    manifest.sort(key=lambda row: (int(float(row["rpm"])), ROTOR_ORDER.get(row["rotor"], 999), int(float(row.get("repeat") or 1))))
    all_targets = []
    prepared = []
    for row in manifest:
        shaft_hz = shaft_by_file[row["file"]]
        primary, interactions = reference_targets(row["bearing"], row["fault"], shaft_hz)
        prepared.append((row, primary, interactions))
        all_targets.extend(primary)
        all_targets.extend(interactions)
    highest = max(target["frequency_hz"] for target in all_targets)
    x_max_hz = max(100.0, math.ceil(highest * 1.10 / 50.0) * 50.0)

    image_paths = []
    target_rows = []
    for number, (row, primary, interactions) in enumerate(prepared, 1):
        path = Path(row["file"])
        frequency, amplitude, fs = load_envelope_spectrum(
            path,
            float(row["analysis_start_s"]),
            float(row["analysis_duration_s"]),
            carrier_band[0],
            carrier_band[1],
        )
        image_path = output_dir / "figures" / "envelope_fft_ch0" / "individual" / canonical_image_name(row)
        plot_one(frequency, amplitude, primary, interactions, row, image_path, carrier_band, x_max_hz)
        image_paths.append(image_path)
        for target in primary:
            target_rows.append({**{key: row[key] for key in ("file", "bearing", "rpm", "rotor", "fault", "repeat")},
                                "target_type": "primary", **target})
        for target in interactions:
            target_rows.append({**{key: row[key] for key in ("file", "bearing", "rpm", "rotor", "fault", "repeat")},
                                "target_type": "interaction_candidate", "component": "compound", "harmonic": "", **target})
        print(f"그림 생성 {number}/{len(prepared)}: {image_path.name}", flush=True)

    make_contact_sheet(image_paths, output_dir / "figures" / "envelope_fft_ch0" / "contact_sheet.png")
    result_path = output_dir / "results" / "ch0_envelope_reference_frequencies.csv"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["file", "bearing", "rpm", "rotor", "fault", "repeat", "target_type", "label",
                  "frequency_hz", "component", "harmonic", "kind"]
    with result_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(target_rows)
    return target_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-run", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--carrier-low-hz", type=float, default=2000.0)
    parser.add_argument("--carrier-high-hz", type=float, default=7000.0)
    args = parser.parse_args()
    run(args.source_run, args.output_dir, (args.carrier_low_hz, args.carrier_high_hz))


if __name__ == "__main__":
    main()
