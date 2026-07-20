# UOS Dataset v2 Design Workspace

Survey에서 확인된 연구 공백과 실제 보유 장비 제약을 연결하는 작업 공간입니다. 구매 장비는 confirmed inventory로 기록하되, sampling rate, 센서 위치, RPM, record 길이, 최종 채널 구성은 survey와 pilot validation 전까지 확정하지 않습니다.

- `hardware_inventory.md`: 구매 장비, 공식 사양, 호환성 및 설계 제약
- `legacy_document_review.md`: 구매 전 조사 문서의 유효 범위와 현재 장비 기준 정정 사항
- `sensor_layout_candidate.md`: shaft-end/motor-end 상단·측면 4채널 후보와 타당성 평가 기준
- `sampling_and_record_length_rationale.md`: survey·hardware·물리 기준을 결합한 rate/duration 후보
- `sampling_and_record_length_rationale_ko.md`: Notion/교수 검토용 한국어 sampling rate/RPM/duration 통합 결정 근거 초안
- `rpm_selection_rationale_ko.md`: Notion/교수 검토용 한국어 RPM grid 정량 분석 및 후보안
- `record_length_and_windowing_rationale_ko.md`: Notion/교수 검토용 한국어 데이터 길이, windowing, split leakage 분석
- `uos_v2_candidate_contributions_ko.md`: 기존 dataset 선례와 내부 literature lead를 분리한 UOS v2 후보 차별성·연구 공백·claim gate 검토
- `pilot_validation_protocol.md`: 위치, mounting, timing, sampling, duration을 확정하기 위한 pilot 절차

Local design references that should not be committed, such as bandwidth notes and PDFs, are kept under `library/documents/design/`. The unverified novelty working note, comparison workbook, and literature leads are in `library/documents/design/novelty/`.
