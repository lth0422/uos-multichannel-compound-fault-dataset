# Current Status

## Current phase

UOS v2 pilot acquisition validation, with published-dataset survey retained as design evidence

## Completed

- 2026-08-04 N204·1600 RPM·IR+OR+B의 H·L·M3·U3에서 12.8·17.0667·25.6 kHz 비교를 수행했다. 공회전 60초 제외 후 rate별 3,072,000표본을 사용했으며 TDMS 실제 rate와 metadata가 설정값에 일치함을 확인했다.
- 2026-08-04 exact rail 표본은 12.8 kHz 5개, 17.0667 kHz 25개, 25.6 kHz 1,252개로 증가했으나 세 rate 모두 4/4파일에 rail이 존재했다. rate 증가가 저장된 clipping 빈도에 영향을 주지만 낮은 rate만으로 clipping이 제거되지 않는다고 판단했다.
- 2026-08-03 다중 필터 대역 분석을 최대충격 주변 10초 중심에서 공회전 제외 120초 전체 g값 분포 중심으로 개편했다. 채널·필터·대역별 RMS, p90~p99.99, crest factor, 10~50 g 초과율과 전체/베어링/RPM별 histogram을 생성했다.
- 2026-08-03 Butterworth 120초 분포에서 2~7 kHz는 7채널·22표본, 7~10 kHz는 1채널·1표본이 50 g를 넘었으며, 전체 표본 대비 각각 약 0.0000156%와 0.0000007%임을 확인했다. 필터 출력 peak는 실제 clipping 이전 센서 입력의 복원값이 아님을 유지했다.
- 2026-08-03 사용자 확인에 따라 일반 파일의 60~180초와 30204·7분 초과 파일의 300~420초만 유효 측정구간으로 정하고, 공회전과 뒤 잔여 구간을 제외해 모든 클리핑·대역·포락선 분석을 재생성했다.
- 2026-08-03 공회전 제외 후 ADC rail은 2,675표본·45/116파일이며, 건강·단일 결함 0/56파일과 복합 결함 45/60파일에서 나타남을 확인했다.
- 2026-08-03 30204·6204·N204의 1400·1600 RPM·IR+OR+B 조건 중 ±50 g 초과 46채널에 Butterworth·Chebyshev I·II·Elliptic·Bessel과 5개 주파수 구간을 적용했다.
- 2026-08-03 최대충격 주변 10초 분석에서는 2~7 kHz 단일 채널만 필터 3종에서 50 g를 넘었으나, 120초 전체 분포 분석에서 다른 시각의 대역 peak가 추가로 확인됨을 정정했다. IR·OR 계열은 2~7 kHz, B 계열은 7~10 kHz 검출이 상대적으로 높으며 필터 후 최대값은 센서 입력 진폭 판정에 사용할 수 없음을 문서화했다.
- 2026-08-03 46채널의 누적 저역통과 시나리오를 추가했다. 10 kHz 저역통과 후 필터별 1~11채널, 필터 3/5 다수결 기준 11채널이 50 g를 넘었으며, 7 kHz 저역통과 후에는 다수결 기준 N204·1600 RPM·H·IR+OR+B·CH0 한 채널만 남았다.
- 2026-08-03 S1-S01의 식 (1)~(9)과 Fig. 11~14를 기준으로 BPFO/BPFI/BSF 고조파, BPFI±1×, BSF±FTF 계열을 고유 116파일 전체에서 분석했다.
- 2026-08-03 30204·1600 RPM의 단일-복합 결함을 동일 로터·채널끼리 비교하고 주파수 중첩을 표시했으며, Task B 대표 파일 오류와 L1/L2/L3 결과를 원자료 기준으로 정정했다.
- 2026-08-03 ADC 포화 보고서를 베어링·RPM·베어링 결함·로터 조건·채널 수가 드러나도록 전면 개정하고, 베어링 정상(H)과 기계 전체 정상을 구분했다.
- 2026-08-03 BPFO·BPFI·BSF 결과를 조건별로 분리하고, 한국어 그래프와 축·분모·색상·해석 범위 설명을 추가했다.
- 2026-08-01 현재 수집 TDMS 124경로를 검사하고 SHA-256 동일 중복 8쌍을 제외한 고유 116파일의 clipping을 전수 재분석했다.
- 초기 전체 기록 검사에서 ADC rail 4,709표본을 확인했으나, 공회전·뒤 잔여 구간을 제외한 최종 판정값은 2,675표본임을 정정하고 대표 8조건 LPF sweep을 재생성했다.
- UOS v1 원논문 Table 2의 geometry로 6204·N204/NJ204·30204 결함주파수를 계산하고 세 베어링 envelope check를 생성했다.
- 클리핑 작업지시서의 주장과 한계를 `validation/clipping_2026-08-01/clipping_assessment_ko.md`에 정리했다.

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
- First UOS v2 acquisition pilot organized and analyzed: 30204 IR, healthy rotor, nominal 1400 RPM; four HS 13A131/NI-9234 channels were sequentially crossed over four shaft-end/motor-end top/side positions
- Pilot raw files relocated under ignored `external_data/uos_v2_pilot/`; reproducible TDMS/MAT analysis, characteristic-frequency calculation, CSV outputs, six figures, tests, evidence table, and Korean validation report added under `pilot/`
- All 16 new-system runs passed exploratory finite/range/shaft/BPFI-envelope screens; same-position RMS CV was 2.06–3.92%, and all channels showed the 23.25 Hz shaft peak and approximately 205.25–205.50 Hz BPFI envelope peak
- CH0 ShaftEndTop raw `H_H` label recorded as a user-confirmed metadata typo; raw data preserved and analysis audit fields retain the conflict
- New-versus-legacy comparison was repeated with identical 0–7 kHz filtering and absolute 1×/BPFI peak amplitudes: bandwidth matching reduces RMS ratios from 1.19–2.12 to 0.97–1.41, while 1× ratios are 1.02–1.24; bandwidth is a major but incomplete explanation and a gross factor-of-two calibration error is not supported
- Per-condition synchronized four-channel master acquisition duration set to 60 seconds; canonical analysis-window length, overlap, stabilization exclusion, and release derivatives remain open
- Exact per-channel peak-frequency CSV and a horizontally offset plot added because overlaid spectra hide coincident channel peaks; all 16 new-system runs show 23.25 Hz shaft peaks and 205.25 or 205.50 Hz BPFI envelope peaks

