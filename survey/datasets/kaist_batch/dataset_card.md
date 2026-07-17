# Dataset Card: KAIST Batch

## Identity

- Dataset ID: kaist_batch
- Dataset name: KAIST varying-load and varying-speed rotating-machine dataset
- Institution: Korea Advanced Institute of Science and Technology (KAIST)
- Release year: 2023

## Purpose and scope

The dedicated Data in Brief article describes two batch-diagnosis parts: a constant-speed, varying-load multi-modal rotating-machine dataset and a constant-/varying-speed bearing dataset. It is a particularly direct sensor-layout precedent for UOS v2 because vibration is recorded simultaneously at two bearing housings in two orthogonal directions. [KAIB-E01, KAIB-E02]

## Acquisition setup

The testbed comprises a motor, gearbox, torque meter, two bearing housings, rotor disks, and hysteresis brake. Four PCB 352C34 ICP accelerometers feed a Siemens SCADAS Mobile 5PM50. Other modalities use a PCB 378B02 microphone, K-type thermocouples, Hioki CT6700 current sensors, and an Autonics FD-620-10 tachometer. [KAIB-E03, KAIB-E04]

### Measurement position and mounting rationale

Accelerometers are placed in x and y directions on bearing housings A and B, citing ISO 10816-1:1995. The paper explicitly states simultaneous vibration measurement. It does not report a comparison against alternative positions, attachment method, coordinates, surface preparation, remount repeatability, or position-wise observability metrics. [KAIB-E02, KAIB-E11]

### Sampling rate, RPM, and record length rationale

Vibration is sampled at 25.6 kHz. Load-part records use 3010 RPM and 0/2/4 Nm, with 120 seconds for normal and 60 seconds for faults. The speed part uses 600 seconds at constant 3010 RPM or 2100 seconds under 680–2460 RPM, stored as seven 300-second varying-speed files. These are useful precedents, but the paper does not derive 25.6 kHz or these durations from bandwidth, alias margin, frequency resolution, rotation count, or learning-window requirements. [KAIB-E05, KAIB-E06, KAIB-E11]

## Sensors and channels

The four vibration channels are `x_direction_housing_A`, `y_direction_housing_A`, `x_direction_housing_B`, and `y_direction_housing_B`. This is multi-sensor, multi-channel, multi-position, multi-direction vibration within a single modality. The broader dataset is multi-modal because it also includes acoustic, temperature, motor-current, speed, and timestamp data, with modality availability differing by part. [KAIB-E02, KAIB-E03, KAIB-E08]

## Operating conditions

The load part uses 3010 RPM and 0, 2, and 4 Nm. Acoustic records are restricted to zero load to avoid air-cooled-brake noise. The speed part includes constant 3010 RPM and varying 680–2460 RPM at zero load. [KAIB-E05, KAIB-E06]

## Fault conditions and labels

The load part separately labels healthy, seeded inner-race and outer-race cracks, parallel misalignment, and rotor unbalance at multiple severities. The speed part separately labels healthy, inner-race, outer-race, and ball faults created by surface spalling with diamond tips. The paper does not describe any same-sample compound-fault class; coexisting sensor modalities are not compound faults. [KAIB-E07]

## Data organization and access

Load-part vibration/acoustic data are MAT files and temperature/current data are TDMS files. Speed-part vibration, current, and synchronized RPM are CSV. Four Mendeley Data records are linked by the paper. Dataset-file licensing was not independently inspected. [KAIB-E01, KAIB-E08]

## Validation reported by source

The paper supplies seeded-fault photographs and dimensions, bearing characteristic-frequency equations and numerical values for the load part, and representative time series/spectrograms for the speed part. It does not report systematic per-condition envelope-spectrum or characteristic-frequency acceptance tests, cross-channel timing error, or paired single-/multi-channel diagnosis. [KAIB-E09]

## Known limitations and conflicts

- No compound-fault samples are documented.
- Exact accelerometer attachment and channel timing/skew specifications are not reported.
- The Specifications Table appears to reverse NI 9775/NI 9211 roles; the body assigns NI 9211 to temperature and NI 9775 to current.
- Constant- and varying-speed fault-bearing locations differ for some records.
- Sampling-rate and duration selection rationale is not reported.
- Repository schema/license and raw-file consistency remain unverified.

## Evidence coverage

Important structured facts are traced in `evidence.md`. Unknowns remain explicit pending official repository inspection.
