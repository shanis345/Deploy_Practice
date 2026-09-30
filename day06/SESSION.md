# Day 6 — 망분리 재현: DMZ · 업무망 · DB존, 그리고 방화벽 신청서

## 진행 상태
- 상태: 종료(2026-09-30) · 6-1~6-3·6-4 학습용 초안 작성 및 설명·화면 관찰·누적 장애 5개 복구·자원 정리 완료. 별도 자기점검·독립 진단 평가는 미실시
- 완료한 범위: 3존 구성·7개 통신 경로 검증·DMZ 추가 실수 재현과 원복. 6-2 ③은 DB IP 직접 시험도 추가했고 ⑤는 실제 agent에서 실행했다.
- 종료 지점: 사용자 출력으로 컨테이너 7개·네트워크 3개 제거, 프로젝트 잔존 목록 없음·8080 리스너 부재 확인
- Codex 작업: 아직 별도 작업을 만들지 않음
- 실행 증거 기준: 사용자 제공 출력과 직접 검증 결과를 구분해 기록

## 목표와 이번 세션 범위
2026-09-29 6-1~6-3을 완료했고 사용자 요청으로 6-4 학습용 방화벽 신청서 초안 작성·설명까지 진행했다. Ubuntu WSL2 실습 명령은 사용자가 직접 실행했고 Codex는 Windows 기록과 초안을 작성했다. 고객사 제출·실제 방화벽 정책 적용은 하지 않았다.

2026-09-30 사용자 요청으로 화면 관찰·누적 장애 5개의 재현과 안내에 따른 진단·복구·학습 요약·자원 정리까지 마쳤다. 아래 실행 기록의 미확인·대기 문구는 각 단계 당시 상태이며 후속 확인 기록과 함께 읽는다.

## 실행 기록
### 2026-09-29 — 6-1 사전 확인 안내
- Codex 직접 확인: Windows의 PROGRESS.md·환경 기록·Day 6 README/SESSION·가이드 원문·compose.yaml·gateway.conf를 읽었다. Windows 작업 트리는 기록 수정 전 깨끗했다.
- Windows SHA-256: compose.yaml `1c2e71cf3ac308e285d14ed3a2a3ab5d7dd7f0db86a82294b610bad4e69db3cb`, gateway.conf `a42b9bf44c67636c41a44a87e38b476a594afe97565dfbf2c5bc59e0393e2ef8`, break.sh `bcfb82849dcdab259bde2babeff19a0dbaaee1afe08e648fd80f6ab33e0db5a3`.
- 아래 명령은 사용자에게 안내한 사전 점검이며 아직 실행 결과를 받지 않았다. Ubuntu 파일 일치·Docker 상태·포트·이미지 존재는 미확인이다. 설치·동기화·컨테이너 생성은 수행하지 않았다.
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day06`.

```bash
cd /home/user/onprem-lab/day06
pwd
ls -l compose.yaml gateway.conf break.sh
sha256sum compose.yaml gateway.conf break.sh
docker version
docker compose version
docker compose config --quiet && echo "Compose 문법 OK"
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
ss -lnt 'sport = :8080'
docker image inspect nginx:1.27-alpine agent:0.2.0 traefik/whoami:v1.10 postgres:16.4-alpine nicolaka/netshoot:v0.13 --format '{{join .RepoTags ", "}} | {{.Os}}/{{.Architecture}}'
```

### 2026-09-29 — 사전 점검 통과 및 기동 안내
- 확인 주체: 사용자 제공 Ubuntu 출력과 Windows 파일의 대조. [사전 점검 증거](evidence/precheck-user-2026-09-29.txt).
- 파일 3개의 SHA-256이 Windows 사본과 일치한다. break.sh는 Ubuntu에서 755이며 Windows 바이트 직접 확인 결과 CR=0·LF=22이므로 일치하는 Ubuntu 사본도 LF다.
- Docker Client/Engine 29.8.0, Desktop 4.92.0(240144), Compose v5.5.1 및 Compose 문법 검사 성공을 확인했다.
- nginx:1.27-alpine·agent:0.2.0·traefik/whoami:v1.10·postgres:16.4-alpine·nicolaka/netshoot:v0.13 모두 로컬에 있으며 linux/amd64다.
- Ubuntu ss에 8080 리스너 행이 없고 Docker 목록에도 8080 게시가 없다. 기존 pub2는 8081을 게시 중이며 web·web2도 실행 중이다. pub·isolated·client·client2·koica 앱은 중지 상태로 남아 있다. 기존 자원은 변경하지 않았다.
- 다음은 아래 명령을 사용자가 실행할 차례다. 아직 기동 출력은 받지 않았으며 6-1 완료로 처리하지 않는다. 기존 이미지로 기동하도록 --pull never를 사용한다.

```bash
docker compose up -d --pull never
sleep 15
docker compose ps -a
docker network inspect day06_dmz day06_biz day06_dbzone --format '{{.Name}} internal={{.Internal}} containers={{range .Containers}}{{.Name}} {{end}}'
```

### 2026-09-29 — 6-1 완료
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day06`. 실행 명령은 바로 위 기동 안내와 같으며 사용자가 실행했다.
- 확인 주체: 사용자 제공 출력. [기동 증거](evidence/startup-user-2026-09-29.txt). Codex는 Ubuntu에서 직접 실행하거나 재조회하지 않았다.
- up 10/10으로 네트워크 3개 생성과 컨테이너 7개 시작을 확인했다. ps에서 7개 모두 Up, agent와 postgres는 healthy다. gateway만 `127.0.0.1:8080->80/tcp`를 게시한다.
- day06_dmz는 internal=false이며 gateway·probe-dmz, day06_biz는 internal=true이며 gateway·erp·agent·probe-biz, day06_dbzone은 internal=true이며 agent·postgres·probe-db가 연결돼 있다. 기대한 소속과 일치한다.
- 결과: 6-1 완료. 네트워크 설정과 실행 상태를 확인한 것이며 HTTP·DB TCP·외부 통신 차단 등 6-2의 기능 시험은 아직 하지 않았다. Day 6 전체 완료와 구분한다.
- 자원 상태: Day 6 컨테이너·네트워크는 실행 상태로 유지한다. 정리 명령은 안내·실행하지 않았다. 기존 Day 4·koica 자원은 변경하지 않았다.

