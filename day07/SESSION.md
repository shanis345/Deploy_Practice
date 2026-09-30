# Day 7 — 포워드 프록시, 화이트리스트, HTTP_PROXY/NO_PROXY 함정

## 진행 상태
- 상태: 완료·종료 · 7-1~7-5 학습·자원 정리·체크포인트 해설 완료, 독립 답변 평가 미실시(2026-09-30)
- 완료한 범위: 7-1 구성, 7-2 응답・로그 검증, 7-3 사례 1~3 실패·복구 비교 및 사례 4 빌드 인자 기록 비교·임시 정리, 7-4 HTTP 요청·응답·Timing 관찰 및 mitm 정리, 7-5 설계 설명·질의응답, Day 7 Compose 정리(실행 증거는 사용자 출력)
- 종료 지점: 사용자 출력으로 Day 7 컨테이너 4개·네트워크 2개 제거와 잔존 목록 부재를 확인했다. 다음 Day는 사용자 요청 후 시작한다.
- Codex 작업: 아직 별도 작업을 만들지 않음
- 실행 증거 기준: 사용자 제공 출력과 직접 검증 결과를 구분해 기록

## 목표와 이번 세션 범위
사용자가 Day 7 시작을 요청했다. 7-1 화이트리스트 프록시 구성의 사전 점검부터 진행한다. 사용자가 Ubuntu WSL2에서 직접 명령을 실행하고 결과를 제공하며, 다음 절은 자동 진행하지 않는다.

## 실행 기록
### 2026-09-30 — Day 7 시작 및 7-1 사전 점검 안내(미실행)
- Codex 직접 확인: Windows의 PROGRESS·환경 기록·Day 7 README·SESSION·가이드 7-1·compose.yaml·squid.conf를 읽었다. 구성은 proxy·agent·probe·internal-api의 네 서비스와 closed·outside 네트워크 두 개이며 호스트 포트 게시가 없다.
- Git 인수인계: Day 6 PR #8의 main 병합(b3a34c5)을 원격 조회로 확인했다. 이전 완료 브랜치를 정리하고 Windows main을 해당 커밋으로 갱신한 뒤 codex/day07-results를 생성했다. 새 PR·커밋은 아직 없다. Ubuntu 사본은 갱신하지 않았다.
- Windows SHA-256: compose.yaml은 8893eb9d936833896fdc185c846d8ccd175e82b5185f19d357275c95b2aeee3e, squid.conf는 2d64f2f2fb011dcf17a2f1053956c0df42e8cb0ad9e888341323b50b4e6a5457.
- 안내 실행 위치: Ubuntu WSL2 /home/user/onprem-lab/day07. Windows Docker Desktop을 실행해 둔다. cd 또는 명령 오류 시 중단하고 출력을 공유한다.

```bash
cd /home/user/onprem-lab/day07
pwd
sha256sum compose.yaml squid.conf
docker version
docker compose version
docker compose config --quiet && echo "문법 OK"
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker network ls --filter label=com.docker.compose.project=day07
docker image inspect ubuntu/squid:5.2-22.04_beta agent:0.2.0 nicolaka/netshoot:v0.13 traefik/whoami:v1.10 --format '{{join .RepoTags ", "}} {{.Os}}/{{.Architecture}}'
```

- 목적: Windows와 Ubuntu 파일 일치, Docker 엔진 응답·Compose 문법, 기존 자원 및 필요 이미지 네 개의 로컬 존재 확인.
- 실행 여부: 안내만 했으며 사용자 결과를 아직 받지 않았다. 설치·다운로드·컨테이너 생성·Ubuntu 파일 수정은 수행하지 않았다. 사전 점검이나 7-1 완료로 기록하지 않는다.

### 2026-09-30 — 사전 점검 정상 및 기동 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: 위 사전 점검 명령 전체. 확인 주체는 사용자 제공 출력이며 Codex 직접 Ubuntu 실행이 아니다.
- 두 파일의 SHA-256은 위 Windows 사본과 모두 일치한다. Docker Client/Engine 29.8.0, API 1.56, Desktop 4.92.0(240144), linux/amd64, Compose v5.5.1 및 `문법 OK`를 확인했다.
- 컨테이너 목록: Day 7 컨테이너 없음. pub2·web2·web 실행 중, pub·isolated·client2·client 및 기존 koica 앱 중지 상태. pub2는 호스트 8081을 게시한다. Day 7 라벨로 조회한 네트워크 목록은 헤더만 표시됐다. 기존 자원은 변경하지 않는다.
- ubuntu/squid:5.2-22.04_beta, agent:0.2.0, nicolaka/netshoot:v0.13, traefik/whoami:v1.10 네 이미지 모두 로컬 존재·linux/amd64를 확인했다.
- 결과: 사전 점검 정상. 다음 명령으로 Day 7 컨테이너 4개·네트워크 2개를 생성·기동하고 상태를 조회하도록 안내한다. --pull never로 확인된 로컬 이미지를 사용한다.

```bash
docker compose up -d --pull never
docker compose ps -a
```

- 기동 명령은 아직 안내만 했으며 실행 결과 대기다. 기동 후 상태와 프록시 설정 전달을 확인해야 7-1 완료로 판단한다. 7-2 통신 검증은 미진행이다.

### 2026-09-30 — 네 서비스 기동 확인 및 구성 검증 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: `docker compose up -d --pull never`, `docker compose ps -a`.
- 사용자 출력: day07_outside·day07_closed Created, day07-probe-1·day07-internal-api-1·day07-agent-1·day07-proxy-1 Started. 네 서비스 모두 Up Less than a second. agent는 health: starting이며 아직 healthy로 확인한 것은 아니다.
- PORTS의 agent 8000/tcp·internal-api 80/tcp·proxy 3128/tcp는 호스트 게시를 뜻하지 않는다. 이미지 노출 포트 표시와 구분한다.
- 확인 주체: 사용자 제공 출력. Codex가 Ubuntu 명령을 직접 실행한 것이 아니다. 아직 프록시 환경변수 전달·외부 허용/차단·실제 네트워크 소속을 검증하지 않았다.
- 다음 안내(결과 대기): 아래 명령으로 상태·네트워크 구성을 확인하고 probe에서 agent의 healthz·diag를 호출한다. q는 현재 Ubuntu 셸에 정의하는 도우미 함수이며 새 셸에서는 다시 정의해야 한다. probe→agent 요청은 --noproxy '*'로 직접 연결하되 agent의 외부 요청용 설정은 바꾸지 않는다.

```bash
docker compose ps -a
docker network inspect day07_closed day07_outside --format '{{.Name}} internal={{.Internal}} containers={{range .Containers}}{{.Name}} {{end}}'
q() { docker compose exec -T probe curl --noproxy '*' -fsS -m 15 "http://agent:8000/$1"; }
q healthz | jq .
q diag | jq '{proxy}'
```

- 기대: agent healthy, closed internal=true에 네 서비스, outside internal=false에 proxy만 연결. healthz status=ok, HTTP(S)_PROXY 대소문자 네 값은 http://proxy:3128, NO_PROXY/no_proxy는 localhost,127.0.0.1,proxy,internal-api,.corp.local. 실제 출력 확인 전 성공으로 기록하지 않는다. 7-2는 아직 미진행.

### 2026-09-30 — 구성·프록시 설정 확인 및 7-1 완료
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: 위 ps·network inspect·q 함수 정의·healthz·diag 조회 전체.
- 상태: 네 서비스 모두 Up About a minute, agent healthy.
- 네트워크: day07_closed internal=true에 internal-api·proxy·agent·probe 연결. day07_outside internal=false에는 proxy만 연결. 설정한 소속과 일치한다.
- healthz: status=ok, version=0.2.0, host=9f5102a4fb70. probe에서 agent API 직접 응답 성공.
- diag: HTTP_PROXY·HTTPS_PROXY·http_proxy·https_proxy 모두 http://proxy:3128. NO_PROXY·no_proxy 모두 localhost,127.0.0.1,proxy,internal-api,.corp.local로 일치한다.
- 결과: 사전 점검·기동과 이번 구성·설정 전달 확인을 합쳐 7-1 완료. 외부 HTTP/HTTPS 허용·차단, internal-api의 프록시 우회 및 Squid 접근 로그 대조는 아직 미시험이며 7-2에서 검증한다. 환경변수 존재만으로 프록시 통신 성공을 판단하지 않는다.
- 확인 주체: 사용자 제공 출력. [증거](evidence/71-config-user-2026-09-30.txt). Codex는 Windows 기록만 갱신했다.
- 종료 상태: Day 7 컨테이너 4개·네트워크 2개를 유지한다. q는 현재 사용자 셸에 정의돼 있다. Day 7 전체 완료나 자원 정리로 처리하지 않으며 다음 절은 자동 시작하지 않는다.

### 2026-09-30 — 7-2 시작·① 허용 HTTP 요청 안내(미실행)
- 사용자 요청: 다음으로 진행. 7-2의 허용·차단 검증을 한 항목씩 진행한다.
- Codex가 가이드 7-2와 agent/app.py의 /egress 구현을 확인했다. /egress는 외부 요청 성공 여부를 JSON의 ok·status·error_type·error로 반환하며 외부 요청 실패 시에도 API 자체는 HTTP 200을 반환한다. 응답 본문을 기준으로 판단한다.
- 실행 위치: 기존 q 함수가 정의된 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 안내 명령:

```bash
q "egress?url=http://example.com" | jq '{ok,status,error_type,error,elapsed_ms}'
```

