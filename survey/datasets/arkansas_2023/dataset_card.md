# Dataset Card: University of Arkansas 2023

## Identity

- Dataset ID: arkansas_2023
- Dataset name: University of Arkansas 2023
- Institution: University of Arkansas
- Release year: 2023

## Purpose and scope

Data in Brief dataset created to support machine-learning classification of single and simultaneous double faults in a rotary-machine simulator. It contains multi-position, multi-direction vibration data from known bearing and bent-shaft faults under three speed conditions. [ARK23-E01, E02, E03, E08, E10]

## Acquisition setup

A SpectraQuest machinery fault simulator contains a DC motor, a shaft supported by two bearings, two weighted disks, and a belt-driven gearbox. Known faulty components replace nominal components. Double-fault samples are produced by installing two known faulty components simultaneously, so “double fault” is not merely a merged class assembled after collection. [ARK23-E02, E10]

### Measurement position and mounting rationale

Eight accelerometers cover the motor, both bearing housings, and gearbox. The raw headers identify Motor, Bearing 1 X/Y/Z, Bearing 2 X/Y/Z, and one Gearbox channel. This is multi-sensor, multi-channel, multi-position, and multi-direction within one vibration modality. Fig. 3 labels the bearing axes, but the paper does not state stud/magnetic/adhesive mounting or experimentally justify why these positions are optimal. The article's “two directions on gearbox” wording conflicts with the deposited headers. [ARK23-E03, E04, E06, E21]

Three perpendicular uniaxial accelerometers are not classified as one triaxial accelerometer under this repository taxonomy.

### Sampling rate, RPM, and record length rationale

The verified rate is 6.4 kHz for 10 seconds, producing 64,000 points per scenario recording. The article does not print the numeric speeds, but official Figshare metadata identifies them as 25, 50, and 75 RPM. No diagnostic-bandwidth, anti-aliasing, minimum-rotation, or frequency-resolution rationale is reported. These conditions are therefore comparative evidence, not defaults for UOS v2. [ARK23-E07, E08, E18, E23]

## Sensors and channels

- Sensor: eight PCB Piezotronics 608A11 ICP piezoelectric accelerometers
- Bearing 1 housing: x, y, z
- Bearing 2 housing: x, y, z
- Motor: one acceleration channel, direction Unknown
- Gearbox housing: one deposited acceleration channel, direction Unknown; article says two directions
- DAQ: NI CompactDAQ with DAQmx; chassis and input-module models Unknown
- Simultaneous sampling: Unknown
- Synchronized acquisition: Yes at record/timestamp level
- Mounting method: Unknown

The paper writes an accelerometer “accuracy of 102mg/V”; the intended quantity/unit should be verified rather than silently converted to sensitivity. [ARK23-E04, E05, E06]

## Operating conditions

- Three fixed shaft speeds: 25, 50, and 75 RPM
- Load, radial force, torque, and temperature conditions: Unknown
- Acquisition begins after reaching the desired steady RPM

[ARK23-E08, E23]

## Fault conditions and labels

The faulty bearing inventory includes IR, OR, ball, and a combined ball-and-raceway defect. Shaft faults are a central bend and a bend near the motor coupling. Permitted pairs of faulty components are installed simultaneously. Therefore, the dataset includes internal-bearing compound faults and bearing–rotor compound faults. It also permits compound cases across bearing locations. It does not report cage or gear faults. The exact raceway involved in the combined ball-and-raceway bearing is Unknown. [ARK23-E09, E10, E11, E12, E13]

## Data organization and access

The raw archive resolves much of the paper's ambiguity: the 25, 50, and 75 RPM groups each contain 975 CSV files, exactly 39 scenarios × 25 trials, for 2,925 trial files. All headers were inspected, and one full record per scenario-speed combination was checked. The files have 64,000 logical rows and nine streams: tachometer plus eight accelerometers. The paper's “114 CSV” statement remains erroneous relative to both its design arithmetic and deposited trial-level layout. [ARK23-E14, E15, E16, E17, E20–E26]

## Validation reported by source

No physics-based validation is reported in the dataset article. It describes checking that accelerometers function before recording, but does not present envelope spectra, characteristic fault frequencies, clipping/noise checks, repeatability statistics, or cross-channel alignment results. [ARK23-E18]

## Known limitations and conflicts

- File-count arithmetic conflicts within the article. [ARK23-E15]
- Bearing model/geometry, sensor mounting, DAQ module, and hardware-simultaneous timing remain Unknown. [ARK23-E05, E06]
- Article channel wording conflicts with deposited headers for motor/gearbox channels. [ARK23-E21]
- The combined ball-and-raceway defect does not specify IR versus OR in the article. [ARK23-E11]
- Physics-based signal validation is absent from the dataset article. [ARK23-E18]
- Figshare identifies the dataset license as CC BY 4.0. [ARK23-E19]

## Evidence coverage

Original-paper extraction and read-only raw-archive audit are linked to ARK23-E01–E26. The user-provided overview is recorded as ARK23-S02 but was not used as authority where it exceeded the paper. Remaining clarification targets are the article/header channel conflict, bearing geometry, sensor mounting, and hardware timing.
