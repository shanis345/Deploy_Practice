# Day 5 — Docker Compose: 다중 서비스와 그 한계

## 진행 상태
- 상태: Day 5 종료 · 5-1~5-4 및 지정 자원 정리 완료(2026-09-29)
- 완료한 범위: 5-1 구성 검증, 5-2 장애 3종·복구, 5-3 프롬프트 변경·원복, 5-4 예시 변수 치환·평문 출력 확인
- 중단 지점: 사용자 정리 출력 확인 후 종료. 다음은 사용자 요청 시 Day 6
- Codex 작업: 아직 별도 작업을 만들지 않음
- 실행 증거 기준: 사용자 제공 출력과 직접 검증 결과를 구분해 기록

## 목표와 이번 세션 범위
2026-09-29 사용자 요청에 따라 5-1~5-4를 완료하고 lazydocker 정상 상태·로그 표시를 확인했다. 체크포인트 5문항 해설 후 사용자 요청 “좋아. 그럼 정리하자”에 따라 Day 5 자원 정리와 종료 기록을 진행한다. 사용자가 Ubuntu WSL2에서 직접 명령을 실행하고 결과를 제공한다. 미확인 Stats·TUI 상태 변화와 별도 자기점검 평가는 완료로 간주하지 않는다.

## 실행 기록
### 2026-09-29 — 5-1 사전 점검 안내(실행 결과 대기)
- Codex 확인: Windows의 진행·환경 기록, Day 5 README·SESSION·가이드 5-1 및 compose.yaml·nginx.conf를 읽었다. Ubuntu 복사본은 조회하거나 변경하지 않았다.
- 안내 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`. Windows에서 Docker Desktop을 실행해 둔 뒤 아래 명령을 한 줄씩 실행한다. cd 실패 시 후속 명령을 중단한다.

```bash
cd /home/user/onprem-lab/day05
pwd
sha256sum compose.yaml nginx.conf config/prompt.txt config/rubric.yaml .env.example
docker version
docker compose version
docker compose config --quiet && echo "문법 OK"
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
ss -ltn '( sport = :8080 )'
```

- 목적: Windows 사본과 파일 일치 여부, Docker 엔진·Compose 응답, 설정 유효성, 기존 컨테이너 및 Ubuntu 8080 리스너 확인. Docker Desktop의 호스트 포트 가용성 전체를 ss만으로 확정하지 않는다.
- Windows SHA-256(Codex 직접 확인):
  - compose.yaml: `28fe426839e574fda4f81ffb357ad8da9a140823145e231b98b1bfb79e3da10d`
  - nginx.conf: `4f6926367b943a6ab23f51051b5dab88ec58c574a7e5408f7785c0e34ae9bd2e`
  - config/prompt.txt: `258e1f7baff4e6bc2c08e6e10ce2f1506d1064b68aef9acf997883d0678565ed`
  - config/rubric.yaml: `9c602d06f106449b8574998108c2a2dce4e4163ae03c41011ff9ff5134b0c996`
  - .env.example: `c5f441309511a137b67196e7d739172a25d696caaaa8bc7b8f934aaf3a76c0d5`
- 실행 결과: 아직 받지 않았다. 컨테이너 기동·설치·동기화는 수행하지 않았다.

### 2026-09-29 — 사용자 사전 점검 결과 및 8080 포트 점유
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.
- 실행 명령: 위 사전 점검 명령 전체(사용자 제공 출력).
- 파일 확인: compose.yaml·nginx.conf·config/prompt.txt·config/rubric.yaml·.env.example의 SHA-256이 위 Windows 사본과 모두 일치한다. 실제 .env 및 셸 환경변수는 확인하지 않았다.
- 도구 확인: Docker Client/Engine 29.8.0, API 1.56, 서버 최소 API 1.40, Desktop 4.92.0(240144), linux/amd64, Context default. Compose v5.5.1이며 `문법 OK`를 확인했다.
- 컨테이너 목록: pub2는 Up 33 hours(8081 게시), pub는 Up 33 hours(127.0.0.1:8080→80), web2·web은 Up 33 hours. isolated는 Exited (0) 19 hours ago, client2는 Exited (0) 32 hours ago, client는 Exited (0) 20 hours ago. 기존 koica 앱은 Exited (143) 2 weeks ago. day05 컨테이너는 목록에 없다.
- 포트 확인: ss에 127.0.0.1:8080 LISTEN이 표시된다. Day 5 nginx의 게시 주소와 pub의 게시 주소가 겹친다.
- 기록 대조: Day 4 종료 당시 사용자 정리 완료 진술과 달리 이번 출력에는 Day 4 컨테이너 7개가 존재한다. 차이의 경위 및 네트워크 잔존 상태는 미확인이다. 과거 진술과 현재 관찰을 구분하며 현재 자원 정리 완료로 간주하지 않는다.
- 확인 주체: 사용자 제공 Ubuntu 출력과 Codex가 앞서 조회한 Windows 파일 해시를 대조. Codex가 Ubuntu에서 재실행하지 않았다.
- 다음 안내(미실행): 5-1에 필요한 8080 포트를 확보하기 위해 pub만 중지하고 아래 조회로 확인한다. 다른 자원 삭제·변경은 안내하지 않았다.

```bash
docker stop pub
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
ss -ltn '( sport = :8080 )'
docker compose config --images
```

### 2026-09-29 — pub 중지·8080 해제 및 적용 이미지 확인
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.
- 실행 명령: 위의 `docker stop pub`, 실행 중 컨테이너 목록, ss, `docker compose config --images`.
- 사용자 출력: stop은 `pub`를 반환했고 실행 중 목록에는 pub2·web2·web만 있다. ss는 헤더만 반환하여 Ubuntu 8080 리스너 부재를 확인했다.
- 적용 이미지: `agent:0.2.0`, `postgres:16.4-alpine`, `nginx:1.27-alpine`으로 가이드와 일치한다. config 출력은 로컬 이미지 존재 검증이 아니며 이번 단계에서 image inspect는 수행하지 않았다.
- 결과: 기존 pub의 포트 점유를 해소했다. pub 삭제 여부는 확인하지 않았고 다른 Day 4 자원은 잔존한다. 확인 주체는 사용자 제공 출력이며 Codex 직접 Ubuntu 실행이 아니다.
- 구성 설명: PostgreSQL의 healthy를 기다려 agent를 시작하고, agent의 healthy를 기다려 nginx를 시작한다. nginx만 127.0.0.1:8080에 게시하며, DB 데이터는 pgdata 볼륨에 저장한다. nginx에는 healthcheck가 없으므로 정상 실행 시에도 healthy 표시를 요구하지 않는다.
- 다음 안내(미실행): 아래 명령으로 5-1의 세 서비스·프로젝트 네트워크·DB 볼륨을 생성/기동하고 상태를 확인한다. `-d`는 백그라운드 실행이며, 필요한 이미지가 로컬에 없으면 기본 정책에 따라 내려받을 수 있다. API 검증은 기동 결과 확인 후 진행한다.

```bash
docker compose up -d
docker compose ps -a
```

### 2026-09-29 — Compose 기동 확인 및 API 검증 안내
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.
- 실행 명령: `docker compose up -d`, `docker compose ps -a`.
- 사용자 출력: day05_default 네트워크 및 day05_pgdata 볼륨 Created. postgres Healthy(11.2s), agent Healthy(16.8s), nginx Started(17.0s).
- ps 결과: day05-agent-1은 agent:0.2.0·Up 4 seconds (healthy)·8000/tcp, day05-postgres-1은 postgres:16.4-alpine·Up 15 seconds (healthy)·5432/tcp, day05-nginx-1은 nginx:1.27-alpine·Up Less than a second·127.0.0.1:8080→80/tcp.
- 의미: 의존 서비스의 healthy 대기 후 기동 및 nginx 포트 게시 성공을 확인했다. 8000/tcp·5432/tcp 표시는 호스트 포트 게시를 뜻하지 않는다. 이 출력만으로 실제 nginx 경유 API 성공이나 DB 인증·SQL 실행을 확인한 것은 아니다.
- 확인 주체: 사용자 제공 출력. Codex는 Windows 기록만 갱신했다.
- 다음 안내(아직 미실행): 아래 세 요청으로 nginx 경유 에이전트 응답, 설정 파일 인식·DB 접속 문자열 설정 여부, 에이전트에서 postgres:5432로 TCP 연결을 확인한다. TCP 성공은 DB 인증·SQL 검증과 구분한다.

```bash
curl -fsS --max-time 10 http://localhost:8080/healthz | jq .
curl -fsS --max-time 10 http://localhost:8080/diag | jq '{prompt_exists, prompt_sha, rubric, db_dsn_set}'
curl -fsS --max-time 10 'http://localhost:8080/tcp?host=postgres&port=5432' | jq .
```

### 2026-09-29 — API 검증 및 5-1 완료
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.
- 실행 명령: 앞서 안내한 healthz·diag·TCP 요청 세 개(curl 및 jq).
- healthz: `status=ok`, `version=0.2.0`, `host=a105f231277a`. nginx의 localhost:8080을 거친 에이전트 응답을 확인했다.
- diag: `prompt_exists=true`, `prompt_sha=258e1f7baff4`, `db_dsn_set=true`. prompt_sha는 사전 파일 해시 앞 12자리와 일치한다. rubric의 thresholds는 min_confidence=0.7·max_retries=3, weights는 grounding=0.5·completeness=0.3·format=0.2로 표시됐다.
- TCP: `ok=true`, `host=postgres`, `port=5432`, `elapsed_ms=1`. 에이전트에서 서비스 이름 postgres로 TCP 연결에 성공했다. DB 인증·SQL 실행·데이터 영속성 시험은 수행하지 않았다.
- 확인 주체: 사용자 제공 Ubuntu 출력. Codex 직접 재실행 아님.
- 완료 판단: 가이드 5-1의 세 서비스 기동·nginx 경유 응답·외부 설정 인식·DB 포트 연결을 확인해 5-1 완료. Day 5 전체 완료와 구분하며 5-2~5-4·lazydocker 관찰·최종 정리·자기점검은 미진행이다.
- 종료 상태: Day 5 세 서비스·day05_default·day05_pgdata를 유지했다. Day 4 pub는 앞서 중지했고 pub2·web2·web 등 잔존 자원은 별도 정리하지 않았다. Ubuntu 파일 동기화·PR 생성은 수행하지 않았다.

### 2026-09-29 — 5-2 시작 및 장애 전 기준 상태 조회 안내
- 사용자 요청: 다음 실습 진행. 가이드 5-2의 프로세스 종료·DB 중단·무응답 시나리오를 순서대로 진행하되 각 결과를 확인한다.
- Codex 확인: 진행·환경 기록, Day 5 README·SESSION 및 가이드 5-2를 읽었다. 이전 5-1 결과는 정상이며 자원을 유지했다.
- 첫 단계: ① 프로세스 종료 전 서비스 상태, nginx 경유 healthz, 현재 재시작 횟수와 정책을 확인한다. RestartCount를 0으로 가정하지 않고 이후 증가 여부를 비교한다.
- 안내 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.

```bash
docker compose ps -a
curl -fsS --max-time 10 http://localhost:8080/healthz | jq .
docker inspect day05-agent-1 --format 'RestartCount={{.RestartCount}} Policy={{.HostConfig.RestartPolicy.Name}}'
```

- 실행 여부: 안내만 했으며 아직 결과를 받지 않았다. 실습용 /_lab/exit 호출 및 기타 장애 유발·복구 명령은 아직 안내하거나 실행하지 않았다.
- 다음: 정상 상태와 기준 횟수를 확인한 뒤 /_lab/exit로 에이전트 프로세스 종료를 재현하고 Docker Engine이 unless-stopped 정책으로 자동 재시작하는지 관찰한다.

### 2026-09-29 — 5-2 ① 기준 상태 확인 및 프로세스 종료 안내
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.
- 사용자 실행 결과: agent·postgres는 Up 14 minutes (healthy), nginx는 Up 14 minutes 및 127.0.0.1:8080→80 게시. healthz는 status=ok·version=0.2.0·host=a105f231277a. `RestartCount=0 Policy=unless-stopped`를 확인했다.
- 확인 주체: 사용자 제공 출력. Codex가 Ubuntu 명령을 직접 실행하지 않았다.
- 소스 확인: Windows agent/app.py의 /_lab/exit는 lab_exit 로그 및 bye=true 응답 후 os._exit(1)을 호출한다. 실행 이미지와 소스 바이트 일치까지 확인한 것은 아니며 실제 결과로 검증한다.
- 다음 안내(미실행): /_lab/exit를 한 번 호출한 뒤 상태 변화를 관찰한다. 기준 0 대비 RestartCount 증가, healthy 복귀 및 nginx 경유 API 응답을 확인한다. Compose에 지정한 정책을 Docker Engine이 수행하는 실습이다.

```bash
curl -fsS --max-time 10 http://localhost:8080/_lab/exit | jq .
sleep 2
docker compose ps -a agent
sleep 12
docker compose ps -a agent
docker inspect day05-agent-1 --format 'RestartCount={{.RestartCount}} Health={{.State.Health.Status}}'
curl -fsS --max-time 10 http://localhost:8080/healthz | jq .
```

- 예상: bye=true, 재시작으로 실행 시간 초기화, health starting→healthy, RestartCount=1, healthz status=ok. 조회 시점에 따라 중간 starting은 보이지 않을 수 있다. 실제 결과는 아직 받지 않았으며 ① 완료로 기록하지 않는다.

### 2026-09-29 — 5-2 ① 자동 복구 확인 및 ② 안내
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.
- 실행 명령: 앞서 안내한 /_lab/exit 1회·sleep 2·ps·sleep 12·ps·inspect·healthz.
- 사용자 출력: bye=true, agent는 Created 16 minutes ago를 유지하며 Up 1 second (health: starting) → Up 13 seconds (healthy). `RestartCount=1 Health=healthy`. healthz는 status=ok·version=0.2.0·host=a105f231277a.
- 의미: 기준 RestartCount=0에서 1로 증가했다. 수동 재시작 명령 없이 unless-stopped 정책으로 프로세스가 재시작되고 API가 복구됐다. 같은 컨테이너의 재시작이며 새 컨테이너 생성이나 무중단 응답을 검증한 것은 아니다. ① 완료.
- 확인 주체: 사용자 제공 출력. Codex 직접 Ubuntu 실행 아님.
- 다음 안내(미실행): ② postgres만 수동 중지한 상태에서 agent의 healthz와 DB TCP 연결을 비교하고 postgres를 다시 시작한다. 그 후 postgres 상태와 TCP 연결 회복을 확인한다.

```bash
docker compose stop postgres
docker compose ps -a
curl -fsS --max-time 10 http://localhost:8080/healthz | jq .
curl -fsS --max-time 10 'http://localhost:8080/tcp?host=postgres&port=5432' | jq .
docker compose start postgres
sleep 12
docker compose ps -a postgres
curl -fsS --max-time 10 'http://localhost:8080/tcp?host=postgres&port=5432' | jq .
```

- 예상: DB 중단 중에도 healthz는 status=ok이나 TCP는 ok=false. 가이드 예시는 gaierror지만 실제 error_type·error를 그대로 확인한다. 재기동 후 postgres healthy·TCP ok=true를 확인해야 ② 복구 완료로 판단한다. DB 중단은 의도한 실습이며 /healthz가 의존성까지 점검하지 않는 한계를 관찰한다.
- 실행 여부: ② 명령은 안내만 했으며 결과 대기. ③ 무응답 실습은 아직 시작하지 않았다.

### 2026-09-29 — 5-2 ② DB 중단·복구 확인 및 ③ 안내
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.
- 실행 명령: 앞서 안내한 postgres stop·ps·healthz·TCP 요청 및 postgres start·sleep 12·ps·TCP 재요청.
- 중단 중 사용자 출력: postgres Exited (0), agent Up 4 minutes (healthy), nginx Up 19 minutes. healthz status=ok·version=0.2.0·host=a105f231277a. TCP는 ok=false·error_type=gaierror·error=[Errno -3] Temporary failure in name resolution.
- 복구 출력: postgres Up 12 seconds (healthy), TCP ok=true·host=postgres·port=5432·elapsed_ms=0.
- 의미: 에이전트의 healthz는 DB 상태를 점검하지 않아 DB 중단에도 정상 응답했다. 이 실행에서 DB 진단은 이름 해석 단계에서 실패했다. DB를 수동 재기동한 뒤 healthy와 TCP 연결 회복을 확인해 ② 완료. DB 인증·SQL 복구를 검증한 것은 아니다.
- 확인 주체: 사용자 제공 출력. Codex 직접 Ubuntu 실행 아님.
- 다음 안내(미실행): ③ 아래 첫 묶음으로 에이전트를 무응답 상태로 만들고 40초 후 unhealthy·RestartCount 불변·curl 타임아웃을 관찰한다. 마지막 확인 재시작 횟수는 1이며 호출 직전에도 조회해 비교한다. healthz 요청은 jq에 파이프하지 않고 바로 다음 줄에서 curl 종료코드를 확인한다.

```bash
docker inspect day05-agent-1 --format 'RestartCount={{.RestartCount}} Health={{.State.Health.Status}}'
curl -fsS --max-time 10 http://localhost:8080/_lab/hang | jq .
sleep 40
docker compose ps -a agent
docker inspect day05-agent-1 --format 'RestartCount={{.RestartCount}} Health={{.State.Health.Status}}'
curl -sS --max-time 3 http://localhost:8080/healthz
echo "종료코드=$?"
```

- 예상: hang=true, agent는 실행 중이지만 unhealthy, RestartCount는 1 유지, curl 종료코드 28. 아직 실제 결과가 아니다. 관찰 후 아래 두 번째 묶음으로 수동 재시작하고 서비스 상태·API·DB TCP 회복을 확인한다.

```bash
docker compose restart agent
sleep 12
docker compose ps -a
curl -fsS --max-time 10 http://localhost:8080/healthz | jq .
curl -fsS --max-time 10 'http://localhost:8080/tcp?host=postgres&port=5432' | jq .
```

- 실행 여부: ③과 복구는 안내만 했으며 결과 대기. 무응답 관찰 또는 복구를 완료로 기록하지 않는다.

### 2026-09-29 — ③ 기존 무응답 상태 관찰 및 수동 복구 확인
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.
- 사용자 출력: hang 호출 전부터 RestartCount=1 Health=unhealthy. /_lab/hang 요청은 bye나 hang 응답 없이 10초 후 curl 코드 28로 종료했다. 40초 대기 후 agent는 Created 28 minutes ago·Up 12 minutes (unhealthy), RestartCount=1 Health=unhealthy를 유지했다. healthz는 3초 후 타임아웃이며 바로 다음 echo에서 종료코드=28을 확인했다.
- 의미: 실행 중 무응답·unhealthy 상태에서도 관찰 구간 동안 자동 재시작되지 않은 사실은 확인했다. 하지만 무응답이 이번 /_lab/hang 호출 전부터 존재하므로 이 호출로 정상→무응답 전환이 발생했다고 기록하지 않는다. 이전 호출 여부·원인은 미확정이다.
- 수동 복구: docker compose restart agent 후 ps에서 agent Up 12 seconds (healthy), nginx Up 28 minutes, postgres Up 8 minutes (healthy). healthz status=ok·version=0.2.0·host=a105f231277a, DB TCP ok=true·elapsed_ms=0. restart 진행 표시가 0/1이었어도 후속 상태·API로 복구를 확인했다. 수동 재시작 후 RestartCount는 아직 조회되지 않았다.
- 확인 주체: 사용자 제공 출력. Codex 직접 Ubuntu 실행 아님.
- 추가 확인 이유: 무응답 유발 직전 정상 상태와 hang=true 응답이 누락됐다. 복구된 상태에서 아래 관찰을 한 번 더 안내한다. 첫 조회가 healthy가 아니면 hang을 호출하지 않고 출력을 공유하도록 안내한다.

```bash
docker inspect day05-agent-1 --format 'RestartCount={{.RestartCount}} Health={{.State.Health.Status}}'
curl -fsS --max-time 10 http://localhost:8080/_lab/hang | jq .
sleep 40
docker inspect day05-agent-1 --format 'RestartCount={{.RestartCount}} Health={{.State.Health.Status}}'
curl -sS --max-time 3 http://localhost:8080/healthz
echo "종료코드=$?"
```

- 관찰 후 복구 안내:

```bash
docker compose restart agent
sleep 12
docker compose ps -a
curl -fsS --max-time 10 http://localhost:8080/healthz | jq .
```

- 현재 확인된 상태는 수동 복구 후 정상이며 재현·복구 재확인 명령은 아직 실행 결과를 받지 않았다. 재현 전후 RestartCount는 첫 조회의 실제 값을 비교하며 1이라고 가정하지 않는다.

### 2026-09-29 — ③ 정상→무응답 재현·복구 및 5-2 완료
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.
- 실행 명령: 직전 안내의 inspect·hang·sleep 40·inspect·healthz/종료코드 조회 및 restart·sleep 12·ps·healthz.
- 재현 전: `RestartCount=0 Health=healthy`. 이전 수동 재시작 후 이번 기준 조회에서 0을 확인했으며 이전 1을 기준으로 비교하지 않는다.
- 장애 유발: /_lab/hang 응답은 `hang=true`. 40초 뒤 `RestartCount=0 Health=unhealthy`. healthz는 3002ms 후 0바이트 수신으로 시간 초과했고 종료코드 28을 확인했다.
- 의미: 정상에서 무응답으로 전환된 것을 이번에는 직접 관찰했다. unhealthy가 되었지만 RestartCount 0→0으로 자동 재시작되지 않았다. 첫 관찰부터 unhealthy였던 과거 원인은 여전히 미확정이며 이번 재현과 구분한다.
- 수동 복구: docker compose restart agent 후 agent Up 10 seconds (healthy), nginx Up 31 minutes·127.0.0.1:8080→80, postgres Up 11 minutes (healthy). healthz는 status=ok·version=0.2.0·host=a105f231277a. restart의 중간 진행 표시 0/1과 별개로 후속 조회와 API로 복구를 확인했다. 이번 마지막 복구 직후 DB TCP 요청은 반복하지 않았으며 직전 복구 때 성공한 이력과 구분한다.
- 확인 주체: 사용자 제공 Ubuntu 출력. Codex 직접 실습 실행 아님.
- 완료 판단: ① 프로세스 종료 후 자동 재시작, ② DB 중단에도 healthz 정상이나 TCP 실패 및 DB 복구, ③ 무응답·unhealthy에서 자동 재시작 없음 및 수동 복구를 모두 확인해 5-2 완료.
- 남은 범위: 5-3·5-4·lazydocker 관찰·최종 정리·자기점검. Day 5 전체 완료로 처리하지 않는다. Day 5 서비스·네트워크·볼륨 및 다른 Day 4 잔존 자원은 유지한다.

### 2026-09-29 — 5-3 시작 및 변경 전 기준 조회 안내
- 사용자 요청: 다음 실습 진행. 5-3만 진행하며 변경 전 확인 → 프롬프트 한 줄 추가 → 재시작 없는 반영 확인 → 원복을 계획한다.
- Codex 확인: PROGRESS·환경·Day 5 README/SESSION·가이드 5-3, Windows prompt.txt 및 agent/app.py의 load_prompt를 읽었다. Ubuntu 파일은 직접 조회하거나 수정하지 않았다.
- 구조: compose.yaml의 ./config:/app/config:ro 마운트로 Ubuntu 파일이 컨테이너에 보인다. 읽기 전용은 컨테이너 측 쓰기 제한이며 호스트의 파일 수정은 가능하다. load_prompt는 호출 시 5초 캐시 제한을 적용하고 파일 mtime 변경을 확인해 다시 읽는다. 독립적인 5초 주기 백그라운드 감시라고 설명하지 않는다.
- 안내 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.

```bash
cat config/prompt.txt
curl -fsS --max-time 10 http://localhost:8080/prompt
docker inspect day05-agent-1 --format 'Image={{.Image}}{{println}}StartedAt={{.State.StartedAt}}{{println}}RestartCount={{.RestartCount}} Health={{.State.Health.Status}}'
```

- 목적: 수정 전 파일과 API 내용 대조 및 이미지 ID·기동 시각·재시작 횟수를 변경 후 비교할 기준으로 확보한다. 실습은 LLM 출력 변화가 아니라 프롬프트 파일 재적재를 검증한다.
- 실행 여부: 안내만 했으며 결과 대기 중이다. 프롬프트 수정·재시작·재빌드·파일 동기화는 수행하지 않았다.

### 2026-09-29 — 5-3 변경 전 기준 확인 및 한 줄 추가 안내
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.
- 사용자 출력: cat과 /prompt가 모두 원본 두 문장(사내 업무 지원 에이전트, 제공된 데이터에 근거하며 근거 없으면 모른다고 답하기)을 반환했다. 출력이 두 번 반복된 것은 파일 조회와 API 조회가 각각 같은 내용을 반환했기 때문이다.
- 기준 이미지 ID: `sha256:a4ef49ae142efb1a03fe43c30d4a6f68ceee1c649578c33407827e8f6f4185a3`.
- 기준 StartedAt: `2026-09-29T00:48:28.108529054Z`. RestartCount=0, Health=healthy.
- 확인 주체: 사용자 제공 출력. Codex가 Ubuntu에서 직접 확인한 것은 아니다.
- 다음 안내(미실행): mktemp로 고유 임시 백업을 만들고 복사가 성공한 경우에만 한 줄을 추가한다. 아래 첫 줄은 한 번만 실행하며 실패하면 중단한다. 같은 터미널에서 백업 경로 변수 day05_prompt_backup을 유지해 이후 원복에 사용한다.

```bash
day05_prompt_backup=$(mktemp /tmp/day05-prompt.XXXXXX) && cp -- config/prompt.txt "$day05_prompt_backup" && printf '%s\n' '추가 지침: 답변은 5문장 이내로.' >> config/prompt.txt
printf '원본 백업: %s\n' "$day05_prompt_backup"
sleep 6
curl -fsS --max-time 10 http://localhost:8080/prompt
docker compose logs --since 2m --no-log-prefix agent | grep prompt_reloaded
docker inspect day05-agent-1 --format 'Image={{.Image}}{{println}}StartedAt={{.State.StartedAt}}{{println}}RestartCount={{.RestartCount}} Health={{.State.Health.Status}}'
```

- 목적: /prompt의 추가 문장 및 prompt_reloaded 로그, 동일 이미지 ID·StartedAt·RestartCount로 재빌드·재시작 없는 반영을 검증한다. 6초 대기 후 요청 시 캐시의 파일 변경 검사 제한(5초)을 지나도록 한다.
- 실행 여부: 백업·파일 변경·반영은 아직 결과를 받지 않았다. 원복은 반영 결과 확인 후 안내한다. Windows prompt.txt는 변경하지 않았다.

### 2026-09-29 — 5-3 프롬프트 반영 확인 및 원복 안내
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.
- 사용자 실행: 직전 안내의 mktemp·cp·printf 추가·sleep 6·/prompt·재적재 로그·inspect.
- 백업 경로: `/tmp/day05-prompt.GrrBHr`.
- API 응답: 원본 두 문장에 `추가 지침: 답변은 5문장 이내로.`가 추가됐다.
- 로그: 2026-09-29T01:16:01+0000의 원본 sha=258e1f7baff4와 01:17:55+0000의 변경 sha=a9099fd31924가 각각 prompt_reloaded로 표시됐다. --since 2m 범위에 두 이벤트가 포함된 것이며 중복 변경이라고 판단하지 않는다.
- 불변 확인: Image=sha256:a4ef49ae142efb1a03fe43c30d4a6f68ceee1c649578c33407827e8f6f4185a3, StartedAt=2026-09-29T00:48:28.108529054Z, RestartCount=0, Health=healthy. 변경 전 기준과 일치한다.
- 의미: 이미지 재빌드·컨테이너 재시작 없이 외부 프롬프트의 변경을 읽었다. 실제 LLM 답변이 5문장으로 제한되는지는 검증하지 않았다.
- 확인 주체: 사용자 제공 Ubuntu 출력. Windows prompt.txt는 변경하지 않았고 Ubuntu와 동기화하지 않았다.
- 다음 안내(미실행): 확인된 백업으로 원복하고 바이트 일치·API 내용·프롬프트 해시를 확인한다. 첫 줄에서 오류가 나면 멈추고 결과를 공유한다. 백업은 아직 삭제하지 않는다.

```bash
cp -- /tmp/day05-prompt.GrrBHr config/prompt.txt && cmp -- /tmp/day05-prompt.GrrBHr config/prompt.txt && echo "원본 파일 복원 확인"
sleep 6
curl -fsS --max-time 10 http://localhost:8080/prompt
curl -fsS --max-time 10 http://localhost:8080/diag | jq '{prompt_exists, prompt_sha}'
```

- 예상: 원본 파일 복원 확인, API에 원본 두 문장만 표시, prompt_exists=true·prompt_sha=258e1f7baff4. 원복 결과는 아직 받지 않았으며 5-3 완료로 기록하지 않는다.

### 2026-09-29 — 5-3 원복 확인 및 절 완료
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.
- 실행 명령: 백업 /tmp/day05-prompt.GrrBHr를 config/prompt.txt로 cp, cmp 및 성공 문구 출력, sleep 6, /prompt와 /diag 조회(직전 안내 명령).
- 사용자 출력: `원본 파일 복원 확인`. /prompt는 원본 두 문장만 반환했다. /diag는 prompt_exists=true·prompt_sha=258e1f7baff4를 반환했다.
- 의미: 백업과 복원 파일의 바이트 일치, API에서 추가 문장 제거, 원본 프롬프트 해시 복귀를 확인했다. 앞선 변경 반영 때 이미지 ID·StartedAt·RestartCount 불변을 확인했으며 원복도 재시작 명령 없이 적용됐다.
- 확인 주체: 사용자 제공 Ubuntu 출력. Codex 직접 Ubuntu 실행·파일 수정 아님.
- 완료 판단: 5-3 변경·재적재·원복 완료. LLM 실제 답변 변화는 검증하지 않았다. 5-4·lazydocker 관찰·최종 정리·자기점검은 미진행이다.
- 남은 자원: Day 5 서비스·네트워크·볼륨은 유지한다. 임시 백업 /tmp/day05-prompt.GrrBHr는 삭제하지 않았다. Windows prompt.txt는 원본 그대로이며 Ubuntu 복원 결과는 위 사용자 증거로 확인했다.

### 2026-09-29 — 5-4 시작 및 공개 더미 값 치환 안내
- 사용자 요청: 다음 실습 진행. 5-4만 시작한다.
- Codex 확인: 진행·환경 기록, Day 5 README·SESSION, 가이드 5-4 및 Windows .env.example·compose.yaml을 읽었다. 실제 .env나 실행 컨테이너의 환경변수 전체는 조회하지 않았다.
- 목표: Compose 변수 치환 후 DB_DSN과 POSTGRES_PASSWORD에 값이 평문으로 표시됨을 공개 더미 값으로 확인한다. .env는 암호화나 자동 비밀 은닉 기능이 아니며 예시 파일 자체가 자동 적용되는 것은 아니다.
- 안내 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.

```bash
cat .env.example
POSTGRES_PASSWORD=demo-only docker compose config | grep -E 'DB_DSN:|POSTGRES_PASSWORD:'
```

- demo-only는 실제 자격 증명이 아닌 공개 실습용 더미 문자열이다. 해당 명령에만 환경변수를 지정하고 두 관련 항목만 출력한다. 원래 비밀값의 조회·공유를 요청하지 않는다.
- 예상: DB_DSN에 postgresql://appuser:demo-only@postgres:5432/appdb, POSTGRES_PASSWORD에 demo-only가 나타난다. 실제 출력은 아직 미수신이다.
- 실행 의미: config는 Compose의 치환된 배포 설정을 미리 보여 준다. 실행 중 컨테이너 설정이나 PostgreSQL 계정 비밀번호를 변경한 것이 아니다. .env 작성·수정、up·재시작은 수행하지 않는다.
- 확인 주체: Codex는 Windows 자료만 확인했다. 사용자 실행 결과 대기이며 5-4는 미완료다.

### 2026-09-29 — 5-4 예시 변수 치환 확인 및 절 완료
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.
- 사용자 실행: `cat .env.example` 및 앞서 안내한 POSTGRES_PASSWORD=demo-only를 해당 명령에만 지정한 compose config의 두 DB 설정 항목 조회.
- 예시 파일 출력: AGENT_IMAGE=agent:0.2.0, POSTGRES_PASSWORD=change-me, LOG_LEVEL=INFO 및 .env를 Git에 넣지 않는다는 안내 주석. change-me와 demo-only는 공개 예시 문자열이며 실제 자격 증명이 아니다.
- 치환 결과: `DB_DSN: postgresql://appuser:demo-only@postgres:5432/appdb`, `POSTGRES_PASSWORD: demo-only`.
- 의미: 해당 명령에 전달한 환경변수가 최종 설정의 DB 접속 문자열·비밀번호 항목에 반영되고 평문으로 표시됐다. 예시 파일은 cat으로 읽었을 뿐 자동 적용한 것이 아니다. 실제 .env 파일 사용·수정이나 실행 중 컨테이너·DB 계정 비밀번호 변경을 수행한 것은 아니다.
- 확인 주체: 사용자 제공 Ubuntu 출력. Codex 직접 Ubuntu 실행 아님.
- 완료 판단: 가이드 5-4의 예시 파일 조회 및 공개 더미 값으로 최종 설정 치환·평문 노출 확인 완료. 실제 비밀값은 조회·보관하지 않았다. .env로 분리하더라도 암호화되는 것은 아니며 최종 설정 공유 시 비밀값을 제거해야 한다는 점을 설명한다.
- 남은 범위: lazydocker 프로젝트·로그·자원·헬스 관찰, 최종 정리, 자기점검. Day 전체 완료로 처리하지 않는다. Day 5 서비스·네트워크·볼륨과 임시 백업은 유지 중이다.

