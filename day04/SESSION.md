# Day 4 — Docker 네트워크와 진단 3단계

## 진행 상태
- 상태: Day 4 완료(2026-09-28 사용자 마무리 요청 및 자원 정리 완료 확인). 4-1~4-6·관찰은 사용자 출력·화면으로 확인했고 마지막 정리는 사용자 진술이다. 별도 자기점검 5문항 평가는 미진행이다.
- 완료한 범위: 4-1 사전 조회·lab-net 및 web·client 생성·사용자 정의 네트워크의 이름 해석과 HTTP 통신·기본 bridge의 이름 해석 실패 비교(사용자 출력 확인).
- 추가 완료 범위: 4-2에서 isolated의 lab-net 연결 전 이름 해석 실패와 연결 후 DNS·HTTP 성공, 양쪽 네트워크 소속 및 인터페이스 확인(사용자 출력).
- 추가 완료 범위: 4-3 포트 게시 및 바인딩 주소별 접근 비교, 게시 없는 client→web:80 통신 확인(사용자 출력).
- 추가 완료 범위: 4-4 localhost·호스트 이름·Ubuntu IP 경로 비교, 바인딩 변경 효과 확인, 호스트 이름 재접속 및 임시 Python 서버 종료. 직접 IP 시간 초과의 세부 원인 해결은 완료 범위에 포함하지 않는다.
- 추가 완료 범위: 4-5 정상 DNS·TCP·HTTP 진단, 연결 거절·시간 초과 비교, IP·네트워크 소속·라우팅·일회용 진단 컨테이너 확인.
- 추가 완료 범위: 4-6 예시 DNS 서버·검색 접미사의 설정 전달 및 /etc/hosts의 정적 이름·IP 등록 확인. 실제 사내 DNS·ERP 연결 검증은 수행하지 않음.
- 추가 완료 범위: lazydocker lab-net·other-net 화면 관찰 및 Docker inspect 대조. TUI에서 연결 목록·서브넷이 표시된 것으로 기록하지 않음.
- 종료 지점: 개념 질의응답 및 자원 정리 완료 확인 후 기록·PR 정리. 삭제 후 목록·포트 출력 원문은 미제공이며 Python 서버 종료는 앞선 출력으로 확인했다.
- Codex 작업: 아직 별도 작업을 만들지 않음
- 실행 증거 기준: 사용자 제공 출력과 직접 검증 결과를 구분해 기록

## 목표와 이번 세션 범위
4-1~4-6, lazydocker 관찰, 개념 질의응답을 진행한 뒤 사용자가 Day 4 마무리와 PR 생성을 요청했다. 실습 명령은 사용자가 Ubuntu WSL2에서 실행했으며 Codex는 Windows 기록을 정리한다. 예시 주소를 실제 사내 DNS로 취급하지 않으며 Docker 데몬 전체 설정·koica 자원은 변경하지 않는다. 아래의 미실행·남은 범위 표시는 각 단계 당시 상태이며 최종 상태는 상단과 종료 기록을 기준으로 한다.

## 실행 기록
### 2026-09-27 — 4-1 사전 상태 확인
- 실행 위치: Ubuntu WSL2, `/home/user/onprem-lab`.
- 실행 명령: `cd /home/user/onprem-lab`, `docker version`, `docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Networks}}'`, `docker network ls`.
- 주요 출력: Docker Client/Engine 29.8.0, API 1.56, Docker Desktop 4.92.0(240144), linux/amd64, Context default. Client와 Server 모두 응답했다.
- 컨테이너 목록: `koica-oda-local-test-oda-app-1` 한 개, `Exited (143) 2 weeks ago`, 네트워크 `koica-oda-local-test_default`.
- 네트워크 목록: `bridge`, `host`, `koica-oda-local-test_default`, `none`.
- 결과와 의미: `web`, `client`, `web2`, `client2`, `lab-net` 이름 충돌 없음. 기존 koica 자원은 실습 변경 대상이 아니다. 포트 점유·이미지 존재·Ubuntu 파일 동기화 여부는 이번 조회로 확인하지 않았다.
- 확인 주체: 사용자 제공 출력. Codex는 Ubuntu 명령을 직접 실행하지 않고 Windows 기록만 갱신했다.
- 다음 안내: `docker network create lab-net`과 생성 결과 조회. 후속 결과는 아래 기록에 보존한다.

### 2026-09-27 — 4-1 사용자 정의 네트워크 생성
- 실행 위치: Ubuntu WSL2, `/home/user/onprem-lab`.
- 실행 명령: `docker network create lab-net`, `docker network inspect lab-net`.
- 주요 출력: ID `abd283b8f29023b88f182d04ee523e646bac3c69689bd468dfe8826d875410ac`, Driver `bridge`, Scope `local`, Subnet `172.19.0.0/16`, Gateway `172.19.0.1`, Containers `{}`. IPv4 활성·IPv6 비활성.
- 결과와 의미: 네트워크 생성 성공. 연결된 컨테이너는 아직 없으며 가이드 예시와 다른 자동 할당 대역은 오류가 아니다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내: nginx의 web과 netshoot의 client를 lab-net에 생성하고 상태 조회. 후속 생성 결과는 아래 기록에 보존한다.

### 2026-09-27 — 4-1 web·client 생성
- 실행 위치: Ubuntu WSL2, `/home/user/onprem-lab`.
- 실행 명령: `docker run -d --name web --network lab-net nginx:1.27-alpine`, `docker run -d --name client --network lab-net nicolaka/netshoot:v0.13 sleep 3600`, `docker ps --filter network=lab-net --format 'table {{.Names}}\t{{.Status}}\t{{.Networks}}'`.
- 주요 출력: web ID 앞자리 `19cc53c0ad10`, client ID 앞자리 `06e486cef5a7`. 두 컨테이너 모두 `Up Less than a second`, 네트워크 `lab-net`.
- 결과와 의미: 컨테이너 생성·실행 및 동일 네트워크 소속 확인. DNS·HTTP 통신 성공은 아직 검증하지 않았다. client는 sleep 3600 종료 후 중지될 수 있다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내: `docker exec client nslookup web`, `docker exec client curl -sS -m5 -o /dev/null -w 'HTTP 상태 코드: %{http_code}\n' http://web`. 후속 결과는 아래 기록에 보존한다.

### 2026-09-27 — 4-1 사용자 정의 네트워크의 이름 해석·HTTP 통신
- 실행 위치: Ubuntu WSL2, `/home/user/onprem-lab`에서 docker exec로 client 내부 명령 실행.
- 실행 명령: `docker exec client nslookup web`, `docker exec client curl -sS -m5 -o /dev/null -w 'HTTP 상태 코드: %{http_code}\n' http://web`.
- 주요 출력: DNS Server `127.0.0.11`, Address `127.0.0.11#53`, web의 Address `172.19.0.2`, HTTP 상태 코드 `200`.
- 결과와 의미: client에서 web 이름 해석과 HTTP 응답 성공. 호스트 포트 게시 없이 같은 사용자 정의 네트워크에서 통신했다. 기본 bridge와의 비교는 아직 미진행이다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내: --network 옵션 없이 web2·client2를 생성하여 기본 bridge에서 동일한 이름 통신을 비교한다. 후속 결과는 아래 기록에 보존한다.

