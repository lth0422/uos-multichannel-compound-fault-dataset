# UOS v2 본 수집 검증

본 수집 TDMS를 지정하면 다음 항목을 같은 형식으로 점검하고 수집 묶음별 보고서를 누적함.

- 공통 검증 규칙: [`protocol.md`](protocol.md)
- 수집 묶음별 누적 현황: [`index.md`](index.md)
- 결함 베어링별 정리: `<bearing>/<bearing_fault>/`
- 실행 당시 산출물 보존: `runs/<run_id>/`

- TDMS 실제 sampling rate와 채널 수 확인
- 분석 표본 수, RMS, peak, p99.99 계산
- NI-9234 입력 rail 도달 표본 수와 전체 표본 대비 비율 계산
- 같은 베어링·결함·로터·채널의 RPM별 RMS 비교
- 원신호 FFT에서 회전주파수 1X 확인
- 원신호 FFT와 대역별 envelope FFT에서 BPFI·BPFO·BSF 확인
- 복합 결함 레이블에서 IR·OR·B 구성 성분을 각각 확인
- CH0 48개 파일의 포락선 FFT를 개별 PNG로 생성하고 문서에는 고정 기준의 대표 그림만 삽입

## 초기 표본 실행

- 베어링: 6204 deep-groove ball bearing
- 베어링 결함: IR+OR+B
- 로터 조건: H
- RPM: 1000, 1200, 1400, 1600
- sampling rate: 25.6 kHz
- 진폭·clipping 분석: 공회전 60초 제외 후 120초
- 주파수 분석: 위 구간의 첫 30초

이 4개 파일은 같은 조건에서 RPM만 달라 RMS 추세를 확인할 수 있고, 3중 내부 결함이므로 IR·OR·B 검출 절차를 동시에 시험할 수 있어 선택함. 전체 수집 자료에 대한 최종 합격 판정이 아니라 코드의 표본 실행임.

추가로 `runs/2026-09-02_N204_H_fault-matrix_1600rpm/`에서 N204·1600 RPM·로터 정상 H의 정상·단일·이중·삼중 내부 결함과 IR+OR 반복 파일을 실행함. 1X는 44/44채널에서 확인됐지만 고조파 계열의 10 dB 고정 기준은 레이블상 기대 성분 6/72채널·성분만 통과했고 정상 파일에서도 IR 후보가 2/4채널 나타남. 따라서 현재 자동 결함주파수 결과는 정상 대조군과 비교할 검토 후보를 고르는 용도로만 사용하며 데이터 합격 기준으로 고정하지 않음.

## 재실행

```bash
MPLCONFIGDIR=/tmp/matplotlib-cache .venv/bin/python \
  scripts/validate_uos_v2_acquisition.py \
  --data-root 'dataset/uosv2/수집 데이터/BearingType_DeepGrooveBall' \
  --output-dir 'validation/acquisition/runs/2026-09-02_6204_H_IR+OR+B_1000-1600rpm' \
  --sampling-rate 25600 \
  --bearing 6204 \
  --fault 'IR+OR+B' \
  --rotor H \
  --rpm 1000 1200 1400 1600 \
  --start-seconds 60 \
  --duration-seconds 120 \
  --spectral-duration-seconds 30
```

본 수집 파일은 앞 60초 공회전을 제외하고 이후 120초를 분석함. 25.6 kHz 기준 채널당 3,072,000표본이며 실행 시 `--start-seconds 60 --duration-seconds 120 --spectral-duration-seconds 120`을 사용함.

CH0의 파일별 2~7 kHz 포락선 FFT 그림은 다음 형식으로 생성함.

```bash
MPLCONFIGDIR=/tmp/matplotlib-cache PYTHONPATH=. .venv/bin/python \
  scripts/plot_uos_v2_ch0_envelope_fft.py \
  --source-run 'validation/acquisition/runs/<run_id>' \
  --output-dir 'validation/acquisition/<bearing>/<bearing_fault>'
```

- 단일 결함에는 해당 결함의 1·2·3차 고조파만 표시함
- 복합 결함에는 구성 결함별 고조파와 쌍별 합·차 주파수 후보를 함께 표시함
- 합·차 주파수는 상호작용 후보이며 복합 결함의 단독 판정 기준으로 사용하지 않음

## 수집 묶음별 결과 위치

- `<bearing>/<bearing_fault>/validation_report_ko.md`: 베어링 형식·결함별 최종 검토 문서
- `<bearing>/<bearing_fault>/figures/envelope_fft_ch0/individual/`: CH0 파일별 포락선 FFT 그림
- `<bearing>/<bearing_fault>/figures/envelope_fft_ch0/contact_sheet.png`: 48개 그림 전체 축소본
- `runs/<run_id>/validation_report_ko.md`: 핵심 수치, 파일별 비교, 해석 제한
- `results/file_channel_metrics.csv`: sample 수, RMS, 진폭, rail 비율, 1X
- `results/frequency_detection_detail.csv`: 모든 예상·관찰 주파수와 주변 잡음 대비 dB
- `results/component_detection_summary.csv`: 채널별 1X·IR·OR·B 요약
- `results/rms_rpm_trend.csv`: 동일 조건의 RPM별 RMS 추세
- `results/input_manifest.csv`: 실제 입력 파일과 분석 구간
- `figures/`: rail 비율, RMS–RPM, 물리 성분 검출 그림

## 판정 기준의 범위

- `near_input_limit_samples`는 TDMS 가속도와 채널 감도를 전압으로 환산했을 때 약 ±5.10 V에 도달한 표본임
- `rail_samples`는 2026-08-01 전수조사에서 확인한 채널별 반복 저장 rail 값과 정확히 같은 표본이며, 보고서의 clipping 비율 분자로 사용함
- 1X는 원신호 FFT의 국소 peak로 확인함
- 베어링 결함은 envelope FFT를 주 자료로 사용함
- IR·OR·B 성분은 같은 carrier 대역에서 해당 결함주파수의 1·2·3차 고조파 중 2개 이상이 주변 잡음보다 10 dB 이상인 경우 자동 선별함
- 위 기준은 데이터 검토 대상을 줄이는 보조 기준이며 데이터 합격이나 결함 존재를 단독으로 확정하지 않음
- 최종 수집 판정은 수집 완전성, 분석 길이, 진폭 범위, RMS의 전체적인 RPM 경향과 회전주파수 1X를 중심으로 수행함
- 결함주파수 검출률은 물리적 보조 검증으로 기록하며 낮은 검출률만으로 수집 묶음을 실패 처리하지 않음
