# 데이터 길이와 windowing 설계 근거

## 결정 상태

UOS Dataset v2의 조건별 synchronized master record 길이는 60초로 결정했다. Window 길이, overlap, 안정화 제외, 공개 파생본과 split 방식은 아직 확정하지 않는다. 이 문서는 60초 원신호를 짧은 sample로 나눌 때 발생할 수 있는 과대평가 문제와 분석 기준을 정리한다.

핵심 질문은 단순히 "몇 초를 측정할 것인가"가 아니다. 더 중요한 질문은 다음이다.

- 장비가 실제로 연속 측정하는 master record 길이는 얼마인가?
- 모델 입력으로 사용할 window 길이는 얼마인가?
- window를 어떻게 자를 것인가?
- train/test split은 어떤 단위로 할 것인가?
- window 개수가 실제 독립 실험 수를 과장하지 않는가?

## 용어 구분

데이터 길이를 논할 때 다음 용어를 구분해야 한다.

| Term | 의미 |
|---|---|
| acquisition duration | 장비가 실제로 연속 측정한 시간 |
| master record duration | 공개 또는 보존하는 원 진동 record의 길이 |
| stored file duration | 파일 하나에 저장된 신호 길이 |
| snapshot length | 장기 실험 중 일정 간격으로 짧게 저장한 조각 |
| analysis window length | 모델 입력 또는 feature extraction에 사용하는 잘린 구간 길이 |
| effective independent sample | 실제로 독립적인 물리 실험/조립/반복에서 나온 sample |

예를 들어 160초를 한 번 측정한 뒤 1초 window 160개로 자르면, 파일상 sample은 160개처럼 보일 수 있다. 그러나 이것은 독립적인 실험 160번과 같지 않다. 같은 bearing, 같은 mounting, 같은 RPM, 같은 physical acquisition run에서 나온 서로 강하게 correlated된 window들이다.

## 외부 데이터셋의 record 길이를 해석하는 방식

선행 데이터셋에서 "record length가 10초"라고 되어 있어도 항상 같은 의미는 아니다. 최소한 다음 세 가지 방식을 구분해야 한다.

| 방식 | 의미 | 해석상 주의점 |
|---|---|---|
| long master record 후처리 | 조건 하나에서 긴 신호를 연속 측정하고, 이후 짧은 window로 잘라 사용 | window 수가 많아도 독립 실험 수가 많아진 것은 아님 |
| short master record 직접 저장 | 조건 하나에서 5초 또는 10초 정도를 연속 측정하고, 그 원신호 파일을 dataset record로 저장 | 10초 record 자체가 raw/master record이며, 필요하면 그 안에서 다시 1/2/5초 window를 만들 수 있음 |
| long-term experiment의 snapshot 저장 | 장시간 운전 또는 run-to-failure 실험 중 일정 간격마다 짧은 신호 조각만 저장 | 전체 운전 시간과 공개된 vibration snapshot 길이를 혼동하면 안 됨 |

따라서 "10초 데이터가 많다"는 말은 두 가지로 나누어 해석해야 한다.

```text
조건별로 10초 raw/master record가 여러 개 있는 것
≠
10초 record를 잘라 만든 1초 ML sample이 여러 개 있는 것
```

예를 들어 조건 하나에서 10초를 연속 측정했다면 기본 구조는 다음과 같다.

```text
RPM 1200, IR fault, load A
→ 10초 연속 측정
→ 10초 raw/master record 1개 저장
→ 필요하면 1초 non-overlap window 10개 또는 2초 window 5개 생성
```

이 경우 10초 신호는 원본 데이터이고, 1초 또는 2초 sample은 후처리로 만든 analysis window다. 반대로 NASA IMS나 XJTU-SY처럼 run-to-failure 성격의 데이터셋은 전체 실험이 장시간 진행되지만, 공개 vibration data는 일정 간격으로 저장된 짧은 snapshot이다. 이때는 "실험 duration"과 "snapshot length"를 분리해서 기록해야 한다.

UOS v2에서는 이 혼동을 피하기 위해 다음 metadata를 명시하는 것이 바람직하다.

```yaml
acquisition_duration_seconds: 10
master_record_duration_seconds: 10
stored_file_duration_seconds: 10
window_length_seconds: [1, 2, 5, 10]
window_source: derived_from_master_record
split_group: physical_acquisition_run
```

즉 현재 후보 전략인 "조건당 10초 synchronized master record를 저장하고, 이후 1/2/5/10초 window를 정의한다"는 방식은 short master record 직접 저장 방식에 해당한다. 중요한 점은 window를 만들더라도 train/test split은 window 단위가 아니라 physical acquisition run 또는 bearing instance 단위로 먼저 정해야 한다는 것이다.

## UOS v1의 긴 record 해석

UOS v1은 8 kHz와 16 kHz 두 sampling rate에서 같은 sample count를 맞추기 위해 서로 다른 duration을 사용했다.

| Sampling rate | Duration | Samples per file |
|---:|---:|---:|
| 8 kHz | 160 s | 1,280,000 |
| 16 kHz | 80 s | 1,280,000 |