- 요청 흐름: probe→agent /egress→proxy:3128→example.com:80. 프록시 ACL의 .example.com은 허용 대상이다. 기대는 ok=true·status=200이며 실제 결과는 아직 받지 않았다. 오류 시 error_type·error를 그대로 확인한다.
- 실행 여부: 안내만 했다. 프록시 경유의 요청별 증거는 후속 Squid 접근 로그와 대조한다. HTTPS·차단 목적지·내부 API·로그 확인은 아직 미진행이다.

### 2026-09-30 — 7-2 ① 허용 HTTP 성공 및 ② HTTPS 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: `q "egress?url=http://example.com" | jq '{ok,status,error_type,error,elapsed_ms}'`.
- 사용자 출력: ok=true, status=200, error_type=null, error=null, elapsed_ms=331.
- 결과: 허용된 example.com의 HTTP 요청 성공. 요청별 프록시 경유 확인은 후속 Squid 접근 로그와 대조하며 이번 응답만으로 로그까지 검증한 것은 아니다. 확인 주체는 사용자 제공 출력이며 Codex 직접 실행 아님.
- 다음 안내(미실행): 같은 허용 도메인에 HTTPS로 요청하여 CONNECT 터널 및 TLS가 포함된 경로의 실제 결과를 확인한다.

```bash
q "egress?url=https://example.com" | jq '{ok,status,error_type,error,elapsed_ms}'
```

- 기대는 ok=true·status=200. 실제 출력은 아직 없다. 인증서 오류가 발생하더라도 TLS 검사 환경으로 즉시 단정하지 않고 오류·인증서·프록시 로그 등 증거로 원인을 구분한다. 인증서 검증 비활성화는 안내하지 않는다. 차단 목적지·내부 API 우회·프록시 로그 검증은 미진행이다.

### 2026-09-30 — 7-2 ② 허용 HTTPS 성공 및 ③ 비허용 HTTP 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: `q "egress?url=https://example.com" | jq '{ok,status,error_type,error,elapsed_ms}'`.
- 사용자 출력: ok=true, status=200, error_type=null, error=null, elapsed_ms=191.
- 결과: 이번 example.com HTTPS 요청 성공. 앞선 HTTP 331ms와 이번 HTTPS 191ms는 각 1회 관찰값이며 프로토콜 성능 비교로 해석하지 않는다. 프록시 CONNECT 경유의 요청별 증거는 후속 접근 로그와 대조한다. Codex 직접 Ubuntu 실행 아님.
- 다음 안내(미실행): 허용 목록에 없는 www.google.com으로 HTTP 요청한다.

```bash
q "egress?url=http://www.google.com" | jq '{ok,status,error_type,error,elapsed_ms}'
```

- 기대는 ok=false·status=403·error_type=HTTPError. 실패가 의도된 통제 결과인지 프록시 로그의 TCP_DENIED/403과 후속 대조한다. 실제 출력은 아직 없으며 ③ 완료로 기록하지 않는다. 비허용 HTTPS·사내 API 우회·로그 대조는 미진행이다.

### 2026-09-30 — 7-2 ③ 비허용 HTTP 거부 확인 및 ④ HTTPS 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: `q "egress?url=http://www.google.com" | jq '{ok,status,error_type,error,elapsed_ms}'`.
- 사용자 출력: ok=false, status=403, error_type=HTTPError, error=HTTP Error 403: Forbidden, elapsed_ms=1.
- 결과: 비허용 HTTP 요청이 예상대로 거부됐다. 403은 이번 통제 검증의 기대 결과이며 애플리케이션 고장으로 처리하지 않는다. 실제 Squid 정책에 의한 차단인지는 후속 접근 로그의 해당 요청·TCP_DENIED/403과 대조한다. 확인 주체는 사용자 출력이며 Codex 직접 Ubuntu 실행 아님.
- 다음 안내(미실행): 같은 비허용 목적지에 HTTPS로 요청한다.

```bash
q "egress?url=https://www.google.com" | jq '{ok,status,error_type,error,elapsed_ms}'
```

- 기대: ok=false, CONNECT 터널 거부를 나타내는 Tunnel connection failed: 403 Forbidden. 가이드 예시는 error_type=OSError이며 실제 값을 확인한다. 이 앱에서 터널 수립 실패는 외부 HTTP 응답 status 필드를 만들지 않을 수 있으므로 jq에 status=null로 표시돼도 오류 문구를 함께 해석한다. 아직 ④ 실행 결과는 없으며 내부 API 우회·프록시 로그 대조도 미진행이다.

### 2026-09-30 — 7-2 ④ 비허용 HTTPS 터널 거부 및 ⑤ 내부 API 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: `q "egress?url=https://www.google.com" | jq '{ok,status,error_type,error,elapsed_ms}'`.
- 사용자 출력: ok=false, status=null, error_type=OSError, error=Tunnel connection failed: 403 Forbidden, elapsed_ms=1.
- 결과: 비허용 HTTPS 목적지의 CONNECT 터널 생성이 403으로 거절됐다. 앞선 HTTPError와 달리 터널 수립 실패가 OSError로 반환됐다. agent의 해당 예외 처리에서 status 필드가 없어 jq가 null을 표시하며, 목적지 HTTPS 응답을 받았다는 뜻이 아니다. 요청별 Squid 정책·로그 대조는 아직 남아 있다. 사용자 제공 출력이며 Codex 직접 Ubuntu 실행 아님.
- 다음 안내(미실행): NO_PROXY/no_proxy에 있는 internal-api로 HTTP 요청한다.

```bash
q "egress?url=http://internal-api" | jq '{ok,status,error_type,error,elapsed_ms}'
```

- 기대: ok=true·status=200. agent와 internal-api는 closed 네트워크를 공유하며 프록시 우회 설정이 있다. 이번 요청은 agent→internal-api 내부 통신 확인이며, 성공 응답만으로 경로를 확정하지 않고 후속 프록시 로그와 설정을 함께 대조한다. ⑤ 결과와 ⑥ 로그 확인 전 7-2 전체 완료로 기록하지 않는다.

### 2026-09-30 — 7-2 ⑤ 내부 API 성공 및 ⑥ 접근 로그 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: `q "egress?url=http://internal-api" | jq '{ok,status,error_type,error,elapsed_ms}'`.
- 사용자 출력: ok=true, status=200, error_type=null, error=null, elapsed_ms=11.
- 결과: agent에서 내부 API HTTP 요청 성공. NO_PROXY/no_proxy의 internal-api 설정 및 closed 네트워크 소속과 일치한다. 성공 응답만으로 프록시 우회 경로를 단독 입증한 것은 아니며 후속 접근 로그와 대조한다. 확인 주체는 사용자 출력이며 Codex 직접 Ubuntu 실행 아님.
- 다음 안내(미실행): 해당 실습 프록시의 접근 로그를 조회한다. 가이드의 tail -n 5 대신 현재 파일 전체를 조회해 앞선 요청이 잘리지 않도록 한다.

```bash
docker compose exec -T proxy cat /var/log/squid/access.log
```

- 대조 대상: example.com HTTP의 GET 및 200, example.com:443 CONNECT 및 200, www.google.com HTTP의 GET 및 TCP_DENIED/403, www.google.com:443 CONNECT 및 TCP_DENIED/403. internal-api 요청이 해당 로그에 나타나는지도 확인한다. 로그 부재만으로 우회를 단정하지 않고 앞서 확인한 설정·네트워크·성공 응답과 함께 판단한다.
- 로그 출력은 아직 없다. ⑥ 확인 전 7-2 완료로 처리하지 않는다. 컨테이너·네트워크 유지, 7-3은 미시작이다.

### 2026-09-30 — 7-2 ⑥ 프록시 로그 대조 및 절 완료
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: `docker compose exec -T proxy cat /var/log/squid/access.log`.
- 사용자 출력: 네 행 모두 클라이언트 주소 172.22.0.2. example.com HTTP는 TCP_MISS/200·GET·HIER_DIRECT/104.20.23.154·298ms, HTTPS는 TCP_TUNNEL/200·CONNECT example.com:443·HIER_DIRECT/172.66.147.243·190ms다.
- www.google.com HTTP 및 HTTPS는 각각 GET과 CONNECT이며 모두 TCP_DENIED/403·HIER_NONE/-·0ms다. 앞선 앱의 HTTPError·403 및 OSError·Tunnel connection failed: 403 Forbidden과 일치한다. 앱과 프록시의 시간 값은 측정 범위가 다르므로 동일할 필요는 없다.
- 현재 접근 로그에 internal-api 요청은 없다. 앞서 확인한 NO_PROXY/no_proxy 설정·동일 closed 네트워크 소속·내부 API 200 응답과 함께 프록시 우회 동작에 부합함을 확인했다. 로그 부재 하나만으로 경로를 단정하거나 패킷 캡처를 수행한 것으로 기록하지 않는다.
- 7-2 ①~⑥ 완료: 허용 HTTP/HTTPS 성공, 비허용 HTTP/HTTPS 거부 및 Squid 로그 대조, 내부 API 성공과 우회 설정·로그 관찰을 마쳤다. [사용자 응답·로그 증거](evidence/72-requests-and-log-user-2026-09-30.txt).
- 확인 주체: 사용자 제공 출력. Codex는 Windows 기록만 갱신했다. 컨테이너 4개·네트워크 2개는 유지하며 7-3·Day 7 전체 정리는 미시작이다. 다음 절은 사용자 요청 시 진행한다.

