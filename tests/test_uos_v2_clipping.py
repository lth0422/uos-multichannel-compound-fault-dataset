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
    centered_excerpt,
    design_sos,
    summarize_cutoff_scenarios,
)
from scripts.plot_uos_v2_multifilter_bands import (
    BANDS as PLOT_BANDS,
    FILTERS as PLOT_FILTERS,
    _matrix,
)


def test_parse_filename_handles_compound_fault():
    result = parse_filename(Path("M3_IR+OR+B_25600_30204_1600.tdms"))
    assert result == {"rotor": "M3", "fault": "IR+OR+B", "fs": "25600", "bearing": "30204", "rpm": "1600"}


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