즉 UOS v1의 80/160초는 다음 관계로 이해하는 것이 안전하다.

```text
8,000 Hz × 160 s = 1,280,000 samples
16,000 Hz × 80 s = 1,280,000 samples
```

이 설계는 같은 sample count를 맞춘다는 장점이 있지만, 그 자체가 물리적으로 80초 또는 160초가 반드시 필요하다는 근거는 아니다. UOS v2에서는 긴 duration을 그대로 계승하기보다, master record 길이와 analysis window 길이를 분리해서 설계해야 한다.

## 긴 record가 만드는 sample 수 착시

긴 record를 짧은 window로 자르면 sample 수가 빠르게 늘어난다.

예를 들어 160초 record를 non-overlap window로 자르면 다음과 같다.

| Window length | Non-overlap windows from 160 s |
|---:|---:|
| 1 s | 160 |
| 2 s | 80 |
| 5 s | 32 |
| 10 s | 16 |

50% overlap을 사용하면 window 수는 더 늘어난다.

| Window length | Step | Approx. windows from 160 s |
|---:|---:|---:|
| 1 s | 0.5 s | 319 |
| 2 s | 1 s | 159 |
| 5 s | 2.5 s | 63 |
| 10 s | 5 s | 31 |

하지만 이 window들은 같은 physical run에서 나온 조각이므로 독립 sample로 취급하면 안 된다. sample count는 많아져도 effective independent sample 수는 크게 늘지 않을 수 있다.

## window-level split의 과대평가 위험

가장 위험한 방식은 긴 record를 먼저 window로 자른 뒤, window 단위로 무작위 train/test split을 하는 것이다.

```text
long record
→ 1 s windows
→ random train/test split
```

이렇게 하면 같은 physical run에서 나온 유사한 window가 train과 test에 동시에 들어갈 수 있다. 이 경우 모델은 결함의 일반적인 물리 특징보다 다음 정보를 외울 수 있다.

- 같은 bearing instance의 고유 신호
- 같은 mounting 상태
- 같은 sensor/cable response
- 같은 RPM stability
- 같은 rig resonance
- 같은 acquisition order나 noise pattern

그 결과 within-dataset accuracy는 높게 나오지만, 다른 bearing, 다른 assembly, 다른 rig, 다른 dataset에서는 성능이 크게 떨어질 수 있다.

이 현상은 특정 외부 데이터셋 하나에만 해당하는 문제가 아니다. 어떤 외부 benchmark와 비교하더라도 다음 상황이 가능하다.

```text
UOS 내부 random-window 평가에서는 성능이 높음
다른 rig/sensor/load/fault-generation dataset에서는 성능이 낮음
```

이때 원인은 모델 자체만이 아니라, UOS 내부 평가가 correlated windows 때문에 과대평가되었을 가능성도 함께 검토해야 한다.

## 올바른 split 단위

UOS v2에서는 window 단위 split을 기본 평가로 사용하면 안 된다. split은 windowing 전에 더 큰 물리 단위에서 수행해야 한다.

권장 split 계층은 다음과 같다.

```text
bearing type
→ bearing instance
→ fault assembly
→ RPM/load condition
→ physical acquisition run
→ windows
```

최소 원칙은 다음과 같다.

- train/test split은 windowing 전에 수행한다.
- 같은 physical acquisition run에서 나온 window가 train과 test에 동시에 들어가면 안 된다.
- 가능하면 같은 bearing instance 또는 같은 remount/assembly가 train/test에 동시에 들어가지 않도록 별도 평가를 둔다.
- RPM generalization, bearing-type generalization, fault-combination generalization은 별도 split으로 정의한다.

## 추천 evaluation split

UOS v2는 하나의 random accuracy만 보고하지 말고, 여러 난이도의 split을 제공하는 것이 좋다.

| Split name | Train/test 분리 기준 | 목적 |
|---|---|---|
| window split | window 단위 무작위 분할 | baseline 또는 leakage demonstration 용도. 주 평가로 사용하지 않음 |
| run-grouped split | physical acquisition run 단위 분할 | 같은 run leakage 방지 |
| bearing-instance split | bearing instance 단위 분할 | 같은 베어링 개체 memorization 방지 |
| remount/assembly split | 재조립 또는 remount 단위 분할 | mounting/assembly signature memorization 방지 |
| RPM-held-out split | 일부 RPM을 test로 제외 | speed generalization 평가 |
| bearing-type-held-out split | 일부 bearing type을 test로 제외 | bearing type domain shift 평가 |
| fault-combination-held-out split | 일부 compound 조합을 test로 제외 | multi-label 조합 일반화 평가 |

주 논문에서는 최소한 run-grouped split을 기본값으로 삼고, window split은 성능 과대평가 가능성을 보이는 보조 실험으로만 다루는 것이 안전하다.

## record length 선정 기준

데이터 길이는 다음 조건을 동시에 고려해서 정해야 한다.

### 1. 최저 RPM에서의 회전 수

600 RPM은 10 rps이므로, duration별 회전 수는 다음과 같다.

