# UOS v2 Pilot Acquisition and Validation

이 디렉터리는 공개 데이터셋 survey와 별도로 UOS v2 자체 수집 파일럿의 설정, 분석 코드 출력, 물리 검증 결과를 관리한다.

- 원시 TDMS, MAT, ZIP은 `external_data/uos_v2_pilot/`에 두며 Git에 포함하지 않는다.
- 실험별 디렉터리에는 조건, 근거, 분석 결과 CSV, 그림, 판정 보고서만 commit한다.
- 순차 측정과 동시 측정을 구분한다. 순차 측정으로는 채널 간 위상, coherence, ADC 동시성을 검증하지 않는다.
- 한 실험에서 확인하지 못한 RPM·결함·반복성 결과를 다른 조건으로 일반화하지 않는다.

## Current pilot

- [`2026-07-22_1400rpm_30204_ir_h/`](2026-07-22_1400rpm_30204_ir_h/README.md): 30204, IR, rotor healthy, nominal 1400 RPM에서 네 13A131/NI-9234 채널을 네 위치로 옮겨가며 측정한 4×4 순차 교차시험과 UOS v1 센서 비교
