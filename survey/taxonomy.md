# Dataset Taxonomy

- **single-sensor**: 하나의 물리 센서 장치로 측정한다.
- **multi-sensor**: 둘 이상의 물리 센서 장치를 사용한다. modality가 같을 수도 있다.
- **multi-modal**: 서로 다른 물리량 또는 sensing modality를 함께 측정한다.
- **multi-channel**: 동시에 또는 한 record에 대응하는 둘 이상의 신호 채널이 있다. 센서 수와 동일하다고 가정하지 않는다.
- **multi-position**: 서로 다른 물리 위치에서 측정한다.
- **multi-direction**: 서로 다른 공간 방향/축의 진동을 측정한다.
- **triaxial**: 한 센서 패키지가 일반적으로 직교하는 세 축을 측정한다.
- **simultaneous sampling**: 채널들이 같은 sampling instant에서 하드웨어적으로 샘플링된다.
- **synchronized acquisition**: 채널/장치의 시간 기준이 정렬되며, simultaneous sampling보다 넓은 개념이다. 동시 샘플링 여부는 별도 기록한다.
- **batch fault dataset**: 사전에 정의한 상태별로 유한한 실험 run을 수집한 데이터셋이다.
- **run-to-failure dataset**: 정상 또는 초기 상태부터 고장에 이를 때까지 시간 경과 데이터를 수집한다.
- **variable-speed dataset**: 한 데이터셋 또는 run에서 복수/변동 회전속도 조건을 명시한다.
- **single fault**: 동일 sample에 하나의 결함만 존재한다.
- **compound fault**: 동일 sample에 둘 이상의 결함이 동시에 존재한다.
- **internal bearing compound fault**: 동일 bearing 내부의 IR, OR, ball/roller, cage 중 둘 이상이 동시에 존재한다.
- **bearing–rotor compound fault**: bearing 결함과 unbalance, misalignment, looseness 등 rotor/rotating-system 결함이 동시에 존재한다.
- **bearing–gear compound fault**: bearing 결함과 gear 결함이 동시에 존재한다.
- **artificial fault**: 실험자가 의도적으로 결함 상태를 만든 결함의 상위 분류다.
- **natural fault**: 실제 운전/열화 과정에서 자연적으로 발생하거나 회수된 결함이다.
- **seeded fault**: 가공·손상 삽입 등으로 의도적으로 특정 결함을 심은 artificial fault다.
- **multi-class label**: sample마다 상호 배타적인 클래스 하나를 부여한다.
- **multi-label annotation**: sample마다 동시에 참인 복수 결함/상태 label을 독립적으로 부여할 수 있다.

## Classification examples

- 가속도계 + 마이크: multi-sensor이자 multi-modal이다.
- 서로 다른 위치의 가속도계 4개: multi-sensor, multi-channel, multi-position이지만 single modality다.
- 하나의 triaxial accelerometer: 3축/3채널이지만 반드시 multi-position은 아니다.
