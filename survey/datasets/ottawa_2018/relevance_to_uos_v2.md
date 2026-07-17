# Relevance to UOS Dataset v2: Ottawa 2018

## Source-supported observations

- Ottawa 2018 provides paired vibration and encoder records with speed changing inside each 10-second sample. [OTT18-E03–E05]
- It samples both channels at 200 kHz for 10 seconds. [OTT18-E04]
- Its 36 records balance three health states, four trajectory families, and three trials, although exact speed endpoints vary. [OTT18-E06, E07]
- It provides BPFI/BPFO order coefficients but not systematic record-level physical validation. [OTT18-E08]
- It contains one vibration position and no compound-fault label. [OTT18-E03, E09]

## Interpretation

Ottawa 2018 is useful for deciding whether UOS v2 should include dynamic speed trajectories and a synchronized tachometer/encoder, but it is not evidence for multi-position vibration or compound diagnosis. Its 200 kHz setting is a precedent without a published rationale and should not be copied. The paired speed channel is particularly important because variable-speed fault frequencies must be represented as time-varying orders rather than stationary FFT peaks.

## Candidate strengths or gaps to test

- Not a gap: within-record increasing/decreasing RPM trajectories exist.
- Not a gap: vibration and shaft-speed signals are paired in each record.
- Candidate difference: UOS v2 targets multiple vibration positions/directions.
- Candidate gap: no internal-bearing or bearing–rotor compound conditions.
- Candidate gap: no paired single-/multi-vibration-channel comparison.
- Candidate gap: no published rationale for the very high sampling rate.
- Candidate gap: no systematic order-tracked envelope/fault-frequency validation reported.

## Design implications

- Decide explicitly whether UOS v2 covers only steady-state RPM levels or also ramp/transient records; label these as different acquisition modes.
- If variable-speed data are collected, preserve synchronized tachometer/encoder data and commanded versus measured speed trajectories.
- Match or balance speed trajectories across health/fault labels to prevent speed from becoming a label shortcut.
- Use order tracking or angle-domain resampling for physics validation under changing RPM.
- Derive vibration sampling rate from sensor/DAQ bandwidth and target bearing resonance/fault features, not the 200 kHz precedent.
- Derive record length jointly from minimum rotations, trajectory duration, spectral/order resolution, storage, and real-time inference windows.

## Open questions

- How were inner- and outer-race faults generated and sized?
- What load, accelerometer axis, and mounting method were used?
- Why was 200 kHz selected, and what analog filtering was applied?
- Are USB-6212 channels simultaneous or multiplexed, and what skew applies?
- Does the repository resolve the duplicated `O-C-1` label?
- What license applies to the Mendeley data files?
