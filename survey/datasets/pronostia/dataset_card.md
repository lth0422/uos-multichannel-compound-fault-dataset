# Dataset Card: PRONOSTIA / FEMTO-ST

## Identity

- Dataset ID: pronostia
- Dataset name: PRONOSTIA / FEMTO-ST / IEEE PHM 2012 Challenge
- Institution: FEMTO-ST Institute
- Release year: 2012
- Primary publication: HAL `hal-00719503`

## Purpose and scope

PRONOSTIA is an accelerated bearing-degradation platform supporting condition monitoring, diagnostics, and RUL prognostics. The PHM 2012 challenge release contains complete learning trajectories and truncated test trajectories under three operating conditions. [PRO-E01, E07, E08]

## Acquisition setup

An asynchronous motor and belt/pulley reduction drive the tested ball bearing. A pneumatic actuator and lever apply radial load to its outer ring. Speed, radial force, and torque are monitored online. Bearings begin without seeded defects and are degraded through operation until failure. [PRO-E02, E07]

## Sensors and channels

- Two miniature accelerometers: horizontal and vertical
- Vibration position: one tested-bearing outer race
- One PT100 temperature probe near the outer ring
- Speed, radial-force, and torque sensors
- NI cDAQ four-slot chassis with three unspecified I/O modules

This is multi-sensor, multi-modal, multi-channel, and multi-direction, but not multi-position vibration. The platform aggregates/timestamps signals, while hardware simultaneity and skew remain Unknown. [PRO-E04–E06, E13]

## Operating conditions

| Condition | Speed | Radial force |
|---|---:|---:|
| 1 | 1,800 RPM | 4,000 N |
| 2 | 1,650 RPM | 4,200 N |
| 3 | 1,500 RPM | 5,000 N |

These values vary across experiments but remain constant within each challenge run. The platform could support variable conditions, but the paper describes within-run variation as future work. Speed and load are coupled, so their effects cannot be independently separated from this matrix. [PRO-E07]

## Sampling and temporal organization

- Acceleration: 25.6 kHz
- Temperature: 10 Hz
- Speed, radial force, torque: 100 Hz
- Snapshot length, samples per snapshot, and snapshot cadence: Unknown
- Physical lifetime: approximately 1–7 hours across bearings

The paper says 25.6 kHz captures the bearing frequency spectrum but does not provide a quantitative highest-frequency, anti-aliasing, or rate-selection derivation. [PRO-E05, E08, E12]

## Fault conditions and labels

Defects are not seeded initially. The authors report that naturally degraded bearings may contain damage in balls, rings, and cage at the same time. This establishes natural internal bearing compound damage, but not a controlled IR+OR/IR+ball/OR+ball matrix. Challenge test failure types are deliberately not supplied to participants. [PRO-E02, E03, E09]

There are no introduced rotor or gear fault classes. Applied radial load accelerates bearing degradation but is an operating condition, not a rotor fault.

## Data organization and access

The challenge contains six full run-to-failure learning trajectories and eleven truncated test trajectories. Conditions 1 and 2 each have two full learning bearings and five test bearings; Condition 3 has two learning and one test bearing. File format, per-file schema, cadence, and sample count are not provided in the reviewed paper. [PRO-E08, E12]

## Validation reported by source

The paper shows normal/degraded bearing images and example PSD, K-factor, crest-factor, and wavelet-packet trends. It explicitly reports that conventional characteristic-frequency signatures and L10 predictions do not match reliably because failure patterns vary and multiple components may degrade together. Thus it documents physical complexity rather than validating every record against a known fault frequency. [PRO-E10, E11]

## Known limitations and conflicts

- Natural compound damage lacks controlled component labels/severity. [PRO-E03, E09]
- Only one vibration position, although two directions are measured. [PRO-E04]
- Speed and load are coupled across three conditions. [PRO-E07]
- Eleven challenge trajectories are truncated. [PRO-E08]
- Snapshot/file schema, exact bearing model, stopping criterion, mounting attachment, and license are Unknown. [PRO-E12]
- cDAQ module identities and timing/skew are Unknown. [PRO-E06, E13]

## Evidence coverage

Original platform/challenge-paper extraction is linked to PRO-E01–E13. Official challenge README, bearing geometry, raw schema, failure/stopping definitions, and license are still required for independent verification; raw signal download is not currently necessary.
