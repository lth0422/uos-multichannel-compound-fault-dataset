# Relevance to UOS Dataset v2: UOS v1

## Source-supported observations

- UOS v1 provides one uniaxial accelerometer channel at one shaft-end housing position. The paper does not establish synchronized multi-position acquisition. [UOSV1-E04, E05, E15]
- Its 21 compound conditions combine a single bearing fault with looseness, unbalance, or misalignment. [UOSV1-E09, E10]
- Its exhaustive bearing-condition list contains H, ball/roller, IR, and OR individually; it does not include simultaneous internal bearing combinations such as IR+OR. [UOSV1-E08, E10]
- It spans three bearing types, six fixed RPM conditions, two sampling rates, and supplies raw vibration plus STFT spectrograms. [UOSV1-E03, E06, E07, E12]
- It reports physics-informed validation using bearing fault frequencies and machine-fault amplitude measures. [UOSV1-E14]

## Interpretation

Relative to the current UOS v2 working hypotheses, UOS v1 already covers the candidate bearing–rotor compound-fault axis and bearing-type domain shift. The clearest candidate extensions are therefore not merely “compound faults” or “multiple conditions,” but synchronized vibration channels across positions/directions, paired single-/multi-channel records, and simultaneous internal-bearing fault combinations. These remain candidate gaps until the broader dataset survey confirms whether other datasets provide them.

## Candidate strengths or gaps to test

- Candidate gap: synchronized multi-position and/or multi-direction vibration is not provided by UOS v1.
- Candidate gap: internal bearing compound faults (IR+OR, IR+ball/roller, OR+ball/roller, triple combinations) are absent from UOS v1's enumerated conditions.
- Candidate continuity: looseness, unbalance, and misalignment combinations can provide a direct conceptual bridge between v1 and a possible v2 design.
- Candidate strength to preserve: bearing-type diversity and physics-informed validation.
- Not established: multi-channel input will improve diagnostic performance; UOS v1 provides no paired comparison for this claim.
- Not established: the v1 sensor position, 8/16 kHz rates, six-speed grid, or 80/160 s record lengths are optimal for v2. They are reference conditions, not design justification. [UOSV1-E03, E05, E06, E17, E18]

## Design implications

- If v2 targets multi-channel research, record the same event simultaneously at explicitly documented positions and directions and retain paired channel subsets.
- Treat internal bearing compound faults separately from bearing–rotor compound faults in labels and acquisition planning.
- Preserve raw time-domain signals and sufficient tachometer/speed metadata for rotational-frequency, fault-frequency, and envelope-spectrum validation.
- Consider compatibility with v1 operating conditions only after hardware limits and the broader gap analysis are complete.
- Document sensor model, mounting, channel timing architecture, DAQ, and synchronization evidence explicitly.
- Select v2 positions using explicit evidence such as bearing/rotor transmission-path reasoning, pilot measurements across candidate positions, signal-to-noise ratio, fault-frequency visibility, repeatability, and channel complementarity.
- Select sampling rate from the required diagnostic bandwidth and anti-aliasing constraints; select RPM coverage from intended operating/domain-shift questions; select record duration from frequency resolution, minimum rotations, stationarity, storage, and inference-window requirements.

## Open questions

- Will v2 reuse any v1 bearing models, speed grid, fault severities, or file conventions?
- What timing evidence will be required to claim simultaneous sampling versus synchronized acquisition?
- Will every multi-channel record expose canonical single-channel subsets for paired evaluation?
- How will compound samples be multi-label annotated without collapsing them into only mutually exclusive class names?
- Can internal bearing compound faults be fabricated and validated without introducing uncontrolled damage interactions?
- Which candidate positions maximize fault-frequency/envelope observability while contributing non-redundant channel information?
- What minimum diagnostic bandwidth and frequency resolution determine sampling rate and record duration?
- Should RPM be a fixed grid, controlled transients, or both, and how will speed be measured and synchronized?
