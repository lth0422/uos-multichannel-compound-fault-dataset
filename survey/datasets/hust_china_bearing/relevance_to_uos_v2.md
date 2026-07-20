# Relevance to UOS v2: HUST China Bearing

## Source-supported comparison

- The main article verifies only that HUSTbearing is a 2022 self-collected artificial-fault bearing dataset with multiple working conditions. [HUSTC-E01–E02]
- The official HUSTbearing README verifies 9 health states, ER-16K tested bearing, 25.6 kHz sampling, 262,144 points per sampling, and 99 Excel files. [HUSTC-E10, HUSTC-E12, HUSTC-E14]
- Operating conditions are primarily speed conditions: ten constant speeds from 20 to 80 Hz plus one 0-40-0 Hz time-varying condition. The README states that correct speed is in filenames and the raw second speed column is redundant for constant-speed records. [HUSTC-E11]
- Fault classes include healthy, medium/severe IR, medium/severe OR, medium/severe ball, and medium/severe IR+OR combination faults. No IR+ball, OR+ball, triple internal compound, or bearing–rotor compound class is reported. [HUSTC-E13]
- Release status is partly clarified by the public HUSTbearing repository links, although the paper's Data Availability statement still says data are available on request. [HUSTC-E04–E05, HUSTC-E14]

## Interpretation for UOS design

HUSTbearing is now a relevant comparator for RPM-domain design because it explicitly includes multiple constant-speed conditions plus one time-varying speed condition. It does not close the UOS v2 candidate gap for a balanced IR+OR, IR+Ball, OR+Ball, and IR+OR+Ball internal compound matrix, nor the bearing–rotor compound matrix, because its documented internal compound is only IR+OR.

The dataset reinforces two UOS v2 design points:

- RPM should be encoded in filenames and metadata, and measured speed columns must be clearly defined as ground truth or redundant.
- Constant-speed and time-varying-speed records should be separated in metadata and evaluation protocols.

## Candidate differentiation to test, not claim

- openly documented raw acquisition and persistent dataset version;
- physical RPM/load values and balanced domain/fault matrix across all fault labels;
- explicit sensor/DAQ/timing/mounting metadata;
- fault taxonomy and compound status traceable to physical evidence;
- controlled internal compound combinations beyond IR+OR and bearing–rotor compound combinations.

## Remaining evidence needed

- official Supplementary Appendix B, if needed for benchmark task mappings;
- GitHub/data-host manifest and raw Excel schema;
- exact sensor model/count, channel directions, DAQ, mounting, and timing;
- file schema, raw/processed distinction, license, and version.
