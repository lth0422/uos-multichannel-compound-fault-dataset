# Dataset Card: Ottawa 2023

## Identity

- Dataset ID: ottawa_2023
- Dataset name: UORED-VAFCLS
- Institution: University of Ottawa
- Release year: 2023
- Dataset paper DOI: 10.1016/j.dib.2023.109327
- Data DOI: 10.17632/y2px5tg92h

## Purpose and scope

UORED-VAFCLS supports rolling-element bearing fault diagnosis under nominally constant speed and load using raw and processed vibration/acoustic data plus operating-condition measurements. Twenty bearings are degraded to inner-race, outer-race, ball, or cage endpoints. [OTT23-E01, E02, E05–E07]

## Acquisition setup

A single-phase motor operates at nominal 1,750 RPM. Its drive-end bearing is degreased and replaced after each test to accelerate naturally developing deterioration. A cantilever system applies load. The tested bearing is the motor drive-end bearing; an additional SKF E22206 bearing transfers the applied load and is not the labeled test bearing. [OTT23-E05, E06]

## Sensors and channels

Six sensors generate five stored values:

- PCB 623C01 accelerometer: vibration at the drive-end bearing
- PCB 130F20 microphone: within 2 cm of that bearing
- OMEGA LCM302 load cell
- OMEGA OMDC-MPU-A hall-effect speed sensor
- Two OMEGA KTSS-HH thermocouples: bearing and room temperatures combined as temperature differential

The raw file is multi-sensor, multi-modal, and multi-channel, but it contains only one vibration channel and is not multi-position vibration. Values share a record, while hardware simultaneity and skew remain Unknown. [OTT23-E02, E10, E11, E14]

## Measurement position and mounting rationale

The accelerometer is magnetically mounted directly on the tested bearing inside an altered motor casing. The authors tested inside versus outside casing placement and selected the inside location because it reportedly reduced noise without electromagnetic-field problems. This is a useful empirical placement rationale, although quantitative comparison metrics are not reported. [OTT23-E10]

## Sampling rate and record length rationale

Each recording contains 420,000 samples per stored channel at 42 kHz for 10 seconds. The source explicitly selects 20 kHz as the highest frequency of interest based on acoustic audible range, then uses 42 kHz based on Nyquist and DAQ capability. Ten seconds is chosen to provide many samples for deep-learning use. [OTT23-E03, E04]

At 1,750 RPM, 10 seconds spans approximately 292 rotations and provides 0.1 Hz nominal FFT-bin spacing. These are project calculations, not source claims. The rate/duration rationale is documented, but it emphasizes audible bandwidth and sample volume rather than bearing characteristic frequencies or an on-device window.

## Operating conditions

- Nominal speed: 1,750 RPM
- Healthy, inner-race, outer-race, cage: 400 N
- Ball fault: 0 N
- NSK 6203ZZ: first five tests/inner-race group
- FAFNIR 203KD: subsequent 15 tests/outer-race, ball, and cage groups

The dataset title says constant load and speed, but load is not constant across all fault classes. Bearing model and load are also coupled to fault labels. [OTT23-E05, E08, E09]

## Fault conditions and labels

The four final fault classes are inner race, outer race, ball, and cage, with five bearings per class. Labels distinguish healthy (`0`), developing (`1`), and faulty (`2`) stages. No simultaneous multi-element or bearing–rotor compound condition is documented. [OTT23-E06, E07]

Table 1 repeats `B-12-1` in the faulty-ball row, inconsistent with its own suffix scheme; raw repository labels are needed to confirm whether this is only a paper typo. [OTT23-E13]

## Data organization and access

The paper reports 60 released raw sets: 20 healthy plus developing/faulty sets for four fault types across five bearings. Each is selected from a pool of about 50 time-ordered files collected during deterioration, so the released collection samples three stages rather than exposing every full trajectory. Raw formats include MAT/XLSX/CSV, and processed 512×512 PNG spectrograms plus processing code are provided. [OTT23-E01, E03, E06]

## Validation reported by source

The source reports visual fault identification and FFT review of candidate files. It illustrates a possible outer-race signature and provides spectrograms, but does not give systematic envelope spectra, calculated fault-frequency agreement, cross-channel timing tests, or repeatability statistics for all bearings. [OTT23-E12]

## Known limitations and conflicts

- Bearing model is coupled with fault class. [OTT23-E08]
- Ball fault is coupled with zero load while other classes use 400 N. [OTT23-E09]
- Only one vibration position/direction is recorded; direction is not specified.
- Released data represent selected lifecycle stages, not all collected files. [OTT23-E06]
- One Table 1 label is inconsistent. [OTT23-E13]
- ADC simultaneity and channel skew are Unknown. [OTT23-E14]
- Article CC BY does not by itself establish the Mendeley dataset-file license.

## Evidence coverage

Dedicated-paper extraction is linked to OTT23-E01–E14. Official Mendeley metadata/README, dataset license, repository label listing, and raw schema remain the next verification targets; full raw download is not required.
