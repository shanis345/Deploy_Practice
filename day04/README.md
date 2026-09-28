# Day 4 — Docker 네트워크와 진단 3단계

- 가이드: [해당 Day 원문](../docs/guide/src/05-day04.md)
- 학습 기록: [SESSION.md](SESSION.md)
- 전체 진행: [PROGRESS.md](../PROGRESS.md)

## Day 4 결과 요약

2026-09-27~28에 4-1~4-6 실습과 lazydocker 관찰을 진행했고, 2026-09-28 사용자의 마무리 요청 및 자원 정리 완료 확인으로 Day 4를 종료했다. 실습 결과는 사용자 제공 출력·화면에 근거한다. 마지막 정리는 사용자 진술이며 삭제 후 목록·포트 출력 원문은 받지 않았다. 별도 자기점검 5문항의 문답 평가는 미진행이다.

| 단계 | 실제 확인한 결과 | 배운 내용 |
|---|---|---|
| 4-1 이름 통신 | lab-net에서 web 이름 해석·HTTP 200, 기본 bridge에서 web2 NXDOMAIN | 사용자 정의 네트워크의 이름 해석과 네트워크 소속 확인 |
| 4-2 양쪽 연결 | isolated에 lab-net 추가 후 DNS·HTTP 성공, 두 네트워크의 IP 확인 | 컨테이너 하나가 여러 네트워크에 연결될 수 있음 |
| 4-3 게시·바인딩 | Ubuntu 비루프백 주소의 8080 실패·8081 성공, 게시 없는 client→web:80 성공 | 내부 통신과 호스트 포트 게시, 바인딩 주소 구분 |
| 4-4 호스트 접근 | 컨테이너 localhost 실패, host.docker.internal 성공, Ubuntu IP 직접 요청 시간 초과 | 실행 환경과 접근 경로를 구분해 진단 |
| 4-5 진단 3단계 | DNS→TCP 80→HTTP 200, TCP 81 거절·다른 IP의 TCP 시간 초과 | 실패 단계와 오류 문구로 조사 범위 좁히기 |
| 4-6 DNS 설정 | resolv.conf의 DNS·검색 접미사 및 hosts 매핑 확인 | 설정 전달과 실제 사내 시스템 연결 검증 구분 |
| 화면 관찰 | lazydocker의 Containers: none과 달리 inspect에서 isolated의 양쪽 연결 확인 | UI와 실제 조회 결과를 대조하고 불일치를 기록 |

핵심은 문제가 발생한 컨테이너에서 이름 해석 → TCP 연결 → HTTP 응답 순으로 확인하는 것이다. 서비스 상태·포트·바인딩·라우팅·방화벽을 조사하고, HTTP 단계에서는 경로·인증 등을 확인한다. 시간 초과만으로 방화벽 문제라고 확정하지 않는다. 인증·TLS 장애를 실제 재현한 것은 아니다.

FDE는 배포·연동 문제의 증거를 수집하고 담당 애플리케이션 설정을 수정하며, 고객사 IT·보안팀과 해결을 조율하고 재검증한다. 사내 DNS·방화벽·계정 변경과 인수인계 후 운영 책임은 프로젝트 계약·권한에 따라 나눈다. 로컬 배포 테스트 성공이 고객 환경의 연결 성공까지 보장하지는 않는다.

## 남은 관찰 사항과 종료 범위

- Docker Desktop에서는 루프백에 바인딩된 Ubuntu 서버에도 기본 host.docker.internal 경로로 접근했다. Linux Docker Engine 가이드의 예상 결과와 구분한다.
- Ubuntu IP 172.18.60.227과 기존 koica 네트워크 172.18.0.0/16의 겹침을 확인했다. 직접 IP 시간 초과의 세부 원인은 미확정이며 기존 koica 자원은 변경하지 않았다.
- lazydocker 0.25.2의 연결 목록 표시 불일치 원인은 미확정이다. [lab-net 화면](evidence/lazydocker-lab-net-user-2026-09-28.png), [other-net 화면](evidence/lazydocker-other-net-user-2026-09-28.png).
- 사용자에게 안내한 정리 대상은 web·client·web2·client2·isolated·pub·pub2 및 lab-net·other-net이다. Python 서버 종료는 앞선 출력으로 확인했고 임시 폴더 `/tmp/day04-http.fdpmdu`와 이미지는 삭제 대상에 포함하지 않았다.
- 다음 Day는 사용자가 요청할 때 시작한다. Windows 기록과 Ubuntu 실습 폴더는 별도이며 동기화하지 않았다.

## 진행 방식
이 Day의 Codex 작업에서 사용자와 합의한 절만 한 단계씩 진행한다.
실행 기록·오류 해결·다음 시작 지점은 SESSION.md에 남긴다.
실습은 Ubuntu WSL2에서 실행하며 Windows 프로젝트 폴더와의 파일 동기화 여부를 먼저 확인한다.

## 실습 파일
- [diag3.sh](diag3.sh)

## 증거 자료
필요한 출력과 화면 캡처를 `evidence/`에 보관하고 SESSION.md에서 링크한다.
실제 비밀 값은 제거한다. 증거가 생길 때 폴더를 만든다.
