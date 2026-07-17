# Relevance to UOS v2: HUST China Bearing

## Source-supported comparison

- The main article verifies only that HUSTbearing is a 2022 self-collected artificial-fault bearing dataset with multiple working conditions. [HUSTC-E01–E02]
- Detailed condition/task mappings are located in an unavailable online supplement. Acquisition hardware, channels, sampling rate, duration, RPM/load values, and fault taxonomy are not locally verified. [HUSTC-E03, HUSTC-E09]
- Release status is ambiguous because the paper both says the datasets were released and says data are available on request. [HUSTC-E04–E05]

## Interpretation for UOS design

The currently available evidence does not affect the UOS compound-fault gap, sensor layout, sampling-rate candidate, or record-length decision. Its useful lesson is metadata-related: cross-condition research needs explicit physical working-condition values and accessible task mappings rather than only domain identifiers.

## Candidate differentiation to test, not claim

- openly documented raw acquisition and persistent dataset version;
- physical RPM/load values and balanced domain/fault matrix;
- explicit sensor/DAQ/timing/mounting metadata;
- fault taxonomy and compound status traceable to physical evidence.

## Remaining evidence needed

- official Supplementary Appendix B and any dataset-specific README;
- GitHub/data-host manifest and actual access method;
- fault classes, bearing models, defect generation and severities;
- sensor, channel, DAQ, mounting, sampling rate, duration, and RPM/load grid;
- file schema, raw/processed distinction, license, and version.