### 2026-09-29 — 6-2 시작, ①② 안내
- 사용자 후속 요청으로 6-2를 시작한다. Windows 기록·가이드 6-2 및 agent/app.py의 엔드포인트를 확인했다. 아래 명령은 안내만 했으며 아직 실행 출력이 없다.
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day06`.
- ① Ubuntu에서 127.0.0.1:8080의 gateway를 거쳐 agent의 healthz를 조회한다. 실제 외부 인터넷에서 접근하는 시험은 아니다.
- ② 같은 HTTP 경로로 agent에게 postgres:5432 TCP 연결을 시도하도록 요청한다. Ubuntu가 직접 DB에 연결하는 시험이나 DB 인증·SQL 시험과 구분한다.

```bash
curl -fsS --max-time 10 'http://127.0.0.1:8080/healthz' | jq .
curl -fsS --max-time 10 'http://127.0.0.1:8080/tcp?host=postgres&port=5432' | jq .
```

#### 6-2 통신 검증표
| 항목 | 실제 시험 경로 | 결과 |
|---|---|---|
| ① | Ubuntu → gateway → agent /healthz | 성공: status=ok, version=0.2.0 |
| ② | agent → postgres:5432 | 성공: ok=true, elapsed_ms=1 |
| ③ | probe-dmz → postgres:5432 | 이름 해석 실패, IP 172.22.0.4:5432도 3초 타임아웃·종료코드 1 |
| ④ | probe-biz → 인터넷 | example.com DNS 실패·코드 1, IPv4 내부 경로만 존재·default 없음 |
| ⑤ | agent → erp:8080 (실제 agent에서 실행) | HTTP 200·Name: erp-api, RemoteAddr=172.21.0.3:57002 |
| ⑥ | agent → 인터넷 | ok=false·gaierror·Temporary failure in name resolution·8ms |
| ⑦ | probe-db → agent:8000 | 172.22.0.3:8000 TCP succeeded·종료코드 0 |

### 2026-09-29 — 6-2 ①② 확인 및 ③ 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. [①② 증거](evidence/connectivity-01-02-user-2026-09-29.txt).
- ① gateway 경유 healthz에서 status=ok·version=0.2.0·host=b03497230cb3를 확인했다. 실제 외부 인터넷 진입 시험은 아니다.
- ② agent의 postgres:5432 TCP 연결은 ok=true·elapsed_ms=1이다. DB 인증·SQL·영속성 시험은 아니다.
- 다음 명령은 Ubuntu `/home/user/onprem-lab/day06`에서 probe-dmz의 이름 기반 DB 접근을 확인하도록 안내했다. 아직 실행 결과는 없으며 DNS 실패만으로 DB IP 직접 접속도 차단됐다고 판정하지 않는다.

```bash
docker compose exec -T probe-dmz sh -c 'nc -z -v -w3 postgres 5432; result=$?; printf "종료코드=%s\n" "$result"'
```

### 2026-09-29 — 6-2 ③ DNS 실패 확인 및 IP 직접 시험 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. [③ DNS 증거](evidence/connectivity-03-dns-user-2026-09-29.txt).
- probe-dmz에서 postgres 이름으로 nc 실행 시 getaddrinfo의 Try again과 종료코드 1을 확인했다. DMZ와 DB가 네트워크를 공유하지 않는 구성에서 예상한 이름 기반 접속 실패다. 이 출력은 DNS 실패를 나타내며, 실제 DB IP로 TCP 연결까지 시도한 결과는 아니다.
- 아래 명령을 Ubuntu `/home/user/onprem-lab/day06`에서 실행하도록 안내했다. DB IP는 실행 중인 컨테이너의 dbzone 인터페이스에서 조회하며 고정값으로 추정하지 않는다. 명령 안내만 했고 직접 시험 결과는 아직 없다.

```bash
db_ip=$(docker inspect day06-postgres-1 --format '{{(index .NetworkSettings.Networks "day06_dbzone").IPAddress}}')
printf 'DB IP=%s\n' "$db_ip"
docker compose exec -T probe-dmz sh -c 'nc -z -v -w3 "$1" 5432; result=$?; printf "종료코드=%s\n" "$result"' sh "$db_ip"
```

### 2026-09-29 — 6-2 ③ IP 직접 시험 확인 및 ④ 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. [③ IP 직접 시험 증거](evidence/connectivity-03-ip-user-2026-09-29.txt).
- postgres의 dbzone IP는 172.22.0.4다. probe-dmz에서 해당 IP의 TCP 5432로 nc -w3 실행 시 timed out: Operation in progress·종료코드 1을 확인했다. 이름 기반 재시도도 getaddrinfo Try again·종료코드 1이었다.
- 결과: DNS를 우회해도 해당 경로로 TCP 연결이 성립하지 않아 ③의 예상한 접근 제한을 확인했다. 앞선 ②에서는 agent→postgres:5432가 성공했다. 특정 방화벽 규칙·패킷 폐기 위치를 직접 검증한 것은 아니다.
- 다음은 Ubuntu `/home/user/onprem-lab/day06`에서 아래 ④ 명령을 실행하도록 안내했다. 아직 실행 결과는 없다. 연결 실패 형태와 라우팅을 함께 확인하며 DNS 실패만으로 IP 기반 외부 통신 차단까지 판정하지 않는다.

```bash
docker compose exec -T probe-biz sh -c 'nc -z -v -w3 example.com 80; result=$?; printf "종료코드=%s\n" "$result"; ip route'
```

### 2026-09-29 — 6-2 ④ 확인 및 ⑤ 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. [④ 증거](evidence/connectivity-04-user-2026-09-29.txt).
- probe-biz에서 example.com:80 시험은 getaddrinfo Try again·종료코드 1이다. ip route에는 `172.21.0.0/16 dev eth0 proto kernel scope link src 172.21.0.2`만 있고 default가 없다.
- 결과: 가이드 ④의 외부 이름 기반 접속 실패와 IPv4 기본 경로 부재를 확인했다. 외부 IP 직접 연결이나 IPv6 전체를 검증한 것은 아니다. 내부 대역 통신은 유지될 수 있다.
- 가이드 ⑤는 제목이 agent→ERP이나 명령은 probe-biz에서 실행한다. 이번에는 실제 출발지를 agent로 맞춰, 이미 설치된 Python 표준 라이브러리로 직접 HTTP 요청하도록 안내했다. 별도 설치·파일 수정은 필요 없다.
- 실행 위치: Ubuntu `/home/user/onprem-lab/day06`. 아래 명령은 안내만 했고 실행 결과는 아직 없다.

```bash
docker compose exec -T agent python -c 'import urllib.request; r = urllib.request.urlopen("http://erp:8080", timeout=5); print("HTTP", r.status); print(r.read().decode())'
```

### 2026-09-29 — 6-2 ⑤ 성공 및 ⑥ 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. [⑤ 증거](evidence/connectivity-05-user-2026-09-29.txt).
- agent 내부 Python에서 erp:8080을 요청해 HTTP 200·Name: erp-api를 확인했다. ERP는 Hostname=a175214f01f1·IP=172.21.0.5를 보고하며 요청 출발지는 RemoteAddr=172.21.0.3:57002다. 같은 업무망의 agent→ERP HTTP 통신 성공으로 ⑤를 확인했다.
- ⑥은 gateway 경유 /egress 엔드포인트로 agent에게 example.com HTTP 요청을 지시한다. Codex가 확인한 Windows app.py는 외부 접속 실패도 HTTP 200의 JSON으로 반환하므로 결과 본문의 ok·error_type·error를 확인해야 한다. 실제 실행 중 이미지의 전체 소스 일치를 이번에 다시 검증한 것은 아니다.
- 아래 명령은 Ubuntu `/home/user/onprem-lab/day06`에서 실행하도록 안내만 했고 아직 출력이 없다.

```bash
curl -fsS --max-time 20 'http://127.0.0.1:8080/egress?url=http://example.com&timeout=5' | jq .
```

### 2026-09-29 — 6-2 ⑥ 확인 및 ⑦ 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. [⑥ 증거](evidence/connectivity-06-user-2026-09-29.txt).
- agent의 example.com 요청은 ok=false·error_type=gaierror·[Errno -3] Temporary failure in name resolution·elapsed_ms=8이다. 외부 요청이 이름 해석 단계에서 실패했다. 모든 외부 IP·포트 차단을 직접 시험한 것으로 해석하지 않는다.
- 마지막 ⑦은 DB존의 probe-db가 agent:8000으로 새 TCP 연결을 시작하는 시험이다. 앞서 agent가 시작한 DB 연결의 응답 패킷과 구분한다. 두 컨테이너가 dbzone을 공유하므로 현재 Docker 구성에서는 연결 성공이 예상된다. 방향별 신규 연결 정책을 구현한 실제 방화벽과의 차이를 확인하는 목적이다.
- 실행 위치: Ubuntu `/home/user/onprem-lab/day06`. 아래 명령은 안내만 했고 아직 출력이 없다.

```bash
docker compose exec -T probe-db sh -c 'nc -z -v -w3 agent 8000; result=$?; printf "종료코드=%s\n" "$result"'
```

### 2026-09-29 — 6-2 ⑦ 확인 및 절 완료
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day06`. 실행 명령은 바로 위 ⑦ 안내와 같다.
- 확인 주체: 사용자 제공 출력. [⑦ 증거](evidence/connectivity-07-user-2026-09-29.txt).
- probe-db→agent(172.22.0.3):8000은 succeeded·종료코드 0이다. DB존에서 agent로 새 TCP 연결을 시작할 수 있음을 확인했다.
- 의미: 두 컨테이너가 dbzone을 공유하며 현재 구성에는 이 신규 연결 방향을 차단하는 별도 정책이 없다. 네트워크 분리만으로 실제 방화벽의 출발지·목적지·포트·방향별 정책까지 구현한 것은 아니다. 상태 추적 방화벽에서 허용된 기존 연결의 응답을 허용하는 것과 반대 방향 신규 연결 허용은 다르다.
- 완료 판정: 6-2의 7개 경로 결과를 확인하고 위 검증표에 기록했다. ①②⑤⑦은 성공, ③은 DNS 실패 및 DB IP TCP 타임아웃, ④는 외부 DNS 실패와 IPv4 기본 경로 부재, ⑥은 agent 외부 DNS 실패다. 모든 외부 IP·IPv6·DB 인증·SQL을 시험했다고 확대 해석하지 않는다.
- 6-1·6-2 완료이며 Day 6 전체 완료는 아니다. 6-3 설정 실수 재현·6-4 신청서·누적 점검·정리는 미진행이다. 실습 컨테이너와 네트워크를 유지한다. Codex가 Ubuntu를 직접 실행하거나 소스를 동기화하지 않았다.

