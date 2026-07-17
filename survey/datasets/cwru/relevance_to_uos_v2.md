# Relevance to UOS Dataset v2: CWRU

## Source-supported observations

- CWRU supplies paired drive-end and fan-end vibration in each MAT file, with a base-plate channel in some experiments. [CWRU-E05, E14]
- It is multi-sensor, multi-channel, and multi-position within a single vibration modality; exact direction and hardware timing are not established. [CWRU-E04, E05, E07]
- Sampling rates are 12 and 48 kS/s, but record duration and explicit rate-selection rationale are not reported on the reviewed official pages. [CWRU-E08, E09]
- Faults are separately seeded IR, OR, and ball single-point defects; compound conditions are not documented. [CWRU-E11, E12]
- Motor load and corresponding fixed speed vary, and OR defect angle relative to the load zone is explicitly controlled. [CWRU-E03, E13]

## Interpretation

CWRU means that “multiple vibration positions” alone cannot be treated as a novel UOS v2 contribution. A more defensible candidate distinction would require explicit simultaneous/synchronized timing evidence, clearly documented directions and mounting, consistent channel availability, paired single-/multi-channel evaluation, and compound-fault coverage. CWRU also provides a useful precedent for controlling defect orientation relative to the load zone, which may affect where UOS v2 sensors should be placed.

## Candidate strengths or gaps to test

- Candidate gap: official CWRU documentation does not establish hardware timing or synchronized acquisition despite paired DE/FE signals.
- Candidate gap: no same-sample internal-bearing or bearing–rotor compound fault is documented.
- Candidate gap: base vibration is not uniformly reported across all experiments.
- Candidate reference: near/remote bearing locations enable paired multi-position analysis.
- Candidate reference: OR defect angle relative to load zone is treated explicitly.
- Not established: CWRU's 12/48 kS/s choices or magnetic mounting should be copied for UOS v2.

## Design implications

- Define a fixed four-channel position/direction layout and ensure every UOS v2 sample contains the same channel set.
- Document the NI-9234 common timing architecture so synchronized/simultaneous claims do not depend merely on signals sharing a file.
- Include sensor mounting, orientation, load-zone relationship, and channel coordinates in metadata.
- Evaluate whether positions near and remote from each bearing, or orthogonal directions around one housing, provide complementary fault information.
- Choose sampling rate from sensor/DAQ bandwidth and fault-frequency requirements rather than benchmark precedent alone.
- Preserve compound components as multi-label fields while retaining paired channel subsets.

## Open questions

- What exact DE/FE/BA record lengths and variable shapes occur across the official files?
- Are DE and FE sampled from a common clock and simultaneous ADC channels?
- What accelerometer and DAT-recorder models, sensitivities, and calibration procedures were used?
- Why were 12 and 48 kS/s chosen, and what analog anti-alias filters were used?
- What license and original release/version metadata govern redistribution and reuse?
