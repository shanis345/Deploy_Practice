# 진행 현황

- 기준일: 2026-09-22
- 실습 중단 지점: **Day 0 — 0-1 부트스트랩 완료**
- Day 0 전체는 아직 진행 중이다. 이후 절은 사용자 요청 전까지 진행하지 않는다.
- 로컬 프로젝트 자료 정리는 실습 진도와 별도로 수행했다.
- GitHub 저장소: [https://github.com/shanis345/Deploy_Practice](https://github.com/shanis345/Deploy_Practice)
- 초기 구성 브랜치: `codex/initial-practice-setup`. 자료는 PR로 제출하며 main 병합은 별도 단계다.
- Codex 프로젝트 등록과 Day별 작업 생성은 아직 하지 않았다.

| Day | 주제 | 상태 | 기록 |
|---|---|---|---|
| 00 | 환경 준비 | 진행 중 · 0-1 완료 | [SESSION](day00/SESSION.md) |
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