### 2026-09-27 — 4-1 기본 bridge 비교 및 절 완료
- 실행 위치: Ubuntu WSL2, `/home/user/onprem-lab`.
- 실행 명령: `docker run -d --name web2 nginx:1.27-alpine`, `docker run -d --name client2 nicolaka/netshoot:v0.13 sleep 3600`, `docker exec client2 nslookup web2`, `docker exec client2 curl -sS -m3 http://web2`, 직후 `echo "종료코드=$?"`.
- 주요 출력: web2 ID 앞자리 `e05409509c5f`, client2 ID 앞자리 `7a8a66ed1db6`. nslookup은 DNS `192.168.65.7#53`에서 `server can't find web2: NXDOMAIN`. curl은 `(28) Resolving timed out after 3018 milliseconds`, 종료코드 `28`.
- 결과와 의미: 기본 bridge에서 web2 이름 해석 실패를 확인했다. 사용자 정의 lab-net의 이름 해석·HTTP 200과 비교하여 4-1 목표 달성. curl은 가이드 예상 코드 6 대신 이름 해석 단계에서 제한 시간 3초에 도달해 코드 28을 반환했다. HTTP 서버나 TCP 포트의 응답 시간 초과를 입증한 것이 아니며 DNS 지연의 상세 원인은 조사하지 않았다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 남은 자원: lab-net, web·client·web2·client2를 생성했고 정리 명령은 아직 실행하지 않았다. client·client2는 sleep 3600 종료 후 중지될 수 있으므로 재개 시 상태 확인이 필요하다.
- 완료 범위: 4-1만 완료. 4-2 이후와 Day 전체 정리·자기점검은 미진행.

### 2026-09-27 — 4-2 시작 안내(미실행)
- 사용자 요청: 다음 실습으로 진행.
- 안내할 위치: Ubuntu WSL2, `/home/user/onprem-lab`.
- 안내 명령: `docker network create other-net`, `docker run -d --name isolated --network other-net nicolaka/netshoot:v0.13 sleep 3600`, `docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Networks}}'`, `docker exec isolated curl -sS -m3 http://web`, 직후 `echo "종료코드=$?"`.
- 목적: web 실행 상태와 네트워크 소속을 조회하고 lab-net 연결 전 isolated의 이름 통신 결과 확인.
- 실행 여부: 안내 당시에는 미실행. 후속 사용자 결과는 아래에 기록한다.

### 2026-09-27 — 4-2 다른 네트워크에서 이름 해석 실패 확인
- 실행 위치: Ubuntu WSL2, `/home/user/onprem-lab`.
- 실행 명령: 위 4-2 첫 단계 안내의 다섯 명령을 사용자가 실행했다.
- 주요 출력: other-net ID 앞자리 `8963d62bb2c3`, isolated ID 앞자리 `70fda45f2410`. isolated는 Up·other-net, web·client는 Up·lab-net, web2·client2는 Up·bridge. curl은 `(6) Could not resolve host: web`, 종료코드 `6`.
- 결과와 의미: isolated와 web은 공통 네트워크가 없으며 web 이름 해석에 실패했다. 이번 결과는 이름으로 하는 접근 실패를 확인한 것이고, IP 직접 접근의 차단까지 시험한 것은 아니다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내: lab-net 추가 연결 후 비교. 후속 실행 명령과 결과는 아래 기록에 보존한다.

### 2026-09-27 — 4-2 양쪽 네트워크 연결 및 절 완료
- 실행 위치: Ubuntu WSL2, `/home/user/onprem-lab`.
- 실행 명령: `docker network connect lab-net isolated`, `docker exec isolated nslookup web`, `docker exec isolated curl -sS -m5 -o /dev/null -w 'HTTP 상태 코드: %{http_code}\n' http://web`, `docker exec isolated ip -brief addr`, `docker inspect isolated --format '{{json .NetworkSettings.Networks}}'`.
- 주요 출력: DNS `127.0.0.11#53`에서 web → `172.19.0.2`, HTTP `200`. isolated의 eth0@if12는 UP·`172.20.0.2/16`, eth1@if13은 UP·`172.19.0.4/16`.
- inspect 대조: other-net의 IP `172.20.0.2`, 게이트웨이 `172.20.0.1`; lab-net의 IP `172.19.0.4`, 게이트웨이 `172.19.0.1`. 기존 other-net 연결도 유지됐다.
- 결과와 의미: lab-net 추가 연결 후 web 이름 해석·HTTP 통신 성공. 컨테이너 한 개가 네트워크 두 개에 동시에 소속됨을 확인했다. 두 네트워크의 다른 컨테이너 사이를 isolated가 자동 중계한다는 의미는 아니며 중계는 시험하지 않았다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 완료 범위: 4-2 완료, 4-3 이후 미진행. lab-net·other-net과 web·client·web2·client2·isolated는 정리하지 않았다. sleep 3600 컨테이너는 재개 시 실행 상태를 확인한다.

### 2026-09-27 — 4-3 사전 조회 안내(결과 대기)
- 사용자 요청: 다음 실습으로 진행.
- Ubuntu 안내: `docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'`, `ss -ltn '( sport = :8080 or sport = :8081 )'`.
- Windows PowerShell 안내: `Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 8080,8081 } | Select-Object LocalAddress,LocalPort,OwningProcess`.
- 목적: pub·pub2 이름 충돌 및 Ubuntu·Windows의 8080·8081 리스너 확인. Docker Desktop 환경이므로 Ubuntu ss 출력만으로 Windows 포트 상태를 판단하지 않는다.
- 실행 여부: 안내 당시 미실행. 후속 사용자 결과는 아래 기록에 보존한다.

### 2026-09-27 — 4-3 사전 조회 결과 확인
- 실행 위치·명령: 위 사전 조회 명령을 Ubuntu WSL2와 Windows PowerShell에서 사용자가 각각 실행했다.
- Ubuntu 주요 출력: isolated·client2·web2·client·web은 Up, 기존 koica 컨테이너는 Exited. pub·pub2는 목록에 없음. web·web2의 PORTS는 `80/tcp`이고 호스트 포트 매핑 표시는 없음. ss는 헤더만 출력했다.
- Windows 주요 출력: Get-NetTCPConnection 조회 후 결과 행 없이 PowerShell 프롬프트 복귀. 명령에 ErrorAction SilentlyContinue가 있으므로 숨겨진 오류 여부까지 별도로 검증한 것은 아니다.
- 결과와 의미: pub·pub2 이름 충돌 없음, Ubuntu 및 Windows의 해당 조회에서 8080·8081 리스너가 표시되지 않음. 생성 시 실제 포트 바인딩 성공 여부는 후속 출력으로 확인한다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내: pub·pub2 생성 및 게시 주소 조회. 후속 명령과 결과는 아래에 기록한다.

### 2026-09-27 — 4-3 pub·pub2 생성 및 포트 게시 확인
- 실행 위치: Ubuntu WSL2, `/home/user/onprem-lab`.
- 실행 명령: `docker run -d --name pub -p 127.0.0.1:8080:80 nginx:1.27-alpine`, `docker run -d --name pub2 -p 8081:80 nginx:1.27-alpine`, `docker port pub`, `docker port pub2`.
- 주요 출력: pub ID 앞자리 `6f416749b272`, pub2 ID 앞자리 `35501b075e91`. pub은 `80/tcp -> 127.0.0.1:8080`; pub2는 `80/tcp -> 0.0.0.0:8081` 및 `80/tcp -> [::]:8081`.
- 결과와 의미: 컨테이너 생성과 설정된 포트 매핑 확인. 실제 HTTP 응답 및 비루프백 주소 접근 차이는 아직 검증하지 않았다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내(미실행): Ubuntu에서 `curl --noproxy '*' -sS -m5 -o /dev/null -w '8080 HTTP: %{http_code}\n' http://127.0.0.1:8080`, `curl --noproxy '*' -sS -m5 -o /dev/null -w '8081 HTTP: %{http_code}\n' http://127.0.0.1:8081`, `ss -ltn '( sport = :8080 or sport = :8081 )'`. 프록시를 경유하지 않는 로컬 요청으로 관찰한다.

