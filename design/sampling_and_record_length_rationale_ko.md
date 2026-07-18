# 샘플링레이트, RPM, 데이터 길이 선정 근거

## 결정 상태

아직 UOS Dataset v2의 최종 샘플링레이트, RPM grid, 데이터 길이는 확정하지 않았다. 이 문서는 보유 장비, 선행 데이터셋 조사 결과, 물리 기반 진단 요구사항을 함께 검토하여 pilot acquisition에서 비교할 후보를 정리하기 위한 작업 문서다.

따라서 아래 내용은 최종 contribution이나 최종 수집 조건이 아니라, 교수 검토와 pilot validation 전에 사용할 근거 정리다.

## 선행 데이터셋 조사에서 확인된 점

현재까지 검토한 회전기계·베어링 데이터셋의 진동 샘플링레이트는 약 6.4 kHz부터 200 kHz까지 다양하다. 예를 들어 Arkansas 2023은 6.4 kHz, NASA IMS는 20 kHz, XJTU-SY와 KAIST Batch는 25.6 kHz, Paderborn은 64 kHz를 사용한다. [ARK23-E07, IMS-E05, XJTU-E04, PU-E07, KAIB-E05, KAIB-E06]

이 값들은 중요한 precedent이지만, 특정 값이 UOS v2의 최적값이라는 뜻은 아니다. 각 데이터셋은 센서, DAQ, 목적, 회전속도, 결함 조건, record 길이, 공개 방식이 다르기 때문이다.

특히 KAIST Batch는 UOS v2와 유사하게 두 bearing housing의 두 방향에서 총 4개의 진동 채널을 수집한 선행 사례이며, 진동 샘플링레이트 25.6 kHz를 사용했다. 이는 UOS v2의 25.6 kS/s 후보를 설명할 때 좋은 비교 근거가 된다. 다만 KAIST 논문도 25.6 kHz를 왜 최적으로 선택했는지에 대한 bandwidth, anti-aliasing, 회전수, 주파수 해상도 기반의 정량 근거를 충분히 제시하지는 않는다. [KAIB-E02, KAIB-E05, KAIB-E06, KAIB-E11]

HUST Vietnam은 NI-9234를 사용한 hardware-relevant precedent다. 이 데이터셋은 steady-state record를 51.2 kHz로 10초 수집하고, run-up data는 5초로 제공한다. 논문은 높은 샘플링레이트가 신호 변화를 자세히 포착한다고 설명하지만, UOS v2에 필요한 bearing characteristic frequency, envelope band, anti-aliasing margin, NI-9234 filter transition 기반의 상세 도출은 제공하지 않는다. [HUSTV-E04-HUSTV-E06]

샘플링레이트, RPM, 데이터 길이를 함께 보면 다음과 같다. 이 표는 비교 근거이며, UOS v2 설정을 그대로 결정하는 voting table이 아니다.

| Dataset | Sampling rate | RPM condition | Record length |
|---|---:|---:|---:|
| UOS v1 | 8,000; 16,000 Hz | 600; 800; 1,000; 1,200; 1,400; 1,600 RPM | 80; 160 s |
| CWRU | 12,000; 48,000 Hz | approximately 1,720-1,797 RPM | Unknown |
| Paderborn | 64,000 Hz | 900; 1,500 RPM | 4 s |
| XJTU-SY | 25,600 Hz | 2,100; 2,250; 2,400 RPM | 1.28 s |
| NASA IMS | 20,000 Hz | 2,000 RPM | 1 s stated; 1.024 s implied by sample count |
| MAFAULDA | 50,000 Hz | 737-3,686 RPM | 5 s |
| Arkansas 2023 | 6,400 Hz | 25; 50; 75 RPM | 10 s |
| Ottawa 2018 | 200,000 Hz | approximately 588-1,740 RPM within variable-speed records | 10 s |
| Ottawa 2023 | 42,000 Hz | 1,750 RPM | 10 s |
| PRONOSTIA | 25,600 Hz acceleration | 1,800; 1,650; 1,500 RPM | Unknown |
| KAIST Batch | 25,600 Hz vibration | 3,010 RPM; 680-2,460 RPM varying | 60; 120; 300; 600; 2,100 s |
| HUST Vietnam | 51,200 Hz | Unknown in reviewed article | 5; 10 s |

