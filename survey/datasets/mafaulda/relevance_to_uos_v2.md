# Relevance to UOS Dataset v2: MAFAULDA

## Source-supported observations

- MAFAULDA records six acceleration axes across two bearing positions together with tachometer and acoustic channels. [MAF-E02, E03]
- It uses 50 kHz, 5-second records over a broad variable-speed range reported as 737–3,686 RPM. [MAF-E04, E05]
- It contains controlled imbalance and horizontal/vertical parallel misalignment severities. [MAF-E06]
- Bearing-defect cases with added imbalance masses are simultaneous bearing–rotor compound conditions under this project's definition. [MAF-E07]
- Same-bearing multi-element compound damage is not documented. [MAF-E08]
- A published feature-level one-versus-two-bearing-sensor comparison reports higher accuracy for two sensor sets in its specific ANN experiments, but does not establish a universal benefit for multichannel raw input. [MAF-E15]

## Interpretation

MAFAULDA means UOS v2 cannot claim multi-position vibration, variable-speed acquisition, imbalance/misalignment coverage, or bearing-plus-imbalance conditions as globally unprecedented. Candidate distinctions are narrower: a fully specified internal IR/OR/ball compound matrix, inclusion of looseness, four-channel hardware timing evidence, paired single-/multi-channel evaluation, and physics-based validation. These remain hypotheses until the remaining datasets are compared.

## Candidate strengths or gaps to test

- Not a gap: two bearing positions and three directions per position are represented.
- Not a gap: bearing-defect samples combined with rotor imbalance are represented.
- Not a gap: variable RPM and multiple fault-severity levels are represented.
- Candidate gap: no verified IR+OR, IR+ball, OR+ball, or triple internal-bearing combination.
- Candidate gap: no verified looseness condition.
- Candidate gap: no documented paired channel-ablation or common-clock/inter-module timing validation.
- Existing partial comparison: the paper compares features from one versus two bearing sensor sets, but not paired raw single-channel versus synchronized multi-channel models under a modern controlled protocol.
- Candidate difference: MAFAULDA is multi-modal, whereas UOS v2 presently targets multiple vibration positions/directions within a single modality.

## Design implications

- Compare UOS candidate positions with MAFAULDA's two-bearing axial/radial/tangential arrangement, but do not copy it without pilot evidence.
- Treat 50 kHz and 5 seconds only as a published precedent. Select UOS rate from sensor/NI-9234 bandwidth and target fault-frequency/sideband requirements.
- At the MAFAULDA minimum of 737 RPM, 5 seconds contains about 61 rotations; use rotation count together with frequency resolution when selecting UOS record length.
- Explicitly separate pure bearing faults, pure rotor faults, and simultaneous bearing–rotor faults in UOS metadata.
- Record channel clock, module synchronization, mounting, coordinates, RPM trace, and condition severity.

## Open questions

- Is there a later dedicated dataset paper, and what release/version does it document?
- Do the raw folder labels confirm the original paper's cage/outer-race/ball taxonomy?
- Are the two NI-9234 modules synchronized through one chassis/common clock, and what is their inter-module skew?
- How are the three uniaxial and one triaxial accelerometers assigned to the two bearing positions?
- What mounting method and microphone position were used?
- What license governs redistribution and reuse of the dataset files?
