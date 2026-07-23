# UOS Dataset v2 차별성 후보

## 한 줄 결론

> **가장 유력한 차별성은 여러 베어링 구조와 RPM에서 정상·단일·내부 복합·베어링–로터 복합 조건을 같은 4채널 동시 측정 방식으로 연결하고, 동일 신호의 단일·다채널 비교와 조건별 물리 검증까지 가능하게 하는 것**이다.

이 내용은 아직 최종 결론이 아니다. 기존 데이터셋의 공식 자료를 더 확인하고 예비 실험을 마친 뒤 확정한다.

## 한눈에 보는 비교표

이 표는 현재 조사한 16개 데이터셋과 UOS v2의 계획을 같은 기준으로 비교한 것이다.

- `O`: 검토한 원 논문 또는 공식 문서에서 확인됨
- `△`: 일부만 충족하거나, 자연 발생·제한된 조합·간접 비교에 해당함
- `X`: 검토한 자료에서 제공하거나 보고하지 않음
- `?`: 자료가 부족해 판단할 수 없음
- `P`: UOS v2에서 계획 중이며 아직 수집·검증하지 않음

| 데이터셋 | 내부 2중 3조합¹ | 내부 3중² | 베어링–로터 3종³ | 베어링–기어 복합⁴ | 다위치 진동 | 동시 샘플링 확인 | 동일 신호 채널 비교⁵ | 물리 검증⁶ | 여러 베어링 구조 | 여러 RPM |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **UOS v2 계획** | **P** | **P** | **P** | X | **P** | **P** | **P** | **P** | **P** | **P** |
| UOS v1[2] | X | X | O | X | X | ? | X | O | O | O |
| CWRU[8] | X | X | X | X | O | ? | X | △ | X | O |
| Paderborn[6] | △ | X | X | X | X | ? | X | O | X | O |
| XJTU-SY[9] | ? | ? | X | X | X | ? | X | △ | X | O |
| NASA IMS[7] | △ | X | X | X | O | ? | X | O | X | X |
| MAFAULDA[5] | X | X | △ | X | O | ? | △ | △ | X | O |
| Arkansas 2023[3] | △ | X | △ | X | O | ? | X | X | X | O |
| Ottawa 2018[10] | X | X | X | X | X | ? | X | △ | X | O |
| Ottawa 2023[11] | X | X | X | X | X | ? | X | O | X | X |
| PRONOSTIA[12] | △ | △ | X | X | X | ? | X | O | X | O |
| KAIST Batch[4] | X | X | X | X | O | O | X | O | X | O |
| HUST Vietnam[1] | O | X | X | X | X | ? | X | △ | X | △ |
| SEU[13] | △ | X | X | X | ? | ? | X | X | X | X |
| HUST China[14] | △ | X | X | X | ? | ? | X | X | X | O |
| **S1 Data[15]** | **O** | **O** | X | X | O | ? | X | O | X | X |
| **MCC5-THU[16]** | X | X | X | **O** | O | ? | X | △ | X | O |

- ¹ `내부 2중 3조합`은 IR+OR, IR+Ball, OR+Ball을 모두 뜻한다. 하나의 조합만 있거나 자연 손상으로 일부가 함께 발생한 경우는 `△`로 표시했다.
- ² `내부 3중`은 같은 베어링에 IR+OR+Ball이 동시에 존재하는 조건이다. PRONOSTIA의 `△`는 자연 열화로 여러 부품이 함께 손상된 사례이며, 통제된 IR+OR+Ball 분류 조건은 아니다.
- ³ `베어링–로터 3종`은 베어링 결함과 불평형·축정렬 불량·풀림의 결합을 뜻한다. MAFAULDA와 Arkansas는 일부 다른 조합만 제공하므로 `△`이다.
- ⁴ `베어링–기어 복합`은 같은 측정 조건에 베어링 결함과 기어 결함이 동시에 존재하는 경우다. UOS v2는 현재 기어 결함을 계획하지 않는다.
- ⁵ `동일 신호 채널 비교`는 같은 측정에서 단일채널과 다채널 입력을 만들어 같은 조건으로 평가하는 것을 뜻한다. MAFAULDA는 센서 묶음 비교가 있으나 이 기준을 모두 충족하지 않아 `△`이다.
- ⁶ `물리 검증`은 결함주파수, 포락선 스펙트럼, 회전주파수 또는 분해 후 손상 확인 중 하나 이상이 보고된 경우다. 모든 결함 조건을 동일 절차로 검증했다는 뜻은 아니다.