### 2026-09-28 — 4-3 Ubuntu 루프백 HTTP·리스너 확인
- 실행 위치: Ubuntu WSL2, `/home/user/onprem-lab`.
- 실행 명령: `curl --noproxy '*' -sS -m5 -o /dev/null -w '8080 HTTP: %{http_code}\n' http://127.0.0.1:8080`, `curl --noproxy '*' -sS -m5 -o /dev/null -w '8081 HTTP: %{http_code}\n' http://127.0.0.1:8081`, `ss -ltn '( sport = :8080 or sport = :8081 )'`.
- 주요 출력: `8080 HTTP: 200`, `8081 HTTP: 200`. ss는 `127.0.0.1:8080`과 `*:8081`이 모두 LISTEN임을 표시했다.
- 결과와 의미: Ubuntu 루프백에서 두 게시 포트 모두 HTTP 응답 성공. 이 환경에서는 Ubuntu ss에도 리스너 주소 차이가 보인다. 프로세스 이름·PID는 이번 명령으로 확인하지 않았다. 비루프백 접근 및 다른 PC에서의 접근은 아직 미검증이다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내(미실행): Ubuntu의 `hostname -I`에서 첫 IP를 LAB_IP로 선택해 값을 출력하고, 그 주소의 8080·8081에 프록시 없이 제한 시간 3초의 curl 요청을 각각 보내 종료코드까지 비교한다. 선택한 주소는 Ubuntu 주소이며 Windows 호스트 주소로 간주하지 않는다. 이번 ss 관찰에 따라 먼저 Ubuntu에서 주소 차이를 비교하고 필요 시 Windows 관찰을 추가한다.

### 2026-09-28 — 4-3 Ubuntu 비루프백 주소 접근 비교
- 실행 위치: Ubuntu WSL2, `/home/user/onprem-lab`.
- 실행 명령: `LAB_IP=$(hostname -I | awk '{print $1}')`, `echo "테스트할 Ubuntu IP: $LAB_IP"`, `curl --noproxy '*' -sS -m3 -o /dev/null -w '8080 HTTP: %{http_code}\n' "http://${LAB_IP}:8080"`, 직후 `echo "8080 종료코드=$?"`, `curl --noproxy '*' -sS -m3 -o /dev/null -w '8081 HTTP: %{http_code}\n' "http://${LAB_IP}:8081"`, 직후 `echo "8081 종료코드=$?"`.
- 주요 출력: Ubuntu IP `172.18.60.227`. 8080은 `curl: (7) Failed to connect ... after 0 ms`, HTTP `000`, 종료코드 `7`. 8081은 HTTP `200`, 종료코드 `0`.
- 결과와 의미: 같은 Ubuntu에서 루프백으로는 두 포트 모두 성공했으나 비루프백 주소로는 8080 연결 실패·8081 성공. ss 및 docker port에서 확인한 바인딩 주소 차이와 일치한다. HTTP 000은 서버가 보낸 상태 코드가 아니라 HTTP 응답을 받지 못했음을 나타낸다. 다른 PC에서의 접근 및 Windows 호스트 주소 접근을 시험한 것은 아니다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내(미실행): `docker port web`, `docker exec client curl --noproxy '*' -sS -m5 -o /dev/null -w 'client -> web:80 HTTP: %{http_code}\n' http://web:80`. 포트 게시 없는 컨테이너 간 통신을 재확인한다.

### 2026-09-28 — 4-3 게시 없는 통신 재확인 및 절 완료
- 실행 위치: Ubuntu WSL2, `/home/user/onprem-lab`.
- 실행 명령: `docker port web`, `docker exec client curl --noproxy '*' -sS -m5 -o /dev/null -w 'client -> web:80 HTTP: %{http_code}\n' http://web:80`.
- 주요 출력: docker port web은 출력 없음. curl은 `client -> web:80 HTTP: 200`.
- 결과와 의미: web에 게시된 호스트 포트 없이 같은 lab-net의 client가 web의 80번 포트로 HTTP 통신함을 재확인했다. 앞선 바인딩 주소 비교와 함께 4-3 완료.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 범위와 잔존 자원: 4-1~4-3 완료, 4-4 이후 미진행. lab-net·other-net 및 web·client·web2·client2·isolated·pub·pub2는 정리하지 않았다. 각 컨테이너의 현재 실행 여부를 모두 재조회한 것은 아니며 sleep 3600 대상은 시간이 지나면 중지될 수 있다.

### 2026-09-28 — 4-4 사전 조회 안내(미실행)
- 사용자 요청: 다음 실습으로 진행.
- Ubuntu 안내: `python3 --version`, `hostname -I`, `ss -ltn '( sport = :9999 )'`.
- Windows PowerShell 안내: `Get-NetTCPConnection -State Listen | Where-Object { $_.LocalPort -eq 9999 } | Select-Object LocalAddress,LocalPort,OwningProcess`.
- 실행 여부: 안내 당시 미실행. 후속 사용자 결과는 아래 기록에 보존한다.
- 환경 검토: 가이드 4-4의 검증 환경은 Linux Docker Engine이다. Docker Desktop 공식 문서는 host.docker.internal을 호스트 내부 IP로 설명하고 WSL 공식 문서는 NAT·mirrored 및 Windows→WSL localhost 경로를 구분한다. 따라서 Docker Desktop의 host.docker.internal을 Ubuntu IP와 같다고 가정하거나 가이드의 실패·성공을 그대로 보장하지 않는다. 서비스는 Ubuntu에 두고 실제 대상 주소·접근 결과를 구분해 진행한다.
- 참고: https://docs.docker.com/desktop/features/networking/networking-how-tos/ 및 https://learn.microsoft.com/en-us/windows/wsl/networking (2026-09-28 Codex 문서 조회).
- 후속 실행 계획: 포트 조회 후 전용 임시 디렉터리에서 HTTP 서버를 실행하고 PID를 별도 변수로 보존하여 해당 프로세스만 종료한다. 프로젝트 루트를 HTTP 디렉터리로 제공하거나 kill %1·광범위한 pkill을 사용하지 않는다. 아직 이 명령들은 안내·실행하지 않았다.

