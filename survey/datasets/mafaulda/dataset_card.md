# Dataset Card: MAFAULDA

## Identity

- Dataset ID: mafaulda
- Dataset name: MAFAULDA Machinery Fault Database
- Institution: COPPE/Poli/UFRJ
- Release year: 2016 original publication; current web-deposit version date Unknown

## Purpose and scope

Official documentation describes 1,951 finite multivariate recordings from a SpectraQuest Alignment/Balance Vibration Trainer. Conditions include normal operation, imbalance, horizontal and vertical parallel misalignment, and defective bearings at two positions. [MAF-E01]

## Acquisition setup

The stand has a DC motor, shaft, rotor, and two bearing positions. One bearing is between motor and rotor (underhang); the other is outside the rotor (overhang). Both positions are represented by axial, radial, and tangential acceleration channels. The documentation does not provide a comparative experiment establishing that these are optimal positions. [MAF-E01, E02, E07]

## Sensors and channels

- Three IMI Sensors 601A01 uniaxial accelerometers
- One IMI Sensors 604B31 triaxial accelerometer
- One Monarch Instrument MT-190 analog tachometer
- One Shure SM81 microphone
- Two NI-9234 four-channel acquisition modules; chassis Unknown
- Eight recorded columns: tachometer 1 + acceleration 6 + microphone 1

This is multi-sensor, multi-channel, multi-position, multi-direction, triaxial, and multi-modal. It must not be described as eight vibration channels. Signals share a multivariate record, but inter-module hardware timing is not documented. [MAF-E02, E03, E10]

## Operating conditions

Records are sampled at 50 kHz for 5 seconds, giving 250,000 samples per channel. Normal data span 737–3,686 RPM in approximately 60 RPM steps; fault cases generally reuse this range, with reduced attainable maximum speed under strong vibration. The documentation supplies conditions but not a bandwidth, frequency-resolution, minimum-rotation, or channel-ablation rationale. [MAF-E04, E05]

## Fault conditions and labels

Imbalance severity is controlled using added masses, and horizontal/vertical parallel misalignment uses stated displacement levels. Defective bearing elements are installed one at a time at underhang or overhang positions. Bearing cases with nonzero added mass simultaneously contain a bearing defect and imbalance, meeting this repository's bearing–rotor compound definition. No internal bearing compound defect is documented. [MAF-E06, E07, E08]

The official page is internally inconsistent: its summary labels bearing groups as cage/outer/ball, while the detailed section describes outer/rolling-element/inner. The 2016 original paper repeatedly specifies cage, outer-race, and ball faults at both bearing positions, resolving the intended classes in favor of cage/outer/ball. [MAF-E09, E13]

## Data organization and access

The official page offers complete and category-specific ZIP/TGZ downloads. Each current recording is described as an eight-column CSV. The original paper analyzed a seven-channel form containing six acceleration signals and one trigger, while current documentation adds a microphone column. No raw files were downloaded for this survey pass. File naming, numeric precision, timestamp representation, and exact label metadata remain unverified. [MAF-E02, E11, E14]

## Validation reported by source

The paper estimates rotational frequency and uses amplitudes at 1×, 2×, and 3× rotational frequency plus kurtosis and entropy. It reports a controlled feature-level comparison using one versus two bearing sensor sets: 81.2% versus 90.1%, and 94.8% versus 99.1% when both variants include kurtosis/entropy. These results apply to the reported feature/ANN experiments and do not prove universal multichannel superiority. Bearing-characteristic-frequency, envelope-spectrum, cross-channel timing, and repeatability validation are not reported. [MAF-E15, E16]

## Known limitations and conflicts

- The 2016 source introduces the database but is an application/method paper, not a dedicated dataset paper.
- Current deposit version date and data license are Unknown.
- Bearing class names conflict within the official page; the original paper supports cage/outer/ball. [MAF-E09, E13]
- The original paper's seven-channel study and current eight-column documentation differ. [MAF-E14]
- Sensor mounting, microphone position, NI chassis, clock routing, and inter-module skew are Unknown. [MAF-E10]
- Raw file schema and labels have not yet been independently inspected.

## Evidence coverage

Original-paper and official-documentation extraction is linked to MAF-E01–E16. Independent verification still requires official license/version metadata and, only if later needed, raw folder names or a small representative file obtained without retaining the full archive.
