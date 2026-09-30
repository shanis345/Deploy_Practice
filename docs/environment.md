# 실습 환경

## 최신 Day 7 상태 — 종료 정리 후 (2026-09-30)
- 사용자 Ubuntu 출력으로 docker compose -p day07 down의 컨테이너 4개(agent·internal-api·probe·proxy)·네트워크 2개(closed·outside) 제거를 확인했다. 프로젝트 필터 컨테이너·네트워크 목록은 헤더만 표시됐다.
- 관찰용 mitm 제거·8082 리스너 부재와 임시 빌드 이미지·폴더 제거는 앞서 확인했다. 이미지·볼륨 삭제 옵션 및 전역 prune은 사용하지 않았다. 다른 프로젝트 자원은 이번에 재조회하지 않았다.
- Codex 직접 Ubuntu 실행·동기화가 아닌 사용자 출력 확인이다. 아래 Day 7 기동·관찰 기록은 종료 전 이력이다. [종료 정리 증거](../day07/evidence/cleanup-user-2026-09-30.txt).

## Day 7 mitm 관찰·정리 완료 (2026-09-30)
- 사용자 출력으로 mitmproxy/mitmproxy:11.0.0의 mitm 컨테이너 running을 확인했다. 초기에는 outside만 연결됐으나 후속 사용자 network connect·inspect 출력으로 day07_closed·day07_outside 양쪽 연결을 확인했다.
- 웹 포트는 호스트 127.0.0.1:8082→컨테이너 8081이다. 가이드의 8081 호스트 포트는 기존 pub2가 사용 중이어서 변경했다. v11.0.0 공식 웹 옵션에 없는 web_password는 제외하고 실행했다.
- 초기 로그는 usermod: no changes만 반환했으나 후속 사용자 출력으로 probe에서 mitm:8080을 명시한 HTTP 요청이 via mitm: 200임을 확인했다. 후속 사용자 제공 Request 탭 텍스트에서 GET http://example.com/·curl/8.7.1 등 헤더와 요청 본문 없음을 확인했다. Response 텍스트에서 HTTP 200·HTML 응답 헤더·Example Domain 본문도 확인했다. Timing에서 요청 첫 바이트→응답 완료 223ms를 관찰했다. 후속 사용자 출력으로 mitm 종료·자동 제거·8082 리스너 부재를 확인했다. 기존 Compose 네 서비스는 모두 실행 중이며 agent는 healthy다. Codex의 직접 브라우저 검증은 아니다. 기존 Compose 서비스는 유지한다. [Day 7 SESSION](../day07/SESSION.md).

## Day 7 임시 빌드 정리 완료 — 7-3 종료 (2026-09-30)
- 사용자 출력으로 default 빌더(docker 드라이버, 사전 조회 BuildKit v0.33.0)의 임시 이미지 day07-buildargs:lab 빌드 성공을 확인했다. 후속 사용자 출력으로 day07-buildargs:lab 삭제·이미지 목록 부재 및 /tmp/day07-buildargs.YTZNch 폴더 제거를 확인했다. 빌드 캐시는 정리하지 않았다. Alpine 3.20 기반 RUN echo build만 수행했다.
- 예약 프록시 인자와 일반 ARG 비교용 공개 더미 값을 사용했다. 사용자 히스토리 출력에서 일반 ARG의 더미 값이 남고 예약 HTTP_PROXY는 표시되지 않음을 확인했다. 임시 이미지·폴더 정리는 완료했으며 실제 프록시 네트워크 장애·pip 설치를 시험한 것은 아니다. [정리 증거](../day07/evidence/73-cleanup-user-2026-09-30.txt).
- buildx ls의 별도 desktop-linux 항목은 protocol not available이다. 해당 항목은 변경하지 않았고 원인은 미확정이다. 이번 빌드는 default를 명시해 성공했다. 기존 Day 7 Compose 구성은 유지한다.

## Day 7 상태 이력 — 7-1·7-2 완료 (2026-09-30)
- 사용자 Ubuntu 출력 기준: /home/user/onprem-lab/day07에서 로컬 이미지로 네 서비스를 기동했다. agent healthy 및 probe→agent healthz status=ok·version=0.2.0을 확인했다.
- day07_closed internal=true: internal-api·proxy·agent·probe. day07_outside internal=false: proxy만 연결. 호스트 포트 게시 없음.
- agent의 HTTP_PROXY·HTTPS_PROXY·http_proxy·https_proxy는 http://proxy:3128, NO_PROXY·no_proxy는 localhost,127.0.0.1,proxy,internal-api,.corp.local로 전달됐다. 7-2 사용자 출력으로 example.com HTTP/HTTPS 200(331ms/191ms), www.google.com HTTP 403·HTTPError·1ms 및 HTTPS OSError·터널 403 거부·1ms를 확인했다. Squid 접근 로그의 외부 요청 네 행(TCP_MISS/200, TCP_TUNNEL/200, TCP_DENIED/403 두 행)이 앱 결과와 일치한다. internal-api는 200·11ms이고 해당 로그에 없어 우회 설정과 일치한다. [응답·로그 증거](../day07/evidence/72-requests-and-log-user-2026-09-30.txt).
- 컨테이너 4개·네트워크 2개 유지. 사전 조회에서 기존 Day 4 pub2·web2·web은 실행 중이었고 나머지 Day 4 컨테이너 및 koica 앱은 중지 상태였다. 해당 자원은 변경하지 않았다.
- Codex 직접 Ubuntu 실행·동기화가 아닌 사용자 출력 확인이다. [Day 7 기록](../day07/SESSION.md), [검증 증거](../day07/evidence/71-config-user-2026-09-30.txt).

