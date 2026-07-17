# Evidence: SEU

| Evidence ID | Claim | Evidence summary | Source ID | Page/Section/Table/Figure | Confidence | Status |
|---|---|---|---|---|---|---|
| SEU-E01 | Source and repository claim | The IEEE application paper says the authors created a repository of induction-motor, bearing, and gearbox benchmark data at `mlmechanics.ics.uci.edu`. | SEU-S01 | p. 2446, abstract; p. 2454, Conclusion | High | Verified |
| SEU-E02 | CWRU is a reused external dataset | Section IV-B explicitly attributes its bearing experiment to CWRU, so those ten CWRU classes are not facts about the self-collected SEU DDS bearing subset. | SEU-S01 | pp. 2451–2452, Section IV-B | High | Verified |
| SEU-E03 | DDS testbed | The gearbox dataset was collected from the photographed drivetrain dynamic simulator containing motor, planetary/parallel gearboxes, and brake system. | SEU-S01 | pp. 2452–2454, Fig. 8 and Section IV-C | High | Verified |
| SEU-E04 | Two controller conditions | DDS experiments use `20 Hz-0 V` and `30 Hz-2 V`; exact RPM, torque, and physical-load interpretation are not supplied. | SEU-S01 | pp. 2453–2454, Section IV-C and Table V headings | High | Verified |
| SEU-E05 | Intentional IR+OR class | DDS bearing types are Ball, Inner, Outer, and Combination; Table VI defines Combination as cracks in both inner and outer rings. | SEU-S01 | p. 2453, Table VI | High | Verified |
| SEU-E06 | Mixture is not bearing–gear compound | The nine-class mixture combines four separate gear-fault classes, four separate bearing-fault classes, and one healthy class; it does not state that bearing and gear defects coexist in a sample. | SEU-S01 | pp. 2453–2454, Table VI and Section IV-C | High | Verified |
| SEU-E07 | Validation is algorithmic | The source reports classification and cross-validation but no defect metrology, characteristic-frequency/envelope checks, or acquisition-quality validation. | SEU-S01 | pp. 2453–2454, Table V and Figs. 9–10 | High | Verified |
| SEU-E08 | 1024 points are processed windows | A 1024-point time window is selected as one input sample for time-frequency imaging; the paper does not identify it as a complete raw record. | SEU-S01 | p. 2451, Section IV-A; p. 2452, Section IV-B references same transformation | Medium | Needs review |
| SEU-E09 | Acquisition facts absent | DDS sensor model/count/position, mounting, DAQ, sampling rate, raw duration, and timing architecture are not reported in the available paper. | SEU-S01 | pp. 2452–2454, Fig. 8 and Section IV-C | Medium | Needs review |
| SEU-E10 | Repository contents unverified | The paper supplies a repository hostname but not a file manifest, persistent dataset DOI, schema, or license. | SEU-S01 | p. 2446, abstract; p. 2454, Conclusion | Medium | Needs review |
