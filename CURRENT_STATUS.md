# Current Status

## Current phase

Published dataset survey and evidence collection

## Completed

- Survey repository structure and templates bootstrapped
- Validation and comparison-table automation added
- Core ten dataset placeholders registered
- UOS v1 original dataset paper reviewed and first-pass card, facts, evidence, sources, and relevance analysis completed
- Paderborn original benchmark paper reviewed and first-pass card, facts, evidence, sources, and UOS v2 relevance analysis completed
- CWRU official Bearing Data Center documentation reviewed and first-pass card, facts, evidence, sources, and UOS v2 relevance analysis completed
- University of Arkansas 2023 Data in Brief paper reviewed and first-pass card, facts, evidence, sources, and UOS v2 relevance analysis completed
- Arkansas raw archive structure audited: 2,925 headers and 117 complete representative records checked; manifest and compact representative subset preserved
- MAFAULDA 2016 original publication and official web documentation reviewed; first-pass card, facts, evidence, sources, sensor-set comparison, and UOS v2 relevance analysis completed
- XJTU-SY original prognostics paper and supplied official README reviewed; first-pass card, facts, evidence, sources, and UOS v2 sampling/location implications completed
- NASA IMS official README, original paper, and supplied NASA catalog metadata reviewed; first-pass card, facts, evidence, sources, compound endpoint, and UOS v2 temporal-design implications completed
- Ottawa 2023 dedicated dataset paper reviewed; first-pass card, facts, evidence, sources, confound analysis, and UOS v2 sampling/placement implications completed
- Ottawa 2018 dedicated dataset paper reviewed; first-pass card, facts, evidence, sources, variable-speed analysis, and UOS v2 order-tracking implications completed
- PRONOSTIA original platform/challenge paper reviewed; first-pass card, facts, evidence, sources, natural compound analysis, and UOS v2 controlled-label implications completed
- Core-ten comparison synthesized into gap analysis, UOS v2 design implications, and a source-linked claim bank
- Current four-channel shaft-end/motor-end top/side layout recorded as a pilot candidate; legacy pre-purchase DAQ/mounting note audited and relocated
- Sampling-rate/record-length rationale and four-channel pilot validation protocol drafted from hardware constraints and survey evidence
- Purchased NI-9234/cDAQ-9171 and four HS 13A131 accelerometers recorded with preliminary specification and compatibility review
- NI-9234 native sampling-rate grid documented from the 13.1072 MHz timebase rule; 25.6 kS/s remains a primary pilot candidate, while 100 Hz is documented only as a processed derivative requiring explicit anti-alias filtering/resampling
- KAIST Batch dedicated Data in Brief paper reviewed and registered as an additional direct comparator; four simultaneous accelerometers at two bearing housings in x/y directions, 25.6 kHz vibration, and 60–2100-second record precedents documented
- Sensor-layout and sampling/record-length design notes updated: KAIST strongly supports the proposed geometry as a pilot candidate but does not validate UOS mounting surfaces or establish an optimal rate/duration
- HUST Vietnam dedicated Data Note reviewed and registered as a direct comparator; intentional IR+OR, IR+Ball, and OR+Ball defects, five bearing models, NI-9234 at 51.2 kHz, and 10-second steady/5-second run-up records documented
- Before S1 review, the internal-compound candidate gap was narrowed from pairwise combinations to a complete pairwise-plus-triple matrix; S1 subsequently established that the combination set itself already exists, so the current candidate is the broader matched multi-bearing/multi-RPM/timing/validation design recorded below
- SEU transfer-learning application paper reviewed; self-collected DDS subset registered separately from reused CWRU data, IR+OR Combination verified, and pooled bearing/gear `mixture` distinguished from same-sample compound faults
- HUST China benchmark/release paper and official HUSTbearing GitHub README reviewed; 25.6 kHz, 262,144-point/10.2-s records, ER-16K bearing, 9 health states, ten constant-speed conditions plus one 0-40-0 Hz time-varying condition, and IR+OR combination faults documented
- Internal dataset-comparison workbook and novelty working note reviewed and relocated under the ignored local design library; their unverified claims are explicitly separated from source-linked survey facts
- UOS v2 candidate-contribution review drafted: multi-channel/multi-position/compound/variable-RPM alone are not novelty claims; controlled compound matrix, paired channel-ablation protocol, timing metadata, physical validation, and confound-resistant metadata remain candidate gaps pending verification and pilot evidence
- S1 Data original PLOS ONE article reviewed and registered; five vibration axes at three positions, all three pairwise internal compounds plus the triple condition, 12 kHz/12,000-point groups at 2,000 RPM, and compound envelope analysis documented
- MCC5-THU dedicated Data in Brief article reviewed and registered; six vibration axes at two positions, speed/torque channels, 12.8 kHz/60-second variable-condition records, three severities, and broken-tooth+IR/OR bearing–gear compounds documented
- Candidate novelty narrowed after S1/MCC5 review: internal pairwise-plus-triple and broad multi-channel compound data are established precedents; matched references across bearing structures/RPMs with explicit timing, paired channel comparison, and release-wide validation remain candidates