## 최신 Day 6 상태 — 종료 정리 후 (2026-09-30)
- 사용자 출력으로 docker compose -p day06 down의 컨테이너 7개·네트워크 3개 제거를 확인했다. Day 6 프로젝트 필터 컨테이너·네트워크 목록 및 Ubuntu의 8080 리스너 조회는 헤더만 표시됐다.
- 이미지·볼륨·임시 백업 삭제는 하지 않았다. 해당 목록과 다른 프로젝트 상태를 이번에 다시 조회한 것은 아니다. Codex 직접 Ubuntu 실행 결과와 구분한다. [정리 증거](../day06/evidence/cleanup-user-2026-09-30.txt).

## Day 6 상태 이력 — 누적 장애 복구 후, 정리 전 (2026-09-30)
- 사용자 출력 기준으로 장애 1~5번 개별 복구를 확인했다. 마지막 agent 소속은 biz·dbzone이며 healthz 정상·외부 요청 gaierror(1ms)다. 4번 복구 후 healthy·FailingStreak=0·최근 검사 5회 성공도 확인했다.
- 실습 컨테이너·네트워크와 /tmp/day06-compose.OTTiFi 백업을 유지한다. 전체 자원 정리나 마지막 시점의 모든 경로 재시험은 하지 않았다. Ubuntu에서 Codex가 직접 실행한 결과가 아니다. 상세 이력은 [Day 6 SESSION](../day06/SESSION.md) 참고.

기준일: 2026-09-29. Day 2~5 실습·정리 결과는 사용자 제공 출력과 스크린샷에 근거한다. 2026-09-23 환경 재점검은 Codex 직접 조회이며 이전 결과는 별도 이력으로 구분한다.

## Day 6 6-3 완료·원복 상태 (2026-09-29)
- 사용자 출력으로 compose.yaml과 `/tmp/day06-compose.OTTiFi`의 SHA-256이 원본 1c2e71cf3ac308e285d14ed3a2a3ab5d7dd7f0db86a82294b610bad4e69db3cb와 일치함을 확인했다.
- agent는 재생성 후 healthy이며 실제 연결은 day06_biz·day06_dbzone만 남았다. healthz status=ok·version=0.2.0·host=f4298542de49, 외부 요청은 ok=false·gaierror·7ms다. 원복 후 DB·ERP는 재시험하지 않았다.
- 6-3 원복까지 완료했다. Day 6 구성은 유지하고 백업 파일도 보존한다. 6-4 이후 및 Day 전체 정리는 미진행이다. [원복 증거](../day06/evidence/63-restored-user-2026-09-29.txt), [SESSION](../day06/SESSION.md).

## Day 6 6-3 DMZ 추가 당시 상태 (2026-09-29, 원복 전 이력)
- 사용자 출력으로 백업 `/tmp/day06-compose.OTTiFi`와 원본 compose.yaml의 SHA-256 일치를 확인한 뒤 agent의 networks 한 줄만 변경·재적용했다. Windows 실습 소스는 원본을 유지한다.
- DMZ 추가 당시 agent는 biz·dbzone·dmz에 연결됐으며 healthy였다. gateway 경유 healthz는 status=ok·version=0.2.0·host=8faa0748aa9d, 외부 example.com 요청은 ok=true·HTTP 200·105ms였다.
- 이후 원복을 확인했으므로 이 구성은 과거 재현 이력이다. [재현 증거](../day06/evidence/63-dmz-added-user-2026-09-29.txt), [SESSION](../day06/SESSION.md).