### 2026-09-28 — 4-4 사전 조회 결과 확인
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab` 및 Windows PowerShell.
- 실행 명령: 위 사전 조회의 Python 버전·Ubuntu IP·Ubuntu/Windows 9999 리스너 조회 명령.
- 주요 출력: Python `3.12.3`, Ubuntu IP `172.18.60.227`. Ubuntu ss는 헤더만 표시, Windows Get-NetTCPConnection 필터 결과는 출력 없이 프롬프트 복귀.
- 결과와 의미: 두 조회에서 9999 포트 리스너가 표시되지 않았으며 Python으로 임시 서버를 실행할 준비를 확인했다. 서버가 실제로 시작했는지는 아직 미검증이다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내(미실행): Ubuntu에서 `LAB_HTTP_DIR=$(mktemp -d /tmp/day04-http.XXXXXX)`로 전용 디렉터리를 만들고 index.html에 `day04 host server`를 기록한다. `python3 -m http.server 9999 --bind 127.0.0.1 --directory "$LAB_HTTP_DIR" >"$LAB_HTTP_DIR/server.log" 2>&1 &` 후 `LAB_HTTP_PID=$!`로 PID를 보존한다. 1초 대기 후 PID·디렉터리 출력, `ps -p "$LAB_HTTP_PID" -o pid,args`, 루프백 curl의 본문·HTTP 상태를 확인한다. 이 변수들을 사용할 수 있도록 같은 Ubuntu 터미널을 유지한다.

### 2026-09-28 — 4-4 Ubuntu 루프백 서버 실행 및 응답 확인
- 실행 위치: Ubuntu WSL2, `/home/user/onprem-lab`.
- 실행 명령: `LAB_HTTP_DIR=$(mktemp -d /tmp/day04-http.XXXXXX)`, `printf 'day04 host server\n' > "$LAB_HTTP_DIR/index.html"`, `python3 -m http.server 9999 --bind 127.0.0.1 --directory "$LAB_HTTP_DIR" >"$LAB_HTTP_DIR/server.log" 2>&1 &`, `LAB_HTTP_PID=$!`, 1초 대기 후 PID·임시 경로 출력 및 `ps -p "$LAB_HTTP_PID" -o pid,args`, `curl --noproxy '*' -sS -m3 -w '\nHTTP: %{http_code}\n' http://127.0.0.1:9999`.
- 주요 출력: 백그라운드 작업 `[1] 1827`, PID `1827`, 디렉터리 `/tmp/day04-http.fdpmdu`. ps에서 Python http.server의 127.0.0.1 바인딩과 해당 디렉터리를 확인했다. 응답 본문 `day04 host server`, HTTP `200`.
- 결과와 의미: Ubuntu에서 서버 실행 및 루프백 HTTP 응답 성공. 이 결과만으로 Windows·컨테이너에서 접근 가능한지는 알 수 없다. 직전 안내의 'Ubuntu 안에서만 접근' 표현은 바인딩 의도를 설명한 것으로, WSL localhost 전달까지 포함한 접근 범위를 검증한 것은 아니다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 남은 자원: PID 1827 서버와 임시 디렉터리 유지. 같은 터미널의 LAB_HTTP_PID·LAB_HTTP_DIR 변수를 후속 바인딩 변경 및 정확한 종료에 사용한다.
- 다음 안내(미실행): `docker run --rm nicolaka/netshoot:v0.13 curl --noproxy '*' -sS -m3 -w '\n컨테이너 localhost HTTP: %{http_code}\n' http://127.0.0.1:9999`, 직후 `echo "종료코드=$?"`. 일회용 컨테이너의 localhost 요청과 Ubuntu의 성공 결과를 비교한다.

### 2026-09-28 — 4-4 컨테이너 localhost 접근 실패 확인
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`에서 일회용 netshoot 컨테이너 실행.
- 실행 명령: `docker run --rm nicolaka/netshoot:v0.13 curl --noproxy '*' -sS -m3 -w '\n컨테이너 localhost HTTP: %{http_code}\n' http://127.0.0.1:9999`, 직후 `echo "종료코드=$?"`.
- 주요 출력: `curl: (7) Failed to connect to 127.0.0.1 port 9999 after 0 ms`, HTTP `000`, 종료코드 `7`.
- 결과와 의미: Ubuntu 루프백 요청의 HTTP 200과 달리 컨테이너 루프백에서는 연결 실패. 컨테이너의 127.0.0.1은 컨테이너 자신이므로 Ubuntu의 Python 서버를 가리키지 않는다. HTTP 000은 서버 응답이 아님.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님. 진단 컨테이너는 --rm으로 실행했으며 별도 삭제 목록 조회는 하지 않았다.
- 다음 안내(미실행): 기본 제공 DNS를 유지하여 일회용 netshoot 안에서 `getent hosts host.docker.internal` 및 프록시 없는 `http://host.docker.internal:9999` curl 요청(3초 제한, 본문·HTTP 상태 출력)을 실행하고 종료코드를 확인한다. --add-host로 이름을 덮어쓰지 않는다. 성공 여부는 Docker Desktop·WSL 경로에 따라 관찰하며 결과를 미리 확정하지 않는다.

### 2026-09-28 — 4-4 host.docker.internal 접근 성공(가이드와 차이)
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`에서 일회용 netshoot 컨테이너 실행.
- 실행 명령: `docker run --rm nicolaka/netshoot:v0.13 sh -c 'getent hosts host.docker.internal; curl --noproxy "*" -sS -m3 -w "\n호스트 이름 HTTP: %{http_code}\n" http://host.docker.internal:9999'`, 직후 `echo "종료코드=$?"`.
- 주요 출력: getent는 `fdc4:f303:9324::254 host.docker.internal host.docker.internal`. curl 본문은 `day04 host server`, HTTP `200`, 종료코드 `0`.
- 결과와 의미: Ubuntu 서버의 바인딩을 바꾸지 않았는데 Docker Desktop의 기본 host.docker.internal 경로로 실습 서버 응답을 받았다. 가이드 Linux Docker Engine의 루프백 바인딩 상태 실패 예측과 다르다. getent의 IPv6 결과만으로 curl이 실제 사용한 주소·프로토콜이나 정확한 전달 경로를 확정하지 않는다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내(미실행): Ubuntu에서 LAB_WSL_IP를 hostname -I의 첫 주소로 지정하고 `ss -ltn '( sport = :9999 )'`로 바인딩을 재확인한다. 일회용 netshoot에서 해당 IPv4 주소의 9999로 프록시 없는 curl 요청을 보내 본문·HTTP 상태·종료코드를 비교한다. 실패 시 바인딩뿐 아니라 경로·대역 충돌 가능성도 구분하며 아직 원인을 확정하지 않는다.

### 2026-09-28 — 4-4 Ubuntu IP 직접 접근 시간 초과
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`에서 조회 및 일회용 netshoot 실행.
- 실행 명령: `LAB_WSL_IP=$(hostname -I | awk '{print $1}')`, IP 출력, `ss -ltn '( sport = :9999 )'`, `docker run --rm nicolaka/netshoot:v0.13 curl --noproxy '*' -sS -m3 -w '\nUbuntu IP HTTP: %{http_code}\n' "http://${LAB_WSL_IP}:9999"`, 직후 종료코드 출력.
- 주요 출력: Ubuntu IP `172.18.60.227`, ss는 `127.0.0.1:9999` LISTEN. curl은 `(28) Connection timed out after 3003 milliseconds`, HTTP `000`, 종료코드 `28`.
- 결과와 의미: 호스트 이름 경로의 성공과 달리 Ubuntu IP 직접 요청은 연결 단계에서 시간 초과. IP 리터럴이므로 앞선 4-1의 Resolving timed out과 구분한다. 서버의 루프백 바인딩은 확인했지만 시간 초과 원인을 바인딩만으로 확정하지 않는다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내(미실행): 같은 Ubuntu에서 `curl --noproxy '*' -sS -m3 -w '\nUbuntu 자체 요청 HTTP: %{http_code}\n' "http://${LAB_WSL_IP}:9999"`와 종료코드 확인. 이어 `docker network inspect bridge koica-oda-local-test_default lab-net other-net --format '{{.Name}}: {{range .IPAM.Config}}{{.Subnet}} {{end}}'`로 Ubuntu IP와 Docker 서브넷의 겹침 여부를 조회한다. 기존 koica 네트워크는 조회만 하며 변경하지 않는다.

