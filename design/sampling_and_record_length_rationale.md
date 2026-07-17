# Sampling Rate and Record Length Rationale

## Decision status

No final rate or duration is selected. This document narrows pilot candidates using purchased hardware, the core-ten survey, and physical requirements.

## What the dataset survey establishes

Reviewed vibration rates range from 6.4 to 200 kHz. KAIST Batch adds a directly comparable four-vibration-channel precedent at 25.6 kHz, with 60/120-second load-part records and much longer 600/2100-second speed records. The variation follows different sensors and objectives; it does not define an optimal setting. [ARK23-E07, IMS-E05, XJTU-E04, PU-E07, MAF-E04, OTT18-E04, OTT23-E03, UOSV1-E07, KAIB-E05, KAIB-E06]

Additional papers may broaden the reference table, but they can only provide precedents. The final UOS choice must still be justified by UOS geometry, sensors, DAQ, RPM, signal bandwidth, and pilot results.

HUST Vietnam is a hardware-relevant precedent because it uses NI-9234 at 51.2 kHz for 10-second steady records and 5-second run-up data. Its stated rationale is only that the high rate captures detailed changes; the paper does not provide the bandwidth/filter/rotation derivation required for UOS. [HUSTV-E04–E06]

## Hardware-constrained rate candidates

NI-9234 uses discrete native rates and provides an alias-free bandwidth of approximately `0.45 × fs`.

| Native rate | Approx. alias-free bandwidth | Four-channel samples/s | Current role |
|---:|---:|---:|---|
| 17.067 kS/s | 7.68 kHz | 68,268 | Lower-bandwidth candidate; does not cover the supplier-listed 10 kHz sensor range |
| 25.6 kS/s | 11.52 kHz | 102,400 | Primary pilot candidate; nominally covers the supplier-listed 0.5–10 kHz range |
| 51.2 kS/s | 23.04 kHz | 204,800 | High-rate master/pilot reference; bandwidth above 10 kHz is not calibrated by the current supplier specification |

The current most defensible hypothesis is to compare 25.6 and 51.2 kS/s during pilot acquisition. If downsampled 25.6 kS/s retains all validated fault/envelope information and phase relationships, it is the more storage-efficient release candidate. A 51.2 kS/s master rate is justified only if high-rate acquisition materially improves alias protection, transient capture, mounting diagnosis, or reproducible downsampling.

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

The RPM values are evaluation points, not a final UOS grid. Recompute the table when the minimum and maximum measured RPMs are confirmed.

## Candidate recording strategy

- Pilot: acquire 10-second synchronized master records at both 25.6 and 51.2 kS/s for representative healthy/pure-fault conditions.
- Analysis: compare deterministic 1-, 2-, 5-, and 10-second windows from the same masters.
- Release hypothesis: retain master records and publish canonical shorter-window indices/downsampling code.
- Splitting: assign train/validation/test at bearing/assembly/physical-run level before windowing.

This strategy is provisional. Ten seconds is useful for comparing resolutions and shorter windows, not yet the final per-record requirement.

KAIST's 60–2100-second files support the feasibility of retaining long master records, but those durations serve different load/speed tasks and are not evidence that UOS inference samples should be equally long. [KAIB-E05, KAIB-E06]

## Storage estimates for raw four-channel master records

Approximate payload excludes file/container metadata.

| Rate | Duration | Samples across 4 channels | float32 payload | float64 payload |
|---:|---:|---:|---:|---:|
| 25.6 kS/s | 1 s | 102,400 | 0.41 MB | 0.82 MB |
| 25.6 kS/s | 10 s | 1,024,000 | 4.10 MB | 8.19 MB |
| 51.2 kS/s | 1 s | 204,800 | 0.82 MB | 1.64 MB |
| 51.2 kS/s | 10 s | 2,048,000 | 8.19 MB | 16.38 MB |

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
