# Gap Analysis

## Scope and confidence

This synthesis covers the ten registered core datasets plus KAIST Batch, HUST Vietnam, and the partially documented SEU DDS comparator. Every card has passed structural validation, but all remain `needs_review`; conclusions below are therefore candidate gaps supported by the reviewed sources, not universal claims about every published dataset.

## Findings that are not research gaps

### Multi-channel and multi-position vibration already exist

KAIST Batch records the same broad geometry proposed for UOS—four simultaneous accelerometers in x/y directions at two bearing housings—and cites ISO 10816-1:1995. CWRU, NASA IMS, MAFAULDA, and Arkansas provide other multi-position precedents, while XJTU-SY and PRONOSTIA provide two vibration directions. Therefore neither “multi-channel vibration,” “multiple vibration sensors,” nor “two positions × two directions” is sufficient as a UOS v2 contribution. [KAIB-E02, CWRU-E04, CWRU-E05, IMS-E04, MAF-E02, ARK23-E03, ARK23-E04, XJTU-E03, PRO-E04]

### Compound bearing and bearing–rotor conditions already exist

Internal compound damage is documented in Paderborn accelerated-life bearings, the NASA IMS Set 1 endpoint, Arkansas's ball-and-raceway bearing, and naturally mixed PRONOSTIA degradation. More directly, HUST Vietnam intentionally provides IR+OR, IR+Ball, and OR+Ball, while SEU DDS includes an IR+OR Combination class. Bearing–rotor combinations are present in UOS v1, MAFAULDA, and Arkansas. Consequently, “compound fault data,” “internal bearing compound damage,” and the three pairwise internal combinations are not defensible standalone novelty claims. [HUSTV-E08, SEU-E05, PU-E11, IMS-E09, ARK23-E11, PRO-E03, UOSV1-E09, MAF-E07, ARK23-E12]

### Variable operating conditions and synchronized speed channels already exist

Several datasets vary fixed RPM across runs, while Ottawa 2018 varies speed inside each record and stores a paired encoder channel. Load, force, torque, temperature, current, acoustic, and tachometer modalities also appear in multiple datasets. Variable RPM and operating-condition metadata are expected design features rather than unique contributions. [OTT18-E03, OTT18-E05, PU-E03, OTT23-E02, PRO-E05]

### Physics-related validation has precedents

UOS v1 and Paderborn use fault-frequency/envelope evidence; NASA IMS relates a detected periodic component to BPFO and provides teardown evidence; CWRU controls outer-race defect angle relative to load. A UOS v2 validation contribution must be systematic and compound-condition-specific, not merely the presence of an FFT figure. [UOSV1-E14, PU-E14, IMS-E09, IMS-E11, CWRU-E13]

## Candidate gaps supported by the core-ten review

### G1. Controlled and explicit internal compound matrix

HUST Vietnam establishes intentional IR+OR, IR+Ball, and OR+Ball labels, and SEU independently reinforces the IR+OR precedent. However, HUST's 6204 matrix is incomplete and severity varies, while SEU acquisition/severity metadata are sparse; neither reports IR+OR+Ball. No reviewed dataset establishes a complete, balanced, repeatable pairwise-plus-triple matrix with matched pure references and independently documented components. This narrower formulation remains a candidate UOS v2 gap. [HUSTV-E08–E09, SEU-E05, SEU-E09, PU-E11, ARK23-E11, IMS-E09, PRO-E03]

Required confirmation before claiming the gap:

- inspect official repository metadata for HUST Vietnam, Paderborn, Arkansas, NASA IMS, and PRONOSTIA;
- extend the survey only to candidate datasets likely to contain controlled internal combinations;
- define what counts as an independent replicate rather than repeated windows from one bearing.

### G2. Controlled bridge between internal-bearing and rotor-system compounds

UOS v1 already contains bearing plus looseness/unbalance/misalignment, MAFAULDA contains bearing plus imbalance, and Arkansas contains bearing plus bent shaft. The possible gap is not bearing–rotor compound data itself, but one coherent acquisition design that combines a systematic internal-bearing matrix with clearly separated unbalance, misalignment, and looseness factors under matched operating conditions. [UOSV1-E09, MAF-E07, ARK23-E12]

### G3. Fixed synchronized vibration layout with paired channel-ablation protocol

Multiple vibration channels exist, KAIST provides an explicitly simultaneous fixed four-channel layout, and MAFAULDA reports a feature-based one-versus-two-sensor comparison. However, the reviewed sources do not document canonical subsets evaluated as paired single-channel versus multi-channel inputs under an otherwise identical physical-run protocol. The remaining candidate gap is the paired evaluation/release protocol, not the four-channel geometry itself and not proof that multi-channel input will improve performance. [KAIB-E02, KAIB-E09, MAF-E15, CWRU-E07, ARK23-E06, PRO-E13]