### 2026-09-28 — 4-4 Ubuntu 자체 요청 및 Docker 대역 겹침 확인
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`.
- 실행 명령: `curl --noproxy '*' -sS -m3 -w '\nUbuntu 자체 요청 HTTP: %{http_code}\n' "http://${LAB_WSL_IP}:9999"`, 직후 종료코드 출력. `docker network inspect bridge koica-oda-local-test_default lab-net other-net --format '{{.Name}}: {{range .IPAM.Config}}{{.Subnet}} {{end}}'`.
- 주요 출력: Ubuntu 자체 요청은 172.18.60.227:9999 연결 실패(0 ms), HTTP 000, 코드 7. Docker 대역은 bridge 172.17.0.0/16, koica-oda-local-test_default 172.18.0.0/16, lab-net 172.19.0.0/16, other-net 172.20.0.0/16.
- 결과와 의미: Ubuntu IP 172.18.60.227이 koica Docker 대역 172.18.0.0/16에 포함됨을 확인했다. 컨테이너 직접 접근 시간 초과에 영향을 줄 수 있는 경로 충돌 후보이며 패킷 경로까지 검증한 것은 아니다. Ubuntu 자체 요청의 즉시 실패는 현재 루프백 전용 리스너와 일치한다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님. koica 자원은 조회만 했으며 수정·삭제하지 않았다.
- 다음 안내(미실행): 같은 터미널에서 LAB_HTTP_PID의 서버를 kill·wait로 종료하고 기존 LAB_HTTP_DIR을 사용해 Python 서버를 --bind 0.0.0.0으로 재실행한다. 새 PID를 저장·출력하고 ss를 조회한다. Ubuntu 자체 IP 요청과 일회용 netshoot의 같은 IP 요청을 각각 비교한다. 컨테이너 요청 성공을 미리 보장하지 않으며 기존 Docker 네트워크는 유지한다.

### 2026-09-28 — 4-4 바인딩 변경 및 직접 IP 경로 비교
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`.
- 실행 명령: 기존 LAB_HTTP_PID에 kill·wait 후, `python3 -m http.server 9999 --bind 0.0.0.0 --directory "$LAB_HTTP_DIR" >>"$LAB_HTTP_DIR/server.log" 2>&1 &`, `LAB_HTTP_PID=$!`, 1초 대기·PID 출력·ss 조회. Ubuntu 자체 및 일회용 netshoot에서 같은 `http://${LAB_WSL_IP}:9999`로 --noproxy·3초 제한 curl을 실행하고 종료코드를 각각 출력했다.
- 주요 출력: 새 PID `1904`, ss는 `0.0.0.0:9999` LISTEN. Ubuntu 자체 요청은 본문 `day04 host server`, HTTP 200·코드 0. 컨테이너 직접 IP 요청은 Connection timed out after 3009 milliseconds, HTTP 000·코드 28.
- 결과와 의미: 바인딩 변경으로 Ubuntu 자체 비루프백 요청은 실패에서 성공으로 바뀌었다. 컨테이너 직접 IP 경로의 시간 초과는 유지되어 루프백 바인딩만의 문제로 설명할 수 없다. 확인된 대역 겹침은 경로 충돌 후보이며 세부 패킷 경로·방화벽까지 검증하지 않았다. 기존 koica 자원은 변경하지 않는다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내(미실행): 일회용 netshoot에서 host.docker.internal:9999로 재요청하며 본문·HTTP·remote_ip·종료코드를 확인한다. 그 후 같은 터미널에서 LAB_HTTP_PID(1904)를 kill·wait하고 ps 및 ss로 종료를 확인한다. 임시 폴더 /tmp/day04-http.fdpmdu와 로그는 유지한다.

### 2026-09-28 — 4-4 호스트 이름 재확인·서버 종료 및 절 완료
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`.
- 실행 명령: `docker run --rm nicolaka/netshoot:v0.13 curl --noproxy '*' -sS -m3 -w '\nHTTP: %{http_code}, 접속 IP: %{remote_ip}\n' http://host.docker.internal:9999`, 직후 종료코드 출력. 이어 `kill "$LAB_HTTP_PID"`, `wait "$LAB_HTTP_PID" 2>/dev/null`, `ps -p "$LAB_HTTP_PID" -o pid,args`, `ss -ltn '( sport = :9999 )'`.
- 주요 출력: 본문 `day04 host server`, HTTP `200`, remote_ip `192.168.65.254`, 종료코드 `0`. 종료 후 ps와 ss는 각각 헤더만 표시했다.
- 결과와 의미: 0.0.0.0 바인딩에서도 Docker Desktop 호스트 이름 경로가 성공했으며 이번 curl의 실제 접속 주소는 IPv4 192.168.65.254로 확인했다. 이전 getent IPv6 출력과 실제 HTTP 접속 주소를 구분한다. PID 1904의 프로세스 부재 및 Ubuntu 9999 리스너 부재로 임시 서버 종료를 확인했다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 완료 판단: 4-4의 localhost 의미·바인딩 차이·호스트 접근을 실제 환경에서 비교하고 가이드와의 차이를 기록하여 절 완료. 컨테이너→Ubuntu IP 직접 경로는 여전히 시간 초과였으며 대역 겹침은 확인했지만 세부 원인 규명·해결은 미완료다. koica 자원은 변경하지 않았다.
- 남은 자원: 임시 폴더 /tmp/day04-http.fdpmdu와 로그 유지. lab-net·other-net과 기존 실습 컨테이너는 아직 Day 전체 정리를 하지 않았다. 4-5 이후와 Day 자기점검은 미진행이다.

### 2026-09-28 — 4-5 시작 안내(미실행)
- 사용자 요청: 다음 실습으로 진행.
- 실행할 위치: Ubuntu WSL2 `/home/user/onprem-lab`.
- 안내 명령: `docker inspect client web --format '{{.Name}}: {{.State.Status}}'`.
- 목적: sleep 3600으로 실행한 client의 만료 여부와 web 상태를 확인한 뒤 기존 lab-net에서 nslookup→nc→curl을 단계별로 실행한다.
- 실행 여부: 안내만 했으며 결과는 아직 받지 않았다. 진단 명령·재시작은 아직 실행하지 않았다.
- 자료 검토: 가이드 4-5와 diag3.sh를 읽었다. 먼저 개별 명령의 의미를 확인하며 TCP 연결 성공과 HTTP 응답 성공을 구분한다. 연결 거절·시간 초과만으로 특정 담당자나 상세 원인을 확정하지 않는다.

### 2026-09-28 — 4-5 사전 조회: client 중지 확인
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`.
- 실행 명령: `docker inspect client web --format '{{.Name}}: {{.State.Status}}'`.
- 주요 출력: `/client: exited`, `/web: running`.
- 결과와 의미: client가 중지되어 docker exec 전에 재시작이 필요하다. 초기 명령은 sleep 3600이지만 이번 출력에는 종료코드·시각이 없어 중지 원인까지 확정하지 않는다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내(미실행): `docker start client`, `docker inspect client --format '{{.Name}}: {{.State.Status}}'`, `docker exec client nslookup web`. 기존 컨테이너를 재사용하고 이름 해석부터 확인한다.

### 2026-09-28 — 4-5 client 재시작 및 1단계 이름 해석 확인
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`.
- 실행 명령: `docker start client`, `docker inspect client --format '{{.Name}}: {{.State.Status}}'`, `docker exec client nslookup web`.
- 주요 출력: `client`, `/client: running`. DNS `127.0.0.11#53`에서 web → `172.19.0.2`.
- 결과와 의미: 기존 client 재시작과 1단계 이름 해석 성공. 이번 단계에서 TCP 연결·HTTP 응답까지 확인한 것은 아니다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내(미실행): `docker exec client nc -zv -w3 web 80`, 직후 `echo "종료코드=$?"`. TCP 연결 가능 여부를 확인한다.

