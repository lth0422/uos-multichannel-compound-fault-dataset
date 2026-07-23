# UOS Multichannel Compound Fault Dataset

서울시립대학교 RTES Lab의 UOS Dataset v2를 설계하기 위해 공개 회전기계·베어링 데이터셋의 근거 조사부터 파일럿 수집·물리 검증까지 추적하는 private research repository입니다.

현재 단계는 **literature/dataset survey 결과를 유지하면서 UOS v2 pilot acquisition validation으로 전환하는 단계**입니다. 조건별 synchronized four-channel master record는 60초로 수집하기로 결정했으며, 최종 센서 위치·RPM·수집률·분석 window·contribution은 아직 확정하지 않습니다.

## Workflow

Survey → Evidence verification → Gap analysis → Dataset design → Pilot acquisition → Full acquisition → Validation → Dataset paper

## Repository policy

- 외부 raw dataset과 저작권이 있는 publisher PDF는 GitHub에 올리지 않습니다.
- 로컬 논문은 `library/papers/`, 기관 문서는 `library/documents/`에 두며 두 경로는 Git에서 제외됩니다.
- 데이터셋별 사실은 `facts.yaml`, 근거 추적은 `evidence.md`, 출처 메타데이터는 `sources.yaml`에 분리합니다.
- 확인되지 않은 값은 `Unknown`, 미작성 서술은 `TBD`, 목록은 빈 목록으로 유지합니다.

## Key directories

- `survey/datasets/`: 데이터셋별 조사 카드와 근거
- `survey/templates/`: 새 조사에 사용할 표준 템플릿
- `survey/synthesis/`: 비교표, claim bank, gap analysis
- `survey/schema/`: 구조 및 허용값 설명
- `library/`: commit하지 않는 로컬 문헌 배치 안내
- `references/`: BibTeX 및 DOI 인덱스
- `scripts/`, `tests/`: 검증 및 비교표 생성 자동화
- `paper/`: 근거가 확보된 뒤 작성할 dataset paper 작업 공간
- `design/`: 구매 장비 제약과 survey 근거를 연결하는 UOS v2 설계 기록
- `pilot/`: UOS v2 자체 파일럿의 설정, 근거, 분석 결과와 go/no-go 판정

## 파일 위치 안내

처음 저장소를 보는 사람은 다음 순서로 확인하면 됩니다.

| 찾는 내용 | 위치 | 설명 |
|---|---|---|
| 프로젝트의 확정·미확정 사항 | `PROJECT_CONTEXT.md` | 확인된 배경, 작업 가설, 아직 정하지 않은 설계 항목 |
| 현재 진행 상황 | `CURRENT_STATUS.md` | 완료 작업, 다음 작업, 질문과 blocker |
| 공개 데이터셋별 조사 결과 | `survey/datasets/<dataset_id>/` | `dataset_card.md`, `facts.yaml`, `evidence.md`, `sources.yaml`, UOS v2 관련성 |
| 데이터셋 전체 비교표 | `survey/synthesis/comparison_master.csv`, `.md` | 자동 생성되는 정형 비교표와 사람이 읽는 표 |
| UOS v2 설계 근거 | `design/` | 센서 위치, sampling rate, RPM, 기록 길이와 차별성 후보 |
| 파일럿별 안내·판정 | `pilot/<pilot_id>/README.md`, `pilot_validation_report_ko.md` | 실험 조건, 분석 결과, 한계와 본 수집 전 판단 |
| 파일럿 분석 설정 | `pilot/<pilot_id>/analysis_config.yaml` | 주파수 탐색 범위와 분석 파라미터 |
| 파일럿 수치 결과 CSV | `pilot/<pilot_id>/results/*.csv` | 채널·위치별 RMS, peak frequency, SNR 및 시스템 비교 수치 |
| 파일럿 그림 PNG | `pilot/<pilot_id>/results/figures/*.png` | 원신호, FFT, envelope spectrum, RMS 및 peak 비교 그림 |
| 파일럿 분석 코드 | `scripts/analyze_uos_pilot.py` | 로컬 원자료에서 CSV와 PNG를 재생성하는 코드 |
| 검증·표 생성 코드 | `scripts/check_dataset_cards.py`, `scripts/build_comparison_table.py` | 조사 파일 검증과 전체 비교표 생성 |
| 자동화 테스트 | `tests/` | 조사 schema, 비교표 및 파일럿 분석 코드 테스트 |
| 로컬 논문·공식 문서 | `library/papers/`, `library/documents/` | Git에 올리지 않는 참고문헌 원문 |
| 로컬 원시 측정 데이터 | `external_data/` | Git에 올리지 않는 TDMS, MAT, ZIP 등 |

현재 파일럿의 결과는
`pilot/2026-07-22_1400rpm_30204_ir_h/`에 있습니다. 핵심 해석은
`pilot_validation_report_ko.md`, 채널별 실제 1×·BPFI peak 주파수는
`results/peak_frequency_by_channel.csv`, 겹침을 분리해 표시한 그림은
`results/figures/10_peak_frequency_by_channel.png`에서 확인할 수 있습니다.

`results/`의 CSV와 PNG는 분석 코드로 재생성할 수 있는 결과물입니다. 반면
`external_data/`의 원자료는 크기와 라이선스 문제로 로컬에만 보관하며 commit하지
않습니다.

## Commands

Python 3.11 이상에서 다음을 실행합니다.

```bash
python -m pip install -e '.[test]'
python scripts/check_dataset_cards.py
python scripts/build_comparison_table.py
pytest
```

비교표 생성 명령은 `survey/dataset_registry.csv`의 행 순서와 priority를 사용해 `survey/synthesis/comparison_master.csv` 및 `.md`를 갱신합니다.

UOS v2 파일럿 분석 dependency와 현재 1400 RPM 파일럿 재생성 방법은 [`pilot/2026-07-22_1400rpm_30204_ir_h/README.md`](pilot/2026-07-22_1400rpm_30204_ir_h/README.md)에 기록되어 있습니다. 원시 TDMS/MAT/ZIP은 `external_data/uos_v2_pilot/`에 두며 Git에 포함하지 않습니다.
