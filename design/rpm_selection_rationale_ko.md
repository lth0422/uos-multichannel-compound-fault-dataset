# RPM 선정 정량 분석 및 후보안

## 결정 상태

아직 UOS Dataset v2의 최종 RPM grid는 확정하지 않는다. 이 문서는 Notion/교수 검토용으로, 현재 survey 결과와 물리 계산 기준을 바탕으로 pilot에서 검토할 RPM 후보를 제안한다.

중요한 전제는 다음과 같다.

- UOS v2 수집 시나리오 초안에서는 UOS v1과 연결되는 bearing set을 우선 고려한다.
- 후보 bearing type은 deep-groove ball bearing 6204, cylindrical roller bearing N204/NJ204, tapered roller bearing 30204이다.
- 다만 각 bearing별 BPFO/BPFI/BSF/FTF order coefficient와 실제 v2 최종 사용 모델은 아직 설계 문서에 확정 계산값으로 정리되지 않았다.
- motor/rig 허용 RPM, load 조건, tachometer/speed measurement 방식은 아직 최종 확정되지 않았다.
- 따라서 아래 계산은 최종 설계값이 아니라, 후보 RPM을 좁히기 위한 정량 프레임이다.
- 최종 RPM은 실제 v2 bearing별 geometry/order coefficient로 BPFO/BPFI/BSF/FTF를 다시 계산하고, pilot spectrum과 안전성 검토 후 확정해야 한다.

## 현재 UOS v2 수집 시나리오 초안

현재 논의 중인 UOS v2 수집 시나리오 초안은 다음과 같다. 여기서 RPM과 sampling rate는 UOS v1 기준으로 임시 입력한 값이며, 이 문서의 목적은 그 값이 그대로 타당한지 검토하는 것이다.

| Axis | Candidate values | Count |
|---|---|---:|
| Sampling rate | 8 kHz, 16 kHz | 2 |
| RPM | 600, 800, 1000, 1200, 1400, 1600 | 6 |
| Bearing type | deep-groove ball 6204; cylindrical roller N204/NJ204; tapered roller 30204 | 3 |
| Rotor class | normal; M1; M2; M3; U1; U2; U3; L | 8 |
| Bearing class | normal; IR; OR; B; IR+OR; IR+B; OR+B; IR+OR+B | 8 |

Sampling rate를 제외한 조건 수는 다음과 같다.

```text
6 RPM × 3 bearing types × 8 rotor classes × 8 bearing classes = 1,152 condition cells
```

sampling rate 2개를 모두 별도 취득하면 총 record cell은 다음과 같다.

```text
1,152 × 2 sampling rates = 2,304 record cells
```

따라서 `2,304 × 2`로 한 번 더 곱하면 중복 계산이 된다. 추가 반복 trial 수가 있다면 그때 별도로 곱해야 한다.

## 선행 데이터셋 RPM precedent

현재 survey에서 확인한 주요 RPM 조건은 다음과 같다.

| Dataset | RPM condition | 성격 |
|---|---:|---|
| UOS v1 | 600; 800; 1000; 1200; 1400; 1600 | fixed-speed multi-RPM |
| Paderborn | 900; 1500 | fixed-speed, load/torque 조건 포함 |
| XJTU-SY | 2100; 2250; 2400 | run-to-failure, RPM-load pair가 묶임 |
| NASA IMS | 2000 | constant-speed run-to-failure |
| Arkansas 2023 | 25; 50; 75 | very-low-speed rotary simulator |
| Ottawa 2018 | approx. 588-1740 within each record | time-varying speed |
| Ottawa 2023 | 1750 | nominal constant speed |
| PRONOSTIA | 1500; 1650; 1800 | run-to-failure, RPM-load pair가 묶임 |
| KAIST Batch | 3010; 680-2460 varying | fixed-speed and varying-speed |

이 표에서 얻을 수 있는 결론은 특정 RPM이 표준이라는 것이 아니다. 대신 UOS v2는 다음 조건을 만족하는 RPM grid를 선택해야 한다.

- UOS v1과 일부 연속성을 가진다.
- Paderborn, PRONOSTIA, Ottawa 등 대표 데이터셋과 설명 가능한 겹침이 있다.
- RPM과 load가 fault label과 confounding되지 않는다.
- 최저 RPM에서도 충분한 회전 수와 주파수 해상도를 확보한다.
- 최고 RPM에서도 bearing fault frequency와 harmonic, rotor sideband를 alias margin 안에서 관측한다.

