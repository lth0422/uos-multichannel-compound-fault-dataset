# UOS Dataset v2 후보 차별성 및 연구 공백 검토

## 목적과 판정 상태

이 문서는 UOS Dataset v2가 논문에서 주장할 수 **있을지도 모르는** 차별성을, 현재까지 검토된 데이터셋 증거와 내부 참고자료에 대조해 정리한다. 이는 contribution 확정 문서가 아니다. 최종 논문에는 각 후보가 공식 원문·공식 repository·pilot 결과로 다시 검증된 뒤에만 반영한다.

현재 후보 수집 계획의 센서 위치, 채널 수, sampling rate, RPM, record 길이, 결함 조합과 반복 수는 모두 미확정이다. 특히 4채널 top/side × shaft-end/motor-end 배치와 25.6 kS/s는 **pilot 후보**이지 이미 확정된 데이터셋 특성이 아니다.

## 현재 결론

UOS v2가 `다채널`, `다위치`, `복합결함`, 또는 `가변 RPM`을 제공한다는 사실만으로는 novelty를 주장할 수 없다. 각 요소의 선례가 이미 확인되어 있다. 남아 있는 가능성은 개별 요소가 아니라, 아래 요소를 같은 물리 run·동일 메타데이터 체계·동일 검증 규약으로 결합하고 공개하는 데 있다.

1. 순수 결함을 대조군으로 갖는 통제된 internal-bearing pairwise-plus-triple 결함 행렬
2. 위 internal-bearing 행렬과 unbalance·misalignment·looseness를 분리 가능한 요인으로 연결한 bearing–rotor 복합 설계
3. 동일 synchronized vibration record에서 파생한 canonical single-channel 및 multi-channel 입력과, 물리 run 기준 split 규약
4. 장비 timing, 센서 위치·방향·mounting, 채널 mapping을 재현 가능하게 공개하고 실제 timing/response를 확인하는 절차
5. 결함 기하·RPM·envelope/order spectrum·반복성·사후 점검을 함께 사용하는 compound-label 물리 검증
6. bearing ID, assembly/remount, load, RPM, acquisition order를 기록하여 label confounding과 window leakage를 방지하는 metadata 설계

위 여섯 항목은 모두 **candidate contribution**이다. 어느 하나도 현재 상태에서 보편적 최초성 또는 성능 우위를 뜻하지 않는다.

## 기존 데이터셋과의 대조

| 후보 주장 | 이미 확인된 선례 | 따라서 주장할 수 없는 것 | 남는 후보 차별성 | 상태 |
|---|---|---|---|---|
| 두 bearing housing의 여러 진동 채널 | KAIST Batch는 two housing × x/y의 동시 4 accelerometer layout을 제공한다. CWRU, NASA IMS, MAFAULDA, Arkansas도 여러 위치의 진동 측정 선례를 가진다. [CB-01] | “4채널”, “두 위치”, “다위치 진동” 자체가 신규라는 주장 | 동일 physical run에서 고정된 channel subset을 제공하고, single-/multi-channel ablation과 split 규약을 미리 정의 | Candidate [CB-08] |
| internal bearing compound fault | HUST Vietnam은 IR+OR, IR+Ball, OR+Ball을 의도적으로 제공하며, SEU는 IR+OR class를 제공한다. Paderborn, NASA IMS, Arkansas, PRONOSTIA에도 복합 손상 선례가 있다. [CB-02] | pairwise internal compound가 최초라는 주장 | matched healthy/pure reference와 함께, 결함 severity·bearing ID·replicate 정의가 분명한 pairwise + IR+OR+Ball 행렬 | Candidate [CB-07] |
| bearing–rotor compound | UOS v1, MAFAULDA, Arkansas에 bearing과 rotor-system 결함이 함께 나타나는 선례가 있다. [CB-03] | bearing–rotor compound 자체가 새롭다는 주장 | 내부 베어링 결함 축과 unbalance/misalignment/looseness 축을 같은 설계 안에서 분리·교차시키는 요인 설계 | Candidate [CB-09] |
| synchronized acquisition | KAIST는 simultaneous 4-channel layout을 명시한다. 여러 데이터셋은 공통 record를 제공하지만 ADC topology/skew를 충분히 쓰지 않는 경우가 있다. [G4] | “동시 수집”이라는 단어만으로의 신규성 | NI-9234 기반 timing architecture, 채널 mapping, start alignment, skew/상한, filter/group delay를 실제로 기록·검증 | Candidate [G4] |
| 물리 기반 결함 검증 | UOS v1, Paderborn, NASA IMS 등은 characteristic frequency 또는 envelope 근거를 사용한다. [G5] | FFT/envelope 그림 하나만으로 validation이 신규라는 주장 | 모든 pure/compound condition을 대상으로 사전 정의한 기하 기반 주파수·RPM tolerance·quality check·repeatability·사후 점검을 연결 | Candidate [CB-10] |
| 여러 RPM/하중 조건 | Ottawa 2018은 record 내부에서 RPM을 변화시키며, 여러 benchmark가 fixed RPM 또는 load 조건을 변화시킨다. [CB-04; G6] | “가변 운전조건” 자체가 신규라는 주장 | fault, bearing batch, RPM, load, acquisition order가 서로 label shortcut이 되지 않도록 균형 또는 block 구조와 metadata를 공개 | Candidate [G6] |