### 2026-09-28 — 4-5 2단계 TCP 연결 확인
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`에서 client 내부 명령 실행.
- 실행 명령: `docker exec client nc -zv -w3 web 80`, 직후 `echo "종료코드=$?"`.
- 주요 출력: `Connection to web (172.19.0.2) 80 port [tcp/http] succeeded!`, 종료코드 `0`.
- 결과와 의미: client에서 web의 TCP 80번 포트 연결 성공. nc의 tcp/http 표시는 포트 이름이며 HTTP 요청·응답을 검증한 것은 아니다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내(미실행): `docker exec client curl --noproxy '*' -sv -m5 http://web/ -o /dev/null`, 직후 `echo "종료코드=$?"`. 연결 로그와 HTTP 상태 줄을 확인한다.

### 2026-09-28 — 4-5 3단계 HTTP 응답 확인
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`에서 client 내부 명령 실행.
- 실행 명령: `docker exec client curl --noproxy '*' -sv -m5 http://web/ -o /dev/null`, 직후 `echo "종료코드=$?"`.
- 주요 출력: web:80 해석, IPv4 `172.19.0.2`, `Connected to web (172.19.0.2) port 80`, `GET / HTTP/1.1`, `HTTP/1.1 200 OK`, Server `nginx/1.27.5`, Content-Length `615`, 종료코드 `0`.
- 결과와 의미: DNS·TCP·HTTP 정상 진단 3단계 모두 성공. 응답 Date 헤더는 `Mon, 28 Sep 2026 03:37:16 GMT`로 사용자가 제공했다. 실패 유형 비교 및 보조 조회는 아직 미진행이다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내(미실행): `docker exec client nc -zv -w3 web 81`, 직후 `echo "종료코드=$?"`. 같은 서버의 다른 포트에 접근하여 연결 거절을 관찰한다.

### 2026-09-28 — 4-5 연결 거절 확인
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`에서 client 내부 명령 실행.
- 실행 명령: `docker exec client nc -zv -w3 web 81`, 직후 `echo "종료코드=$?"`.
- 주요 출력: `nc: connect to web (172.19.0.2) port 81 (tcp) failed: Connection refused`, 종료코드 `1`.
- 결과와 의미: web 이름은 해석됐지만 81번 TCP 연결은 거절됐다. nginx를 80번에만 실행한 실습 구성과 일치한다. 일반 환경에서는 연결 거절만으로 서비스 미기동과 방화벽 REJECT 등 상세 원인을 확정할 수 없다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내(미실행): 가이드의 `docker exec client nc -zv -w3 10.255.255.1 80`, 직후 종료코드 출력. 해당 사설 IP가 실제로 미사용이라고 보장하지 않으며 환경별 결과를 그대로 해석한다. 시간 초과 여부를 미리 완료로 기록하지 않는다.

### 2026-09-28 — 4-5 TCP 시간 초과 확인
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`에서 client 내부 명령 실행.
- 실행 명령: `docker exec client nc -zv -w3 10.255.255.1 80`, 직후 `echo "종료코드=$?"`.
- 주요 출력: `nc: connect to 10.255.255.1 port 80 (tcp) timed out: Operation in progress`, 종료코드 `1`.
- 결과와 의미: 제한 시간 내 TCP 연결을 맺지 못했다. 앞선 web:81의 Connection refused와 종료코드는 동일하게 1이므로 문구와 대상·포트를 함께 기록해야 한다. 방화벽·라우팅 등 상세 원인을 확정하거나 대상 IP가 미사용이라고 입증한 것은 아니다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내(미실행): web의 NetworkSettings.Networks, lab-net 컨테이너 이름·IPv4Address, client의 ip route를 조회한다. 이어 --rm --network lab-net의 일회용 netshoot에서 dig +short web 및 프록시 없는 curl HEAD 요청으로 진단 컨테이너 사용법을 확인한다.

### 2026-09-28 — 4-5 보조 조회 및 절 완료
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`.
- 실행 명령: `docker inspect web --format '{{json .NetworkSettings.Networks}}'`, `docker network inspect lab-net --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{println}}{{end}}'`, `docker exec client ip route`, `docker run --rm --network lab-net nicolaka/netshoot:v0.13 sh -c 'dig +short web; curl --noproxy "*" -sS -I -m5 http://web/'`.
- 주요 출력: web은 lab-net의 `172.19.0.2/16`, Gateway `172.19.0.1`. lab-net의 Containers 조회에는 client `172.19.0.3/16`, web `172.19.0.2/16` 두 개가 표시됐다.
- 라우팅 출력: `default via 172.19.0.1 dev eth0`, `172.19.0.0/16 dev eth0 proto kernel scope link src 172.19.0.3`.
- 일회용 진단 결과: dig는 `172.19.0.2`, curl HEAD는 HTTP/1.1 200 OK, Server nginx/1.27.5, Content-Length 615. Date 헤더는 Mon, 28 Sep 2026 03:42:49 GMT.
- 결과와 의미: 같은 서브넷의 직접 연결 경로와 그 밖의 목적지에 쓰는 기본 경로를 조회했다. 새 진단 컨테이너를 같은 네트워크에 연결해도 이름 해석·HTTP 응답이 성공했다. 정상 진단 3단계 및 실패 유형 비교와 함께 4-5 완료로 기록한다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 관찰 범위: 이번 lab-net 조회에 isolated는 표시되지 않았다. 초기 sleep 3600 종료 가능성은 있으나 현재 상태를 직접 조회하지 않았으므로 삭제·설정 해제로 단정하지 않는다. 일회용 컨테이너는 --rm으로 실행했다.
- 학습 자료 메모: 폐쇄망에서는 진단용 netshoot 이미지를 반입 목록에 포함할 필요가 있다. 이번에는 반입 패키지 문서 변경이나 추가 다운로드를 수행하지 않았다.
- 남은 범위: 4-6 사내 DNS·정적 호스트, lazydocker Networks 관찰, Day 전체 정리·자기점검은 미진행이다. 기존 실습 Docker 자원과 임시 폴더 /tmp/day04-http.fdpmdu를 유지한다.

### 2026-09-28 — 4-6 DNS 설정 전달 확인 안내(미실행)
- 사용자 요청: 다음 실습으로 진행.
- 실행할 위치: Ubuntu WSL2 `/home/user/onprem-lab`.
- 안내 명령: `docker run --rm --dns 10.0.0.53 --dns-search corp.local alpine:3.20 cat /etc/resolv.conf`.
- 목적: DNS 서버 주소 및 검색 접미사 옵션이 일회용 컨테이너의 설정 파일에 전달되는지 확인한다. 10.0.0.53과 corp.local은 가이드 예시이며 실제 DNS 서버 연결·도메인 해석을 시험하는 단계가 아니다.
- 실행 여부: 안내만 했으며 결과는 아직 받지 않았다. 데몬 설정·기존 컨테이너 DNS는 변경하지 않았다.

