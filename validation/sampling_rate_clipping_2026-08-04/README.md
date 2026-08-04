# N204 sampling rate–clipping 비교

## 먼저 볼 파일

- [`sampling_rate_clipping_report_ko.md`](sampling_rate_clipping_report_ko.md): 핵심 결과와 실행 판단
- [`figures/sampling_rate_verification.png`](figures/sampling_rate_verification.png): 실제 sampling rate와 대역폭
- [`figures/clipping_by_sampling_rate.png`](figures/clipping_by_sampling_rate.png): 로터 조건별 ADC rail 비교
- [`figures/amplitude_distribution_by_sampling_rate.png`](figures/amplitude_distribution_by_sampling_rate.png): 원신호와 공통 대역의 진폭 분포
- [`results/sampling_rate_summary.csv`](results/sampling_rate_summary.csv): rate별 핵심 요약
- [`results/sampling_rate_file_metrics.csv`](results/sampling_rate_file_metrics.csv): 파일별 결과
- [`results/sampling_rate_channel_metrics.csv`](results/sampling_rate_channel_metrics.csv): 채널별 전체 결과

## 분석 범위

- 베어링: N204 원통 롤러 베어링임
- 회전수: 1600 RPM임
- 베어링 결함: IR+OR+B 3중 결함임
- 로터 조건: H·L·M3·U3임
- rate당 파일 4개·채널 기록 16개임
- 각 rate의 공회전 60초 제외 후 정확히 3,072,000표본 사용함
- 12.8 kHz는 60~300초, 17.0667 kHz는 60~240초, 25.6 kHz는 60~180초임
- 같은 폴더의 6204·12.8 kHz 파일은 이번 비교에서 제외함
- 원시 TDMS 수정 없음

## 재현 명령

```bash
python -m scripts.analyze_uos_v2_sampling_rate_clipping \
  --data-root 'uosv2/수집 데이터' \
  --output-dir validation/sampling_rate_clipping_2026-08-04/results
MPLCONFIGDIR=/tmp/matplotlib \
python -m scripts.plot_uos_v2_sampling_rate_clipping \
  --results-dir validation/sampling_rate_clipping_2026-08-04/results \
  --figures-dir validation/sampling_rate_clipping_2026-08-04/figures
pytest
```
