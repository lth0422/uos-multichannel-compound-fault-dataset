# Contributing

작업 전 `PROJECT_CONTEXT.md`, `AGENTS.md`, `survey/taxonomy.md`를 읽으십시오. 데이터셋 하나를 한 작업 단위로 다루고, source metadata → evidence → facts → card/relevance 순으로 기록합니다. Primary source가 없으면 사실을 확정하지 않습니다.

제출 전 다음을 실행하십시오.

```bash
python scripts/check_dataset_cards.py
python scripts/build_comparison_table.py
pytest
```

외부 데이터, publisher PDF, 자격 증명, 개인정보는 commit하지 않습니다.