### 2026-09-29 — 6-3 시작 및 백업 안내
- 승인 범위: agent에 dmz를 추가해 외부 연결 변화를 관찰하고 원래 biz·dbzone 구성으로 복구한다. 6-4 이후로 넘어가지 않는다.
- Codex는 Windows 기록·가이드 6-3·compose.yaml을 읽었다. Windows 실습 소스는 변경하지 않았다. Ubuntu 사본을 사용자가 직접 수정할 예정이며 자동 동기화하지 않는다.
- 첫 단계는 현재 agent의 Compose 설정·실제 네트워크와 실행 상태를 조회하고 compose.yaml을 고유한 임시 경로에 백업하는 것이다. 기존 백업을 덮어쓰지 않도록 mktemp를 사용한다. 아직 출력이 없으므로 백업 생성·현재 설정 일치는 미확인이다.
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day06`.

```bash
cd /home/user/onprem-lab/day06
docker compose ps agent
docker compose config --format json | jq '.services.agent.networks'
docker inspect day06-agent-1 --format '{{range $name, $config := .NetworkSettings.Networks}}{{$name}} {{end}}'
day06_backup=$(mktemp /tmp/day06-compose.XXXXXX) && cp -p compose.yaml "$day06_backup" && printf '백업 파일: %s\n' "$day06_backup" && sha256sum compose.yaml "$day06_backup"
```

- 다음 단계에서 백업 경로와 원본 해시를 확인한 뒤 agent 네트워크만 변경한다. 기동·설정 변경 명령은 아직 안내하지 않았다.

### 2026-09-29 — 6-3 백업 확인 및 DMZ 추가 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. [사전 확인·백업 증거](evidence/63-backup-user-2026-09-29.txt).
- agent는 Up 6 hours (healthy)다. Compose 설정은 biz·dbzone만 있고 실제 연결도 day06_biz·day06_dbzone이다.
- 백업 경로는 `/tmp/day06-compose.OTTiFi`이며 compose.yaml과 모두 SHA-256 `1c2e71cf3ac308e285d14ed3a2a3ab5d7dd7f0db86a82294b610bad4e69db3cb`로 일치한다. 원복 시 이 백업을 사용한다.
- 다음 명령은 Ubuntu `/home/user/onprem-lab/day06`에서 agent의 networks 행에만 dmz를 추가하도록 안내했다. Linux sed로 수정하므로 LF를 유지한다. Windows 소스는 수정하지 않았다.
- diff에서 networks 행 한 줄만 바뀐 것을 확인한 뒤 적용하도록 안내했다. 다른 변경이나 오류가 있으면 멈추고 출력을 공유한다. diff의 종료코드 1은 차이가 있다는 정상 표시다.
- 기존 이미지로 agent만 재생성한다. 이후 networks·healthy·gateway 경유 healthz와 외부 HTTP 요청을 관찰한다. 아래 명령은 안내만 했고 적용 결과는 아직 없다.

```bash
sed -i 's/^    networks: \[biz, dbzone\].*$/    networks: [dmz, biz, dbzone] # Day 6-3 temporary test/' compose.yaml
diff -u /tmp/day06-compose.OTTiFi compose.yaml

