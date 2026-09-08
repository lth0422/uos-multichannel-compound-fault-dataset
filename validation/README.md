# UOS v2 Validation

UOS v2 자체 수집 데이터의 품질 검증 코드, 수치 결과와 판정 보고서를 관리한다.
원시 TDMS는 `uosv2/수집 데이터/` 또는 향후 정리할 `external_data/`에 로컬로만
보관하며 Git에 포함하지 않는다.

- [`clipping_2026-08-01/`](clipping_2026-08-01/README.md): 현재까지 수집된 TDMS의 ADC rail, 50 g 초과, 저역통과 스윕과 대역별 포락선 재검토
- [`acquisition/`](acquisition/README.md): 본 수집 공통 규칙, 누적 인덱스와 `베어링/결함`별 검증 보고서·그림

본 수집 검증의 공통 진입점은 `scripts/validate_uos_v2_acquisition.py`임. 대상
폴더와 분석 시작·길이를 지정하면 채널별 clipping 비율, RMS, 1X, BPFI·BPFO·BSF,
복합 결함 구성 성분 결과를 CSV·PNG·한국어 보고서로 생성함.

CH0 파일별 포락선 FFT는 `scripts/plot_uos_v2_ch0_envelope_fft.py`로 생성함.
각 결함 묶음의 48개 개별 그림은 `validation/acquisition/<bearing>/<fault>/figures/envelope_fft_ch0/individual/`에 저장함.
