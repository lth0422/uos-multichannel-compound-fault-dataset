# Dataset Card: NASA IMS

## Identity

- Dataset ID: nasa_ims
- Dataset name: IMS Bearings / NASA IMS
- Data provider: NSF I/UCR Center for Intelligent Maintenance Systems, University of Cincinnati, with Rexnord support
- Current host: NASA Prognostics Center of Excellence/Open Data
- Acquisition period: 2003–2004
- Original paper: Journal of Sound and Vibration 289 (2006), DOI 10.1016/j.jsv.2005.03.007

## Purpose and scope

The released package contains three natural run-to-failure experiments for bearings operated beyond design life. It supports degradation diagnostics and prognostics rather than controlled seeded-fault classification. [IMS-E01, E08]

## Acquisition setup

Four Rexnord ZA-2115 double-row bearings are installed on a common shaft driven at 2,000 RPM. A spring mechanism applies 6,000 lb radial load, and the bearings are force lubricated. PCB 353B33 ICP accelerometers measure vibration on all four bearing housings using an NI DAQCard-6062E. [IMS-E02, E03]

## Sensors and channels

- Set 1: four bearing positions × x/y directions = 8 vibration channels
- Sets 2 and 3: four bearing positions × one direction = 4 vibration channels
- Multi-sensor, multi-channel, and multi-position: Yes
- Multi-direction: Set 1 Yes; Sets 2–3 one direction per position, direction Unknown
- Synchronized acquisition: Yes at common-record level
- Hardware simultaneous sampling and channel skew: Unknown
- Mounting attachment method: Unknown

[IMS-E03, E04, E12]

## Operating conditions

- Speed: constant 2,000 RPM
- Radial load: 6,000 lb
- Lubrication: forced lubrication
- Variable-speed operation: No

[IMS-E02]

## Sampling and temporal organization

Each file contains 20,480 samples per channel at 20 kHz. The README nevertheless calls it a one-second snapshot; the sample arithmetic gives 1.024 seconds. Both are preserved as a source conflict rather than silently rounded. [IMS-E05]

The released README reports 10-minute intervals for Sets 2 and 3 and most of Set 1, with Set 1's first 43 files at five-minute intervals. The original paper describes 20-minute collection for its experiment. This likely reflects documentation or release-version differences, but the cause is unverified. [IMS-E06]

At 2,000 RPM, the numeric 1.024-second record spans about 34.1 shaft rotations and has a nominal FFT-bin spacing of about 0.977 Hz. These are project calculations from verified acquisition values, not source claims.

## Fault conditions and labels

The damage develops through extended operation rather than being seeded before collection. Set 1 endpoint inspection found inner-race damage on bearing 3 and simultaneous roller-element plus outer-race damage on bearing 4. The latter is a verified internal bearing compound fault under this repository taxonomy. Sets 2 and 3 end with outer-race failures on bearings 1 and 3, respectively. No rotor or gear fault is introduced. [IMS-E08, E09, E10]

The compound condition is a naturally developed endpoint state, not a controlled IR/OR/ball combination matrix with independently selected severity.

## Data organization and access

The released sets contain 2,156, 984, and 4,448 timestamp-named ASCII files. Set 1 has eight columns; Sets 2 and 3 have four. Larger timestamp gaps can denote continuation on a later working day. NASA currently hosts a public `IMS.zip` catalog resource. [IMS-E07]

## Validation reported by source

The original paper includes component teardown photographs, full-life RMS/kurtosis trajectories, and wavelet-filter analysis. For bearing 4 it reports a detected periodic component near 230 Hz against calculated BPFO 236.4 Hz. This is meaningful physics-related validation, although it is not a systematic validation of every channel and endpoint. [IMS-E09, E11]

## Known limitations and conflicts

- “One second” conflicts with 20,480 samples at 20 kHz. [IMS-E05]
- Released cadence conflicts with the original paper's 20-minute statement. [IMS-E06]
- Set 1 and Sets 2–3 have different directional coverage. [IMS-E04]
- DAQ simultaneity, clock/skew, and mounting method are Unknown. [IMS-E12]
- NASA catalog licensing guidance may not automatically determine rights for IMS-origin files. [IMS-E13]
- The natural compound endpoint is not a controlled compound-fault design.

## Evidence coverage

Official README, original paper, supplied NASA catalog metadata, and user overview are linked to IMS-E01–E13. The full raw archive is unnecessary for the present survey. If exact cadence/schema verification becomes important, a central-directory listing and one representative file per set would suffice.