### 2026-09-29 — lazydocker 정상 상태 관찰 안내
- 사용자 요청: lazydocker에서 확인하는 방법 안내.
- Codex 확인: 진행·환경·Day 5 기록, 가이드의 화면 관찰 절 및 compose.yaml의 메모리 제한 512M·CPU 제한 1.0 설정을 읽었다. 과거 Day 4에서 lazydocker 0.25.2 표시와 CLI 결과가 달랐던 이력을 고려해 화면 표시를 미리 단정하지 않는다.
- 안내 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.

```bash
cd /home/user/onprem-lab/day05
lazydocker
```

- 첫 관찰: Containers 또는 Services에서 day05 소속 nginx·agent·postgres를 찾고, agent를 선택해 상태 및 Logs·Stats를 본다. 가이드의 탭 전환 키는 [와 ]이며 실제 화면 하단 도움말을 우선한다.
- 기대: agent·postgres 정상, nginx 실행 중. Logs에서 healthz 요청·prompt_reloaded 등 이벤트, Stats에서 CPU·메모리 사용량을 관찰한다. 로그 이벤트가 현재 화면에 모두 보인다고 가정하지 않는다. 메모리 그래프 눈금의 최대값을 컨테이너 제한으로 단정하지 않으며 제한 표시가 없으면 CLI로 보완한다.
- 화면 공유: agent를 선택한 Logs 또는 Stats 화면을 요청한다. Config/Env에는 접속 정보가 표시될 수 있으므로 해당 화면의 비밀값을 공유하지 않도록 안내한다.
- 실행 여부: 안내만 했으며 사용자 화면·결과는 아직 없다. 별도 터미널의 요청 발생이나 hang 재현은 이 단계에서 안내·실행하지 않는다. 정상 상태 관찰 후 필요한 화면 확인 및 가이드의 상태 변화 관찰로 이어 간다.

