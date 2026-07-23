import math

import numpy as np

from scripts.analyze_uos_pilot import (
    BearingGeometry,
    GEOMETRY_30204,
    amplitude_spectrum,
    bearing_frequencies_hz,
    bearing_frequency_orders,
    common_band_signal,
    summarize_peak_frequencies,
    target_peak,
    _pairwise_correlations,
    windowed_rms,
)


def test_30204_characteristic_frequencies_at_1400_rpm():
    frequencies = bearing_frequencies_hz(GEOMETRY_30204, 1400.0)
    assert math.isclose(frequencies["shaft"], 23.333333, rel_tol=1e-6)
    assert math.isclose(frequencies["BPFI"], 204.577366, rel_tol=1e-6)
    assert math.isclose(frequencies["BPFO"], 145.422634, rel_tol=1e-6)
    assert math.isclose(frequencies["BSF"], 65.441255, rel_tol=1e-6)
    assert math.isclose(frequencies["FTF"], 9.694842, rel_tol=1e-6)


def test_bearing_orders_are_independent_of_rpm():
    geometry = BearingGeometry(34.57, 7.94, 0.0, 8)
    orders = bearing_frequency_orders(geometry)
    low = bearing_frequencies_hz(geometry, 600.0)
    high = bearing_frequencies_hz(geometry, 1600.0)
    assert math.isclose(low["BPFI"] / (600.0 / 60.0), orders["BPFI"])
    assert math.isclose(high["BPFI"] / (1600.0 / 60.0), orders["BPFI"])


def test_target_peak_detects_known_sinusoid():
    sampling_rate = 2_000.0
    time = np.arange(int(8 * sampling_rate)) / sampling_rate
    values = np.sin(2 * np.pi * 123.0 * time) + 0.01 * np.sin(
        2 * np.pi * 80.0 * time
    )
    frequencies, amplitudes = amplitude_spectrum(values, sampling_rate)
    peak_frequency, _, snr_db = target_peak(frequencies, amplitudes, 123.0)
    assert abs(peak_frequency - 123.0) <= 0.25
    assert snr_db > 40.0


def test_windowed_rms_returns_nonoverlapping_windows():
    sampling_rate = 100.0
    values = np.r_[np.ones(500), np.ones(500) * 2.0]
    times, rms = windowed_rms(values, sampling_rate, window_seconds=5.0)
    assert np.allclose(times, [2.5, 7.5])
    # Standard deviation is used after implicit DC removal for acceleration RMS.
    assert np.allclose(rms, [0.0, 0.0])


def test_pairwise_correlations_returns_each_unique_pair():
    vectors = [np.arange(10.0), np.arange(10.0) * 2.0, -np.arange(10.0)]
    correlations = _pairwise_correlations(vectors)
    assert len(correlations) == 3
    assert np.allclose(sorted(correlations), [-1.0, -1.0, 1.0])


def test_common_band_filter_rejects_above_cutoff_component():
    sampling_rate = 25_600.0
    time = np.arange(int(2 * sampling_rate)) / sampling_rate
    low = np.sin(2 * np.pi * 1_000.0 * time)
    high = np.sin(2 * np.pi * 9_000.0 * time)
    filtered = common_band_signal(low + high, sampling_rate, cutoff_hz=7_000.0)
    assert math.isclose(np.std(filtered), np.std(low), rel_tol=0.01)


def test_peak_frequency_summary_keeps_exact_channel_values():
    row = {
        "system": "13A131 + NI-9234",
        "position": "ShaftEndTop",
        "channel": "CH0",
        "shaft_expected_hz": 23.333,
        "shaft_fft_peak_hz": 23.25,
        "shaft_fft_local_snr_db": 60.0,
        "bpfi_expected_hz": 204.577,
        "bpfi_envelope_peak_hz": 205.25,
        "bpfi_envelope_local_snr_db": 20.0,
    }
    summary = summarize_peak_frequencies([row])
    assert summary[0]["shaft_fft_peak_hz"] == 23.25
    assert math.isclose(summary[0]["bpfi_error_hz"], 0.673)
