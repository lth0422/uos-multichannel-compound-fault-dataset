# UOS v2 본 수집 검증 규칙

## 1. 목적

- 새 TDMS가 추가될 때마다 동일한 절차로 파일 형식·진폭·회전주파수·베어링 결함주파수를 점검함
- 수집 묶음별 결과를 `runs/`에 보존하고 전체 상태를 `index.md`에서 누적 관리함
- 자동 검출 결과와 연구자의 최종 판정을 구분함

## 2. 원자료와 결과물 위치

- 원자료: `dataset/uosv2/수집 데이터/`
- 검증 코드: `scripts/validate_uos_v2_acquisition.py`
- 수집 묶음별 결과: `validation/acquisition/runs/<run_id>/`
- 전체 진행표: `validation/acquisition/index.md`
- 원시 TDMS는 Git에 포함하지 않음
- CSV·PNG·Markdown 검증 결과만 Git에서 관리함

## 3. 결함 레이블 규칙

결함 레이블은 반드시 다음 순서를 사용함.

```text
{로터결함}_{베어링결함}
```

허용하는 로터 결함 레이블은 다음과 같음.

- `H`: 로터 정상
- `M1`, `M2`, `M3`: misalignment 조건
- `U1`, `U2`, `U3`: unbalance 조건
- `L`: looseness 조건

허용하는 베어링 결함 레이블은 다음과 같음.

- `H`: 베어링 정상
- `IR`: 내륜 결함
- `OR`: 외륜 결함
- `B`: 볼 또는 롤러 결함
- `IR+OR`, `IR+B`, `OR+B`: 2중 내부 복합 결함
- `IR+OR+B`: 3중 내부 복합 결함

예시는 다음과 같음.

| 결함 레이블 | 의미 |
|---|---|
| `H_H` | 로터 정상·베어링 정상 |
| `H_IR` | 로터 정상·베어링 내륜 결함 |
| `M2_H` | M2 로터 오정렬·베어링 정상 |
| `U3_IR+OR` | U3 로터 불균형·베어링 IR+OR 복합 결함 |
| `L_IR+OR+B` | 로터 looseness·베어링 3중 내부 복합 결함 |

`H`를 단독 레이블로 사용하지 않음. 첫 번째 `H`와 두 번째 `H`의 대상을 혼동하지 않도록 항상 두 부분을 함께 기록함.

## 4. TDMS 파일명 규칙

```text
{로터결함}_{베어링결함}_{sampling_rate}_{bearing_model}_{rpm}[_repeat].tdms
```

예시는 다음과 같음.

```text
H_IR_25600_6204_600.tdms
M2_IR+OR_25600_N204_1000.tdms
H_IR+OR_25600_N204_1600_2.tdms
```

- `sampling_rate`: Hz 단위 정수 사용을 원칙으로 함
- `bearing_model`: `6204`, `N204`, `NJ204`, `30204` 중 하나를 사용함
- `rpm`: 명목 회전속도를 정수로 기록함
- `_repeat`: 동일 조건 재측정에서만 `_2`, `_3` 순으로 추가함
- 파일명 레이블과 TDMS 내부 metadata가 다르면 `Needs review`로 처리함

## 5. 수집 묶음과 폴더명

한 번에 함께 검토할 조건을 하나의 수집 묶음으로 정의함. TDMS 하나마다 보고서를 만들지 않음.

```text
validation/acquisition/runs/YYYY-MM-DD_{bearing}_{bearing-fault}_{rpm-range}/
```

예시는 다음과 같음.

```text
validation/acquisition/runs/2026-09-10_6204_IR_600-1600rpm/
```

각 수집 묶음에는 다음 결과를 생성함.

