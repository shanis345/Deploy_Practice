# 진행 현황

- 기준일: 2026-09-23
- 실습 중단 지점: **Day 0 실습 완료 — 0-1~0-5 완료**
- 2026-09-23 Codex 재점검: 사용자가 Docker Desktop을 실행한 후 `check` 전 항목 통과(종료 코드 0), 실습 이미지 12개 모두 존재. 0-1 실행 가능 상태를 재확인했다. kubectl 1.36.1·dive 0.13.1·Compose 5.5.1의 가이드 버전 차이는 남아 있다.
- 2026-09-23 사용자 제공 출력·화면: 0-2~0-5 완료. lazydocker 0.25.2 교체 후 이미지·네트워크 화면 확인 및 Ubuntu 실습 폴더 목록 확인을 마쳤다. day14 폴더는 없지만 Day 14는 skeleton을 사용한다.
- Day 0 실습 체크리스트 3개를 충족했다. 개념 자기점검 4문항의 사용자 답변 평가는 별도로 진행하지 않았다. 도구 버전 차이는 후속 실습의 미해결 확인 사항으로 유지한다. Day 1은 사용자 요청 전까지 진행하지 않는다.
- 2026-09-23 세션 회고: [Day 0 기록](day00/SESSION.md)에 실습 결과 요약, 오류 원인·해결·재진단 순서, 핵심 Lessons, 이미지/컨테이너와 학습용 에이전트에 관한 후속 질문을 정리했다. Windows 기록에 반영했으며 Ubuntu 복사본은 동기화하지 않았다.
- 로컬 프로젝트 자료 정리는 실습 진도와 별도로 수행했다.
- GitHub 저장소: [https://github.com/shanis345/Deploy_Practice](https://github.com/shanis345/Deploy_Practice)
- 초기 구성 PR #1은 GitHub `main`에 병합된 상태를 확인했다(2026-09-23, `3c8a290`). 초기 연결 직후 로컬 파일과 `origin/main`의 Git 기준 차이가 없었다.
- Day 0 세션은 사용자 요청으로 종료한다. 완료 기록·환경 차이·증거 파일은 `codex/day00-completion` 브랜치에서 `main` 대상 PR로 제출하며, 병합은 별도 단계다.
- Codex 프로젝트 등록과 Day별 작업 생성은 아직 하지 않았다.

| Day | 주제 | 상태 | 기록 |
|---|---|---|---|
| 00 | 환경 준비 | 실습 완료 · 0-1~0-5 | [SESSION](day00/SESSION.md) |
| 01 | 가상화 계층과 vSphere: 물리 서버부터 컨테이너까지 | 미시작 | [SESSION](day01/SESSION.md) |
| 02 | 리눅스 네트워크 기초: 네임스페이스·브리지·라우팅·DNS | 미시작 | [SESSION](day02/SESSION.md) |
| 03 | Docker 이미지·레이어·컨테이너, 그리고 심의를 통과하는 이미지 | 미시작 | [SESSION](day03/SESSION.md) |
| 04 | Docker 네트워크와 진단 3단계 | 미시작 | [SESSION](day04/SESSION.md) |
| 05 | Docker Compose: 다중 서비스와 그 한계 | 미시작 | [SESSION](day05/SESSION.md) |
| 06 | 망분리 재현: DMZ · 업무망 · DB존, 그리고 방화벽 신청서 | 미시작 | [SESSION](day06/SESSION.md) |
| 07 | 포워드 프록시, 화이트리스트, HTTP_PROXY/NO_PROXY 함정 | 미시작 | [SESSION](day07/SESSION.md) |
| 08 | 사내 CA와 TLS 검사(SSL 인스펙션) | 미시작 | [SESSION](day08/SESSION.md) |
| 09 | 폐쇄망 이미지 반입: 오프라인 빌드 · save/load · 사내 레지스트리 · 스캔 · SBOM | 미시작 | [SESSION](day09/SESSION.md) |
| 10 | Kubernetes 기초: Pod · Deployment · Service · probe | 미시작 | [SESSION](day10/SESSION.md) |
| 11 | 설정 · 비밀 · 수신 · Helm: ConfigMap, Secret, Ingress, 차트 | 미시작 | [SESSION](day11/SESSION.md) |
| 12 | NetworkPolicy로 존 분리, 그리고 OpenShift의 차이 | 미시작 | [SESSION](day12/SESSION.md) |
| 13 | LLM 게이트웨이 · 감사 로그 · 관측성 기초 | 미시작 | [SESSION](day13/SESSION.md) |
| 14 | Walking Skeleton 종합: 전 구간 관통, 검증 스크립트, 런북, 이관 | 미시작 | [SESSION](day14/SESSION.md) |

## 다음 실습을 시작할 때

1. Day 0 기록과 환경 차이를 읽는다.
2. 사용자에게 지정받은 절과 범위를 기준으로 이어 간다.
3. kubectl 고정 버전 불일치 등 미해결 사항을 완료로 간주하지 않는다.