## Day 6 6-2 완료·통신 확인 (2026-09-29, DMZ 추가 전 이력)
- 사용자 Ubuntu 출력으로 gateway 경유 healthz status=ok·version=0.2.0·host=b03497230cb3 및 agent→postgres:5432 TCP ok=true·elapsed_ms=1을 확인했다. DB 인증·SQL은 미시험이다.
- ③ DMZ→DB 이름 기반 접속은 getaddrinfo Try again·종료코드 1로 실패했다. DB IP 172.22.0.4:5432 직접 시도도 3초 타임아웃·종료코드 1이다. 예상한 접근 제한은 확인했으며 특정 방화벽 규칙을 조회한 것은 아니다. ④ probe-biz에서 example.com DNS 실패·코드 1을 확인했고 IPv4 라우팅에는 172.21.0.0/16 직접 연결 경로(src 172.21.0.2)만 있고 default가 없다. 외부 IP 직접 연결·IPv6는 미시험이다. ⑤ 실제 agent→ERP HTTP 200·Name: erp-api를 확인했다. ERP IP는 172.21.0.5, 요청 RemoteAddr는 172.21.0.3:57002다. ⑥ agent의 example.com 요청은 ok=false·gaierror·이름 해석 실패·8ms다. 모든 외부 IP·포트를 시험한 것은 아니다. ⑦ probe-db→agent(172.22.0.3):8000 신규 TCP 연결은 succeeded·종료코드 0이다. 6-2 완료이며 실습 구성은 유지한다. 6-3 이후는 미진행이다. [⑦ 증거](../day06/evidence/connectivity-07-user-2026-09-29.txt). [⑥ 증거](../day06/evidence/connectivity-06-user-2026-09-29.txt). [⑤ 증거](../day06/evidence/connectivity-05-user-2026-09-29.txt). [④ 증거](../day06/evidence/connectivity-04-user-2026-09-29.txt). [①② 증거](../day06/evidence/connectivity-01-02-user-2026-09-29.txt), [③ DNS 증거](../day06/evidence/connectivity-03-dns-user-2026-09-29.txt), [③ IP 증거](../day06/evidence/connectivity-03-ip-user-2026-09-29.txt).

## Day 6 6-1 완료·실행 상태 (2026-09-29)
- 사용자 up·ps·network inspect 출력으로 네트워크 3개와 컨테이너 7개 생성·기동을 확인했다. 모두 Up이고 agent·postgres는 healthy다. gateway가 127.0.0.1:8080→80을 게시한다.
- day06_dmz internal=false: gateway·probe-dmz. day06_biz internal=true: gateway·erp·agent·probe-biz. day06_dbzone internal=true: agent·postgres·probe-db. 소속이 구성과 일치한다.
- 6-1 완료이며 구성은 실행 중이다. 6-2 실제 통신·차단 시험은 미진행이다. Codex 직접 Ubuntu 실행·재조회와 구분한다. [기동 증거](../day06/evidence/startup-user-2026-09-29.txt), [SESSION](../day06/SESSION.md).

## Day 6 사전 점검 (2026-09-29, 기동 전 이력)
- 사용자 Ubuntu 출력으로 Day 6 파일 3개(compose.yaml·gateway.conf·break.sh)의 SHA-256이 Windows 사본과 일치함을 확인했다. break.sh는 755이며 동일 해시의 Windows 파일은 LF다.
- Docker Client/Engine 29.8.0, Desktop 4.92.0(240144), Compose v5.5.1, Compose 문법 검사 성공 및 필요 이미지 5개의 linux/amd64 로컬 존재를 확인했다.
- Ubuntu 8080 리스너와 Docker의 8080 게시가 없다. pub2(8081 게시)·web·web2는 실행 중이고 pub·isolated·client·client2·기존 koica 앱은 중지 상태로 남아 있다. 기존 자원 변경·파일 동기화는 수행하지 않았다.
- 이 사전 점검 뒤 6-1 기동을 안내했고 후속 출력으로 위 실행 상태를 확인했다. [사전 점검 증거](../day06/evidence/precheck-user-2026-09-29.txt), [SESSION](../day06/SESSION.md).

## Day 5 종료 상태 (2026-09-29)
- 사용자 compose down 출력으로 day05-nginx-1·day05-agent-1·day05-postgres-1 및 day05_default 제거를 확인했다. compose ps -a·해당 네트워크 목록은 헤더만 남았고 Ubuntu ss에 8080 LISTEN 행이 없다.
- day05_pgdata 볼륨은 local로 존재한다. 이미지와 프롬프트 임시 백업 /tmp/day05-prompt.GrrBHr는 삭제 대상으로 지정하지 않았으며 이번 단계에서 재조회하지 않았다. 프롬프트 원복은 앞선 파일 비교·API·해시로 확인했다.
- Day 4 잔존 자원·기존 koica 자원은 정리 범위에 포함하지 않았다. 아래 실행 중 상태는 실습 당시 이력이며 Day 5의 현재 컨테이너 실행 상태가 아니다.
- 5-1~5-4·지정 자원 정리를 완료해 사용자 요청에 따라 Day 5를 종료했다. 일부 TUI 상세 관찰과 별도 자기점검 평가는 미확인으로 남긴다. [정리 증거](../day05/evidence/cleanup-user-2026-09-29.txt), [SESSION](../day05/SESSION.md).

