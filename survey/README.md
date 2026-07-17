# Dataset Survey

각 하위 디렉터리는 데이터셋 하나의 사실, 근거, 출처, UOS v2 관련성을 분리해 관리합니다. 템플릿을 복사한 직후 값은 `Unknown`, `TBD`, 빈 목록이어야 하며 근거 확인 후에만 변경합니다.

검증은 `python scripts/check_dataset_cards.py`, 통합표 생성은 `python scripts/build_comparison_table.py`로 수행합니다.

로컬에 준비된 문헌과 데이터셋별 검토 순서는 [source_intake_queue.md](source_intake_queue.md)에서 관리합니다. `Ready`는 자료가 배치됐다는 뜻이며 사실 검증 완료를 의미하지 않습니다.
