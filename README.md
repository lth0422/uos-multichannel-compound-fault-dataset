# UOS Multichannel Compound Fault Dataset

서울시립대학교 RTES Lab의 UOS Dataset v2를 설계하기 위해 공개 회전기계·베어링 데이터셋의 근거를 체계적으로 조사하는 private research repository입니다.

현재 단계는 장비 제어나 데이터 수집이 아닌 **literature/dataset survey**입니다. 잠정 아이디어는 선행 근거를 검증하기 전까지 contribution으로 확정하지 않습니다.

## Workflow

Survey → Evidence verification → Gap analysis → Dataset design → Pilot acquisition → Full acquisition → Validation → Dataset paper

## Repository policy

- 외부 raw dataset과 저작권이 있는 publisher PDF는 GitHub에 올리지 않습니다.
- 로컬 논문은 `library/papers/`, 기관 문서는 `library/documents/`에 두며 두 경로는 Git에서 제외됩니다.
- 데이터셋별 사실은 `facts.yaml`, 근거 추적은 `evidence.md`, 출처 메타데이터는 `sources.yaml`에 분리합니다.
- 확인되지 않은 값은 `Unknown`, 미작성 서술은 `TBD`, 목록은 빈 목록으로 유지합니다.

## Key directories

- `survey/datasets/`: 데이터셋별 조사 카드와 근거
- `survey/templates/`: 새 조사에 사용할 표준 템플릿
- `survey/synthesis/`: 비교표, claim bank, gap analysis
- `survey/schema/`: 구조 및 허용값 설명
- `library/`: commit하지 않는 로컬 문헌 배치 안내
- `references/`: BibTeX 및 DOI 인덱스
- `scripts/`, `tests/`: 검증 및 비교표 생성 자동화
- `paper/`: 근거가 확보된 뒤 작성할 dataset paper 작업 공간
- `design/`: 구매 장비 제약과 survey 근거를 연결하는 UOS v2 설계 기록

## Commands

Python 3.11 이상에서 다음을 실행합니다.

```bash
python -m pip install -e '.[test]'
python scripts/check_dataset_cards.py
python scripts/build_comparison_table.py
pytest
```

비교표 생성 명령은 `survey/dataset_registry.csv`의 행 순서와 priority를 사용해 `survey/synthesis/comparison_master.csv` 및 `.md`를 갱신합니다.