docker compose config --quiet && docker compose up -d --no-deps --pull never agent
sleep 15
docker compose ps agent
docker inspect day06-agent-1 --format '{{range $name, $config := .NetworkSettings.Networks}}{{$name}} {{end}}'
curl -fsS --max-time 10 'http://127.0.0.1:8080/healthz' | jq .
curl -fsS --max-time 20 'http://127.0.0.1:8080/egress?url=http://example.com&timeout=5' | jq .
```

- 후속: 외부 요청 결과를 확인한 뒤 백업으로 원복하고 동일 해시·원래 networks·외부 요청 실패·서비스 정상까지 검증한다. gateway 경유 요청에 이상이 있으면 agent 재생성 후 주소 변경·nginx의 기존 이름 해석 결과 등부터 조회해 진단하며 성공으로 가정하지 않는다.

### 2026-09-29 — 6-3 외부 접속 재현 확인 및 원복 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. [DMZ 추가·외부 접속 증거](evidence/63-dmz-added-user-2026-09-29.txt).
- diff에서 agent의 networks 행만 biz·dbzone에서 dmz·biz·dbzone으로 변경됐다. Compose 문법 검사 뒤 agent 재생성·시작을 확인했다.
- agent는 Created 19 seconds ago·Up 15 seconds (healthy)이며 실제 네트워크는 day06_biz·day06_dbzone·day06_dmz다. healthz는 status=ok·version=0.2.0·host=8faa0748aa9d다.
- 외부 요청은 http://example.com에 ok=true·status=200·elapsed_ms=105다. 기존 DNS 실패에서 외부 HTTP 성공으로 바뀌었다. 서비스 건강 상태가 정상이어도 네트워크 연결 추가로 외부 접근 경로가 생기는 실수를 재현했다.
- 다음은 Ubuntu `/home/user/onprem-lab/day06`에서 백업으로 원복하는 명령을 안내했다. cp·문법 검사·재적용을 &&로 연결한다. 원복 결과는 아직 미수신이므로 6-3 완료가 아니다. 백업 파일은 삭제하지 않는다.

```bash
cp /tmp/day06-compose.OTTiFi compose.yaml && docker compose config --quiet && docker compose up -d --no-deps --pull never agent
sleep 15
sha256sum compose.yaml /tmp/day06-compose.OTTiFi
docker compose ps agent
docker inspect day06-agent-1 --format '{{range $name, $config := .NetworkSettings.Networks}}{{$name}} {{end}}'
curl -fsS --max-time 10 'http://127.0.0.1:8080/healthz' | jq .
curl -fsS --max-time 20 'http://127.0.0.1:8080/egress?url=http://example.com&timeout=5' | jq .
```

### 2026-09-29 — 6-3 원복 검증 및 완료
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day06`. 명령은 위 원복 안내와 같으며 사용자가 실행했다.
- 확인 주체: 사용자 제공 출력. [원복 증거](evidence/63-restored-user-2026-09-29.txt). Codex는 Ubuntu 명령을 직접 실행하지 않았다.
- compose.yaml과 백업 `/tmp/day06-compose.OTTiFi`의 SHA-256이 모두 원본 `1c2e71cf3ac308e285d14ed3a2a3ab5d7dd7f0db86a82294b610bad4e69db3cb`와 일치한다. Windows에 유지한 원본과도 일치한다.
- agent 재생성 후 Created 20 seconds ago·Up 15 seconds (healthy)를 확인했다. 실제 연결은 day06_biz·day06_dbzone만 남아 DMZ 연결 제거를 확인했다.
- gateway 경유 healthz는 status=ok·version=0.2.0·host=f4298542de49다. example.com 요청은 ok=false·gaierror·Temporary failure in name resolution·elapsed_ms=7로 돌아왔다.
- 결과: 원본 파일·네트워크 소속·서비스 정상·외부 요청 실패 복귀를 확인해 6-3 완료. DMZ 추가 시 외부 HTTP 200(105ms), 원복 시 이름 해석 실패(7ms)로 변화했다. 원복 후 DB·ERP 연결을 다시 시험한 것은 아니다.
- 자원 상태: Day 6 구성은 유지하며 정리는 수행하지 않았다. 임시 백업 `/tmp/day06-compose.OTTiFi`도 보존한다. 기존 Day 4·koica 자원은 변경하지 않았다. 6-4 신청서·누적 점검·자기점검·Day 전체 정리는 미진행이다.

### 2026-09-29 — 6-4 시작 및 학습용 신청서 초안 작성
- 사용자 요청으로 6-4를 시작했다. Codex가 진행·환경 기록과 Day 6 README/SESSION, 가이드 본문 6-4 및 부록 E-2/E-3를 확인했다.
- 작업 위치: Windows 프로젝트. [FIREWALL-REQUEST.md](FIREWALL-REQUEST.md)에 신청 개요·7행·번호를 맞춘 흐름도·외부 FQDN 별첨·최소 권한 근거·실습 대조를 작성했다. Ubuntu에서 실행한 명령은 없다.
- 실제 고객사 정보가 없으므로 가이드의 10.x 주소는 가상 예시로, 종료일·FQDN·계정 스키마 등은 미정으로 표시했다. 새로운 서비스나 정책을 적용하지 않았고 고객사에 제출하지 않았다.
- 본문 2번은 8000/TCP, 부록 E-2는 8080/TCP로 다르다. 이번 초안은 본문·현재 agent 리스너 기준의 8000 예시를 채택하되 실제 VM 공개 포트 확인 필요를 기록했다. 실습의 localhost:8080과 신청서의 사용자 HTTPS 443도 구분했다.
- 부록의 LLM 게이트웨이 전제는 이후 Day의 설계이므로 현재 초안에서는 Day 6 본문대로 agent→프록시를 사용했다. registry pull은 호스트 런타임의 통신으로 구분했다.
- 상태: 초안 작성은 완료했고 사용자 학습·검토가 진행 중이다. 사용자 독립 작성·이해도 평가 통과나 Day 6 전체 완료로 처리하지 않는다. 이전 6-3 원복 상태의 자원은 유지한다.

### 2026-09-30 — lazydocker 화면 관찰
- 확인 근거: 사용자가 첨부한 day6_lazydocker.png. Codex가 화면 내용을 읽었으며 Ubuntu 명령을 직접 실행하지 않았다.
- Project=day06, Services의 7개 항목 모두 running이고 agent·postgres는 healthy다. Networks에 day06_biz·day06_dbzone·day06_dmz가 보인다.
- 선택된 day06_biz의 Config는 Driver=bridge, Internal=true, EnabledIPv6=false, Containers=none이다. 다른 두 존의 상세 설정은 이 화면에 없다.
- Day 4에도 Containers: none과 CLI 소속 목록의 불일치가 기록돼 있다. 이번 화면만으로 실제 연결 부재나 특정 버그 원인을 확정하지 않는다.
- Ubuntu WSL2에서 다음 읽기 전용 명령을 안내했다. 아직 결과를 받지 않았으므로 현재 소속 재검증 완료로 기록하지 않는다.

```bash
docker network inspect day06_dmz day06_biz day06_dbzone --format '{{.Name}} internal={{.Internal}} containers={{range .Containers}}{{.Name}} {{end}}'
```

- 누적 고장 점검·자원 정리는 수행하지 않았다. 다음 시작 지점은 위 조회 결과와 예상 소속 대조다.

### 2026-09-30 — CLI 대조 및 화면 관찰 완료
- 사용자 제공 Ubuntu WSL2 `/home/user/onprem-lab/day06` 출력으로 위 network inspect 결과를 확인했다. Codex 직접 실행 결과가 아니다.
- dmz: internal=false, gateway·probe-dmz. biz: internal=true, gateway·erp·probe-biz·agent. dbzone: internal=true, postgres·agent·probe-db.
- 세 존 모두 예상 설정·소속과 일치하며 agent는 DMZ에 없다. lazydocker의 Containers: none과 실제 소속 조회가 불일치함을 확인했다. 표시 원인은 미확정이다.
- [CLI 증거](evidence/network-observation-user-2026-09-30.txt). 화면 관찰은 CLI 보완을 포함해 완료했다. 통신 시험을 재실행하거나 설정을 변경하지 않았다.
- 다음은 사용자 요청 시 누적 고장 진단 실습을 시작한다. 자원 정리와 Day 6 전체 완료는 아직 아니다.

