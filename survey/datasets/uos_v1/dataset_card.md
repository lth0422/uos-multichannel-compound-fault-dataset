# Dataset Card: UOS v1

## Identity

- Dataset ID: uos_v1
- Dataset name: UOS v1
- Institution: University of Seoul
- Release year: 2024

## Purpose and scope

Data in Brief dataset article for fault diagnosis under bearing-type domain shifts and compound machine-fault scenarios. It provides raw vibration and STFT spectrogram data across three bearing types, six speeds, and two sampling rates. [UOSV1-E01, E03, E07, E12]

## Acquisition setup

An AST fault simulator with a 40 W BLDC motor, shaft, two rotor disks, and two bearing housings was used. Predefined artificial fault scenarios were collected at 600–1600 RPM. Each MAT record contains 1,280,000 samples: 160 s at 8 kHz or 80 s at 16 kHz. This is a batch dataset, not a run-to-failure dataset. [UOSV1-E02, E03, E06, E11]

### Measurement position and mounting rationale

The reported position is the top of the shaft-end bearing housing, with magnetic-stud mounting. The reviewed paper does not compare alternative sensor positions or provide an explicit rationale validating this location; therefore, the position and mounting are verified facts, while position-selection rationale and validation remain `Unknown`. [UOSV1-E05]

### Sampling rate, RPM, and record length rationale

The verified conditions are 8/16 kHz, six fixed speeds from 600 to 1600 RPM, and 1,280,000 samples per file, corresponding to 160 s at 8 kHz and 80 s at 16 kHz. The paper explains that the two durations produce equal sample counts. It does not establish that these rates, speeds, or durations are optimal for a future UOS v2 design. [UOSV1-E03, E06]

## Sensors and channels

One PCB Piezotronics 333D01 USB digital accelerometer was mounted with a magnetic stud on top of the shaft-end bearing housing. The paper describes the raw signal as uniaxial, so this is a single-sensor, single-modality, single-position, single-channel configuration under the project taxonomy. A separate DAQ is not reported. Multi-channel simultaneous sampling or synchronization is not applicable as an observed feature and is retained as `Unknown` in structured facts. [UOSV1-E04, E05, E15]

## Operating conditions

- Rotating speeds: 600, 800, 1000, 1200, 1400, 1600 RPM
- Sampling rates: 8 and 16 kHz
- Bearing models: 6204, N204, NJ204, 30204
- Bearing types: deep-groove ball, cylindrical roller, tapered roller
- Load, torque, radial-force, and temperature variation: Unknown

[UOSV1-E03, E06, E07]

## Fault conditions and labels

The exhaustive condition definition contains 32 states: one healthy, three single bearing faults (ball/roller, IR, OR), seven single rotating-component faults (looseness; three unbalance severities; three misalignment severities), and 21 compound conditions. Each compound condition combines one bearing fault with one rotating-component fault. Therefore, the dataset contains bearing–rotor/rotating-component compound faults but does not contain internal bearing compound faults such as IR+OR or IR+ball in the same sample. Cage and gear faults are not included. [UOSV1-E08, E09, E10]

## Data organization and access

Data are split across three Mendeley Data repositories:

- Subset 1, deep-groove ball bearing: `10.17632/53vtnjy6c6`
- Subset 2, cylindrical roller bearing: `10.17632/7trwzz77xh`
- Subset 3, tapered roller bearing: `10.17632/2cygy6y4rk`

MAT filenames encode rotating-component condition, bearing condition, sampling rate, bearing model, and speed. Each file contains raw vibration plus spectrogram and STFT axis fields. Repository-level dataset license remains `Unknown` until the official repository metadata is independently checked. [UOSV1-E12, E13, E16]

## Validation reported by source

The authors checked measurement range and invalid values, visually screened noise in raw/frequency-domain signals, verified bearing-fault frequencies with envelope spectra (BPFI, BPFO, BSF), and compared peak/RMS amplitudes of machine-fault and healthy data. [UOSV1-E14]

## Known limitations and conflicts

- All faults are artificial and laboratory-generated; the article notes that external vibration and electromagnetic noise in industrial environments are not fully represented. [UOSV1-E11]
- Only one uniaxial vibration channel and one mounting position are described. [UOSV1-E04, E05]
- Simultaneous multi-channel acquisition and synchronization are not reported because no multi-channel configuration is described. [UOSV1-E15]
- Dataset repository license and software/code availability remain Unknown. [UOSV1-E16]
- Load, torque, radial-force, and temperature variation are not established by the reviewed source.

## Evidence coverage

First-pass extraction from the original dataset paper is complete. Important structured facts are linked to UOSV1-E01–E16. Independent verification against official Mendeley repository metadata is still required, especially for license, exact deposited files, and version information.