## Day 5 사전 점검 및 Day 4 자원 잔존 (2026-09-29)
- 사용자 Ubuntu 출력에서 Docker Client/Engine 29.8.0, Desktop 4.92.0(240144), Compose v5.5.1 및 Compose 문법 검사 성공을 확인했다. Day 5 실습 파일 5개의 SHA-256은 Windows 사본과 일치한다.
- 사전 점검에서 이전 Day 4 정리 완료 진술과 달리 pub·pub2·web·web2가 실행 중이며 isolated·client·client2도 중지된 상태로 남아 있었다. 이후 pub 중지를 확인했고 lazydocker 화면에는 lab-net·other-net도 보였다. 과거 진술과 다른 경위는 미확인이다. Day 4 자원 정리 완료로 간주하지 않는다.
- 사전 점검에서 pub는 127.0.0.1:8080→80, pub2는 8081→80을 게시했고 Ubuntu ss에도 127.0.0.1:8080 LISTEN이 표시됐다. 후속 사용자 출력으로 pub 중지 및 ss의 8080 리스너 부재를 확인했다. 실행 중 목록에는 pub2·web2·web이 남아 있다.
- Day 5 적용 이미지는 agent:0.2.0·postgres:16.4-alpine·nginx:1.27-alpine이다. 후속 사용자 up·ps 출력으로 day05_default 네트워크·day05_pgdata 볼륨 생성, agent·postgres healthy 및 nginx 실행·127.0.0.1:8080→80 게시 성공을 확인했다.
- 후속 API 출력으로 healthz의 status=ok·version=0.2.0, prompt_exists=true·prompt_sha=258e1f7baff4·rubric 내용·db_dsn_set=true, postgres:5432의 TCP ok=true·elapsed_ms=1을 확인해 5-1 완료. DB 인증·SQL·영속성 시험은 미진행이다.
- 5-2 ① 사용자 출력으로 agent의 /_lab/exit 후 RestartCount 0→1, health starting→healthy 및 healthz 정상 응답을 확인했다. 컨테이너 생성 시각과 host a105f231277a는 유지됐다.
- ② 사용자 출력에서 postgres 중단(Exited 0) 중에도 agent healthy·healthz ok이나 DB TCP는 gaierror(Temporary failure in name resolution)였다. postgres 재기동 후 Up 12 seconds (healthy)·TCP ok=true·elapsed_ms=0을 확인했다.
- ③ 첫 조회부터 RestartCount=1·unhealthy였고 hang 요청은 10초 타임아웃이었다. 40초 후에도 횟수 1·unhealthy 및 healthz 3초 타임아웃(코드 28)을 확인했다. 수동 restart 후 agent Up 12 seconds (healthy)·healthz ok·DB TCP ok=true로 복구됐다. 처음 무응답의 원인은 미확정이다.
- ③ 재확인에서는 RestartCount=0·healthy → hang=true 응답 → 40초 후 RestartCount=0·unhealthy 및 healthz 3002ms 타임아웃(코드 28)을 확인했다. 수동 restart 후 agent Up 10 seconds (healthy), nginx Up 31 minutes, postgres Up 11 minutes (healthy) 및 healthz ok로 복구돼 5-2 완료. 마지막 복구 후 DB TCP는 재조회하지 않았다. Day 5 서비스·네트워크·볼륨은 유지 중이다.
- 5-3 사용자 출력으로 Ubuntu config/prompt.txt의 한 줄 추가가 /prompt에 반영되고 prompt_reloaded sha가 258e1f7baff4→a9099fd31924로 바뀐 것을 확인했다. 이미지 ID a4ef49ae142e… 및 StartedAt=2026-09-29T00:48:28.108529054Z, RestartCount=0·healthy는 유지됐다. 후속 cp·cmp·API 출력으로 백업 /tmp/day05-prompt.GrrBHr와 파일 일치, 원본 두 문장·sha=258e1f7baff4 복귀를 확인해 5-3 완료. 임시 백업은 삭제하지 않았고 Windows prompt.txt는 원본을 유지한다.
- 기존 koica 앱은 사전 조회에서 Exited (143) 2 weeks ago이며 변경하지 않았다. Codex가 Ubuntu 명령을 직접 실행하거나 파일을 동기화하지 않았다. 상세는 [Day 5 SESSION](../day05/SESSION.md)을 참고한다.

