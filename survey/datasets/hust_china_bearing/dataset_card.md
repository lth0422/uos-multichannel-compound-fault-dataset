# Dataset Card: HUST China Bearing

## Identity

- Dataset ID: hust_china_bearing
- Dataset name: HUSTbearing
- Institution: Huazhong University of Science and Technology
- Release year: 2022 (as listed by the 2024 source)

## Purpose and scope

The available 2024 review/benchmark paper introduces eight open datasets and two self-collected datasets, `HUSTbearing` and `HUSTgearbox`, for domain-generalization experiments. This card covers only HUSTbearing. The paper is an original release/benchmark source but not a dedicated dataset paper. [HUSTC-E01, HUSTC-E02]

## Acquisition setup

Unknown from the locally available main article. The source assigns the detailed dataset and task settings to online Supplementary Appendix B, which is not embedded in the local PDF. [HUSTC-E03, HUSTC-E09]

### Measurement position and mounting rationale

Unknown. Sensor position, direction, mounting, position-selection rationale, and validation are not reported in the main article. [HUSTC-E09]

### Sampling rate, RPM, and record length rationale

Unknown. The main article does not state HUSTbearing sampling rate, RPM/load grid, raw duration, samples per record, bandwidth rationale, or window rationale. These values must not be inferred from other benchmark datasets or algorithm input processing. [HUSTC-E09]

## Sensors and channels

Unknown. The main article does not identify HUSTbearing sensor modality/model/count, channel layout, simultaneous sampling, synchronization, or DAQ. [HUSTC-E09]

## Operating conditions

Table 4 classifies HUSTbearing as having multiple working conditions, but their numeric values and controlled variables are absent from the main article. [HUSTC-E02]

## Fault conditions and labels

Table 4 states that the bearing faults are artificial. Exact health classes, defect components, severities, generation method, and compound-fault status are not stated in the main article. The cross-machine benchmark discusses healthy/IR/OR tasks across selected datasets, but without Supplementary Appendix B it is not safe to attribute every class to HUSTbearing. [HUSTC-E02, HUSTC-E06]

## Data organization and access

The abstract/conclusion says two self-collected datasets were released and provides a GitHub code repository. The Data Availability statement instead says data will be made available on request. The local PDF contains no embedded supplement, manifest, persistent dataset DOI, file schema, or license. Raw availability is therefore Partial pending official supplementary/repository verification. [HUSTC-E04, HUSTC-E05]

## Validation reported by source

The paper benchmarks eight domain-generalization algorithms and reports difficulty on HUSTbearing cross-condition tasks. This validates its use as an algorithm benchmark, not physical fault labels, sensor placement, or signal bandwidth. [HUSTC-E07]

## Known limitations and conflicts

- Detailed Appendix B is not included in the local PDF.
- “Released” statements coexist with “available on request.”
- Acquisition, schema, license, and fault taxonomy are unavailable locally.
- HUSTbearing and HUSTgearbox are separate datasets and must not be merged.
- No conclusion about compound faults, multi-channel acquisition, sampling rate, or duration is currently supportable.

## Evidence coverage

This is an intentionally sparse card. Values requiring supplementary or official repository evidence remain Unknown.
