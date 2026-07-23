# Pilot Validation Protocol

## Execution status

- 2026-07-22 first crossover pilot: four 13A131/NI-9234 channels were moved sequentially across shaft-end/motor-end top/side positions under 30204 IR, healthy rotor, nominal 1400 RPM. All channels passed preliminary finite/range/shaft/BPFI-envelope screening.
- This run supports sensor/channel commissioning and position observability only. It does not complete simultaneous-layout, phase/coherence, multi-RPM, healthy-reference, remount-repeatability, rate-comparison, or compound-feasibility phases.
- Evidence and results: [`../pilot/2026-07-22_1400rpm_30204_ir_h/pilot_validation_report_ko.md`](../pilot/2026-07-22_1400rpm_30204_ir_h/pilot_validation_report_ko.md)

## Objective

Determine whether the proposed CH1–CH4 layout is mechanically and diagnostically justified, and select evidence-based sampling-rate and record-length candidates before full acquisition.

## Phase 0 — documentation and compatibility

- Record delivered 13A131 serial numbers and calibration sensitivities.
- Confirm exact NI-9234 connector variant, cable/adapters, IEPE configuration, and cDAQ-9171 setup.
- Resolve M5 sensor mounting against the actual magnet/stud/adapter; do not reuse the legacy 1/4-28 conclusion.
- Photograph housing surfaces and define rig-fixed x/y/z, shaft-end/motor-end, top/side, and load direction.
- Record candidate bearing model/geometry and RPM/load limits.

## Phase 1 — channel commissioning

- Check IEPE bias/health on every channel.
- Measure stationary electrical/mechanical noise.
- Apply a common-input or co-located excitation to compare gain, phase, polarity, and timing.
- Swap sensor serial numbers among channels to identify sensor-specific bias.
- Verify simultaneous NI-9234 configuration and record software/task settings.

## Phase 2 — mounting repeatability

For each candidate position, perform at least three remove/remount cycles under the same healthy condition. Preserve mounting operator, surface preparation, magnet/adapter, cable routing, and photos.

Evaluate RMS/peak variation, broadband spectrum, coherence, resonance changes, and repeatability of shaft/order peaks. A position with unstable remount response should not enter the full dataset without mounting redesign.

## Phase 3 — layout comparison

Use matched healthy and pure-fault references before compound faults. Record the proposed four-channel layout and at least one alternative containing an axial or support/base location.

For every run retain:

- all four raw channels;
- measured RPM/tachometer alignment;
- load/torque and temperature if available;
- bearing/assembly ID, defect metadata, sensor serial-to-position map;
- mounting/remount and acquisition-order identifiers.

Compare physical peak SNR, envelope/order visibility, cross-channel complementarity, noise/clipping, repeatability, and grouped channel-ablation performance.

## Phase 4 — rate comparison

Acquire identical or closely repeated pilot conditions at NI-9234-native 51.2 and 25.6 kS/s. Apply a documented filter/downsampling procedure from 51.2 to 25.6 kS/s and compare:

- retained diagnostic/envelope peaks;
- aliasing or filter artifacts;
- phase/coherence;
- transient/impact representation;
- storage and inference cost.

Include 17.067 kS/s only if pilot evidence shows that useful information is confined below its approximately 7.68 kHz alias-free band.

## Phase 5 — duration/window comparison

Acquire 60-second synchronized master records and evaluate deterministic 1-, 2-, 5-, 10-, 30-, and 60-second analysis windows. Compare minimum rotations, spectral/order resolution, feature variance, stationarity, repeatability, and model stability. Prevent windows from the same physical run from crossing dataset splits. The 60-second acquisition duration is selected; the canonical model-input window and stabilization-exclusion rule remain open.

## Phase 6 — compound feasibility

Only after pure references pass physical validation, assemble candidate compound faults. Confirm component geometry before installation and inspect after acquisition. Treat unexpected collateral damage or missing physical signatures as `conflicting`, not automatically verified.

## Pilot outputs

- selected four-channel positions/directions with quantitative rationale;
- rejected alternatives and reasons;
- selected native master rate and release/downsample rate;
- selected master duration and canonical inference windows;
- mounting procedure and response limit;
- RPM/load grid recommendation;
- expected physical frequencies and validation tolerances;
- projected full-dataset storage;
- unresolved risks requiring another pilot iteration.

## Stop/go criteria

Do not begin full acquisition until all channels pass health/timing checks, mounting is repeatable, selected positions add non-redundant physical information, rate/duration meet predeclared bandwidth/rotation criteria, and proposed compound labels can be independently confirmed.