### 2026-09-30 — 7-3 시작 및 실패 1 안내(미실행)
- 사용자 요청: 7-3으로 진행. 가이드 7-3·현재 Compose 구성·기록을 확인했다. 첫 사례는 프록시 환경변수 누락이며 사용자 실행 결과를 확인한 뒤 다음 사례로 진행한다.
- 실행 위치: Ubuntu WSL2 /home/user/onprem-lab/day07.
- 안내 명령: 기존 closed 네트워크에 일회용 agent 이미지 컨테이너를 연결하고 Python 프로세스의 프록시 환경변수를 제거해 외부 HTTP를 요청한다. Docker 클라이언트가 자동 주입하는 프록시 변수가 있더라도 시험 조건이 달라지지 않도록 Python에서 이름이 _proxy로 끝나는 변수를 대소문자 구분 없이 제거한다. 비밀 값은 출력하지 않는다.

```bash
docker run --rm --pull never --network day07_closed agent:0.2.0 python -c "
import os, urllib.request
for key in list(os.environ):
    if key.lower().endswith('_proxy'):
        os.environ.pop(key)
print('프록시 설정:', urllib.request.getproxies())
try:
    with urllib.request.urlopen('http://example.com', timeout=5) as r:
        print('성공:', r.status)
except Exception as e:
    print('실패:', type(e).__name__, e)
"
```

- 기대: 프록시 설정 {} 및 외부 요청 실패. 가이드 예시는 URLError·Temporary failure in name resolution이나 실제 오류를 그대로 확인한다. timeout=5가 OS DNS 해석 시간까지 항상 5초로 제한한다는 뜻은 아니다. 오류 문구만으로 일반 환경의 원인을 확정하지 않으며 이번 통제된 설정과 비교한다.
- 범위: 기존 Compose agent·proxy와 파일은 변경하지 않는다. 일회용 컨테이너는 종료 시 --rm으로 제거하도록 실행한다. 필요한 이미지는 --pull never로 로컬 이미지 사용. 명령은 아직 안내만 했으며 생성·실패·자동 제거 성공을 실제 확인한 것은 아니다.
- 다음: 실제 프록시 설정과 실패 출력을 확인한 뒤 같은 일회용 환경에 프록시를 지정한 비교 요청으로 원인을 검증한다. 실패 2~4는 아직 미진행이다.

### 2026-09-30 — 7-3 실패 1 재현 확인 및 프록시 지정 비교 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: 위 일회용 컨테이너에서 프록시 환경변수를 제거한 Python HTTP 요청.
- 사용자 출력: `프록시 설정: {}`, `실패: URLError <urlopen error [Errno -3] Temporary failure in name resolution>`.
- 결과: 프록시 미설정 상태에서 example.com 직접 요청이 이름 해석 단계에서 실패했다. 현재 closed 구성과 일치한다. 오류 문구만으로 모든 환경에서 프록시 누락이 원인이라고 단정하지 않으며 다음 비교 요청으로 이번 사례를 검증한다. HTTP 403 거부 응답을 받은 것과 구분한다.
- 확인 주체: 사용자 출력. Codex 직접 Ubuntu 실행 아님. --rm 실행 후 프롬프트 복귀를 확인했으나 종료 뒤 컨테이너 목록은 별도 조회하지 않았다. 기존 Compose 설정 변경은 없다.
- 다음 안내(미실행): 같은 이미지·네트워크·목적지의 새 일회용 컨테이너에서 다른 프록시 환경변수는 제거하고 http_proxy 한 항목만 지정한다. 기존 서비스 설정은 변경하지 않는다.

```bash
docker run --rm --pull never --network day07_closed agent:0.2.0 python -c "
import os, urllib.request
for key in list(os.environ):
    if key.lower().endswith('_proxy'):
        os.environ.pop(key)
os.environ['http_proxy'] = 'http://proxy:3128'
print('프록시 설정:', urllib.request.getproxies())
try:
    with urllib.request.urlopen('http://example.com', timeout=5) as r:
        print('성공:', r.status)
except Exception as e:
    print('실패:', type(e).__name__, e)
"
```

- 기대: 프록시 설정 {'http': 'http://proxy:3128'}, 성공: 200. 아직 결과는 받지 않았으며 실패 1 비교 검증 완료로 기록하지 않는다. 실패 2~4는 미진행이다.

### 2026-09-30 — 7-3 실패 1 비교 성공 및 실패 2 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: 위 동일 이미지·closed 네트워크의 일회용 컨테이너에서 프록시 환경변수를 초기화하고 http_proxy=http://proxy:3128을 설정한 HTTP 요청.
- 사용자 출력: `프록시 설정: {'http': 'http://proxy:3128'}`, `성공: 200`.
- 결과: 프록시 미설정 시 이름 해석 실패, 프록시 지정 시 200을 확인해 실패 1 비교 검증 완료. 기존 Compose 서비스 변경·재시작 없이 새 일회용 프로세스의 설정만 비교했다. --rm 종료 후 프롬프트 복귀를 확인했으며 별도 잔존 목록 조회는 하지 않았다. 확인 주체는 사용자 출력이며 Codex 직접 Ubuntu 실행 아님.
- 다음 안내(미실행): 실패 2. 같은 방식으로 http_proxy만 설정하고 NO_PROXY/no_proxy는 없는 상태에서 internal-api로 요청한다. 사내 API 요청도 프록시로 향해 허용 목록에 없는 목적지로 거부되는지 로그와 함께 확인한다.

```bash
docker run --rm --pull never --network day07_closed agent:0.2.0 python -c "
import os, urllib.request
for key in list(os.environ):
    if key.lower().endswith('_proxy'):
        os.environ.pop(key)
os.environ['http_proxy'] = 'http://proxy:3128'
print('프록시 설정:', urllib.request.getproxies())
try:
    with urllib.request.urlopen('http://internal-api', timeout=5) as r:
        print('성공:', r.status)
except Exception as e:
    print('실패:', type(e).__name__, e)
"
docker compose exec -T proxy tail -n 3 /var/log/squid/access.log
```

- 기대: 프록시 설정에 http만 존재, HTTPError·403, Squid 로그에 GET http://internal-api/·TCP_DENIED/403. 아직 결과는 없다. 실패 2 재현 후 no_proxy 지정 비교를 안내한다. 기존 Compose 설정·파일은 유지하며 실패 3·4는 미진행이다.

### 2026-09-30 — 7-3 실패 2 재현 및 우회 설정 비교 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: 위 http_proxy만 지정한 일회용 컨테이너의 internal-api 요청 및 Squid tail -n 3.
- 사용자 출력: `프록시 설정: {'http': 'http://proxy:3128'}`, `실패: HTTPError HTTP Error 403: Forbidden`.
- 관련 로그 원문: `1790737309.411      0 172.22.0.6 TCP_DENIED/403 3443 GET http://internal-api/ - HIER_NONE/- text/html`.
- 결과: 내부 API 요청이 프록시로 전달돼 Squid에서 거부됐다. no_proxy 누락의 의도한 실패를 확인했다. 기존 Compose agent의 7-2 내부 API 성공과 구분한다. 확인 주체는 사용자 출력이며 Codex 직접 Ubuntu 실행 아님.
- 같은 tail 출력의 이전 행: `1790735990.981      0 172.22.0.2 TCP_DENIED/403 3456 CONNECT www.google.com:443 - HIER_NONE/- text/html`, `1790737209.642    160 172.22.0.6 TCP_MISS_ABORTED/200 1145 GET http://example.com/ - HIER_DIRECT/104.20.23.154 text/html`. 후자는 앞선 비교 요청의 200 응답 관찰과 함께 보존하며 전체 본문 수신 성공을 입증하지 않는다. ABORTED의 상세 원인은 이번 출력만으로 확정하지 않는다.
- 다음 안내(미실행): 같은 이미지·내부망에서 프록시 변수를 초기화하고 http_proxy 및 no_proxy=internal-api를 지정한다.

```bash
docker run --rm --pull never --network day07_closed agent:0.2.0 python -c "
import os, urllib.request
for key in list(os.environ):
    if key.lower().endswith('_proxy'):
        os.environ.pop(key)
os.environ['http_proxy'] = 'http://proxy:3128'
os.environ['no_proxy'] = 'internal-api'
print('프록시 설정:', urllib.request.getproxies())
try:
    with urllib.request.urlopen('http://internal-api', timeout=5) as r:
        print('성공:', r.status)
except Exception as e:
    print('실패:', type(e).__name__, e)
"
docker compose exec -T proxy tail -n 3 /var/log/squid/access.log
```

- 기대: getproxies에 http와 no 항목, 성공: 200, 새 internal-api 프록시 로그 없음. 이전 403 로그는 삭제되지 않으므로 시각·행을 비교한다. 아직 사용자 결과를 받지 않았으며 실패 2 비교 검증 완료로 기록하지 않는다. 기존 서비스·파일은 유지한다.

### 2026-09-30 — 7-3 실패 2 우회 성공 및 실패 3 대문자 변수 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: 위 no_proxy=internal-api 지정 일회용 요청 및 Squid tail -n 3.
- 사용자 출력: `프록시 설정: {'http': 'http://proxy:3128', 'no': 'internal-api'}`, `성공: 200`.
- tail의 세 행은 직전 출력과 동일하다. 마지막 internal-api 거부 행의 시각은 1790737309.411로 유지됐으며 새 internal-api 로그가 없다. 앞선 no_proxy 없는 요청의 403 및 이번 200·우회 설정과 합쳐 실패 2 비교 검증 완료. 로그 부재만으로 판단한 것은 아니다.
- 확인 주체: 사용자 출력. Codex 직접 Ubuntu 실행 아님. 기존 Compose 서비스는 변경하지 않았다. 일회용 컨테이너는 --rm 실행 후 프롬프트로 복귀했으며 별도 잔존 목록은 조회하지 않았다.
- 다음 안내(미실행): 실패 3. 같은 closed 네트워크의 netshoot 일회용 컨테이너에서 프록시 환경변수를 모두 해제하고 curl에 대문자 HTTP_PROXY만 전달한다. 쉘 안에서 초기화하여 Docker 클라이언트의 자동 프록시 주입 등으로 실험 조건이 달라지지 않도록 한다.

