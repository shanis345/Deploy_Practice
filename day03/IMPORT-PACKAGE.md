# Day 3 — 이미지 반입 패키지 초안

기준일: 2026-09-27. Day 3의 반입 패키지 초안 작성 완료. 사용자 Ubuntu 실행 결과를 근거로 작성한 학습용 문서이며 제출·승인된 문서가 아니다. 미검증 항목은 아래에 명시한다.

| 항목 | 값 또는 상태 | 근거·확인 범위 |
|---|---|---|
| 이미지명:태그 | agent:0.2.0 | [빌드 출력](evidence/build-agent-0.2.0-user-2026-09-27.txt) |
| 현재 이미지 ID | sha256:a4ef49ae142efb1a03fe43c30d4a6f68ceee1c649578c33407827e8f6f4185a3 | [inspect 출력](evidence/image-agent-0.2.0-user-2026-09-27.txt). 이번 환경에서는 빌드 manifest list 해시와 같음 |
| 현재 RepoDigests | agent@sha256:a4ef49ae142efb1a03fe43c30d4a6f68ceee1c649578c33407827e8f6f4185a3 | 실제 조회값. 원격 push·반입 완료를 뜻하지 않음 |
| 빌드 출력 manifest | sha256:edd499f43e2a868f9c5a8ec5d6a194f0f7801b2618eaa605753687f04708db74 | 빌드 당시 값. 레지스트리 push·반입본 검증은 미진행 |
| 빌드 출력 manifest list | sha256:a4ef49ae142efb1a03fe43c30d4a6f68ceee1c649578c33407827e8f6f4185a3 | 빌드 당시 값. 위 manifest와 다른 종류의 식별자 |
| 베이스 이미지 | python:3.12.14-slim | 사용자 Dockerfile·빌드 로그. 고객사 승인 목록 미확인 |
| 베이스 digest | sha256:f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f | 빌드의 resolve 출력 |
| OS / Python | Debian 13.7 / Python 3.12.14 | 스캔 대상 식별·python --version 출력 |
| 플랫폼·이미지 크기 | linux/amd64 · 181,278,388바이트 (약 172.9 MiB) | inspect Size. 반입 압축 파일 크기·실제 디스크 사용량과 구분 |
| 실행 사용자·그룹 | UID 10001(appuser) / GID 0(root) | 0.2.0의 User=10001 설정 및 실제 id 출력 확인 |
| 선언 포트 | 8000/TCP | 0.2.0 inspect 확인. 호스트 공개 포트와 구분 |
| 헬스체크 | /healthz · 간격 15초 · 제한시간 3초 · 시작 유예 5초 · 재시도 3회 | 0.2.0 정의 조회. 실제 healthy 상태 검사는 미진행 |
| 취약점 | HIGH 44 / CRITICAL 0 | [재스캔 요약](evidence/trivy-agent-0.2.0-user-2026-09-27.txt), Trivy 0.56.2, 2026-09-27 |
| 수정 버전 미제공 항목 제외 | HIGH 0 / CRITICAL 0 | [필터 검사 요약](evidence/trivy-agent-0.2.0-fixed-user-2026-09-27.txt). 잔여 44건 해소·예외 승인 아님 |
| 비밀 정보 미포함 | 미확정 | 이번 스캔은 --scanners vuln이며 비밀 검사·전체 레이어 검증은 미수행. ENV·.dockerignore만으로 미포함을 보증하지 않음 |
| 읽기 전용 루트·임시 경로 | 0.1.0에서 쓰기 제한·tmpfs 관찰 완료 | 0.2.0 및 앱 전체 기능의 읽기 전용 동작은 미검증 |
| 반입 tar·파일 SHA256·SBOM | 미생성 | Day 9에서 구체화할 항목. 지금 완료로 표기하지 않음 |
| 고객사 기준·반입자·승인자 | 미정 | 실제 고객사 정보 없이 확정하지 않음 |

## 스캔 보고서

- Ubuntu 전체 실행 로그: /home/user/onprem-lab/day03/trivy-agent-0.2.0.log
- Ubuntu 필터 검사 로그: /home/user/onprem-lab/day03/trivy-agent-0.2.0-fixed.log
- [새 이미지 검사 결과 표 전체](evidence/trivy-agent-0.2.0-report-user-2026-09-27.txt): 사용자가 첨부한 출력에서 HIGH 44건의 표를 모두 발췌했다. 재검사하거나 Ubuntu 파일을 동기화한 것이 아니다.
- [수정 버전 미제공 항목 제외 결과](evidence/trivy-agent-0.2.0-fixed-user-2026-09-27.txt): 원래 표와 함께 보존하며 이를 단독으로 취약점 0건 보고서로 사용하지 않는다.
- DB는 초기 검사에서 다운로드하고 두 재검사에는 --skip-db-update를 사용했다. DB metadata의 정확한 갱신 시각·해시는 별도 수집하지 않았다.

## 잔여 항목 대응

HIGH 44건의 실제 영향·사용 경로·완화 조치를 검토하고 필요하면 고객사 예외 승인을 요청한다. 수정 버전이 없다는 사실만으로 위험이 없다고 판정하지 않는다. 패치 제공 시 베이스 갱신·재검사를 수행한다.
