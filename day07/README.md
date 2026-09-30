# Day 7 — 포워드 프록시, 화이트리스트, HTTP_PROXY/NO_PROXY 함정

- 가이드: [해당 Day 원문](../docs/guide/src/08-day07.md)
- 학습 기록: [SESSION.md](SESSION.md)
- 전체 진행: [PROGRESS.md](../PROGRESS.md)

## 진행 상태 (2026-09-30)
- **종료: 7-1~7-5 학습·자원 정리 완료.** 사용자 출력으로 Day 7 컨테이너 4개·네트워크 2개 제거 및 프로젝트 잔존 목록 부재를 확인했다. [종료 정리 증거](evidence/cleanup-user-2026-09-30.txt).
- 7-1: 네 서비스 기동·agent healthy·healthz, 네트워크 소속과 프록시 환경변수 전달을 확인했다. [구성 증거](evidence/71-config-user-2026-09-30.txt).
- 7-2: 허용 HTTP/HTTPS 200, 비허용 HTTP 403·HTTPS 터널 403, 내부 API 200 및 Squid 로그를 비교했다. [응답·로그 증거](evidence/72-requests-and-log-user-2026-09-30.txt).
- 7-3: 프록시 미설정, NO_PROXY 누락, curl 대소문자 차이의 실패·복구를 비교했다. 일반 ARG 값의 히스토리 노출과 예약 HTTP_PROXY 부재를 확인하고 임시 이미지·폴더를 제거했다. 실제 빌드 프록시 통신 장애를 재현한 것은 아니다. [빌드 증거](evidence/73-build-history-user-2026-09-30.txt), [정리 증거](evidence/73-cleanup-user-2026-09-30.txt).
- 7-4: mitmweb으로 HTTP 요청·응답·Timing(응답 완료 223ms)을 관찰했다. 이후 mitm 제거·8082 리스너 부재를 확인했다. HTTPS/CA 시험은 수행하지 않았다. [관찰 증거](evidence/74-http-observation-user-2026-09-30.txt), [mitm 정리 증거](evidence/74-cleanup-user-2026-09-30.txt).
- 7-5: 게이트웨이 설계·고객사 확인 항목 설명과 질의응답을 진행했다. agent의 목적지를 단일화해도 gateway 이후 외부 API 허용 목록은 별도로 관리한다. 실제 gateway 구축은 하지 않았다.
- 체크포인트 6문항 해설과 실습 복습을 제공했다. 사용자 독립 답변 평가는 미실시다. buildx의 desktop-linux 조회 오류는 원인 미확정으로 남긴다. 다음은 사용자 요청 후 Day 8이며 아직 시작하지 않았다.

## 진행 방식
이 Day의 Codex 작업에서 사용자와 합의한 절만 한 단계씩 진행한다.
실행 기록·오류 해결·다음 시작 지점은 SESSION.md에 남긴다.
실습은 Ubuntu WSL2에서 실행하며 Windows 프로젝트 폴더와의 파일 동기화 여부를 먼저 확인한다.

## 실습 파일
- [compose.yaml](compose.yaml)
- [squid.conf](squid.conf)

## 증거 자료
필요한 출력과 화면 캡처를 `evidence/`에 보관하고 SESSION.md에서 링크한다.
실제 비밀 값은 제거한다. 증거가 생길 때 폴더를 만든다.