## 계산에 사용한 임시 bearing-order 계수

현재 UOS v2 후보 bearing model은 위 시나리오에 들어 있지만, 각 bearing별 order coefficient는 아직 이 문서에 확정값으로 정리되지 않았다. 따라서 아래 정량 분석은 Wang et al. 2024 메모에서 정리된 SKF 6205, 2000 RPM 조건의 예시 order 계수로 먼저 계산한다. 해당 메모의 값은 다음과 같다.

| Quantity | Value at 2000 RPM | Shaft-order coefficient |
|---|---:|---:|
| shaft frequency `fr` | 33.3 Hz | 1.00x |
| FTF `fc` | 13.667 Hz | 0.41x |
| BSF `fb` | 78.7 Hz | 2.36x |
| BPFO `fo` | 119.7 Hz | 3.59x |
| BPFI `fi` | 180.3 Hz | 5.41x |

이 계수는 UOS v2 베어링이 SKF 6205와 동일하다는 뜻이 아니다. 특히 6204, N204/NJ204, 30204는 서로 bearing type과 geometry가 다르므로 BPFO/BPFI/BSF/FTF 계수가 달라진다. 다만 RPM 후보를 비교하는 1차 계산에는 유용한 예시 계수로 사용할 수 있다.

## 후보 RPM별 기본 계산

아래 표는 후보 RPM에서 shaft frequency, 10초 record에 포함되는 회전 수, 그리고 예시 BPFI/BPFO/BSF를 계산한 것이다.

| RPM | `fr` (Hz) | 10 s rotations | BPFO 3.59x (Hz) | BPFI 5.41x (Hz) | BSF 2.36x (Hz) |
|---:|---:|---:|---:|---:|---:|
| 600 | 10.0 | 100 | 35.9 | 54.1 | 23.6 |
| 900 | 15.0 | 150 | 53.9 | 81.1 | 35.4 |
| 1200 | 20.0 | 200 | 71.8 | 108.2 | 47.2 |
| 1500 | 25.0 | 250 | 89.8 | 135.2 | 59.1 |
| 1800 | 30.0 | 300 | 107.7 | 162.3 | 70.8 |

이 범위에서는 기본 결함주파수 자체가 모두 200 Hz 이하에 위치한다. 따라서 기본 BPFO/BPFI/BSF만 보면 매우 낮은 샘플링레이트로도 관측 가능해 보인다. 하지만 실제 수집률은 기본 결함주파수만 기준으로 정하면 안 된다. harmonic, sideband, impact transient, envelope analysis 대역까지 고려해야 한다.

## 고차 harmonic 기준 대역 검토

Wang et al. 2024 메모에서는 복합 결함에서 BPFI 6차, BSF 15차 같은 고차 성분을 검토한다. 같은 order 관점으로 후보 RPM에서 상한을 계산하면 다음과 같다.

| RPM | 6x BPFI (Hz) | 15x BSF (Hz) | 보수적 저주파 결함대역 상한 |
|---:|---:|---:|---:|
| 600 | 324.6 | 354.3 | approx. 355 Hz |
| 900 | 486.8 | 531.4 | approx. 532 Hz |
| 1200 | 649.1 | 708.6 | approx. 709 Hz |
| 1500 | 811.4 | 885.7 | approx. 886 Hz |
| 1800 | 973.6 | 1062.9 | approx. 1063 Hz |

이 계산만 보면 600-1800 RPM grid에서 복합 베어링 결함의 주요 저주파 성분은 대략 1.1 kHz 이하에 들어온다. 이는 사용자의 직관, 즉 “복합이어도 베어링 결함주파수 자체는 1 kHz 근처 이하일 가능성이 높다”는 판단과 잘 맞는다.

다만 이것은 envelope spectrum에서 나타나는 demodulated fault frequency 대역에 가까운 해석이다. raw vibration에서 충격을 잘 포착하기 위한 구조 공진 대역은 더 높을 수 있으므로, 샘플링레이트를 이 값만 보고 3.2 또는 6.4 kS/s로 낮추는 것은 아직 이르다.

## record length 관점

10초 record 기준 회전 수는 다음과 같다.

| RPM | 1 s rotations | 2 s rotations | 5 s rotations | 10 s rotations |
|---:|---:|---:|---:|---:|
| 600 | 10 | 20 | 50 | 100 |
| 900 | 15 | 30 | 75 | 150 |
| 1200 | 20 | 40 | 100 | 200 |
| 1500 | 25 | 50 | 125 | 250 |
| 1800 | 30 | 60 | 150 | 300 |

