from pathlib import Path

import numpy as np
from scipy import signal

from scripts.validate_uos_v2_acquisition import (
    KNOWN_STORED_RAILS_G,
    amplitude_and_clipping_metrics,
    carrier_bands,
    choose_window,
    condition_label,
    estimate_one_x,
    file_sort_key,
    fault_components,
    parse_acquisition_filename,
    physical_targets,
    spectrum_amplitude,
    summarize_component_family,
    summarize_fft_component_counts,
    summarize_rms_trends,
    target_peak,
)


def test_filename_parser_accepts_repeat_suffix():
    meta = parse_acquisition_filename(Path("H_IR+OR_25600_N204_1600_4.tdms"))
    assert meta is not None
    assert meta.fault == "IR+OR"
    assert meta.nominal_fs == 25600
    assert meta.repeat == 4


def test_filename_parser_accepts_fractional_rate():
    meta = parse_acquisition_filename(Path("M3_IR+OR+B_17066_67_N204_1600.tdms"))
    assert meta is not None
    assert np.isclose(meta.nominal_fs, 17066.67)
    assert meta.repeat == 1


def test_explicit_analysis_window_uses_requested_samples():
    assert choose_window(5_204_480, 25_600.0, 60.0, 120.0) == (1_536_000, 4_608_000)


def test_clipping_ratio_uses_all_analysed_samples_as_denominator():
    negative, positive = KNOWN_STORED_RAILS_G[0]
    values = np.array([0.0, 10.0, positive, negative, 1.0])
    metrics = amplitude_and_clipping_metrics(values, sensitivity_v_per_g=0.1,
                                             input_limit_v=5.0, channel_index=0)
    assert metrics["rail_samples"] == 2
    assert metrics["near_input_limit_samples"] == 2
    assert np.isclose(metrics["rail_ratio_pct"], 40.0)
    assert metrics["rail_segments"] == 1
    assert metrics["max_rail_run_samples"] == 2


def test_sensor_range_screen_counts_only_values_outside_plus_minus_50g():
    values = np.array([-50.1, -50.0, 0.0, 50.0, 50.1])
    metrics = amplitude_and_clipping_metrics(
        values, sensitivity_v_per_g=0.1, input_limit_v=5.0
    )
    assert metrics["over_50g_samples"] == 2
    assert np.isclose(metrics["over_50g_ratio_pct"], 40.0)


def test_one_x_screen_finds_synthetic_rotation():
    fs = 25_600.0
    time = np.arange(int(4 * fs)) / fs
    values = np.sin(2 * np.pi * 20.0 * time) + 0.01 * np.sin(2 * np.pi * 75 * time)
    result = estimate_one_x(values, fs, nominal_rpm=1200)
    assert abs(result["observed_hz"] - 20.0) < 0.2
    assert result["local_prominence_db"] > 10


def test_envelope_spectrum_finds_amplitude_modulation_rate():
    fs = 25_600.0
    time = np.arange(int(4 * fs)) / fs
    modulation_hz = 120.0
    values = (1.0 + 0.5 * np.sin(2 * np.pi * modulation_hz * time)) * np.sin(
        2 * np.pi * 3500.0 * time
    )
    frequency, amplitude = spectrum_amplitude(np.abs(signal.hilbert(values)), fs)
    result = target_peak(frequency, amplitude, modulation_hz)
    assert abs(result["observed_hz"] - modulation_hz) < 0.2
    assert result["local_prominence_db"] > 10


def test_fault_components_treats_healthy_as_no_bearing_fault():
    assert fault_components("H") == set()
    assert fault_components("IR+OR+B") == {"IR", "OR", "B"}


def test_condition_label_places_rotor_before_bearing_fault():
    assert condition_label("M2", "IR+OR") == "M2_IR+OR"
    assert condition_label("H", "H") == "H_H"


def test_file_sort_key_uses_numeric_rpm_then_rotor_order():
    names = [
        "U1_B_25600_N204_600.tdms",
        "H_B_25600_N204_1000.tdms",
        "H_B_25600_N204_600.tdms",
    ]
    assert sorted(names, key=file_sort_key) == [
        "H_B_25600_N204_600.tdms",
        "U1_B_25600_N204_600.tdms",
        "H_B_25600_N204_1000.tdms",
    ]


