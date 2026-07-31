# 2026-08-01 UOS v2 클리핑 재검토

## 먼저 볼 파일

- [`clipping_assessment_ko.md`](clipping_assessment_ko.md): 분석 결과와 객관적 판단
- [`current_data_decision_ko.md`](current_data_decision_ko.md): 현재 데이터만으로 가능한 추가 분석과 수집 진행 판단
- [`figures/clipping_risk_dashboard.png`](figures/clipping_risk_dashboard.png): 결함 레이블별 clipping과 채널 간 동시 반응
- [`figures/physical_signal_dashboard.png`](figures/physical_signal_dashboard.png): 대역 에너지·포락선 검출·1× 후보 요약
- [`results/clipping_scan_file.csv`](results/clipping_scan_file.csv): 파일별 요약
- [`results/clipping_scan_channel.csv`](results/clipping_scan_channel.csv): 채널별 레일·범위·메타데이터 결과
- [`results/rail_values.csv`](results/rail_values.csv): 채널별 디지털 레일과 전압 환산
- [`results/expected_bearing_frequencies.csv`](results/expected_bearing_frequencies.csv): 세 베어링의 RPM별 BPFO·BPFI·BSF·FTF
- [`results/lpf_sweep.csv`](results/lpf_sweep.csv): 대표 8개 조건의 3–11 kHz 저역통과 스윕
- [`results/envelope_check.csv`](results/envelope_check.csv): 6204·N204·30204의 대역별 결함주파수 포락선 결과
- [`results/duplicate_candidates.csv`](results/duplicate_candidates.csv): 전수 집계에서 제외한 중복 경로
- [`results/one_x_candidates.csv`](results/one_x_candidates.csv): 명목 RPM 주변의 채널별 1× 후보와 파일 합의값
- [`results/rail_event_cross_channel.csv`](results/rail_event_cross_channel.csv): rail 사건 시각의 다른 채널 반응
- [`results/rail_event_periodicity.csv`](results/rail_event_periodicity.csv): rail 사건과 회전·결함주기의 위상 집중도
- [`results/band_metrics_10s.csv`](results/band_metrics_10s.csv): 전 파일 첫 10초의 대역별 RMS·에너지 비율
- [`results/envelope_validation_10s.csv`](results/envelope_validation_10s.csv): 전 파일 첫 10초의 계산 결함주파수 포락선 검증
- [`results/clipping_label_association.csv`](results/clipping_label_association.csv): clipping과 bearing/RPM/rotor/fault 레이블의 연관성

원시 파일을 수정하지 않고 다음 명령으로 재생성한다.

```bash
python -m pip install -e '.[analysis,test]'
python scripts/analyze_uos_v2_clipping.py \
  --data-root 'uosv2/수집 데이터' \
  --output-dir validation/clipping_2026-08-01/results
python -m scripts.analyze_uos_v2_clipping_extended \
  --data-root 'uosv2/수집 데이터' \
  --output-dir validation/clipping_2026-08-01/results \
  --scan-csv validation/clipping_2026-08-01/results/clipping_scan_file.csv
python -m scripts.plot_uos_v2_clipping_extended \
  --results validation/clipping_2026-08-01/results \
  --figures validation/clipping_2026-08-01/figures
pytest
```

`results/masks/*.npz`는 레일에 도달한 sample index의 로컬 파생물이며 전역
`*.npz` 정책에 따라 Git에서 제외된다. 데이터 공개 단계에서는 원자료와 함께
다시 생성하거나 별도 허용 규칙을 검토한다.

분석 입력 문서는 로컬 `library/documents/design/clipping/`에 정리했으며 Git에
포함하지 않는다.
