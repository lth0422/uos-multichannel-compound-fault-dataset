import csv
from pathlib import Path

import numpy as np

from scripts.analyze_uos_v2_clipping import (
    _max_run,
    _zero_shift_screen,
    bearing_frequencies,
    bearing_orders,
    parse_filename,
)
from scripts.analyze_uos_v2_clipping_extended import (
    collapse_events,
    consensus_one_x,
    estimate_one_x,
    local_envelope_prominence,
    phase_concentration,
)
from scripts.plot_uos_v2_clipping_extended import relevant_target
from scripts.analyze_uos_v2_compound_features import (
    component_expected,
    compound_targets,
    fault_tokens,
)
from scripts.plot_uos_v2_task_b_lpf import combine_task_b_c, interpret_row
from scripts.analyze_uos_v2_multifilter_bands import (
    BANDS,
    FILTERS,
    _histogram_counts,
    acceleration_distribution,
    centered_excerpt,
    design_sos,
    summarize_cutoff_scenarios,
)
from scripts.plot_uos_v2_multifilter_bands import (
    BANDS as PLOT_BANDS,
    FILTERS as PLOT_FILTERS,
    _channel_median_matrix,
    _matrix,
)
from scripts.uos_v2_measurement_window import measurement_window
from scripts.analyze_uos_v2_sampling_rate_clipping import (
    _rate_label,
    distribution_metrics as sampling_rate_distribution_metrics,
    sampling_rate_measurement_window,
)


def test_parse_filename_handles_compound_fault():
    result = parse_filename(Path("M3_IR+OR+B_25600_30204_1600.tdms"))
    assert result == {"rotor": "M3", "fault": "IR+OR+B", "fs": "25600", "bearing": "30204", "rpm": "1600"}


def test_parse_filename_handles_fractional_native_rate():
    result = parse_filename(Path("M3_IR+OR+B_17066_67_N204_1600.tdms"))
    assert result["fs"] == "17066.67"
    assert result["bearing"] == "N204"


def test_max_run_counts_sparse_and_consecutive_events():
    events, maximum, mean = _max_run(np.array([1, 3, 4, 10]))
    assert events == 3
    assert maximum == 2
    assert np.isclose(mean, 4 / 3)


def test_zero_shift_screen_flags_persistent_step():
    status, _ = _zero_shift_screen(np.array([0.0, 0.01, 0.0, 0.3, 0.31, 0.29, 0.3]))
    assert status == "suspect"


def test_zero_shift_screen_accepts_stationary_mean():
    status, _ = _zero_shift_screen(np.array([0.0, 0.01, -0.01, 0.02, 0.0, -0.01]))
    assert status == "pass"


def test_uos_table_2_bearing_orders():
    assert np.isclose(bearing_orders("6204")["BPFI"], 4.918716, atol=1e-6)
    assert np.isclose(bearing_orders("N204")["BPFO"], 4.286765, atol=1e-6)
    assert np.isclose(bearing_frequencies("30204", 1400)["BPFI"], 204.577366, atol=1e-6)


def test_collapse_events_keeps_one_index_per_run():
    assert np.array_equal(collapse_events(np.array([2, 3, 8, 10, 11, 12])), np.array([2, 8, 10]))


def test_one_x_estimator_finds_known_rotation():
    fs = 25600.0
    time = np.arange(int(4 * fs)) / fs
    values = np.sin(2 * np.pi * 23.5 * time) + 0.05 * np.sin(2 * np.pi * 80 * time)
    result = estimate_one_x(values, fs, 1400)
    assert abs(result["candidate_hz"] - 23.5) < 0.2
    assert result["local_ratio_db"] > 10


def test_consensus_marks_consistent_candidates_high():
    estimates = [
        {"candidate_hz": hz, "candidate_rpm": hz * 60, "local_ratio_db": 20.0}
        for hz in (23.40, 23.42, 23.38, 23.41)
    ]
    assert consensus_one_x(estimates)["confidence"] == "High"


def test_phase_concentration_detects_periodic_events():
    fs = 1000.0
    events = np.arange(0, 10000, 100)
    r, p = phase_concentration(events, fs, 10.0)
    assert r > 0.99
    assert p < 1e-10