### 새 자료를 원문과 대조한 결과

- **S1 Data:** Fig. 9에서 지지 베어링과 결함 베어링의 1축 가속도계 2개, 기어박스의 3축 가속도계 1개가 확인된다. 따라서 3개 위치·5축 진동으로 표시했다. 단, 축 정의와 동시 샘플링 방식은 확인되지 않았다[15].
- **MCC5-THU:** 모터 구동단과 기어박스 중간축 베어링 좌석에서 3축씩 총 6축 진동을 측정한다. 기어 파손+베어링 IR, 기어 파손+베어링 OR 복합결함과 3단계 심각도가 확인된다[16].
- **MAFAULDA:** 내부 비교표에는 복합결함이 없다고 적혀 있었지만, 공식 문서상 베어링 결함 측정에 6·20·35 g 불평형 질량을 함께 사용한 조건이 있다. 따라서 베어링 내부 복합결함은 `X`지만 베어링–로터 복합은 `△`로 유지한다[5].

### 표에서 보이는 핵심

S1 Data는 내부 2중 세 조합과 3중 결함, 5축 다위치 진동, 복합결함 포락선 분석을 이미 제공한다[15]. MCC5-THU는 6축 다위치 진동, 속도·토크, 60초 가변조건, 3단계 심각도와 베어링–기어 복합결함을 제공한다[16]. 따라서 내부 3중 결함이나 다채널 복합결함만으로는 차별성을 주장할 수 없다.

현재 검토 범위에서 남는 조합은 **여러 베어링 구조와 RPM에서 정상·단일·내부 복합·베어링–로터 복합을 같은 동시 4채널 방식으로 연결하고, 동일 신호의 단일·다채널 비교와 조건별 검증을 함께 제공하는 것**이다. UOS v2가 계획한 항목을 실제로 수집하고 검증한다면 다음과 같이 설명할 수 있다.

> **기존 데이터셋에 각각 존재하는 복합결함과 다위치 진동을, 여러 베어링 구조·RPM·베어링–로터 조건까지 확장하고 동일 신호 채널 비교와 조건별 검증으로 연결한다.**

다만 현재 UOS v2 행은 전부 `P`이다. 수집과 검증이 끝나기 전에는 “우리는 모두 제공한다”가 아니라 “모두 제공하는 것을 목표로 한다”고 표현해야 한다. 최종적으로 수행하지 않은 항목은 `P`를 `O`로 바꾸지 않고 표와 차별성 설명에서 제외한다.

## 우리가 만들려는 데이터

현재 검토 중인 구성은 다음과 같다.

- 베어링 정상 및 단일결함: IR(내륜), OR(외륜), Ball(볼)
- 베어링 내부 복합결함: IR+OR, IR+Ball, OR+Ball, IR+OR+Ball
- 로터 결함: Unbalance(불평형), Misalignment(축정렬 불량), Looseness(풀림)
- 베어링 결함과 로터 결함이 동시에 존재하는 조건
- 축 양쪽 베어링 하우징의 상단·측면에서 수집한 4채널 진동
- 같은 측정 신호에서 만든 단일채널·2채널·4채널 비교 데이터
- 결함주파수, 회전주파수, envelope spectrum(포락선 스펙트럼) 등을 이용한 결함 확인

