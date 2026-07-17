# Relevance to UOS Dataset v2: Paderborn University

## Source-supported observations

- PU reports synchronized 64 kHz acquisition of one bearing-housing vibration channel and two motor-current channels, plus lower-rate operating-condition signals. [PU-E03, E06]
- Its vibration sensor is at one top adapter position in the main radial-load direction; it is not a synchronized multi-position vibration dataset. [PU-E04, E15]
- Four-second records are repeated twenty times per operating setting. [PU-E07]
- PU includes artificial single IR/OR faults and accelerated-life damage. Three documented bearing instances contain concurrent IR and OR damage. [PU-E10, E11]
- It validates vibration with characteristic-frequency envelope spectra. [PU-E14]

## Interpretation

Compared with UOS v1, PU contributes two features that matter to the v2 hypotheses: cross-modality synchronization and evidence of internal IR+OR compound damage. However, PU's synchronized channels are not four vibration positions, and its internal compound cases are naturally developed bearing instances rather than a complete controlled compound matrix. Therefore, a candidate UOS v2 contribution could be controlled, repeatable internal compound combinations combined with synchronized multi-position vibration—but only if the broader survey confirms this remains uncommon and pilot validation shows the channels are physically informative.

## Candidate strengths or gaps to test

- Candidate gap: one vibration location cannot support paired single- versus multi-position vibration evaluation.
- Candidate gap: no designed IR+ball, OR+ball, or IR+OR+ball coverage is reported.
- Candidate reference: PU shows how to distinguish naturally developed multiple damage from artificial single-point damage and documents bearing instances in detail.
- Candidate reference: PU records load, radial force, speed, and temperature alongside diagnostic signals and uses repeated fixed-length records.
- Candidate validation precedent: envelope analysis against bearing characteristic frequencies.
- Not established: PU's 64 kHz rate or four-second duration is optimal for UOS v2; its sensors and analog filters have different bandwidths from the purchased UOS v2 hardware.

## Design implications

- Separate `fault_generation` (seeded versus accelerated-life/natural) from `compound components` in v2 labels.
- Record every defect component independently so IR+OR remains multi-label traceable rather than only a bearing-code class.
- Store RPM, torque/load, radial force, and temperature with explicit timestamps or synchronization metadata.
- Evaluate candidate vibration positions using the main load direction and transmission paths, but test multiple locations rather than copying PU's single position.
- Determine sampling rate from the HS 13A131 bandwidth, NI-9234 native rates, desired envelope band, and pilot spectra—not from PU's 64 kHz alone.
- Treat four-second records and twenty repetitions as comparative evidence for survey synthesis, not a default acquisition requirement.

## Open questions

- Do deposited MAT files contain the supporting signals and their exact sample rates, units, and timestamps?
- Are bearing damage fact sheets and photographs downloadable separately and machine-readable?
- How are the IR+OR cases labeled in files: only bearing code, component fields, or explicit multiple labels?
- Does current official documentation provide the A/D converter model, accelerometer mounting method, calibration, and channel phase information?
- What independent repetitions exist across distinct bearings for each compound configuration?
