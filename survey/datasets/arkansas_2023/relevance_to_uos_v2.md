# Relevance to UOS Dataset v2: University of Arkansas 2023

## Source-supported observations

- Arkansas provides eight vibration channels across both bearing housings and a gearbox, including three perpendicular directions at each bearing. [ARK23-E03, E04]
- It deliberately constructs simultaneous double faults by installing two known faulty components. [ARK23-E10]
- It includes a same-bearing ball-and-raceway compound defect and bearing-plus-bent-shaft combinations. [ARK23-E11, E12]
- It uses 6.4 kHz, 10-second records at 25, 50, and 75 RPM. [ARK23-E07, E08, E23]
- Raw files use a common timestamp grid across tachometer and eight acceleration channels, but hardware-simultaneous ADC timing, mounting, and physics-based validation remain unestablished. [ARK23-E06, E18, E22]

## Interpretation

Arkansas directly weakens several broad novelty claims that might otherwise be proposed for UOS v2: multi-channel/multi-position vibration, simultaneous compound faults, internal-bearing compound damage, and bearing–rotor compound scenarios already exist in this published dataset. A candidate UOS v2 distinction must therefore be narrower and evidence-based—for example, explicitly timed four-channel acquisition, a systematic and fully specified IR/OR/ball combination matrix, unbalance/misalignment/looseness rather than only bent shaft, paired channel-ablation design, and physics-based validation. These remain candidate strengths pending the rest of the survey.

## Candidate strengths or gaps to test

- Not a gap: multi-position and multi-direction vibration channels exist in Arkansas.
- Not a gap: deliberate simultaneous double faults exist.
- Not a gap: internal ball+raceway and bearing+bent-shaft compound cases exist.
- Candidate gap: exact internal combinations are not fully specified; no complete IR+OR, IR+ball, OR+ball, and triple matrix is documented in the article.
- Candidate gap: synchronization/simultaneous-sampling evidence is absent despite NI CompactDAQ use.
- Candidate gap: no reported fault-frequency/envelope validation or paired single-/multi-channel performance study.
- Candidate difference to test: UOS v2 targets unbalance, misalignment, and looseness combinations, whereas Arkansas reports bent-shaft faults.

## Design implications

- Do not frame four vibration channels or compound faults alone as novel.
- Define every bearing defect component and rotor fault independently in multi-label metadata.
- Explicitly record common clock, ADC topology, channel skew, coordinates, directions, and mounting.
- Include a designed comparison of single-channel subsets against the same synchronized multi-channel records.
- Validate each compound condition using rotational/fault frequencies, envelope spectra, expected sidebands, clipping/noise checks, and repeatability.
- Select sampling rate and record duration from UOS hardware bandwidth and physical-validation requirements, not Arkansas's 6.4 kHz/10-second precedent.

## Open questions

- How was tachometer voltage converted or calibrated to verify the stated RPM?
- Why does the paper report 114 files when the archive contains 2,925 trial CSVs organized as 39 × 25 × 3?
- Why does the article describe two gearbox directions while raw headers show one Motor and one Gearbox acceleration channel?
- Is the combined ball-and-raceway defect on the inner or outer raceway?
- Which permitted double-fault pairs correspond to bearing–shaft and cross-bearing combinations?
- What NI CompactDAQ modules and mounting methods were used, and are channels hardware simultaneous?