```bash
docker run --rm --pull never --network day07_closed nicolaka/netshoot:v0.13 sh -c '
unset HTTP_PROXY http_proxy HTTPS_PROXY https_proxy ALL_PROXY all_proxy NO_PROXY no_proxy
export HTTP_PROXY=http://proxy:3128
curl -sS --max-time 5 -o /dev/null -w "HTTP=%{http_code}\n" http://example.com
printf "curl exit=%s\n" "$?"
'
```

- 가이드 기대: curl은 HTTP 요청용 대문자 HTTP_PROXY를 사용하지 않아 직접 접근을 시도하고 실패한다. HTTP=000 및 curl exit=6(이름 해석 실패)이 예상되나 실제 출력을 확인한다. printf는 curl 직후의 종료 코드를 출력하며 docker run 최종 종료 코드와 구분한다. 결과 확인 후 소문자 http_proxy만 지정한 비교를 안내한다.
- 실행 여부: 아직 안내만 했다. 실패 3 완료·실패 4 진행으로 기록하지 않는다. 기존 Compose 구성·q 함수 유지.

### 2026-09-30 — 7-3 실패 3 대문자 실패 확인 및 소문자 비교 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: 위 netshoot 일회용 컨테이너에서 다른 프록시 변수를 해제하고 HTTP_PROXY만 지정한 curl 요청.
- 사용자 출력: `curl: (6) Could not resolve host: example.com`, `HTTP=000`, `curl exit=6`.
- 결과: 대문자 HTTP_PROXY만 지정한 HTTP 요청에서 외부 이름 해석 실패를 확인했다. HTTP=000은 실제 HTTP 응답 코드가 아니라 응답을 받지 못했다는 curl 출력이다. Docker 실행 자체의 실패와 구분하며 curl 직후 기록한 종료 코드는 6이다. 사용자 제공 출력이며 Codex 직접 Ubuntu 실행 아님.
- 다음 안내(미실행): 동일 이미지·내부망·목적지·curl 옵션을 유지하고 소문자 http_proxy만 설정한다.

```bash
docker run --rm --pull never --network day07_closed nicolaka/netshoot:v0.13 sh -c '
unset HTTP_PROXY http_proxy HTTPS_PROXY https_proxy ALL_PROXY all_proxy NO_PROXY no_proxy
export http_proxy=http://proxy:3128
curl -sS --max-time 5 -o /dev/null -w "HTTP=%{http_code}\n" http://example.com
printf "curl exit=%s\n" "$?"
'
```

- 기대: HTTP=200, curl exit=0. 결과 확인 전 실패 3 비교 검증 완료로 기록하지 않는다. 기존 Compose 서비스·파일은 변경하지 않으며 실패 4는 미진행이다.

### 2026-09-30 — 7-3 실패 3 비교 완료 및 실패 4 준비
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: 위 netshoot 일회용 컨테이너에서 http_proxy만 지정한 curl HTTP 요청.
- 사용자 출력: `HTTP=200`, `curl exit=0`.
- 결과: 대문자 HTTP_PROXY만 지정 시 이름 해석 실패·HTTP=000·exit=6, 소문자 http_proxy 지정 시 200·exit=0을 확인해 실패 3 비교 검증 완료. 이번 결과를 모든 도구·모든 프록시 변수의 대소문자 규칙으로 일반화하지 않는다. 기존 Compose 설정은 유지했다. 사용자 출력이며 Codex 직접 Ubuntu 실행 아님.
- 다음 범위: 가이드 실패 4의 빌드 시 프록시 전달 개념과 예약 프록시 인자·일반 ARG의 이미지 히스토리 차이를 작은 임시 이미지로 확인할 예정이다. 실제 고객사 프록시 주소를 사용하거나 기존 agent:0.2.0 이미지를 덮어쓰지 않는다. 실제 pip 설치 장애를 재현한 것으로 기록하지 않는다.
- 공식 문서 확인: https://docs.docker.com/build/building/variables/#proxy-arguments 에서 예약 프록시 인자의 --build-arg 전달 및 기본적인 docker history 제외를 확인했다. 일반 ARG는 메타데이터·히스토리에 남을 수 있으며 모든 인자가 항상 같은 방식으로 남는다고 단정하지 않는다. 실제 실습 결과로 비교한다.
- 먼저 아래 읽기 전용 명령을 사용자에게 안내한다. 아직 출력은 없다.

```bash
docker image inspect alpine:3.20 --format '{{join .RepoTags ", "}} {{.Os}}/{{.Architecture}}'
docker buildx ls
docker image ls day07-buildargs --format 'table {{.Repository}}\t{{.Tag}}\t{{.ID}}'
```

- 목적: Alpine 로컬 존재, 선택된 빌더와 드라이버, 계획한 임시 이미지 이름의 기존 사용 여부 확인. 빌더 생성·기동, 빌드·다운로드·임시 파일 생성은 아직 안내하거나 수행하지 않았다. 결과를 확인한 뒤 고유 임시 디렉터리와 공개 더미 값으로 실습을 안내한다.

### 2026-09-30 — 실패 4 사전 조회 확인 및 임시 이미지 빌드 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 사용자 출력: alpine:3.20 linux/amd64 존재. buildx의 default*는 docker 드라이버·running·BuildKit v0.33.0이며 linux/amd64 지원. day07-buildargs 이미지 목록은 헤더만 표시돼 해당 저장소 이름의 기존 이미지가 없다.
- 별도 desktop-linux 빌더는 error이며 `Cannot load builder desktop-linux: protocol not available`을 표시했다. 해당 항목의 상세 원인은 조사하지 않았다. 정상 조회된 default를 --builder default로 명시하여 실습하며 Docker Desktop 설정·컨텍스트·빌더 등록을 변경하지 않는다.
- 다음 안내(미실행): 고유 임시 폴더에 작은 Dockerfile을 만들고 공개 더미 값으로 빌드한다. HTTP_PROXY는 Dockerfile에 선언·참조하지 않는 예약 인자, PIP_INDEX_URL은 직접 선언하는 일반 ARG다. demo:demo와 .invalid 주소는 실습용 가짜 값이며 실제 자격 증명·접속 대상이 아니다.

```bash
day07_build_dir=$(mktemp -d /tmp/day07-buildargs.XXXXXX) && printf 'FROM alpine:3.20\nARG PIP_INDEX_URL\nRUN echo build\n' > "$day07_build_dir/Dockerfile"
printf '빌드 폴더: %s\n' "$day07_build_dir"
docker build --builder default --pull=false --network=none --no-cache --progress=plain \
  --build-arg HTTP_PROXY=http://demo:demo@proxy.invalid:3128 \
  --build-arg PIP_INDEX_URL=https://demo:demo@packages.invalid/simple \
  -t day07-buildargs:lab "$day07_build_dir"
```

- --network=none은 RUN 단계의 네트워크를 비활성화하며 Dockerfile의 RUN은 echo만 실행한다. 빌더 전체의 모든 네트워크 요청을 금지한다는 뜻은 아니다. --pull=false는 항상 새 기반 이미지를 가져오도록 강제하지 않는 옵션이며 사전 확인한 로컬 Alpine을 이용할 예정이다.
- 이번 작업은 빌드 인자 전달·히스토리 비교용이다. 실제 프록시를 통한 pip 설치나 네트워크 실패를 재현하지 않으며 agent:0.2.0 및 Compose 구성은 유지한다.
- 실행 여부: 빌드 명령은 아직 안내만 했다. 임시 폴더의 실제 경로·빌드 성공·이미지 생성·히스토리 노출은 사용자 결과로 확인한다. 빌드 후 history를 조회하고 결과 확인 뒤 이 실습의 임시 이미지·폴더만 정리할 예정이다.

### 2026-09-30 — 실패 4 임시 빌드 성공 및 히스토리 조회 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: 위 mktemp·Dockerfile 작성·폴더 경로 출력·docker build 명령 전체.
- 사용자 출력: 실제 임시 폴더는 /tmp/day07-buildargs.YTZNch. default 인스턴스·docker 드라이버로 빌드했다. Alpine 기반 레이어는 CACHED, RUN echo build는 build 출력 후 DONE. day07-buildargs:lab 이름 지정·unpacking 및 이미지 export가 완료됐다.
- 빌드 출력의 식별자: 기반 Alpine digest d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc, 이미지 config digest f7e48bbc0162bea046f9271aa9d62ba47e8d31b22b35e8721a3c9f9533697e95, manifest list digest c8a558367039da731016b0e92eebec645231565df0d28b7629ffd0fa442dc2bd. 서로 다른 대상의 digest이며 inspect로 이미지 ID를 별도 조회한 것은 아니다.
- 결과: 임시 이미지 빌드 성공. attestation manifest 내보내기도 표시됐으나 그 내용은 검사하지 않았다. RUN에 네트워크가 필요 없는 빌드이며 실제 프록시 접속 성공·pip 설치 장애 재현으로 해석하지 않는다. load metadata 출력은 있으며 빌드 전체의 네트워크 사용 유무를 이 출력만으로 단정하지 않는다.
- 확인 주체: 사용자 제공 출력. Codex 직접 Ubuntu 실행 아님. 임시 폴더·이미지는 유지하며 기존 Compose 서비스·agent:0.2.0은 변경하지 않았다.
- 다음 안내(미실행): 필터로 일부만 숨기지 않고 CreatedBy 전체를 조회해 두 인자 이름·값의 기록 여부를 비교한다.

