# Current Status

## Current phase

UOS v2 full-acquisition preparation and automated validation, with published-dataset survey retained as design evidence

## Completed

- 2026-09-09: N204 B와 30204 IR+OR+B를 `validation/acquisition/<bearing>/<fault>/` 구조로 정리하고 각 48파일 CH0의 2~7 kHz 포락선 FFT 개별 그림과 전체 축소본을 생성함. 최종 판정은 수집 완전성·RMS·1X 중심으로 조정하고 결함주파수는 보조 검증으로 구분함
- 2026-09-09 N204·B와 30204·IR+OR+B 본 수집 보고서에 요청 검증 항목별 최종 결론표를 추가함. N204는 ±50 g 초과 3표본·DAQ rail 1표본, 30204는 ±50 g 초과 827표본·DAQ rail 493표본으로 범위 초과와 rail을 분리함. 두 묶음 모두 1,600 RPM RMS가 32/32조합에서 600 RPM보다 높고 파일 단위 1X가 확인됨. N204 BSF는 부분 확인, 30204는 IR·OR 부분 확인과 B 검증 부족으로 정리함
- 2026-09-08 30204·IR+OR+B 본 수집의 48개 고유 조건을 검증함. 모든 파일에서 앞 60초를 제외한 60~180초를 사용해 채널당 3,072,000표본을 통일함. ±50 g 초과는 827표본, rail은 493/589,824,000표본이며 CH0·CH1에 분포함. 48/48파일에서 최소 3개 채널의 1X가 확인됐고 1,600 RPM RMS가 32/32조합에서 600 RPM보다 높아 `통과(보완사항 있음)`로 기록함. IR·OR·B 검출률은 보조 검증으로 관리함
- 2026-09-02 본 수집 검증 구조를 `validation/acquisition/`으로 통합했다. `protocol.md`에 원자료·결과 위치, 수집 묶음, 검증 항목과 판정 상태를 규정하고 `index.md`에 수집 묶음별 결과를 누적하도록 했다. 결함 레이블은 `{로터결함}_{베어링결함}` 순서로 고정했으며 코드의 모든 CSV와 manifest에 `condition_label`을 추가했다.
- 2026-09-02 본 수집 TDMS를 지정해 4채널 sample 수·NI-9234 rail 비율·RMS·1X·BPFI/BPFO/BSF를 일괄 검사하는 `scripts/validate_uos_v2_acquisition.py`를 추가했다. 파일 반복번호, 명시적 분석 구간, 25.6 kHz 실제 rate, 복합 결함의 IR·OR·B 구성 성분을 처리하며 상세 CSV·요약 CSV·PNG·한국어 보고서를 생성한다.
- 2026-09-02 6204·로터 정상 H·IR+OR+B·1000/1200/1400/1600 RPM 4파일을 표본 실행했다. 공회전 60초 제외 후 120초·총 49,152,000표본에서 rail 13개(0.000026449%)를 확인했고, 1X는 16/16채널에서 검출됐으며 네 채널 모두 RPM 증가에 따라 RMS가 계속 증가했다. 보수적인 동일 대역 2개 이상 고조파 기준에서 IR·OR·B 기대 성분은 29/48채널·성분이 자동 선별됐으며 이는 최종 합격 판정이 아니다.
- 2026-09-02 N204·1600 RPM·로터 정상 H의 정상·단일·이중·삼중 내부 결함과 IR+OR 반복을 포함한 11파일을 추가 표본 실행했다. 1X는 44/44채널에서 확인됐으나 기대 결함 성분은 고정 10 dB·2개 고조파 기준에서 6/72채널·성분만 통과했고 정상 파일에서도 IR 후보가 2/4채널 나타났다. 결함주파수 자동 선별 기준은 정상 대조군·반복 자료로 조정하기 전까지 데이터 합격 기준으로 사용하지 않는다.
- 2026-09-02 `dataset/uosv2/수집 데이터/`의 sampling-rate별 하위 폴더를 제외하고 RPM 폴더 바로 아래 TDMS 160개를 점검했다. 모두 4채널·실제 25,600 Hz였으며 반복 수집 6개를 합친 고유 조건 154개를 30204·6204·N204 체크리스트 CSV에 `TRUE`로 반영했다. 베어링별 완료 조건은 30204 108개, 6204 16개, N204 30개다.
- 2026-08-16 Update Article 사례 검토 문서를 원문 근거 수준에 맞춰 수정했다. 장비·대상·rate가 변경된 출판 사례를 UOS 변경의 기술적 근거가 아닌 형식상 선례로 구분하고, 각 사례의 변경 설명·변경 전후 직접 비교 검증 여부·원본과 비교한 논문 내 위치와 방식을 표로 정리했다. 검토 사례 대부분은 새 목적·사양·수집법을 설명했으나 장비 동등성을 통제 실험으로 입증하지 않았고, sampling rate 감소를 정당화한 직접 사례는 없음을 명시했다.
- 2026-08-16 Data in Brief 원본–Update Article 6쌍·12개 자료를 대조했다. 단순 증량뿐 아니라 장비·대상·측정 범위·파일 schema·품질관리 변경 후 Update Article로 출판된 사례를 확인했다. UOS v2는 v1의 계보와 겹치는 조건을 유지하고 변경 manifest를 제공하는 후속 Update Article 후보로 정리했으며, 별도 한글 검토 문서와 6쌍 비교 CSV를 생성했다.
- 2026-08-16 검토한 6쌍에는 sampling rate 감소를 직접 정당화한 사례가 없음을 확인했다. UOS v2의 rate 변경은 Update Article 선례가 아니라 alias-free 대역, 결함주파수·포락선 검출, clipping, 독립 반복과 protocol-label confounding 검증으로 별도 입증해야 한다고 정리했다.
- 2026-08-15 N204·1,600 RPM·10.24 kHz의 이중·삼중 내부 결함 32파일·128채널을 검사했다. RPM 설정시간과 공회전 60초를 제외한 300초에서 채널당 3,072,000표본을 확보했으며, 총 393,216,000표본에서 rail과 50 g 초과 표본은 모두 0개였다. 별도 clipping 보고서를 생성했으며 포락선 검출과 최종 rate 선정은 수행하지 않았다.
- 2026-08-14 N204·1,600 RPM·IR+OR의 M1 재측정·M2·M3 장시간 파일을 검사했다. 실제 25,600 Hz·4채널이며 사용자 규칙으로 계산한 정식 120초 구간에서 채널당 3,072,000표본을 동일하게 사용했다.
- 2026-08-14 공회전 제외 310초 전체에서 신규 M1·M2·M3은 기존 M1과 같은 RMS 급락이나 회전 신호 소실이 없어 축 분리 현상이 재현되지 않았다. M2·M3은 마지막 30초 RMS가 초반 대비 약 ±5% 이내였고 M1 재측정은 CH0·CH1이 15.7%·23.6% 증가했다.
- 2026-08-14 신규 M1·M2·M3의 정식 120초 rail 합계는 1,860·1,535·767표본이며 모두 CH0·CH1에 나타났다. 전체 IR+OR 보고서·CSV·그림을 14파일·56채널로 갱신했다.
- 2026-08-14 N204·1,600 RPM·L·IR+OR 2·3차를 추가 검사했다. 실제 25,600 Hz·4채널·180초 이상이며 60~180초의 채널당 3,072,000표본을 사용했다. rail 합계는 L 2차 1,847표본, L 3차 1,730표본으로 모두 CH0·CH1에 나타났다.
- 2026-08-14 L 1차 CH2·CH3 감소는 L 2·3차에서 같은 형태로 재현되지 않았다. L 2차는 CH0·CH1 감소, L 3차는 CH2 증가가 나타나 세 파일 모두 안정적인 L 대표 수집 확정을 보류했다.
- 2026-08-14 전체 IR+OR 11파일·44채널의 10초 RMS를 각 수집 60~120초 RMS로 정규화해 비교했다. M1은 네 채널이 모두 감소하고 CH0·CH2·CH3의 감소가 후반으로 이어져 다른 조건보다 일관된 상태 변화가 확인됐다. 통합 보고서·CSV와 전체 비교 그림을 갱신했다.
- 2026-08-14 N204·1,600 RPM·IR+OR의 U1·U2·U3·L을 추가 검사했다. 네 파일 모두 실제 25,600 Hz·4채널·180초 이상이며 원파일 60~180초의 채널당 3,072,000표본을 사용했다. rail 합계는 각각 2,983·2,644·2,726·2,419표본이고 모두 CH0·CH1에 집중됐다.
- 2026-08-14 U1·U2·U3은 후반/초반 RMS 변화가 약 ±3% 이내였으나 L은 CH2·CH3이 각각 22.5%·11.2% 감소하고 CH0·CH1 기준선 변화도 커 재측정을 권고했다. 기존 IR+OR 보고서·CSV·그림을 9파일·36채널 결과로 갱신했다.
- 2026-08-14 N204·1,600 RPM·H·IR+OR 4차 파일을 추가 검사했다. 실제 25,600 Hz·4채널·191.9초이며 원파일 60~180초의 채널당 3,072,000표본을 사용했다. rail은 CH0 1,605·CH1 997표본으로 합계 2,602표본이었고 CH2·CH3은 0표본이었다.
- 2026-08-14 H 4차 결과를 기존 반복 보고서·CSV·그림에 통합했다. H 1~4차 rail은 각각 4,302·3,249·2,099·2,602표본으로 모두 CH0·CH1에 재현되어 네 파일의 clean 본 수집 승인을 계속 보류했다.
- 2026-08-13 N204·1,600 RPM·IR+OR의 H 2차, M1, 축 재체결 후 H 3차를 추가 검사했다. 모든 파일은 실제 25,600 Hz·4채널·180초 이상이며 원파일 60~180초의 채널당 3,072,000표본을 동일하게 사용했다.
- 2026-08-13 H 1·2·3차의 rail은 각각 4,302·3,249·2,099표본으로 모두 CH0·CH1에서 재현됐다. 재체결 후 H 3차의 RMS는 H 2차보다 채널별 6.9~13.5% 낮았으나 clipping은 남아 세 반복 모두 clean 본 수집 자료 승인을 보류했다.
- 2026-08-13 M1은 약 140초 이후 네 채널 RMS가 감소하고 원파일 190초 이후 거의 0으로 급감했다. 축 결합 이탈 또는 운전 중단과 정합되는 이상 구간으로 판단하여 현재 M1 파일을 대표 수집에서 제외하고 재측정하도록 보고서·CSV·그림을 생성했다.
- 2026-08-12 N204·1,600 RPM·로터 정상 H·25.6 kHz에서 추가 수집한 정상·IR·OR·B·IR+OR·IR+B·OR+B 7파일을 검사했다. 모든 파일은 4채널·실제 25,600 Hz·180초 이상·finite 값으로 확인됐으며 원파일 60~180초의 채널당 3,072,000표본을 동일하게 사용했다.
- 2026-08-12 신규 N204 결함 행렬에서 정상·IR·OR·B는 rail 0표본, IR+OR는 4,302표본, IR+B는 93표본, OR+B는 21표본이었다. IR+OR의 rail은 CH0 2,350·CH1 1,952표본이고 12개 10초 구간 모두에 지속되어 clean 본 수집 자료 승인을 보류하고 독립 재측정을 우선하도록 별도 보고서·CSV·그림을 생성했다.
- 2026-08-11 PRONOSTIA 보고서에 rail 발생 파일 비율 119/24,889=0.478123%와 파일별 rail 표본 비율 범위 0.019531~0.546875%를 명시했다. 119개 발생 파일 합산 비율 0.1354% 및 전체 자료 기준 0.0006474%와 분모를 구분했다.
- 2026-08-07 PRONOSTIA의 rail 발생 119개 파일을 수명 진행률과 대응시켰다. 0.1초 파일별 5,120개 진동값을 분모로 rail 비율을 계산하고, Bearing1_1·1_3·1_4·2_3의 최초 발생 시점과 파일별 비율을 비교하는 그림을 추가했다. rail은 수명 진행률 88.0% 이후에만 확인됐으나 파일별 비율이 단조 증가하지는 않았다.
- 2026-08-07 clipping 발생 파일 내부의 rail 표본 비율을 별도로 계산했다. HUST Vietnam 정상상태 `data`는 13,720,683표본 중 8,919표본으로 0.06500%였고, rail 발생 29개 파일의 개별 비율은 0.000195~0.383398%였다. PRONOSTIA는 119개 파일의 2채널 609,280표본 중 825표본으로 0.1354%였다. 각각의 전체 자료 기준 비율 0.01824%와 0.0006474%를 함께 제시하여 분모 차이를 명확히 했다.
- 2026-08-06 세 데이터셋 통합 다운로드·장비 조사 문서를 S1·HUST Vietnam·PRONOSTIA 원자료 clipping 보고서에 대조 반영했다. 공식 다운로드 경로, 센서·DAQ 확인 수준, Nyquist와 센서 대역의 구분, 장비 일반 사양과 실제 실험 설정의 경계를 추가했다. PRONOSTIA의 NI 모듈명과 HUST의 352C33 가설은 공식 원문 확인 전까지 조건부로 유지했다.
- 2026-08-06 PRONOSTIA 중첩 ZIP을 해제하여 Training 6개와 Validation full 11개, 총 17개 전체수명 궤적의 진동 CSV 24,889개·저장 진폭 127,431,680개를 검사했다. 가로 `-48.148/+48.128`, 세로 `-47.843/+47.849`의 채널별 저장 rail을 4개 베어링·119개 파일·825표본에서 확인했다.
- 2026-08-06 PRONOSTIA rail은 Bearing1_4의 수명 진행률 약 88.0%, 나머지 3개는 약 98.1~99.6% 이후에 처음 나타났다. Test는 Validation의 절단된 앞부분이며, Test 내부의 Training/Validation ZIP도 최상위 파일과 SHA-256이 같은 복사본임을 확인하여 중복 집계에서 제외했다. 0.1초·2채널 스냅샷, 10초 간격, delimiter 차이와 Bearing1_1 시간값 이상도 문서화했다.
- 2026-08-06 HUST Vietnam 원자료 99개 MAT의 `data`·`ru`·`ru_raw` 197개 진동 배열을 전수 검사했다. 정상상태 `data` 29/99파일에서 저장 rail 8,919표본을 확인했으며, 2표본 이상 연속 rail 구간은 2,705개였다. 상·하한 전환을 포함한 최장 rail 상태는 6표본(117.2 μs), 동일 bound의 최장 평탄 구간은 3표본(58.6 μs)이었다.
- 2026-08-06 HUST Vietnam의 clipping은 IB에 집중됐다. IB는 9/12파일·7,492표본이 rail에 도달한 반면 N·O·IO는 0표본이어서 label shortcut 위험을 기록했다. 실제 정상상태 속도 1,351.8~1,497.6 RPM, 18개 비표준 길이 `data`, 불일치하는 run-up 필드 구조도 문서화했다.
- 2026-08-06 S1 Data 원자료의 MATLAB v5 파일 4개·20개 채널 기록·5,160,000개 값을 점검했다. 저장 최솟값·최댓값 반복과 peak 99% 이상 평탄 구간이 없어 명확한 digital rail은 관찰되지 않았다. 센서·DAQ 범위가 원 논문에 없어 아날로그 포화 여부는 미확정이다.
- 2026-08-06 S1 파일명 충돌을 검토했다. `BR+OR.mat`는 OR+B로 추정했으며, `OR+BR.mat`는 논문의 네 결함 조합과 대조할 때 IR+B 오기 가능성이 있으나 결함주파수 결과가 이를 확정하지 못했다. OR+B 중복·IR+B 누락 가능성을 포함해 Needs review로 유지하고, 논문의 20×12,000표본 설명과 실제 252,000·264,000행의 불일치도 기록했다.
- 2026-08-05 N204·1600 RPM·IR+OR+B의 10.24 kHz H·L·M3·U3 파일을 추가 검증했다. 실제 rate는 모두 10,240 Hz였으며, 공회전 60초를 제외한 60~360초의 300초·3,072,000표본/채널을 사용했다. 4개 파일·16개 채널에서 rail과 50 g 초과 표본은 없었다.
- 2026-08-05 10.24·12.8·17.0667·25.6 kHz를 동일한 3,072,000표본/채널로 재비교했다. rail 표본은 각각 0·5·25·1,252개였으며, 0~4.4 kHz 공통 대역 및 4.4 kHz 위 저장 에너지를 함께 제시한 별도 보고서를 생성했다. 10.24 kHz의 최종 채택 여부는 고주파 결함 정보와 동일 조건 반복시험 전까지 미확정이다.
- 2026-08-05 30204·6204·N204의 IR+OR+B 3중 내부 결함을 25.6 kHz·1000~1600 RPM에서 비교했다. 30204와 N204는 1000 RPM에서도 rail이 발생했고, 6204는 1000·1200 RPM에서 rail이 없으며 1400 RPM부터 발생했다. 세 베어링 공통 rail 미발생 하한은 확인되지 않아 30204·N204의 800 RPM 이하 추가 측정이 필요하다.
- 2026-08-04 N204·1600 RPM·IR+OR+B의 H·L·M3·U3에서 12.8·17.0667·25.6 kHz 비교를 수행했다. 공회전 60초 제외 후 rate별 3,072,000표본을 사용했으며 TDMS 실제 rate와 metadata가 설정값에 일치함을 확인했다.
- 2026-08-04 rail 표본은 12.8 kHz 5개, 17.0667 kHz 25개, 25.6 kHz 1,252개로 증가했으나 세 rate 모두 4/4파일에 rail이 존재했다. rate 증가가 저장된 clipping 빈도에 영향을 주지만 낮은 rate만으로 clipping이 제거되지 않는다고 판단했다.
- 2026-08-04 sampling-rate 비교의 집계 단위를 rate·채널·로터 조건으로 재구성했다. clipping은 CH0·CH1에 집중됐고 CH2·CH3에서는 세 rate 모두 rail이 없었다. 0~5.5 kHz 공통 대역은 CH0·CH2·CH3에서 비교적 일관됐으나 CH1의 수집 간 변동이 남아 전체가 동일하다는 결론은 보류했다.
- 2026-08-03 다중 필터 대역 분석을 최대충격 주변 10초 중심에서 공회전 제외 120초 전체 g값 분포 중심으로 개편했다. 채널·필터·대역별 RMS, p90~p99.99, crest factor, 10~50 g 초과율과 전체/베어링/RPM별 histogram을 생성했다.
- 2026-08-03 Butterworth 120초 분포에서 2~7 kHz는 7채널·22표본, 7~10 kHz는 1채널·1표본이 50 g를 넘었으며, 전체 표본 대비 각각 약 0.0000156%와 0.0000007%임을 확인했다. 필터 출력 peak는 실제 clipping 이전 센서 입력의 복원값이 아님을 유지했다.
- 2026-08-03 사용자 확인에 따라 일반 파일의 60~180초와 30204·7분 초과 파일의 300~420초만 유효 측정구간으로 정하고, 공회전과 뒤 잔여 구간을 제외해 모든 클리핑·대역·포락선 분석을 재생성했다.
- 2026-08-03 공회전 제외 후 ADC rail은 2,675표본·45/116파일이며, 건강·단일 결함 0/56파일과 복합 결함 45/60파일에서 나타남을 확인했다.
- 2026-08-03 30204·6204·N204의 1400·1600 RPM·IR+OR+B 조건 중 ±50 g 초과 46채널에 Butterworth·Chebyshev I·II·Elliptic·Bessel과 5개 주파수 구간을 적용했다.
- 2026-08-03 최대충격 주변 10초 분석에서는 2~7 kHz 단일 채널만 필터 3종에서 50 g를 넘었으나, 120초 전체 분포 분석에서 다른 시각의 대역 peak가 추가로 확인됨을 정정했다. IR·OR 계열은 2~7 kHz, B 계열은 7~10 kHz 검출이 상대적으로 높으며 필터 후 최대값은 센서 입력 진폭 판정에 사용할 수 없음을 문서화했다.
- 2026-08-03 46채널의 누적 저역통과 시나리오를 추가했다. 10 kHz 저역통과 후 필터별 1~11채널, 필터 3/5 다수결 기준 11채널이 50 g를 넘었으며, 7 kHz 저역통과 후에는 다수결 기준 N204·1600 RPM·H·IR+OR+B·CH0 한 채널만 남았다.
- 2026-08-03 S1-S01의 식 (1)~(9)과 Fig. 11~14를 기준으로 BPFO/BPFI/BSF 고조파, BPFI±1×, BSF±FTF 계열을 고유 116파일 전체에서 분석했다.
- 2026-08-03 30204·1600 RPM의 단일-복합 결함을 동일 로터·채널끼리 비교하고 주파수 중첩을 표시했으며, Task B 대표 파일 오류와 L1/L2/L3 결과를 원자료 기준으로 정정했다.
- 2026-08-03 ADC 포화 보고서를 베어링·RPM·베어링 결함·로터 조건·채널 수가 드러나도록 전면 개정하고, 베어링 정상(H)과 기계 전체 정상을 구분했다.
- 2026-08-03 BPFO·BPFI·BSF 결과를 조건별로 분리하고, 한국어 그래프와 축·분모·색상·해석 범위 설명을 추가했다.
- 2026-08-01 현재 수집 TDMS 124경로를 검사하고 SHA-256 동일 중복 8쌍을 제외한 고유 116파일의 clipping을 전수 재분석했다.
- 초기 전체 기록 검사에서 ADC rail 4,709표본을 확인했으나, 공회전·뒤 잔여 구간을 제외한 최종 판정값은 2,675표본임을 정정하고 대표 8조건 LPF sweep을 재생성했다.
- UOS v1 원논문 Table 2의 geometry로 6204·N204/NJ204·30204 결함주파수를 계산하고 세 베어링 envelope check를 생성했다.
- 클리핑 작업지시서의 주장과 한계를 `validation/clipping_2026-08-01/clipping_assessment_ko.md`에 정리했다.