| Duration | Rotations at 600 RPM |
|---:|---:|
| 1 s | 10 |
| 2 s | 20 |
| 5 s | 50 |
| 10 s | 100 |
| 60 s | 600 |
| 80 s | 800 |
| 160 s | 1600 |

60초 record는 600 RPM에서도 600회전을 포함한다. 충분한 원신호를 보존하면서 1/2/5/10/30초 window를 동일 run에서 비교할 수 있다. 다만 60초에서 만든 여러 window는 독립 실험이 아니며, 1초 window는 on-device inference 후보로는 의미가 있지만 물리 검증용 단독 record로는 짧을 수 있다.

### 2. 주파수 해상도

FFT bin spacing은 `1/T`이다.

| Duration | Frequency resolution |
|---:|---:|
| 1 s | 1 Hz |
| 2 s | 0.5 Hz |
| 5 s | 0.2 Hz |
| 10 s | 0.1 Hz |
| 60 s | 0.0167 Hz |
| 80 s | 0.0125 Hz |
| 160 s | 0.00625 Hz |

80/160초는 매우 높은 주파수 해상도를 제공하지만, 조건 수가 많은 UOS v2에서는 저장량과 correlated window 문제가 커진다.

### 3. stationarity

record가 너무 길면 같은 조건이라고 해도 다음 변화가 생길 수 있다.

- bearing/shaft 온도 변화
- grease 또는 접촉 상태 변화
- RPM drift
- mounting/cable 상태 변화
- 결함 충격의 비정상성

따라서 긴 record가 항상 좋은 것은 아니다. UOS v2는 60초 master를 보존하되, 5초 단위 RMS와 RPM drift로 record 내부 stationarity를 확인하고 모델 입력은 더 짧은 window도 함께 비교한다.

### 4. 저장 용량과 조건 수

UOS v2 시나리오 초안은 sampling rate를 제외하면 다음 조건 수를 가진다.

```text
6 RPM × 3 bearing types × 8 rotor classes × 8 bearing classes = 1,152 condition cells
```

sampling rate 2개를 모두 별도 취득하면:

```text
1,152 × 2 = 2,304 record cells
```

여기에 반복 trial 수를 곱하면 전체 record 수는 빠르게 커진다. 따라서 UOS v1처럼 80/160초를 모든 조건에 적용하면 저장량과 후처리 비용이 커진다.

## 추천 수집/공개 전략

현재 가장 방어 가능한 전략은 다음이다.

```text
1. 각 physical condition에서 60초 synchronized 4-channel master record를 수집한다.
2. 같은 master record에서 1초, 2초, 5초, 10초, 30초, 60초 deterministic windows를 비교한다.
3. raw master record와 window index를 모두 공개한다.
4. train/test split은 physical run 또는 bearing instance 기준으로 먼저 정의한다.
5. window는 split 이후에 생성하거나, split group ID를 반드시 유지한다.
```

이 전략의 장점은 다음과 같다.

- 긴 raw signal을 보존한다.
- 1/2/5/10/30/60초 window 성능 비교가 가능하다.
- on-device inference용 짧은 window를 제공할 수 있다.
- 같은 master record에서 나온 paired window 비교가 가능하다.
- window leakage를 통제할 수 있다.
- UOS v1보다 짧은 record를 쓰더라도 물리적 근거를 제시할 수 있다.

## pilot에서 확인할 항목

pilot에서는 다음을 확인해야 한다.

- 60초 record 안에서 RPM, RMS와 온도가 충분히 안정적인가?
- 1/2/5/10/30/60초 window에서 BPFO/BPFI/BSF/FTF와 harmonic이 안정적으로 보이는가?
- envelope spectrum에서 필요한 대역이 window 길이에 따라 얼마나 달라지는가?
- 1초 또는 2초 window가 on-device inference에 충분한가?
- 5초 또는 10초 window가 물리 검증에 충분한가?
- 같은 physical run에서 나온 window 간 correlation이 얼마나 큰가?
- window-level split과 run-grouped split 사이 성능 차이가 얼마나 나는가?

특히 마지막 항목은 중요하다. window-level split 성능이 높고 run-grouped split 성능이 낮다면, 이는 긴 record에서 나온 correlated window가 성능을 과대평가했을 가능성을 보여준다.

## 현재 결론

UOS v1의 80/160초 record는 sample count를 맞춘 설계로 이해하는 것이 안전하다. UOS v2에서는 이를 그대로 계승하기보다, master record와 analysis window를 분리해서 설계하는 것이 더 방어적이다.

현재 추천은 다음과 같다.

```text
Master record decision:
60 s synchronized 4-channel record

Analysis-window candidates:
1 s, 2 s, 5 s, 10 s, 30 s, 60 s

Default evaluation split:
physical-run grouped split

Stronger evaluation:
bearing-instance/remount/RPM-held-out split
```

60초 master 수집 길이는 결정됐다. Canonical analysis window, overlap과 안정화 제외는 pilot spectrum, stationarity, storage estimate와 grouped-split 성능 차이를 확인한 뒤 확정한다.
