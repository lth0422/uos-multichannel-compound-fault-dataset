# 2026-08-01 UOS v2 클리핑 재검토

## 먼저 볼 파일

- [`clipping_assessment_ko.md`](clipping_assessment_ko.md): 분석 결과와 객관적 판단
- [`results/clipping_scan_file.csv`](results/clipping_scan_file.csv): 파일별 요약
- [`results/clipping_scan_channel.csv`](results/clipping_scan_channel.csv): 채널별 레일·범위·메타데이터 결과
- [`results/rail_values.csv`](results/rail_values.csv): 채널별 디지털 레일과 전압 환산
- [`results/expected_bearing_frequencies.csv`](results/expected_bearing_frequencies.csv): 세 베어링의 RPM별 BPFO·BPFI·BSF·FTF
- [`results/lpf_sweep.csv`](results/lpf_sweep.csv): 대표 8개 조건의 3–11 kHz 저역통과 스윕
- [`results/envelope_check.csv`](results/envelope_check.csv): 6204·N204·30204의 대역별 결함주파수 포락선 결과
- [`results/duplicate_candidates.csv`](results/duplicate_candidates.csv): 전수 집계에서 제외한 중복 경로

원시 파일을 수정하지 않고 다음 명령으로 재생성한다.

```bash
python -m pip install -e '.[analysis,test]'
python scripts/analyze_uos_v2_clipping.py \
  --data-root 'uosv2/수집 데이터' \
  --output-dir validation/clipping_2026-08-01/results
pytest
```

`results/masks/*.npz`는 레일에 도달한 sample index의 로컬 파생물이며 전역
`*.npz` 정책에 따라 Git에서 제외된다. 데이터 공개 단계에서는 원자료와 함께
다시 생성하거나 별도 허용 규칙을 검토한다.

분석 입력 문서는 로컬 `library/documents/design/clipping/`에 정리했으며 Git에
포함하지 않는다.
