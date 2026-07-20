# Dataset Card: HUST China Bearing

## Identity

- Dataset ID: hust_china_bearing
- Dataset name: HUSTbearing
- Institution: Huazhong University of Science and Technology
- Release year: 2022 (as listed by the 2024 source)

## Purpose and scope

The available 2024 review/benchmark paper introduces eight open datasets and two self-collected datasets, `HUSTbearing` and `HUSTgearbox`, for domain-generalization experiments. This card covers only HUSTbearing. The paper is an original release/benchmark source but not a dedicated dataset paper. [HUSTC-E01, HUSTC-E02]

## Acquisition setup

The official HUSTbearing GitHub README identifies a SpectraQuest Mechanical Fault Simulator with speed control, motor, shaft, acceleration sensor, bearing, and data acquisition board. The exact accelerometer model/count, DAQ model, axis count, mounting, and channel schema remain Unknown because the README describes components generically and the raw Excel files were not downloaded. [HUSTC-E03, HUSTC-E09, HUSTC-E10]

### Measurement position and mounting rationale

Unknown. The official README shows an acceleration sensor near the bearing in the rig schematic, but exact sensor position, direction, mounting, position-selection rationale, and validation are not reported in text. [HUSTC-E09, HUSTC-E10]

### Sampling rate, RPM, and record length rationale

The official HUSTbearing GitHub README reports 25.6 kHz sampling and 262,144 points per sampling, approximately 10.2 s. It lists ten constant-speed operating conditions at 20, 25, 30, 35, 40, 60, 65, 70, 75, and 80 Hz, plus one time-varying 0-40-0 Hz condition. The README warns that the second column in raw files represents speed but is redundant for constant-speed records; correct speed should be taken from filenames. No bandwidth, anti-aliasing, frequency-resolution, rotation-count, or window-selection rationale is reported. [HUSTC-E09, HUSTC-E11, HUSTC-E12]

## Sensors and channels

The official README establishes vibration/acceleration data from an acceleration sensor, but model, count, axis directions, simultaneous sampling, synchronization, and DAQ model remain Unknown. [HUSTC-E09, HUSTC-E10]

## Operating conditions

HUSTbearing has 11 operating conditions: ten constant-speed conditions at 20-80 Hz and one 0-40-0 Hz time-varying speed condition. Converted to shaft speed, the constant-speed set is approximately 1200, 1500, 1800, 2100, 2400, 3600, 3900, 4200, 4500, and 4800 RPM. The 0-40-0 Hz condition corresponds to approximately 0-2400-0 RPM if the listed Hz is shaft rotational frequency. [HUSTC-E02, HUSTC-E11]

## Fault conditions and labels

The official README lists nine health states: normal, medium/severe inner-race fault, medium/severe outer-race fault, medium/severe ball fault, and medium/severe combination fault. It states that combination fault denotes both inner-race and outer-race faults and that all faults are artificially preset. Reported defect sizes are 0.15/0.3 mm for inner/outer race medium/severe faults and 0.25/0.5 mm for ball medium/severe faults. No IR+ball, OR+ball, triple internal compound, rotor, or gear fault is reported. [HUSTC-E10, HUSTC-E13]

## Data organization and access

The official HUSTbearing repository links Quark and Google Drive data locations and states that raw data comprise 99 Excel files, equal to 9 health states times 11 working conditions. Filenames encode fault class/severity and operating condition, for example `0.5X_B_65Hz`. Repository license and raw Excel schema still require verification; raw data were not downloaded for this update. [HUSTC-E04, HUSTC-E05, HUSTC-E14]

## Validation reported by source

The paper benchmarks eight domain-generalization algorithms and reports difficulty on HUSTbearing cross-condition tasks. This validates its use as an algorithm benchmark, not physical fault labels, sensor placement, or signal bandwidth. [HUSTC-E07]

## Known limitations and conflicts

- Detailed Appendix B is not included in the local PDF.
- The paper's “available on request” statement conflicts with the public HUSTbearing GitHub data links.
- Exact sensor model/count, DAQ model, mounting, channel schema, and license remain Unknown.
- HUSTbearing and HUSTgearbox are separate datasets and must not be merged.
- Only IR+OR internal compound is documented; IR+ball, OR+ball, and IR+OR+ball are not reported.
- The README text says “4 different operating conditions” but lists 11 conditions and elsewhere says 11. This is treated as a README typo.

## Evidence coverage

First-pass extraction now uses both the 2024 benchmark paper and the official HUSTbearing GitHub README. Values requiring raw Excel inspection, Supplementary Appendix B, or hardware documentation remain Unknown.