```bash
docker history --no-trunc --format '{{.CreatedBy}}' day07-buildargs:lab
```

- 기대: 직접 선언한 PIP_INDEX_URL의 공개 더미 값은 RUN 히스토리에 보이고, Dockerfile에 선언·참조하지 않은 예약 HTTP_PROXY는 기본적으로 제외된다. 실제 결과 대기다. 히스토리만 검사하며 attestation·캐시 등 모든 저장 위치에서 부재를 입증하는 것은 아니다. 결과 확인 후 이번 임시 이미지·폴더만 정리한다.

### 2026-09-30 — 사례 4 히스토리 확인 및 임시 자원 정리 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: `docker history --no-trunc --format '{{.CreatedBy}}' day07-buildargs:lab`.
- 사용자 출력: RUN |1 및 ARG 두 행에 PIP_INDEX_URL=https://demo:demo@packages.invalid/simple이 표시됐다. CMD와 기반 ADD 행도 출력됐고 HTTP_PROXY는 이 히스토리에 표시되지 않았다. [증거](evidence/73-build-history-user-2026-09-30.txt).
- 결과: 이번 일반 ARG 값은 이미지 히스토리에 남았으며, Dockerfile에 선언·참조하지 않은 예약 프록시 인자는 해당 출력에서 제외됐다. 가짜 값 demo:demo를 사용한 실습이며 실제 비밀을 기록하지 않았다. 이 관찰을 모든 캐시·attestation·로그에서 HTTP_PROXY가 항상 비공개라는 주장으로 확대하지 않는다.
- 학습 의미: 실행 시 프록시 설정과 빌드 시 인자는 별개이며, 일반 ARG는 비밀 전달 수단으로 쓰지 않는다. 필요한 빌드 인증값은 BuildKit secret mount 같은 방식을 사용한다. 실제 비밀 설정·secret mount 실습·프록시 연결·pip 설치 장애를 재현한 것은 아니다. 앞서 확인한 Docker 공식 문서의 기본 동작과 구분해 실제 조회 범위를 기록한다.
- 확인 주체: 사용자 출력. Codex 직접 Ubuntu 실행 아님. 사례 1~3 실패·복구 비교와 사례 4 빌드 인자 기록 비교는 확인했으며 임시 자원 정리는 아직 남아 있다.
- 다음 안내(미실행): 이번에 만든 정확한 이미지 태그 및 알려진 임시 폴더의 Dockerfile만 삭제한 뒤 빈 디렉터리를 rmdir로 제거한다. 이미지 강제 삭제·재귀 폴더 삭제·캐시 prune은 사용하지 않는다. 첫 명령 또는 파일 삭제에 오류가 있으면 후속 정리를 중단하고 결과를 공유하도록 안내한다.

```bash
docker image rm day07-buildargs:lab
rm -- /tmp/day07-buildargs.YTZNch/Dockerfile && rmdir -- /tmp/day07-buildargs.YTZNch
docker image ls day07-buildargs --format 'table {{.Repository}}\t{{.Tag}}\t{{.ID}}'
test ! -e /tmp/day07-buildargs.YTZNch && echo '임시 폴더 정리 완료'
```

- 기대: day07-buildargs 목록에 헤더만 남고 임시 폴더 정리 완료 출력. 아직 사용자 결과는 없으며 삭제 완료로 기록하지 않는다. 이미지 태그·폴더 제거는 빌드 캐시 등 모든 사본 제거를 뜻하지 않는다. 기존 Day 7 컨테이너 4개·네트워크 2개는 계속 유지한다. 7-4는 미시작이다.

### 2026-09-30 — 임시 자원 정리 확인 및 7-3 완료
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: 위 docker image rm·정확한 Dockerfile rm 및 빈 폴더 rmdir·이미지 목록·폴더 부재 검사.
- 사용자 출력: Untagged: day07-buildargs:lab, Deleted: sha256:c8a558367039da731016b0e92eebec645231565df0d28b7629ffd0fa442dc2bd. 이미지 목록에 REPOSITORY TAG IMAGE ID 헤더만 남고 `임시 폴더 정리 완료`가 출력됐다.
- 결과: 이번 임시 이미지 태그와 /tmp/day07-buildargs.YTZNch 폴더 제거 확인. 빌드 캐시 prune·실제 비밀의 복구 불가능한 삭제를 수행한 것은 아니다. [정리 증거](evidence/73-cleanup-user-2026-09-30.txt).
- 완료 판정: 7-3 학습·실습·임시 정리 완료. 사례 1은 프록시 없음→DNS 실패, 지정→200. 사례 2는 no_proxy 없음→내부 API 403·거부 로그, 지정→200·로그 불변. 사례 3은 curl 대문자 HTTP_PROXY만→DNS 실패·exit=6, 소문자→200·exit=0. 사례 4는 빌드 시 전달 개념 및 일반 ARG의 더미 값 히스토리 노출·예약 HTTP_PROXY 미표시 비교를 확인했다.
- 범위 제한: 사례 4에서 실제 빌드 프록시 연결 장애·pip 설치·BuildKit secret mount 사용은 시험하지 않았다. 기존 Compose 서비스·네트워크는 정리 대상으로 지정하지 않았으며 유지한다. 별도 desktop-linux 빌더의 protocol not available 원인은 미해결로 보존한다.
- 확인 주체: 사용자 제공 출력. Codex는 Windows 기록만 갱신했다. Ubuntu 직접 실행·동기화·7-4 시작은 수행하지 않았다.