def test_local_envelope_prominence_finds_target_peak():
    freq = np.arange(0, 500, 0.1)
    amplitude = np.ones_like(freq)
    amplitude[np.argmin(np.abs(freq - 120.2))] = 10
    observed, prominence = local_envelope_prominence(freq, amplitude, 120.0)
    assert np.isclose(observed, 120.2)
    assert np.isclose(prominence, 20.0)


def test_relevant_target_uses_fault_tokens():
    assert relevant_target("IR+OR+B", "BPFI")
    assert relevant_target("IR+OR+B", "BPFO")
    assert relevant_target("IR+OR+B", "BSF")
    assert not relevant_target("IR", "BPFO")


def test_compound_targets_follow_s1_physical_families():
    targets = {row["target"]: row for row in compound_targets("30204", 20.0)}
    orders = bearing_orders("30204")
    assert np.isclose(targets["BPFI_2x_plus_1X"]["frequency_hz"], 2 * orders["BPFI"] * 20 + 20)
    assert np.isclose(targets["BSF_2x_minus_FTF"]["frequency_hz"],
                      2 * orders["BSF"] * 20 - orders["FTF"] * 20)
    assert "BPFO_2x" in targets
    assert "BPFI_1x_plus_BPFO" not in targets
    assert targets["BSF_3x_plus_FTF"]["overlaps_other_family_search_window"] == "Yes"
    assert targets["BSF_3x_plus_FTF"]["nearest_other_family_target"] == "BPFI_1x"


def test_fault_token_matching_does_not_use_substrings():
    assert fault_tokens("IR+OR+B") == {"IR", "OR", "B"}
    assert component_expected("IR+B", "IR")
    assert not component_expected("IR+B", "OR")


def test_task_b_interpretation_uses_seven_and_ten_khz_thresholds():
    base = {"file": "x", "bearing": "30204", "rpm": "1600", "rotor": "H",
            "fault": "IR", "channel": "CH0", "raw_peak_abs_g": "55"}
    base.update({f"lpf_{cutoff}_peak_abs_g": str(value) for cutoff, value in
                 zip((3000, 5000, 7000, 9000, 10000, 11000), (20, 25, 40, 45, 48, 53))})
    assert interpret_row(base)["task_b_branch"] == "L1"
    base["lpf_10000_peak_abs_g"] = "52"
    assert interpret_row(base)["task_b_branch"] == "L2"
    base["lpf_7000_peak_abs_g"] = "51"
    assert interpret_row(base)["task_b_branch"] == "L3"


def test_task_b_c_combination_uses_branch_band(tmp_path):
    task_b = [{"file": "f", "bearing": "30204", "rpm": "1600", "rotor": "H", "fault": "IR",
               "channel": "Channel 0", "raw_peak_abs_g": 52.0, "task_b_branch": "L2"}]
    compound = tmp_path / "compound.csv"
    compound.write_text(
        "file,channel,carrier_band_hz,expected_for_label,component,overlaps_other_family_search_window,target,local_prominence_db\n"
        "f,CH0,7000-10000,Yes,IR,No,BPFI_1x,18\n"
        "f,CH0,2000-7000,Yes,IR,No,BPFI_1x,20\n", encoding="utf-8")
    output = combine_task_b_c(task_b, compound, tmp_path / "combined.csv")
    assert output[0]["task_c_status"] == "M+ (expanded family)"
    assert output[0]["control_2_7khz_status"] == "M+ (expanded family)"


def test_all_established_iir_families_design_as_sos():
    for filter_name in FILTERS:
        for band in BANDS:
            sos = design_sos(filter_name, band, 25600.0)
            assert sos.ndim == 2 and sos.shape[1] == 6
            assert np.all(np.isfinite(sos))


def test_centered_excerpt_contains_global_peak():
    values = np.zeros(1000); values[900] = 10
    excerpt, start, peak = centered_excerpt(values, 100.0, duration_s=2.0)
    assert peak == 900
    assert start <= peak < start + len(excerpt)


def test_acceleration_distribution_reports_quantiles_and_threshold_counts():
    values = np.array([-50.0, -20.0, 0.0, 10.0, 60.0])
    result = acceleration_distribution(values)
    assert result["distribution_samples"] == 5
    assert result["peak_abs_g"] == 60.0
    assert result["median_abs_g"] == 20.0
    assert result["samples_over_50g"] == 1
    assert result["pct_samples_over_50g"] == 20.0


