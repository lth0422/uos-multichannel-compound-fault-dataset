# Gap Analysis

## Scope and confidence

This synthesis covers the ten registered core datasets plus KAIST Batch, HUST Vietnam, SEU DDS, HUSTbearing, S1 Data, and MCC5-THU. Every card has passed structural validation, but all remain `needs_review`; conclusions below are therefore candidate gaps supported by the reviewed sources, not universal claims about every published dataset.

## Findings that are not research gaps

### Multi-channel and multi-position vibration already exist

KAIST Batch records the same broad geometry proposed for UOS—four simultaneous accelerometers in x/y directions at two bearing housings—and cites ISO 10816-1:1995. CWRU, NASA IMS, MAFAULDA, Arkansas, S1 Data, and MCC5-THU provide other multi-position precedents, while XJTU-SY and PRONOSTIA provide two vibration directions. Therefore neither “multi-channel vibration,” “multiple vibration sensors,” nor “two positions × two directions” is sufficient as a UOS v2 contribution. [KAIB-E02, CWRU-E04, CWRU-E05, IMS-E04, MAF-E02, ARK23-E03, ARK23-E04, S1-E05, MCC5-E04, XJTU-E03, PRO-E04]

### Compound bearing and bearing–rotor conditions already exist

Internal compound damage is documented in Paderborn accelerated-life bearings, the NASA IMS Set 1 endpoint, Arkansas's ball-and-raceway bearing, and naturally mixed PRONOSTIA degradation. More directly, HUST Vietnam intentionally provides IR+OR, IR+Ball, and OR+Ball, while S1 Data provides all three pairwise combinations plus the triple IR+OR+rolling-element condition. Bearing–rotor combinations are present in UOS v1, MAFAULDA, and Arkansas; MCC5-THU adds bearing–gear compounds. Consequently, “compound fault data,” “internal bearing compound damage,” the complete pairwise-plus-triple internal set, and broad multi-channel compound data are not defensible standalone novelty claims. [HUSTV-E08, S1-E05, S1-E08, SEU-E05, PU-E11, IMS-E09, ARK23-E11, PRO-E03, UOSV1-E09, MAF-E07, ARK23-E12, MCC5-E04, MCC5-E08]

### Variable operating conditions and synchronized speed channels already exist

Several datasets vary fixed RPM across runs, while Ottawa 2018 varies speed inside each record and stores a paired encoder channel. Load, force, torque, temperature, current, acoustic, and tachometer modalities also appear in multiple datasets. Variable RPM and operating-condition metadata are expected design features rather than unique contributions. [OTT18-E03, OTT18-E05, PU-E03, OTT23-E02, PRO-E05]

### Physics-related validation has precedents

UOS v1 and Paderborn use fault-frequency/envelope evidence; NASA IMS relates a detected periodic component to BPFO and provides teardown evidence; S1 Data presents calculated frequencies and envelope analysis for all four internal compound combinations; MCC5-THU reports rotation/gear-mesh/sideband evidence for a missing-tooth example. A UOS v2 validation contribution must be release-wide and traceable to each condition, not merely the presence of an FFT or envelope figure. [UOSV1-E14, PU-E14, IMS-E09, IMS-E11, S1-E07–E10, MCC5-E13]

## Candidate gaps supported by the core-ten review

### G1. Matched compound matrix across references, bearing types, and operating conditions

S1 Data establishes that the complete IR+OR, IR+rolling-element, OR+rolling-element, and triple combination set already exists at 2,000 RPM on one SKF 6205 bearing model, with 20 one-second groups per compound type and envelope analysis. The remaining candidate gap is not the combination list. It is a matched design that includes healthy and pure references, several bearing structural types and RPMs, traceable independent physical runs, fixed simultaneous channels, and the same validation policy across all conditions. [S1-E04–E10, HUSTV-E08–E09]

Required confirmation before claiming the gap:

- inspect the official S1 supporting ZIP and HUST Vietnam repository metadata;
- extend the survey only to candidate datasets likely to contain controlled internal combinations;
- define what counts as an independent replicate rather than repeated windows from one bearing.

### G2. Controlled bridge between internal-bearing and rotor-system compounds

UOS v1 already contains bearing plus looseness/unbalance/misalignment, MAFAULDA contains bearing plus imbalance, and Arkansas contains bearing plus bent shaft. The possible gap is not bearing–rotor compound data itself, but one coherent acquisition design that combines a systematic internal-bearing matrix with clearly separated unbalance, misalignment, and looseness factors under matched operating conditions. [UOSV1-E09, MAF-E07, ARK23-E12]

### G3. Fixed synchronized vibration layout with paired channel-ablation protocol

Multiple vibration channels exist, KAIST provides an explicitly simultaneous fixed four-channel layout, S1 Data provides five axes at three positions under internal compound faults, MCC5-THU provides six axes at two positions under bearing–gear compounds, and MAFAULDA reports a feature-based one-versus-two-sensor comparison. However, the reviewed sources do not document canonical subsets evaluated as paired single-channel versus multi-channel inputs under an otherwise identical physical-run protocol. The remaining candidate gap is the paired evaluation/release protocol, not the four-channel geometry, multi-channel compound data, or proof that multi-channel input will improve performance. [KAIB-E02, KAIB-E09, S1-E05, S1-E13, MCC5-E04–E05, MCC5-E15, MAF-E15]