- Survey repository structure and templates bootstrapped
- Validation and comparison-table automation added
- Core ten dataset placeholders registered
- UOS v1 original dataset paper reviewed and first-pass card, facts, evidence, sources, and relevance analysis completed
- Paderborn original benchmark paper reviewed and first-pass card, facts, evidence, sources, and UOS v2 relevance analysis completed
- CWRU official Bearing Data Center documentation reviewed and first-pass card, facts, evidence, sources, and UOS v2 relevance analysis completed
- University of Arkansas 2023 Data in Brief paper reviewed and first-pass card, facts, evidence, sources, and UOS v2 relevance analysis completed
- Arkansas raw archive structure audited: 2,925 headers and 117 complete representative records checked; manifest and compact representative subset preserved
- MAFAULDA 2016 original publication and official web documentation reviewed; first-pass card, facts, evidence, sources, sensor-set comparison, and UOS v2 relevance analysis completed
- XJTU-SY original prognostics paper and supplied official README reviewed; first-pass card, facts, evidence, sources, and UOS v2 sampling/location implications completed
- NASA IMS official README, original paper, and supplied NASA catalog metadata reviewed; first-pass card, facts, evidence, sources, compound endpoint, and UOS v2 temporal-design implications completed
- Ottawa 2023 dedicated dataset paper reviewed; first-pass card, facts, evidence, sources, confound analysis, and UOS v2 sampling/placement implications completed
- Ottawa 2018 dedicated dataset paper reviewed; first-pass card, facts, evidence, sources, variable-speed analysis, and UOS v2 order-tracking implications completed
- PRONOSTIA original platform/challenge paper reviewed; first-pass card, facts, evidence, sources, natural compound analysis, and UOS v2 controlled-label implications completed
- Core-ten comparison synthesized into gap analysis, UOS v2 design implications, and a source-linked claim bank
- Current four-channel shaft-end/motor-end top/side layout recorded as a pilot candidate; legacy pre-purchase DAQ/mounting note audited and relocated
- Sampling-rate/record-length rationale and four-channel pilot validation protocol drafted from hardware constraints and survey evidence
- Purchased NI-9234/cDAQ-9171 and four HS 13A131 accelerometers recorded with preliminary specification and compatibility review
- NI-9234 native sampling-rate grid documented from the 13.1072 MHz timebase rule; 25.6 kS/s remains a primary pilot candidate, while 100 Hz is documented only as a processed derivative requiring explicit anti-alias filtering/resampling
- KAIST Batch dedicated Data in Brief paper reviewed and registered as an additional direct comparator; four simultaneous accelerometers at two bearing housings in x/y directions, 25.6 kHz vibration, and 60–2100-second record precedents documented
- Sensor-layout and sampling/record-length design notes updated: KAIST strongly supports the proposed geometry as a pilot candidate but does not validate UOS mounting surfaces or establish an optimal rate/duration
- HUST Vietnam dedicated Data Note reviewed and registered as a direct comparator; intentional IR+OR, IR+Ball, and OR+Ball defects, five bearing models, NI-9234 at 51.2 kHz, and 10-second steady/5-second run-up records documented
- Before S1 review, the internal-compound candidate gap was narrowed from pairwise combinations to a complete pairwise-plus-triple matrix; S1 subsequently established that the combination set itself already exists, so the current candidate is the broader matched multi-bearing/multi-RPM/timing/validation design recorded below
- SEU transfer-learning application paper reviewed; self-collected DDS subset registered separately from reused CWRU data, IR+OR Combination verified, and pooled bearing/gear `mixture` distinguished from same-sample compound faults
- HUST China benchmark/release paper and official HUSTbearing GitHub README reviewed; 25.6 kHz, 262,144-point/10.2-s records, ER-16K bearing, 9 health states, ten constant-speed conditions plus one 0-40-0 Hz time-varying condition, and IR+OR combination faults documented
- Internal dataset-comparison workbook and novelty working note reviewed and relocated under the ignored local design library; their unverified claims are explicitly separated from source-linked survey facts
- UOS v2 candidate-contribution review drafted: multi-channel/multi-position/compound/variable-RPM alone are not novelty claims; controlled compound matrix, paired channel-ablation protocol, timing metadata, physical validation, and confound-resistant metadata remain candidate gaps pending verification and pilot evidence
- S1 Data original PLOS ONE article reviewed and registered; five vibration axes at three positions, all three pairwise internal compounds plus the triple condition, 12 kHz/12,000-point groups at 2,000 RPM, and compound envelope analysis documented
- MCC5-THU dedicated Data in Brief article reviewed and registered; six vibration axes at two positions, speed/torque channels, 12.8 kHz/60-second variable-condition records, three severities, and broken-tooth+IR/OR bearing–gear compounds documented
- Candidate novelty narrowed after S1/MCC5 review: internal pairwise-plus-triple and broad multi-channel compound data are established precedents; matched references across bearing structures/RPMs with explicit timing, paired channel comparison, and release-wide validation remain candidates
- First UOS v2 acquisition pilot organized and analyzed: 30204 IR, healthy rotor, nominal 1400 RPM; four HS 13A131/NI-9234 channels were sequentially crossed over four shaft-end/motor-end top/side positions
- Pilot raw files relocated under ignored `external_data/uos_v2_pilot/`; reproducible TDMS/MAT analysis, characteristic-frequency calculation, CSV outputs, six figures, tests, evidence table, and Korean validation report added under `pilot/`
- All 16 new-system runs passed exploratory finite/range/shaft/BPFI-envelope screens; same-position RMS CV was 2.06–3.92%, and all channels showed the 23.25 Hz shaft peak and approximately 205.25–205.50 Hz BPFI envelope peak
- CH0 ShaftEndTop raw `H_H` label recorded as a user-confirmed metadata typo; raw data preserved and analysis audit fields retain the conflict
- New-versus-legacy comparison was repeated with identical 0–7 kHz filtering and absolute 1×/BPFI peak amplitudes: bandwidth matching reduces RMS ratios from 1.19–2.12 to 0.97–1.41, while 1× ratios are 1.02–1.24; bandwidth is a major but incomplete explanation and a gross factor-of-two calibration error is not supported
- Per-condition synchronized four-channel master acquisition duration set to 60 seconds; canonical analysis-window length, overlap, stabilization exclusion, and release derivatives remain open
- Exact per-channel peak-frequency CSV and a horizontally offset plot added because overlaid spectra hide coincident channel peaks; all 16 new-system runs show 23.25 Hz shaft peaks and 205.25 or 205.50 Hz BPFI envelope peaks
- 30204·6204·N204의 1000~1600 RPM IR+OR+B 자료 48개 파일·192개 채널 기록을 rail 지속시간 기준으로 재분석함. 단일표본 rail은 2,525개, 2표본 이상 연속 clipping은 18개이며 최장은 3표본(117.2 μs)임. RPM 비교 보고서와 세 종류의 요약 그림을 지속시간 중심으로 개정함

