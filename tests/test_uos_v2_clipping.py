from pathlib import Path

import numpy as np

from scripts.analyze_uos_v2_clipping import (
    _max_run,
    _zero_shift_screen,
    bearing_frequencies,
    bearing_orders,
    parse_filename,
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