`CB-*`는 [claim_bank.md](../survey/synthesis/claim_bank.md), `G*`는 [gap_analysis.md](../survey/synthesis/gap_analysis.md)의 source-linked claim/gap ID를 가리킨다. 해당 문서의 모든 결론도 reviewed sources 범위 안에서만 유효하다.

## 다채널의 연구 필요성과 주장 경계

다채널 신호에는 위치·방향별 전달경로 차이, 국부 noise, load-zone 영향, 장착 상태 차이 때문에 상호보완적 정보가 있을 수 있다. 하지만 이것은 UOS v2의 데이터셋 수준에서 아직 검증해야 할 가설이다.

- MAFAULDA에는 특정 ANN feature 실험에서 one-versus-two bearing sensor-set 비교가 보고되어 있다. 이는 해당 실험 설정의 근거일 뿐, 모든 모델·결함·센서 배치에서 multi-channel이 항상 우수하다는 증명은 아니다. [CB-06]
- 내부 참고 메모는 다채널 fusion 관련 후속 논문 후보를 제시한다. 그러나 원문 전문, 데이터셋, split, 비교 대상, 수치 산출 조건을 아직 이 저장소에서 검토하지 않았으므로 그 정확도 수치나 일반화 결론을 논문 claim으로 사용하지 않는다. [LOCAL-NOV-01]
- UOS v2의 유효한 검증 질문은 “4채널이 1채널보다 항상 좋은가?”가 아니라, **동일한 physical run에서 어떤 위치·방향 조합이 어떤 결함·RPM·노이즈 조건에서 보완적 정보를 제공하는가**이다.

따라서 향후 benchmark에는 최소한 다음을 함께 제시한다.

1. 고정 single-channel baseline: 각 CH1–CH4를 독립적으로 평가
2. 위치별 pair와 4-channel 조합: 같은 물리 record에서 파생
3. 동일 model family, 동일 split, 동일 window/feature budget 비교
4. 평균 성능뿐 아니라 condition별 성능, variance, channel failure/ablation 결과
5. window-level 분할이 아닌 physical acquisition run, bearing instance, remount 또는 assembly 기준 분할

성능 향상 수치는 이 비교가 실제로 완료된 뒤에만 기록한다.

## 복합결함 후보의 주장 경계

복합결함은 같은 sample/physical condition에 둘 이상의 결함이 실제로 존재할 때만 인정한다. 서로 다른 단일결함 record를 단순히 병합하거나, 여러 class가 한 dataset 안에 있다는 사실은 compound condition의 증거가 아니다.

UOS v2에서 검토할 수 있는 최소 대조 구조는 다음과 같다.

| 축 | 필요한 대조군 | 검증해야 할 점 |
|---|---|---|
| Internal bearing | healthy, IR, OR, Ball, IR+OR, IR+Ball, OR+Ball, IR+OR+Ball | 같은 bearing type·severity 정책·RPM/load·assembly 조건에서 component labels와 결함 기하가 추적되는가 |
| Rotor system | healthy, unbalance, misalignment, looseness | 각 rotor condition의 설치/정렬/질량/체결 상태가 독립 metadata로 남는가 |
| Bearing–rotor | pure bearing, pure rotor, 결합 condition | 결합 label이 같은 physical run에서 성립하고, 순수 대조군과 비교 가능한가 |

이는 권장 설계이지 확정 수집 범위가 아니다. 특히 triple internal compound와 모든 bearing–rotor 교차조합은 조립 가능성, 안전성, 재현성, 사후 점검을 pilot으로 통과한 경우에만 채택한다.

## 내부 비교자료의 활용 범위

다음 세 파일은 현재 `library/documents/design/novelty/`에 보관했다. Git-ignore 대상의 로컬 참고자료이며, 최종 근거 저장소가 아니다.

| Local ID | 파일 | 역할 | 사용 제한 |
|---|---|---|---|
| LOCAL-NOV-01 | `multichannel_literature_leads.csv` | 다채널 fusion 관련 논문 후보와 URL 목록 | 원문을 읽고 source ID·page/table/figure를 등록하기 전에는 수치나 결론을 인용하지 않음 |
| LOCAL-NOV-02 | `dataset_competitiveness_working_matrix.xlsx` | dataset 후보를 빠르게 비교하는 내부 작업표 | 각 O/X, 채널 수, 공개 여부를 독립 증거로 취급하지 않음 |
| LOCAL-NOV-03 | `dataset_construction_necessity_working_note.pdf` | 다채널·복합결함 필요성을 정리한 내부 메모 | 인용문헌의 원문 확인 전에는 해석 초안으로만 사용 |

