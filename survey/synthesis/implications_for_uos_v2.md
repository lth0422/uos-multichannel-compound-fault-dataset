# Implications for UOS Dataset v2

## Decision status

The core-ten survey plus KAIST Batch and HUST Vietnam supports a pilot design, not final acquisition settings. Sensor positions, channel count, sampling rate, RPM/load grid, record length, fault combinations, repetitions, and paper contributions remain unconfirmed until hardware characterization and pilot validation are complete.

## Proposed design requirements for the pilot

### 1. Separate fault axes in metadata

Use independent fields for bearing component (`IR`, `OR`, `ball/roller`, `cage`) and rotating-system condition (`unbalance`, `misalignment`, `looseness`, other). Store multi-label vectors rather than collapsing compounds into opaque class names. Record defect generation, size, angular location/load-zone relationship, severity, bearing identity, installation, and post-test observations.

### 2. Preserve pure references and planned compounds

Before compound acquisition, collect matched healthy and pure single-fault references. HUST Vietnam already publishes IR+OR, IR+Ball, and OR+Ball, so UOS differentiation requires more than those class names. A candidate design is a balanced pairwise-plus-triple matrix with controlled severity and independent validation, but feasibility must be demonstrated before this becomes final scope. Bearing–rotor combinations should be factorially separated from internal components where practical. [HUSTV-E08–E09]

### 3. Treat synchronization as a measured/documented property

For the purchased NI-9234/cDAQ-9171 system, document:

- physical channel-to-sensor mapping;
- chassis/module clock architecture and ADC topology;
- supported native rate actually used;
- anti-alias/filter behavior and group delay;
- start alignment, channel skew specification or measurement;
- timestamp/RPM alignment;
- calibration and units.

Use `simultaneous sampling` only if hardware documentation supports it; otherwise use the narrower verified term.

### 4. Select positions through a pilot

Evaluate candidate positions/directions with the same event recorded on all four accelerometers. At minimum measure:

- fault-frequency and envelope visibility;
- signal-to-noise ratio/noise floor;
- clipping and dynamic range;
- repeatability across reinstallations and trials;
- coherence/correlation and non-redundant information;
- sensitivity to load direction and defect angular location;
- single-position and position-combination diagnostic performance.

The result may be multiple positions, multiple directions around one housing, or a mixture. Do not decide taxonomy before measuring the physical layout.

KAIST's simultaneous x/y measurements at two bearing housings and ISO 10816-1 citation make the present UOS arrangement a defensible pilot candidate, but not a validated or novel final layout. [KAIB-E02, KAIB-E11]

### 5. Derive sampling rate rather than voting across datasets

Determine the highest diagnostic frequency from bearing geometry, maximum RPM, expected fault harmonics/sidebands, and useful structural/sensor resonance band. Intersect this with the calibrated HS 13A131 bandwidth and NI-9234 supported rates/filter response. Apply alias margin, then choose a native acquisition rate. If on-device inference needs a lower rate, retain the master signal and publish a reproducible downsampling pipeline.

### 6. Derive record length from four constraints

For every candidate duration calculate:

1. rotations at the minimum RPM;
2. spectral resolution `1/T`;
3. stationarity or trajectory coverage;
4. storage and inference-window cost.

Prefer collecting longer synchronized master records and defining non-overlapping or explicitly indexed shorter windows afterward. Preserve grouping IDs so windows from the same physical run cannot leak across train/test splits.

### 7. Design RPM and load independently

Avoid assigning every RPM to only one load or every fault to a different bearing batch. Use a balanced factorial grid or explicitly document incomplete blocks. Randomize/block acquisition order and retain measured RPM/load traces, temperature, bearing ID, assembly ID, and trial ID.

### 8. Predeclare physical validation

For each pure and compound condition plan:

- expected rotational and bearing characteristic frequencies from geometry;
- envelope/order spectrum method and frequency tolerance;
- expected rotor-fault harmonics/sidebands;
- time-domain clipping, saturation, missing-value, and noise checks;
- cross-channel timing/coherence checks;
- repeated-run variability;
- photographic/metrological or teardown confirmation.

Allow `conflicting` outcomes. A missing expected peak must not be silently converted into a verified label.

## Candidate acquisition architecture

This is a pilot hypothesis, not a final configuration:

- acquire all four HS 13A131 accelerometers synchronously through the NI-9234;
- include measured RPM/tachometer data with an explicitly verified alignment method;
- store calibrated raw master records before windowing;
- retain fixed canonical channel order and position coordinates;
- expose canonical single-channel and multi-channel subsets from the same records;
- create split groups at physical run/bearing/assembly level, never at window level alone.

## Decision gates

### Gate A — hardware

Confirm sensor calibration, mounting hardware, NI-9234 connector/power compatibility, supported native rates, filter response, and RPM-channel integration.

### Gate B — pilot positions

Choose the four-channel layout only after quantitative visibility, repeatability, redundancy, and mounting tests.

### Gate C — sampling and duration

Approve a rate/duration pair only after bandwidth/alias, minimum-rotation, resolution, storage, and inference analyses.

### Gate D — fault feasibility

Demonstrate that every proposed compound can be assembled reproducibly and independently confirmed without uncontrolled collateral damage.

### Gate E — dataset contribution

Freeze paper claims only after repository verification of the closest datasets and pilot evidence. Until then use `candidate contribution` or `candidate strength`.

## Immediate next work

1. Verify NI-9234 and HS 13A131 primary datasheets/calibration documents.
2. Define the candidate bearing geometry and calculate shaft/BPFO/BPFI/BSF/FTF ranges over proposed RPMs.
3. Draft a four-sensor placement pilot with explicit metrics and remount repetitions.
4. Compare two or three NI-9234-native rate/duration candidates using pilot spectra and storage estimates.
5. Verify official metadata for the closest compound comparators: Arkansas, MAFAULDA, Paderborn, NASA IMS, and PRONOSTIA.
6. Verify KAIST Batch's official repository schema/license and exact mounting only if those details affect a design gate; review SEU/HUST only with original or official dataset documentation.