## Day 4 종료 상태와 네트워크 관찰 (2026-09-28)
- Day 4 컨테이너 web·client·web2·client2·isolated·pub·pub2 및 lab-net·other-net의 삭제와 목록·포트 조회를 안내했고 사용자가 “완료했어”라고 확인했다. 종료 출력 원문은 미제공이므로 현재 목록·리스너 부재를 Codex가 검증한 것은 아니다. 아래 주소·연결 정보는 실습 당시 관찰이다. 기존 koica 자원·이미지·볼륨은 정리 대상에 포함하지 않았다.
- lazydocker 0.25.2의 사용자 lab-net·other-net 화면은 모두 Containers: none 및 서브넷 미표시였지만, Docker inspect는 lab-net의 client·web·isolated와 other-net의 isolated를 보고했다. 양쪽 연결은 직접 조회 출력으로 확인했으며 두 화면을 증거로 보존해 관찰을 마쳤다. 화면 표시 불일치의 내부 원인은 미확정이다. 업데이트·설정 변경은 수행하지 않았다.
- Ubuntu IP는 `172.18.60.227`, Docker bridge는 `172.17.0.0/16`, 기존 koica-oda-local-test_default는 `172.18.0.0/16`, lab-net은 `172.19.0.0/16`, other-net은 `172.20.0.0/16`이다. Ubuntu IP와 기존 koica Docker 대역의 겹침을 확인했다. koica 자원은 변경하지 않았다.
- Ubuntu의 Python 9999 서버를 127.0.0.1에서 0.0.0.0으로 바꾸자 Ubuntu 자체의 비루프백 IP 요청은 코드 7에서 HTTP 200으로 바뀌었다. 컨테이너의 Ubuntu IP 직접 요청은 변경 전후 모두 연결 시간 초과(코드 28)였다. 대역 겹침은 경로 충돌 후보이며 패킷 경로·방화벽의 상세 원인은 미검증이다.
- Docker Desktop 기본 host.docker.internal 경로는 Ubuntu 서버가 루프백에 바인딩된 상태에서도 실습 본문·HTTP 200을 반환했다. getent의 IPv6 결과는 `fdc4:f303:9324::254`였으나 0.0.0.0으로 바인딩을 바꾼 뒤 마지막 curl은 HTTP 200과 실제 remote_ip `192.168.65.254`를 반환했다. 이름 조회 결과와 실제 접속 주소를 구분하며 가이드 Linux Docker Engine의 실패 예상과도 구분한다.
- 4-4 임시 Python 서버(PID 1904)는 종료했다. 사용자 출력의 ps·ss에 헤더만 남아 프로세스 및 Ubuntu 9999 리스너 부재를 확인했다. 임시 폴더 `/tmp/day04-http.fdpmdu`와 로그는 삭제 대상에 포함하지 않았다. Docker 실습 자원 정리는 위 사용자 완료 진술과 구분해 기록한다. 상세 명령·범위는 [Day 4 SESSION](../day04/SESSION.md)에 있다.

## Day 3 종료 상태 (2026-09-27)
- 사용자 출력으로 Docker Client/Engine 29.8.0, Desktop 4.92.0(240144), API 1.56 및 화면으로 lazydocker 0.25.2의 정상 작동을 확인했다. 시작 시 WSL 연동 오류가 있었으나 후속 명령 성공으로 복구를 확인했다. Windows 조작 상세는 미제공이다.
- agent:0.2.0을 python:3.12.14-slim으로 빌드했다. Python 3.12.14, 스캔 식별 OS Debian 13.7, linux/amd64, UID 10001·GID 0, 이미지 크기 181278388바이트를 확인했다.
- Trivy 0.56.2의 사용자 결과: 초기 agent:0.1.0은 HIGH 95·CRITICAL 9, 새 이미지는 HIGH 44·CRITICAL 0, --ignore-unfixed 적용 시 0건. 실제 영향 평가·예외 승인과 구분한다.
- 종료 조회로 agent:0.1.0·0.2.0 보존, 정확한 이름 agent의 컨테이너와 leak:1 이미지 부재를 확인했다. 앞서 day03/leak/x·leak.tar 제거도 확인했다. [정리 증거](../day03/evidence/cleanup-user-2026-09-27.txt).
- day03/leak의 가짜 비밀 연습 소스와 day03의 스캔 로그·trivy-cache는 삭제 대상으로 지정하지 않았다. 캐시 전체 삭제나 비밀의 복구 불가능한 삭제를 수행한 것은 아니다. 화면의 기존 koica 자원은 이번 실습 정리 대상이 아니다.
- Windows 기록과 Ubuntu 실습 폴더는 별도다. 전체 결과와 범위는 [Day 3 SESSION](../day03/SESSION.md), [반입 초안](../day03/IMPORT-PACKAGE.md)을 참고한다.

## Day 2 종료 상태 (2026-09-25)
- 실습 2-1~2-7 완료. 사용자 정리 출력으로 who1·who2·lim·demo-net 삭제 및 빈 ip netns list를 확인했다. 기존 koica 프로젝트는 정리 대상에 포함하지 않았다.
- 첫 재확인 시 세 명령이 구분자 없이 한 줄로 붙어 sysctl 옵션 오류가 발생했으나 세미콜론으로 구분해 재실행했다. 후속 사용자 출력은 `net.ipv4.ip_forward = 0`, NAT는 `-P POSTROUTING ACCEPT`만 표시, 브리지 목록은 빈 출력이었다. 사전 전달 설정 복구와 실습 NAT·브리지 제거까지 확인해 정리를 완료했다.
- 아래 2026-09-24의 실행 중 구성은 실습 당시 관찰 이력이며 현재 잔존 상태를 뜻하지 않는다. [정리 증거](../day02/evidence/day02-cleanup-user-2026-09-25.txt), [전체 기록](../day02/SESSION.md).