## In progress

- N204 롤러 단일 결함 본 수집은 수집 완전성·저속/고속 RMS 경향·192/192채널 1X를 근거로 `통과(보완사항 있음)`로 정리함. BSF 자동 기준 보정과 희소 rail 1표본의 공개 정책 검토는 후속 보완사항임
- 25.6 kHz를 UOS v2 본 수집의 우선 sampling-rate안으로 정리 중이며, 최종 승인과 clipping 처리 정책은 아직 확정 전임
- 2026-08-01 clipping 결과의 원인 분리를 위한 보유 장비 반복·재부착·센서/DAQ 채널 교차시험 및 rail 구간 전후 baseline 개별 검토
- UOS v1 official repository metadata and independent verification
- Paderborn official KAt-DataCenter metadata, README/fact sheets, and deposited MAT schema verification
- CWRU exact MAT record shape, optional base-channel coverage, timing architecture, release year, and license verification
- Arkansas article/header channel conflict, bearing specification, mounting, and hardware timing architecture verification
- MAFAULDA later dedicated-paper 여부, license, raw schema/version difference, and NI-9234 inter-module timing verification
- XJTU-SY official repository URL/version/license, raw schema, endpoint labels, DAQ, mounting, and channel timing verification
- NASA IMS snapshot-duration/cadence conflicts, DAQ timing, mounting, and third-party data-license applicability verification
- Ottawa 2023 repository license/schema, label typo, accelerometer direction, ADC timing, and full lifecycle-file availability verification
- Ottawa 2018 fault generation, load, mounting, sampling rationale, ADC timing, repository label, and license verification
- PRONOSTIA official challenge README/checksum, bearing geometry, stopping criterion, endpoint damage, stored acceleration unit, hardware range/timing, and license verification
- Remaining core dataset primary-source collection and fact verification
- Candidate UOS v2 contribution verification and follow-up simultaneous four-channel placement/rate/duration pilot
- Delivered 13A131 mounting/calibration documents and actual M5 magnet/adapter compatibility verification
- Delivered sensor documentation 확인 및 four-channel pilot compatibility test 준비
- KAIST Batch official repository schema/license, exact accelerometer attachment, cross-device timing, and NI module-role conflict verification
- HUST Vietnam Mendeley manifest, 99-record accounting, RPM values, MAT schema, mounting, chassis/timing, and dataset license verification
- SEU official repository documentation, raw acquisition schema, sensor/DAQ/mounting, sampling/duration, controller-setting interpretation, persistent access, and license verification
- HUSTbearing raw Excel schema, license, exact sensor/DAQ/mounting/channel details, and Supplementary Appendix B task mappings
- Full-text audit of the multi-channel fusion literature leads, including sensor taxonomy, split protocol, comparison baseline, quantitative result, and limitations
- S1 official supporting ZIP schema, exact sensor axes/models, DAQ, mounting, simultaneous timing, and license verification
- MCC5-THU official repository license/raw schema, 48-versus-112 transitional-condition conflict, DAQ, mounting, and timing verification
- First pilot follow-up: simultaneous four-channel healthy/IR runs over multiple RPMs, repeat/remount runs, tachometer alignment, and severe-condition clipping headroom

