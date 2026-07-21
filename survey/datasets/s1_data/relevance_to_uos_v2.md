# Relevance to UOS Dataset v2

## Source-supported observations

- S1 experimentally covers IR+OR, IR+rolling-element, OR+rolling-element, and IR+OR+rolling-element faults. [S1-E08]
- It records 20 groups per fault type at 12 kHz, 12,000 points, and 2,000 RPM. [S1-E06, S1-E07]
- It provides five vibration axes from two uniaxial bearing sensors and one three-way gearbox sensor, but exact axes and timing are not documented. [S1-E05, S1-E13]
- It calculates bearing/gear frequencies and presents envelope spectra for all four compound cases. [S1-E07, S1-E10]

## Interpretation

S1 removes both “all three pairwise internal combinations plus a triple combination” and broad “multi-position compound-fault vibration” as standalone UOS v2 novelty claims. Its limitations leave a narrower candidate distinction: matched healthy and pure-fault references, multiple bearing structural types, multiple RPM conditions, explicitly simultaneous fixed-layout records, paired single-/multi-channel evaluation, and release-level metadata linking every physical run and validation result.

## Candidate strengths or gaps to test

- Not a gap: complete pairwise-plus-triple internal compound experiments exist.
- Not a gap: physics-based envelope analysis of compound conditions exists.
- Candidate difference: matched pure references and balanced factor design are not documented for S1.
- Candidate difference: S1 uses one verified bearing model and one RPM.
- Candidate difference: S1 has five vibration axes, but exact axes, stored schema, simultaneous sampling, mounting, and paired channel comparison are unresolved.
- Candidate difference: UOS targets bearing–rotor compounds; S1 treats shaft/gear behavior as interference rather than introduced fault labels.

## Design implications

- Do not claim that IR+OR+Ball or the three pairwise combinations are globally new.
- Preserve matched healthy, pure single-fault, pairwise, and triple records under identical RPM/load/assembly rules.
- Publish exact channel mapping and NI-9234 timing evidence rather than relying on a multi-location diagram.
- Compare compound spectra with matched pure references and retain conflicting/masked outcomes.
- Use more than one physical acquisition run and prevent windows from one group crossing data splits.

## Open questions

- What files, channel columns, units, and metadata are inside the official S1 ZIP?
- Are the three stated measurement positions recorded simultaneously or in separate acquisitions?
- What accelerometer models, exact axes, mounting, DAQ, and calibration were used?
- Does the supporting release include healthy or pure single-fault groups not described in the paper?