### 2026-09-28 — 4-6 DNS 설정 전달 확인
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`.
- 실행 명령: `docker run --rm --dns 10.0.0.53 --dns-search corp.local alpine:3.20 cat /etc/resolv.conf`.
- 주요 출력: `nameserver 10.0.0.53`, `search corp.local`. Docker 생성 주석과 `Overrides: [nameservers search]`도 표시됐다. 가이드 예시의 options 줄은 표시되지 않았다.
- 결과와 의미: 컨테이너별 DNS 서버·검색 접미사 설정 전달 성공. 예시 DNS 서버 도달성 또는 실제 이름 해석 성공을 검증한 것은 아니다. options 줄 부재만으로 실패로 판단하지 않는다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내(미실행): `docker run --rm --add-host erp.corp.local:10.20.30.40 alpine:3.20 grep erp /etc/hosts`. 일회용 컨테이너의 정적 이름·IP 매핑을 조회한다.

### 2026-09-28 — 4-6 정적 호스트 등록 및 절 완료
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`.
- 실행 명령: `docker run --rm --add-host erp.corp.local:10.20.30.40 alpine:3.20 grep erp /etc/hosts`.
- 주요 출력: `10.20.30.40     erp.corp.local`.
- 결과와 의미: 일회용 컨테이너 /etc/hosts에 예시 이름·IP 매핑이 등록됐다. 앞선 /etc/resolv.conf의 DNS 서버·검색 접미사 설정 전달과 비교하여 4-6 실습 완료. 실제 DNS 조회 성공이나 ERP 서버 연결을 검증한 것은 아니다. 호스트 /etc/hosts나 Docker 데몬 설정은 변경하지 않았다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 개념 정리: --dns는 조회할 DNS 서버, --dns-search는 짧은 이름 조회 시 사용할 도메인 검색 접미사, --add-host는 컨테이너에 직접 기록할 이름·IP 매핑이다. 실제 사내 환경에서는 DNS 주소·접미사·DNS 통신 가능 여부 및 Docker 대역과 사내 대역의 겹침을 확인한다. daemon.json의 공통 DNS·주소 풀 설정은 가이드 설명 사항으로 남기며 이번 실습에서는 변경하지 않는다.
- 완료 범위: 4-1~4-6 실습 절 완료. lazydocker Networks 관찰·Day 전체 자원 정리·자기점검은 별도이며 아직 미진행이다.

### 2026-09-28 — lazydocker 관찰 준비 안내(미실행)
- 사용자 요청: lazydocker 관찰.
- 안내 명령: Ubuntu에서 `docker inspect web client isolated --format '{{.Name}}: {{.State.Status}}'`.
- 목적: Networks에서 lab-net·other-net과 isolated의 양쪽 연결을 관찰하기 전 실행 상태 확인. 앞선 lab-net 목록에 isolated가 없었으나 종료 원인은 아직 조회하지 않았다.
- 실행 여부: 안내만 했으며 결과는 아직 받지 않았다. 재시작 및 lazydocker 화면 관찰도 미확인이다.

### 2026-09-28 — lazydocker 관찰 전 isolated 중지 확인
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`.
- 실행 명령: `docker inspect web client isolated --format '{{.Name}}: {{.State.Status}}'`.
- 주요 출력: `/web: running`, `/client: running`, `/isolated: exited`.
- 결과와 의미: 관찰 준비를 위해 isolated 재시작이 필요하다. sleep 3600으로 생성했으나 이번 출력에는 종료 사유가 없으므로 만료로 단정하지 않는다.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 아님.
- 다음 안내(미실행): `docker start isolated`, `docker inspect isolated --format '{{.Name}}: {{.State.Status}}'`, `lazydocker`. Networks에서 lab-net과 other-net을 선택하여 서브넷·연결 컨테이너 목록을 관찰한다. 양쪽에 isolated가 보이는지는 후속 화면으로 확인한다.

### 2026-09-28 — lazydocker lab-net 화면 관찰 및 표시 차이
- 확인 자료: 사용자 제공 [lazydocker lab-net 화면](evidence/lazydocker-lab-net-user-2026-09-28.png). 원본은 사용자 첨부 lazy_labnet.png이며 Codex가 Windows 기록 폴더에 증거 사본을 저장했다.
- 주요 화면: lazydocker 0.25.2, Networks에 lab-net·other-net이 있고 lab-net이 선택됨. Config의 ID는 기존 abd283b8… 네트워크와 일치하고 Name lab-net, Driver bridge, Scope local. Containers는 none으로 표시되며 현재 화면에 서브넷·게이트웨이는 보이지 않는다.
- 컨테이너 화면: client·isolated·pub·pub2·web·web2 running, client2 exited (0), 기존 koica 컨테이너 exited (143). isolated가 실행 중인 것은 화면으로 확인했으나 재시작 명령의 터미널 출력은 별도 제공되지 않았다.
- 결과와 의미: lazydocker 실행과 네트워크 목록은 확인했다. Containers: none만으로 실제 미연결을 단정하지 않으며 Docker 직접 inspect 결과와 비교한다. 화면 표시 차이의 원인은 아직 미확정이다.
- 확인 주체: 사용자 제공 스크린샷을 Codex가 판독. Ubuntu 명령 직접 실행 아님.
- 다음 안내(미실행): 화면 하단의 q: quit에 따라 lazydocker를 나와 Ubuntu에서 `docker network inspect lab-net other-net --format '{{.Name}} {{json .IPAM.Config}}{{println}}{{range .Containers}}{{.Name}} {{.IPv4Address}}{{println}}{{end}}'`로 대역·게이트웨이·연결 컨테이너를 조회한다.

### 2026-09-28 — lazydocker 표시와 Docker 직접 조회 대조
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`.
- 실행 명령: `docker network inspect lab-net other-net --format '{{.Name}} {{json .IPAM.Config}}{{println}}{{range .Containers}}{{.Name}} {{.IPv4Address}}{{println}}{{end}}'`.
- 주요 출력: lab-net은 Subnet 172.19.0.0/16·Gateway 172.19.0.1, client 172.19.0.3/16·web 172.19.0.2/16·isolated 172.19.0.4/16. other-net은 Subnet 172.20.0.0/16·Gateway 172.20.0.1, isolated 172.20.0.2/16.
- 결과와 의미: isolated의 두 네트워크 연결 및 대역·게이트웨이 확인. lazydocker lab-net 화면의 Containers: none은 Docker 직접 inspect가 보고한 연결 상태와 불일치한다. 실제 미연결로 판단하지 않으며 표시 차이의 내부 원인·버전 호환성은 미확정이다.
- 확인 주체: 사용자 제공 출력과 앞선 사용자 화면을 Codex가 대조. Ubuntu 직접 실행 아님.
- 다음 안내(미실행): `lazydocker`를 다시 열어 Networks에서 other-net을 선택하고 화면을 확인한다. 업데이트·설정 변경·컨테이너 재생성은 수행하지 않는다.

### 2026-09-28 — lazydocker other-net 화면 및 관찰 완료
- 확인 자료: 사용자 제공 [other-net 화면](evidence/lazydocker-other-net-user-2026-09-28.png). 원본 other_net.png를 Codex가 Windows 증거 폴더에 복사했다.
- 주요 화면: Networks의 other-net 선택, Config Name other-net·Driver bridge·Scope local·ID 8963d62b…로 기존 생성 ID와 일치. Containers: none이며 현재 화면에 서브넷·게이트웨이는 보이지 않는다. 좌측 isolated·client·web 등은 running, client2는 exited (0)로 표시된다. 하단 버전은 0.25.2다.
- 대조 결과: lab-net과 other-net 모두 TUI의 Containers: none 표시가 Docker inspect의 연결 목록과 불일치한다. 직접 조회로 isolated는 lab-net 172.19.0.4/16, other-net 172.20.0.2/16 양쪽에 연결된 것을 확인했다. 표시 차이의 내부 원인은 미확정이며 네트워크 장애·미연결로 판정하지 않는다.
- 확인 주체: 사용자 제공 스크린샷 및 앞선 사용자 CLI 출력 대조. Codex가 Ubuntu에서 직접 조회한 것은 아니다.
- 완료 판단: 두 네트워크의 존재·드라이버를 TUI로 관찰하고, 화면에 없는 연결·IPAM 정보는 CLI로 보완해 관찰 완료. 가이드처럼 TUI에서 모든 정보가 보인 것으로 기록하지 않는다. 업데이트·설정 변경·컨테이너 재생성은 수행하지 않았다.
- 남은 범위: Day 전체 자원 정리·자기점검. 정리 명령은 아직 안내·실행하지 않았다. q로 TUI 종료는 안내 가능하나 실행 결과는 아직 미확인이다.