## In progress

- 2026-08-01 clipping 결과의 원인 분리를 위한 보유 장비 반복·재부착·센서/DAQ 채널 교차시험 및 rail-event 전후 baseline 개별 검토
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
- Candidate UOS v2 contribution verification and follow-up simultaneous four-channel placement/rate/duration pilot
- Delivered 13A131 mounting/calibration documents and actual M5 magnet/adapter compatibility verification
- Delivered sensor documentation 확인 및 four-channel pilot compatibility test 준비
- KAIST Batch official repository schema/license, exact accelerometer attachment, cross-device timing, and NI module-role conflict verification
- HUST Vietnam Mendeley manifest, 99-record accounting, RPM values, MAT schema, mounting, chassis/timing, and dataset license verification
- SEU official repository documentation, raw acquisition schema, sensor/DAQ/mounting, sampling/duration, controller-setting interpretation, persistent access, and license verification
- HUSTbearing raw Excel schema, license, exact sensor/DAQ/mounting/channel details, and Supplementary Appendix B task mappings
- Full-text audit of the multi-channel fusion literature leads, including sensor taxonomy, split protocol, comparison baseline, quantitative result, and limitations
- S1 official supporting ZIP schema, exact sensor axes/models, DAQ, mounting, simultaneous timing, and license verification
- MCC5-THU official repository license/raw schema, 48-versus-112 transitional-condition conflict, DAQ, mounting, and timing verification
- First pilot follow-up: simultaneous four-channel healthy/IR runs over multiple RPMs, repeat/remount runs, tachometer alignment, and severe-condition clipping headroom

## Next actions

1. N204/1600/M3/IR+OR+B와 건강 대조에서 동일 장비로 완전 재부착 3회 반복
2. 센서 개체–DAQ 채널–물리 위치를 교차하여 clipping 원인의 상대 기여 분리
3. stud 부착이 현재 보유 부품으로 가능하면 현재 mounting과 같은 조건에서 비교
4. 자동 zero-shift suspect 채널의 rail-event 전후 baseline을 개별 검토하고 판정법 확정
5. 위 결과 전까지 신규 대규모 조건 수집과 hardware 변경 결정을 보류
6. 향후 수집에 tachometer/실측 RPM과 sensor serial–DAQ channel–position manifest 저장
7. 실제 포화 이전 절대진폭이 연구에 필수이고 rail이 계속될 때만 저감도 reference를 검토
8. NI-9234/HS 13A131 primary documentation과 calibration certificate 확인

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
- Full acquisition 전에 통과해야 할 channel-gain, mounting-repeatability, target-SNR, clipping-margin 수치 기준
- 60초 기록의 안정화 제외를 고정 30초로 할지, tachometer/RMS 기반 조건부 규칙으로 할지

## Blockers

- 현재 100 mV/g·±50 g 센서와 약 ±5.12 V DAQ rail이 같은 지점에 있어, 이미 clipping된 신호만으로 실제 50 g 초과 진폭과 mounting 기여도를 분리할 수 없음
- rail 유무만으로 현재 전체 116파일의 복합 결함 여부를 87.1%, 균형적인 30204/1600 subset을 92.2% 맞힐 수 있어 raw ML benchmark에는 label shortcut 교란이 존재함
- 첫 파일럿은 순차 단일채널·단일 RPM·단일 IR 조건이므로 동시 4채널 complementarity, RPM trend, healthy 대비, remount repeatability를 아직 검증하지 못함
- 핵심 데이터셋의 1차 상세 검토는 완료됐으나 independent verification과 일부 공식 repository 메타데이터가 남아 있음

## Last updated

2026-08-04
