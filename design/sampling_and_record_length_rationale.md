# Sampling Rate and Record Length Rationale

## Decision status

The per-condition synchronized four-channel master acquisition duration is set to 60 seconds. No final sampling rate, RPM grid, canonical model-input window, overlap, or stabilization-exclusion rule is selected. This document connects the selected acquisition duration and remaining candidates to purchased hardware, survey precedents, and physical requirements.

## What the dataset survey establishes

Reviewed vibration rates range from 6.4 to 200 kHz. KAIST Batch adds a directly comparable four-vibration-channel precedent at 25.6 kHz, with 60/120-second load-part records and much longer 600/2100-second speed records. The variation follows different sensors and objectives; it does not define an optimal setting. [ARK23-E07, IMS-E05, XJTU-E04, PU-E07, MAF-E04, OTT18-E04, OTT23-E03, UOSV1-E07, KAIB-E05, KAIB-E06]

Additional papers may broaden the reference table, but they can only provide precedents. The final UOS choice must still be justified by UOS geometry, sensors, DAQ, RPM, signal bandwidth, and pilot results.

HUST Vietnam is a hardware-relevant precedent because it uses NI-9234 at 51.2 kHz for 10-second steady records and 5-second run-up data. Its stated rationale is only that the high rate captures detailed changes; the paper does not provide the bandwidth/filter/rotation derivation required for UOS. [HUSTV-E04–E06]

## Hardware-constrained rate candidates

NI-9234 uses discrete native rates and provides an alias-free bandwidth of approximately `0.45 × fs`.

The internal-timebase equation is `fs = 13,107,200 Hz / (256 × n)`, with integer `n = 1..31`. The complete native grid therefore spans 51.2 kS/s down to about 1.652 kS/s. Planning should prefer documented native rates such as 51.2, 25.6, 12.8, 6.4, and 3.2 kS/s unless pilot evidence gives a specific reason to use a fractional rate.

| Native rate | Approx. alias-free bandwidth | Four-channel samples/s | Current role |
|---:|---:|---:|---|
| 12.8 kS/s | 5.76 kHz | 51,200 | Possible storage-saving candidate if pilot spectra show no required content above this band |
| 17.067 kS/s | 7.68 kHz | 68,268 | Lower-bandwidth candidate; does not cover the supplier-listed 10 kHz sensor range |
| 25.6 kS/s | 11.52 kHz | 102,400 | Primary pilot candidate; nominally covers the supplier-listed 0.5–10 kHz range |
| 51.2 kS/s | 23.04 kHz | 204,800 | High-rate master/pilot reference; bandwidth above 10 kHz is not calibrated by the current supplier specification |

The current most defensible hypothesis is to compare 25.6 and 51.2 kS/s during pilot acquisition. If downsampled 25.6 kS/s retains all validated fault/envelope information and phase relationships, it is the more storage-efficient release candidate. A 51.2 kS/s master rate is justified only if high-rate acquisition materially improves alias protection, transient capture, mounting diagnosis, or reproducible downsampling.

Any 100 Hz representation should be treated as a derived low-rate signal for on-device or algorithm demonstrations. It requires an explicit anti-alias filter, resampling method, and statement of which physical peaks are intentionally preserved or discarded; it is not a native NI-9234 rate.

KAIST's use of 25.6 kHz strengthens its status as a practical comparison point for the same four-channel, two-housing/two-direction geometry. It does not replace the UOS derivation: the paper reports no bandwidth, anti-alias, rotation-count, or duration-selection analysis. [KAIB-E02, KAIB-E11]

## Required physical calculation

Before selection, calculate for the actual bearing geometry and proposed RPM range:

- shaft frequency;
- FTF, BPFO, BPFI, and BSF;
- required harmonics and rotor-fault sidebands;
- expected structural/sensor resonance band used for envelope analysis;
- analog/sensor/mount usable bandwidth;
- alias margin and NI-9234 filter transition.

Do not assume that sum/difference peaks uniquely prove a compound fault. Establish candidate compound features from matched pure-fault references and repeated compound trials.

## Duration candidates

Duration must be evaluated by rotations and resolution, not seconds alone.

| Duration | Resolution `1/T` | Rotations at 600 RPM | Rotations at 1,000 RPM | Rotations at 1,700 RPM |
|---:|---:|---:|---:|---:|
| 1 s | 1 Hz | 10 | 16.7 | 28.3 |
| 2 s | 0.5 Hz | 20 | 33.3 | 56.7 |
| 5 s | 0.2 Hz | 50 | 83.3 | 141.7 |
| 10 s | 0.1 Hz | 100 | 166.7 | 283.3 |
| 60 s | 0.0167 Hz | 600 | 1,000 | 1,700 |

The RPM values are evaluation points, not a final UOS grid. Recompute the table when the minimum and maximum measured RPMs are confirmed.

## Candidate recording strategy

- Acquisition: retain 60-second synchronized master records for each physical condition.
- Analysis: compare deterministic 1-, 2-, 5-, 10-, 30-, and 60-second windows from the same masters.
- Release hypothesis: retain master records and publish canonical shorter-window indices/downsampling code. If a 100 Hz derivative is needed, generate it from the master record with versioned filtering/resampling code and keep it clearly separate from raw acquisition.
- Splitting: assign train/validation/test at bearing/assembly/physical-run level before windowing.

The 60-second master duration is an acquisition decision, not a claim that 60 seconds is the optimal model-input length. Shorter canonical windows remain an analysis decision.

KAIST's 60–2100-second files support the feasibility of retaining long master records, but those durations serve different load/speed tasks and are not evidence that UOS inference samples should be equally long. [KAIB-E05, KAIB-E06]

## Storage estimates for raw four-channel master records

Approximate payload excludes file/container metadata.

| Rate | Duration | Samples across 4 channels | float32 payload | float64 payload |
|---:|---:|---:|---:|---:|
| 12.8 kS/s | 1 s | 51,200 | 0.20 MB | 0.41 MB |
| 12.8 kS/s | 10 s | 512,000 | 2.05 MB | 4.10 MB |
| 25.6 kS/s | 1 s | 102,400 | 0.41 MB | 0.82 MB |
| 25.6 kS/s | 10 s | 1,024,000 | 4.10 MB | 8.19 MB |
| 51.2 kS/s | 1 s | 204,800 | 0.82 MB | 1.64 MB |
| 51.2 kS/s | 10 s | 2,048,000 | 8.19 MB | 16.38 MB |
| 12.8 kS/s | 60 s | 3,072,000 | 12.29 MB | 24.58 MB |
| 25.6 kS/s | 60 s | 6,144,000 | 24.58 MB | 49.15 MB |
| 51.2 kS/s | 60 s | 12,288,000 | 49.15 MB | 98.30 MB |

Total project storage requires the final counts of conditions, repetitions, RPM/load cells, remounts, and metadata channels.

## Rate/duration acceptance criteria

Select the lowest native rate and shortest master/window combination that simultaneously:

- preserves required physical peaks/envelope bands with alias margin;
- maintains cross-channel phase/coherence needed by the study;
- contains the predeclared minimum number of rotations at lowest RPM;
- supplies adequate resolution and repeatability;
- avoids clipping and excessive noise;
- supports the intended on-device window after reproducible preprocessing;
- keeps total acquisition and release storage practical.
