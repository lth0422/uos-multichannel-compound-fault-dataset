# Dataset Card: XJTU-SY

## Identity

- Dataset ID: xjtu_sy
- Dataset name: XJTU-SY Bearing Datasets
- Institution: Xi'an Jiaotong University and Changxing Sumyoung Technology Co., Ltd.
- Dataset release year: Unknown
- Cited paper: IEEE Transactions on Reliability, online 2018 and issue 2020

## Purpose and scope

XJTU-SY provides complete accelerated run-to-failure vibration data for 15 rolling-element bearings, intended for bearing prognostics and RUL validation. It is not a seeded-fault batch classification dataset. [XJTU-E01, E02, E06]

## Acquisition setup

Fifteen LDK UER204 bearings are tested in groups of five under three radial-load and fixed-speed conditions. Two PCB 352C33 accelerometers are placed at 90 degrees on the same tested-bearing housing. The test continues through degradation until a safety threshold is exceeded. [XJTU-E02, E03, E07]

### Measurement-position rationale

The horizontal and vertical channels are directions at one bearing housing, not two measurement positions. Because hydraulic radial load is applied horizontally, the paper states that the horizontal channel captures more degradation information and selects it for RUL estimation. This supplies a physical direction-selection rationale, though it is not a controlled channel-ablation result. [XJTU-E03, E05]

## Sensors and channels

- Two PCB 352C33 accelerometers
- Position: tested-bearing housing
- Directions: horizontal and vertical, separated by 90 degrees
- Modality: vibration acceleration
- Synchronized paired records: Yes at record level
- Simultaneous ADC sampling and channel skew: Unknown
- DAQ and mounting attachment method: Unknown

[XJTU-E03, E11]

## Operating conditions

| Condition | Speed | Radial force | Bearings |
|---|---:|---:|---:|
| 1 | 2,100 RPM | 12 kN | 5 |
| 2 | 2,250 RPM | 11 kN | 5 |
| 3 | 2,400 RPM | 10 kN | 5 |

Speed is fixed within each run. Thus the collection varies speed across conditions but is not documented as a continuously variable-speed experiment. [XJTU-E02, E08]

## Sampling and temporal organization

Each snapshot contains 32,768 samples per channel at 25.6 kHz, giving 1.28 seconds. A snapshot is recorded every minute throughout each bearing life. The paper does not explain the diagnostic-bandwidth or 1.28-second selection rationale. [XJTU-E04]

At the three speeds, a 1.28-second snapshot contains approximately 44.8, 48, and 51.2 shaft rotations. This calculation is an interpretation from verified settings and may help define a minimum rotation-count criterion for UOS v2; it is not a source claim.

## Fault conditions and labels

Damage develops during accelerated operation rather than through installation of a pre-seeded defect. The paper illustrates inner-race wear, outer-race wear, and outer-race fracture as examples of varied endpoint failures. It does not provide enough bearing-by-bearing evidence to classify any sample as an internal compound fault. Rotor and gear faults are not introduced. [XJTU-E06, E09, E10]

## Data organization and access

The official README describes 15 complete run-to-failure datasets and provides multiple download mirrors. File format, raw schema, filenames, timestamp representation, exact per-bearing endpoint labels, license, and official GitHub URL remain Unknown because no raw files or repository URL were supplied. [XJTU-E01, E10, E11]

## Validation reported by source

The paper shows full-life vibration evolution, endpoint bearing photographs, and a safety-based failure threshold of vibration amplitude above 20 g. Its primary validation target is RUL prediction, not physics-based bearing-fault verification. It does not report envelope spectra, bearing characteristic-frequency validation, channel timing, or repeatability analysis. [XJTU-E06, E07]

## Known limitations and conflicts

- Dataset release/version date and license are Unknown.
- DAQ, exact mounting, hardware simultaneous-sampling, and channel skew are Unknown. [XJTU-E11]
- File structure and final fault labels have not been inspected.
- Final internal compound-fault status is Unknown. [XJTU-E10]
- Load and speed are coupled across only three conditions, so their individual effects cannot be separated from this matrix alone. [XJTU-E02]

## Evidence coverage

Original-paper and supplied official-README extraction is linked to XJTU-E01–E11. A saved README or exact official GitHub URL and license are the next priorities; the full raw dataset is not required for the present sampling-rate and record-length comparison.