최저 600 RPM에서도 10초 record는 100회전을 포함한다. 5초 window도 50회전을 포함하므로, steady-state 조건이 안정적이라면 5초 window는 분석 후보가 될 수 있다. 반면 1초 window는 600 RPM에서 10회전뿐이므로, on-device inference 후보로는 가능하지만 물리 검증용 master window로는 짧을 수 있다.

주파수 해상도는 record 길이에 의해 결정된다.

| Duration | FFT bin spacing |
|---:|---:|
| 1 s | 1.0 Hz |
| 2 s | 0.5 Hz |
| 5 s | 0.2 Hz |
| 10 s | 0.1 Hz |

RPM grid를 600, 900, 1200, 1500, 1800처럼 300 RPM 간격으로 두면 shaft frequency 간격은 5 Hz다. 5초 이상 window에서는 0.2 Hz 이하의 bin spacing을 확보하므로, speed가 안정적이고 tachometer alignment가 된다면 order/fault-frequency 검증에 충분히 여유가 있다.

## 추천 후보안

RPM grid는 두 가지 방향으로 판단할 수 있다.

- UOS v1 continuity와 기존 수집 시나리오 유지
- 대표 benchmark와의 일부 겹침을 늘리는 재설계

전체 조건 수가 이미 큰 편이므로, RPM 6개를 유지할지 5개 또는 3개로 줄일지는 수집 시간, 반복 trial 수, sampling rate 수, load 조건 추가 여부를 함께 보고 결정해야 한다.

### UOS v1 continuity 우선안: 6-level grid

현재 시나리오 초안의 RPM은 다음과 같다.

```text
600, 800, 1000, 1200, 1400, 1600 RPM
```

이 후보는 다음 장점이 있다.

- UOS v1과 직접 연결된다.
- 이미 수집 시나리오 산술에 반영되어 있다.
- 200 RPM 간격이므로 speed resolution이 촘촘하다.
- 600-1600 RPM 범위는 Ottawa 2018의 약 588-1740 RPM time-varying range와도 대략 겹친다.
- 1600 RPM에서도 예시 6205 order 기준 저주파 fault-band 상한은 15x BSF 약 945 Hz 수준이므로, 기본 결함주파수/harmonic 검증에는 충분한 margin이 있다.

주의점은 다음과 같다.

- Paderborn의 900/1500 RPM과 정확히 겹치지 않는다.
- PRONOSTIA의 1500/1650/1800 RPM과도 정확한 겹침이 약하다.
- RPM 6개를 유지하면 조건 수가 커진다. 현재 초안 기준 sampling rate 2개까지 포함해 2,304 record cells이며, 반복 trial을 3회만 두어도 6,912 records가 된다.

### 1차 추천: 5-level fixed-speed grid

현재 가장 방어 가능한 후보는 다음 5개 fixed RPM이다.

```text
600, 900, 1200, 1500, 1800 RPM
```

선정 이유는 다음과 같다.

- 600 RPM은 UOS v1의 최저 speed와 연결된다.
- 900 RPM은 Paderborn 조건과 겹친다.
- 1200 RPM은 UOS v1 중앙부 조건과 연결된다.
- 1500 RPM은 Paderborn 및 PRONOSTIA 조건과 겹친다.
- 1800 RPM은 PRONOSTIA 조건과 겹치고, 일반 4-pole motor의 nominal speed 근처 비교점으로 설명 가능하다.
- 300 RPM 간격은 shaft frequency 기준 5 Hz 간격이므로 해석이 단순하다.
- 10초 record에서 100-300회전을 확보한다.
- 예시 6205 order 기준 15x BSF도 약 1.06 kHz 이하라서, 12.8 또는 25.6 kS/s 후보에서 충분한 저주파 fault-band margin을 가진다.

### 시간/조건 수가 부담될 때: 3-level reduced grid

복합 결함 조합, load 조건, 반복 수가 많아져 전체 수집량이 부담되면 다음 3개 RPM으로 줄일 수 있다.

```text
600, 1200, 1800 RPM
```

이 경우 장점은 조건 수를 줄이면서 low/mid/high speed 효과를 볼 수 있다는 점이다. 단점은 Paderborn의 900/1500 RPM과 직접 겹치는 조건이 사라진다는 점이다. 선행 데이터셋 비교 설명을 중시하면 5-level grid가 낫다.

### v1 continuity를 가장 중시할 때

