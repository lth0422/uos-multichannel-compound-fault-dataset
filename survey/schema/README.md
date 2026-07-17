# Survey Schema

`facts.yaml`은 비교표용 구조화 사실, `sources.yaml`은 출처 목록, `evidence.md`는 사실-근거 추적표입니다. Yes/No 성격의 값은 `Yes`, `Partial`, `No`, `Unknown`만 허용합니다. 데이터가 없거나 확인되지 않은 문자열·숫자는 `Unknown`으로 기록합니다. 배열형 필드는 근거가 없으면 빈 목록을 사용합니다.

조사 상태와 검증 상태는 registry가 관리합니다. 독립 검증 전에는 verification status를 `complete`로 설정하지 않습니다.

`acquisition`은 UOS v2 측정 설계 비교를 위한 필수 조사 블록입니다. `sensor_mounting`, `record_duration_seconds`, `samples_per_record`는 관측값을 저장하고, `position_selection_rationale`과 `position_validation_methods`는 논문이 위치 선택의 타당성을 어떻게 설명·검증했는지를 저장합니다. 위치가 명시되어도 선정 근거가 없으면 rationale은 `Unknown`입니다.
