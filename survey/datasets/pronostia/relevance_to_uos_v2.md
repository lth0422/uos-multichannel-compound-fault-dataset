# Relevance to UOS Dataset v2: PRONOSTIA / FEMTO-ST

## Source-supported observations

- PRONOSTIA measures horizontal and vertical vibration at one tested-bearing position plus temperature, speed, radial force, and torque. [PRO-E04, E05]
- It uses 25.6 kHz acceleration under three fixed-per-run RPM/load pairs. [PRO-E05, E07]
- Six challenge trajectories are full run-to-failure and eleven are truncated for RUL prediction. [PRO-E08]
- Naturally degraded bearings can contain ball, ring, and cage damage simultaneously. [PRO-E02, E03]
- Classical characteristic-frequency and theoretical-life models are reported to mismatch these mixed, stochastic degradations. [PRO-E10]

## Interpretation

PRONOSTIA shows that naturally developed internal compound damage and two-direction bearing vibration already exist. However, the absence of controlled component labels makes it unsuitable as a clean multi-label compound-diagnosis matrix. UOS v2 can be complementary by deliberately controlling fault components and validating each label physically, while avoiding claims that natural compound degradation itself is new.

## Candidate strengths or gaps to test

- Not a gap: two-direction vibration at one bearing position exists.
- Not a gap: natural simultaneous multi-component bearing degradation exists.
- Not a gap: multiple RPM/load conditions and full lifecycle data exist.
- Candidate difference: UOS v2 targets controlled, repeatable, component-level compound labels.
- Candidate difference: UOS v2 targets multiple vibration positions and paired channel ablation.
- Candidate gap: no bearing–rotor fault matrix or looseness/misalignment/unbalance class.
- Candidate gap: no hardware timing evidence or published single-/multi-channel comparison.
- Candidate opportunity: combine known seeded geometry with envelope/order validation, while clearly distinguishing it from natural degradation realism.

## Design implications

- State explicitly whether each UOS defect is seeded/artificial or naturally developed; do not treat these as interchangeable.
- For compound labels, document every simultaneously present component, defect size/location, assembly, and post-test inspection result.
- Use controlled single faults as physical references before interpreting compound spectra.
- Preserve synchronized RPM/load signals and avoid coupling each RPM to only one load if independent robustness analysis is intended.
- Select sampling rate from known bearing geometry, resonance bandwidth, sensor/DAQ response, and validation targets; 25.6 kHz alone is only a precedent.
- Select record length after comparing minimum rotations, frequency resolution, repeatability, storage, and on-device windows; PRONOSTIA's paper cannot supply this because snapshot duration is absent.

## Open questions

- What snapshot duration, cadence, sample count, and file format are defined by the official challenge README?
- What bearing model/geometry and theoretical BPFI/BPFO/BSF/FTF values apply?
- What exact stopping/failure criterion defines the end of each run?
- Which final components were damaged in each learning and test bearing?
- What accelerometer models, mounting attachment, cDAQ modules, and timing topology were used?
- What license governs the challenge data files?
