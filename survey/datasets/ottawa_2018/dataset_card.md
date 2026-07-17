# Dataset Card: Ottawa 2018

## Identity

- Dataset ID: ottawa_2018
- Dataset name: Bearing vibration data under time-varying rotational speed
- Institution: University of Ottawa
- Release year: 2018
- Dataset paper DOI: 10.1016/j.dib.2018.11.019
- Data DOI: 10.17632/v43hmbwxpm

## Purpose and scope

This dataset supports bearing fault diagnosis under speed trajectories that vary within each record. It contains healthy, inner-race, and outer-race states rather than run-to-failure trajectories or compound faults. [OTT18-E01, E05, E09]

## Acquisition setup

A SpectraQuest MFS-PK5M shaft is supported by two ER16K ball bearings. The left bearing remains healthy; the right experimental bearing is replaced according to health condition. One ICP 623C01 accelerometer is placed on the experimental-bearing housing, and one EPC 775 incremental encoder measures shaft speed. [OTT18-E02, E03]

## Sensors and channels

- `Channel_1`: one vibration-acceleration channel
- `Channel_2`: one encoder/speed channel
- DAQ: NI USB-6212 BNC
- Multi-sensor and multi-channel: Yes
- Multi-modal: vibration plus rotational speed
- Multi-position vibration: No
- Accelerometer direction and attachment: Unknown
- Record-level synchronization: Yes
- Simultaneous ADC architecture and skew: Unknown

[OTT18-E03, E10, E11]

## Operating conditions

Four trajectory families are recorded: increasing speed, decreasing speed, increasing then decreasing, and decreasing then increasing. Across the listed records, speed ranges from 9.8 to 29.0 Hz, approximately 588–1,740 RPM. Each trial has its own endpoints, so these are not identical commanded profiles. Applied load and torque are Unknown. [OTT18-E05, E06, E10]

## Sampling rate and record length

Both channels are sampled at 200 kHz for 10 seconds, implying 2,000,000 samples per channel. The paper gives no anti-aliasing, sensor-bandwidth, diagnostic-bandwidth, storage, or frequency-resolution rationale for 200 kHz. [OTT18-E04, E10]

At the minimum and maximum listed speeds, a 10-second record contains approximately 98–290 rotations and has a nominal FFT-bin spacing of 0.1 Hz. These are project calculations, not source claims.

## Fault conditions and labels

The label matrix contains healthy, inner-race fault, and outer-race fault. There are no ball, cage, rotor, gear, or compound labels. The paper does not describe how the IR/OR defects were generated, so artificial-versus-natural status remains Unknown. [OTT18-E07, E09, E10]

## Data organization and access

Three health states × four speed-trajectory families × three trials yield 36 MAT files. Each file contains paired vibration and encoder channels. The article's detailed list repeats `O-C-1`; the second occurrence structurally appears to represent the third trial, but the raw repository must confirm its actual name. [OTT18-E03, E07, E12]

## Validation reported by source

The paper supplies ER16K geometry and characteristic orders: BPFI = 5.43× shaft frequency and BPFO = 3.57× shaft frequency. It does not present record-level order tracking, envelope spectra, fault-frequency agreement, sensor-quality results, or repeatability statistics. [OTT18-E08]

## Known limitations and conflicts

- Only one vibration position and unspecified direction.
- Defect generation, applied load, mounting, and sampling-rate rationale are Unknown. [OTT18-E10]
- Hardware simultaneous sampling/channel skew are Unknown. [OTT18-E11]
- One record label is duplicated in the paper. [OTT18-E12]
- Article CC BY does not independently establish the dataset-file license.
- Trial speed endpoints vary, so trajectory matching across health classes requires careful use of encoder data.

## Evidence coverage

Dedicated-paper extraction is linked to OTT18-E01–E12. Official Mendeley README/license and a repository file listing are needed to resolve label/schema details; the full raw dataset is unnecessary for first-pass design comparison.