def test_run_validation_supports_per_file_start_override(monkeypatch, tmp_path):
    from scripts import validate_uos_v2_acquisition as module

    files = [
        (Path("H_B_25600_N204_600.tdms"), parse_acquisition_filename(Path("H_B_25600_N204_600.tdms"))),
        (Path("H_B_25600_N204_800.tdms"), parse_acquisition_filename(Path("H_B_25600_N204_800.tdms"))),
    ]
    starts = []

    def fake_analyse(path, meta, start_s, duration_s, spectral_s, detection_db):
        starts.append((path.name, start_s))
        base = {
            "file": str(path), "bearing": meta.bearing, "rpm": meta.rpm,
            "rotor": meta.rotor, "fault": meta.fault, "repeat": meta.repeat,
            "condition_label": condition_label(meta.rotor, meta.fault), "channel": "CH0",
            "actual_sampling_rate_hz": 25600.0, "analysis_start_s": start_s,
            "analysis_duration_s": duration_s, "spectral_duration_s": spectral_s,
            "samples": int(25600 * duration_s), "rail_samples": 0,
            "near_input_limit_samples": 0, "rms_g": 1.0,
        }
        return [base], [], []

    monkeypatch.setattr(module, "analyse_file", fake_analyse)
    monkeypatch.setattr(module, "summarize_rms_trends", lambda rows: [])
    monkeypatch.setattr(module, "_write_csv", lambda *args, **kwargs: None)
    monkeypatch.setattr(module, "plot_clipping", lambda *args, **kwargs: None)
    monkeypatch.setattr(module, "plot_rms", lambda *args, **kwargs: None)
    monkeypatch.setattr(module, "plot_detection", lambda *args, **kwargs: None)
    monkeypatch.setattr(module, "write_report", lambda *args, **kwargs: None)

    module.run_validation(
        files, tmp_path, 60.0, 120.0, 120.0, 10.0,
        start_overrides={files[1][0]: 300.0},
    )
    assert starts == [
        ("H_B_25600_N204_600.tdms", 60.0),
        ("H_B_25600_N204_800.tdms", 300.0),
    ]


def test_physical_targets_include_harmonics_and_supported_sidebands():
    targets = {row["target"] for row in physical_targets("6204", 20.0)}
    assert "BPFO_1x" in targets
    assert "BPFI_2x_plus_1X" in targets
    assert "BSF_3x_minus_FTF" in targets
    assert "BPFO_1x_plus_1X" not in targets


def test_carrier_bands_respect_alias_free_limit():
    assert carrier_bands(25_600.0) == [(2000.0, 7000.0), (7000.0, 10000.0), (10000.0, 11200.0)]
    assert carrier_bands(10_240.0) == []


def test_rms_trend_requires_matched_condition_and_reports_monotonicity():
    rows = []
    for rpm, rms in ((1000, 1.0), (1200, 1.2), (1400, 1.4)):
        rows.append({"bearing": "6204", "fault": "IR", "rotor": "H",
                     "channel": "CH0", "repeat": 1, "rpm": rpm, "rms_g": rms})
    result = summarize_rms_trends(rows)
    assert len(result) == 1
    assert result[0]["strictly_increasing"] == "Yes"
    assert np.isclose(result[0]["highest_to_lowest_rms_ratio"], 1.4)


def test_component_summary_requires_two_harmonics_in_same_envelope_band():
    rows = []
    for band, values in (("2000-7000", (12.0, 11.0, 3.0)),
                         ("7000-10000", (20.0, 2.0, 2.0))):
        for harmonic, value in enumerate(values, 1):
            rows.append({"component": "IR", "method": "envelope FFT",
                         "carrier_band_hz": band, "family": "harmonic",
                         "target": f"BPFI_{harmonic}x", "expected_hz": harmonic * 100.0,
                         "observed_hz": harmonic * 100.0, "local_prominence_db": value})
    result = summarize_component_family(rows, "IR", detection_db=10.0)
    assert result["best_carrier_band_hz"] == "2000-7000"
    assert result["harmonic_targets_detected"] == 2
    assert result["screen_detected"] == "Yes"


def test_fft_component_summary_separates_raw_and_envelope_support():
    detection_rows = [
        {
            "file": "sample.tdms", "channel": "CH0", "component": "B",
            "method": "raw FFT", "family": "harmonic", "target": "BSF_1x",
            "expected_for_label": "Yes", "screen_detected": "Yes",
        },
        {
            "file": "sample.tdms", "channel": "CH0", "component": "B",
            "method": "raw FFT", "family": "harmonic", "target": "BSF_2x",
            "expected_for_label": "Yes", "screen_detected": "No",
        },
    ]
    component_rows = [{
        "file": "sample.tdms", "channel": "CH0", "component": "B",
        "expected_for_label": "Yes", "harmonic_targets_detected": 2,
    }]
    result = summarize_fft_component_counts(detection_rows, component_rows)
    assert result == [{
        "component": "B",
        "raw_fft_at_least_one_harmonic_channels": 1,
        "raw_fft_at_least_two_harmonics_channels": 0,
        "envelope_fft_at_least_one_harmonic_channels": 1,
        "envelope_fft_at_least_two_harmonics_channels": 1,
        "total_channels": 1,
    }]