### 2026-09-29 — lazydocker 전체 화면 확인 및 agent 위치 안내
- 사용자 질문: 에이전트가 어디 있는지 모르겠다는 요청과 day5_lazydocker.png 제공.
- 증거: [사용자 전체 화면](evidence/lazydocker-overview-user-2026-09-29.png). Codex가 제공된 원본을 Windows evidence 폴더로 복사했으며 수정하지 않았다.
- 화면: lazydocker 0.25.2. [1]-Project는 day05, [2]-Services에는 agent running (healthy)·8000/tcp, nginx running·게시 주소 일부, postgres running (healthy)·5432/tcp가 보인다. 각 서비스 CPU 표시는 0.00%다. 잘린 nginx 주소 전체는 이 화면만으로 판독하지 않는다.
- 현재 선택: 녹색 테두리의 [3]-Standalone Containers에서 exited (0) pub가 파란색으로 선택돼 있다. 오른쪽 Logs 탭은 선택돼 있으나 내용이 비어 있다. 이 상태로 agent의 로그가 없다고 판단하지 않는다.
- 기타 관찰: day05_pgdata 볼륨과 day05_default 네트워크 존재. lab-net·other-net 및 이전 실습 컨테이너도 남아 있다. 기존 koica 관련 자원도 화면에 보이며 변경하지 않았다.
- 다음 안내: 숫자 2로 Services 패널 이동 후 위/아래 화살표로 첫 행 agent를 선택하고 오른쪽 Logs를 확인한다. 상단 Logs 오른쪽에 Stats 탭이 있다. 상세 화면을 받아 추가 해석한다.
- 확인 주체: 사용자 스크린샷 판독. Codex가 Ubuntu 명령이나 UI를 직접 조작한 것은 아니다. 프로젝트·정상 상태 관찰은 확인했고 agent 로그·Stats·unhealthy 변화 화면은 아직 미확인이다.