## Day 2 실습 당시 상태 (2026-09-24)
- 2-6 사전 조회에서 Docker 명령 네 개 모두 WSL integration 안내 오류로 실패했으나, Desktop 실행 안내 후 사용자 docker version 출력으로 Client·Engine 29.8.0, API 1.56, Desktop 4.92.0 (240144), linux/amd64, Context default 및 Client·Server 응답을 확인해 복구됐다. Windows에서 수행한 조작 상세는 미제공이다. 이후 사전 조회와 2-6 실습도 사용자 출력으로 확인했다.
- 사용자 출력으로 2-1~2-7 완료를 확인했다. Day 전체 자원 정리·자기점검은 남아 있다. Ubuntu의 biz·db 네임스페이스, br-lab(10.42.0.1/24), veth 연결 및 biz(10.42.0.10/24)·db(10.42.0.20/24)의 통신을 확인했다. biz의 기본 경로는 10.42.0.1이며 db 기본 경로는 추가하지 않았다.
- 2-7에서 lim을 --memory=64m·--rm·sleep 3600으로 실행했다. stats는 416KiB / 64MiB, 0.63%, PIDS 1이며 cgroup 상한 조회는 67108864바이트였다. 제한 값 일치를 확인했으며 OOM은 시험하지 않았다. lim은 아직 수동 정리하지 않았다.
- 2-6의 Docker 엔진 관찰에서 demo-net(172.19.0.0/16·게이트웨이 172.19.0.1), who1(172.19.0.2/16), br-0256008dc546·veth 포트 및 해당 대역 MASQUERADE를 확인했다. who1은 DNS 127.0.0.11에서 자기 이름 조회 성공, 기본 bridge의 who2는 DNS 192.168.65.7에서 NXDOMAIN이었다. who1·who2는 --rm·sleep 3600으로 실행했고 demo-net과 함께 아직 수동 정리하지 않았다. 시간 경과 시 잔존 상태를 확인한다. 기존 koica 프로젝트는 정리 대상이 아니다.
- 2-5에서 tcpdump 미검출 후 설치를 안내했고 사용자 버전 출력으로 tcpdump 4.99.4·libpcap 1.10.4·OpenSSL 3.0.13을 확인했다. db TCP 5432의 nc 리스너로 접속하며 SYN·SYN-ACK와 TCP 연결 성공을 관찰했다. 이후 캡처 작업 종료 및 리스너 PID 2129 종료·LISTEN 해제를 확인했다. 실제 PostgreSQL 서버를 설치한 것은 아니다.
- iptables 명령 미검출 후 설치를 안내했고, 후속 출력에서 v1.8.10 (nf_tables)과 규칙 조회 성공을 확인했다. apt 설치 로그는 미제공이다. nc 경로는 /usr/bin/nc다.
- 설정 전 ip_forward=0, FORWARD 기본 ACCEPT·개별 규칙 없음, NAT POSTROUTING 개별 규칙 없음을 확인했다. 이후 사용자가 ip_forward=1과 `-s 10.42.0.0/24 ! -o br-lab -j MASQUERADE` 규칙 한 개를 설정했다.
- biz에서 `nc -zv -w3 1.1.1.1 443` 성공·종료 코드 0. DNS·TLS·HTTP 및 외부 ping 성공까지 검증한 것은 아니다. Ubuntu 경로 조회는 `via 172.18.48.1 dev eth0 src 172.18.60.227`이었다.
- 실습 구성은 유지 중이다. 최종 정리 시 실습 NAT·네트워크 제거 및 ip_forward의 사전 값 0 복구를 포함한다. 영구 설정은 추가하지 않았다. Codex가 Ubuntu 설정을 직접 변경하거나 재시험하지 않았다. 상세 명령·출력은 [Day 2 SESSION](../day02/SESSION.md)에 기록했다.

