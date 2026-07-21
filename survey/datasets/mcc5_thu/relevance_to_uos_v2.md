# Relevance to UOS Dataset v2

## Source-supported observations

- MCC5-THU provides six vibration axes at two positions plus actual speed and torque channels. [MCC5-E04]
- It uses 12.8 kHz, 60-second records under fixed and time-varying speed/load modes. [MCC5-E06, MCC5-E10]
- It provides broken-tooth+IR and broken-tooth+OR bearing–gear compounds at three severities. [MCC5-E08, MCC5-E09]
- A missing-tooth example is checked using rotation, mesh, sideband, and envelope-spectrum evidence. [MCC5-E13]

## Interpretation

MCC5-THU demonstrates that multi-position triaxial vibration, actual speed/torque signals, long variable-condition records, severity labels, and same-sample component compounds can coexist in a public dataset. It is not a direct internal-bearing or bearing–rotor comparator because its compounds link a bearing race fault to a broken gear tooth. UOS v2 must not claim that multi-channel compound machinery data broadly are new.

## Candidate strengths or gaps to test

- Not a gap: six-channel two-position vibration under compound faults exists.
- Not a gap: public bearing–gear compound data and three severities exist.
- Not a gap: 60-second variable-speed/load records with actual speed and torque exist.
- Candidate difference: MCC5 has no complete internal-bearing pairwise/triple matrix.
- Candidate difference: MCC5 has no unbalance/misalignment/looseness bearing–rotor matrix.
- Candidate difference: hardware simultaneity and paired single-/multi-channel evaluation are not documented.
- Candidate difference: condition-wide physics validation is not reported.

## Design implications

- Add bearing–gear compound as a separate comparison column; do not merge it with bearing–rotor compound.
- Consider measured RPM rather than command-only RPM, especially during transition records.
- Decide whether UOS needs severity levels; MCC5 already provides a strong three-level precedent.
- Preserve long master records and actual operating-condition channels when feasible.
- Publish exact timing and channel-ablation protocol if those are intended UOS contributions.

## Open questions

- What license, row counts, file naming consistency, and missing-value behavior appear in the official deposit?
- What DAQ, mounting method, anti-alias filters, clock routing, and channel skew were used?
- How should the Table 1 value of 48 transitional conditions be reconciled with Section 3's 112 combinations?
- Are all eight columns sampled on the same 12.8 kHz grid in every raw file?
