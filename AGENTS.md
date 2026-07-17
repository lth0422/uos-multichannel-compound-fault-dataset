# Agent Rules

1. 작업 전에 `PROJECT_CONTEXT.md`를 읽는다.
2. 한 작업에서는 하나의 데이터셋만 조사한다.
3. 기술적 사실은 원 논문 또는 공식 문서에 근거해야 한다.
4. 모든 사실에는 source ID와 page/table/figure/section을 기록한다.
5. 확인되지 않은 정보는 `Unknown`으로 기록한다.
6. multi-sensor, multi-modal, multi-channel, multi-position, multi-direction, triaxial을 구분한다.
7. 복합 결함은 동일 sample에서 둘 이상의 결함이 동시에 존재할 때만 인정한다.
8. internal bearing compound fault와 bearing–rotor compound fault를 구분한다.
9. 외부 raw dataset과 저작권이 있는 publisher PDF는 commit하지 않는다.
10. 로컬 PDF를 읽더라도 파일 자체는 Git에 포함하지 않는다.
11. 기존 데이터셋보다 UOS v2가 우수하다고 미리 결론 내리지 않는다.
12. `facts.yaml`과 `evidence.md`가 서로 불일치하면 작업 완료로 처리하지 않는다.
13. 다른 데이터셋 디렉터리의 파일을 임의로 수정하지 않는다.
14. 코드 변경에는 test를 추가한다.
15. 작업 종료 시 `CURRENT_STATUS.md`를 필요한 범위에서 갱신한다.
