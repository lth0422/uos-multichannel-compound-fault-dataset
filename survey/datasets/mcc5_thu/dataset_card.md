# Dataset Card: MCC5-THU

## Identity

- Dataset ID: `mcc5_thu`
- Dataset name: MCC5-THU Multi-mode Fault Diagnosis Datasets of Gearbox Under Variable Working Conditions
- Institution: MCC5 Group Shanghai and Tsinghua University
- Release year: 2024
- Primary source: MCC5-S01

## Purpose and scope

This dedicated Data in Brief article releases gearbox-condition data under steady and time-varying speed/load modes. It covers healthy, single gear faults, and two same-sample bearing–gear compound faults at multiple severity levels. [MCC5-E01, MCC5-E02]

## Acquisition setup

The rig contains a 2.2 kW three-phase motor, torque sensor, two-stage parallel gearbox, magnetic-powder brake, speed sensor, and measurement/control system. The faulty gear is a 36-tooth intermediate-shaft gear; the adjacent faulty bearing is an ER16K ball bearing. Faults are laser etched with 0.01 mm machining accuracy. [MCC5-E03, MCC5-E07, MCC5-E08]

### Measurement position and mounting rationale

Two TES001V triaxial accelerometers measure the motor drive end and the gearbox intermediate-shaft bearing seat in axial, horizontal, and vertical directions. The locations span the drive motor and the faulty gear/bearing neighborhood. Exact attachment method and a measured position-selection comparison are not reported. [MCC5-E04, MCC5-E15]

### Sampling rate, RPM, and record length rationale

All released records use 12.8 kHz and 60 seconds. Time-varying-speed tests use fixed 10 or 20 Nm loads; time-varying-load tests use fixed 1,000, 2,000, or 3,000 RPM. The set curves also include transient speed levels such as 2,500 RPM. Actual speed and torque are measured because actuator hysteresis can make actual trajectories differ from commands. [MCC5-E06, MCC5-E10]

## Sensors and channels

Each CSV contains eight columns: speed key-phase, torque, three motor acceleration axes, and three gearbox-bearing-seat acceleration axes. This is six vibration channels at two positions plus two operating-condition channels. Common rows support synchronized records, but ADC simultaneity, common clock, channel skew, and DAQ identity are not established. [MCC5-E04, MCC5-E05]

## Operating conditions

The paper reports 12 working-condition curve families, 24 steady conditions, and either 48 or 112 transitional combinations in different parts of the article. Fixed-speed values are 1,000, 2,000, and 3,000 RPM; fixed-load values are 10 and 20 Nm, with corresponding time-varying speed/load curves. [MCC5-E10, MCC5-E11]

## Fault conditions and labels

Single gear faults are missing tooth, wear, pitting, root crack, and broken tooth. Compound classes combine broken tooth with bearing inner-race damage or bearing outer-race damage in the same condition. Wear, pitting, crack, break, and both compound classes have light, medium, and high severities. This is bearing–gear compound data, not internal-bearing or bearing–rotor compound data. [MCC5-E08, MCC5-E09, MCC5-E14]

## Data organization and access

The release contains 240 CSV files. Each 60-second record has eight named columns and no explicit timestamp column. The paper links Mendeley Data DOI 10.17632/p92gj2732w.1. [MCC5-E02, MCC5-E06, MCC5-E12]

## Validation reported by source

For a missing-tooth example, the paper identifies intermediate-shaft rotational frequency, gear-meshing frequency, and sidebands in the gearbox z-axis envelope spectrum. It also documents actual speed and torque sensing. It does not report an equivalent condition-by-condition physical validation for every fault and severity. [MCC5-E10, MCC5-E13]

## Known limitations and conflicts

- Table 1 reports 48 transitional conditions, whereas Section 3 reports 112 transitional combinations. [MCC5-E11]
- Exact accelerometer attachment, DAQ model, ADC architecture, and channel skew are Unknown. [MCC5-E05, MCC5-E15]
- The paper does not report paired single-/multi-channel diagnostic experiments. [MCC5-E15]
- Physical spectral validation is shown for a missing-tooth example, not every compound condition. [MCC5-E13]
- Dataset-file license must be confirmed separately from the CC BY article. [MCC5-E02]

## Evidence coverage

The original dedicated paper provides strong evidence for the released schema, six vibration channels, speed/load trajectories, fault/severity design, and bearing–gear compounds. Official raw repository metadata and representative file inspection remain required for licensing, exact row counts, filenames, and signal alignment.