## 보유 장비에 따른 제약

UOS v2에서 현재 확정된 장비는 NI-9234 + cDAQ-9171, 그리고 HS Sensors 13A131 가속도계 4개다. 장비 보유는 확정됐지만, 최종 수집 조건은 아직 확정되지 않았다.

NI-9234는 4채널 simultaneous sampling을 지원하며, 내부 13.1072 MHz timebase를 기준으로 다음과 같은 discrete native rate를 사용한다.

`fs = 13,107,200 Hz / (256 × n)`, `n = 1..31`

| n | native sampling rate |
|---:|---:|
| 1 | 51,200.00 Hz |
| 2 | 25,600.00 Hz |
| 3 | 17,066.67 Hz |
| 4 | 12,800.00 Hz |
| 5 | 10,240.00 Hz |
| 6 | 8,533.33 Hz |
| 7 | 7,314.29 Hz |
| 8 | 6,400.00 Hz |
| 9 | 5,688.89 Hz |
| 10 | 5,120.00 Hz |
| 11 | 4,654.55 Hz |
| 12 | 4,266.67 Hz |
| 13 | 3,938.46 Hz |
| 14 | 3,657.14 Hz |
| 15 | 3,413.33 Hz |
| 16 | 3,200.00 Hz |
| 17 | 3,011.76 Hz |
| 18 | 2,844.44 Hz |
| 19 | 2,694.74 Hz |
| 20 | 2,560.00 Hz |
| 21 | 2,438.10 Hz |
| 22 | 2,327.27 Hz |
| 23 | 2,226.09 Hz |
| 24 | 2,133.33 Hz |
| 25 | 2,048.00 Hz |
| 26 | 1,969.23 Hz |
| 27 | 1,896.30 Hz |
| 28 | 1,828.57 Hz |
| 29 | 1,765.52 Hz |
| 30 | 1,706.67 Hz |
| 31 | 1,651.61 Hz |

계획 문서에서는 51.2, 25.6, 12.8, 6.4, 3.2 kS/s처럼 설명하기 쉬운 native rate를 우선 후보로 다루는 것이 좋다. fractional rate도 사용할 수 있지만, 특별한 물리적 또는 실험적 이유가 있을 때만 선택하는 것이 바람직하다.

NI-9234의 alias-free bandwidth는 대략 `0.45 × fs`로 볼 수 있다. 따라서 주요 후보의 대역은 다음과 같이 정리할 수 있다.

| 후보 샘플링레이트 | NI alias-free bandwidth | 현재 해석 |
|---:|---:|---|
| 12.8 kS/s | 약 5.76 kHz | pilot spectrum에서 필요한 정보가 이 대역 안에 충분히 있으면 저장 효율 후보 |
| 17.067 kS/s | 약 7.68 kHz | 중간 후보지만 설명이 다소 복잡하고, 13A131의 supplier-listed 10 kHz 범위 전체는 커버하지 못함 |
| 25.6 kS/s | 약 11.52 kHz | 현재 primary pilot candidate. 13A131의 supplier-listed 0.5-10 kHz 범위를 nominal하게 커버 |
| 51.2 kS/s | 약 23.04 kHz | high-rate master/pilot reference. 단, 10 kHz 이상 대역은 현재 센서 사양 기준으로 추가 유효 정보가 보장되지 않음 |

## 현재 가장 방어 가능한 샘플링레이트 가설

현재 가장 방어 가능한 접근은 pilot acquisition에서 25.6 kS/s와 51.2 kS/s를 함께 비교하는 것이다.

25.6 kS/s가 유력한 이유는 다음과 같다.

- NI-9234의 native rate다.
- KAIST Batch, XJTU-SY, PRONOSTIA 등 주요 데이터셋에서 25.6 kHz급 진동 수집 precedent가 있다.
- NI-9234 기준 alias-free bandwidth가 약 11.52 kHz로, 현재 확인된 HS 13A131 supplier-listed 10 kHz 범위를 nominal하게 포함한다.
- 4채널 기준 초당 sample 수가 102,400개로, 51.2 kS/s보다 저장 부담이 절반이다.