### 2026-09-29 — lazydocker 로그 표시 사용자 확인 및 완료 범위 정리
- 사용자 응답: agent 선택·Logs 확인 안내 후 “잘 나오는군 실습 완료인가”. 문맥상 로그 표시 성공에 대한 사용자 진술로 기록한다. 후속 스크린샷·로그 원문은 받지 않았으므로 개별 이벤트나 Stats 내용을 직접 확인했다고 기록하지 않는다.
- 완료 범위: 5-1~5-4의 명령 실습은 완료. lazydocker 프로젝트·세 서비스 정상 상태는 앞선 화면으로 확인했고 로그 표시는 이번 사용자 진술로 확인했다.
- 남은 범위: Stats의 자원 사용량·제한 확인, 가이드의 TUI unhealthy 변화 관찰, 자원 정리 및 자기점검. unhealthy 재현·수동 복구 자체는 이미 5-2 CLI 출력으로 확인한 것과 구분한다.
- 상태: 서비스·네트워크·볼륨·임시 백업은 유지 중이다. 이번 완료 여부 질문을 자원 삭제·정리 요청으로 해석하지 않았으며 Ubuntu 명령을 실행하거나 삭제 명령을 안내하지 않았다. Day 5 전체는 완료 처리하지 않는다.

### 2026-09-29 — 체크포인트 5문항 해설
- 사용자 요청: 체크포인트 다섯 문항에 대한 이해하기 쉬운 답변. 답변 설명이며 사용자의 독립적인 자기점검 응답·평가 통과로 기록하지 않는다.
- 1번 보완: Compose도 정식 운영에 사용할 수 있다. 단일 서버 장애 시 자동 이전, 무응답 자동 복구, 무중단 순차 배포 같은 기능은 이번 Compose 구성만으로 제공되지 않아 운영 요구에 따른 추가 설계가 필요하다고 설명한다.
- 2번: 기본 json-file 로그에 회전·크기 제한이 없으면 디스크를 소진할 수 있다. 이번 max-size=10m·max-file=3은 로그 크기·보관 수를 제한한다. Docker 전역 기본 설정으로도 가능하므로 모든 Compose 파일의 logging 키 자체가 절대 필수라는 의미와 구분한다.
- 3번: 프로세스가 실행 중이면 restart 정책의 종료 조건이 발생하지 않는다. unhealthy 판정과 복구 동작을 구분하며 올바르게 설정한 Kubernetes liveness probe 또는 외부 복구 자동화가 대응할 수 있음을 설명한다. 실습은 수동 재시작으로 복구했다.
- 4번: 기본 docker compose kill은 운영자의 강제 중지 요청이며 이번 unless-stopped 정책에서 이를 자동으로 되살리지 않는다. ①의 /_lab/exit는 프로그램 스스로 비정상 종료시켜 자동 복구를 확인했다. kill 동작은 설명만 했으며 이번 환경에서 직접 시험하지 않았다.
- 5번: 폐쇄망에서 이미지 재빌드·스캔·반입 절차를 반복하지 않고 허용된 설정 변경 절차로 프롬프트를 조정할 수 있다. 외부 파일 마운트뿐 아니라 애플리케이션의 파일 재적재 구현이 필요하다. 모든 설정 변경이 무승인이라는 뜻은 아니다.
- 공식 근거: [Compose 운영 배포](https://docs.docker.com/compose/how-tos/production/), [재시작 정책](https://docs.docker.com/engine/containers/start-containers-automatically/), [로그 설정](https://docs.docker.com/engine/logging/configure/), [JSON 로그](https://docs.docker.com/engine/logging/drivers/json-file/), [compose kill](https://docs.docker.com/reference/cli/docker/compose/kill/), [Kubernetes probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/).
- 자원 상태: 변경하지 않았다. Stats·제한·TUI 상태 변화 관찰 및 최종 정리는 남아 있다.

### 2026-09-29 — Day 5 종료 정리 안내(결과 대기)
- 사용자 요청: 체크포인트 해설 후 정리·마무리.
- 범위: Day 5 컨테이너 3개와 day05_default 네트워크를 compose down으로 제거한다. 가이드 기본 방식에 따라 day05_pgdata DB 볼륨과 이미지는 보존한다. Day 4 잔존 컨테이너·네트워크 및 koica 자원은 이번 명령 대상이 아니다. 임시 백업 /tmp/day05-prompt.GrrBHr도 이번 정리 명령에 포함하지 않는다.
- 실행 위치: lazydocker에서 q로 나온 뒤 Ubuntu WSL2 `/home/user/onprem-lab/day05`. cd 실패 시 다음 명령을 실행하지 않는다.

```bash
cd /home/user/onprem-lab/day05
docker compose down
docker compose ps -a
docker network ls --filter name=day05_default
docker volume ls --filter name=day05_pgdata
ss -ltn '( sport = :8080 )'
```

- 기대 결과: 컨테이너 3개·네트워크 제거, 프로젝트 컨테이너 및 해당 네트워크 목록은 헤더만 표시, DB 볼륨은 존재, Ubuntu 8080 리스너는 없음.
- 확인 주체: 현재는 명령 안내만 했다. 사용자 정리 결과는 아직 받지 않았고 Codex가 Ubuntu 자원을 삭제하지 않았다.
- 종료 기록 원칙: 5-1~5-4 핵심 실습, 정상 상태·로그 관찰, 체크포인트 해설과 실제 정리 결과를 구분한다. Stats·제한 및 TUI unhealthy 변화 화면, 사용자의 독립적인 자기점검 평가는 미확인으로 보존한다. 사용자의 종료 요청에 따라 추가 실습을 강제로 진행하지 않는다.

### 2026-09-29 — Day 5 자원 정리 확인 및 종료
- 사용자 요청: 앞선 마무리 요청에 따른 정리 결과 제공.
- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day05`.
- 실행 명령: 앞서 안내한 compose down·ps -a·네트워크/볼륨 필터 조회·ss. lazydocker 실행 후 셸 프롬프트로 돌아온 내용도 제공됐다.
- 결과: day05-nginx-1·day05-agent-1·day05-postgres-1 및 day05_default가 Removed. 프로젝트 ps와 네트워크 목록은 헤더만 표시. day05_pgdata 볼륨은 local로 존재하며 ss에는 8080 LISTEN 행이 없다.
- 증거: [사용자 정리 출력 발췌](evidence/cleanup-user-2026-09-29.txt). 공백·장식을 간소화한 발췌이며 실제 사용자 결과에 근거한다.
- 확인 주체: 사용자 제공 출력. Codex가 Ubuntu 정리 명령을 직접 실행하지 않았다.
- 보존 범위: day05_pgdata는 출력으로 존재 확인. 이미지와 임시 백업 /tmp/day05-prompt.GrrBHr는 삭제 대상으로 지정하지 않았으며 이번 단계에서 재조회하지 않았다. Day 4 잔존 자원·koica 자원도 정리 범위에 포함하지 않았다.
- 종료 판단: 사용자 마무리 요청 및 핵심 실습 5-1~5-4·정상 상태/로그 관찰·체크포인트 해설·지정 자원 정리 확인을 근거로 Day 5를 종료한다. Stats·자원 제한과 TUI unhealthy 변화 화면, 사용자 독립 자기점검 평가는 미확인/미진행으로 남기며 모든 항목을 검증했다고 기록하지 않는다.
- Codex 작업: Windows SESSION·README·PROGRESS·환경 기록 및 정리 증거를 갱신한다. Ubuntu 동기화·Day 6 실행·커밋·PR 생성은 수행하지 않는다.

### 2026-09-29 — 학습 요약 및 PR 준비
- 사용자 요청: Day 5 핵심 메시지·배운 내용을 쉬운 언어로 요약한 뒤 Day 5를 마무리하고 PR 생성.
- 핵심 메시지: 여러 프로그램을 함께 실행하는 것과 장애에도 안정적으로 운영하는 것은 다르다. Compose의 사용 여부만으로 정식 운영 가능 여부를 판단하지 않는다.
- README에 실행 구성, 자동 재시작의 한계, healthz의 검사 범위, 외부 설정과 재적재, 환경변수의 평문 노출, 컨테이너와 볼륨의 수명 차이를 실습 근거와 함께 정리했다.
- PR 범위: Day 5 기록·증거, 전체 진행·환경 기록 및 이전 세션에서 다음 기록 커밋에 포함하기로 남긴 Day 4 PR #6 병합 확인 메모. 실습 소스 변경이나 Ubuntu 재실행·동기화는 포함하지 않는다.
- Codex 직접 확인: GitHub 인증과 원격 조회 성공. PR 제출 결과와 문서 검증 결과는 후속 기록에 남긴다. Day 6은 미시작이다.
- 문서 검증: git diff --check 통과, 변경 문서 5개의 로컬 링크 56개 대상 존재 확인. 추가 텍스트의 대표 자격 증명 패턴 검사와 사용자 화면·정리 증거 검토를 수행했다. 환경변수 예시는 공개 더미 값이다. 문서·증거만 변경하므로 애플리케이션 테스트나 Ubuntu 실습 재실행은 수행하지 않았다.

### 2026-09-29 — PR 제출
- 제출 결과: [PR #7](https://github.com/shanis345/Deploy_Practice/pull/7), `codex/day05-results` → `main`. 기록 커밋은 `209fc6a`이며 PR 링크를 인수인계 기록에도 추가했다. 병합은 수행하지 않았다.
- Git 처리: 작성자 설정 누락으로 첫 커밋이 실패해 기존 실습 커밋의 이름·GitHub 비공개 이메일을 해당 커밋 명령에만 지정한 뒤 성공했다. 전역 Git 설정은 변경하지 않았다.
- 완료 범위와 미확인 항목은 위 종료 기록대로 유지한다. Ubuntu 복사본은 변경하지 않았으며 다음은 사용자 요청 시 Day 6이다.

## 오류와 해결
- 기동 전 발견: 기존 pub가 Day 5 nginx와 동일한 127.0.0.1:8080을 사용 중이었다. 충돌 가능성을 사전 점검에서 발견했으며 실제 기동 오류를 받은 것은 아니다.
- 대응: 사용자 출력으로 pub 중지·8080 리스너 해제 후 Day 5 nginx 기동·포트 게시 성공을 확인했다.

## 배운 내용과 질문
- PostgreSQL은 데이터 저장·조회, nginx는 이번 구성의 리버스 프록시, Compose는 여러 서비스의 실행 설정과 기동을 함께 관리하는 역할로 설명했다.
- 사용자는 Compose의 장단점, KOICA 장애와의 연관성, Kubernetes 비교 및 국내 도입 비율을 질문했다. KOICA의 실제 장애 원인은 로그·구성을 확인하지 않아 확정하지 않았다. 도구 선택만으로 안정성을 보장하지 않으며 장애 원인과 복구 능력을 구분했다.
- 실제 기동 순서는 postgres healthy → agent healthy → nginx이며, 요청 경로는 nginx → agent다. TCP 진단 요청은 agent → postgres:5432 연결을 검사한다.
- 5-2 핵심: restart 정책은 프로세스 종료에 대응하며 unhealthy 표시만으로 자동 재시작하지 않는다. 현재 healthz는 DB 의존성 정상 여부를 보장하지 않는다. 설정된 정책을 실행하는 주체는 Docker Engine이다.
- 5-3 핵심: 외부 파일 마운트와 애플리케이션의 재적재 구현을 함께 사용하면 프롬프트를 이미지 재빌드·컨테이너 재시작 없이 변경할 수 있다. 모든 설정이 자동 재적재된다고 일반화하지 않는다.
- 5-4 핵심: 변수로 설정을 분리하는 것과 비밀값을 암호화하는 것은 다르다. compose config는 치환된 배포 설정을 보여 주며 실행 중 서비스의 변경·배포를 수행하지 않는다.

## 가이드와 실제 환경의 차이
공통 환경은 [환경 기록](../docs/environment.md)을 참고한다.

## 다음에 이어 할 지점
Day 5 종료. 다음은 사용자 요청 시 Day 6이며 자동 시작하지 않는다. Day 5 컨테이너·네트워크 제거 및 8080 해제, DB 볼륨 보존을 확인했다. 이미지·임시 백업 /tmp/day05-prompt.GrrBHr와 Day 4·koica 자원은 정리 대상이 아니었다. Stats·TUI 상태 변화 화면과 별도 자기점검 평가는 미확인으로 보존한다. Windows 기록과 Ubuntu 실습 폴더는 별도이며 동기화하지 않았다.