## 현재 상태 — Docker Desktop 실행 후 (2026-09-23)
- Day 1의 1-3 사용자 출력으로 Ansible core 2.21.4를 `/home/user/onprem-lab/day01/.venv/bin/ansible`에서 확인했다(Python 3.12.3, Jinja 3.1.6, PyYAML 6.0.3). community.docker 5.3.0은 `/home/user/.ansible/collections/ansible_collections`에 설치돼 있다. 후속 사용자 출력에서 두 대상 연결 SUCCESS·pong, 첫 플레이북 실행 ok=5·changed=3·failed=0·unreachable=0, 두 번째 실행 ok=5·changed=0·failed=0·unreachable=0을 확인했다. 내부 별도 조회에서도 appuser UID 10001·nologin, 디렉터리 appuser:root·0750, 예시 설정 파일 root:root·0644를 확인했다. [내부 상태 증거](../day01/evidence/day01-13-state-user-2026-09-23.txt). 컨테이너 삭제와 deactivate 실행 결과는 아직 없으며 현재 실행 여부를 재조회하지 않았다.
- Day 1의 1-3 사전 확인 사용자 출력: Docker Desktop 4.92.0(240144), Docker Client/Engine 29.8.0, API 1.56(서버 최소 1.40), linux/amd64, Python 3.12.3. Ubuntu day01의 inventory.ini·prepare-vm.yaml 두 파일은 Windows 사본과 SHA-256이 일치한다. 이번에는 사용자 제공 출력이며 Codex가 Ubuntu에서 직접 재실행한 것이 아니다. [증거](../day01/evidence/day01-13-precheck-user-2026-09-23.txt).
- 후속 0-4 실습에서 lazydocker 0.23.3의 API 1.25 고정 사용과 Docker 최소 API 1.40 사이의 호환 오류를 확인했다. 사용자가 `/usr/local/bin/lazydocker`를 공식 바이너리 0.25.2(linux/amd64)로 교체한 뒤 오류 없이 이미지·네트워크 목록이 표시되는 화면을 제공했다. `agent:0.1.0`은 화면상 189.09MB이며 기본 네트워크 bridge·host·none이 모두 보인다.
- lazydocker의 실제 설치 버전은 이제 0.25.2다. 가이드와 bootstrap.sh의 0.23.3 고정값은 수정하지 않았으므로 새 환경 설치 시 동일한 호환 오류가 재발할 수 있다. `check`의 버전 출력 성공만으로 TUI 동작을 보장할 수 없다.
- 사용자가 Docker Desktop 실행을 알린 뒤 Codex가 Ubuntu에서 직접 재점검했다. `./bootstrap.sh check` 전 항목 통과, 종료 코드 0이다.
- Docker Client / Server 모두 29.8.0, Docker Compose v5.5.1, kubectl Client v1.36.1. Docker Engine은 가이드의 27 이상 조건을 충족한다.
- 가이드 고정값과의 차이는 kubectl 1.36.1 대 1.31.0, dive 0.13.1 대 본문 0.12.0, Compose 5.5.1 대 v2 표기다. check는 실제 Compose 버전에 상관없이 성공 문구를 `docker compose v2`로 출력한다. 향후 실습 호환성을 검증한 것은 아니다.
- Docker 소켓은 root:docker, 660이고 현재 사용자 그룹에 docker가 포함돼 있다. 추가 권한 변경 없이 Docker 엔진이 응답한다.
- bootstrap.sh에 지정된 이미지 12개 모두 `docker image inspect`로 직접 존재를 확인했다. 다운로드나 컨테이너 실행은 하지 않았다.
- 이전 Docker·kubectl 미검출은 Desktop 실행 후 해소됐다. 아래 초기 점검 실패는 이력으로 보존한다.

## 초기 재점검 결과 — Docker Desktop 실행 전 (2026-09-23)
- Windows 11 Pro 10.0.26200, 물리 RAM 약 31.18GiB, C: 여유 약 454.53GiB. 가이드의 PC 자원 권장치 이상이다.
- Ubuntu 24.04.1 LTS, WSL2, 커널 `5.15.167.4-microsoft-standard-WSL2`. WSL 메모리는 약 15GiB, `/`의 가상 디스크 여유 표시는 954GiB다. 실제 호스트 여유와 구분한다.
- 초기 `wsl --list --verbose`에서 Ubuntu와 docker-desktop은 모두 Stopped, VERSION 2였다. 조회를 위해 Ubuntu를 실행했다. Windows에서 Docker Desktop과 com.docker.backend 프로세스는 검출되지 않았다.
- Ubuntu의 `./bootstrap.sh check` 결과는 종료 코드 1: kubectl 미검출, Docker 데몬 연결 실패, Compose 실행 실패. Docker 줄의 ✓는 Windows 측 안내용 명령이 PATH에 있다는 뜻이며 정상 동작을 입증하지 않는다.
- `/usr/bin/docker`와 `/usr/local/bin/kubectl`은 `/mnt/wsl/docker-desktop/cli-tools/...`를 가리키지만 현재 해당 마운트 경로가 없다. `/var/run/docker.sock`도 없다. 현재 사용자 그룹에는 docker가 포함돼 있다.
- k3d v5.7.4, helm v3.16.2, k9s v0.32.5, lazydocker 0.23.3, dive 0.13.1, jq 1.7, curl 8.5.0, git 2.43.0, Python 3.12.3, iproute2 6.1.0을 직접 확인했다.
- `/home/user/onprem-lab/bootstrap.sh`는 755, LF이며 Windows 사본과 SHA-256이 일치한다. agent, day01~day13, skeleton 디렉터리도 존재한다. 전체 소스의 일치 여부까지 검사한 것은 아니다.
- 이 초기 점검에서는 엔진에 연결되지 않아 이미지 12개를 재확인하지 못했다. 이후 Desktop 실행 후 모두 확인했다(위 현재 상태 참고).
- 설치·다운로드·버전 변경·컨테이너 실행은 하지 않았다. [직접 점검 증거](../day00/evidence/local-check-2026-09-23.txt)를 참고한다.