51.2 kS/s가 필요한지는 아직 검증해야 한다. 다음 중 하나가 pilot에서 확인되면 51.2 kS/s master record를 저장할 근거가 생긴다.

- 25.6 kS/s에서 alias margin이 부족하다.
- 10 kHz 이상 대역의 transient 또는 mounting-related signal이 진단에 실제로 유효하다.
- 51.2 kS/s에서 취득한 뒤 controlled downsampling한 결과가 더 안정적이다.
- 고장 충격, envelope analysis, cross-channel phase/coherence 검증에 high-rate master가 필요하다.

반대로 25.6 kS/s로 필요한 fault frequency, harmonics, envelope spectrum 정보가 충분히 보존되고, 51.2 kS/s가 추가 진단 정보를 제공하지 않는다면 25.6 kS/s가 더 실용적인 release candidate가 된다.

12.8 kS/s는 저장 효율 측면의 후보로 남길 수 있다. 다만 13A131의 10 kHz 범위를 전체적으로 커버하지 못하므로, pilot spectrum에서 필요한 분석 대역이 5.76 kHz 이하라는 근거가 있어야 한다.

## 100 Hz 데이터에 대한 주의

100 Hz는 NI-9234의 native acquisition rate가 아니다. 따라서 100 Hz 신호가 필요하다면 raw acquisition이 아니라 후처리된 derivative signal로 정의해야 한다.

100 Hz 데이터를 제공하거나 on-device inference 예시로 사용할 경우에는 다음을 반드시 문서화해야 한다.

- 원본 master sampling rate
- anti-alias filter 설계
- resampling/downsampling 방법
- 어떤 물리 peak를 유지하고 어떤 고주파 정보를 버리는지
- raw data와 derived data의 파일/메타데이터 구분

즉, UOS v2에서 100 Hz는 "수집 설정"이 아니라 "재현 가능한 후처리 산출물"로 다루는 것이 타당하다.

## 최종 결정을 위해 필요한 물리 계산

샘플링레이트는 기존 데이터셋이 사용한 값을 그대로 따라가는 방식으로 정하면 안 된다. 실제 UOS rig, bearing geometry, RPM 범위, sensor/DAQ 대역을 기준으로 계산해야 한다.

최소한 다음 항목을 계산해야 한다.

- shaft frequency
- FTF
- BPFO
- BPFI
- BSF
- 필요한 harmonic 범위
- rotor fault 관련 1x, 2x, sideband
- envelope spectrum에서 사용할 구조/센서 공진 대역
- sensor, mounting, DAQ의 usable bandwidth
- NI-9234 filter transition과 alias margin

복합 결함에서는 sum/difference peak가 보인다고 해서 곧바로 compound fault의 물리 검증으로 결론 내리면 안 된다. matched pure-fault reference와 repeated compound trial을 함께 비교해야 한다.

## RPM 선정 원칙

RPM은 단순히 기존 데이터셋에서 자주 쓰인 값을 따라 정하면 안 된다. RPM은 결함주파수, 회전주파수, 데이터 길이, load 조건, motor/rig 한계, 안전성, domain-shift 실험 목적을 동시에 결정하는 핵심 변수다.

현재 선행 데이터셋은 서로 다른 RPM 전략을 사용한다.

- UOS v1은 600-1,600 RPM의 여러 fixed-speed 조건을 제공한다.
- Paderborn은 900 RPM과 1,500 RPM을 사용한다.
- PRONOSTIA는 1,500, 1,650, 1,800 RPM을 load와 함께 condition으로 묶어 사용한다.
- XJTU-SY는 2,100, 2,250, 2,400 RPM을 radial load와 함께 묶어 사용한다.
- KAIST Batch는 3,010 RPM fixed-speed와 680-2,460 RPM varying-speed 조건을 제공한다.
- Ottawa 2018은 record 내부에서 speed가 변하는 variable-speed 데이터를 제공한다.

이 비교에서 얻을 수 있는 결론은 "특정 RPM이 표준"이라는 것이 아니다. 오히려 UOS v2는 RPM과 load가 fault label 또는 bearing batch와 confounding되지 않도록 독립적으로 설계해야 한다.