- `validation_report_ko.md`: 조건, 핵심 결과, 이상 항목과 판정
- `results/input_manifest.csv`: 실제 입력 파일과 분석 구간
- `results/file_channel_metrics.csv`: sample 수, RMS, peak, rail, 1X
- `results/frequency_detection_detail.csv`: 모든 예상·관찰 주파수와 주변 잡음 대비 dB
- `results/component_detection_summary.csv`: 채널별 1X·IR·OR·B 요약
- `results/fft_component_summary.csv`: 원신호 FFT와 포락선 FFT의 구성 결함별 고조파 검출 채널 수
- `results/ch0_envelope_reference_frequencies.csv`: CH0 포락선 그림에 표시한 1X·결함 고조파·복합 결함 합차 후보
- `results/rms_rpm_trend.csv`: 같은 조건의 RPM별 RMS 변화
- `figures/`: clipping, RMS–RPM, 결함주파수 요약 그림

### 최종 판정 원칙

- 주 판정 항목은 48조건 완전성, 4채널·시간축, 25.6 kHz, 120초 길이, 진폭 범위, RMS의 전체적인 RPM 경향과 회전주파수 1X로 정함
- RPM별 RMS가 매 단계 단조 증가할 것을 요구하지 않고, 동일 로터·채널에서 고속 RMS가 저속 RMS보다 대체로 높은지 확인함
- 일부 채널에서 1X 자동 기준을 통과하지 못해도 같은 파일의 다른 채널에서 회전 성분이 확인되면 파일 전체 누락으로 판정하지 않음
- 결함주파수는 베어링 충격, 전달경로와 공진 영향으로 모든 조건에서 뚜렷하지 않을 수 있으므로 보조 검증으로 관리함
- 복합 결함은 구성 단일 결함의 주파수와 쌍별 합·차 주파수 후보를 기록하되, 합·차 성분 하나만으로 복합 결함을 확정하지 않음
- 희소한 단일 rail과 짧은 rail 구간은 위치와 비율을 명시하고 보완사항으로 관리함. 반복적이거나 긴 포화가 분석을 지배하면 재측정 대상으로 올림

## 6. 기본 분석 단위

- 본 수집 후보 sampling rate: 25.6 kHz
- 원파일 목표 길이: 공회전 60초와 유효 진동 120초를 포함한 조건당 180초 이상
- 모든 본 수집 검증: 원파일 앞 60초를 제외하고 이후 120초를 사용함
- 25.6 kHz에서 유효 구간의 표본 수: 채널당 3,072,000개, 4채널 합계 12,288,000개
- 원파일이 180초를 초과해도 기본 검증은 60~180초만 사용하고 실제 구간을 `input_manifest.csv`에 기록함
- 4채널은 같은 시점의 공동 측정값이므로 표본 수를 네 배의 독립 관측으로 해석하지 않음

하루 수집·검증 묶음은 `베어링 모델 1종 × 베어링 결함 1종 × RPM 6종 × 로터 조건 8종 = 48파일`로 구성함. RPM은 `600, 800, 1000, 1200, 1400, 1600`을 모두 사용함. 48파일이 채워지지 않은 묶음은 `Incomplete`로 기록함.

## 7. 검증 항목

### 7.1 파일과 시간축

- TDMS 파일명 파싱 여부 확인
- 4채널 존재 여부 확인
- 채널별 sample 수 일치 여부 확인
- 채널별 sampling rate 일치 여부 확인
- 파일명 rate와 TDMS 실제 rate 일치 여부 확인
- 4채널 시작시각 일치 여부 확인
- 요청한 분석 길이의 sample 수 확보 여부 확인

### 7.2 Clipping

- 저장 가속도값이 센서 명목 측정 범위인 ±50 g를 초과하는 표본 수와 비율을 계산함
- 약 ±5.10 V 입력 한계 접근 표본 수 계산
- 기존 전수조사에서 확인한 채널별 반복 저장 rail 표본 수 계산
- ±50 g 초과는 센서 명목 범위 검사이며, 특정 반복 저장값과 일치하는 rail 판정과 구분함
- `rail 표본 수 / 분석한 전체 진동 표본 수 × 100`으로 clipping 비율 계산
- rail이 0이면 clipping screen `Pass` 후보로 기록함
- rail이 1개 이상이면 자동 폐기하지 않고 발생 채널·연속 길이·레이블 편중을 검토함
- clipping 처리 정책이 확정되기 전에는 rail 발생 자료를 최종 `Pass`로 처리하지 않음

