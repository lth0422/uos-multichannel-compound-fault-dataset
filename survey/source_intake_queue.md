# Local Source Intake Queue

Last inventory: 2026-07-17

This file records locally prepared source material. `Ready` means a file is available for review, not that its technical claims have been verified. Dataset investigation remains one dataset per task.

| Dataset | Local source | Intake status | Survey status / next action |
|---|---|---|---|
| NASA IMS | `library/papers/NASA IMS/Readme Document for IMS Bearing Data.pdf` | Reviewed | First-pass complete; resolve duration/cadence and license caveats |
| NASA IMS | `library/papers/NASA IMS/Wavelet filter-based weak signature detection method and.pdf` | Reviewed | Original experiment paper linked to evidence |
| Ottawa 2023 | `library/papers/ottawa 2023/University of Ottawa constant load and speed.pdf` | Reviewed | First-pass complete; repository/license/schema verification pending |
| Ottawa 2018 | `library/papers/ottawa 2018/Bearing vibration data collected under time-varying.pdf` | Reviewed | First-pass complete; repository/license/acquisition gaps pending |
| PRONOSTIA | `library/papers/PRONOSTIA/PRONOSTIA, An experimental platform for bearings.pdf` | Reviewed | First-pass complete; official challenge README/schema pending |
| CWRU | `library/papers/cwru/Rolling element bearing diagnostics using the Case Western Reserve University data, a benchmark study.pdf` | Ready | Follow-up/benchmark critique review pending |
| KAIST Batch | `library/papers/kaist(Batch)/Vibration, acoustic, temperature, and motor current dataset of rotating machine under varying operating conditions for fault diagnosis.pdf` | Reviewed | Registered as P2 direct comparator; repository/license/mounting/timing verification pending |
| HUST Vietnam | `library/papers/HUST (vietnam)/HUST bearing.pdf` | Reviewed | Registered as P2 direct comparator; repository/RPM/mounting/timing/license verification pending |
| SEU | `library/papers/SEU/Highly_Accurate_Machine_Fault_Diagnosis_Using_Deep_Transfer_Learning.pdf` | Reviewed | Application paper only; DDS facts registered conservatively and official dataset documentation required |
| HUST China bearing | `library/papers/HUST (china)/Domain generalization for cross-domain fault diagnosis.pdf` | Reviewed | Minimal HUSTbearing card registered; online Supplementary Appendix B and repository documentation required |

## Recommended processing order

1. CWRU follow-up evidence reconciliation
2. Review core-ten comparison and draft gap analysis
3. Obtain HUST China online Supplementary Appendix B before further technical comparison; treat HUSTgearbox as a separate future task

Publisher PDFs remain ignored and must not be committed. Exact repository URLs, official README files, licenses, and supplementary acquisition documentation should be added when available.