작업표를 현재 survey와 대조했을 때의 주의점은 다음과 같다.

- UOS v2의 채널 수·sampling rate·RPM·bearing 구성은 작업표에 적힌 값이 있어도 아직 설계 후보다. 최종 facts로 승격하지 않는다.
- `bearing count/type`, `sensor position count`, `vibration channel count`, `total recorded channel count`는 별도 열이어야 한다. 예를 들어 비진동 modality까지 포함한 총 채널 수로 multi-channel vibration을 판단하면 안 된다.
- 공개 여부가 불명확하거나 비공개 comparator는 research-gap의 부재를 입증하는 증거로 사용하지 않는다.
- 복합결함 O/X는 same-sample 여부, 결함 조합, 의도성, severity, pure control을 별도로 확인해야 한다.
- 작업표의 HUST/MAFAULDA/Arkansas/KAIST/Paderborn 값은 현재 survey card의 source-linked facts와 충돌할 수 있으므로, 이후 변경은 `facts.yaml`과 `evidence.md`를 기준으로 한다.

## 논문에서 사용할 수 있는 표현 초안

다음은 검증이 진행될 때까지 안전한 표현이다.

- “UOS Dataset v2 is designed to investigate whether synchronized multi-position vibration offers complementary diagnostic information under controlled conditions.”
- “The dataset design targets a candidate gap: matched pure, internal-bearing compound, and bearing–rotor compound conditions with traceable acquisition metadata.”
- “Paired channel subsets are intended to enable controlled single- versus multi-channel evaluation; no universal performance advantage is assumed.”
- “Final sensor placement, sampling rate, record duration, and fault matrix will be selected after hardware and pilot validation.”

피해야 할 표현은 다음과 같다.

- “The first/only/best multi-channel compound-fault dataset”
- “Multi-channel data outperform single-channel data”
- “Existing datasets lack compound faults”
- “The proposed four-channel layout is optimal”

## Claim 확정 전 증거 게이트

| Gate | 필요한 증거 | 통과 전 상태 |
|---|---|---|
| G-A: closest comparator audit | HUST Vietnam, Arkansas, MAFAULDA, Paderborn, KAIST, UOS v1의 공식 repository와 원문에서 compound matrix·채널·metadata를 재확인 | Candidate gap |
| G-B: multi-channel literature audit | LOCAL-NOV-01의 각 논문을 원문 기준으로 dataset, sensor modality/position, split, baseline, 성능 수치, 한계를 evidence table에 기록 | Literature lead only |
| G-C: timing and layout pilot | NI-9234 task 설정, channel mapping, timing, mounting/remount, noise/clipping, coherence 및 위치별 fault visibility 측정 | Candidate acquisition architecture |
| G-D: factorial/confound pilot | bearing ID, assembly, fault, RPM, load, acquisition order를 분리해 pure/compound repeat를 획득 | Candidate dataset design |
| G-E: physical label validation | defect geometry, measured RPM, envelope/order spectrum, repeatability, 사후 점검을 condition별로 연결 | Candidate validation contribution |
| G-F: paired benchmark | physical-run grouped split에서 single-/multi-channel ablation을 동일 조건으로 수행 | Candidate performance claim |

## 다음 자료 우선순위

1. `LOCAL-NOV-01`에 적힌 다채널 fusion 논문의 원문 또는 저자 공개본을 추가한다. 각 논문은 별도 source ID로 등록하고, fusion이 multi-position vibration인지 multi-modal인지부터 분리한다.
2. 가장 가까운 공개 comparator의 공식 metadata를 확인한다. 우선순위는 HUST Vietnam, Arkansas, MAFAULDA, KAIST Batch, Paderborn, UOS v1이다.
3. UOS rig의 실제 bearing geometry, fault 제작 방식, load direction, tachometer/RPM 측정 방식을 확정해 물리 주파수 표와 label-validation plan을 작성한다.
4. 4채널 배치와 25.6 kS/s/record-length 후보는 [pilot_validation_protocol.md](pilot_validation_protocol.md)의 pilot으로 판정한다. 수집 software의 30초 파일 단위와 안정화 파일 처리 규칙도 이 단계에서 metadata로 고정한다.

## Evidence references

- [claim_bank.md](../survey/synthesis/claim_bank.md): CB-01–CB-10과 각 dataset evidence ID
- [gap_analysis.md](../survey/synthesis/gap_analysis.md): G1–G6의 범위·한계·추가 검증 항목
- [implications_for_uos_v2.md](../survey/synthesis/implications_for_uos_v2.md): pilot design requirements와 decision gates
- [comparison_master.md](../survey/synthesis/comparison_master.md): 현재 14개 dataset의 source-linked 비교 결과(모든 row는 `needs_review`)
- LOCAL-NOV-01–03: 위 표에 정의한 로컬 working references; primary evidence가 아님

Last reviewed: 2026-07-20