UOS v1과의 연속성을 최우선으로 두면 다음 grid도 가능하다.

```text
600, 800, 1000, 1200, 1400, 1600 RPM
```

이 후보는 v1과 가장 잘 연결되지만, Paderborn 900/1500, PRONOSTIA 1800과의 겹침은 약하다. 또한 조건 수가 6개로 늘어난다. v1 계승성이 논문상 핵심이 아니라면 600/900/1200/1500/1800이 더 균형 잡힌 후보로 보인다.

현재 사용자가 제시한 시나리오처럼 UOS v1 기준의 600-1600 RPM을 임시값으로 이미 잡아둔 상태라면, 바로 바꾸기보다는 다음과 같이 해석하는 것이 안전하다.

```text
Default scenario candidate:
600, 800, 1000, 1200, 1400, 1600 RPM

Alternative benchmark-aligned candidate:
600, 900, 1200, 1500, 1800 RPM
```

교수 검토에서는 두 안을 비교하고, v1 continuity를 우선할지 benchmark overlap과 조건 수 절감을 우선할지 결정하는 방식이 좋다.

## RPM-load 설계 주의

RPM을 정할 때 가장 피해야 할 것은 confounding이다.

나쁜 예시는 다음과 같다.

| Fault condition | RPM | Load |
|---|---:|---:|
| healthy | 600 | 0 Nm |
| IR | 900 | 0 Nm |
| OR | 1200 | 2 Nm |
| IR+OR | 1500 | 4 Nm |

이렇게 하면 모델이 결함을 학습한 것이 아니라 RPM 또는 load 차이를 학습할 수 있다.

더 나은 원칙은 다음과 같다.

- 모든 fault condition을 같은 RPM grid에서 측정한다.
- load를 쓴다면 각 RPM에서 동일한 load grid를 반복한다.
- 시간 제약 때문에 일부 조합을 생략하면 incomplete block으로 명시한다.
- acquisition order는 fault/RPM/load 순서가 한쪽으로 몰리지 않게 randomize 또는 block design으로 배치한다.
- 실제 measured RPM을 저장하고, commanded RPM과 measured RPM을 구분한다.

## variable-speed/run-up 조건의 위치

Ottawa 2018과 KAIST Batch는 시간에 따라 speed가 변하는 데이터를 제공한다. 이는 UOS v2에서도 매력적인 확장 후보지만, 처음부터 main grid에 섞으면 annotation과 물리 검증이 복잡해진다.

따라서 현재 추천은 다음과 같다.

- main dataset: fixed-speed grid 중심
- pilot extension: 일부 healthy/pure-fault 조건에서 run-up 또는 varying-speed record 별도 수집
- compound-fault main comparison: fixed-speed 조건에서 먼저 검증

이렇게 하면 UOS v2의 핵심인 synchronized multi-position vibration과 compound fault validation을 먼저 안정화하고, variable-speed 연구는 확장 가능성으로 남길 수 있다.

## 현재 결론

현재 문헌조사, UOS v1 연속성, 대표 benchmark와의 겹침, 회전 수, fault-frequency 대역 계산을 함께 보면 다음 후보가 가장 균형적이다.

```text
Benchmark-aligned fixed-speed candidate:
600, 900, 1200, 1500, 1800 RPM
```

다만 현재 UOS v2 수집 시나리오 초안이 UOS v1 기준의 600-1600 RPM 6-level grid를 이미 사용하고 있으므로, 실무상 primary draft는 다음과 같이 둘 수 있다.

```text
UOS-v1-continuity draft candidate:
600, 800, 1000, 1200, 1400, 1600 RPM
```

조건 수가 부담되면 다음 reduced grid를 사용할 수 있다.

```text
Reduced pilot candidate:
600, 1200, 1800 RPM
```

단, 위 값은 최종 확정이 아니다. 최종 RPM grid는 다음 정보를 확인한 뒤 확정해야 한다.

- 실제 UOS v2에서 사용할 bearing model 확정
- 6204, N204/NJ204, 30204 각각의 BPFO/BPFI/BSF/FTF order coefficient
- motor/rig가 안정적으로 유지 가능한 speed range
- load 조건에서의 slip, 발열, 안전성
- tachometer/speed sensor의 측정 및 vibration record와의 시간 정렬
- pilot spectrum에서 BPFO/BPFI/BSF/FTF, harmonic, sideband, envelope peak가 안정적으로 보이는지
- 각 RPM/load/fault condition에서 clipping, noise, stationarity 문제가 없는지
