# Relevance to UOS v2: KAIST Batch

## Source-supported comparison

- KAIST uses four simultaneous vibration channels at two bearing housings in x/y directions, citing ISO 10816-1:1995. This is the closest reviewed geometric precedent for the proposed UOS shaft-end/motor-end top/side layout. [KAIB-E02]
- KAIST vibration is sampled at 25.6 kHz, matching one NI-9234-native UOS pilot candidate. Its fixed records are 60/120 s; constant-/varying-speed records extend to 600/2100 s. [KAIB-E05, KAIB-E06]
- KAIST separately provides bearing, misalignment, and unbalance states, but no same-sample internal-bearing or bearing–rotor compound labels. [KAIB-E07]
- It provides multiple modalities and varying operating conditions, but does not report paired single-channel versus four-channel evaluation or systematic physical validation across every condition. [KAIB-E09, KAIB-E10]

## Interpretation for UOS design

The proposed two-housing × two-radial-direction layout is technically plausible and has a strong published precedent; it is therefore not a novelty claim by itself. UOS still needs rig-specific pilot evidence that shaft-end/motor-end top/side channels are repeatable, sensitive, and non-redundant. KAIST's 25.6 kHz is useful precedent, not a sufficient rate derivation. Its long continuous records support retaining master acquisitions and deriving deterministic shorter windows, but do not establish an optimal UOS duration.

## Candidate differentiation to test, not claim

- controlled same-sample internal-bearing and bearing–rotor compound conditions;
- explicit NI-9234 simultaneous-sampling and timing metadata;
- paired single-channel/housing/direction/all-channel evaluation from identical physical runs;
- predeclared characteristic-frequency, envelope, order, repeatability, and placement-validation criteria;
- reproducible master-to-on-device window/downsampling definitions.

## Remaining evidence needed

- official Mendeley README, dataset-file license, and raw column/schema consistency;
- accelerometer attachment and coordinate details, if present outside the paper;
- SCADAS and NI cross-device timing architecture;
- explanation for the NI 9211/9775 role reversal in the Specifications Table;
- any follow-up experiment that quantitatively compares positions or channel subsets.