## Next actions

1. N204/1600/M3/IR+OR+B와 건강 대조에서 동일 장비로 완전 재부착 3회 반복
2. 센서 개체–DAQ 채널–물리 위치를 교차하여 clipping 원인의 상대 기여 분리
3. stud 부착이 현재 보유 부품으로 가능하면 현재 mounting과 같은 조건에서 비교
4. 자동 zero-shift suspect 채널의 rail 구간 전후 baseline을 개별 검토하고 판정법 확정
5. 위 결과 전까지 신규 대규모 조건 수집과 hardware 변경 결정을 보류
6. 향후 수집에 tachometer/실측 RPM과 sensor serial–DAQ channel–position manifest 저장
7. 실제 포화 이전 절대진폭이 연구에 필수이고 rail이 계속될 때만 저감도 reference를 검토
8. NI-9234/HS 13A131 primary documentation과 calibration certificate 확인
9. N204·1600 RPM·IR+OR+B에서 10.24·12.8·17.0667·25.6 kHz의 수집 순서를 무작위화하여 rate별 3회 이상 반복하고, 4.4 kHz 위 결함 정보의 포락선 검출 기여를 평가

## Open questions

- 조사 완료와 independent verification의 담당자 및 승인 절차
- 비교 실험에 필요한 paired-data 기준과 최소 메타데이터
- UOS v2 후보 센서 위치를 평가할 물리 근거와 pilot validation metric
- sampling rate, RPM 범위, record 길이를 결정할 최소 bandwidth·frequency-resolution·rotation-count 기준
- 13A131 제조사 원본 datasheet, 개별 calibration certificate, 정확한 NI-9234 connector variant
- SEU 등 남은 후보가 unresolved gap을 실제로 좁히는지와 추가 등록 우선순위
- 내부 비교 작업표의 값 중 source-linked survey와 충돌하거나 미검증인 항목의 처리 기준
- S1 Data의 5축 신호가 동시에 저장됐는지와 정확한 축·열 순서, `OR+BR.mat` 파일명 및 21·22초 배열의 공식 의미
- HUST Vietnam 저장 단위, PCB 325C33 감도·범위, CompactDAQ 섀시·입력 설정, `ru`/`ru_raw`의 공식 차이와 clipping 원인
- PRONOSTIA 저장 진폭 단위, 가속도계 감도·범위, cDAQ 입력 모듈·범위와 채널별 약 ±48 rail의 발생 단계
- MCC5-THU의 transitional condition 수가 48인지 112인지와 모든 8개 열의 공통 시간축 여부
- Full acquisition 전에 통과해야 할 channel-gain, mounting-repeatability, target-SNR, clipping-margin 수치 기준
- 60초 기록의 안정화 제외를 고정 30초로 할지, tachometer/RMS 기반 조건부 규칙으로 할지

## Blockers

- 현재 100 mV/g·±50 g 센서와 약 ±5.12 V DAQ rail이 같은 지점에 있어, 이미 clipping된 신호만으로 실제 50 g 초과 진폭과 mounting 기여도를 분리할 수 없음
- rail 유무만으로 현재 전체 116파일의 복합 결함 여부를 87.1%, 균형적인 30204/1600 subset을 92.2% 맞힐 수 있어 raw ML benchmark에는 label shortcut 교란이 존재함
- 첫 파일럿은 순차 단일채널·단일 RPM·단일 IR 조건이므로 동시 4채널 complementarity, RPM trend, healthy 대비, remount repeatability를 아직 검증하지 못함
- 핵심 데이터셋의 1차 상세 검토는 완료됐으나 independent verification과 일부 공식 repository 메타데이터가 남아 있음

## Last updated

2026-09-09
