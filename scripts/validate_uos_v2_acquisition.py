#!/usr/bin/env python3
"""Run repeatable quality and physics screens on UOS v2 TDMS acquisitions.

This is a screening tool, not an automatic scientific acceptance test.  It
keeps the numerical evidence (frequency error and local prominence) beside
each pass/fail screen so that borderline results can be reviewed manually.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from nptdms import TdmsFile
from scipy import signal, stats

try:
    from scripts.analyze_uos_v2_clipping import _channels, bearing_orders
except ModuleNotFoundError:  # Direct execution from scripts/.
    from analyze_uos_v2_clipping import _channels, bearing_orders


FILE_RE = re.compile(
    r"(?P<rotor>H|L|M[123]|U[123])_"
    r"(?P<fault>H|IR|OR|B|IR\+B|IR\+OR|OR\+B|IR\+OR\+B)_"
    r"(?P<nominal_fs>\d+(?:_\d+)?)_"
    r"(?P<bearing>6204|30204|N204|NJ204)_"
    r"(?P<rpm>\d+)(?:_(?P<repeat>\d+))?\.tdms$"
)

DEFAULT_CARRIER_BANDS_HZ = ((2000.0, 7000.0), (7000.0, 10000.0), (10000.0, 11200.0))
COMPONENT_LABEL = {"IR": "BPFI", "OR": "BPFO", "B": "BSF"}
ROTOR_ORDER = {name: index for index, name in enumerate(("H", "L", "M1", "M2", "M3", "U1", "U2", "U3"))}
KNOWN_STORED_RAILS_G = {
    # Current 13A131/NI-9234 system; established by the 2026-08-01 exhaustive scan.
    0: (-53.129211775684645, 53.14191454931536),
    1: (-50.655637040792065, 50.67458878321781),
    2: (math.nan, 51.62331855642786),
    3: (math.nan, math.nan),
}


@dataclass(frozen=True)
class AcquisitionMeta:
    rotor: str
    fault: str
    nominal_fs: float
    bearing: str
    rpm: int
    repeat: int


def parse_acquisition_filename(path: Path) -> AcquisitionMeta | None:
    """Parse a UOS v2 TDMS name, including optional repeat suffixes."""
    match = FILE_RE.fullmatch(path.name)
    if match is None:
        return None
    fields = match.groupdict()
    return AcquisitionMeta(
        rotor=fields["rotor"],
        fault=fields["fault"],
        nominal_fs=float(fields["nominal_fs"].replace("_", ".")),
        bearing=fields["bearing"],
        rpm=int(fields["rpm"]),
        repeat=int(fields["repeat"] or 1),
    )


def fault_components(label: str) -> set[str]:
    if label == "H":
        return set()
    return set(label.split("+"))


def condition_label(rotor_fault: str, bearing_fault: str) -> str:
    """Return the repository-wide ``{rotor}_{bearing}`` fault label."""
    return f"{rotor_fault}_{bearing_fault}"


def file_sort_key(file_name: str) -> tuple:
    meta = parse_acquisition_filename(Path(file_name))
    if meta is None:
        return (math.inf, math.inf, file_name)
    return (meta.rpm, ROTOR_ORDER.get(meta.rotor, 999), meta.repeat, file_name)


def choose_window(total_samples: int, fs: float, start_s: float, duration_s: float | None) -> tuple[int, int]:
    start = int(round(start_s * fs))
    end = total_samples if duration_s is None else start + int(round(duration_s * fs))
    if start < 0 or end <= start or end > total_samples:
        available = total_samples / fs
        raise ValueError(
            f"invalid analysis window {start_s:g}s + {duration_s}s for {available:.3f}s recording"
        )
    return start, end


def discover_files(
    data_root: Path,
    target_fs: float | None = None,
    bearings: set[str] | None = None,
    rpms: set[int] | None = None,
    rotors: set[str] | None = None,
    faults: set[str] | None = None,
) -> list[tuple[Path, AcquisitionMeta]]:
    candidates = [data_root] if data_root.is_file() else data_root.rglob("*.tdms")
    selected: list[tuple[Path, AcquisitionMeta]] = []
    for path in candidates:
        meta = parse_acquisition_filename(path)
        if meta is None:
            continue
        if target_fs is not None and not math.isclose(meta.nominal_fs, target_fs, abs_tol=0.1):
            continue
        if bearings and meta.bearing not in bearings:
            continue
        if rpms and meta.rpm not in rpms:
            continue
        if rotors and meta.rotor not in rotors:
            continue
        if faults and meta.fault not in faults:
            continue
        selected.append((path, meta))
    return sorted(selected, key=lambda item: (item[1].bearing, item[1].fault, item[1].rotor,
                                               item[1].rpm, item[1].repeat, str(item[0])))


def _write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is not None:
        names = fieldnames
    else:
        names = []
        for row in rows:
            for name in row:
                if name not in names:
                    names.append(name)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=names, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _run_lengths(indices: np.ndarray) -> np.ndarray:
    indices = np.asarray(indices, dtype=np.int64)
    if len(indices) == 0:
        return np.array([], dtype=np.int64)
    starts = np.r_[0, np.flatnonzero(np.diff(indices) > 1) + 1]
    ends = np.r_[starts[1:], len(indices)]
    return ends - starts


def amplitude_and_clipping_metrics(
    values: np.ndarray,
    sensitivity_v_per_g: float,
    input_limit_v: float,
    channel_index: int | None = None,
    rail_fraction: float = 1.02,
    sensor_range_g: float = 50.0,
) -> dict[str, float | int]:
    """Return amplitude metrics and samples at the observed NI-9234 rail.

    Existing UOS v2 files reach a stored plateau near +/-5.10 V although the
    channel range property says +/-5.0 V.  ``rail_fraction=1.02`` therefore
    reproduces the existing audit while adapting to each channel sensitivity.
    """
    x = np.asarray(values, dtype=np.float64)
    centered = x - float(np.mean(x))
    absolute = np.abs(centered)
    over_sensor_range = np.abs(x) > sensor_range_g
    voltage = np.abs(x * sensitivity_v_per_g)
    threshold_v = abs(input_limit_v) * rail_fraction
    near_limit_indices = np.flatnonzero(voltage >= threshold_v)
    if channel_index in KNOWN_STORED_RAILS_G:
        negative, positive = KNOWN_STORED_RAILS_G[channel_index]
        rail_mask = np.zeros(len(x), dtype=bool)
        if math.isfinite(negative):
            rail_mask |= x == negative
        if math.isfinite(positive):
            rail_mask |= x == positive
        rail_indices = np.flatnonzero(rail_mask)
    else:
        # A caller without a channel identity receives the conservative limit
        # screen. Production TDMS calls always supply the channel index.
        rail_indices = near_limit_indices
    lengths = _run_lengths(rail_indices)
    return {
        "samples": len(x),
        "rms_g": float(np.sqrt(np.mean(centered * centered))),
        "peak_abs_g": float(np.max(absolute)),
        "p99_99_abs_g": float(np.quantile(absolute, 0.9999)),
        "over_50g_samples": int(np.count_nonzero(over_sensor_range)),
        "over_50g_ratio_pct": float(np.mean(over_sensor_range) * 100.0),
        "rail_threshold_v": threshold_v,
        "near_input_limit_samples": int(len(near_limit_indices)),
        "near_input_limit_ratio_pct": float(len(near_limit_indices) / len(x) * 100.0),
        "rail_samples": int(len(rail_indices)),
        "rail_ratio_pct": float(len(rail_indices) / len(x) * 100.0),
        "rail_segments": int(len(lengths)),
        "max_rail_run_samples": int(np.max(lengths)) if len(lengths) else 0,
    }


def spectrum_amplitude(values: np.ndarray, fs: float, segment_s: float = 8.0) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(values, dtype=np.float64)
    x = x - float(np.mean(x))
    nperseg = min(len(x), max(256, int(round(segment_s * fs))))
    frequency, psd = signal.welch(
        x,
        fs=fs,
        window="hann",
        nperseg=nperseg,
        noverlap=nperseg // 2,
        detrend="constant",
        scaling="spectrum",
    )
    return frequency, np.sqrt(np.maximum(psd, 0.0))


def target_peak(
    frequency: np.ndarray,
    amplitude: np.ndarray,
    target_hz: float,
) -> dict[str, float]:
    peak_half_width = max(0.5, 0.01 * target_hz)
    background_inner = max(2.0, 0.02 * target_hz)
    background_outer = max(10.0, 0.10 * target_hz)
    peak_mask = np.abs(frequency - target_hz) <= peak_half_width
    background_mask = (
        (np.abs(frequency - target_hz) >= background_inner)
        & (np.abs(frequency - target_hz) <= background_outer)
    )
    if not np.any(peak_mask) or not np.any(background_mask):
        observed, prominence = math.nan, math.nan
    else:
        indices = np.flatnonzero(peak_mask)
        selected = indices[np.argmax(amplitude[indices])]
        observed = float(frequency[selected])
        prominence = float(20 * np.log10(
            max(float(amplitude[selected]), 1e-15)
            / max(float(np.median(amplitude[background_mask])), 1e-15)
        ))
    return {
        "observed_hz": observed,
        "frequency_error_hz": observed - target_hz if math.isfinite(observed) else math.nan,
        "local_prominence_db": prominence,
    }


def estimate_one_x(values: np.ndarray, fs: float, nominal_rpm: float) -> dict[str, float]:
    """Find the strongest raw-spectrum candidate within +/-10% of nominal 1X."""
    frequency, amplitude = spectrum_amplitude(values, fs, segment_s=min(16.0, len(values) / fs))
    nominal_hz = nominal_rpm / 60.0
    search = (frequency >= nominal_hz * 0.90) & (frequency <= nominal_hz * 1.10)
    if not np.any(search):
        return {"observed_hz": math.nan, "frequency_error_hz": math.nan,
                "local_prominence_db": math.nan}
    indices = np.flatnonzero(search)
    peak_index = indices[np.argmax(amplitude[indices])]
    observed_hz = float(frequency[peak_index])
    # Prominence is evaluated around the selected peak, while error remains
    # referenced to the nominal RPM.
    result = target_peak(frequency, amplitude, observed_hz)
    result["observed_hz"] = observed_hz
    result["frequency_error_hz"] = observed_hz - nominal_hz
    return result


def carrier_bands(fs: float) -> list[tuple[float, float]]:
    """Return carrier bands wholly inside the approximate alias-free region."""
    safe_upper = 0.45 * fs
    return [(low, high) for low, high in DEFAULT_CARRIER_BANDS_HZ if high <= safe_upper]


def physical_targets(bearing: str, shaft_hz: float) -> list[dict]:
    orders = bearing_orders(bearing)
    base = {name: orders[name] * shaft_hz for name in ("FTF", "BSF", "BPFO", "BPFI")}
    targets: list[dict] = []
    for component, label in COMPONENT_LABEL.items():
        for harmonic in (1, 2, 3):
            targets.append({
                "component": component,
                "target": f"{label}_{harmonic}x",
                "family": "harmonic",
                "frequency_hz": base[label] * harmonic,
            })
            if component == "IR":
                for sign, text in ((-1, "minus"), (1, "plus")):
                    value = base[label] * harmonic + sign * shaft_hz
                    if value > 0:
                        targets.append({"component": component,
                                        "target": f"{label}_{harmonic}x_{text}_1X",
                                        "family": "shaft_sideband", "frequency_hz": value})
            if component == "B":
                for sign, text in ((-1, "minus"), (1, "plus")):
                    value = base[label] * harmonic + sign * base["FTF"]
                    if value > 0:
                        targets.append({"component": component,
                                        "target": f"{label}_{harmonic}x_{text}_FTF",
                                        "family": "cage_sideband", "frequency_hz": value})
    return targets


def summarize_rms_trends(channel_rows: list[dict]) -> list[dict]:
    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for row in channel_rows:
        key = (row["bearing"], row["fault"], row["rotor"], row["channel"], row["repeat"])
        grouped[key].append(row)
    output: list[dict] = []
    for key, rows in sorted(grouped.items()):
        by_rpm = {}
        for row in rows:
            by_rpm[int(row["rpm"])] = float(row["rms_g"])
        if len(by_rpm) < 2:
            continue
        rpm = np.array(sorted(by_rpm), dtype=float)
        rms = np.array([by_rpm[int(value)] for value in rpm], dtype=float)
        rho, p_value = stats.spearmanr(rpm, rms)
        slope = float(np.polyfit(rpm, rms, 1)[0])
        output.append({
            "bearing": key[0], "fault": key[1], "rotor": key[2],
            "channel": key[3], "repeat": key[4], "rpm_count": len(rpm),
            "rpm_values": ";".join(str(int(value)) for value in rpm),
            "rms_values_g": ";".join(f"{value:.6g}" for value in rms),
            "spearman_rho": float(rho), "spearman_p": float(p_value),
            "linear_slope_g_per_rpm": slope,
            "strictly_increasing": "Yes" if np.all(np.diff(rms) > 0) else "No",
            "highest_to_lowest_rms_ratio": float(rms[-1] / rms[0]),
        })
    return output


def summarize_component_family(
    members: list[dict], component: str, detection_db: float
) -> dict[str, float | int | str]:
    """Select one envelope carrier band and require coherent harmonics.

    Choosing a single maximum from many bands and sidebands creates an overly
    optimistic multiple-comparison screen.  The summary therefore requires at
    least two of the 1x/2x/3x defect harmonics in the same carrier band.  Every
    individual target remains available in the detail CSV.
    """
    envelope = [row for row in members if row["component"] == component
                and row["method"] == "envelope FFT"]
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in envelope:
        grouped[row["carrier_band_hz"]].append(row)
    if not grouped:
        candidates = [row for row in members if row["component"] == component
                      and row["method"] == "raw FFT" and row["family"] == "harmonic"]
        harmonics = candidates
        selected_band = "Not available"
    else:
        def band_score(item: tuple[str, list[dict]]) -> tuple[int, float]:
            harmonics = [row for row in item[1] if row["family"] == "harmonic"]
            count = sum(float(row["local_prominence_db"]) >= detection_db for row in harmonics)
            return count, sum(float(row["local_prominence_db"]) for row in harmonics)

        selected_band, candidates = max(grouped.items(), key=band_score)
        harmonics = [row for row in candidates if row["family"] == "harmonic"]
    harmonic_hits = [row for row in harmonics if float(row["local_prominence_db"]) >= detection_db]
    sideband_hits = [row for row in candidates if row["family"] != "harmonic"
                     and float(row["local_prominence_db"]) >= detection_db]
    best = max(candidates, key=lambda row: float(row["local_prominence_db"]))
    detected = len(harmonic_hits) >= 2
    return {
        "best_method": best["method"], "best_carrier_band_hz": selected_band,
        "best_target": best["target"], "best_expected_hz": best["expected_hz"],
        "best_observed_hz": best["observed_hz"],
        "best_prominence_db": best["local_prominence_db"],
        "harmonic_targets_detected": len(harmonic_hits),
        "supporting_sidebands_detected": len(sideband_hits),
        "screen_detected": "Yes" if detected else "No",
        "screen_rule": "at least 2 of 1x/2x/3x harmonics in one envelope carrier band",
    }


def summarize_fft_component_counts(
    detection_rows: list[dict],
    component_rows: list[dict],
) -> list[dict]:
    """Count direct-FFT and envelope-FFT harmonic support per expected component."""
    expected = [
        row for row in component_rows
        if row["component"] in ("IR", "OR", "B") and row["expected_for_label"] == "Yes"
    ]
    raw_hits: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    for row in detection_rows:
        if (
            row["method"] == "raw FFT"
            and row["component"] in ("IR", "OR", "B")
            and row["family"] == "harmonic"
            and row["expected_for_label"] == "Yes"
            and row["screen_detected"] == "Yes"
        ):
            raw_hits[(row["file"], row["channel"], row["component"])].add(row["target"])

    output = []
    for component in ("IR", "OR", "B"):
        members = [row for row in expected if row["component"] == component]
        if not members:
            continue
        raw_counts = [
            len(raw_hits[(row["file"], row["channel"], component)]) for row in members
        ]
        envelope_counts = [int(row["harmonic_targets_detected"]) for row in members]
        output.append({
            "component": component,
            "raw_fft_at_least_one_harmonic_channels": sum(count >= 1 for count in raw_counts),
            "raw_fft_at_least_two_harmonics_channels": sum(count >= 2 for count in raw_counts),
            "envelope_fft_at_least_one_harmonic_channels": sum(
                count >= 1 for count in envelope_counts
            ),
            "envelope_fft_at_least_two_harmonics_channels": sum(
                count >= 2 for count in envelope_counts
            ),
            "total_channels": len(members),
        })
    return output


def _metadata_dict(path: Path, meta: AcquisitionMeta) -> dict:
    return {
        "file": str(path), "bearing": meta.bearing, "rpm": meta.rpm,
        "rotor": meta.rotor, "fault": meta.fault, "repeat": meta.repeat,
        "condition_label": condition_label(meta.rotor, meta.fault),
        "nominal_sampling_rate_hz": meta.nominal_fs,
    }


def analyse_file(
    path: Path,
    meta: AcquisitionMeta,
    start_s: float,
    duration_s: float | None,
    spectral_duration_s: float,
    detection_db: float,
) -> tuple[list[dict], list[dict], list[dict]]:
    channel_rows: list[dict] = []
    detection_rows: list[dict] = []
    component_rows: list[dict] = []
    spectra: list[tuple[str, float, np.ndarray]] = []
    one_x_rows: list[dict] = []

    with TdmsFile.open(path) as tdms:
        channels = _channels(tdms)
        if len(channels) != 4:
            raise ValueError(f"expected four channels, found {len(channels)}: {path}")
        channel_lengths = [len(channel) for channel in channels]
        if len(set(channel_lengths)) != 1:
            raise ValueError(f"channel sample counts differ: {path}")
        actual_rates = [1.0 / float(channel.properties["wf_increment"]) for channel in channels]
        if max(actual_rates) - min(actual_rates) > 1e-6:
            raise ValueError(f"channel sampling rates differ: {path}")
        start_times = [str(channel.properties.get("wf_start_time", "Unknown")) for channel in channels]
        timebase_status = "Unknown" if "Unknown" in start_times else (
            "Yes" if len(set(start_times)) == 1 else "No"
        )
        fs = actual_rates[0]
        if not math.isclose(fs, meta.nominal_fs, abs_tol=0.1):
            raise ValueError(f"filename rate {meta.nominal_fs:g} differs from TDMS rate {fs:g}: {path}")

        for index, channel in enumerate(channels):
            start, end = choose_window(len(channel), fs, start_s, duration_s)
            values = np.asarray(channel[start:end], dtype=np.float64)
            spectral_count = min(len(values), int(round(spectral_duration_s * fs)))
            spectral_values = values[:spectral_count]
            sensitivity = float(channel.properties.get("NI_SensorSensitivity", math.nan))
            high_range = float(channel.properties.get("DAC~Channel~HighRange", 5.0))
            if not math.isfinite(sensitivity) or sensitivity <= 0:
                raise ValueError(f"missing valid NI_SensorSensitivity in {path}, {channel.name}")
            metrics = amplitude_and_clipping_metrics(values, sensitivity, high_range, index)
            one_x = estimate_one_x(spectral_values, fs, meta.rpm)
            row = {
                **_metadata_dict(path, meta), "channel": f"CH{index}",
                "actual_sampling_rate_hz": fs, "source_samples": len(channel),
                "source_duration_s": len(channel) / fs, "analysis_start_s": start / fs,
                "analysis_duration_s": len(values) / fs,
                "spectral_duration_s": len(spectral_values) / fs,
                "four_channel_sample_count_match": "Yes",
                "four_channel_start_time_match": timebase_status,
                "sensitivity_v_per_g": sensitivity, "input_limit_v": high_range,
                **metrics,
                "nominal_one_x_hz": meta.rpm / 60.0,
                "observed_one_x_hz": one_x["observed_hz"],
                "one_x_error_hz": one_x["frequency_error_hz"],
                "one_x_prominence_db": one_x["local_prominence_db"],
                "one_x_screen_detected": "Yes" if one_x["local_prominence_db"] >= detection_db else "No",
            }
            channel_rows.append(row)
            one_x_rows.append(one_x)
            spectra.append((f"CH{index}", fs, spectral_values))

    usable_one_x = [row["observed_hz"] for row in one_x_rows
                    if math.isfinite(row["observed_hz"]) and row["local_prominence_db"] >= detection_db]
    shaft_hz = float(np.median(usable_one_x)) if usable_one_x else meta.rpm / 60.0
    shaft_source = "four-channel median" if usable_one_x else "nominal RPM fallback"
    targets = physical_targets(meta.bearing, shaft_hz)
    expected_components = fault_components(meta.fault)

    for channel_name, fs, values in spectra:
        raw_frequency, raw_amplitude = spectrum_amplitude(values, fs)
        one_x_target = target_peak(raw_frequency, raw_amplitude, shaft_hz)
        detection_rows.append({
            **_metadata_dict(path, meta), "channel": channel_name, "method": "raw FFT",
            "carrier_band_hz": "Not applicable", "component": "ROT", "target": "1X",
            "family": "rotation", "expected_for_label": "Yes", "shaft_frequency_source": shaft_source,
            "expected_hz": shaft_hz, **one_x_target,
            "screen_detected": "Yes" if one_x_target["local_prominence_db"] >= detection_db else "No",
            "detection_threshold_db": detection_db,
        })
        # Direct FFT is retained for audit, but envelope FFT is the primary
        # bearing-impact screen because the defect rate commonly modulates a
        # higher-frequency structural resonance.
        for target in targets:
            if target["family"] != "harmonic":
                continue
            result = target_peak(raw_frequency, raw_amplitude, target["frequency_hz"])
            target_fields = {name: value for name, value in target.items() if name != "frequency_hz"}
            detection_rows.append({
                **_metadata_dict(path, meta), "channel": channel_name, "method": "raw FFT",
                "carrier_band_hz": "Not applicable", **target_fields,
                "expected_for_label": "Yes" if target["component"] in expected_components else "No",
                "shaft_frequency_source": shaft_source, "expected_hz": target["frequency_hz"], **result,
                "screen_detected": "Yes" if result["local_prominence_db"] >= detection_db else "No",
                "detection_threshold_db": detection_db,
            })

        for low, high in carrier_bands(fs):
            sos = signal.butter(4, (low, high), btype="bandpass", fs=fs, output="sos")
            filtered = signal.sosfiltfilt(sos, values)
            envelope = np.abs(signal.hilbert(filtered))
            env_frequency, env_amplitude = spectrum_amplitude(envelope, fs)
            for target in targets:
                result = target_peak(env_frequency, env_amplitude, target["frequency_hz"])
                target_fields = {name: value for name, value in target.items() if name != "frequency_hz"}
                detection_rows.append({
                    **_metadata_dict(path, meta), "channel": channel_name, "method": "envelope FFT",
                    "carrier_band_hz": f"{low:g}-{high:g}", **target_fields,
                    "expected_for_label": "Yes" if target["component"] in expected_components else "No",
                    "shaft_frequency_source": shaft_source, "expected_hz": target["frequency_hz"], **result,
                    "screen_detected": "Yes" if result["local_prominence_db"] >= detection_db else "No",
                    "detection_threshold_db": detection_db,
                })

    for channel_name in ("CH0", "CH1", "CH2", "CH3"):
        members = [row for row in detection_rows if row["channel"] == channel_name]
        rotation = next(row for row in members if row["component"] == "ROT")
        component_rows.append({
            **_metadata_dict(path, meta), "channel": channel_name, "component": "ROT",
            "expected_for_label": "Yes", "best_method": rotation["method"],
            "best_carrier_band_hz": rotation["carrier_band_hz"], "best_target": "1X",
            "best_expected_hz": rotation["expected_hz"], "best_observed_hz": rotation["observed_hz"],
            "best_prominence_db": rotation["local_prominence_db"],
            "harmonic_targets_detected": 1 if rotation["screen_detected"] == "Yes" else 0,
            "supporting_sidebands_detected": 0,
            "screen_detected": rotation["screen_detected"],
            "screen_rule": "1X local prominence threshold",
        })
        for component in ("IR", "OR", "B"):
            summary = summarize_component_family(members, component, detection_db)
            component_rows.append({
                **_metadata_dict(path, meta), "channel": channel_name, "component": component,
                "expected_for_label": "Yes" if component in expected_components else "No",
                **summary,
            })
    return channel_rows, detection_rows, component_rows


def plot_clipping(channel_rows: list[dict], path: Path) -> None:
    files = []
    for row in channel_rows:
        if row["file"] not in files:
            files.append(row["file"])
    files.sort(key=file_sort_key)
    channels = ("CH0", "CH1", "CH2", "CH3")
    lookup = {(row["file"], row["channel"]): row for row in channel_rows}
    values = np.array([
        [float(lookup[(file_name, channel)]["rail_ratio_pct"]) for file_name in files]
        for channel in channels
    ])
    counts = np.array([
        [int(lookup[(file_name, channel)]["rail_samples"]) for file_name in files]
        for channel in channels
    ])
    labels = []
    for file_name in files:
        meta = parse_acquisition_filename(Path(file_name))
        labels.append(f"{meta.rpm} {condition_label(meta.rotor, meta.fault)}")
    fig, ax = plt.subplots(figsize=(max(12, len(files) * 0.34), 4.8))
    image = ax.imshow(values, aspect="auto", cmap="Reds")
    ax.set_yticks(np.arange(len(channels)), channels)
    ax.set_xticks(np.arange(len(labels)), labels, rotation=90, fontsize=6)
    for row_index in range(values.shape[0]):
        for column_index in range(values.shape[1]):
            if counts[row_index, column_index]:
                ax.text(column_index, row_index, str(counts[row_index, column_index]),
                        ha="center", va="center", fontsize=6)
    ax.set_title("Stored rail samples by condition and channel (number: rail samples)")
    fig.colorbar(image, ax=ax, label="Rail samples / analysed samples (%)")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_rms(channel_rows: list[dict], path: Path) -> None:
    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for row in channel_rows:
        grouped[(row["bearing"], row["fault"], row["rotor"], row["repeat"])].append(row)
    usable = {key: rows for key, rows in grouped.items() if len({row["rpm"] for row in rows}) >= 2}
    if not usable:
        return
    panels = sorted(usable.items(), key=lambda item: (
        item[0][0], item[0][1], ROTOR_ORDER.get(item[0][2], 999), item[0][3]
    ))
    columns = min(2, len(panels))
    rows_count = math.ceil(len(panels) / columns)
    fig, axes = plt.subplots(rows_count, columns, figsize=(12, 3.4 * rows_count), squeeze=False,
                             sharex=True)
    for ax, (key, members) in zip(axes.flat, panels):
        for channel in ("CH0", "CH1", "CH2", "CH3"):
            selected = sorted((row for row in members if row["channel"] == channel),
                              key=lambda row: int(row["rpm"]))
            ax.plot([int(row["rpm"]) for row in selected],
                    [float(row["rms_g"]) for row in selected], marker="o", linewidth=1.4,
                    label=channel)
        ax.set_title(f"{key[0]} {condition_label(key[2], key[1])} R{key[3]}")
        ax.set_xlabel("Nominal RPM")
        ax.set_ylabel("RMS acceleration (g)")
        ax.grid(alpha=0.25)
        ax.legend(fontsize=7, ncol=4)
    for ax in axes.flat[len(panels):]:
        ax.set_visible(False)
    fig.suptitle("RMS comparison across matched RPM conditions", y=1.0)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_detection(component_rows: list[dict], path: Path) -> None:
    expected = [row for row in component_rows if row["expected_for_label"] == "Yes"]
    if not expected:
        return
    columns = []
    for row in component_rows:
        if row["file"] not in columns:
            columns.append(row["file"])
    columns.sort(key=file_sort_key)
    components = ("ROT", "IR", "OR", "B")
    matrix = np.full((len(components), len(columns)), np.nan)
    lookup: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in expected:
        lookup[(row["file"], row["component"])].append(row)
    for column, file_name in enumerate(columns):
        for line, component in enumerate(components):
            rows = lookup.get((file_name, component), [])
            if not rows:
                continue
            matrix[line, column] = sum(row["screen_detected"] == "Yes" for row in rows)
    labels = []
    for file_name in columns:
        meta = parse_acquisition_filename(Path(file_name))
        labels.append(f"{meta.rpm} {condition_label(meta.rotor, meta.fault)}")
    masked = np.ma.masked_invalid(matrix)
    fig, ax = plt.subplots(figsize=(max(12, len(columns) * 0.34), 4.8))
    image = ax.imshow(masked, aspect="auto", cmap="viridis", vmin=0, vmax=4)
    ax.set_yticks(np.arange(len(components)), components)
    ax.set_xticks(np.arange(len(labels)), labels, rotation=90, fontsize=7)
    for line in range(matrix.shape[0]):
        for column in range(matrix.shape[1]):
            if not math.isfinite(matrix[line, column]):
                continue
            ax.text(column, line, f"{int(matrix[line, column])}/4", ha="center", va="center",
                    fontsize=6, color="white" if matrix[line, column] < 2.5 else "black")
    ax.set_title("Channels meeting each expected physical-component screen")
    fig.colorbar(image, ax=ax, label="Channels meeting criterion (0-4)")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_report(
    output_dir: Path,
    channel_rows: list[dict],
    component_rows: list[dict],
    rms_rows: list[dict],
    start_s: float,
    duration_s: float | None,
    spectral_duration_s: float,
    detection_db: float,
) -> None:
    files = sorted({row["file"] for row in channel_rows}, key=file_sort_key)
    total_samples = sum(int(row["samples"]) for row in channel_rows)
    rail_samples = sum(int(row["rail_samples"]) for row in channel_rows)
    near_limit_samples = sum(int(row["near_input_limit_samples"]) for row in channel_rows)
    over_50g_samples = sum(int(row.get("over_50g_samples", 0)) for row in channel_rows)
    rail_channels = sum(int(row["rail_samples"]) > 0 for row in channel_rows)
    one_x = [row for row in component_rows if row["component"] == "ROT"]
    expected_faults = [row for row in component_rows
                       if row["component"] in ("IR", "OR", "B") and row["expected_for_label"] == "Yes"]
    monotonic = sum(row["strictly_increasing"] == "Yes" for row in rms_rows)
    channels_by_file: dict[str, list[dict]] = defaultdict(list)
    components_by_file: dict[str, list[dict]] = defaultdict(list)
    for row in channel_rows:
        channels_by_file[row["file"]].append(row)
    for row in component_rows:
        components_by_file[row["file"]].append(row)

    file_windows = {
        row["file"]: (float(row["analysis_start_s"]), float(row["analysis_duration_s"]))
        for row in channel_rows if row["channel"] == "CH0"
    }
    window_counts = Counter(file_windows.values())
    if len(window_counts) == 1:
        (actual_start, actual_duration), _ = next(iter(window_counts.items()))
        analysis_window_text = (
            f"원파일 {actual_start:g}~{actual_start + actual_duration:g}초 "
            f"({actual_duration:g}초)"
        )
    else:
        parts = [
            f"{count}파일은 {actual_start:g}~{actual_start + actual_duration:g}초"
            for (actual_start, actual_duration), count in sorted(window_counts.items())
        ]
        analysis_window_text = "파일별 적용 구간 상이함: " + ", ".join(parts)

    lines = [
        "# UOS v2 수집 데이터 자동 검증 결과",
        "",
        "## 분석 설정",
        "",
        f"- 입력 TDMS: {len(files)}개",
        f"- 분석 채널: {len(channel_rows)}개",
        f"- 진폭·clipping 분석 구간: {analysis_window_text}",
        f"- 주파수 분석 길이: 각 분석 구간 앞 {spectral_duration_s:g}초",
        f"- 자동 peak 선별 기준: 예상 주파수 주변 잡음 중앙값보다 {detection_db:g} dB 이상",
        "- 결함주파수 계산 근거: UOS v1 원 논문 Table 2의 베어링 형상과 표준 결함주파수 식 [UOSV1-S01, p. 6, Table 2]",
        "",
        "## 핵심 결과",
        "",
        f"- Rail 표본: {rail_samples:,}/{total_samples:,}개 ({rail_samples / total_samples * 100:.9f}%)",
        f"- ±50 g 초과 표본: {over_50g_samples:,}/{total_samples:,}개 "
        f"({over_50g_samples / total_samples * 100:.9f}%)",
        f"- 약 ±5.10 V 입력 한계 접근 표본: {near_limit_samples:,}/{total_samples:,}개 ({near_limit_samples / total_samples * 100:.9f}%)",
        f"- Rail 발생 채널: {rail_channels}/{len(channel_rows)}개",
        f"- 4채널 sample 수 일치: {sum(rows[0]['four_channel_sample_count_match'] == 'Yes' for rows in channels_by_file.values())}/{len(files)}파일",
        f"- 4채널 TDMS 시작시각 일치: {sum(rows[0]['four_channel_start_time_match'] == 'Yes' for rows in channels_by_file.values())}/{len(files)}파일",
        f"- 1X 자동 검출: {sum(row['screen_detected'] == 'Yes' for row in one_x)}/{len(one_x)}채널",
        f"- 레이블상 기대되는 IR·OR·B 고조파 계열 자동 검출: "
        f"{sum(row['screen_detected'] == 'Yes' for row in expected_faults)}/{len(expected_faults)}채널·성분",
    ]
    if rms_rows:
        lines.append(f"- 같은 베어링·결함·로터·채널에서 RPM 증가에 따라 RMS가 계속 증가한 조합: {monotonic}/{len(rms_rows)}개")
    else:
        lines.append("- 같은 조건의 RPM이 2개 이상인 조합이 없어 RMS–RPM 추세는 이번 입력에서 판정하지 않음")
    lines.extend([
        "",
        "## 파일별 비교",
        "",
        "| 조건 | 분석 표본(4채널) | Rail 표본·비율 | CH0/CH1/CH2/CH3 RMS (g) | 1X 예상/관찰 (Hz) | BPFI/BPFO/BSF 예상 (Hz) | IR | OR | B |",
        "|---|---:|---:|---|---:|---|---:|---:|---:|",
    ])
    for file_name in files:
        rows = sorted(channels_by_file[file_name], key=lambda row: row["channel"])
        comps = components_by_file[file_name]
        total = sum(int(row["samples"]) for row in rows)
        rail = sum(int(row["rail_samples"]) for row in rows)
        rms_text = "/".join(f"{float(row['rms_g']):.3f}" for row in rows)
        one_x_hz = float(np.median([float(row["observed_one_x_hz"]) for row in rows]))
        orders = bearing_orders(str(rows[0]["bearing"]))
        fault_frequency_text = "/".join(
            f"{orders[name] * one_x_hz:.2f}" for name in ("BPFI", "BPFO", "BSF")
        )
        condition = (
            f"{rows[0]['bearing']}·{rows[0]['rpm']} RPM·"
            f"{rows[0]['condition_label']}·R{rows[0]['repeat']}"
        )
        counts = {}
        for component in ("IR", "OR", "B"):
            selected = [row for row in comps if row["component"] == component]
            counts[component] = f"{sum(row['screen_detected'] == 'Yes' for row in selected)}/4"
        lines.append(
            f"| {condition} | {total:,} | {rail:,}·{rail / total * 100:.9f}% | {rms_text} | "
            f"{int(rows[0]['rpm']) / 60:.3f}/{one_x_hz:.3f} | {fault_frequency_text} | "
            f"{counts['IR']} | {counts['OR']} | {counts['B']} |"
        )
    lines.extend([
        "",
        "- IR·OR·B 열의 분모는 4개 채널임",
        "- 성분 검출은 같은 포락선 carrier 대역에서 해당 결함주파수의 1·2·3차 고조파 중 2개 이상이 기준을 넘은 경우로 정함",
        "- 개별 예상·관찰 주파수와 기준 대비 dB 값은 `frequency_detection_detail.csv`에 저장함",
    ])
    lines.extend([
        "",
        "## 판정 시 주의사항",
        "",
        "- RMS는 속도뿐 아니라 결함, 로터 상태, 체결, 부착, 운전 변동의 영향을 받으므로 같은 조건끼리만 비교함",
        "- 원신호 FFT는 회전주파수 1X 확인에 사용함",
        "- 베어링 결함은 충격이 구조 공진을 변조할 수 있으므로 대역통과 후 포락선 FFT를 주 판정 자료로 사용하고 원신호 FFT 결과도 함께 보존함",
        "- 자동 검출은 예상점 주변에 두드러진 peak가 있는지 선별하는 절차이며, 결함 존재를 단독으로 확정하는 통계 검정이 아님",
        "- 복합 결함에서는 성분 간 간섭, 공진대역 차이, 하중 전달경로 때문에 IR·OR·B가 모두 검출되지 않을 수 있음",
        "- Rail 표본이 있으면 해당 구간의 실제 peak 진폭은 복원할 수 없고 FFT·포락선에도 왜곡이 생길 수 있으므로 별도 검토가 필요함",
        "- 입력 한계 접근 표본과 반복 저장 rail 표본은 별도 열로 제공하며, clipping 비율은 더 강한 증거인 반복 저장 rail 표본을 분자로 계산함",
        "",
        "## 결과 파일",
        "",
        "- `results/file_channel_metrics.csv`: 채널별 sample 수, RMS, peak, ±50 g 초과, rail 비율, 1X 결과",
        "- `results/frequency_detection_detail.csv`: 모든 raw/envelope target의 예상·관찰 주파수와 prominence",
        "- `results/component_detection_summary.csv`: 채널별 1X·IR·OR·B 최상 검출 결과",
        "- `results/fft_component_summary.csv`: 원신호 FFT와 포락선 FFT의 구성 결함별 검출 채널 수",
        "- `results/rms_rpm_trend.csv`: 같은 조건에서 RPM별 RMS 변화",
        "- `results/input_manifest.csv`: 실제 분석 파일과 적용 구간",
        "- `figures/`: clipping, RMS–RPM, 결함 성분 요약 그림",
        "",
    ])
    (output_dir / "validation_report_ko.md").write_text("\n".join(lines), encoding="utf-8")


def run_validation(
    files: list[tuple[Path, AcquisitionMeta]],
    output_dir: Path,
    start_s: float,
    duration_s: float | None,
    spectral_duration_s: float,
    detection_db: float,
    start_overrides: dict[Path, float] | None = None,
) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    if not files:
        raise ValueError("no matching TDMS files")
    channel_rows: list[dict] = []
    detection_rows: list[dict] = []
    component_rows: list[dict] = []
    start_overrides = start_overrides or {}
    for number, (path, meta) in enumerate(files, 1):
        file_start_s = start_overrides.get(path, start_s)
        channels, detections, components = analyse_file(
            path, meta, file_start_s, duration_s, spectral_duration_s, detection_db
        )
        channel_rows.extend(channels)
        detection_rows.extend(detections)
        component_rows.extend(components)
        print(f"validated {number}/{len(files)}: {path}", flush=True)

    rms_rows = summarize_rms_trends(channel_rows)
    fft_component_rows = summarize_fft_component_counts(detection_rows, component_rows)
    results = output_dir / "results"
    _write_csv(results / "file_channel_metrics.csv", channel_rows)
    _write_csv(results / "frequency_detection_detail.csv", detection_rows)
    _write_csv(results / "component_detection_summary.csv", component_rows)
    _write_csv(results / "fft_component_summary.csv", fft_component_rows, [
        "component", "raw_fft_at_least_one_harmonic_channels",
        "raw_fft_at_least_two_harmonics_channels",
        "envelope_fft_at_least_one_harmonic_channels",
        "envelope_fft_at_least_two_harmonics_channels", "total_channels",
    ])
    _write_csv(results / "rms_rpm_trend.csv", rms_rows, [
        "bearing", "fault", "rotor", "channel", "repeat", "rpm_count", "rpm_values",
        "rms_values_g", "spearman_rho", "spearman_p", "linear_slope_g_per_rpm",
        "strictly_increasing", "highest_to_lowest_rms_ratio",
    ])
    manifest = [{
        "file": row["file"], "bearing": row["bearing"], "rpm": row["rpm"],
        "rotor": row["rotor"], "fault": row["fault"], "repeat": row["repeat"],
        "condition_label": row["condition_label"],
        "actual_sampling_rate_hz": row["actual_sampling_rate_hz"],
        "analysis_start_s": row["analysis_start_s"], "analysis_duration_s": row["analysis_duration_s"],
        "spectral_duration_s": row["spectral_duration_s"], "samples_per_channel": row["samples"],
    } for row in channel_rows if row["channel"] == "CH0"]
    _write_csv(results / "input_manifest.csv", manifest)
    plot_clipping(channel_rows, output_dir / "figures" / "clipping_ratio_by_channel.png")
    plot_rms(channel_rows, output_dir / "figures" / "rms_by_rpm.png")
    plot_detection(component_rows, output_dir / "figures" / "expected_component_prominence.png")
    write_report(output_dir, channel_rows, component_rows, rms_rows, start_s, duration_s,
                 spectral_duration_s, detection_db)
    return channel_rows, detection_rows, component_rows, rms_rows


def _set(values: list | None) -> set | None:
    return set(values) if values else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--sampling-rate", type=float, default=25_600.0,
                        help="Select the nominal rate encoded in the filename")
    parser.add_argument("--bearing", nargs="+", choices=("6204", "N204", "NJ204", "30204"))
    parser.add_argument("--rpm", nargs="+", type=int)
    parser.add_argument("--rotor", nargs="+", choices=("H", "L", "M1", "M2", "M3", "U1", "U2", "U3"))
    parser.add_argument("--fault", nargs="+", choices=("H", "IR", "OR", "B", "IR+B", "IR+OR", "OR+B", "IR+OR+B"))
    parser.add_argument("--start-seconds", type=float, default=0.0)
    parser.add_argument("--duration-seconds", type=float)
    parser.add_argument("--spectral-duration-seconds", type=float, default=30.0)
    parser.add_argument("--detection-prominence-db", type=float, default=10.0)
    args = parser.parse_args()

    files = discover_files(args.data_root, args.sampling_rate, _set(args.bearing), _set(args.rpm),
                           _set(args.rotor), _set(args.fault))
    run_validation(files, args.output_dir, args.start_seconds, args.duration_seconds,
                   args.spectral_duration_seconds, args.detection_prominence_db)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