조건별 synchronized master record 길이는 60초로 결정했다. 센서 위치, 25.6 kS/s의 샘플링 주파수, RPM, 분석 window와 결함 조합 수는 아직 후보값이다.

## 그래서 무엇이 다른가

### 1. 베어링 내부결함과 로터결함을 하나의 체계로 비교한다

기존 데이터셋에도 복합결함은 있다. HUST Vietnam은 IR+OR, IR+Ball, OR+Ball을 제공한다[1]. S1 Data는 이 세 조합과 IR+OR+Ball까지 제공한다[15]. UOS v1은 베어링 결함과 불평형·축정렬 불량·풀림이 결합된 조건을 제공한다[2]. Arkansas 데이터셋에도 베어링 결함과 굽은 축이 함께 존재하는 조건이 있고[3], MCC5-THU는 기어 파손과 베어링 IR/OR 결함을 결합한다[16].

따라서 “복합결함이 있다”, “내부 3중 결함이 있다”, “다채널로 복합결함을 측정했다”만으로는 차별성이 아니다.

UOS v2의 차별성 후보는 다음 조건을 **같은 장비, 같은 운전조건, 같은 측정 규칙**으로 연결하는 것이다.

| 구분 | 비교 조건 |
|---|---|
| 기준 데이터 | 정상 |
| 베어링 단일결함 | IR, OR, Ball |
| 베어링 내부 복합결함 | IR+OR, IR+Ball, OR+Ball, IR+OR+Ball |
| 로터 단일결함 | 불평형, 축정렬 불량, 풀림 |
| 베어링–로터 복합결함 | 위 베어링 결함과 로터 결함이 동시에 존재하는 조건 |

즉, S1에 이미 있는 결함 조합을 반복하는 것이 아니라 **여러 베어링 구조와 RPM에서 정상·단일결함 → 베어링 내부 복합결함 → 베어링–로터 복합결함**으로 이어지는 비교 구조를 만드는 것이 핵심이다.

다만 모든 조합을 실제로 수집할지는 결함 제작 가능성, 안전성, 반복성, 전체 데이터 규모를 확인한 후 정한다.

### 2. 같은 측정에서 단일채널과 다채널을 공정하게 비교한다

다위치·다채널 진동 데이터도 이미 존재한다. KAIST Batch는 두 베어링 하우징의 x·y 방향에서 가속도계 4개를 동시에 측정한다[4]. MAFAULDA는 두 베어링 위치에서 6축 진동을 수집하며, 특정 실험에서 한쪽과 양쪽 센서 사용 결과를 비교했다[5]. S1 Data는 지지 베어링·결함 베어링·기어박스의 5축 진동을 사용하고[15], MCC5-THU는 모터와 기어박스 베어링 위치에서 6축 진동을 수집한다[16].

따라서 “4채널 진동” 자체도 차별성이 아니다.

UOS v2에서는 하나의 물리적 측정에서 다음 입력을 함께 만들 수 있다.

- CH1, CH2, CH3, CH4 각각의 단일채널 입력
- 같은 베어링 위치의 2채널 입력
- 서로 다른 베어링 위치를 조합한 2채널 입력
- 전체 4채널 입력

모든 입력이 같은 시점의 같은 운전상태에서 나오므로, 채널 수 외의 조건을 최대한 동일하게 유지할 수 있다. 이를 paired comparison(동일 측정 기반 짝지어진 비교)이라고 한다.

이 비교를 통해 확인하려는 것은 “다채널이 항상 더 좋다”가 아니다. 다음 질문에 답하는 것이 목적이다.

- 어느 센서 위치가 어떤 결함을 잘 감지하는가?
- 두 위치의 정보가 실제로 서로 보완적인가?
- 복합결함에서 다채널의 효과가 단일결함보다 큰가?
- 일부 채널이 없거나 잡음이 심할 때 성능이 얼마나 변하는가?

성능 향상은 실제 비교 실험 결과가 나온 뒤에만 수치로 제시한다.