def test_acceleration_histogram_accounts_for_every_sample():
    values = np.array([0.0, 0.2, 1.5, 9.0, 25.0, 55.0])
    counts = _histogram_counts(values)
    assert int(np.sum(counts)) == len(values)
    assert counts[-1] == 1


def test_multifilter_plot_matrix_preserves_declared_order():
    rows = [
        {"filter": filter_name, "band": band, "value": str(i * 10 + j)}
        for i, filter_name in enumerate(PLOT_FILTERS)
        for j, band in enumerate(PLOT_BANDS)
    ]
    values = _matrix(rows, "value")
    assert values.shape == (5, 5)
    assert values[0, 0] == 0
    assert values[-1, -1] == 44


def test_channel_median_matrix_separates_ch0_and_ch1():
    rows = []
    for filter_name in PLOT_FILTERS:
        for band in PLOT_BANDS:
            rows.extend([
                {"filter": filter_name, "band": band, "channel": "CH0", "band_peak_abs_g": "10"},
                {"filter": filter_name, "band": band, "channel": "CH0", "band_peak_abs_g": "20"},
                {"filter": filter_name, "band": band, "channel": "CH1", "band_peak_abs_g": "40"},
            ])
    ch0 = _channel_median_matrix(rows, "CH0")
    ch1 = _channel_median_matrix(rows, "CH1")
    assert ch0.shape == (5, 5)
    assert np.all(ch0 == 15)
    assert np.all(ch1 == 40)


def test_cutoff_scenario_summary_counts_above_and_below_50g(tmp_path):
    rows = []
    for channel, peak_count in (("CH0", 2), ("CH1", 3)):
        for index, filter_name in enumerate(FILTERS):
            rows.append({
                "file": "f", "bearing": "N204", "rpm": "1600", "rotor": "H",
                "fault": "IR+OR+B", "channel": channel, "filter": filter_name,
                "cutoff_hz": "10000", "retained_peak_abs_g": "50.1" if index < peak_count else "49.9",
            })
    summary = summarize_cutoff_scenarios(rows, tmp_path)
    assert sum(row["retained_peak_over_50g_channels"] for row in summary) == 5
    with (tmp_path / "multifilter_cutoff_consensus_summary.csv").open(encoding="utf-8") as handle:
        consensus = list(csv.DictReader(handle))
    assert consensus[0]["majority_at_least_3_of_5_channels"] == "1"


def test_measurement_window_discards_first_minute_for_ordinary_recording():
    window = measurement_window(total_samples=200 * 25600, fs=25600.0, bearing="N204")
    assert window.start_s == 60.0
    assert window.end_s == 180.0
    assert window.policy == "discard_first_60s_keep_next_120s"


def test_measurement_window_discards_five_minutes_for_long_30204_recording():
    window = measurement_window(total_samples=431 * 25600, fs=25600.0, bearing="30204")
    assert window.start_s == 300.0
    assert window.end_s == 420.0
    assert window.policy == "discard_first_300s_keep_next_120s"


def test_measurement_window_rejects_recording_shorter_than_required_interval():
    with np.testing.assert_raises(ValueError):
        measurement_window(total_samples=170 * 25600, fs=25600.0, bearing="6204")


def test_sampling_rate_label_preserves_fractional_native_rate():
    assert _rate_label(12800.0) == "12.8 kHz"
    assert _rate_label(17066.666666666668) == "17.0667 kHz"
    assert _rate_label(25600.0) == "25.6 kHz"


def test_sampling_rate_distribution_metrics_use_absolute_tail():
    metrics = sampling_rate_distribution_metrics(np.array([-4.0, 0.0, 3.0]), "x")
    assert metrics["x_peak_abs_g"] == 4.0
    assert metrics["x_rms_g"] == np.sqrt(25.0 / 3.0)
    assert metrics["x_p99_99_abs_g"] <= 4.0


def test_sampling_rate_windows_keep_equal_sample_counts_after_idle():
    expected_durations = {12800.0: 240.0, 17066.666666666668: 180.0, 25600.0: 120.0}
    for rate, duration in expected_durations.items():
        window = sampling_rate_measurement_window(int((60 + duration + 1) * rate), rate)
        assert window.end_sample - window.start_sample == 3_072_000
        assert np.isclose(window.duration_s, duration)
