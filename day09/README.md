# Day 9 — 폐쇄망 이미지 반입: 오프라인 빌드 · save/load · 사내 레지스트리 · 스캔 · SBOM

- 가이드: [해당 Day 원문](../docs/guide/src/10-day09.md)
- 학습 기록: [SESSION.md](SESSION.md)
- 전체 진행: [PROGRESS.md](../PROGRESS.md)

## 진행 방식
최신 상태(2026-10-05): **9-1~9-5·실습 자원 정리 완료.** 사용자 출력으로 registry·UI·day09_default 제거, 압축 전 tar 삭제 명령 성공과 regdata·이미지·반입 파일·보고서·SBOM·캐시 보존을 확인했다. UI는 종료 상태다. 누적 점검·체크포인트 평가는 미진행이며 Day 9 전체 통과로 판정하지 않는다. [정리 증거](evidence/cleanup-user-2026-10-05.txt). 아래는 정리 전 완료 기록이다.

최신 진행(2026-10-05): **9-1~9-5 완료.** 첨부 파일의 정확한 크기·해시와 이미지 식별 정보를 반영한 [학습용 반입 신청서](IMPORT-PACKAGE.md)를 Windows에 작성했다. 스캔은 HIGH 51·CRITICAL 0, SBOM은 CycloneDX 1.6·구성 요소 90개다. 실제 제출·승인은 미진행이며 원본 산출물은 Ubuntu에 유지한다. UI 주소는 http://localhost:18082다. 누적 점검·전체 정리·Day 9 전체 완료는 아직이다. [첨부 식별 증거](evidence/95-artifacts-user-2026-10-05.txt). 아래는 이전 완료 기록이다.

최신 상태(2026-10-03): **9-1·9-2 완료·9-3 이후 미진행.** save·압축·해시 검증·복원 후 인터넷 없는 빈 별도 Docker 엔진에서 파일 적재·앱 기동에 성공했다. /tmp tmpfs에 따른 파일 조회 오류는 /day09-import 경로로 해결했다. 내부 agent·day09-airgap·해당 익명 볼륨 제거와 호스트 이미지·반입 파일 보존 및 해시 OK를 확인했다. [정리 증거](evidence/92-cleanup-user-2026-10-03.txt). Day 9 전체는 미완료다.

9-1 완료 근거: 사용자 출력으로 로컬 wheel 설치·오프라인 빌드와 network=none 기동, UID=10001·GID=0, PyYAML=6.0.2·healthz ok를 확인했다. 이후 시험 컨테이너 제거와 온라인용 pip 빌드의 이름 해석 실패·종료 코드 1을 확인했다. 이미지·wheels는 삭제하지 않았다. [9-1 마지막 증거](evidence/91-cleanup-online-failure-user-2026-10-03.txt).

이 Day의 Codex 작업에서 사용자와 합의한 절만 한 단계씩 진행한다.
실행 기록·오류 해결·다음 시작 지점은 SESSION.md에 남긴다.
실습은 Ubuntu WSL2에서 실행하며 Windows 프로젝트 폴더와의 파일 동기화 여부를 먼저 확인한다.

## 실습 파일
- [IMPORT-PACKAGE.md](IMPORT-PACKAGE.md) — 9-5 학습용 반입 신청서
- [.gitignore](.gitignore)
- [app.py](app.py)
- [compose.yaml](compose.yaml)
- [Dockerfile.offline](Dockerfile.offline)
- [requirements.txt](requirements.txt)

## 증거 자료
필요한 출력과 화면 캡처를 `evidence/`에 보관하고 SESSION.md에서 링크한다.
실제 비밀 값은 제거한다. 증거가 생길 때 폴더를 만든다.