## In progress

- UOS v1 official repository metadata and independent verification
- Paderborn official KAt-DataCenter metadata, README/fact sheets, and deposited MAT schema verification
- CWRU exact MAT record shape, optional base-channel coverage, timing architecture, release year, and license verification
- Arkansas article/header channel conflict, bearing specification, mounting, and hardware timing architecture verification
- MAFAULDA later dedicated-paper 여부, license, raw schema/version difference, and NI-9234 inter-module timing verification
- XJTU-SY official repository URL/version/license, raw schema, endpoint labels, DAQ, mounting, and channel timing verification
- NASA IMS snapshot-duration/cadence conflicts, DAQ timing, mounting, and third-party data-license applicability verification
- Ottawa 2023 repository license/schema, label typo, accelerometer direction, ADC timing, and full lifecycle-file availability verification
- Ottawa 2018 fault generation, load, mounting, sampling rationale, ADC timing, repository label, and license verification
- PRONOSTIA official challenge README/schema, bearing geometry, stopping criterion, endpoint damage, hardware timing, and license verification
- Remaining core dataset primary-source collection and fact verification
- Candidate UOS v2 contribution verification and four-channel placement/rate/duration pilot design
- Delivered 13A131 mounting/calibration documents and actual M5 magnet/adapter compatibility verification
- Delivered sensor documentation 확인 및 four-channel pilot compatibility test 준비
- KAIST Batch official repository schema/license, exact accelerometer attachment, cross-device timing, and NI module-role conflict verification
- HUST Vietnam Mendeley manifest, 99-record accounting, RPM values, MAT schema, mounting, chassis/timing, and dataset license verification
- SEU official repository documentation, raw acquisition schema, sensor/DAQ/mounting, sampling/duration, controller-setting interpretation, persistent access, and license verification
- HUSTbearing raw Excel schema, license, exact sensor/DAQ/mounting/channel details, and Supplementary Appendix B task mappings
- Full-text audit of the multi-channel fusion literature leads, including sensor taxonomy, split protocol, comparison baseline, quantitative result, and limitations
- S1 official supporting ZIP schema, exact sensor axes/models, DAQ, mounting, simultaneous timing, and license verification
- MCC5-THU official repository license/raw schema, 48-versus-112 transitional-condition conflict, DAQ, mounting, and timing verification

## Next actions

1. UOS v1 official repository metadata와 dataset license 독립 검증
2. CWRU file-level metadata 보강 및 Paderborn 공식 repository 자료 보강
3. closest compound comparators의 공식 repository 메타데이터 독립 검증
4. NI-9234/HS 13A131 primary documentation과 candidate bearing geometry 확정
5. existing four-channel 위치·방향 pilot protocol을 실제 rig 좌표·하중방향·mounting 정보로 구체화
6. candidate bearing geometry/RPM을 반영해 sampling rate·record length 계산 갱신
7. HUST Vietnam official repository metadata로 복합결함 matrix와 raw schema 독립 검증
8. 다채널 fusion literature lead 원문을 source-linked evidence로 전환하고, UOS v2 paired channel-ablation claim의 외부 근거 범위를 확정
9. S1 Data와 MCC5-THU 공식 deposit의 channel schema와 timing metadata를 확인해 차별성 표의 `?` 항목을 해소

## Open questions

- 조사 완료와 independent verification의 담당자 및 승인 절차
- 비교 실험에 필요한 paired-data 기준과 최소 메타데이터
- UOS v2 후보 센서 위치를 평가할 물리 근거와 pilot validation metric
- sampling rate, RPM 범위, record 길이를 결정할 최소 bandwidth·frequency-resolution·rotation-count 기준
- 13A131 제조사 원본 datasheet, 개별 calibration certificate, 정확한 NI-9234 connector variant
- SEU 등 남은 후보가 unresolved gap을 실제로 좁히는지와 추가 등록 우선순위
- 내부 비교 작업표의 값 중 source-linked survey와 충돌하거나 미검증인 항목의 처리 기준
- S1 Data의 5축 신호가 supporting ZIP 안에서 동시에 저장되는지와 정확한 축·열 순서
- MCC5-THU의 transitional condition 수가 48인지 112인지와 모든 8개 열의 공통 시간축 여부

## Blockers

- 핵심 10개 데이터셋의 1차 상세 검토가 완료됐으나 각 데이터셋의 독립 검증 및 일부 공식 repository 메타데이터가 남아 있음

## Last updated

2026-07-21