### 3. 결함이 실제로 측정되었는지 조건별로 검증한다

기존에도 결함주파수와 포락선 스펙트럼을 사용한 데이터셋이 있다. UOS v1과 Paderborn은 베어링 결함주파수에 근거한 분석을 제시했고[2][6], NASA IMS는 결함주파수와 분해 후 손상 상태를 함께 확인했다[7]. S1 Data는 네 가지 내부 복합결함의 계산 주파수와 포락선 스펙트럼을 비교했으며[15], MCC5-THU는 기어 결함 예제에서 회전·기어물림·측파대 성분을 확인했다[16].

따라서 FFT(고속 푸리에 변환)나 포락선 스펙트럼 그림을 제시하는 것만으로는 차별성이 아니다.

UOS v2에서는 각 조건마다 다음 사항을 같은 기준으로 확인하는 방안을 검토한다.

- 실제 RPM과 회전주파수
- 베어링 형상으로 계산한 BPFO(외륜 결함주파수), BPFI(내륜 결함주파수), BSF(볼 결함주파수)
- 결함주파수와 고조파가 원신호·포락선 스펙트럼에 나타나는지
- 로터결함의 회전주파수 성분과 고조파가 나타나는지
- 4개 채널에서 신호가 어떻게 다르게 전달되는지
- 센서 포화, 잡음, RPM 흔들림, 누락값 여부
- 반복 측정과 센서 재부착 후에도 결과가 유지되는지
- 측정 후 실제 결함 상태를 사진 또는 치수로 다시 확인했는지

특히 복합결함에서는 예상 성분이 보이지 않을 수도 있다. 이 경우에도 결함이 확인되었다고 처리하지 않고, 확인 실패 또는 결과 불일치로 기록한다.

## 보조적인 강점

아래 항목은 단독 차별성이라기보다 데이터의 신뢰성과 활용도를 높이는 요소다.

### 측정 조건을 자세히 기록

베어링 번호, 결함 제작 정보, 조립·재부착 번호, 센서 위치, 실제 RPM, 하중, 수집 순서와 온도 등을 함께 기록한다. 이렇게 해야 모델이 결함이 아니라 특정 베어링이나 수집 순서를 외워서 높은 성능을 내는 문제를 줄일 수 있다.

### 물리적 측정 단위로 학습·시험 데이터 분리

한 번 수집한 60초 신호를 여러 구간으로 나누면 파일 수는 늘어나지만, 각 구간은 서로 매우 비슷하다. 같은 60초 신호에서 나온 구간을 학습 데이터와 시험 데이터에 나누어 넣으면 성능이 실제보다 높게 보일 수 있다.

따라서 같은 측정에서 잘라낸 모든 구간은 같은 그룹에 두고, 가능하면 측정 회차·베어링 개체·재조립 단위로 학습·검증·시험 데이터를 나눈다.

### 원신호와 짧은 분석 구간을 함께 제공

60초 동시 측정 원신호를 보존하고, 1초·2초·5초·10초·30초 분석 구간을 동일한 규칙으로 만들 수 있다. 이렇게 하면 물리 분석에는 긴 신호를 사용하고, 실시간 추론 연구에는 짧은 신호를 사용할 수 있다.

60초 master 수집 길이는 결정했다. 첫 구간을 고정적으로 버릴지, tachometer와 RMS 기반 안정화 규칙으로 일부만 제외할지는 추가 파일럿 후 확정한다.

## 차별성이 아닌 것

다음 표현은 현재 조사 결과와 맞지 않으므로 사용하지 않는다.

- “최초의 다채널 회전기계 데이터셋”
- “최초의 복합결함 데이터셋”
- “기존 데이터셋에는 베어링–로터 복합결함이 없다”
- “다채널은 단일채널보다 항상 우수하다”
- “현재 제안한 센서 위치가 최적이다”
- “25.6 kS/s와 60초가 최적의 수집 조건이다”