### G4. Reproducible timing metadata

Many datasets store channels in a common record, but reviewed sources often omit ADC topology, common-clock evidence, channel skew, anti-alias configuration, or inter-module synchronization. Publishing NI-9234/cDAQ-9171 timing architecture, channel mapping, clock assumptions, and measured/upper-bound skew would be a useful reproducibility contribution. It is not yet established as globally absent. [CWRU-E07, ARK23-E06, XJTU-E11, IMS-E12, OTT23-E14, PRO-E13]

### G5. Systematic physical validation of controlled compound labels

Existing studies offer valuable but uneven validation. S1 Data already analyzes envelope spectra for the complete internal pairwise-plus-triple set, while MCC5-THU validates one missing-tooth example. A candidate UOS contribution is therefore a predeclared release-wide protocol for every pure and compound condition using defect geometry, measured RPM, envelope/order spectra, expected component frequencies/sidebands, signal-quality checks, repeated physical runs, cross-channel consistency, and post-test inspection. [S1-E07–E10, MCC5-E13, ARK23-E18, PRO-E10, UOSV1-E14, PU-E14, IMS-E11]

### G6. Confound-resistant factorial metadata and acquisition

Ottawa 2023 couples bearing model with fault group and uses a different load for ball faults. Several prognostics datasets couple each RPM to one load. A balanced or explicitly blocked UOS design that prevents fault labels from being inferred through bearing batch, load, RPM, acquisition order, or sensor configuration would strengthen reuse and generalization research. [OTT23-E08, OTT23-E09, XJTU-E02, PRO-E07]

## Sampling-rate synthesis

Reviewed vibration rates range from 6.4 kHz (Arkansas) to 200 kHz (Ottawa 2018), with additional compound-data precedents at 12 kHz (S1) and 12.8 kHz (MCC5-THU). KAIST's 25.6 kHz is geometrically comparable, while HUST Vietnam directly uses NI-9234 at 51.2 kHz for 10 seconds. These values do not identify an optimal UOS rate because sensor bandwidths, analog filtering, fault geometry, resonance bands, and study objectives differ. [ARK23-E07, S1-E06, MCC5-E06, IMS-E05, XJTU-E04, MAF-E04, PU-E07, OTT18-E04, KAIB-E02, HUSTV-E04–E05]

Current conclusion: final UOS sampling rate remains unconfirmed. It must be selected from HS 13A131 usable bandwidth, NI-9234 supported rates and filtering, target bearing characteristic/resonance bands, pilot spectra, alias protection, storage, and on-device downsampling needs.

## Record-length synthesis

Verified fixed-record precedents include approximately 1 s (S1 and NASA IMS, with IMS conflict), 1.28 s (XJTU-SY), 4 s (Paderborn), 5 s (MAFAULDA and HUST run-up), 10 s (Arkansas, both Ottawa datasets, and HUST steady records), 60 s (MCC5-THU), 80/160 s (UOS v1), and KAIST's longer masters. The range reflects different purposes and does not select a UOS duration. [S1-E06, IMS-E05, XJTU-E04, PU-E07, MAF-E04, ARK23-E07, OTT18-E04, OTT23-E03, MCC5-E06, UOSV1-E07, KAIB-E05–E06, HUSTV-E05–E06]

Current conclusion: final UOS record length remains unconfirmed. It should be justified through lowest-RPM rotation count, desired spectral resolution, stationarity, transient coverage, repeatability, storage, and canonical on-device windows. Long master records may be retained while publishing deterministic shorter paired windows.

## Sensor-position synthesis

Precedents include near/remote motor bearings, four bearing housings, two bearing positions in multiple directions, load-direction placement, direct bearing mounting, and motor/gearbox positions. KAIST provides the closest ISO-referenced two-housing × x/y layout, while Ottawa 2023 and XJTU-SY provide other qualitative/physical rationales. None establishes the optimal surfaces for the planned UOS rig. [KAIB-E02, KAIB-E11, CWRU-E05, IMS-E04, MAF-E02, ARK23-E04, OTT23-E10, XJTU-E05]

Current conclusion: final UOS positions remain unconfirmed. Candidate positions must be selected by pilot measurements, not benchmark imitation.

## Contribution status

The following remain candidate contributions, not final claims:

1. matched healthy/single/pairwise/triple internal-bearing matrix across selected bearing types and RPMs;
2. matched internal-bearing and bearing–rotor compound design including looseness;
3. explicitly timed fixed multi-position/multi-direction vibration layout;
4. paired single-/multi-channel benchmark protocol;
5. compound-condition physics and teardown validation;
6. confound-resistant metadata and factorial operating-condition design;
7. raw master records plus reproducible on-device window definitions.