### 2026-09-30 — 기업 프록시 허용 목록 운영 방식 질의응답
- 사용자 질문: 기업에서는 프록시 허용 목록을 제품 콘솔에서 관리하는지, 이번 실습처럼 터미널로 관리하는지.
- 설명: 제품·운영 방식에 따라 다르다. 상용 보안 프록시는 관리자 웹 콘솔의 URL 범주·허용 정책으로 관리할 수 있고, 직접 운영하는 Squid는 squid.conf의 ACL·http_access 같은 설정으로 관리한다. 지원 제품에서는 API·자동화로 변경을 적용할 수도 있다.
- 실습과 연결: 허용 목적지는 기존 squid.conf의 allowed_sites에 정의돼 있다. 방금 터미널에서 주로 바꾼 HTTP_PROXY·NO_PROXY는 클라이언트의 접속 경로 설정이며 프록시 허용 목록을 추가하는 작업이 아니었다. NO_PROXY에 추가해도 기업 방화벽의 직접 통신 허용 권한이 생기는 것은 아니다.
- 역할 예시: FDE/개발자가 출발지·목적지 도메인·포트·용도·기간을 정리해 요청하고, 고객사 보안·네트워크 운영 담당자가 검토·승인 절차에 따라 정책을 적용하며 개발자는 결과·로그를 검증한다. 실제 담당·권한은 조직마다 다르다.
- 근거: [Zscaler URL 범주 관리](https://help.zscaler.com/zia/adding-custom-url-categories), [Zscaler 허용 목록](https://help.zscaler.com/zia/adding-urls-allowlist), [Squid 접근 제어](https://wiki.squid-cache.org/SquidFaq/SquidAcl). Zscaler의 경로 안내는 공식 검색 결과로 확인했으며 본문 직접 열기는 JavaScript 안내만 반환했다.
- 설명만 진행했다. 정책 변경·외부 서비스 작업·7-4 시작은 수행하지 않았다. 진행 상태는 7-1~7-3 완료로 유지한다.

### 2026-09-30 — 7-4 시작 및 사전 점검 안내(미실행)
- 사용자 요청: 7-4로 진행. PROGRESS·환경·README·SESSION·가이드 7-4와 Compose 구성, bootstrap.sh의 mitmproxy 이미지 태그를 확인했다.
- 목표: mitmweb을 관찰용 프록시로 기동하고 probe에서 명시적으로 해당 프록시를 지정한 공개 HTTP 요청을 보내 브라우저에서 요청·응답을 관찰한다. 기존 agent의 Squid 프록시 설정은 유지한다. 7-5와 Day 8은 이번 요청 범위가 아니다.
- 환경 차이: 가이드 웹 UI 호스트 포트 8081은 사전 기록상 Day 4 pub2가 점유했다. 기존 자원을 변경하지 않고 호스트 127.0.0.1:8082를 사용할 계획이다. 컨테이너 안 웹 UI는 8081, 관찰용 프록시는 8080이다. 실제 8082 가용성·mitm 이름 사용 여부는 아래 결과로 확인한다.
- 안내 실행 위치: Ubuntu WSL2 /home/user/onprem-lab/day07.

```bash
docker image inspect mitmproxy/mitmproxy:11.0.0 --format '{{join .RepoTags ", "}} {{.Os}}/{{.Architecture}}'
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
ss -ltn '( sport = :8082 )'
docker network inspect day07_closed day07_outside --format '{{.Name}} internal={{.Internal}} containers={{range .Containers}}{{.Name}} {{end}}'
```

- 목적: 이미지 로컬 존재, probe 등 기존 서비스 상태, mitm 이름·게시 포트 충돌 및 두 네트워크 상태 확인. ss는 Ubuntu 조회 범위이며 Docker Desktop 전체 호스트 포트 가용성을 단독 보장하지 않는다.
- 실행 여부: 안내만 했으며 결과 대기. mitm 생성·네트워크 연결·포트 게시·설치·다운로드·브라우저 접속은 아직 하지 않았다. 사전 확인 후 기동을 안내한다.

### 2026-09-30 — 7-4 사전 확인 및 버전에 맞춘 mitmweb 기동 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 사용자 사전 출력: mitmproxy/mitmproxy:11.0.0 linux/amd64 존재. Day 7 네 서비스 Up 2 hours, agent healthy. mitm 컨테이너는 목록에 없다. pub2가 8081을 게시하며 Ubuntu ss의 8082 조회는 헤더만 표시됐다. closed에는 기존 네 서비스, outside에는 proxy만 연결됐다. 기존 koica·Day 4 자원은 변경하지 않는다.
- 버전 차이 발견: 가이드의 web_password=lab은 공식 v11.0.0 webaddons.py의 웹 옵션에 없다. 공식 master.py는 인증 토큰 없이 웹 서버 URL을 출력하고 app.py의 IndexHandler는 웹 페이지를 제공한다. 가이드 명령·접속 URL을 그대로 실행하지 않고 v11.0.0에서 지원하는 옵션으로 기동한다. 로컬 이미지의 실제 실행 결과는 후속 출력으로 검증한다.
- 근거: [v11.0.0 웹 옵션](https://github.com/mitmproxy/mitmproxy/blob/v11.0.0/mitmproxy/tools/web/webaddons.py), [서버 기동](https://github.com/mitmproxy/mitmproxy/blob/v11.0.0/mitmproxy/tools/web/master.py). 가이드 원문은 수정하지 않는다.
- 기동 계획: 웹 UI만 호스트 127.0.0.1:8082→컨테이너 8081로 게시, 프록시 8080은 호스트에 게시하지 않는다. outside에서 기동 후 closed를 추가한다. 컨테이너 내 브라우저 자동 실행은 끈다. 7-4가 끝나면 이 관찰용 컨테이너를 정리한다.
- 다음 안내(미실행): 아래를 한 줄/명령씩 실행하고 오류 시 중단해 공유한다.

```bash
docker run -d --rm --pull never --name mitm --network day07_outside \
  -p 127.0.0.1:8082:8081 \
  mitmproxy/mitmproxy:11.0.0 mitmweb \
  --web-host 0.0.0.0 --web-port 8081 \
  --set block_global=false --set web_open_browser=false
docker network connect day07_closed mitm
docker inspect mitm --format 'status={{.State.Status}} networks={{range $name, $config := .NetworkSettings.Networks}}{{$name}} {{end}} ports={{json .NetworkSettings.Ports}}'
docker logs --tail 20 mitm
```

- 기대: mitm running, day07_closed·day07_outside 소속, 호스트 127.0.0.1:8082의 8081 게시, 프록시 및 웹 서버 리스너 시작 로그. 아직 결과를 받지 않았다. 요청 전송·브라우저 화면 관찰도 미진행이다. 향후 브라우저 주소는 http://localhost:8082/이며 가이드의 token 쿼리는 사용하지 않는다.

### 2026-09-30 — mitm 기동 확인 및 누락된 closed 연결 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 사용자 실행: 위 docker run 및 inspect·logs. run은 컨테이너 ID 7df28813eb9699af9413f1439fae191ea8609029c00077c87a67288fbd6e0d0b를 반환했다.
- inspect 출력: status=running, networks=day07_outside만 표시. 8081/tcp의 HostIp=127.0.0.1, HostPort=8082. 로그에는 `usermod: no changes`만 있다.
- 판단: 컨테이너 실행 및 호스트 웹 포트 매핑은 확인했다. 사용자 제공 명령에 network connect가 없고 실제 소속에도 closed가 없어 두 네트워크 연결은 미완료다. 로그만으로 프록시·웹 애플리케이션 리스너 준비를 확인한 것은 아니다.
- 확인 주체: 사용자 제공 출력. Codex 직접 Ubuntu 실행 아님.
- 다음 안내(미실행): 아래 연결 후 실제 소속을 조회한다. 기존 컨테이너를 재사용하고 새로 만들지 않는다.

```bash
docker network connect day07_closed mitm
docker inspect mitm --format 'status={{.State.Status}} networks={{range $name, $config := .NetworkSettings.Networks}}{{$name}} {{end}}'
```

- 기대: running 및 day07_closed·day07_outside 두 소속. 결과 확인 후 probe를 통한 실제 HTTP 요청 및 웹 화면을 검증한다. 아직 요청·화면 관찰은 미진행이다.

### 2026-09-30 — mitm 양쪽 연결 확인 및 HTTP 요청·화면 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: `docker network connect day07_closed mitm` 및 위 소속 inspect.
- 사용자 출력: `status=running networks=day07_closed day07_outside`.
- 결과: mitm 실행 및 두 네트워크 소속 확인. 아직 실제 HTTP 전달·브라우저 화면 검증은 하지 않았다. 확인 주체는 사용자 출력이며 Codex 직접 Ubuntu 실행 아님.
- 다음 안내(미실행): probe에서 프록시를 명시해 공개 HTTP 요청을 보낸다. --noproxy의 빈 문자열로 probe의 우회 환경변수보다 명시한 프록시 사용을 우선하도록 한다. 기존 agent의 프록시 설정은 변경하지 않는다.

```bash
docker compose exec -T probe curl --noproxy '' -x http://mitm:8080 -sS --max-time 15 -o /dev/null -w 'via mitm: %{http_code}\n' http://example.com
```

- 기대: via mitm: 200. 성공한 경우 Windows 브라우저에서 http://localhost:8082/를 열고 example.com의 GET 요청·상태 200 행이 보이는지 확인하도록 안내한다. 포트 8082는 웹 UI, mitm:8080은 프록시 접속 주소다. 가이드의 token 쿼리는 사용하지 않는다.
- 실행 결과: 아직 없다. 요청 실패 시 브라우저 관찰 완료로 간주하지 않고 오류를 확인한다. 요청 행 확인 뒤 상세 Request·Response 등 화면을 관찰할 예정이다. HTTPS·인증서 설치는 아직 수행하지 않았다. 7-4 전체 완료·정리는 미진행이다.

### 2026-09-30 — mitm 경유 HTTP 성공 및 웹 상세 관찰 안내
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07.
- 실행 명령: `docker compose exec -T probe curl --noproxy '' -x http://mitm:8080 -sS --max-time 15 -o /dev/null -w 'via mitm: %{http_code}\n' http://example.com`.
- 사용자 출력: `via mitm: 200`.
- 결과: 명시한 mitm:8080 프록시를 경유한 공개 HTTP 요청 성공. 브라우저 접속·요청 목록·헤더·본문 화면은 아직 확인하지 않았다. Codex가 Ubuntu나 브라우저를 직접 조작한 결과가 아니다.
- 다음 안내(미관찰): Windows 브라우저에서 http://localhost:8082/를 열고 example.com의 GET·200 행을 선택한다. Request에서 Host·User-Agent 등 요청 헤더, Response에서 200·응답 헤더·Example Domain 본문을 확인하도록 안내한다. Timing이나 상세 연결 정보의 실제 UI 위치는 화면을 받은 뒤 확인한다.
- 관찰 구분: 이번 흐름은 probe의 curl→mitm→example.com이다. agent의 요청이나 기존 Squid 허용 정책 검증으로 기록하지 않는다. 실제 인증 정보나 Authorization 헤더를 추가하는 요청은 하지 않았다. HTTP 요청이므로 TLS 인증서 설치도 없다.
- 다음 완료 조건: 사용자의 요청 목록·상세 화면 관찰 결과를 확인한 뒤 7-4 관찰 정리와 mitm 컨테이너 종료를 안내한다. 아직 화면 관찰·정리·7-4 완료로 기록하지 않는다.

### 2026-09-30 — 사용자 제공 Request 탭 내용 확인
- 확인 자료: 사용자가 mitmweb Request 탭 내용을 텍스트로 붙여넣었다. Codex의 브라우저 직접 조작·스크린샷 검증 결과가 아니다.
- 요청: GET http://example.com/ HTTP/1.1. 헤더는 Host: example.com, User-Agent: curl/8.7.1, Accept: */*, Proxy-Connection: Keep-Alive. 본문 영역은 No content다. Request·Response·Connection·Timing·Comment 탭 이름도 제공됐다.
- 의미: 앞서 probe에서 전송한 curl 요청의 목적지·메서드·요청 헤더를 관찰했다. No content는 이 GET 요청에 요청 본문이 없음을 뜻하며, 외부 응답 본문 부재나 실패를 뜻하지 않는다. GET은 이번 명령에서 본문을 보내지 않았다.
- 다음 안내: 같은 요청의 Response 탭을 눌러 응답 상태 200·응답 헤더·Example Domain 본문을 확인하고 내용을 공유하도록 안내한다. 응답과 Timing 상세 관찰·mitm 정리는 아직 미확인이다.
- 기존 Compose 및 mitm 컨테이너는 유지한다. 새 요청 전송·정책 변경·7-5 진행은 하지 않았다.

### 2026-09-30 — Response 상태·헤더·본문 확인 및 Timing 안내
- 확인 자료: 사용자가 mitmweb Response 탭 내용을 텍스트로 제공했다. Codex 직접 브라우저 조작·스크린샷 검증이 아니다.
- 응답: HTTP/1.1 200 OK, Date Wed, 30 Sep 2026 03:39:16 GMT. Content-Type text/html; charset=utf-8, Transfer-Encoding chunked, Connection keep-alive, Server cloudflare, cf-cache-status HIT 등 헤더를 관찰했다.
- HTML 본문: title은 Example Domain, 문서 예제용 도메인 설명 및 IANA 링크가 있다. 링크를 방문하거나 HTML의 스크립트를 실행하는 작업은 수행하지 않았다.
- 의미: 앞선 curl의 HTTP 200과 화면의 응답 상태가 일치하고 요청/응답 헤더 및 HTML 본문 관찰을 확인했다. 요청의 No content와 응답 본문 존재를 구분했다. 이번 대상은 명시적 프록시를 통과한 공개 HTTP이며 HTTPS 복호화나 CA 설치를 검증한 것은 아니다.
- [관찰 증거](evidence/74-http-observation-user-2026-09-30.txt)에 사용자 제공 Request·Response 핵심 내용과 본문 요약을 보존한다. 전체 HTML 원문 보존이나 실시간 직접 검증으로 표기하지 않는다.
- 다음 안내: 같은 요청의 Timing 탭에 표시되는 시간·단계를 공유하도록 안내한다. 실제 시간 항목은 결과를 보고 해석하며 아직 DNS/TCP/응답 대기 중 어느 단계가 오래 걸렸는지 판단하지 않는다. 이후 관찰용 mitm 정리를 안내할 예정이다.
- 현재 상태: mitm 및 기존 Compose 구성 유지. Timing·mitm 정리·7-4 전체 완료는 아직 미확인이다.

### 2026-09-30 — Timing 관찰 확인 및 mitm 정리 안내
- 확인 자료: 사용자가 mitmweb Timing 탭의 시각·상대 시간을 텍스트로 제공했다. [관찰 증거](evidence/74-http-observation-user-2026-09-30.txt)에 추가했다. 시각은 사용자 UI 표시를 그대로 보존하며 시간대를 별도로 검증하지 않았다.
- 주요 관찰: First request byte 03:39:17.494, Request complete 17.495(+1ms), Server conn. initiated 17.496(+2ms), TCP handshake 17.700(+207ms), First response byte 17.716(+222ms), Response complete 17.717(+223ms).
- 해석: 첫 요청 바이트부터 응답 완료까지 표시상 약 223ms. 서버 연결 시작→TCP 완료는 표시 시각 차이 약 204ms, TCP 완료→첫 응답 약 16ms, 첫 응답→응답 완료 약 1ms. 반올림된 절대 시각과 상대 ms는 약 1ms 차이가 날 수 있다.
- Client conn. established의 -4ms는 기준인 첫 요청 바이트보다 연결이 먼저 맺어졌다는 뜻이며 음수 지연 오류로 해석하지 않는다. 서버 연결 구간이 이번 한 요청에서 큰 비중을 차지하지만 DNS 별도 시각·반복 측정이 없어 TCP RTT나 특정 병목 원인으로 단정하지 않는다.
- 관찰 완료 범위: 명시적 mitm 프록시를 경유한 공개 HTTP 200, Request 헤더, Response 헤더·HTML 본문, Timing을 사용자 출력으로 확인했다. HTTPS/CA 신뢰 문제·인증서 설치·실제 비밀 포함 요청은 시험하지 않았다.
- 다음 안내(미실행): 관찰용 mitm만 정상 종료한다. 생성 시 --rm을 사용했으므로 종료 후 자동 제거를 기대하고 목록·포트와 기존 Compose 서비스 상태를 확인한다.

```bash
docker stop mitm
docker ps -a --filter 'name=^/mitm$' --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
ss -ltn '( sport = :8082 )'
docker compose ps -a
```

- 기대: mitm 목록 및 Ubuntu 8082 리스너 조회에 헤더만 남음, 기존 Day 7 네 서비스 유지. 실제 정리 결과는 아직 받지 않았다. mitm 이미지·다른 프로젝트 자원·Day 7 Compose는 삭제 대상이 아니다. 7-5는 미시작이다.

### 2026-09-30 — mitm 정리 확인 및 7-4 완료
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07. 앞서 안내한 docker stop mitm, 이름 필터 docker ps -a, ss 8082 조회, docker compose ps -a를 사용자가 실행했다.
- 사용자 결과: stop은 mitm을 반환했고 컨테이너 목록과 8082 리스너 조회는 헤더만 표시됐다. --rm으로 생성한 mitm의 종료·자동 제거와 해당 리스너 부재를 확인했다.
- 기존 Compose: agent·internal-api·probe·proxy 네 서비스 모두 Up 2 hours, agent healthy. Compose 전체 종료는 하지 않았다. 이미지 및 다른 프로젝트 자원은 이번 조회·정리 대상이 아니다.
- [정리 증거](evidence/74-cleanup-user-2026-09-30.txt)에 사용자 출력을 보존했다. Codex 직접 Ubuntu 실행 결과가 아니다.
- 7-4는 HTTP 요청·응답·Timing 관찰과 관찰용 컨테이너 정리까지 완료했다. HTTPS/CA 시험은 수행하지 않았다. 7-5·Day 7 전체 정리·자기점검은 아직 미진행이며 다음 절로 자동 진행하지 않는다.

### 2026-09-30 — 7-5 시작: 게이트웨이 설계 개념 설명
- 사용자 요청: 7-5를 시작한다. Codex는 PROGRESS·환경 기록·Day 7 README·SESSION·가이드 7-5를 확인했다. 이번 절은 개념 설명이며 새 Ubuntu 명령이나 컨테이너 변경은 없다.
- 설계: agent → 사내 LLM gateway → 포워드 프록시 → 각 외부 모델 API. agent의 호출 주소를 gateway로 모으고, gateway에서 모델 라우팅·사용량/비용 집계·감사 기록을 구현할 수 있다. 프록시는 외부 통신 중계와 목적지 허용/차단을 담당한다. 실제 gateway 구현은 가이드 Day 13 범위이며 이번 절에서 설치하지 않는다.
- 가이드 보완: gateway 도입만으로 외부 목적지가 하나로 줄어드는 것은 아니다. agent→gateway 구간의 목적지를 단일화해도 gateway가 여러 제공자를 호출하면 gateway→외부 구간에는 각 목적지 허용이 필요하다. 방화벽 협의는 출발지·목적지·포트별로 구분한다. 직접 호출을 막는 네트워크 정책도 있어야 경로를 강제할 수 있다.
- 기록 범위 보완: gateway 로그의 항목·저장 위치·본문 포함 여부는 설정에 달린다. gateway를 세웠다는 이유만으로 모든 요청/응답 본문이 자동 보관된다고 설명하지 않는다.
- 고객사 확인 항목: 프록시 주소·포트·인증 및 PAC 사용 여부, CONNECT 허용 포트, FQDN/와일드카드/IP 허용 단위, 요청·스트리밍 요구에 맞는 타임아웃, 이중화·정책 동기화. PAC 지원은 클라이언트마다 다르므로 컨테이너 애플리케이션의 지원 여부와 사용 가능한 고정 프록시 주소를 확인한다. 300초 같은 값을 일괄 필수 조건으로 보지 않는다.
- 7-5 설명 제공과 사용자 독립 이해도 평가는 구분한다. 실제 고객사 값 수집·방화벽 신청·gateway 배포는 수행하지 않았다. Day 7 전체 정리·자기점검·Day 8 진행도 하지 않았다.

### 2026-09-30 — Day 7 종료 정리 안내(결과 대기)
- 사용자 요청: "그럼 정리하자". 기존 진행 방식대로 사용자가 Ubuntu WSL2에서 직접 실행하도록 안내하며 Codex가 대신 실행하지 않는다.
- 정리 대상: Day 7 Compose 서비스 agent·internal-api·probe·proxy와 closed·outside 네트워크. mitm은 이미 제거 확인했다. 이미지·볼륨 삭제 옵션이나 전역 prune은 사용하지 않는다.
- 안내 명령(미실행, 실행 위치 /home/user/onprem-lab/day07):

```bash
cd /home/user/onprem-lab/day07 && docker compose -p day07 down
docker ps -a --filter label=com.docker.compose.project=day07 --format 'table {{.Names}}\t{{.Status}}'
docker network ls --filter label=com.docker.compose.project=day07
```

- 기대 결과: 컨테이너 4개와 네트워크 2개 제거, 후속 프로젝트 필터 목록에는 헤더만 표시. 결과를 받기 전까지 종료 완료로 기록하지 않는다. 별도 자기점검 6문항은 미진행으로 유지한다.

### 2026-09-30 — Day 7 정리 확인 및 종료
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day07. 사용자가 앞서 안내한 docker compose -p day07 down 및 프로젝트 필터 컨테이너·네트워크 조회를 실행했다.
- 결과: internal-api·proxy·agent·probe 컨테이너 4개와 day07_closed·day07_outside 네트워크 2개가 Removed로 표시됐다. 후속 조회 두 목록에는 헤더만 남았다.
- [종료 정리 증거](evidence/cleanup-user-2026-09-30.txt)에 사용자 출력을 보존했다. Codex 직접 Ubuntu 실행·동기화는 하지 않았다. 이미지·볼륨 삭제 옵션 및 전역 prune은 사용하지 않았고 다른 프로젝트 자원은 재조회하지 않았다.
- 완료 범위: 7-1~7-4 실습, 7-5 설계 개념 설명·질의응답, 임시 빌드 이미지·폴더 및 mitm 정리, 최종 Compose 자원 정리. 별도 자기점검 6문항은 미실시다. 7-3 사례 4는 빌드 인자 히스토리 비교이며 실제 빌드 프록시 통신 장애 재현은 아니다. 7-4 HTTPS/CA 시험·7-5 실제 gateway 구축은 수행하지 않았다.
- 남은 환경 관찰: buildx ls의 별도 desktop-linux 항목 protocol not available 원인은 미확정으로 유지한다. default 빌더로 수행한 이번 실습은 성공했다.
- Windows의 PROGRESS·README·환경 기록을 종료 상태로 갱신한다. 다음은 사용자 요청 후 Day 8이며 이번 세션에서 자동 시작하지 않는다. Git 커밋·푸시·PR 생성·병합은 이번 종료 기록 작업에서 수행하지 않는다.

### 2026-09-30 — 사용자 완료 확인 및 저장소 push 요청
- 사용자 요청: Day 7을 완료하고 저장소에 push한다. 기존 codex/day07-results 브랜치에서 학습 기록·환경 차이·사용자 실행 증거를 커밋해 origin에 반영하는 범위다. main 병합·Day 8 실습은 이번 요청에 포함하지 않는다.
- Codex 직접 확인: 원격 fetch 후 현재 브랜치 시작점과 origin/main이 b3a34c5로 같음을 확인했다. 변경 대상은 PROGRESS.md, day07/README.md, day07/SESSION.md, docs/environment.md와 day07/evidence의 텍스트 7개다. 실습 소스 변경은 없다.
- 완료 판정: 사용자가 학습 완료를 확인했다. 7-1~7-5 및 자원 정리·체크포인트 해설 완료와 독립 답변 평가 미실시를 구분한다. Windows 기록만 반영하며 Ubuntu 실습을 재실행하지 않는다.
## 오류와 해결
- 주요 실습 오류와 비교 결과는 위 실행 기록에 보존했다. 프록시·NO_PROXY 누락과 curl 변수 대소문자는 설정 비교로 복구를 확인했다. mitm의 closed 연결 누락은 network connect 후 통신 성공으로 확인했다. 별도 desktop-linux 빌더 조회 오류는 원인 미확정으로 남긴다.

## 배운 내용과 질문
### 2026-09-30 — 7-5 게이트웨이 질의응답
- 사용자는 게이트웨이가 파일인지, 프록시 관리자인지, 프록시에 요청을 보내는지 질문했다. LLM 게이트웨이는 설정 파일을 읽어 실행되는 서비스이며, 모델 호출을 처리하고 프록시가 필요한 환경에서는 프록시를 통해 외부 API에 요청한다고 설명했다. 프록시 정책 관리와는 별도 역할이며, 직접 통신이 허용된 환경에서는 프록시 없이도 동작할 수 있다.
- 제품 여부와 사례 질문: 게이트웨이는 역할·제품군 이름이며 직접 구현하거나 기존 소프트웨어·서비스를 사용할 수 있다. 공식 자료로 LiteLLM Proxy Server(자체 서버·컨테이너에서 운영하는 LLM 게이트웨이), Kong AI Gateway, Azure API Management의 AI 게이트웨이 기능을 확인해 소개했다. 이번 가이드의 Day 13 대상은 LiteLLM이다. 설치·구매·제품 선정은 수행하지 않았다.
- 공식 참고: [LiteLLM](https://docs.litellm.ai/docs/), [Kong AI Gateway](https://developer.konghq.com/ai-gateway/), [Azure API Management](https://learn.microsoft.com/en-us/azure/api-management/api-management-key-concepts). LiteLLM의 Proxy Server라는 명칭은 LLM 요청 중계를 뜻하며 이번 Squid 포워드 프록시와 담당 범위가 다르다고 설명한다.

### 2026-09-30 — 체크포인트 6문항 해설 및 Day 7 복습
- 사용자 요청으로 실제 실습 결과와 연결한 답변을 제공했다. 이는 해설 제공 기록이며 사용자 독립 답변 평가·통과로 처리하지 않는다. 새 Ubuntu 명령 실행·컨테이너 기동은 없다.
- 전체 흐름: closed에 agent·probe·internal-api를 두고 closed/outside 양쪽의 Squid를 외부 출구로 구성했다. example.com HTTP/HTTPS 허용과 google.com 거부, 내부 API 직접 호출을 확인했다. 설정 누락·대소문자 실패 및 복구, 빌드 인자 히스토리, mitmweb HTTP 관찰, gateway 개념을 학습하고 자원을 정리했다.
- 1번: 일반 CONNECT 터널에서 프록시는 목적지 호스트·포트, 연결 시간·전송량 등 메타데이터를 알지만 TLS 내부의 URL 경로·쿼리·Authorization·요청/응답 본문을 읽지 못한다. TCP_TUNNEL/200의 200은 터널 수립 응답이며 원 서버 HTTP 응답 코드와 다르다. TLS 검사로 중간에서 TLS를 종료하는 구성은 별도이고 이번 Squid 실습에서는 수행하지 않았다. mitmweb 본문 관찰 대상은 HTTP였다.
- 2번: 프록시 설정이 있는 상태에서 NO_PROXY를 누락하면 내부 HTTP 요청까지 프록시에 전달될 수 있다. 실습은 internal-api가 허용 목록에 없어 403, no_proxy=internal-api 추가 후 직접 호출 200·로그 불변이었다. 일반적인 DB 드라이버의 DB 프로토콜 연결은 HTTP 프록시 환경변수를 따르지 않아 DB와 내부 HTTP API의 결과가 다를 수 있다. 이번 Day 7에서 DB 연결 자체를 시험한 것은 아니다. NO_PROXY는 프록시 우회 설정이며 방화벽 허용을 대신하지 않는다.
- 3번: Compose environment는 실행 컨테이너 설정이고 Dockerfile RUN의 빌드 환경에 자동 전달되지 않는다. 빌드에는 예약 --build-arg HTTP_PROXY/HTTPS_PROXY/NO_PROXY 등을 별도로 전달할 수 있다. 실제 실습에서 선언한 ARG PIP_INDEX_URL의 공개 더미 값은 history에 남았고 선언·참조하지 않은 예약 HTTP_PROXY는 표시되지 않았다. 예약 인자도 Dockerfile에서 ARG로 선언하거나 값을 파일·출력에 남기면 보호 범위가 달라지므로 비밀 전달에는 BuildKit secret mount를 사용한다. 실제 pip 설치 장애는 재현하지 않았다.
- 4번: 이번 HTTP google.com 요청은 Squid가 일반 HTTP 요청에 403을 반환해 HTTPError 403이었다. HTTPS는 CONNECT google.com:443 요청부터 거절돼 OSError: Tunnel connection failed: 403이었다. 원 서버로의 TLS 통신 전에 실패해 앱 status가 null이었다. TCP_DENIED/403 로그로 둘 다 Squid 정책 거부임을 확인했다. 다른 환경의 HTTP 403까지 모두 프록시 거부라고 단정하지 않는다.
- 5번: agent의 호출 목적지를 사내 gateway로 통일하면 agent 구간 방화벽 신청과 모델 변경·사용량/감사 관리의 접점을 줄일 수 있다. gateway가 여러 외부 제공자를 호출하면 gateway 이후의 외부 허용 목록은 여전히 필요하다. 실제 배포 대신 설계 설명을 진행했다.
- 6번: HTTP_PROXY는 모든 프로그램을 강제로 변경하는 OS 설정이 아니다. Node.js는 버전·사용 클라이언트에 따라 지원이 다르며 지원 버전에서는 NODE_USE_ENV_PROXY=1 또는 --use-env-proxy로 내장 프록시 기능을 활성화한다. 공식 문서 기준 환경변수 옵션은 v24.0.0 및 v22.21.0에 추가됐고 http/https 모듈 내장 지원은 v24.5.0에 추가됐다. 구버전 fetch/Undici에서는 호환되는 EnvHttpProxyAgent를 dispatcher로 연결하는 방식이 있다. 사용자 설치 Node 버전·Java 버전은 이번에 조회하지 않았으며 실행 예시는 설명용이다.
- Java 표준 네트워킹은 일반적으로 HTTP_PROXY를 자동 적용하지 않으므로 -Dhttp.proxyHost/-Dhttp.proxyPort, -Dhttps.proxyHost/-Dhttps.proxyPort와 -Dhttp.nonProxyHosts를 사용하거나 HTTP 클라이언트에 프록시를 명시한다. nonProxyHosts는 세로줄 구분이며 표준 HTTPS 핸들러도 같은 속성을 사용한다. 서드파티 클라이언트는 설정 방식이 다를 수 있다.
- 공식 근거: [Squid CONNECT](https://wiki.squid-cache.org/Features/HTTPS), [Docker proxy arguments](https://docs.docker.com/build/building/variables/#proxy-arguments), [Dockerfile predefined ARGs](https://docs.docker.com/reference/dockerfile/#predefined-args), [Node 환경변수](https://nodejs.org/api/cli.html#node_use_env_proxy1), [Node v24 HTTP 프록시](https://nodejs.org/download/release/latest-v24.x/docs/api/http.html#built-in-proxy-support), [Undici EnvHttpProxyAgent](https://github.com/nodejs/undici/blob/main/docs/docs/api/EnvHttpProxyAgent.md), [Java networking](https://docs.oracle.com/en/java/javase/17/core/java-networking.html).
## 가이드와 실제 환경의 차이
공통 환경은 [환경 기록](../docs/environment.md)을 참고한다.

## 다음에 이어 할 지점
Day 7 학습·정리 완료 및 종료. 체크포인트 6문항 해설을 제공했으며 사용자 독립 답변 평가는 미실시로 남긴다. Day 7 컨테이너·네트워크와 관찰용 mitm은 제거 확인했다. 다음은 사용자 요청 후 Day 8 사내 CA와 TLS 검사 학습이며 아직 시작하지 않았다. Windows 기록과 Ubuntu 실습 사본은 별개다.
