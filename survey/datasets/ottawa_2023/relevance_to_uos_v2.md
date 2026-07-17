# Relevance to UOS Dataset v2: Ottawa 2023

## Source-supported observations

- Ottawa 2023 provides one vibration channel plus acoustic, RPM, load, and temperature information in five-column, 42 kHz, 10-second records. [OTT23-E02–E04]
- It explicitly reports a sampling rationale based on 20 kHz audible bandwidth, Nyquist, DAQ capability, and deep-learning sample volume. [OTT23-E04]
- It records healthy, developing, and faulty stages for natural accelerated inner-race, outer-race, ball, and cage deterioration. [OTT23-E06, E07]
- It tests inside/outside accelerometer placement and selects direct inside-casing bearing mounting for lower noise. [OTT23-E10]
- Fault labels are confounded with bearing model and, for ball faults, load. [OTT23-E08, E09]

## Interpretation

Ottawa 2023 is valuable for sensor-placement and sampling-rationale comparison, but it is not multi-position vibration and does not contain controlled compound faults. Its 42 kHz/10-second choice should not automatically become the UOS setting because its rationale prioritizes audible acoustic bandwidth and deep-learning sample count. UOS v2 needs a vibration-specific bandwidth, rotation-count, frequency-resolution, storage, and real-time-window argument.

## Candidate strengths or gaps to test

- Not a gap: natural IR, OR, ball, and cage classes with developing stages exist.
- Not a gap: explicit empirical accelerometer-position selection exists.
- Not a gap: multimodal synchronized records and published rate/length rationale exist.
- Candidate difference: UOS v2 targets several vibration positions/directions rather than one vibration channel plus other modalities.
- Candidate gap: no internal-bearing or bearing–rotor compound matrix.
- Candidate gap: no paired single-/multi-vibration-channel comparison.
- Candidate gap: no systematic characteristic-frequency/envelope validation for all records.
- Candidate strength to protect: UOS factorial design should avoid coupling fault label with bearing model, load, or acquisition order.

## Design implications

- Pilot UOS sensor locations quantitatively using SNR, fault-frequency visibility, clipping/noise floor, repeatability, and cross-channel complementarity.
- Derive sampling rate from HS 13A131/NI-9234 usable bandwidth and target bearing/sideband frequencies, rather than acoustic audible range.
- Derive record length from lowest-RPM rotation count, desired spectral resolution, repeatability, storage, and on-device windowing.
- Use the same bearing model and matched load/RPM matrix across fault labels unless domain-shift factors are intentionally balanced.
- Randomize or block acquisition order so defect label cannot be inferred from bearing batch or time.
- Preserve pure faults and deliberate compound combinations with independent multi-label component metadata.

## Open questions

- What license and version metadata govern the Mendeley data files?
- Does the repository contain `B-12-2`, resolving the Table 1 typo?
- What exact accelerometer direction is measured?
- Are USB-6212 channels simultaneous or multiplexed, and what skew applies?
- Are all roughly 50 lifecycle files per bearing retained anywhere, or only the selected three stages?
- What quantitative metric supported the inside-versus-outside placement decision?
