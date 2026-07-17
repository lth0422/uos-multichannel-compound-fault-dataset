# Dataset Card: SEU

## Identity

- Dataset ID: seu
- Dataset name: SEU drivetrain dynamic simulator dataset
- Institution: Southeast University; repository hosted by University of California, Irvine
- Release year: 2018 online / 2019 issue

## Purpose and scope

The available source is a machine-fault transfer-learning application paper, not a dedicated dataset paper. It reports experiments on three collections: a self-collected induction-motor dataset, CWRU bearing data, and a drivetrain dynamic simulator (DDS) dataset with separate bearing and gearbox classes. This card covers only the self-collected DDS data commonly associated with SEU; CWRU facts remain in the CWRU card. [SEU-E01, SEU-E02]

## Acquisition setup

The photographed DDS includes a motor, planetary gearbox, parallel gearbox, brake, and controllers. The paper says the data were collected from this simulator but does not identify vibration sensor model/count/position, DAQ model, sampling rate, raw record duration, or mounting. [SEU-E03, SEU-E09]

### Measurement position and mounting rationale

Unknown. The available application paper provides no verifiable sensor layout or position-selection study for the DDS dataset. [SEU-E09]

### Sampling rate, RPM, and record length rationale

Unknown. Operating settings are reported as `20 Hz-0 V` and `30 Hz-2 V`, but the source does not translate these controller settings into shaft RPM/load or state a sampling rate. A 1024-point window is documented for model preprocessing in the broader pipeline, not established as the raw DDS record length. [SEU-E04, SEU-E08]

## Sensors and channels

The paper generally describes sensor/time-series processing, but DDS sensor identities, vibration channel count, positions, directions, simultaneity, and synchronization are Unknown. [SEU-E09]

## Operating conditions

Two DDS settings are `20 Hz-0 V` and `30 Hz-2 V`. Their physical speed and load values are not reported in the article. [SEU-E04]

## Fault conditions and labels

Separate bearing classes are healthy, Ball, Inner, Outer, and Combination; Table VI defines Combination as cracks in both inner and outer rings, qualifying as an internal-bearing compound condition. Separate gearbox classes are healthy, chipped tooth, missing tooth, root crack, and surface wear. The nine-class “mixture” experiment pools four bearing-fault and four gear-fault classes with healthy data; it does not document simultaneous bearing and gear faults in one sample. [SEU-E05, SEU-E06]

## Data organization and access

The authors state that they created a repository at `mlmechanics.ics.uci.edu`. The current availability, raw-versus-processed contents, file formats, schema, version, and license have not been independently verified. [SEU-E01, SEU-E10]

## Validation reported by source

The paper reports transfer-learning classification results and cross-validation. It does not report defect metrology, characteristic-frequency/envelope validation, sensor-placement validation, or raw signal quality checks. Classification accuracy is a downstream-use result rather than physical dataset-label validation. [SEU-E07]

## Known limitations and conflicts

- Not a dedicated dataset paper; acquisition reporting is sparse.
- CWRU bearing results in the same article must not be attributed to SEU DDS.
- Sampling rate, duration, channel layout, mounting, DAQ, RPM, physical load, fault generation, and raw schema are Unknown.
- “Mixture” means pooled classes, not simultaneous bearing–gear compound faults.
- Repository availability and license require official verification.

## Evidence coverage

Only source-supported DDS facts are structured. Missing acquisition facts remain Unknown.
