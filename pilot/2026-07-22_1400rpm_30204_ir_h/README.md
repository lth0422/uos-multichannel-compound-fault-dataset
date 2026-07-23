# 2026-07-22 UOS v2 Four-Sensor Crossover Pilot

## 목적

네 HS Sensors 13A131 가속도계와 NI-9234의 네 입력 채널이 네 후보 위치에서 정상적으로 진동과 물리 주파수 성분을 수집하는지 확인한다. 동일 조건에서 UOS v1 센서로 수집한 16 kHz MAT 신호도 참고 비교한다.

## 조건

| 항목 | 값 | 근거 |
|---|---|---|
| 회전속도 | nominal 1400 RPM | PILOT-S01; TDMS test property |
| 베어링 | 30204 tapered roller bearing | PILOT-S01; TDMS test property |
| 베어링 상태 | IR | PILOT-S01; 대부분의 TDMS metadata |
| 로터 상태 | H, healthy | PILOT-S01; TDMS test property |
| 새 수집계 | four HS Sensors 13A131 + NI-9234/cDAQ-9171 | PILOT-S01; TDMS channel properties |
| 새 수집률 | 25.6 kS/s | TDMS `wf_increment`와 test property |
| 새 기록 길이 | 약 59.6–60.4초 | TDMS sample count / `wf_increment` |
| 비교 수집계 | UOS v1 sensor, exact current acquisition interface Unknown | PILOT-S01; MAT filenames |
| 비교 수집률·길이 | 16 kHz, 80초, 1,280,000 points | PILOT-S01; MAT shape |

네 센서를 네 위치로 각각 옮겨 측정한 순차 4×4 교차시험이다. 한 파일에 네 채널이 동시에 들어 있는 측정이 아니다. 따라서 같은 위치에서 채널별 응답의 반복성을 비교할 수 있지만 위상, coherence, 동시성은 평가하지 않는다.

## 원자료 위치

Git에서 제외되는 로컬 경로는 다음과 같다.

```text
external_data/uos_v2_pilot/2026-07-22_1400rpm_30204_ir_h/
├── new_13a131_ni9234/UOS_Compare.zip
└── legacy_333d01_16khz/*.mat
```

ZIP은 압축 해제하지 않고 분석 코드가 내부 TDMS 16개를 직접 읽는다. 원자료를 Git에 추가하지 않는다.
원파일 동일성은 [`raw_manifest.sha256`](raw_manifest.sha256)으로 확인할 수 있다.

## 분석 재생성

Python 3.11 이상에서:

```bash
python -m pip install -e '.[analysis,test]'
python scripts/analyze_uos_pilot.py \
  --tdms-zip external_data/uos_v2_pilot/2026-07-22_1400rpm_30204_ir_h/new_13a131_ni9234/UOS_Compare.zip \
  --legacy-mat-dir external_data/uos_v2_pilot/2026-07-22_1400rpm_30204_ir_h/legacy_333d01_16khz \
  --output-dir pilot/2026-07-22_1400rpm_30204_ir_h/results \
  --rpm 1400
pytest
```

분석 설정과 선별 기준은 [`analysis_config.yaml`](analysis_config.yaml), 판정과 한계는 [`pilot_validation_report_ko.md`](pilot_validation_report_ko.md), 주장별 근거는 [`evidence.md`](evidence.md)에 기록한다. Bandwidth-matched comparison(동일 대역 비교)은 두 시스템 모두에 같은 7 kHz low-pass를 적용한 [`common_band_comparison.csv`](results/common_band_comparison.csv)와 Fig. 7–9에 저장한다.

UOS v2 본 수집의 조건별 synchronized four-channel master record는 60초로 수집한다. 25.6 kS/s를 사용할 경우 명목상 채널당 1,536,000 samples가 필요하다. 분석 window 길이와 안정화 제외 규칙은 아직 별도 검증 대상이다. 채널별 정확한 1×/BPFI peak는 [`peak_frequency_by_channel.csv`](results/peak_frequency_by_channel.csv)와 Fig. 10에서 확인한다.

## 알려진 메타데이터 정정

`Channel 0/ShaftEndTop/H_H_25600_30204_1400_1.tdms`는 파일명과 TDMS 내부 bearing fault가 `H`로 저장됐지만, 실험자가 실제 조건은 `IR`이며 입력 오타라고 2026-07-22 확인했다. 원파일은 수정하지 않고 분석 CSV에서 `metadata_conflict=Yes`, `bearing_fault_condition_used=IR`로 추적한다.
