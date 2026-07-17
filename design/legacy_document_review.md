# Review of Legacy DAQ and Mounting Note

## Document status

- Local source: `library/documents/design/legacy/DAQ_필요성_Magnet_Stud_검증_legacy.pdf`
- Role: pre-purchase internal research note
- Status: retained for provenance; not an authoritative current design specification

The note was prepared around a proposed PCB 603C01 + NI USB-4431 system. The confirmed purchase is instead four HS Sensors 13A131 accelerometers with NI-9234 and cDAQ-9171. Any model-specific compatibility, connector, mounting, bandwidth, cost, or timing conclusion in the legacy note must therefore be re-established for the delivered hardware.

## Statements that remain useful as hypotheses

- A common four-channel DAQ is appropriate for paired spatial/directional vibration records.
- A two-bearing × two-direction layout is a reasonable pilot candidate.
- Mounting response can limit usable measurement bandwidth.
- Sampling rate should cover the useful resonance/envelope band with anti-alias margin.
- Channel timing, mounting, and cable configuration should be documented.

These statements motivate tests; they do not validate the final layout or rate.

## Statements requiring correction or re-verification

| Legacy statement | Current assessment |
|---|---|
| Proposed hardware is PCB 603C01 + NI USB-4431 | Obsolete for this project; confirmed hardware is HS 13A131 ×4 + NI-9234/cDAQ-9171. |
| KTMA004 1/4-28 directly fits the accelerometer | Not established. Supplier information for 13A131 lists an M5 mounting thread; an appropriate M5 adapter/base or delivered accessory must be confirmed. |
| All reviewed multichannel datasets establish simultaneous acquisition | Unsupported. Many papers show common records but omit ADC topology/skew. NI-9234 itself is officially specified for simultaneous sampling, which is the relevant UOS basis. |
| XJTU-SY uses DT9837 and magnetic bases | Not established in the reviewed original paper; DAQ and attachment remain Unknown. [XJTU-E03, XJTU-E11] |
| Arkansas has proven simultaneous sampling | Not established; only common timestamp records were verified. [ARK23-E06, ARK23-E22] |
| Ottawa 2018/2023 can be represented as one two-channel/42 kHz dataset | Incorrect conflation. Ottawa 2018 is acceleration+encoder at 200 kHz; Ottawa 2023 has one vibration channel plus other modalities at 42 kHz. [OTT18-E03, OTT18-E04, OTT23-E02, OTT23-E03] |
| PRONOSTIA accelerometer is DYTRAN 3035B | Model is not stated in the reviewed original paper. [PRO-E04, PRO-E06] |
| CWRU always has three vibration channels | Overgeneralized; DE/FE are paired and base is present only in some experiments. [CWRU-E05, CWRU-E14] |
| Magnet bandwidth values validate the delivered mounting | Not yet. The cited mounting white paper, actual magnet/adapter, housing curvature/finish, tightening, and 13A131 response must be reviewed/tested. |
| Cross-modulation sum/difference peaks will necessarily prove compound faults | Too strong. Such components may be hypotheses, but nonlinear coupling and detectability must be demonstrated against matched pure-fault controls. |

## Current hardware facts that supersede the note

- NI-9234: four 24-bit simultaneously sampled inputs, maximum 51.2 kS/s per channel, rate-dependent filtering, alias-free bandwidth approximately `0.45 × fs`.
- cDAQ-9171: one-slot USB chassis; installed NI-9234 sets the analog-input ceiling.
- HS 13A131: four purchased IEPE uniaxial sensors; supplier-listed 100 mV/g, ±50 g, 0.5–10 kHz, M5 top-entry configuration, pending delivered primary datasheet/calibration confirmation.

See [hardware_inventory.md](hardware_inventory.md). The legacy PDF remains Git-ignored and must not be committed.