### 2026-09-30 — Containers: none 원인 조사
- 사용자 질문에 따라 공식 저장소의 [동일 증상 버그 #752](https://github.com/jesseduffield/lazydocker/issues/752)를 확인했다. 해당 보고도 네트워크 화면은 none이지만 CLI inspect에는 컨테이너가 나오는 현상이다.
- [Docker API 문서](https://docs.docker.com/reference/api/engine/version/v1.40/)는 네트워크 목록 조회가 상세 조회보다 축약돼 있으며 API 1.28 이후 연결 컨테이너 목록을 포함하지 않는다고 명시한다.
- 목록 응답의 생략된 정보를 none으로 표시하는 것이 유력한 원인이라고 설명한다. 설치된 바이너리의 실제 API 요청과 해당 네트워크 표시 코드는 검증하지 못했으므로 내부 원인 확정과 구분한다. 설치·업데이트·설정 변경은 하지 않았다.

### 2026-09-30 — 누적 장애 진단 1번 안내
- Codex가 Windows의 break.sh와 가이드 누적 점검 절을 읽고 동작·복구 범위를 확인했다. 스크립트는 수정하지 않았고 Ubuntu 명령은 직접 실행하지 않았다. 이전 사용자 결과로 실행 권한·파일 해시 일치를 확인한 상태다.
- 사용자에게 원인을 미리 설명하지 않고 아래 명령으로 고장 1개를 주입한 뒤 상태와 응답을 비교하도록 안내했다. ./break.sh answer는 5개 정답을 모두 출력하므로 아직 실행하지 않도록 안내한다.
- 실행 위치: Ubuntu WSL2 /home/user/onprem-lab/day06. 아래는 제안한 명령이며 실행 결과 대기 상태다.

```bash
cd /home/user/onprem-lab/day06
./break.sh 1
docker compose ps -a
curl -fsS --max-time 10 'http://127.0.0.1:8080/healthz' | jq .
curl -fsS --max-time 15 'http://127.0.0.1:8080/tcp?host=postgres&port=5432' | jq .
```

- 주입 명령에서 오류가 나면 중단하고 공유한다. 출력과 사용자 원인 추정을 받은 뒤 추가 진단·복구로 이어 간다. 정답 판정·독립 진단 통과·복구 완료 기록은 아직 없다.
- 복구 구현 확인: 원본 fix는 unpause를 시도한 뒤 해당 Compose 프로젝트 전체를 force-recreate하며 출력을 숨긴다. 복구 단계에서는 필요한 검증과 출력 확보를 고려한다. 현재는 복구 명령을 실행하도록 안내하지 않았다.

### 2026-09-30 — 누적 장애 1번 증상 확인
- 사용자 제공 Ubuntu 출력으로 ./break.sh 1 실행 후 프롬프트 복귀·오류 메시지 없음을 확인했다. 7개 서비스는 Up이며 agent·postgres는 healthy다.
- gateway 경유 healthz는 status=ok·version=0.2.0·host=f4298542de49다. DB TCP 요청은 ok=false·host=postgres·port=5432·error_type=gaierror·Temporary failure in name resolution이다.
- 관찰: 이번 DB 시도는 이름 해석 단계에서 실패했다. TCP 연결 거절·DB 인증 실패로 해석하지 않는다. 사용자 독립 원인 판단은 아직 제공되지 않았다. [증거](evidence/fault-01-symptoms-user-2026-09-30.txt).
- 다음 읽기 전용 명령을 Ubuntu에서 실행해 실제 소속을 비교하도록 안내했다. 결과는 아직 없고 복구도 수행하지 않았다.

```bash
docker inspect day06-agent-1 day06-postgres-1 --format '{{.Name}} networks={{range $name, $config := .NetworkSettings.Networks}}{{$name}} {{end}}'
```

### 2026-09-30 — 누적 장애 1번 원인 확인·복구 안내
- 사용자 제공 docker inspect 출력: /day06-agent-1 networks=day06_biz, /day06-postgres-1 networks=day06_dbzone. 공통 네트워크가 사라졌고 agent의 DB존 연결 이탈을 확인했다.
- 이는 Windows에서 확인한 break.sh 1의 동작과 일치한다. biz 연결은 유지돼 gateway 경유 healthz가 성공했으나 postgres 이름 해석은 실패했다. 사용자에게 진단 명령과 비교 기준을 안내했으므로 독립 진단 통과로 계산하지 않는다.
- 복구는 해당 연결만 되살리는 방법을 안내한다. 전체 서비스를 재생성하는 원본 ./break.sh fix 대신 docker network connect를 사용하고 agent 서비스 별칭도 지정한다. compose.yaml은 이번 고장 주입으로 수정되지 않는다.
- 실행 위치: Ubuntu WSL2 /home/user/onprem-lab/day06. 아래 명령은 안내만 했으며 복구 결과 대기 중이다. connect에서 오류가 나면 멈추고 공유하도록 안내한다.

```bash
docker network connect --alias agent day06_dbzone day06-agent-1
docker inspect day06-agent-1 --format '{{range $name, $config := .NetworkSettings.Networks}}{{$name}} {{end}}'
curl -fsS --max-time 10 'http://127.0.0.1:8080/healthz' | jq .
curl -fsS --max-time 15 'http://127.0.0.1:8080/tcp?host=postgres&port=5432' | jq .
```

- 기대 결과: agent는 biz·dbzone에 연결, healthz status=ok, DB TCP ok=true. DB 인증·SQL을 시험하는 것은 아니다. 확인 전 다음 고장을 주입하지 않는다.

### 2026-09-30 — 누적 장애 1번 복구 확인 및 2번 안내
- 사용자 제공 Ubuntu 출력으로 docker network connect --alias agent day06_dbzone day06-agent-1 실행 후 agent 소속이 day06_biz·day06_dbzone으로 복귀함을 확인했다.
- healthz는 status=ok·version=0.2.0·host=f4298542de49이며 DB TCP는 ok=true·host=postgres·port=5432·elapsed_ms=1이다. 1번 재현·안내에 따른 진단·복구 검증 완료. DB 인증·SQL 검증이나 독립 진단 평가 통과는 아니다.
- [복구 증거](evidence/fault-01-restored-user-2026-09-30.txt). Codex가 Ubuntu 명령을 직접 실행한 것은 아니다.
- 이어 2번 고장을 주입하고 사용자 진입·ERP HTTP 응답을 비교하도록 아래 명령을 안내했다. Ubuntu WSL2 /home/user/onprem-lab/day06에서 실행하며 결과는 아직 없다. 주입 오류가 있으면 중단하고 공유한다. answer·fix는 아직 실행하지 않는다.

```bash
./break.sh 2
curl -fsS --max-time 10 'http://127.0.0.1:8080/healthz' | jq .
docker compose exec -T agent python -c 'import urllib.request; r = urllib.request.urlopen("http://erp:8080", timeout=5); print("HTTP", r.status); print(r.read().decode())'
```

- 오류가 나오면 마지막 오류 유형과 메시지에 주목하도록 안내한다. 2번 실제 재현·진단·복구 완료로 기록하지 않는다.

### 2026-09-30 — 누적 장애 2번 증상 확인
- 사용자 제공 Ubuntu 출력으로 ./break.sh 2 실행 후 출력 없이 프롬프트 복귀를 확인했다. Codex가 직접 실행하지 않았다.
- healthz 응답: status=ok·version=0.2.0·host=f4298542de49. agent에서 http://erp:8080 요청은 socket.gaierror: [Errno -3] Temporary failure in name resolution이며 urllib.error.URLError로 감싸져 출력됐다. ERP HTTP 응답까지 도달하지 못했다.
- 해석: 이번 요청의 이름 해석 단계 실패는 확인했지만 오류 메시지만으로 네트워크 분리와 대상 서비스 중단을 구별할 수 없다. 사용자에게 원인을 미리 확정해 알려주지 않고 아래 조회로 agent·erp의 STATUS를 비교하도록 안내했다.

```bash
docker compose ps -a
```

- 실행 위치: Ubuntu WSL2 /home/user/onprem-lab/day06. 상태 조회 출력과 사용자 판단은 아직 없고 2번 복구는 수행하지 않았다. [증상 요약 증거](evidence/fault-02-symptoms-user-2026-09-30.txt).

### 2026-09-30 — 누적 장애 2번 원인 확인·복구 안내
- 사용자 제공 docker compose ps -a 출력: day06-erp-1만 Exited (2) About a minute ago, 나머지 6개는 Up이다. agent는 Up 12 hours (healthy), postgres는 Up 20 hours (healthy)다.
- ERP 중지는 앞서 읽은 break.sh 2의 docker compose stop erp 동작과 일치한다. 종료 코드 2만으로 별도의 앱 오류 원인을 추정하지 않는다. 이번에는 네트워크 연결을 수정하지 않고 기존 ERP 컨테이너를 시작한다.
- 아래 명령을 Ubuntu WSL2 /home/user/onprem-lab/day06에서 실행하도록 안내했다. 아직 복구 출력은 받지 않았다. start 명령에서 오류가 나면 멈추고 공유하도록 안내한다.

```bash
docker compose start erp
docker compose ps -a erp
docker compose exec -T agent python -c 'import urllib.request; r = urllib.request.urlopen("http://erp:8080", timeout=5); print("HTTP", r.status); print(r.read().decode())'
```

- 기대 결과: ERP가 Up이고 agent의 요청에 HTTP 200·Name: erp-api 응답. 실제 복구는 후속 출력으로 판정한다. 사용자 독립 진단 통과와 구분한다.

### 2026-09-30 — 누적 장애 2번 복구 완료 및 3번 안내
- 사용자 제공 Ubuntu 출력으로 docker compose start erp 성공, ERP Up 3 seconds 및 실제 agent→ERP HTTP 200·Name: erp-api를 확인했다. Hostname=a175214f01f1, ERP IP=172.21.0.5, RemoteAddr=172.21.0.3:44254다. 2번 복구 완료이며 독립 진단 통과와 구분한다.
- [복구 증거](evidence/fault-02-restored-user-2026-09-30.txt). Codex 직접 Ubuntu 실행 결과가 아니다.
- 이어 3번 고장 주입 후 서비스 상태와 사용자 진입 경로를 관찰하도록 아래 명령을 안내했다. 실행 위치는 Ubuntu WSL2 /home/user/onprem-lab/day06이며 아직 실행 결과는 없다. 주입 명령 오류 시 중단하고 공유한다.

```bash
./break.sh 3
docker compose ps -a
curl -sS -i --max-time 10 'http://127.0.0.1:8080/healthz'
```

- 오류 응답·타임아웃을 그대로 관찰하도록 jq 없이 조회한다. 요청은 최대 10초로 제한한다. 아직 3번 원인 설명·복구 또는 다음 고장 주입은 진행하지 않았다.

### 2026-09-30 — 누적 장애 3번 증상 확인
- 사용자 제공 Ubuntu 출력: ./break.sh 3 후 오류 출력 없이 복귀. docker compose ps -a에서 서비스 7개 모두 Up, agent·postgres healthy이며 gateway의 127.0.0.1:8080->80/tcp 게시도 표시된다.
- 사용자 healthz 요청은 curl: (28) Operation timed out after 10002 milliseconds with 0 bytes received다. 이 출력만으로 gateway 도달 여부나 차단 구간을 확정하지 않는다. [증상 증거](evidence/fault-03-symptoms-user-2026-09-30.txt).
- 다음 읽기 전용 명령으로 실제 소속과 업무망에서의 agent 직접 응답을 비교하도록 안내했다. 실행 위치는 Ubuntu WSL2 /home/user/onprem-lab/day06. 아직 결과는 없고 복구도 수행하지 않았다.

```bash
docker inspect day06-gateway-1 day06-agent-1 --format '{{.Name}} networks={{range $name, $config := .NetworkSettings.Networks}}{{$name}} {{end}}'
docker compose exec -T probe-biz curl -sS -i --max-time 5 http://agent:8000/healthz
```

- 직접 요청은 사용자→gateway 경로를 우회한다. 사용자 경로와 직접 경로의 결과를 비교해 다음 진단·복구로 이어 간다.

### 2026-09-30 — 누적 장애 3번 원인 확인·복구 안내
- 사용자 제공 inspect 출력: gateway는 day06_dmz만, agent는 day06_biz·day06_dbzone에 연결돼 있다. gateway의 업무망 연결 이탈은 break.sh 3 동작과 일치한다.
- probe-biz에서 http://agent:8000/healthz 직접 조회는 HTTP/1.0 200 OK, status=ok·version=0.2.0·host=f4298542de49다. agent가 업무망에서 실제로 응답함을 확인해 gateway↔agent 공통 네트워크 부재로 진단했다. 수신 전체 경로의 패킷 캡처를 한 것은 아니다.
- 복구는 gateway를 biz에 재연결한다. 원본 fix의 전체 재생성 대신 해당 연결만 복구하도록 아래 명령을 안내했다. Ubuntu WSL2 /home/user/onprem-lab/day06에서 사용자 실행하며 결과는 아직 없다. connect 오류 시 중단하고 공유한다.

```bash
docker network connect --alias gateway day06_biz day06-gateway-1
docker inspect day06-gateway-1 --format '{{range $name, $config := .NetworkSettings.Networks}}{{$name}} {{end}}'
curl -sS -i --max-time 10 'http://127.0.0.1:8080/healthz'
```

- 기대 결과: gateway는 biz·dmz 소속, 사용자 경로 healthz HTTP 200·status=ok. 실패하면 실제 출력으로 추가 진단하며 성공으로 가정하지 않는다. 아직 3번 복구 완료가 아니다.

### 2026-09-30 — 누적 장애 3번 복구 확인 및 4번 안내
- 사용자 제공 inspect 출력에서 gateway의 day06_biz·day06_dmz 소속을 확인했다. 사용자 healthz는 HTTP/1.1 200 OK, Server=nginx/1.27.5, status=ok·version=0.2.0·host=f4298542de49다. 3번 복구 완료.
- 복구 명령 첫 줄에는 이전 JSON 닫는 괄호·프롬프트가 섞여 있고 컨테이너명이 day06-gateway-11로 붙어 있다. 실제로 그 문자열이 실행됐다고 확정하지 않는다. 후속의 정확한 대상 inspect 및 HTTP 응답을 복구 근거로 삼았다.
- [복구 증거](evidence/fault-03-restored-user-2026-09-30.txt). 사용자 제공 결과이며 Codex가 Ubuntu 명령을 직접 실행하지 않았다.
- 다음은 Ubuntu WSL2 /home/user/onprem-lab/day06에서 아래 4번 주입·관찰 명령을 안내했다. 실행 결과는 아직 없으며 주입 오류가 나면 중단하고 공유한다.

```bash
./break.sh 4
docker compose ps -a
curl -sS -i --max-time 10 'http://127.0.0.1:8080/healthz'
```

- STATUS 괄호 안 표시까지 관찰하도록 안내했다. 4번의 실제 상태·원인 판단·복구는 미확인이다.

### 2026-09-30 — 누적 장애 4번 원인 확인·복구 안내
- 사용자 제공 Ubuntu 출력: ./break.sh 4는 day06-agent-1을 출력했고 ps -a에서 agent는 Up 12 hours (Paused)다. 나머지 6개 서비스는 Up이며 postgres는 healthy다.
- 사용자 healthz 요청은 curl (28), 10002 milliseconds, 0 bytes received로 종료됐다. break.sh 4의 docker pause 동작과 상태 표시가 일치한다. 컨테이너 내부 프로세스 일시 정지가 원인이며 Up만으로 응답 가능 여부를 판단할 수 없음을 설명했다.
- 아래 복구 명령을 Ubuntu WSL2 /home/user/onprem-lab/day06에서 실행하도록 안내했다. 아직 복구 출력은 없으며 unpause 오류가 나면 멈추고 공유한다.

```bash
docker unpause day06-agent-1
docker compose ps -a agent
curl -sS -i --max-time 10 'http://127.0.0.1:8080/healthz'
```

- 기대 결과: Paused 표시 해제와 사용자 healthz HTTP 200·status=ok. 건강 상태 표시는 다음 검사 때 갱신될 수 있으므로 실제 응답과 함께 판단한다. 재생성·네트워크 변경은 안내하지 않았다. 독립 진단 평가 통과와 구분한다.

### 2026-09-30 — 4번 응답 복구 및 unhealthy 추가 확인
- 사용자 제공 출력으로 docker unpause day06-agent-1 성공, Paused 해제를 확인했다. ps는 Up 12 hours (unhealthy)다.
- 사용자 healthz 요청은 HTTP/1.1 200 OK·Server nginx/1.27.5·status=ok·version=0.2.0·host=f4298542de49다. 요청 처리는 복구됐지만 건강 상태 정상 복귀는 아직 확인되지 않았다.
- Codex가 Windows 소스를 읽어 agent/Dockerfile의 HEALTHCHECK interval=15s·timeout=3s·start-period=5s·retries=3을 확인했다. 이는 소스 설정이며 실행 중 이미지의 설정을 직접 조회한 것은 아니다.
- 일시 정지 중 검사 실패와 검사 주기에 따른 상태 갱신 지연이 가능한 설명이지만 실제 이력을 보기 전 원인으로 확정하지 않는다. 아래 읽기 전용 확인을 Ubuntu WSL2 /home/user/onprem-lab/day06에서 안내했고 결과 대기 중이다.

```bash
sleep 20
docker compose ps -a agent
docker inspect day06-agent-1 --format '{{json .State.Health}}' | jq .
```

- 건강 상태·최근 검사 ExitCode/Output을 보고 후속 판단한다. 재시작·재생성·5번 고장 주입은 안내하지 않았다.

### 2026-09-30 — 누적 장애 4번 복구 완료 및 5번 안내
- 사용자 제공 후속 출력: agent Up 12 hours (healthy), State.Health.Status=healthy, FailingStreak=0. 최근 로그 5개 모두 ExitCode=0·Output 빈 문자열이다. 검사 시작 시각은 UTC 00:46:46, 00:47:00, 00:47:15, 00:47:29, 00:47:45다.
- 앞선 unpause 후 HTTP 200과 이번 건강 상태 복귀를 합쳐 4번 복구 완료로 판단했다. 이전 실패 기록은 이번 최근 5개 로그에 없으므로 당시 unhealthy의 상세 실패 원인을 이 로그로 확정하지 않는다. 붙여넣은 대기 명령은 sleep 200으로 표시되며 정확한 대기 시간은 검증하지 않았다.
- 다음 5번 주입 후 healthz와 외부 요청을 비교하도록 아래 명령을 안내했다. Ubuntu WSL2 /home/user/onprem-lab/day06에서 사용자 실행하며 아직 결과는 없다. 주입 오류 시 중단하고 공유한다.

```bash
./break.sh 5
docker compose ps -a agent
curl -fsS --max-time 10 'http://127.0.0.1:8080/healthz' | jq .
curl -fsS --max-time 20 'http://127.0.0.1:8080/egress?url=http://example.com&timeout=5' | jq .
```

- 정상 구성에서 외부 직접 요청은 실패했음을 비교 기준으로 안내한다. 5번 고장 실행·진단·복구는 아직 확인하지 않았다. 독립 진단 평가 통과와 구분한다.

### 2026-09-30 — 누적 장애 5번 통제 위반 재현 확인
- 사용자 제공 Ubuntu 출력: ./break.sh 5는 출력 없이 복귀했고 agent는 Up 12 hours (healthy)다. healthz는 status=ok·version=0.2.0·host=f4298542de49다.
- 외부 요청은 ok=true·url=http://example.com·status=200·elapsed_ms=228이다. 정상 구성에서 실패하던 외부 직접 요청이 성공해 의도한 통신 제한 위반을 재현했다. 모든 외부 목적지 접근을 시험한 것은 아니다.
- 원인 확인을 위해 아래 읽기 전용 조회를 Ubuntu WSL2 /home/user/onprem-lab/day06에서 안내했다. 정상 소속 biz·dbzone과 비교하도록 설명했으며 실제 조회 출력은 아직 없다.

```bash
docker inspect day06-agent-1 --format '{{range $name, $config := .NetworkSettings.Networks}}{{$name}} {{end}}'
```

- 5번 복구·Day 전체 정리는 수행하지 않았다. [증상 증거](evidence/fault-05-symptoms-user-2026-09-30.txt). Codex 직접 Ubuntu 실행이나 독립 진단 통과와 구분한다.

### 2026-09-30 — 누적 장애 5번 원인 확인·복구 안내
- 사용자 제공 docker inspect 출력은 day06_biz day06_dbzone day06_dmz다. 정상 소속에 DMZ가 추가됐으며 break.sh 5의 동작과 일치한다. 앞서 확인한 외부 HTTP 200과 함께 원인을 확인했다.
- Ubuntu WSL2 /home/user/onprem-lab/day06에서 아래 명령으로 추가된 DMZ 연결만 제거하고 검증하도록 안내했다. 네트워크 자체나 컨테이너를 삭제하지 않는다. disconnect 오류 시 멈추고 공유하며 아직 복구 결과는 없다.

```bash
docker network disconnect day06_dmz day06-agent-1
docker inspect day06-agent-1 --format '{{range $name, $config := .NetworkSettings.Networks}}{{$name}} {{end}}'
curl -fsS --max-time 10 'http://127.0.0.1:8080/healthz' | jq .
curl -fsS --max-time 20 'http://127.0.0.1:8080/egress?url=http://example.com&timeout=5' | jq .
```

- 기대 결과는 biz·dbzone만 남음, healthz status=ok 유지, 외부 직접 요청 ok=false다. 결과 확인 전 5번 복구나 누적 실습 전체 완료로 기록하지 않는다. Day 전체 정리는 별도다.

### 2026-09-30 — 누적 장애 5번 복구 및 실습 마무리
- 사용자 제공 Ubuntu 출력으로 docker network disconnect day06_dmz day06-agent-1 실행 후 agent가 day06_biz·day06_dbzone에만 연결됨을 확인했다.
- healthz는 status=ok·version=0.2.0·host=f4298542de49다. 외부 요청은 ok=false·gaierror·Temporary failure in name resolution·elapsed_ms=1이다. 5번 복구 완료. [복구 증거](evidence/fault-05-restored-user-2026-09-30.txt).
- 누적 장애 1~5번 모두 사용자 출력으로 재현·안내에 따른 진단·개별 복구 검증을 마쳤다. 원본 ./break.sh fix로 전체 재생성하는 대신 각 변경을 되돌렸다. 1번 DB존 재연결, 2번 ERP 시작, 3번 gateway 업무망 재연결, 4번 unpause 후 healthy 복귀, 5번 agent DMZ 연결 제거다.
- 사용자에게 진단 명령·비교 기준·원인을 안내했으므로 가이드의 독립 진단 4/5 통과로 평가하지 않는다. 마지막 5번 복구 시 DB·ERP 등 모든 경로를 다시 시험한 것은 아니다.
- Windows 기록만 갱신했으며 Codex가 Ubuntu 명령을 직접 실행하지 않았다. 실습 자원·백업은 유지한다. 개념 자기점검과 Day 6 자원 정리는 남아 있으며 Day 전체 완료·종료로 처리하지 않는다.

### 2026-09-30 — 학습 요약 및 종료 정리 안내
- 사용자 요청에 따라 3존 구조와 장애 5개의 증상·원인·복구를 설명했다. 같은 이름 해석 실패·타임아웃도 원인이 다를 수 있으며 실행 상태·실제 응답·통신 제한을 별도로 확인해야 함을 정리했다. 별도 자기점검 문답 평가나 독립 진단 통과 기록은 없다.
- 후속 “좋아 이제 정리하자” 요청으로 Day 6 종료 정리를 시작한다. Codex가 Compose의 프로젝트명·구성과 기록을 확인했다. 삭제 범위는 Day 6 컨테이너·네트워크이며 이미지·볼륨·임시 백업·기존 Day 4/koica 자원은 포함하지 않는다.
- Ubuntu WSL2에서 아래 명령을 사용자가 실행하도록 안내했다. --volumes·--rmi·prune은 사용하지 않는다. 아직 실행 결과는 없으므로 정리 완료나 Day 종료로 처리하지 않는다.

```bash
cd /home/user/onprem-lab/day06 && docker compose -p day06 down
docker ps -a --filter label=com.docker.compose.project=day06 --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker network ls --filter label=com.docker.compose.project=day06 --format 'table {{.Name}}\t{{.Driver}}'
ss -lnt 'sport = :8080'
```

- 기대 결과: Day 6 컨테이너 7개·네트워크 3개 제거, 프로젝트 필터 목록과 8080 리스너 조회에 헤더만 표시. 실패·잔존이 있으면 출력으로 확인하며 다른 프로젝트를 자동 정리하지 않는다.

### 2026-09-30 — 자원 정리 확인 및 Day 6 종료
- 사용자 제공 Ubuntu WSL2 /home/user/onprem-lab/day06 출력으로 docker compose -p day06 down 완료를 확인했다. 컨테이너 7개와 네트워크 day06_dmz·day06_biz·day06_dbzone이 모두 Removed다.
- 프로젝트 라벨로 필터한 docker ps -a와 docker network ls는 헤더만 표시됐다. ss -lnt 'sport = :8080'도 헤더만 표시돼 해당 Ubuntu 조회의 리스너 부재를 확인했다. [정리 증거](evidence/cleanup-user-2026-09-30.txt).
- 이미지·볼륨·임시 백업 삭제 옵션은 사용하지 않았다. 해당 자원의 잔존 목록을 이번 출력으로 재확인한 것은 아니다. 기존 Day 4·koica 자원은 정리 범위에 포함하지 않았다.
- Day 6 학습·실습·누적 장애 복구·요약·정리를 마치고 종료한다. 별도 자기점검 문답 평가와 독립 진단 4/5 통과는 미실시로 남긴다. 학습용 방화벽 초안은 작성·설명했으나 고객사 제출·실제 정책 적용은 없다.
- Codex는 사용자 결과를 근거로 Windows SESSION·PROGRESS·README·환경 기록을 갱신했다. Ubuntu 직접 실행·동기화·Day 7 시작은 하지 않았다.

### 2026-09-30 — GitHub PR 준비
- 사용자가 Day 6 추진 결과의 GitHub PR 제출을 요청했다. GitHub 조회에서 Day 5 PR #7의 병합 커밋 077b241을 확인했고 해당 origin/main에서 codex/day06-results를 만들었다. 기존 Day 6 미커밋 변경을 보존했다.
- 종료 상태와 충돌하던 PROGRESS·README 요약을 정리하고 README에 장애 5개의 원인·복구 표를 추가했다. 날짜별 SESSION 이력은 유지했다.
- Codex 직접 검증: git diff --check 통과, 변경 문서 5개의 로컬 Markdown 링크 대상 존재 확인, 기록·증거에서 자격 증명 패턴 검색 결과 없음. 실습 소스·가이드·부록 파일 목록은 수정하지 않았고 Ubuntu 실습은 재실행하지 않았다.
- GitHub 인증은 샌드박스 밖에서 기존 로그인으로 확인했다. 이 항목은 PR 준비 기록이며 제출 URL·결과는 생성 후 기록한다.

### 2026-09-30 — Day 6 PR 제출
- [PR #8](https://github.com/shanis345/Deploy_Practice/pull/8): codex/day06-results → main. 최초 결과 커밋은 1bc1ca5이며 문서·증거 27개 파일을 포함한다.
- Git 작성자 설정 부재로 첫 커밋 시도가 실패했다. 기존 커밋에서 확인한 작성자 이름·GitHub noreply 이메일을 명령별 -c 옵션으로 적용해 커밋했고 전역 설정은 변경하지 않았다.
- 브랜치를 origin에 푸시하고 PR을 생성해 이 Codex 작업에 첨부했다. 병합은 수행하지 않았다. 이 링크를 인수인계 기록에 추가한다.

## 오류와 해결
- 6-1 사전 점검·기동 출력에서 오류가 보고되지 않았다.

## 배운 내용과 질문
- gateway는 dmz·biz, agent는 biz·dbzone의 두 네트워크에 연결되고 postgres는 dbzone에만 연결된다. probe는 각 존에 하나씩 둔다.
- internal 설정값 확인과 실제 외부 통신 차단 검증을 구분한다. healthy는 존 간 통신 전체의 정상 여부를 보장하지 않는다.
- ⑦에서 DB존→agent 신규 연결이 열림을 확인했다. Docker 네트워크의 분리와 방향별 통제는 구분해야 한다.
- 6-3에서 DMZ 연결을 추가하자 healthy·healthz 정상 상태를 유지하면서 외부 HTTP 요청까지 성공했다. 가용성과 네트워크 통제 준수는 별도로 확인해야 한다.

## 가이드와 실제 환경의 차이
공통 환경은 [환경 기록](../docs/environment.md)을 참고한다.
- 가이드의 network ls 템플릿 대신 network inspect로 Internal과 컨테이너 소속을 조회했다. 사전 확인한 로컬 이미지를 사용하도록 기동에 --pull never를 지정했다.
- 6-2 ③에 실제 DB IP 직접 TCP 시험을 추가했다. ⑤는 가이드 제목과 실제 명령의 출발지가 달라 probe-biz 대신 agent의 Python으로 실행했다. 가이드 원문·실습 소스는 수정하지 않았다.

## 다음에 이어 할 지점
Day 6은 종료했다. 사용자 요청 시 Day 7의 README·SESSION·가이드와 환경 기록을 읽고 프록시·화이트리스트 실습을 시작한다. 별도 자기점검 평가는 미실시로 남긴다. 임시 백업 `/tmp/day06-compose.OTTiFi`·이미지·볼륨은 삭제하지 않았으며 기존 Day 4·koica 자원은 별도다. Windows와 Ubuntu 사본은 자동 동기화되지 않는다.
