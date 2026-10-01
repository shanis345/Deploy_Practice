# Day 8 — 사내 CA와 TLS 검사(SSL 인스펙션)

- 가이드: [해당 Day 원문](../docs/guide/src/09-day08.md)
- 학습 기록: [SESSION.md](SESSION.md)
- 전체 진행: [PROGRESS.md](../PROGRESS.md)

## 진행 방식
현재 상태(2026-10-01): **종료·8-1~8-4 실습 및 자원 정리 완료.** 사용자 텍스트로 [HTTPS 요청·응답 헤더 및 복호화된 HTML 본문](evidence/84-https-observation-user-2026-10-01.txt)을 관찰했다. 이후 사용자 출력으로 컨테이너 5개·네트워크 2개 제거와 프로젝트 잔존 목록 부재, 공개 CA 파일·agent:0.2.0-ca 이미지 보존을 확인했다. [정리 증거](evidence/cleanup-user-2026-10-01.txt). 체크포인트 6문항 해설은 제공했으며 사용자 독립 평가는 미실시다.

8-1~8-3 근거: 사용자 출력으로 프록시·CA 준비, CA 미신뢰 실패·두 해결 방식의 HTTPS 200, [발급자·검증 오류](evidence/83-issuer-user-2026-10-01.txt), [CA 번들 150·151개·mitmproxy CA](evidence/83-bundle-user-2026-10-01.txt), [curl CA 지정 전후 비교](evidence/83-curl-user-2026-10-01.txt)를 확인했다. 상세 빌드·실행 근거는 SESSION에 있다. 세 agent는 마지막 ps에서 healthy였다.

이 Day의 Codex 작업에서 사용자와 합의한 절만 한 단계씩 진행한다.
실행 기록·오류 해결·다음 시작 지점은 SESSION.md에 남긴다.
실습은 Ubuntu WSL2에서 실행하며 Windows 프로젝트 폴더와의 파일 동기화 여부를 먼저 확인한다.

## 실습 파일
- [.gitignore](.gitignore)
- [compose.yaml](compose.yaml)

## 증거 자료
필요한 출력과 화면 캡처를 `evidence/`에 보관하고 SESSION.md에서 링크한다.
실제 비밀 값은 제거한다. 증거가 생길 때 폴더를 만든다.
