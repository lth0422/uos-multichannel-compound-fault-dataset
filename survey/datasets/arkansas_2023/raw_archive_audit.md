# Raw Archive Audit: University of Arkansas 2023

## Scope

Read-only audit performed on 2026-07-17. The outer archive was not extracted or modified. The audit read all nested ZIP directory entries and all 2,925 CSV metadata headers, then streamed one complete CSV for every scenario-speed combination (117 files). This establishes packaging and record structure; it is not a substitute for physics-based signal validation.

## Archive inventory

| Item | Archive bytes | Uncompressed CSV bytes | CSV files |
|---|---:|---:|---:|
| Outer `22693120.zip` | 14,832,979,838 | — | — |
| 25 RPM nested ZIP | 4,726,862,392 | 17,782,097,136 | 975 |
| 50 RPM nested ZIP | 4,983,597,508 | 18,099,692,663 | 975 |
| 75 RPM nested ZIP | 5,122,519,200 | 18,068,148,770 | 975 |

Each speed group contains 39 scenarios and 25 trials per scenario. The full deposit therefore contains 2,925 CSV files. A `desktop.ini` is also present in the 25 RPM nested ZIP and is not data.

## File schema

All CSV metadata headers report an interval of 0.00015625 seconds, equivalent to 6,400 Hz, for these nine streams:

| Stream | Unit |
|---|---|
| Tachometer | V |
| Motor | g |
| Bearing 1 Z, Y, X | g |
| Bearing 2 Z, Y, X | g |
| Gearbox | g |

The eight acceleration streams conflict with the article's description of three directions at each bearing plus two gearbox directions: the deposited header instead names one Motor and one Gearbox stream. This requires clarification and is not silently reconciled.

## Completeness and integrity findings

- All 39 scenarios and trials 1–25 are present in every RPM group.
- At 25 RPM, Bearing 2 inner-race trials 1–3 use `Bearing (2) Fault (inner race)` while trials 4–25 use `Bearing (2) Fault (inner)`. This is a naming inconsistency, not a missing scenario.
- All 117 fully streamed representative records contain 64,000 logical data rows with timestamps from 0 to 9.99984375 seconds at 0.00015625-second spacing.
- Eleven representative files omit the final newline byte, but their final logical data row is present. Newline-byte counting alone should not be used as a row-integrity test.

## Preserved audit artifacts

- `archive_manifest.csv`: committed file-level manifest for all 2,925 CSVs; SHA-256 `2a9ba4cd41f8d9bdffc9078474ca7730efc99bafd83b5f53a34ba2a68943698a`.
- `external_data/arkansas_2023/representative_samples.zip`: Git-ignored six-file working subset; 28,261,803 bytes; SHA-256 `4e155aafb009f3dcf10a9d2d751f598b190cca5598055a25bc95333fa82690af`.

The representative subset includes healthy trial 1 at every RPM and, at 50 RPM, one single bearing fault, one cross-bearing double fault, and one bearing–bent-shaft double fault.

## Safe local cleanup boundary

The large original is exactly `external_data/arkansas_2023/22693120.zip`. It remains untouched and Git-ignored. If local disk recovery is needed, the user may delete that file manually after retaining the manifest and, if future spot checks are desired, `representative_samples.zip`. Deleting the original prevents deeper signal-level analysis without downloading it again.
