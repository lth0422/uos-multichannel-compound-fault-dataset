#!/usr/bin/env python3
"""Analyze the UOS v2 four-sensor/position crossover pilot.

The pilot is intentionally treated as sequential, single-channel acquisition.
It can screen channel/sensor health and position-dependent observability, but it
cannot establish simultaneous sampling, phase alignment, or coherence.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Iterable, Sequence
from zipfile import ZipFile

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from nptdms import TdmsFile
from scipy import signal, stats
from scipy.io import loadmat


POSITION_ORDER = ["ShaftEndTop", "ShaftEndSide", "MotorEndTop", "MotorEndSide"]
COMMON_ENVELOPE_BAND_HZ = (2_000.0, 7_000.0)
COMMON_COMPARISON_LOW_PASS_HZ = 7_000.0
ANALYSIS_DURATION_SECONDS = 30.0
WELCH_SEGMENT_SECONDS = 4.0
RMS_WINDOW_SECONDS = 5.0


@dataclass(frozen=True)
class BearingGeometry:
    pitch_diameter_mm: float
    rolling_element_diameter_mm: float
    contact_angle_deg: float
    rolling_element_count: int


@dataclass
class Recording:
    source: str
    system: str
    channel: str
    position: str
    signal_g: np.ndarray
    sampling_rate_hz: float
    measurement_range_g: float
    duration_seconds: float
    bearing_fault_metadata: str
    rotor_fault_metadata: str
    metadata_conflict: bool
    bearing_fault_condition_used: str
    metadata_resolution: str
    sensor_sensitivity_v_per_g: float | None = None


GEOMETRY_30204 = BearingGeometry(
    pitch_diameter_mm=35.8,
    rolling_element_diameter_mm=6.20,
    contact_angle_deg=12.6,
    rolling_element_count=15,
)


def bearing_frequency_orders(geometry: BearingGeometry) -> dict[str, float]:
    """Return classical characteristic-frequency orders relative to shaft speed."""

    ratio = (
        geometry.rolling_element_diameter_mm
        / geometry.pitch_diameter_mm
        * math.cos(math.radians(geometry.contact_angle_deg))
    )
    count = geometry.rolling_element_count
    return {
        "shaft": 1.0,
        "FTF": 0.5 * (1.0 - ratio),
        "BPFO": count / 2.0 * (1.0 - ratio),
        "BPFI": count / 2.0 * (1.0 + ratio),
        "BSF": geometry.pitch_diameter_mm
        / (2.0 * geometry.rolling_element_diameter_mm)
        * (1.0 - ratio**2),
    }


def bearing_frequencies_hz(
    geometry: BearingGeometry, rpm: float
) -> dict[str, float]:
    shaft_hz = rpm / 60.0
    return {
        name: order * shaft_hz
        for name, order in bearing_frequency_orders(geometry).items()
    }


def _first_tdms_channel(tdms: TdmsFile):
    channels = [channel for group in tdms.groups() for channel in group.channels()]
    if len(channels) != 1:
        raise ValueError(f"Expected one TDMS signal channel, found {len(channels)}")
    return channels[0]


def load_tdms_zip(zip_path: Path, expected_fault: str = "IR") -> list[Recording]:
    recordings: list[Recording] = []
    with ZipFile(zip_path) as archive:
        members = sorted(
            (item for item in archive.infolist() if item.filename.endswith(".tdms")),
            key=lambda item: item.filename,
        )
        for member in members:
            tdms = TdmsFile.read(BytesIO(archive.read(member)))
            channel_obj = _first_tdms_channel(tdms)
            values = np.asarray(channel_obj[:], dtype=np.float64)
            sampling_rate = 1.0 / float(channel_obj.properties["wf_increment"])
            channel_match = re.search(r"Channel (\d+)", member.filename)
            if channel_match is None:
                raise ValueError(f"Cannot parse channel from {member.filename}")
            position = Path(member.filename).parent.name
            fault = str(tdms.properties.get("Test_properties~BearingFaultType", "Unknown"))
            rotor = str(tdms.properties.get("Test_properties~RotorFaultType", "Unknown"))
            recordings.append(
                Recording(
                    source=member.filename,
                    system="13A131 + NI-9234",
                    channel=f"CH{channel_match.group(1)}",
                    position=position,
                    signal_g=values,
                    sampling_rate_hz=sampling_rate,
                    measurement_range_g=50.0,
                    duration_seconds=len(values) / sampling_rate,
                    bearing_fault_metadata=fault,
                    rotor_fault_metadata=rotor,
                    metadata_conflict=fault != expected_fault,
                    bearing_fault_condition_used=expected_fault,
                    metadata_resolution=(
                        "User-confirmed raw metadata typo; analyzed as IR"
                        if fault != expected_fault
                        else "Raw metadata matches stated condition"
                    ),
                    sensor_sensitivity_v_per_g=_optional_float(
                        channel_obj.properties.get("NI_SensorSensitivity")
                    ),
                )
            )
    return recordings


def _optional_float(value) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def load_legacy_mat_directory(mat_directory: Path) -> list[Recording]:
    recordings: list[Recording] = []
    for path in sorted(mat_directory.glob("*.mat")):
        contents = loadmat(path)
        if "Data" not in contents:
            raise ValueError(f"MAT file has no Data variable: {path}")
        values = np.asarray(contents["Data"], dtype=np.float64).reshape(-1)
        position = path.name.split("_", 1)[0]
        recordings.append(
            Recording(
                source=str(path),
                system="UOS v1 sensor + 16 kHz acquisition",
                channel="legacy",
                position=position,
                signal_g=values,
                sampling_rate_hz=16_000.0,
                measurement_range_g=20.0,
                duration_seconds=len(values) / 16_000.0,
                bearing_fault_metadata="IR",
                rotor_fault_metadata="H",
                metadata_conflict=False,
                bearing_fault_condition_used="IR",
                metadata_resolution="Filename matches stated condition",
            )
        )
    return recordings


def analysis_segment(recording: Recording) -> np.ndarray:
    sample_count = int(round(ANALYSIS_DURATION_SECONDS * recording.sampling_rate_hz))
    if len(recording.signal_g) <= sample_count:
        return recording.signal_g.copy()
    return recording.signal_g[-sample_count:].copy()


def amplitude_spectrum(values: np.ndarray, sampling_rate_hz: float):
    centered = np.asarray(values, dtype=np.float64) - np.mean(values)
    segment_samples = min(
        len(centered), int(round(WELCH_SEGMENT_SECONDS * sampling_rate_hz))
    )
    frequencies, power = signal.welch(
        centered,
        fs=sampling_rate_hz,
        window="hann",
        nperseg=segment_samples,
        noverlap=segment_samples // 2,
        detrend="constant",
        scaling="spectrum",
    )
    return frequencies, np.sqrt(power)


def envelope_spectrum(
    values: np.ndarray,
    sampling_rate_hz: float,
    requested_band_hz: tuple[float, float] = COMMON_ENVELOPE_BAND_HZ,
):
    upper_limit = 0.45 * sampling_rate_hz
    low = requested_band_hz[0]
    high = min(requested_band_hz[1], upper_limit)
    if high <= low:
        raise ValueError(
            f"Envelope band {requested_band_hz} is invalid for fs={sampling_rate_hz}"
        )
    centered = np.asarray(values, dtype=np.float64) - np.mean(values)
    sos = signal.butter(4, (low, high), btype="bandpass", fs=sampling_rate_hz, output="sos")
    filtered = signal.sosfiltfilt(sos, centered)
    envelope = np.abs(signal.hilbert(filtered))
    return amplitude_spectrum(envelope, sampling_rate_hz), (low, high)


def common_band_signal(
    values: np.ndarray,
    sampling_rate_hz: float,
    cutoff_hz: float = COMMON_COMPARISON_LOW_PASS_HZ,
) -> np.ndarray:
    """Apply the same physical low-pass cutoff before cross-system comparison."""

    if cutoff_hz >= sampling_rate_hz / 2.0:
        raise ValueError(f"cutoff {cutoff_hz} must be below Nyquist for fs={sampling_rate_hz}")
    centered = np.asarray(values, dtype=np.float64) - np.mean(values)
    sos = signal.butter(8, cutoff_hz, btype="lowpass", fs=sampling_rate_hz, output="sos")
    return signal.sosfiltfilt(sos, centered)


def target_peak(
    frequencies: np.ndarray,
    amplitudes: np.ndarray,
    target_hz: float,
    tolerance_hz: float = 1.0,
    background_half_width_hz: float = 8.0,
) -> tuple[float, float, float]:
    target_mask = np.abs(frequencies - target_hz) <= tolerance_hz
    if not np.any(target_mask):
        return math.nan, math.nan, math.nan
    candidate_indices = np.flatnonzero(target_mask)
    peak_index = candidate_indices[np.argmax(amplitudes[target_mask])]
    background_mask = (
        (np.abs(frequencies - target_hz) <= background_half_width_hz)
        & (np.abs(frequencies - target_hz) > max(1.5 * tolerance_hz, 1.0))
    )
    background = np.median(amplitudes[background_mask])
    snr_db = (
        20.0 * math.log10(float(amplitudes[peak_index]) / float(background))
        if background > 0.0
        else math.nan
    )
    return (
        float(frequencies[peak_index]),
        float(amplitudes[peak_index]),
        snr_db,
    )


def windowed_rms(
    values: np.ndarray, sampling_rate_hz: float, window_seconds: float = RMS_WINDOW_SECONDS
) -> tuple[np.ndarray, np.ndarray]:
    window_samples = int(round(window_seconds * sampling_rate_hz))
    starts = np.arange(0, len(values) - window_samples + 1, window_samples)
    rms_values = np.array(
        [np.std(values[start : start + window_samples]) for start in starts],
        dtype=float,
    )
    times = (starts + window_samples / 2.0) / sampling_rate_hz
    return times, rms_values


def analyze_recording(
    recording: Recording, theoretical_frequencies: dict[str, float]
) -> tuple[dict[str, object], dict[str, np.ndarray]]:
    values = analysis_segment(recording)
    half_record_samples = int(round(30.0 * recording.sampling_rate_hz))
    first_30 = recording.signal_g[:half_record_samples]
    first_30_rms = float(np.std(first_30))
    centered = values - np.mean(values)
    rms_g = float(np.sqrt(np.mean(centered**2)))
    common_values = common_band_signal(values, recording.sampling_rate_hz)
    common_rms_g = float(np.sqrt(np.mean(common_values**2)))
    peak_g = float(np.max(np.abs(centered)))
    fft_frequency, fft_amplitude = amplitude_spectrum(values, recording.sampling_rate_hz)
    (envelope_frequency, envelope_amplitude), envelope_band = envelope_spectrum(
        values, recording.sampling_rate_hz
    )
    times, rolling_rms = windowed_rms(
        recording.signal_g, recording.sampling_rate_hz
    )

    low_frequency_mask = (fft_frequency >= 1.0) & (fft_frequency <= 1_000.0)
    low_indices = np.flatnonzero(low_frequency_mask)
    global_index = low_indices[np.argmax(fft_amplitude[low_frequency_mask])]
    result: dict[str, object] = {
        "system": recording.system,
        "channel": recording.channel,
        "position": recording.position,
        "source": recording.source,
        "sampling_rate_hz": recording.sampling_rate_hz,
        "sample_count": len(recording.signal_g),
        "duration_seconds": recording.duration_seconds,
        "analysis_duration_seconds": len(values) / recording.sampling_rate_hz,
        "unit": "g",
        "bearing_fault_metadata": recording.bearing_fault_metadata,
        "bearing_fault_condition_used": recording.bearing_fault_condition_used,
        "rotor_fault_metadata": recording.rotor_fault_metadata,
        "metadata_conflict": "Yes" if recording.metadata_conflict else "No",
        "metadata_resolution": recording.metadata_resolution,
        "sensor_sensitivity_v_per_g": recording.sensor_sensitivity_v_per_g
        if recording.sensor_sensitivity_v_per_g is not None
        else "Unknown",
        "finite_fraction": float(np.mean(np.isfinite(recording.signal_g))),
        "mean_g": float(np.mean(values)),
        "rms_g": rms_g,
        "common_0_7khz_rms_g": common_rms_g,
        "common_0_7khz_rms_retained_percent": common_rms_g / rms_g * 100.0,
        "first_30s_rms_g": first_30_rms,
        "final_30s_rms_g": rms_g,
        "final_vs_first_30s_rms_change_percent": (rms_g / first_30_rms - 1.0)
        * 100.0,
        "peak_abs_g": peak_g,
        "peak_to_peak_g": float(np.ptp(values)),
        "crest_factor": peak_g / rms_g,
        "kurtosis_pearson": float(stats.kurtosis(centered, fisher=False, bias=False)),
        "range_utilization_percent": peak_g / recording.measurement_range_g * 100.0,
        "range_exceedance_fraction": float(
            np.mean(np.abs(recording.signal_g) > recording.measurement_range_g)
        ),
        "rms_5s_mean_g": float(np.mean(rolling_rms)),
        "rms_5s_min_g": float(np.min(rolling_rms)),
        "rms_5s_max_g": float(np.max(rolling_rms)),
        "rms_5s_cv_percent": float(
            np.std(rolling_rms, ddof=1) / np.mean(rolling_rms) * 100.0
        ),
        "fft_global_peak_1_1000_hz": float(fft_frequency[global_index]),
        "fft_global_peak_1_1000_amplitude_g": float(fft_amplitude[global_index]),
        "envelope_band_low_hz": envelope_band[0],
        "envelope_band_high_hz": envelope_band[1],
    }
    for name, target_hz in theoretical_frequencies.items():
        frequency, amplitude, snr = target_peak(fft_frequency, fft_amplitude, target_hz)
        env_frequency, env_amplitude, env_snr = target_peak(
            envelope_frequency, envelope_amplitude, target_hz
        )
        key = name.lower()
        result[f"{key}_expected_hz"] = target_hz
        result[f"{key}_fft_peak_hz"] = frequency
        result[f"{key}_fft_amplitude_g"] = amplitude
        result[f"{key}_fft_local_snr_db"] = snr
        result[f"{key}_envelope_peak_hz"] = env_frequency
        result[f"{key}_envelope_amplitude_g"] = env_amplitude
        result[f"{key}_envelope_local_snr_db"] = env_snr

    second_bpfi = 2.0 * theoretical_frequencies["BPFI"]
    frequency, amplitude, snr = target_peak(
        envelope_frequency, envelope_amplitude, second_bpfi
    )
    result["2bpfi_expected_hz"] = second_bpfi
    result["2bpfi_envelope_peak_hz"] = frequency
    result["2bpfi_envelope_amplitude_g"] = amplitude
    result["2bpfi_envelope_local_snr_db"] = snr
    result["screen_finite"] = "Pass" if result["finite_fraction"] == 1.0 else "Fail"
    result["screen_range"] = (
        "Pass" if result["range_exceedance_fraction"] == 0.0 else "Fail"
    )
    result["screen_shaft_peak"] = (
        "Pass" if result["shaft_fft_local_snr_db"] >= 10.0 else "Review"
    )
    result["screen_bpfi_envelope"] = (
        "Pass" if result["bpfi_envelope_local_snr_db"] >= 6.0 else "Review"
    )

    arrays = {
        "analysis_signal": values,
        "fft_frequency": fft_frequency,
        "fft_amplitude": fft_amplitude,
        "envelope_frequency": envelope_frequency,
        "envelope_amplitude": envelope_amplitude,
        "rms_time": times,
        "rms_values": rolling_rms,
        "common_band_signal": common_values,
    }
    return result, arrays


def _write_csv(path: Path, rows: Sequence[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def summarize_positions(rows: Sequence[dict[str, object]]) -> list[dict[str, object]]:
    summary: list[dict[str, object]] = []
    for position in POSITION_ORDER:
        selected = [
            row
            for row in rows
            if row["system"] == "13A131 + NI-9234" and row["position"] == position
        ]
        if not selected:
            continue
        rms = np.array([float(row["rms_g"]) for row in selected])
        summary.append(
            {
                "position": position,
                "channel_count": len(selected),
                "rms_median_g": float(np.median(rms)),
                "rms_min_g": float(np.min(rms)),
                "rms_max_g": float(np.max(rms)),
                "rms_across_channel_cv_percent": float(
                    np.std(rms, ddof=1) / np.mean(rms) * 100.0
                ),
                "shaft_snr_median_db": float(
                    np.median([float(row["shaft_fft_local_snr_db"]) for row in selected])
                ),
                "bpfi_envelope_snr_median_db": float(
                    np.median(
                        [float(row["bpfi_envelope_local_snr_db"]) for row in selected]
                    )
                ),
                "metadata_conflict_count": sum(
                    row["metadata_conflict"] == "Yes" for row in selected
                ),
            }
        )
    return summary


def summarize_channels(rows: Sequence[dict[str, object]]) -> list[dict[str, object]]:
    new_rows = [row for row in rows if row["system"] == "13A131 + NI-9234"]
    position_medians = {
        position: float(
            np.median(
                [float(row["rms_g"]) for row in new_rows if row["position"] == position]
            )
        )
        for position in POSITION_ORDER
    }
    summary: list[dict[str, object]] = []
    for channel in sorted({str(row["channel"]) for row in new_rows}):
        selected = [row for row in new_rows if row["channel"] == channel]
        normalized_rms = np.array(
            [
                float(row["rms_g"]) / position_medians[str(row["position"])]
                for row in selected
            ]
        )
        summary.append(
            {
                "channel": channel,
                "sensor_sensitivity_v_per_g": selected[0]["sensor_sensitivity_v_per_g"],
                "position_count": len(selected),
                "position_normalized_rms_median": float(np.median(normalized_rms)),
                "position_normalized_rms_min": float(np.min(normalized_rms)),
                "position_normalized_rms_max": float(np.max(normalized_rms)),
                "maximum_absolute_rms_deviation_percent": float(
                    np.max(np.abs(normalized_rms - 1.0)) * 100.0
                ),
                "shaft_screen_pass_count": sum(
                    row["screen_shaft_peak"] == "Pass" for row in selected
                ),
                "bpfi_screen_pass_count": sum(
                    row["screen_bpfi_envelope"] == "Pass" for row in selected
                ),
                "range_screen_pass_count": sum(
                    row["screen_range"] == "Pass" for row in selected
                ),
                "metadata_conflict_count": sum(
                    row["metadata_conflict"] == "Yes" for row in selected
                ),
            }
        )
    return summary


def _pairwise_correlations(vectors: Sequence[np.ndarray]) -> list[float]:
    correlations: list[float] = []
    for left_index in range(len(vectors)):
        for right_index in range(left_index + 1, len(vectors)):
            correlations.append(
                float(np.corrcoef(vectors[left_index], vectors[right_index])[0, 1])
            )
    return correlations


def summarize_spectral_consistency(
    rows: Sequence[dict[str, object]],
    arrays_by_source: dict[str, dict[str, np.ndarray]],
) -> list[dict[str, object]]:
    """Summarize shape consistency; this is not simultaneous coherence."""

    new_rows = [row for row in rows if row["system"] == "13A131 + NI-9234"]
    output: list[dict[str, object]] = []
    bands = [
        ("fft_1_500_hz", "fft_frequency", "fft_amplitude", 1.0, 500.0),
        ("fft_500_7000_hz", "fft_frequency", "fft_amplitude", 500.0, 7_000.0),
        (
            "envelope_1_500_hz",
            "envelope_frequency",
            "envelope_amplitude",
            1.0,
            500.0,
        ),
    ]
    for position in POSITION_ORDER:
        selected = [row for row in new_rows if row["position"] == position]
        for name, frequency_key, amplitude_key, low, high in bands:
            vectors: list[np.ndarray] = []
            for row in selected:
                arrays = arrays_by_source[str(row["source"])]
                frequencies = arrays[frequency_key]
                amplitudes = arrays[amplitude_key]
                mask = (frequencies >= low) & (frequencies <= high)
                # Log amplitude emphasizes spectral shape rather than absolute gain.
                vectors.append(np.log10(np.maximum(amplitudes[mask], 1e-12)))
            correlations = _pairwise_correlations(vectors)
            output.append(
                {
                    "position": position,
                    "spectrum": name,
                    "pair_count": len(correlations),
                    "pairwise_pearson_median": float(np.median(correlations)),
                    "pairwise_pearson_min": float(np.min(correlations)),
                    "pairwise_pearson_max": float(np.max(correlations)),
                    "interpretation_limit": "Sequential shape similarity; not coherence",
                }
            )
    return output


def summarize_system_comparison(
    rows: Sequence[dict[str, object]],
) -> list[dict[str, object]]:
    """Compare systems descriptively; acquisitions were not simultaneous."""

    output: list[dict[str, object]] = []
    for position in POSITION_ORDER:
        new_rows = [
            row
            for row in rows
            if row["system"] == "13A131 + NI-9234" and row["position"] == position
        ]
        legacy_rows = [
            row
            for row in rows
            if row["system"] == "UOS v1 sensor + 16 kHz acquisition"
            and row["position"] == position
        ]
        if not new_rows or len(legacy_rows) != 1:
            continue
        legacy = legacy_rows[0]
        new_rms = float(np.median([float(row["rms_g"]) for row in new_rows]))
        new_peak = float(
            np.median([float(row["peak_abs_g"]) for row in new_rows])
        )
        output.append(
            {
                "position": position,
                "new_rms_median_g": new_rms,
                "legacy_rms_g": float(legacy["rms_g"]),
                "new_to_legacy_rms_ratio": new_rms / float(legacy["rms_g"]),
                "new_peak_median_g": new_peak,
                "legacy_peak_g": float(legacy["peak_abs_g"]),
                "new_to_legacy_peak_ratio": new_peak / float(legacy["peak_abs_g"]),
                "new_shaft_snr_median_db": float(
                    np.median(
                        [float(row["shaft_fft_local_snr_db"]) for row in new_rows]
                    )
                ),
                "legacy_shaft_snr_db": float(legacy["shaft_fft_local_snr_db"]),
                "new_bpfi_envelope_snr_median_db": float(
                    np.median(
                        [
                            float(row["bpfi_envelope_local_snr_db"])
                            for row in new_rows
                        ]
                    )
                ),
                "legacy_bpfi_envelope_snr_db": float(
                    legacy["bpfi_envelope_local_snr_db"]
                ),
                "comparison_limit": "Sequential systems/runs; not calibration equivalence",
            }
        )
    return output


def summarize_common_band_comparison(
    rows: Sequence[dict[str, object]],
) -> list[dict[str, object]]:
    """Compare both acquisition systems after an identical 0-7 kHz filter."""

    output: list[dict[str, object]] = []
    for position in POSITION_ORDER:
        new_rows = [
            row
            for row in rows
            if row["system"] == "13A131 + NI-9234" and row["position"] == position
        ]
        legacy = next(
            row
            for row in rows
            if row["system"] == "UOS v1 sensor + 16 kHz acquisition"
            and row["position"] == position
        )
        new_full = float(np.median([float(row["rms_g"]) for row in new_rows]))
        new_common = float(
            np.median([float(row["common_0_7khz_rms_g"]) for row in new_rows])
        )
        legacy_full = float(legacy["rms_g"])
        legacy_common = float(legacy["common_0_7khz_rms_g"])
        output.append(
            {
                "position": position,
                "new_full_band_rms_median_g": new_full,
                "legacy_full_band_rms_g": legacy_full,
                "full_band_new_to_legacy_ratio": new_full / legacy_full,
                "new_common_0_7khz_rms_median_g": new_common,
                "legacy_common_0_7khz_rms_g": legacy_common,
                "common_0_7khz_new_to_legacy_ratio": new_common / legacy_common,
                "new_common_band_rms_retained_percent": new_common / new_full * 100.0,
                "legacy_common_band_rms_retained_percent": legacy_common
                / legacy_full
                * 100.0,
                "comparison_limit": (
                    "Same digital filter and final 30 s, but different sensors, runs, "
                    "mounting events, and native anti-alias responses"
                ),
            }
        )
    return output


def summarize_target_amplitude_comparison(
    rows: Sequence[dict[str, object]],
) -> list[dict[str, object]]:
    """Compare absolute low-frequency peaks after identical spectral processing."""

    output: list[dict[str, object]] = []
    for position in POSITION_ORDER:
        new_rows = [
            row
            for row in rows
            if row["system"] == "13A131 + NI-9234" and row["position"] == position
        ]
        legacy = next(
            row
            for row in rows
            if row["system"] == "UOS v1 sensor + 16 kHz acquisition"
            and row["position"] == position
        )
        row: dict[str, object] = {"position": position}
        for target in ("shaft", "bpfi"):
            key = f"{target}_fft_amplitude_g"
            new_value = float(np.median([float(item[key]) for item in new_rows]))
            legacy_value = float(legacy[key])
            row[f"new_{target}_fft_amplitude_median_g"] = new_value
            row[f"legacy_{target}_fft_amplitude_g"] = legacy_value
            row[f"new_to_legacy_{target}_fft_amplitude_ratio"] = (
                new_value / legacy_value
            )
        new_envelope = float(
            np.median(
                [float(item["bpfi_envelope_amplitude_g"]) for item in new_rows]
            )
        )
        legacy_envelope = float(legacy["bpfi_envelope_amplitude_g"])
        row["new_bpfi_envelope_amplitude_median_g"] = new_envelope
        row["legacy_bpfi_envelope_amplitude_g"] = legacy_envelope
        row["new_to_legacy_bpfi_envelope_amplitude_ratio"] = (
            new_envelope / legacy_envelope
        )
        row["comparison_limit"] = (
            "Same Welch/envelope processing, but sequential runs and different "
            "sensor/mount/native transfer functions"
        )
        output.append(row)
    return output


def summarize_peak_frequencies(
    rows: Sequence[dict[str, object]],
) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for row in rows:
        if row["system"] != "13A131 + NI-9234":
            continue
        output.append(
            {
                "position": row["position"],
                "channel": row["channel"],
                "shaft_expected_hz": row["shaft_expected_hz"],
                "shaft_fft_peak_hz": row["shaft_fft_peak_hz"],
                "shaft_error_hz": float(row["shaft_fft_peak_hz"])
                - float(row["shaft_expected_hz"]),
                "shaft_fft_local_snr_db": row["shaft_fft_local_snr_db"],
                "bpfi_expected_hz": row["bpfi_expected_hz"],
                "bpfi_envelope_peak_hz": row["bpfi_envelope_peak_hz"],
                "bpfi_error_hz": float(row["bpfi_envelope_peak_hz"])
                - float(row["bpfi_expected_hz"]),
                "bpfi_envelope_local_snr_db": row["bpfi_envelope_local_snr_db"],
            }
        )
    return output


def _normalized_db(amplitude: np.ndarray, mask: np.ndarray) -> np.ndarray:
    reference = np.max(amplitude[mask])
    return 20.0 * np.log10(np.maximum(amplitude / reference, 1e-8))


def plot_rms(rows: Sequence[dict[str, object]], output: Path) -> None:
    figure, axis = plt.subplots(figsize=(10, 5.5))
    x = np.arange(len(POSITION_ORDER))
    for index, channel in enumerate(["CH0", "CH1", "CH2", "CH3"]):
        channel_rows = {row["position"]: row for row in rows if row["channel"] == channel}
        axis.plot(
            x,
            [channel_rows[position]["rms_g"] for position in POSITION_ORDER],
            marker="o",
            label=channel,
        )
    legacy_rows = {
        row["position"]: row
        for row in rows
        if row["system"] == "UOS v1 sensor + 16 kHz acquisition"
    }
    axis.plot(
        x,
        [legacy_rows[position]["rms_g"] for position in POSITION_ORDER],
        marker="s",
        linestyle="--",
        linewidth=2.0,
        color="black",
        label="legacy sensor",
    )
    axis.set_xticks(x)
    axis.set_xticklabels(POSITION_ORDER, rotation=15)
    axis.set_ylabel("RMS acceleration (g), final 30 s")
    axis.set_title("RMS by physical position and sequential sensor/channel")
    axis.grid(alpha=0.25)
    axis.legend(ncol=5, fontsize=8)
    figure.tight_layout()
    figure.savefig(output, dpi=180)
    plt.close(figure)


def plot_snr(rows: Sequence[dict[str, object]], output: Path) -> None:
    new_rows = [row for row in rows if row["system"] == "13A131 + NI-9234"]
    figure, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True)
    x = np.arange(len(POSITION_ORDER))
    for channel in ["CH0", "CH1", "CH2", "CH3"]:
        selected = {row["position"]: row for row in new_rows if row["channel"] == channel}
        axes[0].plot(
            x,
            [selected[position]["shaft_fft_local_snr_db"] for position in POSITION_ORDER],
            marker="o",
            label=channel,
        )
        axes[1].plot(
            x,
            [selected[position]["bpfi_envelope_local_snr_db"] for position in POSITION_ORDER],
            marker="o",
            label=channel,
        )
    axes[0].axhline(10.0, color="gray", linestyle="--", label="screen 10 dB")
    axes[1].axhline(6.0, color="gray", linestyle="--", label="screen 6 dB")
    axes[0].set_title("Shaft-frequency local SNR")
    axes[1].set_title("BPFI envelope local SNR (2-7 kHz band)")
    for axis in axes:
        axis.set_xticks(x)
        axis.set_xticklabels(POSITION_ORDER, rotation=20)
        axis.set_ylabel("Local peak-to-background ratio (dB)")
        axis.grid(alpha=0.25)
        axis.legend(fontsize=8)
    figure.tight_layout()
    figure.savefig(output, dpi=180)
    plt.close(figure)


def plot_spectra(
    rows: Sequence[dict[str, object]],
    arrays_by_source: dict[str, dict[str, np.ndarray]],
    theoretical_frequencies: dict[str, float],
    output: Path,
    envelope: bool,
) -> None:
    figure, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=True, sharey=True)
    for axis, position in zip(axes.flat, POSITION_ORDER):
        for row in rows:
            if row["position"] != position:
                continue
            arrays = arrays_by_source[str(row["source"])]
            frequency_key = "envelope_frequency" if envelope else "fft_frequency"
            amplitude_key = "envelope_amplitude" if envelope else "fft_amplitude"
            frequencies = arrays[frequency_key]
            amplitudes = arrays[amplitude_key]
            mask = (frequencies >= 1.0) & (frequencies <= 500.0)
            label = str(row["channel"])
            linestyle = "--" if row["system"] != "13A131 + NI-9234" else "-"
            color = "black" if label == "legacy" else None
            axis.plot(
                frequencies[mask],
                _normalized_db(amplitudes, mask)[mask],
                linewidth=1.0,
                alpha=0.85,
                linestyle=linestyle,
                color=color,
                label=label,
            )
        axis.axvline(theoretical_frequencies["shaft"], color="tab:green", alpha=0.7)
        axis.axvline(theoretical_frequencies["BPFI"], color="tab:red", alpha=0.7)
        axis.text(theoretical_frequencies["shaft"] + 4, -5, "1x", color="tab:green")
        axis.text(theoretical_frequencies["BPFI"] + 4, -5, "BPFI", color="tab:red")
        axis.set_title(position)
        axis.set_xlim(0, 500)
        axis.set_ylim(-80, 3)
        axis.grid(alpha=0.2)
    axes[0, 0].legend(ncol=5, fontsize=7)
    figure.text(0.5, 0.01, "Frequency (Hz)", ha="center")
    figure.text(0.01, 0.5, "Normalized amplitude (dB)", va="center", rotation=90)
    title = (
        "Envelope spectra from common 2-7 kHz carrier band"
        if envelope
        else "Low-frequency Welch amplitude spectra"
    )
    figure.suptitle(title, y=0.995)
    figure.tight_layout(rect=(0.025, 0.025, 1.0, 0.96))
    figure.savefig(output, dpi=180)
    plt.close(figure)


def plot_rms_timeline(
    rows: Sequence[dict[str, object]],
    arrays_by_source: dict[str, dict[str, np.ndarray]],
    output: Path,
) -> None:
    figure, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=True)
    for axis, position in zip(axes.flat, POSITION_ORDER):
        for row in rows:
            if row["position"] != position or row["system"] != "13A131 + NI-9234":
                continue
            arrays = arrays_by_source[str(row["source"])]
            axis.plot(
                arrays["rms_time"],
                arrays["rms_values"],
                marker="o",
                label=row["channel"],
            )
        axis.axvspan(0, 30, color="gray", alpha=0.08, label="first 30 s")
        axis.set_title(position)
        axis.set_ylabel("5 s RMS (g)")
        axis.grid(alpha=0.25)
    axes[0, 0].legend(fontsize=8)
    figure.text(0.5, 0.01, "Time from record start (s)", ha="center")
    figure.suptitle("Within-record RMS stability (sequential acquisitions)", y=0.995)
    figure.tight_layout(rect=(0.0, 0.025, 1.0, 0.96))
    figure.savefig(output, dpi=180)
    plt.close(figure)


def plot_waveforms(
    rows: Sequence[dict[str, object]],
    arrays_by_source: dict[str, dict[str, np.ndarray]],
    output: Path,
) -> None:
    figure, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=True)
    for axis, position in zip(axes.flat, POSITION_ORDER):
        selected = [
            row
            for row in rows
            if row["position"] == position and row["channel"] in {"CH1", "legacy"}
        ]
        for row in selected:
            values = arrays_by_source[str(row["source"])]["analysis_signal"]
            sampling_rate = float(row["sampling_rate_hz"])
            sample_count = int(0.5 * sampling_rate)
            times = np.arange(sample_count) / sampling_rate
            axis.plot(times, values[:sample_count], linewidth=0.7, label=row["channel"])
        axis.set_title(position)
        axis.set_ylabel("Acceleration (g)")
        axis.grid(alpha=0.2)
    axes[0, 0].legend(fontsize=8)
    figure.text(0.5, 0.01, "Time within final 30 s segment (s)", ha="center")
    figure.suptitle("Representative raw waveforms: CH1 versus legacy sensor", y=0.995)
    figure.tight_layout(rect=(0.0, 0.025, 1.0, 0.96))
    figure.savefig(output, dpi=180)
    plt.close(figure)


def plot_common_band_comparison(
    common_rows: Sequence[dict[str, object]], output: Path
) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    x = np.arange(len(POSITION_ORDER))
    width = 0.18
    values = {str(row["position"]): row for row in common_rows}
    series = [
        ("new full band", "new_full_band_rms_median_g", -1.5 * width, "tab:blue"),
        ("new 0-7 kHz", "new_common_0_7khz_rms_median_g", -0.5 * width, "tab:cyan"),
        ("legacy full band", "legacy_full_band_rms_g", 0.5 * width, "0.25"),
        ("legacy 0-7 kHz", "legacy_common_0_7khz_rms_g", 1.5 * width, "0.65"),
    ]
    for label, key, offset, color in series:
        axes[0].bar(
            x + offset,
            [float(values[position][key]) for position in POSITION_ORDER],
            width,
            label=label,
            color=color,
        )
    axes[0].set_ylabel("RMS acceleration (g), final 30 s")
    axes[0].set_title("Absolute RMS before and after common-band filtering")
    axes[0].legend(fontsize=8)
    axes[0].grid(axis="y", alpha=0.25)

    axes[1].plot(
        x,
        [
            float(values[position]["full_band_new_to_legacy_ratio"])
            for position in POSITION_ORDER
        ],
        marker="o",
        linewidth=2,
        label="native/full-band ratio",
    )
    axes[1].plot(
        x,
        [
            float(values[position]["common_0_7khz_new_to_legacy_ratio"])
            for position in POSITION_ORDER
        ],
        marker="s",
        linewidth=2,
        label="common 0-7 kHz ratio",
    )
    axes[1].axhline(1.0, color="black", linestyle="--", linewidth=1)
    axes[1].set_ylabel("New / legacy RMS ratio")
    axes[1].set_title("Effect of matching the comparison bandwidth")
    axes[1].legend(fontsize=8)
    axes[1].grid(alpha=0.25)
    for axis in axes:
        axis.set_xticks(x)
        axis.set_xticklabels(POSITION_ORDER, rotation=20)
    figure.suptitle("Fair RMS comparison with identical 7 kHz low-pass filters", y=0.995)
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.95))
    figure.savefig(output, dpi=180)
    plt.close(figure)


def plot_broadband_spectra(
    rows: Sequence[dict[str, object]],
    arrays_by_source: dict[str, dict[str, np.ndarray]],
    output: Path,
) -> None:
    figure, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=True, sharey=True)
    for axis, position in zip(axes.flat, POSITION_ORDER):
        new_rows = [
            row
            for row in rows
            if row["system"] == "13A131 + NI-9234" and row["position"] == position
        ]
        new_arrays = [arrays_by_source[str(row["source"])] for row in new_rows]
        new_frequency = new_arrays[0]["fft_frequency"]
        new_amplitude = np.median(
            np.vstack([arrays["fft_amplitude"] for arrays in new_arrays]), axis=0
        )
        legacy = next(
            row
            for row in rows
            if row["system"] == "UOS v1 sensor + 16 kHz acquisition"
            and row["position"] == position
        )
        legacy_arrays = arrays_by_source[str(legacy["source"])]
        for frequencies, amplitudes, label, style in [
            (new_frequency, new_amplitude, "new median", "-"),
            (
                legacy_arrays["fft_frequency"],
                legacy_arrays["fft_amplitude"],
                "legacy",
                "--",
            ),
        ]:
            mask = (frequencies >= 1.0) & (frequencies <= 10_000.0)
            db_g = 20.0 * np.log10(np.maximum(amplitudes[mask], 1e-10))
            axis.plot(frequencies[mask], db_g, linestyle=style, linewidth=0.8, label=label)
        axis.axvline(
            COMMON_COMPARISON_LOW_PASS_HZ,
            color="tab:red",
            linestyle=":",
            label="7 kHz common cutoff",
        )
        axis.set_title(position)
        axis.grid(alpha=0.2)
        axis.set_xlim(0, 10_000)
    axes[0, 0].legend(fontsize=8)
    figure.text(0.5, 0.01, "Frequency (Hz)", ha="center")
    figure.text(0.01, 0.5, "Welch amplitude (dB re 1 g)", va="center", rotation=90)
    figure.suptitle("Broadband spectra and the common comparison cutoff", y=0.995)
    figure.tight_layout(rect=(0.025, 0.025, 1.0, 0.96))
    figure.savefig(output, dpi=180)
    plt.close(figure)


def plot_target_amplitude_comparison(
    target_rows: Sequence[dict[str, object]], output: Path
) -> None:
    values = {str(row["position"]): row for row in target_rows}
    figure, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    x = np.arange(len(POSITION_ORDER))
    width = 0.34
    panels = [
        ("shaft", "1x shaft peak amplitude"),
        ("bpfi", "BPFI peak amplitude in direct FFT"),
    ]
    for axis, (target, title) in zip(axes, panels):
        new_values = [
            float(values[position][f"new_{target}_fft_amplitude_median_g"])
            for position in POSITION_ORDER
        ]
        legacy_values = [
            float(values[position][f"legacy_{target}_fft_amplitude_g"])
            for position in POSITION_ORDER
        ]
        axis.bar(x - width / 2, new_values, width, label="new median")
        axis.bar(x + width / 2, legacy_values, width, label="legacy")
        for index, position in enumerate(POSITION_ORDER):
            ratio = float(
                values[position][f"new_to_legacy_{target}_fft_amplitude_ratio"]
            )
            axis.text(
                index,
                max(new_values[index], legacy_values[index]) * 1.04,
                f"{ratio:.2f}x",
                ha="center",
                fontsize=8,
            )
        axis.set_title(title)
        axis.set_ylabel("Welch amplitude (g)")
        axis.set_xticks(x)
        axis.set_xticklabels(POSITION_ORDER, rotation=20)
        axis.grid(axis="y", alpha=0.25)
        axis.legend(fontsize=8)
        axis.margins(y=0.15)
    figure.suptitle("Absolute low-frequency peak comparison", y=0.995)
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.95))
    figure.savefig(output, dpi=180)
    plt.close(figure)


def plot_peak_frequencies(
    peak_rows: Sequence[dict[str, object]], output: Path
) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    x = np.arange(len(POSITION_ORDER), dtype=float)
    offsets = {"CH0": -0.18, "CH1": -0.06, "CH2": 0.06, "CH3": 0.18}
    markers = {"CH0": "o", "CH1": "s", "CH2": "^", "CH3": "D"}
    for channel in ["CH0", "CH1", "CH2", "CH3"]:
        selected = {
            str(row["position"]): row
            for row in peak_rows
            if row["channel"] == channel
        }
        axes[0].scatter(
            x + offsets[channel],
            [float(selected[position]["shaft_fft_peak_hz"]) for position in POSITION_ORDER],
            s=55,
            marker=markers[channel],
            label=channel,
        )
        axes[1].scatter(
            x + offsets[channel],
            [
                float(selected[position]["bpfi_envelope_peak_hz"])
                for position in POSITION_ORDER
            ],
            s=55,
            marker=markers[channel],
            label=channel,
        )
    shaft_expected = float(peak_rows[0]["shaft_expected_hz"])
    bpfi_expected = float(peak_rows[0]["bpfi_expected_hz"])
    axes[0].axhline(shaft_expected, color="black", linestyle="--", label="expected")
    axes[1].axhline(bpfi_expected, color="black", linestyle="--", label="expected")
    axes[0].set_title("Observed 1x shaft-frequency peak")
    axes[1].set_title("Observed BPFI peak in envelope spectrum")
    axes[0].set_ylabel("Peak frequency (Hz)")
    axes[1].set_ylabel("Peak frequency (Hz)")
    axes[0].set_ylim(22.9, 23.55)
    axes[1].set_ylim(204.25, 205.75)
    for axis in axes:
        axis.set_xticks(x)
        axis.set_xticklabels(POSITION_ORDER, rotation=20)
        axis.grid(alpha=0.25)
        axis.legend(fontsize=8, ncol=3)
    figure.suptitle("Per-channel peak frequencies with horizontal offsets", y=0.995)
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.95))
    figure.savefig(output, dpi=180)
    plt.close(figure)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tdms-zip", type=Path, required=True)
    parser.add_argument("--legacy-mat-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--rpm", type=float, default=1400.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    figure_directory = args.output_dir / "figures"
    figure_directory.mkdir(parents=True, exist_ok=True)

    theoretical_frequencies = bearing_frequencies_hz(GEOMETRY_30204, args.rpm)
    recordings = load_tdms_zip(args.tdms_zip) + load_legacy_mat_directory(
        args.legacy_mat_dir
    )
    rows: list[dict[str, object]] = []
    arrays_by_source: dict[str, dict[str, np.ndarray]] = {}
    for recording in recordings:
        row, arrays = analyze_recording(recording, theoretical_frequencies)
        rows.append(row)
        arrays_by_source[recording.source] = arrays

    position_index = {position: index for index, position in enumerate(POSITION_ORDER)}
    rows.sort(
        key=lambda row: (
            row["system"] != "13A131 + NI-9234",
            position_index.get(str(row["position"]), 999),
            str(row["channel"]),
        )
    )
    _write_csv(args.output_dir / "recording_metrics.csv", rows)
    _write_csv(args.output_dir / "position_summary.csv", summarize_positions(rows))
    _write_csv(args.output_dir / "channel_summary.csv", summarize_channels(rows))
    _write_csv(
        args.output_dir / "spectral_consistency_summary.csv",
        summarize_spectral_consistency(rows, arrays_by_source),
    )
    _write_csv(
        args.output_dir / "system_comparison_summary.csv",
        summarize_system_comparison(rows),
    )
    common_band_rows = summarize_common_band_comparison(rows)
    _write_csv(
        args.output_dir / "common_band_comparison.csv",
        common_band_rows,
    )
    target_amplitude_rows = summarize_target_amplitude_comparison(rows)
    _write_csv(
        args.output_dir / "target_amplitude_comparison.csv",
        target_amplitude_rows,
    )
    peak_frequency_rows = summarize_peak_frequencies(rows)
    _write_csv(
        args.output_dir / "peak_frequency_by_channel.csv",
        peak_frequency_rows,
    )
    frequency_rows = [
        {
            "component": name,
            "order_relative_to_shaft": bearing_frequency_orders(GEOMETRY_30204)[name],
            "frequency_hz_at_rpm": frequency,
            "rpm": args.rpm,
        }
        for name, frequency in theoretical_frequencies.items()
    ]
    _write_csv(args.output_dir / "expected_frequencies.csv", frequency_rows)

    plot_rms(rows, figure_directory / "01_rms_by_position_and_channel.png")
    plot_snr(rows, figure_directory / "02_target_peak_snr.png")
    plot_spectra(
        rows,
        arrays_by_source,
        theoretical_frequencies,
        figure_directory / "03_low_frequency_fft.png",
        envelope=False,
    )
    plot_spectra(
        rows,
        arrays_by_source,
        theoretical_frequencies,
        figure_directory / "04_envelope_spectrum.png",
        envelope=True,
    )
    plot_rms_timeline(rows, arrays_by_source, figure_directory / "05_rms_timeline.png")
    plot_waveforms(rows, arrays_by_source, figure_directory / "06_raw_waveform.png")
    plot_common_band_comparison(
        common_band_rows, figure_directory / "07_common_band_rms_comparison.png"
    )
    plot_broadband_spectra(
        rows, arrays_by_source, figure_directory / "08_broadband_spectrum.png"
    )
    plot_target_amplitude_comparison(
        target_amplitude_rows,
        figure_directory / "09_absolute_target_peak_comparison.png",
    )
    plot_peak_frequencies(
        peak_frequency_rows,
        figure_directory / "10_peak_frequency_by_channel.png",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
