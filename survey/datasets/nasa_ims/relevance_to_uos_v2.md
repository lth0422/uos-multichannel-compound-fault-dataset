# Relevance to UOS Dataset v2: NASA IMS

## Source-supported observations

- IMS records four bearing-housing positions together, with two directions per position in Set 1 and one in Sets 2–3. [IMS-E04]
- It uses 20 kHz and 20,480-sample snapshots under constant 2,000 RPM/6,000 lb load. [IMS-E02, E05]
- It provides three natural run-to-failure trajectories with timestamped snapshot files. [IMS-E01, E07, E08]
- Set 1 ends with simultaneous roller-element and outer-race damage on bearing 4, a naturally developed internal bearing compound state. [IMS-E09]
- Original-paper validation relates a detected periodic component to BPFO and includes teardown inspection. [IMS-E09, E11]

## Interpretation

NASA IMS is a partial/canonical comparator rather than a direct UOS v2 counterpart. It demonstrates that multi-position bearing vibration and naturally developed internal compound damage already exist, but it does not provide a controlled multi-label compound-fault matrix or bearing–rotor combinations. Its strongest contribution to UOS design is the distinction between snapshot duration, collection cadence, and full experiment duration.

## Candidate strengths or gaps to test

- Not a gap: simultaneous record-level observation of four bearing positions exists.
- Not a gap: a naturally developed internal bearing compound endpoint exists.
- Not a gap: teardown and BPFO-related physical evidence exist for at least one endpoint.
- Candidate difference: UOS v2 would deliberately control and label internal compound combinations rather than observe an emergent endpoint.
- Candidate gap: no paired single-/multi-channel diagnosis comparison is reported.
- Candidate gap: no bearing–rotor fault matrix, variable RPM, load matrix, or hardware timing evidence is documented.
- Candidate difference: UOS v2 targets repeatable batch conditions and on-device diagnosis, whereas IMS targets lifetime evolution/prognostics.

## Design implications

- Separate `record_duration`, `snapshot_interval`, and `total_run_duration` in UOS metadata.
- Avoid calling a record “one second” when sample count and sampling rate imply another duration.
- Preserve all selected positions in the same record and document common clock, ADC topology, and skew.
- Use teardown/inspection together with fault-frequency and envelope evidence to verify compound labels.
- For controlled compound faults, identify every simultaneously present component in multi-label metadata.
- Treat 20 kHz/approximately 1.024 seconds only as a precedent. At 2,000 RPM it contains about 34 rotations; UOS duration should instead follow its lowest RPM, resolution, repeatability, and on-device window requirements.

## Open questions

- Why do the original paper and released README report different collection intervals?
- Was Set 1 acquired with simultaneous ADCs, multiplexed channels, or another timing topology?
- What mounting method and axes were used for Sets 2 and 3?
- Does NASA's linked government-works guidance license the third-party-origin raw files, or only portal metadata?
- Are temperature measurements included anywhere in the released package or only used for rig monitoring?