### G4. Reproducible timing metadata

Many datasets store channels in a common record, but reviewed sources often omit ADC topology, common-clock evidence, channel skew, anti-alias configuration, or inter-module synchronization. Publishing NI-9234/cDAQ-9171 timing architecture, channel mapping, clock assumptions, and measured/upper-bound skew would be a useful reproducibility contribution. It is not yet established as globally absent. [CWRU-E07, ARK23-E06, XJTU-E11, IMS-E12, OTT23-E14, PRO-E13]

### G5. Systematic physical validation of controlled compound labels

Existing studies offer valuable but uneven validation. PRONOSTIA explicitly reports characteristic-frequency mismatch under naturally mixed damage, and Arkansas does not report physics-based validation. A candidate UOS contribution is a predeclared validation protocol for every pure and compound condition using defect geometry, measured RPM, envelope/order spectra, expected component frequencies/sidebands, signal-quality checks, repeatability, and post-test inspection. [ARK23-E18, PRO-E10, UOSV1-E14, PU-E14, IMS-E11]

### G6. Confound-resistant factorial metadata and acquisition

Ottawa 2023 couples bearing model with fault group and uses a different load for ball faults. Several prognostics datasets couple each RPM to one load. A balanced or explicitly blocked UOS design that prevents fault labels from being inferred through bearing batch, load, RPM, acquisition order, or sensor configuration would strengthen reuse and generalization research. [OTT23-E08, OTT23-E09, XJTU-E02, PRO-E07]

## Sampling-rate synthesis

Reviewed vibration rates range from 6.4 kHz (Arkansas) to 200 kHz (Ottawa 2018), with common precedents at 20, 25.6, 42, 50, 51.2, and 64 kHz. KAIST's 25.6 kHz is geometrically comparable, while HUST Vietnam directly uses NI-9234 at 51.2 kHz for 10 seconds; neither paper provides a complete physical derivation of its rate. These values do not identify an optimal UOS rate because sensor bandwidths, analog filtering, fault geometry, resonance bands, and study objectives differ. [ARK23-E07, IMS-E05, XJTU-E04, OTT23-E03, OTT23-E04, MAF-E04, PU-E07, OTT18-E04, KAIB-E02, KAIB-E11, HUSTV-E04–E05]

Current conclusion: final UOS sampling rate remains unconfirmed. It must be selected from HS 13A131 usable bandwidth, NI-9234 supported rates and filtering, target bearing characteristic/resonance bands, pilot spectra, alias protection, storage, and on-device downsampling needs.

## Record-length synthesis

Verified fixed-record precedents include 1/1.024 s (NASA IMS conflict), 1.28 s (XJTU-SY), 4 s (Paderborn), 5 s (MAFAULDA and HUST run-up), 10 s (Arkansas, both Ottawa datasets, and HUST steady records), 80/160 s (UOS v1), and KAIST's 60/120/600/2100 s masters. PRONOSTIA's reviewed paper does not state snapshot length. The range reflects different purposes and does not select a UOS duration. [IMS-E05, XJTU-E04, PU-E07, MAF-E04, ARK23-E07, OTT18-E04, OTT23-E03, UOSV1-E07, PRO-E12, KAIB-E05, KAIB-E06, HUSTV-E05–E06]

Current conclusion: final UOS record length remains unconfirmed. It should be justified through lowest-RPM rotation count, desired spectral resolution, stationarity, transient coverage, repeatability, storage, and canonical on-device windows. Long master records may be retained while publishing deterministic shorter paired windows.

## Sensor-position synthesis

Precedents include near/remote motor bearings, four bearing housings, two bearing positions in multiple directions, load-direction placement, direct bearing mounting, and motor/gearbox positions. KAIST provides the closest ISO-referenced two-housing × x/y layout, while Ottawa 2023 and XJTU-SY provide other qualitative/physical rationales. None establishes the optimal surfaces for the planned UOS rig. [KAIB-E02, KAIB-E11, CWRU-E05, IMS-E04, MAF-E02, ARK23-E04, OTT23-E10, XJTU-E05]

Current conclusion: final UOS positions remain unconfirmed. Candidate positions must be selected by pilot measurements, not benchmark imitation.

## Contribution status

The following remain candidate contributions, not final claims:

1. controlled complete internal-bearing compound matrix;
2. matched internal-bearing and bearing–rotor compound design including looseness;
3. explicitly timed fixed multi-position/multi-direction vibration layout;
4. paired single-/multi-channel benchmark protocol;
5. compound-condition physics and teardown validation;
6. confound-resistant metadata and factorial operating-condition design;
7. raw master records plus reproducible on-device window definitions.
