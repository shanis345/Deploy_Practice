# Day 2 — 리눅스 네트워크 기초: 네임스페이스·브리지·라우팅·DNS

- 가이드: [해당 Day 원문](../docs/guide/src/03-day02.md)
- 학습 기록: [SESSION.md](SESSION.md)
- 전체 진행: [PROGRESS.md](../PROGRESS.md)

## 이번 학습 결과
- 실습 2-1~2-7 완료: 네임스페이스·브리지 연결, 라우팅·NAT, 패킷 관찰, Docker 네트워크·DNS, cgroup 메모리 제한.
- [절별 결과와 핵심 개념](SESSION.md), [주요 실행 증거](evidence/day02-results-user-2026-09-24.txt), [정리 증거](evidence/day02-cleanup-user-2026-09-25.txt).
- 정리·자기점검의 최신 상태는 SESSION.md의 진행 상태와 인수인계를 따른다. Windows 기록과 Ubuntu 실행 결과를 구분한다.

## 진행 방식
이 Day의 Codex 작업에서 사용자와 합의한 절만 한 단계씩 진행한다.
실행 기록·오류 해결·다음 시작 지점은 SESSION.md에 남긴다.
실습은 Ubuntu WSL2에서 실행하며 Windows 프로젝트 폴더와의 파일 동기화 여부를 먼저 확인한다.

## 실습 파일
- [netns-lab.sh](netns-lab.sh)

## 증거 자료
사용자 제공 주요 출력을 `evidence/`에 보관하고 SESSION.md에서 링크한다.
실제 비밀 값은 기록하지 않는다. 파일은 전체 터미널 덤프가 아닌 출처를 명시한 주요 발췌다.
