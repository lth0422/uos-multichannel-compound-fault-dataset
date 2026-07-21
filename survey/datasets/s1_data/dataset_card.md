# Dataset Card: S1 Data

## Identity

- Dataset ID: `s1_data`
- Dataset name: S1 Data — Original diagnosis signal at 2000 rpm
- Institution: Harbin University of Science and Technology and collaborating institutions
- Release year: 2024
- Primary source: S1-S01

## Purpose and scope

The PLOS ONE article studies vibration responses of compound rolling-bearing faults under gearbox, shaft-installation, and random-noise interference. Its supporting information releases the experimental signals as `S1 Data`. This is an application/research article with supporting data, not a dedicated dataset paper. [S1-E01, S1-E02]

## Acquisition setup

The rig contains a variable-frequency motor, support bearings, a tested bearing, radial loading, a coupling, and a planetary gearbox. The tested bearing is an SKF 6205 deep-groove ball bearing near the gearbox. Inner-race, outer-race, and rolling-element pitting defects are produced by laser cauterization. [S1-E03, S1-E04]

### Measurement position and mounting rationale

The article names three vibration measurement locations: the support-bearing housing, faulty-bearing housing surface, and gearbox casing. Fig. 9 labels one acceleration sensor at each bearing location and one three-way acceleration sensor on the gearbox, supporting five vibration axes in total. Sensor models, the two uniaxial sensitive directions, triaxial coordinate labels, attachment, and synchronized channel mapping are not stated. [S1-E05, S1-E13]

### Sampling rate, RPM, and record length rationale

Signals are sampled at 12 kHz. Each fault type has 20 groups of 12,000 points, implying one second per group. The experiment uses 2,000 RPM. The article reports these settings but does not establish them as generally optimal. [S1-E06, S1-E07]

## Sensors and channels

Fig. 9 supports two uniaxial acceleration sensors plus one three-way accelerometer, for five vibration axes at three positions. Exact models, axes, and timing architecture are Unknown. [S1-E05, S1-E13]

## Operating conditions

The verified operating speed is 2,000 RPM. Gear-meshing, shaft/coupling installation, centrifugal, and random-noise components are studied as interference factors; they are not separately introduced fault labels. Radial load magnitude and other operating-condition levels are Unknown. [S1-E07, S1-E09]

## Fault conditions and labels

The experimental analysis covers all three pairwise internal combinations—IR+OR, IR+rolling element, OR+rolling element—and the triple IR+OR+rolling-element combination. These are artificial same-bearing compound faults. The reviewed article does not document matched healthy and pure single-fault records as released S1 groups. [S1-E04, S1-E08]

## Data organization and access

The article states that every compound-fault type contains 20 groups and each group has 12,000 samples. Supporting information identifies `S1 Data. Original diagnosis signal at 2000 rpm (ZIP)`. The internal archive schema and file format were not available inside the local PDF and remain Unknown. [S1-E06, S1-E11]

## Validation reported by source

The paper calculates shaft, cage, inner-race, outer-race, rolling-element, and gear-meshing frequencies from documented geometry. It presents time signals and envelope spectra for the four compound-fault combinations, including cases with interference where expected components become weak or unidentifiable. [S1-E07, S1-E10]

## Known limitations and conflicts

- The five vibration axes are supported by Fig. 9, but exact sensor models, axis definitions, mounting, DAQ, and channel simultaneity are Unknown. [S1-E05, S1-E13]
- Matched healthy and pure single-fault release groups are not documented. [S1-E08]
- Only one verified RPM is used and each group is approximately one second. [S1-E06, S1-E07]
- The supporting ZIP's internal files and license terms require official-supplement inspection. [S1-E11, S1-E12]

## Evidence coverage

The local original paper supports the rig, five-axis layout, compound matrix, sampling, RPM, group count, and physics analysis. Official supporting-archive inspection is still required for stored column schema, file organization, metadata, and exact reuse terms.