## 현재 가장 적절한 설명

논문 작성 전 단계에서는 다음처럼 설명하는 것이 가장 정확하다.

> UOS Dataset v2는 베어링 단일결함, 베어링 내부 복합결함, 로터결함 및 베어링–로터 복합결함을 같은 시험 장치와 운전조건에서 비교할 수 있도록 구성하는 것을 목표로 한다. 또한 동일 시점에 수집한 4채널 진동을 이용하여 단일채널과 다채널 진단을 공정하게 비교하고, 각 결함 조건을 물리적 특징과 실험 기록으로 검증하는 것을 목표로 한다. 이 구성의 신규성과 최종 수집 조건은 기존 데이터셋의 추가 확인과 예비 실험 후 확정한다.

더 짧게 표현하면 다음과 같다.

> **체계적인 복합결함 구성 + 동일 측정 기반 단일·다채널 비교 + 조건별 물리 검증**

## 확정하기 위해 남은 작업

1. S1 Data와 MCC5-THU의 공식 저장소에서 실제 채널 구조, 동시성, 파일 형식과 라이선스를 추가 확인한다.
2. 다채널 성능 비교 논문의 원문에서 센서 종류·위치, 데이터 분할 방식, 비교 조건과 성능 수치를 확인한다.
3. 4채널 후보 위치가 서로 다른 유용한 정보를 제공하는지 예비 실험으로 확인한다.
4. 베어링 형상과 RPM을 이용해 조건별 결함주파수 범위를 계산한다.
5. 베어링 내부 3중 결함과 베어링–로터 조합을 반복 제작할 수 있는지 확인한다.
6. 선택한 60초 master에서 1/2/5/10/30/60초 window의 물리 신호 안정성, 모델 성능과 저장 비용을 비교한다.

## 참고문헌

