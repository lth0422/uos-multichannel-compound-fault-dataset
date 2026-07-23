# Four-Channel Sensor Layout Candidate

## Status

This is the team's current candidate and a pilot subject, not the final acquisition layout.

The 2026-07-22 sequential crossover pilot found that all four 13A131/NI-9234 channels observed the shaft peak and 30204 IR BPFI envelope peak at all four positions. Same-position RMS and spectral shape were consistent across moved sensors. Because the records were sequential rather than simultaneous, this result establishes preliminary channel health and position observability, not final four-channel complementarity or timing. See [`../pilot/2026-07-22_1400rpm_30204_ir_h/pilot_validation_report_ko.md`](../pilot/2026-07-22_1400rpm_30204_ir_h/pilot_validation_report_ko.md).

```text
   [CH1 top]                 [CH3 top]
       |                         |
       O -- [CH2 side]           O -- [CH4 side]
       |                         |
   shaft-end                 motor-end
   bearing housing           bearing housing
```

| Channel | Candidate position | Candidate direction | Intended role |
|---|---|---|---|
| CH1 | shaft-end bearing housing, top | radial vertical | continuity with the UOS v1 top shaft-end position |
| CH2 | shaft-end bearing housing, side | radial horizontal | orthogonal response at shaft end |
| CH3 | motor-end bearing housing, top | radial vertical | spatial comparison near motor end |
| CH4 | motor-end bearing housing, side | radial horizontal | orthogonal response at motor end |

`Top`, `side`, `vertical`, and `horizontal` must be converted to a rig-fixed coordinate system and photographed. They are not substitutes for measured coordinates or orientation arrows.

## Why the candidate is plausible

### Spatial coverage

Two housings provide near/remote transmission-path information and may respond differently to bearing and rotor-system faults. KAIST Batch is the closest geometric precedent: four accelerometers simultaneously measure x/y vibration at two bearing housings, with ISO 10816-1:1995 cited for placement. Multi-position precedents also exist in CWRU, NASA IMS, MAFAULDA, and Arkansas, so the value is plausible but not novel by itself. [KAIB-E02, CWRU-E05, IMS-E04, MAF-E02, ARK23-E04]

### Directional coverage

Orthogonal radial channels can capture load-direction and structural anisotropy. XJTU-SY reports that the direction aligned with applied load contains more degradation information; PRONOSTIA and MAFAULDA also record orthogonal/multiple directions. [XJTU-E05, PRO-E04, MAF-E02]

KAIST establishes an ISO-referenced layout precedent, but does not compare alternative positions, disclose the exact attachment, or quantify remount repeatability and per-position observability. UOS must therefore treat it as support for pilot candidacy, not as validation of the present shaft-end/motor-end surfaces. [KAIB-E11]

### Baseline continuity

CH1 preserves conceptual continuity with UOS v1's shaft-end top position, allowing a controlled comparison if bearing, speed, load, and mounting differences are documented. [UOSV1-E04, UOSV1-E05]

### Paired evaluation

Every physical event can expose CH1 alone, each single channel, each housing pair, each directional pair, and all four channels without recollection. This supports paired channel-ablation research, provided split groups remain at physical-run level.

## Why the layout is not yet validated

- The actual radial-load direction relative to `top` and `side` has not been recorded here.
- Housing geometry, surface flatness/curvature, magnetic holding force, and remount repeatability may differ by position.
- Motor-end channels may include motor electromagnetic/structural vibration; this may be useful context or unwanted confounding.
- Both channels on one housing may be redundant, while an axial or base/rotor-support location could add more information.
- Cable routing and strain can introduce position-dependent artifacts.
- Sensor mass/orientation and mounting resonance may limit high-frequency comparison.
- The delivered 13A131 M5 mounting interface has not been matched to the legacy 1/4-28 magnet proposal.

## Pilot alternatives to compare

The proposed layout should be evaluated against at least one alternative during pilot work:

- replace one side channel temporarily with an axial direction;
- replace one channel temporarily with a motor casing/base or support-path position;
- co-locate all sensors for gain/phase consistency before distributing them;
- swap sensor serial numbers between positions to separate sensor bias from position effects.

The final four locations should maximize repeatable fault observability and complementary information, not visual symmetry.

## Required evidence and decision metrics

For healthy and matched pure-fault pilot runs, calculate per channel:

- time-domain RMS, peak, crest factor, clipping rate, DC/bias health, and noise floor;
- shaft-order and bearing-frequency/envelope peak SNR;
- coherence/correlation and mutual redundancy between channels;
- repeatability across runs and at least three remove/remount cycles;
- sensitivity to speed/load and fault type;
- classifier/channel-ablation performance using physical-run grouped splits;
- mounting/cable sensitivity and usable high-frequency response.

## Candidate acceptance rule

Retain a channel position only if it is mechanically repeatable and contributes either stronger physical observability or non-redundant diagnostic information. Multi-channel accuracy alone is insufficient if improvement can be explained by leakage, RPM/load imbalance, sensor identity, or acquisition order.