## RPM 후보를 정할 때 필요한 계산

최종 RPM grid를 정하기 전에 각 후보 RPM에 대해 다음을 계산해야 한다.

- shaft frequency `fr = RPM / 60`
- bearing geometry 기반 FTF, BPFO, BPFI, BSF
- 각 fault frequency의 harmonic 범위
- unbalance, misalignment, looseness 관련 1x, 2x, 3x 성분
- RPM 변화에 따른 sideband 간격
- 최저 RPM에서 필요한 최소 회전 수
- 최고 RPM에서 필요한 최고 분석 주파수와 sampling-rate margin
- motor/rig가 안정적으로 유지할 수 있는 speed range
- load 조건과 함께 걸었을 때의 안전성, 발열, slip, stationarity

RPM grid는 가능한 한 load와 독립적으로 설계해야 한다. 예를 들어 `RPM A`에는 healthy만 있고 `RPM B`에는 compound fault만 있으면, 모델이 결함이 아니라 RPM 차이를 학습할 수 있다. 따라서 이상적인 설계는 각 fault condition이 동일한 RPM/load 조합에서 반복 측정되는 balanced factorial grid다. 장비 또는 시간 제약 때문에 incomplete block이 필요하면, 어떤 조합이 빠졌는지 metadata와 논문에 명시해야 한다.

## 현재 제안 가능한 RPM strategy

현재 단계에서 RPM을 확정하지 않고, 다음 세 가지 후보 strategy를 pilot 전 검토 대상으로 두는 것이 안전하다.

| Strategy | 설명 | 장점 | 주의점 |
|---|---|---|---|
| UOS v1 continuity grid | 600-1,600 RPM 범위를 중심으로 v1과 연결되는 fixed-speed grid 구성 | v1과 비교 설명이 쉬움; 낮은 RPM에서 충분한 회전 수/해상도 검토 가능 | v2 rig와 bearing geometry에 맞는 fault-frequency 대역 재계산 필요 |
| common benchmark grid | 900, 1,500, 1,800 RPM 등 Paderborn/PRONOSTIA와 겹치는 fixed-speed 후보 포함 | 선행 데이터셋과 조건 설명이 쉬움 | load, bearing type, sensor bandwidth가 다르므로 직접 비교로 과장하면 안 됨 |
| fixed + variable-speed pilot | fixed-speed 조건을 기본으로 두고, 일부 run-up 또는 variable-speed record를 별도 pilot로 수집 | real-time/order tracking 연구 가능성 확인 | variable-speed는 annotation, tachometer alignment, stationarity 처리가 더 어려움 |

현재 가장 방어 가능한 임시안은 fixed-speed grid를 우선 설계하고, variable-speed는 별도 pilot candidate로 분리하는 것이다. fixed-speed 조건에서 먼저 channel quality, fault-frequency visibility, envelope spectrum, repeated-run stability를 확인한 뒤 variable-speed 확장 여부를 결정한다.

## 데이터 길이 후보

데이터 길이는 초 단위만으로 정하면 안 된다. 최소 회전 수, 주파수 해상도, stationarity, storage, inference window를 함께 봐야 한다.

주파수 해상도는 `1 / T`로 계산된다.

| record 길이 | 주파수 해상도 | 600 RPM 회전 수 | 1,000 RPM 회전 수 | 1,700 RPM 회전 수 |
|---:|---:|---:|---:|---:|
| 1 s | 1 Hz | 10 | 16.7 | 28.3 |
| 2 s | 0.5 Hz | 20 | 33.3 | 56.7 |
| 5 s | 0.2 Hz | 50 | 83.3 | 141.7 |
| 10 s | 0.1 Hz | 100 | 166.7 | 283.3 |

위 RPM 값은 계산 예시이며 UOS v2의 최종 RPM grid가 아니다. 실제 최저/최고 RPM이 확정되면 다시 계산해야 한다.

현재 pilot에서는 10초 master record를 우선 수집하고, 동일 record에서 1초, 2초, 5초, 10초 window를 비교하는 전략이 방어 가능하다. 이렇게 하면 데이터 길이를 나중에 임의로 바꾸는 것이 아니라, 같은 원 신호에서 주파수 해상도와 inference 성능을 비교할 수 있다.