[1] N. D. Thuan and H. S. Hong, “HUST bearing: a practical dataset for ball bearing fault diagnosis,” *BMC Research Notes*, vol. 16, 2023. DOI: [10.1186/s13104-023-06400-4](https://doi.org/10.1186/s13104-023-06400-4).

[2] S. Lee, T. Kim, and T. Kim, “Multi-domain vibration dataset with various bearing types under compound machine fault scenarios,” *Data in Brief*, vol. 57, 2024, Art. 110940. DOI: [10.1016/j.dib.2024.110940](https://doi.org/10.1016/j.dib.2024.110940).

[3] L. Marshall and D. Jensen, “Dataset of single and double faults scenarios using vibration signals from a rotary machine,” *Data in Brief*, vol. 49, 2023, Art. 109358. DOI: [10.1016/j.dib.2023.109358](https://doi.org/10.1016/j.dib.2023.109358).

[4] W. Jung, S.-H. Kim, S.-H. Yun, J. Bae, and Y.-H. Park, “Vibration, acoustic, temperature, and motor current dataset of rotating machine under varying operating conditions for fault diagnosis,” *Data in Brief*, vol. 48, 2023, Art. 109049. DOI: [10.1016/j.dib.2023.109049](https://doi.org/10.1016/j.dib.2023.109049).

[5] D. Pestana-Viana, R. Zambrano-Lopez, A. A. de Lima, T. de M. Prego, S. L. Netto, and E. A. B. da Silva, “The influence of feature vector on the classification of mechanical faults using neural networks,” *2016 IEEE 7th Latin American Symposium on Circuits and Systems*, 2016. DOI: [10.1109/LASCAS.2016.7451023](https://doi.org/10.1109/LASCAS.2016.7451023).

[6] C. Lessmeier, J. K. Kimotho, D. Zimmer, and W. Sextro, “Condition Monitoring of Bearing Damage in Electromechanical Drive Systems by Using Motor Current Signals of Electric Motors: A Benchmark Data Set for Data-Driven Classification,” *European Conference of the Prognostics and Health Management Society*, 2016. 공식 데이터셋 페이지: [Paderborn KAt Data Center](http://mb.uni-paderborn.de/kat/datacenter).

[7] H. Qiu, J. Lee, J. Lin, and G. Yu, “Wavelet filter-based weak signature detection method and its application on rolling element bearing prognostics,” *Journal of Sound and Vibration*, vol. 289, pp. 1066–1090, 2006. DOI: [10.1016/j.jsv.2005.03.007](https://doi.org/10.1016/j.jsv.2005.03.007).

[8] Case Western Reserve University, “Bearing Data Center,” Case School of Engineering. 공식 문서: [CWRU Bearing Data Center](https://engineering.case.edu/bearingdatacenter).

[9] B. Wang, Y. Lei, N. Li, and N. Li, “A Hybrid Prognostics Approach for Estimating Remaining Useful Life of Rolling Element Bearings,” *IEEE Transactions on Reliability*, vol. 69, no. 1, pp. 401–412, 2020. DOI: [10.1109/TR.2018.2882682](https://doi.org/10.1109/TR.2018.2882682).

[10] H. Huang and N. Baddour, “Bearing vibration data collected under time-varying rotational speed conditions,” *Data in Brief*, vol. 21, pp. 1745–1749, 2018. DOI: [10.1016/j.dib.2018.11.019](https://doi.org/10.1016/j.dib.2018.11.019).

[11] M. Sehri, P. Dumond, and M. Bouchard, “University of Ottawa constant load and speed rolling-element bearing vibration and acoustic fault signature datasets,” *Data in Brief*, vol. 49, 2023, Art. 109327. DOI: [10.1016/j.dib.2023.109327](https://doi.org/10.1016/j.dib.2023.109327).

[12] P. Nectoux et al., “PRONOSTIA: An Experimental Platform for Bearings Accelerated Degradation Tests,” *IEEE International Conference on Prognostics and Health Management*, 2012. 공식 공개본: [HAL hal-00719503](https://hal.science/hal-00719503).

[13] S. Shao, S. McAleer, R. Yan, and P. Baldi, “Highly Accurate Machine Fault Diagnosis Using Deep Transfer Learning,” *IEEE Transactions on Industrial Informatics*, vol. 15, no. 4, pp. 2446–2455, 2019. DOI: [10.1109/TII.2018.2864759](https://doi.org/10.1109/TII.2018.2864759).

[14] C. Zhao, E. Zio, and W. Shen, “Domain generalization for cross-domain fault diagnosis: An application-oriented perspective and a benchmark study,” *Reliability Engineering & System Safety*, vol. 245, 2024, Art. 109964. DOI: [10.1016/j.ress.2024.109964](https://doi.org/10.1016/j.ress.2024.109964); 공식 데이터셋 저장소: [HUSTbearing](https://github.com/CHAOZHAO-1/HUSTbearing-dataset).

[15] Y. Wang, H. Yang, S. Zhao, Y. Fan, and R. Dong, “Vibration characterization of rolling bearings with compound fault features under multiple interference factors,” *PLOS ONE*, vol. 19, no. 2, 2024, e0297935. DOI: [10.1371/journal.pone.0297935](https://doi.org/10.1371/journal.pone.0297935).

[16] S. Chen, Z. Liu, X. He, D. Zou, and D. Zhou, “Multi-mode fault diagnosis datasets of gearbox under variable working conditions,” *Data in Brief*, vol. 54, 2024, Art. 110453. DOI: [10.1016/j.dib.2024.110453](https://doi.org/10.1016/j.dib.2024.110453).

## 저장소 내 상세 근거

- [데이터셋 비교표](../survey/synthesis/comparison_master.md)
- [연구 공백 분석](../survey/synthesis/gap_analysis.md)
- [근거 기반 주장 목록](../survey/synthesis/claim_bank.md)
- [UOS v2 설계 시사점](../survey/synthesis/implications_for_uos_v2.md)

최종 검토일: 2026-07-20