### 2026-09-28 — 개념 정리 및 FDE 업무 범위 질의응답
- 사용자 질문: Day 4의 목적·핵심, 로컬 배포 테스트를 통과한 이미지가 고객 환경에서 실패할 수 있는지, 실패 시 진단 순서, FDE와 고객사 유지보수팀의 역할 분담.
- 학습 정리: 이미지 외부의 DNS·네트워크 소속·바인딩·경로·방화벽·인증 설정이 실행 결과에 영향을 줄 수 있다. 문제가 발생한 컨테이너에서 이름 해석 → TCP 연결 → HTTP 응답을 확인하고 단계별 증거로 원인을 좁힌다. 인증·TLS는 설명만 했으며 장애 재현은 하지 않았다.
- 사용자 이해 확인: 사용자가 DNS·네트워크, 서비스 실행·포트·바인딩·방화벽 경로, HTTP 응답·인증 확인 순서를 자신의 말로 정리했다. 가이드 자기점검 5문항을 별도로 평가하거나 모두 통과한 것으로 기록하지 않는다.
- 역할 구분: FDE의 배포·연동 진단, 담당 애플리케이션 수정, 고객 IT·보안팀과의 해결 조율 및 재검증을 설명했다. 사내 인프라 변경 권한·상시 운영 책임은 계약과 인수인계 범위에 따라 정한다. 특정 BCG 프로젝트의 내부 업무분장을 확인한 것은 아니다.
- 참고 자료: [BCG, AI and the Changing Face of Work](https://www.bcg.com/assets/2026/276-weekly-brief-ai-and-the-changing-face-of-work.pdf). FDE 등을 포함한 전문 인력이 고객 업무에 AI를 적용하고 기존 시스템을 연결하는 역할을 설명한다. 위의 상세 역할 분담은 일반적인 프로젝트 적용 설명이다.

### 2026-09-28 — 종료 정리 완료 확인 및 PR 준비
- 사용자 요청: “Day4를 마무리하고 PR을 만들자”.
- 안내 위치: Ubuntu WSL2 `/home/user/onprem-lab`. 기존 방식대로 사용자가 실행하며 Codex가 Docker 자원을 직접 삭제하지 않았다.
- 안내 명령:

```bash
docker rm -f web client web2 client2 isolated pub pub2
docker network rm lab-net other-net
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker network ls
ss -ltn '( sport = :8080 or sport = :8081 or sport = :9999 )'
```

- 사용자 응답: “완료했어”. 안내한 정리의 완료 확인으로 기록한다. 개별 명령 출력·종료코드는 제공되지 않았으므로 삭제 후 목록과 리스너 부재를 직접 대조했다고 기록하지 않는다.
- 범위: Day 4 컨테이너 7개 및 네트워크 2개만 정리 대상으로 안내했다. 기존 koica 자원·이미지·볼륨·임시 폴더 `/tmp/day04-http.fdpmdu`는 삭제 대상에 포함하지 않았다. Python 서버는 앞선 ps·ss 출력으로 종료를 확인했다.
- 완료 판단: 4-1~4-6 실습·화면 관찰·개념 질의응답 및 사용자 자원 정리 완료 확인으로 Day 4를 종료한다. 별도 자기점검 5문항 평가, 직접 IP 시간 초과 및 TUI 불일치의 세부 원인 해결은 완료 범위에 포함하지 않는다.
- Codex 작업: Windows의 README·SESSION·PROGRESS·환경 기록과 사용자 스크린샷을 정리한다. Ubuntu 동기화나 실습 재실행은 하지 않는다.
- Git 기준: 원격 조회로 Day 3 PR #5의 main 병합(027012d)을 확인하고 `codex/day04-results`를 해당 main에서 생성했다. Day 4 변경만 별도 PR로 제출한다.
- 제출 결과: [PR #6](https://github.com/shanis345/Deploy_Practice/pull/6), `codex/day04-results` → `main`. 2026-09-28 생성했으며 병합은 수행하지 않았다.
- 문서 검증: git diff --check 통과, 변경 문서 4개의 로컬 링크 45개 대상 존재 확인, 변경 텍스트 범위의 자격 증명 패턴 검출 없음. 문서·화면 증거만 변경하여 애플리케이션 테스트나 Ubuntu 실습 재실행은 하지 않았다.

### 2026-09-28 — PR 병합 확인
- 사용자 알림: “merge 했어”. Codex가 GitHub에서 PR #6의 MERGED 상태와 병합 커밋 `f316ff898cfdf5390c8207ae460f2061d60d6cd6`을 확인했다. 병합 시각은 2026-09-28 13:33:50 KST다.
- Windows 로컬 main으로 전환하고 origin/main까지 fast-forward 갱신했다. Ubuntu 복사본은 변경하지 않았다.
- 이 병합 확인 메모와 PROGRESS 갱신은 로컬 미커밋 변경으로 남겨 다음 기록 커밋에 포함한다. 추가 PR·원격 main 직접 푸시는 수행하지 않았다. Day 5는 시작하지 않았다.

## 오류와 해결
- 기본 bridge의 web2 이름 해석 실패는 비교 실습에서 의도한 결과다. 수정하지 않았다.
- 4-1의 curl 코드 28은 `Resolving timed out`이므로 이름 해석 단계 시간 초과다. 4-4 Ubuntu IP 직접 요청의 코드 28은 `Connection timed out`이므로 연결 단계 시간 초과다. 코드만으로 방화벽·바인딩 등 상세 원인을 단정하지 않는다.

## 배운 내용과 질문
- 사용자 질문: 서브넷과 게이트웨이의 의미. 서브넷은 하나의 네트워크로 묶인 IP 주소 범위, 게이트웨이는 다른 네트워크로 통신할 때 거치는 출구로 설명했다.

## 가이드와 실제 환경의 차이
공통 환경은 [환경 기록](../docs/environment.md)을 참고한다.
- 4-1 기본 bridge 비교에서 nslookup은 NXDOMAIN이었지만 curl은 가이드의 코드 6 대신 코드 28(이름 해석 중 3초 제한 도달)을 반환했다. 가이드와 다른 종료코드 및 실제 오류 문구를 그대로 보존한다.
- 4-4에서는 Ubuntu 서버가 127.0.0.1에 바인딩된 상태에서도 Docker Desktop 기본 host.docker.internal 경로로 본문·HTTP 200을 받았다. 가이드의 --add-host=host.docker.internal:host-gateway를 적용하지 않았고 기본 이름 해석을 사용했다. Linux Docker Engine의 예측을 이 환경에 그대로 적용하지 않는다.

## 다음에 이어 할 지점
Day 4 종료. 사용자가 다음 Day를 요청하면 해당 가이드와 기록을 읽고 시작한다. 자기점검 5문항 평가는 별도 미진행으로 남긴다. 마지막 자원 정리는 사용자 완료 진술이며 필요 시 재개 전에 현재 상태를 조회한다. Python 서버는 종료했고 임시 폴더 /tmp/day04-http.fdpmdu는 삭제하지 않았다. TUI 표시 불일치와 직접 IP 경로 시간 초과·대역 겹침의 상세 원인은 미해결로 유지한다. 기존 koica 자원과 Docker 전역 설정은 변경하지 않는다.