## 후보 recording strategy

현재 제안 가능한 pilot strategy는 다음과 같다.

- 후보 RPM grid를 먼저 정하되, 각 fault condition이 같은 RPM/load 조합을 공유하도록 설계한다.
- RPM은 tachometer 또는 speed sensor로 측정하고, vibration record와 시간 정렬 방법을 문서화한다.
- 대표 healthy/pure-fault 조건에서 25.6 kS/s와 51.2 kS/s를 모두 수집한다.
- 각 조건은 synchronized 4-channel master record로 저장한다.
- 우선 10초 master record를 수집한다.
- 동일 master record에서 deterministic 1, 2, 5, 10초 window를 만든다.
- train/validation/test split은 windowing 전에 bearing, assembly, physical run 단위로 먼저 정한다.
- 100 Hz derivative가 필요하면 master record에서 versioned filtering/resampling code로 생성한다.

이 전략도 아직 최종안은 아니다. 10초는 여러 window와 frequency resolution을 비교하기 좋은 pilot 길이일 뿐, 최종 공개 record 길이라고 단정하지 않는다.

## 저장 용량 추정

아래 값은 container metadata를 제외한 4채널 raw payload의 대략적인 크기다.

| 샘플링레이트 | 길이 | 4채널 전체 sample 수 | float32 payload | float64 payload |
|---:|---:|---:|---:|---:|
| 12.8 kS/s | 1 s | 51,200 | 0.20 MB | 0.41 MB |
| 12.8 kS/s | 10 s | 512,000 | 2.05 MB | 4.10 MB |
| 25.6 kS/s | 1 s | 102,400 | 0.41 MB | 0.82 MB |
| 25.6 kS/s | 10 s | 1,024,000 | 4.10 MB | 8.19 MB |
| 51.2 kS/s | 1 s | 204,800 | 0.82 MB | 1.64 MB |
| 51.2 kS/s | 10 s | 2,048,000 | 8.19 MB | 16.38 MB |

최종 저장 용량은 결함 조건 수, 반복 수, RPM/load 조건 수, remount 횟수, metadata channel 수에 따라 다시 계산해야 한다.

## 최종 선택 기준

최종 샘플링레이트와 record/window 길이는 다음 조건을 동시에 만족하는 가장 낮은 native rate와 가장 짧은 길이로 선택하는 것이 원칙이다.

- 필요한 bearing fault frequency와 harmonic을 보존한다.
- envelope analysis에 필요한 대역을 alias margin과 함께 보존한다.
- cross-channel phase/coherence 비교에 충분하다.
- 최저 RPM에서 사전에 정한 최소 회전 수를 포함한다.
- 필요한 주파수 해상도와 반복성을 제공한다.
- clipping과 noise 문제가 없다.
- on-device inference용 window를 재현 가능한 전처리로 만들 수 있다.
- 전체 dataset 저장 용량과 공개 용량이 현실적이다.

## 현재 임시 결론

현재 문헌조사와 장비 제약만 기준으로 하면, 25.6 kS/s는 가장 설명하기 쉬운 primary pilot candidate다. 51.2 kS/s는 high-rate master 또는 downsampling 검증용 후보로 남긴다. 12.8 kS/s는 저장 효율 후보지만, 필요한 진단 대역이 5.76 kHz 이하라는 pilot 근거가 있어야 한다.

RPM은 UOS v1의 600-1,600 RPM 범위, Paderborn/PRONOSTIA/XJTU-SY/KAIST의 fixed-speed precedent, UOS rig의 motor/load 한계, bearing geometry 기반 fault-frequency 계산을 함께 검토해 정해야 한다. 현재는 fixed-speed grid를 먼저 설계하고, variable-speed/run-up은 별도 pilot candidate로 두는 것이 안전하다.

데이터 길이는 10초 master record를 수집한 뒤 1, 2, 5, 10초 window를 비교하는 방식이 현재 가장 방어 가능하다. 최종 길이는 실제 RPM, bearing characteristic frequency, frequency resolution, stationarity, storage, on-device inference 요구사항을 함께 검토한 뒤 확정해야 한다.
