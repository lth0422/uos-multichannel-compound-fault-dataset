# Dataset Card: CWRU

## Identity

- Dataset ID: cwru
- Dataset name: CWRU
- Institution: Case Western Reserve University
- Release year: Unknown

## Purpose and scope

Canonical seeded-fault ball-bearing benchmark distributed by the Case Western Reserve University Bearing Data Center. It provides vibration from normal and separately seeded IR, OR, and ball faults under multiple fixed motor load/speed conditions. [CWRU-E01, E03, E11]

## Acquisition setup

A 2 hp motor drives a dynamometer through a torque transducer/encoder. Test bearings support the motor shaft. EDM single-point defects were seeded separately, faulted bearings were reinstalled, and finite records were acquired under 0–3 hp conditions. This is a batch dataset, not a run-to-failure dataset. [CWRU-E02, E03, E11]

### Measurement position and mounting rationale

Accelerometers with magnetic bases were placed at 12 o'clock on both drive-end and fan-end motor housings; some experiments also used the motor supporting base plate. The official overview characterizes these as positions near to and remote from the motor bearings. This supports multi-position vibration classification. The precise sensing-axis orientation and a controlled comparison validating sensor-position choice are not stated. [CWRU-E05, E06, E07]

### Sampling rate, RPM, and record length rationale

Most data were collected at 12 kS/s, with 48 kS/s additionally available for drive-end bearing faults. Fan-end fault data are 12 kS/s. Tests span 0–3 hp and approximately 1720–1797 RPM. The official pages do not state record duration, sample count, or an explicit bandwidth rationale for choosing 12 versus 48 kS/s. [CWRU-E03, E08, E09]

## Sensors and channels

- Vibration positions: drive-end housing, fan-end housing, and base plate in some experiments
- Maximum reported vibration-channel configuration: three
- Every file is documented as containing DE and FE vibration; BA is optional
- Modality: vibration acceleration only
- Triaxial: No
- Simultaneous sampling: Unknown
- Synchronized acquisition: Unknown
- Sensor model and calibrated sensitivity: Unknown
- Acquisition: 16-channel DAT recorder, exact model Unknown

Co-location in one MAT file is evidence of paired records, but it is not sufficient by itself to claim a common ADC sampling instant. [CWRU-E04, E05, E07, E14, E15]

## Operating conditions

- Motor loads: 0, 1, 2, 3 hp
- Approximate motor-speed range: 1720–1797 RPM
- Normal baseline page explicitly lists 1797, 1772, 1750, and 1730 RPM; individual fault tables provide condition-specific approximate speeds
- Radial force, torque, temperature: Unknown

[CWRU-E03]

## Fault conditions and labels

Normal, IR, OR, and ball conditions are provided. Defects are artificial single-point EDM faults introduced separately. The official fault tables do not list cage faults or any same-sample internal-bearing, bearing–rotor, or bearing–gear compound combination. OR defect angular position relative to the load zone is varied at 3, 6, and 12 o'clock; this is a defect-position variable rather than a sensor-position variable. [CWRU-E11, E12, E13]

## Data organization and access

Official pages distribute MATLAB files. Variable-name markers identify drive-end vibration (`DE`), fan-end vibration (`FE`), optional base vibration (`BA`), time series, and RPM. Current license, original release year, record lengths, and full file-level completeness remain Unknown. [CWRU-E14, E16]

## Validation reported by source

The reviewed official documentation carefully enumerates fault location, diameter/depth, bearing geometry and theoretical defect-frequency multipliers. It does not present a dataset-wide physics-validation analysis such as envelope-spectrum verification for every condition. Validation methods therefore remain an empty list in structured facts. [CWRU-E10, E11]

## Known limitations and conflicts

- All documented faults are artificial single-point defects; natural degradation is absent. [CWRU-E02, E11]
- No compound-fault samples are documented. [CWRU-E12]
- Base channel availability depends on the experiment. [CWRU-E05, E14]
- Exact sensor axes, timing architecture, sensor/recorder models, record lengths, calibration, release year, and license remain Unknown. [CWRU-E07, E09, E15, E16]
- Two bearing models are used at different motor ends, but both are deep-groove ball bearings; this is not bearing-type domain shift. [CWRU-E10]

## Evidence coverage

First-pass verification against the official institutional documentation is complete and linked to CWRU-E01–E16. The local PDF/CSV are secondary project summaries and were not used to establish technical facts. Independent file-level verification is still needed only for exact MAT shapes, record duration, optional channel coverage, and timing metadata.