## 실행 위치와 파일 위치
- 호스트: Windows 11 Pro, 컴퓨터 이름 DESKTOP-6KJVBND. RAM·디스크는 위 재점검 결과 참고.
- 리눅스: Ubuntu 24.04.1 LTS, WSL2, linux/amd64.
- Ubuntu 사용자: user
- 현재 실습 디렉터리: `/home/user/onprem-lab`
- 2026-09-23 사용자 제공 0-5 목록: agent, bootstrap.sh, day01~day13, skeleton 존재. Ubuntu에 day14는 없으며 Day 14 실습 시작 경로는 skeleton이다. Windows의 Day별 기록 폴더와 구분한다.
- Windows 프로젝트 디렉터리: `C:\Users\user\Desktop\Applications\25. BCG X\7. 준비\12. Deploy Practice`
- Windows 폴더와 Ubuntu 폴더는 별도 복사본이며 자동 동기화되지 않는다. 이후 코드 변경 시 어느 쪽을 수정했는지 기록하고 반영한다.
- bootstrap.sh 원본의 LAB은 `${HOME}/onprem-lab`이다. 이 프로젝트를 Windows에 배치했다고 실습 위치가 변경되지는 않는다.
- Docker Desktop은 Windows에서 실행하고 Ubuntu WSL Integration을 사용한다.

## 이전에 확인된 도구 (2026-09-22 사용자 제공 출력)
| 도구 | 실제 결과 | 비고 |
|---|---|---|
| Docker Desktop | 4.90.0 (238679) | Server 출력 |
| Docker Engine / CLI | 29.7.2 | Client와 Server 응답 |
| Docker Compose | v5.5.1 | docker compose 명령 확인 |
| kubectl | v1.36.1 | 가이드 고정값 v1.31.0과 다름; 미조정 |
| k3d | v5.7.4 | 설치 확인; 클러스터는 아직 만들지 않음 |
| helm | v3.16.2+g13654a5 | 설치 확인 |
| k9s | v0.32.5 | 설치 확인 |
| lazydocker | 0.23.3 | 설치 확인 |
| dive | 0.13.1 | 첨부 스크립트 설정과 일치, 본문의 0.12.0과 다름 |
| jq | 1.7 | 설치 확인 |
| curl | 8.5.0 | 설치 확인 |
| git | 2.43.0 | Ubuntu 출력 |
| python3 | 3.12.3 | Ubuntu 출력 |
| iproute2 | ip 명령 존재 | 버전 미기록 |

## 알려진 차이와 남은 확인
- Ansible 2.21.4의 Day 1 첫 실행에서 Python 인터프리터 자동 탐색 경고와 INJECT_FACTS_AS_VARS 변경 예고가 표시됐다. 후자는 가이드 prepare-vm.yaml의 top-level facts 참조 방식 때문이며 출력은 2.24에서 제거 예정이라고 알린다. 현재 실행은 성공했으며 향후에는 ansible_facts 사전 참조로 수정할 필요가 있다. 이번에는 동일 플레이북 재실행 확인을 위해 소스를 변경하지 않았다.
- Day 1의 1-3에서 `python3 -m venv .venv`가 ensurepip 불가로 실패했다. 이후 사용자 출력으로 `python3.12-venv` 3.12.3-1ubuntu0.17, `python3-pip-whl` 24.0+dfsg-1ubuntu1.3, `python3-setuptools-whl` 68.1.2-2ubuntu1.2 설치 완료를 확인했다. 기존 패키지 업그레이드는 없었다. 재실행 후 가상환경 생성·활성화에 성공했고 Python은 `/home/user/onprem-lab/day01/.venv/bin/python`, pip 24.0은 같은 .venv의 Python 3.12 경로를 가리켰다. ensurepip 오류 해소 확인. 후속 Ansible·community.docker 설치 버전도 사용자 출력으로 확인했다(위 현재 상태 참고). [오류·대응 기록](../day01/SESSION.md) 참고.
- check의 ✓는 고정 버전 일치나 모든 후속 실습의 호환성을 보장하지 않는다.
- kubectl 버전 차이는 해결되지 않은 항목으로 유지한다.
- 가이드의 k3s v1.30 클러스터는 아직 생성·검증하지 않았다.
- 실제 소켓 권한은 root:docker, 660이었고 user는 docker 그룹에 등록돼 있었다. newgrp docker로 현재 셸에 적용한 뒤 연결됐다.
- 실습 이미지 12개 존재는 [최종 사용자 출력](../day00/evidence/bootstrap-final.txt)에 기록했다. 이미지 바이트는 이 프로젝트 폴더로 복사하지 않았다.
- 원본 가이드의 검증 주장과 이 PC에서 실제 확인한 결과를 구분한다.
