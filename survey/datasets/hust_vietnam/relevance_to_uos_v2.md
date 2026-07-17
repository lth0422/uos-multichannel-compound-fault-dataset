# Relevance to UOS v2: HUST Vietnam

## Source-supported comparison

- HUST Vietnam explicitly provides the three pairwise internal-bearing compounds IR+OR, IR+Ball, and OR+Ball in artificially faulted bearings. It therefore substantially narrows the previously proposed internal-compound gap. [HUSTV-E08]
- It spans five bearing models and three loads, but the matrix is incomplete for 6204 and crack depth differs between bearings. [HUSTV-E02, HUSTV-E09]
- It uses one vertical vibration channel, NI-9234, 51.2 kHz, 10-s steady records, and 5-s run-up data. Exact position/mounting and RPM values are not reported in the article. [HUSTV-E03–E06, HUSTV-E10]
- No IR+OR+Ball triple condition, bearing–rotor compound, paired multi-channel evaluation, or systematic physics-based label validation is reported. [HUSTV-E08, HUSTV-E11]

## Interpretation for UOS design

UOS must not claim that pairwise internal-bearing compound data are absent from prior work. A narrower candidate distinction is a complete and balanced pairwise-plus-triple matrix, acquired with a fixed simultaneous multi-position layout and matched pure/compound references. HUST also provides a direct NI-9234/51.2-kHz/10-s precedent, but its paper does not physically derive those settings; UOS still needs bandwidth, alias, rotation-count, resolution, and pilot evidence.

## Candidate differentiation to test, not claim

- complete IR+OR, IR+Ball, OR+Ball, and IR+OR+Ball coverage across declared bearing/severity blocks;
- matched pure faults and compound faults without missing bearing-model cells or uncontrolled depth variation;
- simultaneous two-position × two-direction vibration with paired channel ablation;
- bearing–rotor compounds under the same acquisition protocol;
- characteristic-frequency, envelope/order, repeatability, and inspection-based validation.

## Remaining evidence needed

- Mendeley file manifest, exact 99-signal accounting, MAT field shapes and units;
- numerical steady/run-up RPM data and load interpretation;
- accelerometer attachment, exact measurement surface, and CompactDAQ chassis model;
- dataset-file license and any acquisition/analysis code;
- independent evidence that each pairwise defect is physically present as intended.
