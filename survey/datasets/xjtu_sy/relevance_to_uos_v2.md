# Relevance to UOS Dataset v2: XJTU-SY

## Source-supported observations

- XJTU-SY provides paired horizontal/vertical vibration snapshots on one tested-bearing housing. [XJTU-E03]
- It uses 25.6 kHz, 1.28-second snapshots collected once per minute over complete accelerated bearing lives. [XJTU-E01, E04]
- Three fixed-per-run conditions couple 2,100/2,250/2,400 RPM with 12/11/10 kN radial force. [XJTU-E02, E08]
- The horizontal channel is selected for RUL estimation because loading is horizontal and it captures more degradation information. [XJTU-E05]
- Documented endpoint failures develop during operation, but simultaneous internal compound damage is not established. [XJTU-E06, E10]

## Interpretation

XJTU-SY addresses a different research role from the planned UOS v2 batch compound-fault dataset: temporal degradation and RUL rather than a controlled matrix of simultaneous seeded faults. It provides useful design precedents for rotation count, snapshot cadence, load-direction sensor placement, and lifecycle metadata, but does not establish that 25.6 kHz or 1.28 seconds is optimal for UOS v2.

## Candidate strengths or gaps to test

- Not a gap: paired two-direction vibration at one bearing housing exists.
- Not a gap: multiple speed/load operating conditions exist across runs.
- Not a gap: full degradation trajectories and endpoint failure criteria exist.
- Candidate difference: UOS v2 targets multiple positions and compound-fault combinations rather than only degradation trajectories.
- Candidate gap: no verified internal IR/OR/ball compound matrix or bearing–rotor fault combination.
- Candidate gap: no documented single-/multi-channel paired diagnostic comparison or hardware timing validation.
- Candidate gap: no reported envelope/fault-frequency validation of the published signals.

## Design implications

- Distinguish multi-direction at one housing from multi-position sensing in UOS metadata.
- Justify UOS directions using force transmission and pilot measurements, following the physical logic of XJTU-SY's horizontal-load observation.
- Select record length using minimum shaft rotations and desired frequency resolution. XJTU-SY's 1.28 seconds spans about 45–51 rotations at its operating speeds.
- Select sampling rate from the UOS sensor/NI-9234 bandwidth and the highest bearing/sideband frequency needed for validation, not from the 25.6 kHz precedent alone.
- For batch diagnosis, record enough repeated snapshots to quantify within-condition variation; for future prognostics, separately define snapshot cadence and stopping criteria.
- Avoid coupling every RPM to only one load if UOS v2 intends to estimate speed and load effects independently.

## Open questions

- What is the exact official GitHub URL, dataset version date, and license?
- What are the raw file format, channel order, filename labels, and per-bearing record counts?
- Are both channels hardware simultaneous, and what DAQ and mounting method were used?
- Is a bearing-by-bearing final failure-mode table available?
- Were 25.6 kHz, 1.28 seconds, and one-minute cadence selected from explicit physical or storage constraints?
