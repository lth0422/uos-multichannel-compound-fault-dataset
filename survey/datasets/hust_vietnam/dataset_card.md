# Dataset Card: HUST Vietnam

## Identity

- Dataset ID: hust_vietnam
- Dataset name: HUST bearing
- Institution: Hanoi University of Science and Technology
- Release year: 2023

## Purpose and scope

This dedicated BMC Research Notes Data Note introduces a vibration dataset spanning five ball-bearing models, three loads, three single defects, and three pairwise internal-bearing compound defects. Its stated motivation is bearing-type diversity and practical diagnosis. [HUSTV-E01, HUSTV-E02]

## Acquisition setup

A 750 W induction motor drives a multi-step shaft and Leroy Somer powder brake. Replaceable housings accommodate the test bearings; torque and speed are monitored. One PCB 325C33 accelerometer connects to an NI-9234 in an NI CompactDAQ chassis controlled by LabVIEW. The chassis model and exact accelerometer attachment are not reported. [HUSTV-E03, HUSTV-E04]

### Measurement position and mounting rationale

The paper states that one accelerometer is installed vertically “on the bearing” after describing replaceable bearing housings. It does not establish whether this means the bearing outer ring or housing surface, nor give attachment method, coordinates, load-direction relation, alternative-position comparison, or remount validation. This is single-position, single-direction vibration rather than multi-position acquisition. [HUSTV-E03, HUSTV-E10]

### Sampling rate, RPM, and record length rationale

Each steady vibration signal is sampled at 51.2 kHz for 10 seconds. Run-up vibration is provided for 5 seconds. The paper says the high rate captures detailed signal changes, but does not derive it from sensor bandwidth, characteristic frequencies, envelope band, anti-alias margin, or NI-9234 filter behavior. Exact steady RPM and the run-up RPM range are stored in data fields but not numerically reported in the article. [HUSTV-E05, HUSTV-E06]

## Sensors and channels

One vertical PCB 325C33 acceleration channel is reported. Shaft frequency and run-up RPM are included as metadata/fields, but the paper does not describe a synchronized tachometer waveform channel. The dataset is therefore not verified as multi-channel or multi-position vibration. [HUSTV-E03, HUSTV-E07]

## Operating conditions

The dataset covers nominal load settings of 0 W, 200 W, and 400 W. Exact torque, steady RPM, run-up range, and temperature are Unknown from the article. [HUSTV-E02, HUSTV-E06]

## Fault conditions and labels

Wire cutting creates nominal 0.2 mm-wide artificial cracks. Labels include healthy, IR, OR, Ball, IR+OR, IR+Ball, and OR+Ball across bearing models 6204–6208. Ball and IR+Ball are missing for model 6204. Crack depth is not controlled consistently across bearings, and no triple compound condition is provided. [HUSTV-E02, HUSTV-E08, HUSTV-E09]

## Data organization and access

MAT files are deposited at Mendeley Data DOI 10.17632/cbv7jyx4p9. The article describes fields including `data`, `fs`, `rpm`, `ru`, and `ru_raw`. Repository-level file counts, field shapes, units, version, and license were not independently inspected. [HUSTV-E01, HUSTV-E07]

## Validation reported by source

The source documents the wire-cutting method, nominal crack width, bearing geometries, and defect images in the repository. It does not report characteristic-frequency, envelope-spectrum, cross-bearing normalization, or label-acceptance validation. [HUSTV-E08, HUSTV-E11]

## Known limitations and conflicts

- 6204 lacks Ball and IR+Ball cases.
- Crack depth differs across bearings, producing large amplitude differences.
- Environmental noise and mechanical imperfections are not represented.
- The abstract reports 99 raw vibration signals, while the body describes 30 bearings × three loads plus run-up fields; repository inspection is needed to reconcile the count.
- Exact RPM values, mounting method, chassis model, timing architecture, and dataset-file license remain Unknown.

## Evidence coverage

Important facts are mapped to `evidence.md`. Repository-dependent values remain Unknown.
