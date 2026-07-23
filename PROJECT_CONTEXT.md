# Project Context

## Confirmed context

- 기존 UOS v1이 존재한다.
- UOS Dataset v2를 새롭게 구축할 예정이다.
- 현재는 published dataset의 literature/dataset survey 단계다.
- 2026-07-22부터 survey 근거를 유지하면서 UOS v2 pilot acquisition validation을 시작했다. 이는 full acquisition 시작 승인이 아니라 장비·채널·위치 후보를 검증하는 전환 단계다.
- UOS v2용 acquisition hardware로 NI-9234와 cDAQ-9171 한 세트, HS Sensors 13A131 가속도계 4개를 구매했다. 장비 보유는 확정됐지만 최종 수집 설정은 미확정이다.
- 현재 4채널 배치 후보는 shaft-end와 motor-end bearing housing의 top/side radial channels이며, 교수 검토와 pilot validation 전까지 확정 배치가 아니다.
- 첫 파일럿은 30204, IR, rotor healthy, nominal 1400 RPM에서 네 13A131/NI-9234 채널을 네 후보 위치로 각각 옮겨 측정한 순차 4×4 교차시험이다. 동시 4채널 자료가 아니다.
- 첫 파일럿에서 네 채널 모두 회전주파수와 BPFI 포락선 성분을 검출했지만, 단일 RPM·단일 결함·순차 측정이므로 최종 배치와 full acquisition protocol은 미확정이다.
- UOS v2의 조건별 synchronized four-channel master record 수집 목표 길이는 60초로 결정했다. 모델 입력 window 길이, overlap, 안정화 제외 규칙과 공개 파생본 길이는 별도 검증 후 결정한다.

## Working hypotheses

아래 항목은 조사로 검증할 가설이며 확정 contribution이 아니다.

- synchronized multi-position vibration이 진단 및 물리 검증에 잠재적 가치가 있다.
- internal bearing compound fault가 기존 benchmark의 공백을 보완할 잠재적 가치가 있다.
- bearing–rotor compound fault가 현실적인 복합 상태 연구에 잠재적 가치가 있다.
- paired single-/multi-channel data가 향후 on-device 활용 연구를 지원할 가능성이 있다.

## Unconfirmed decisions

- 최종 센서 위치와 마운팅
- 최종 채널 수
- 최종 샘플링레이트
- 최종 결함 조합
- 최종 데이터 개수
- 최종 논문 contribution
- 최종 hardware-supported sampling rate와 저장/downsampling 정책

## Source hierarchy

1. Original dataset paper
2. Official dataset documentation
3. Official institutional repository
4. Follow-up peer-reviewed paper
5. Secondary summary
