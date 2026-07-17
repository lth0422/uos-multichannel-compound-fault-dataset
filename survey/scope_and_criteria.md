# Scope and Criteria

## Primary scope

- 논문으로 발표된 bearing 또는 rotating machinery dataset
- 공식 dataset paper가 있거나 공식 기관 문서로 구성이 검증 가능한 dataset
- 원시 진동 데이터가 공개되었거나 접근 방법이 명시된 dataset

## Secondary scope

- 널리 사용되는 canonical benchmark
- dedicated dataset paper가 없더라도 공식 문서가 있는 dataset

## Exclusion

- 블로그 설명만 존재하는 dataset
- 출처를 확인할 수 없는 Kaggle 재업로드
- 원 데이터셋을 임의로 전처리한 파생 dataset
- 센서와 결함 조건을 확인할 수 없는 dataset

## Evidence priority

1. Original paper
2. Official documentation
3. Official repository
4. Follow-up peer-reviewed paper
5. Secondary material

## Acquisition-design evidence to extract

각 데이터셋에서 아래 항목을 독립적으로 조사한다. 단순히 조건값만 옮기지 말고, 원문이 해당 선택의 근거나 검증을 제시하는지도 구분한다.

- 센서의 물리적 측정 위치와 housing/component 기준 위치
- 측정 방향/축, 센서 수, 채널 수, 센서 마운팅 방식
- 위치 선정의 명시적 rationale과 위치 비교·검증 방법
- sampling rate와 그 선택 근거(관심 주파수, anti-aliasing, 장비 한계 등)
- 고정/가변 RPM 조건, RPM 범위·간격, speed 측정 또는 제어 방법
- record당 진동 신호 길이, sample 수, segment/window 길이
- 조건별 반복 횟수와 총 record 수
- channel 간 simultaneous sampling 또는 synchronization 근거

원문이 값만 제시하고 타당성 근거를 설명하지 않으면 조건값은 기록하되 rationale/validation은 `Unknown`으로 둔다. 여러 데이터셋에서 자주 사용된 값이라는 이유만으로 UOS v2의 최종 조건으로 채택하지 않는다.