### 7.3 RMS와 RPM

- 같은 베어링·결함 레이블·채널·반복번호끼리만 비교함
- RPM별 RMS, Spearman 상관계수, 증가 여부를 기록함
- 높은 RPM에서 RMS가 항상 증가해야 한다는 절대 합격 기준으로 사용하지 않음
- 비단조 변화가 나타나면 체결, 부착, 로터 상태, 운전 안정성과 실제 RPM을 함께 점검함

### 7.4 회전주파수

- 원신호 FFT에서 명목 `RPM/60` 주변의 1X 후보를 확인함
- 예상 주파수, 관찰 주파수, 오차, 주변 잡음 대비 dB를 기록함
- tachometer가 없으므로 진동에서 찾은 1X를 실측 RPM으로 단정하지 않음

### 7.5 베어링 결함주파수

- UOS v1 원 논문 Table 2의 베어링 형상과 표준 식으로 BPFI·BPFO·BSF를 계산함 [UOSV1-S01, p. 6, Table 2]
- 원신호 FFT 결과를 보존함
- 베어링 충격에 의한 공진 변조를 확인하기 위해 대역통과 후 envelope FFT를 주 검토 자료로 사용함
- IR은 BPFI, OR은 BPFO, B는 BSF와 해당 고조파를 확인함
- 복합 결함은 레이블을 구성하는 IR·OR·B를 각각 확인함
- 임의의 합·차 주파수를 결함 증거로 추가하지 않음

현재 자동 선별은 같은 carrier 대역에서 1·2·3차 고조파 중 2개 이상이 주변 잡음보다 10 dB 이상인 경우임. 정상 N204에서도 IR 후보가 나타나고 실제 결함 성분의 미검출도 확인됐으므로, 이 기준은 검토 후보 선별에만 사용함. 정상 대조군과 반복 자료로 기준을 확정하기 전에는 최종 합격 기준으로 사용하지 않음.

## 8. 수집 묶음 판정 상태

| 상태 | 의미 |
|---|---|
| `Pass` | 파일 구조·시간축·clipping과 물리 검토에서 현재 기준의 문제가 없음 |
| `Needs review` | 자동 검사에서 이상이 있거나 수동 확인이 필요한 상태 |
| `Retest` | sample 부족, rate 불일치, 운전 중단, 반복 clipping 등으로 재측정이 필요한 상태 |
| `Incomplete` | 비교할 RPM·정상 대조군·반복 조건 등이 아직 부족한 상태 |

자동 보고서가 `Pass`를 확정하지 않음. 담당자가 CSV·그림과 실험 기록을 확인한 뒤 `index.md`에 판정을 기록함.

## 9. 실행 절차

1. 원시 TDMS를 베어링과 RPM 폴더에 배치함
2. 파일명이 `{로터결함}_{베어링결함}` 순서를 따르는지 확인함
3. 수집 묶음의 `run_id`를 정함
4. 검증 코드를 실행함
5. 생성된 보고서·CSV·그림을 검토함
6. `index.md`에 결과와 `Pass/Needs review/Retest/Incomplete` 상태를 추가함
7. 재측정이 필요하면 기존 원자료를 덮어쓰지 않고 반복번호를 추가함

본 수집 파일의 실행 예시는 다음과 같음.

```bash
MPLCONFIGDIR=/tmp/matplotlib-cache .venv/bin/python \
  scripts/validate_uos_v2_acquisition.py \
  --data-root 'dataset/uosv2/수집 데이터/<대상 폴더>' \
  --output-dir 'validation/acquisition/runs/<run_id>' \
  --sampling-rate 25600 \
  --start-seconds 60 \
  --duration-seconds 120 \
  --spectral-duration-seconds 120
```
