# Day 8 — 사내 CA와 TLS 검사(SSL 인스펙션)

## 진행 상태
- 상태: 종료(2026-10-01) · 8-1~8-4 실습·자원 정리·체크포인트 해설 완료 · 독립 평가 미실시
- 완료한 범위: 8-1 프록시·CA 준비, 8-2 실패 재현·두 해결 방식·임시 빌드용 CA 사본 제거, 8-3 발급자·번들·curl 비교, 8-4 HTTPS 요청·응답 헤더와 복호화된 응답 본문 관찰
- 중단 지점: Day 8 종료·체크포인트 해설 제공. CA·이미지는 보존, Day 9는 사용자 요청 후 진행
- Codex 작업: 아직 별도 작업을 만들지 않음
- 실행 증거 기준: 사용자 제공 출력과 직접 검증 결과를 구분해 기록

## 목표와 이번 세션 범위
2026-10-01 사용자 요청으로 8-1~8-4를 완료한 뒤 "좋아 그러면 정리하자" 요청에 따라 Day 8 종료 정리를 안내한다. 사용자가 Ubuntu WSL2에서 직접 실행한다. 정리 대상은 Day 8 컨테이너 5개·네트워크 2개이며 certs·이미지·기존 백업은 보존한다. Day 9는 시작하지 않는다.

## 실행 기록
### 2026-10-01 — 8-1 사전 점검 안내(결과 대기)
- Codex 직접 확인 위치: Windows 프로젝트. PROGRESS.md, docs/environment.md, Day 8 README·SESSION, 가이드 8-1 및 compose.yaml을 읽었다.
- Windows compose.yaml SHA-256: `3ce23a8732febb08b91acc12d0b253fdd7d98ef0b760b26d5173fdc5b68793bf`. Ubuntu 사본과의 일치는 미확인이다.
- Windows 설정에는 mitmproxy:11.0.0의 web_password=lab 및 호스트 8081 게시가 남아 있다. Day 7 기록의 옵션 차이·8081 충돌 이력을 반영하되, 실제 Ubuntu 파일·현재 포트 상태 확인 후 조정한다. 실습 소스는 아직 변경하지 않았다.
- 사용자 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day08`.
- 안내 명령(아직 실행 결과 없음):

```bash
cd /home/user/onprem-lab/day08
pwd
ls -la
sha256sum compose.yaml
sed -n '1,28p' compose.yaml
docker version
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker image ls mitmproxy/mitmproxy:11.0.0
ss -ltn '( sport = :8081 or sport = :8082 )'
openssl version
```

- 목적: 파일 일치 여부, Docker 연결, 기존 자원, UI 포트, 사용할 이미지와 openssl 확인.
- Ubuntu 명령 실행·파일 동기화·컨테이너 기동·CA 생성은 Codex가 수행하지 않았으며 사용자 결과를 기다린다.

## 오류와 해결
### 2026-10-01 — Ubuntu 설정 검증 확인 및 프록시 기동 안내
- 사용자 Ubuntu 출력으로 `docker compose -p day08 config -q` 성공과 `Compose 설정 검사 통과`를 확인했다. 설정 앞부분에서 web_password 제거·127.0.0.1:8082:8081 게시를 확인했다.
- Ubuntu SHA-256 `544ce577e4f07bde13a6944377961606efea87d10d8990b8ae1532e134a9cbc9`가 수정한 Windows 사본과 일치한다. 자동 동기화가 아니라 각각 수정한 두 파일의 해시 비교 결과다.
- cp -n은 비이식성·향후 동작 변경 경고를 반환했다. 백업 파일 존재·내용은 별도 출력으로 확인하지 않았으며 백업 검증 완료로 처리하지 않는다. Compose 검증 성공은 서비스 실행 성공과 구분한다.
- 다음 명령을 Ubuntu `/home/user/onprem-lab/day08`에서 실행하도록 안내했다. 아직 기동·CA 생성 결과는 받지 않았다.

```bash
mkdir -p certs
docker compose -p day08 up -d --pull never --no-build tls-proxy
```

- 기동 성공 후 5~10초 기다리고 아래를 실행하도록 안내한다. 기동 오류가 나면 오류 출력부터 받는다.

```bash
docker compose -p day08 ps -a
ls -l certs/
openssl x509 -in certs/mitmproxy-ca-cert.pem -noout -subject -issuer -dates
```

- 목표는 tls-proxy 단독 기동과 CA 인증서 메타데이터 확인이다. agent 서비스 기동·이미지 빌드·8-2 통신 시험은 포함하지 않는다. 개인 키 파일 내용은 요청·기록하지 않는다.

### 2026-10-01 — Docker Desktop 실행 후 복구 확인 및 설정 조정 안내
- 사용자가 Docker Desktop을 실행하지 않았음을 확인하고 실행했다고 알렸다. 후속 Ubuntu 출력으로 Client/Engine 29.8.0, API 1.56, Desktop 4.92.0(240144), default context를 확인했다. Desktop 실행 후 Docker 사용이 복구됐으며 별도 연동 설정 변경은 보고되지 않았다.
- 사용자 docker ps -a 출력의 기존 컨테이너 8개는 모두 Exited다. pub2의 게시 설정은 0.0.0.0:8081→80이지만 현재 실행 중이지 않으므로 현재 포트 점유로 판정하지 않는다. web·web2·pub2의 exit=255 원인은 미확정이다. 기존 자원은 변경하지 않았다.
- mitmproxy/mitmproxy:11.0.0 이미지 ID ba52f9c5c5e3, 디스크 사용량 399MB·content size 106MB를 확인했다. ss는 헤더만 반환했다. Docker 시작 후 Ubuntu 8081·8082 리스너 부재를 관찰했지만 Windows 전체 포트 가용성 보장은 아니다.
- Day 7에서 확인한 버전별 옵션 차이를 반영해 web_password=lab을 제거하고, pub2 재기동 시 충돌을 피하도록 호스트 UI 포트를 8082로 변경한다. 컨테이너 내부 웹 포트 8081 및 프록시 포트 8080은 유지한다.
- Codex는 Windows day08/compose.yaml의 두 항목만 수정했다. Ubuntu 사본에는 사용자가 아래 명령을 실행하도록 안내했다. 아직 Ubuntu 수정·구성 검증 결과는 받지 않았다.

```bash
cp -n compose.yaml compose.yaml.before-8-1
sed -i 's/ --set web_password=lab//; s/127.0.0.1:8081:8081/127.0.0.1:8082:8081/' compose.yaml
docker compose -p day08 config -q && echo 'Compose 설정 검사 통과'
sed -n '1,16p' compose.yaml
sha256sum compose.yaml
```

- 프록시 기동과 CA 생성은 아직 미진행이다. 구성 검증 후 tls-proxy만 기동한다.

### 2026-10-01 — 사용자 사전 점검 출력 확인
- 실행 위치: 사용자 Ubuntu `/home/user/onprem-lab/day08`. 앞서 안내한 사전 점검 명령의 출력이다. Codex 직접 Ubuntu 검증이 아니다.
- compose.yaml SHA-256이 Windows 사본의 `3ce23a8732febb08b91acc12d0b253fdd7d98ef0b760b26d5173fdc5b68793bf`와 일치한다. 파일 앞부분에서 web_password=lab·8081 게시도 확인했다. 디렉터리 목록에는 certs/가 없다.
- docker version·docker ps·docker image ls 모두 `The command 'docker' could not be found in this WSL 2 distro` 및 WSL Integration 활성화 안내를 반환했다. Docker Desktop 미실행인지 연동 설정 문제인지는 아직 확정하지 않았다. 컨테이너·이미지 상태는 확인하지 못했다.
- ss 결과는 헤더만 표시됐다. 당시 Ubuntu에서 8081·8082 TCP 리스너를 찾지 못한 결과이며 Windows 호스트 포트 사용 여부나 Docker 시작 후 포트 가용성을 보장하지 않는다.
- OpenSSL 3.0.13 (30 Jan 2024)을 확인했다.
- 다음 안내: Windows 시작 메뉴에서 Docker Desktop을 열고 엔진 준비 후 Ubuntu에서 `docker version`을 재실행한다. 같은 오류가 계속되면 Settings > Resources > WSL Integration의 Ubuntu 활성화 여부를 확인한다. [Docker 공식 문서](https://docs.docker.com/desktop/features/wsl/).
- 복구 결과 대기. 실습 설정 변경·컨테이너 기동·CA 생성은 아직 하지 않았다.

## 배운 내용과 질문
### 2026-10-01 — Docker 재조회도 동일 오류
- 사용자 Ubuntu에서 `docker version` 재실행 결과도 동일한 WSL Integration 안내 오류였다. Docker Desktop 실행 상태나 설정 화면은 아직 제공되지 않아 원인은 확정하지 않았다.
- 다음 단계는 Windows Docker Desktop의 실행 상태와 Settings > Resources > WSL Integration에서 Ubuntu 활성화 여부를 직접 확인하는 것이다. 변경했다면 Apply 또는 Apply & restart 후 Ubuntu에서 `docker version`을 재확인하도록 안내한다.
- Ubuntu 연동 항목이 없거나 이미 활성화돼 있다면 현재 화면의 상태·문구를 받아 후속 진단한다. 재설치·WSL 종료·실습 기동은 안내하거나 실행하지 않았다.

앞선 대화에서 CA·CA 인증서·신뢰 저장소의 차이와 TLS 검사 프록시가 제시하는 인증서를 신뢰하는 원리를 설명했고 사용자가 이해했다고 답했다. 별도 독립 평가는 하지 않았다.

## 가이드와 실제 환경의 차이
공통 환경은 [환경 기록](../docs/environment.md)을 참고한다.

### 2026-10-01 — 8-1 기동·CA 생성 확인 및 절 완료
- 사용자 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab/day08`. 앞서 안내한 mkdir·Compose up·ps·ls·openssl 명령의 출력을 제공했다.
- 사용자 출력으로 day08_closed·day08_outside 생성, day08-tls-proxy-1 Started 및 후속 Up 4 seconds를 확인했다. 이미지 mitmproxy/mitmproxy:11.0.0, UI 게시 127.0.0.1:8082→8081/tcp다. agent 등 다른 Day 8 서비스는 기동하지 않았다.
- certs/에 파일 6개가 생성됐고, mitmproxy-ca-cert.pem의 subject·issuer는 모두 CN=mitmproxy, O=mitmproxy다. notBefore=2026-09-29 13:29:25 GMT, notAfter=2036-09-28 13:29:25 GMT를 확인했다. 파일 목록의 시각은 사용자 출력 그대로 보존하며 터미널 시간대는 별도 검증하지 않았다.
- [사용자 실행 증거](evidence/81-startup-user-2026-10-01.txt)에 기동·파일 목록·인증서 메타데이터를 보존했다. 인증서 원본이나 개인 키는 Windows로 복사하거나 저장소에 추가하지 않았다.
- 8-1 목표인 프록시 기동과 실습용 CA 생성·정보 확인 완료. HTTPS 실패·복구, 웹 화면 접속·복호화 관찰, 네트워크 실제 소속·internal 속성 직접 inspect는 이번 출력으로 검증하지 않았다. Day 8 전체 완료와 구분한다.
- 클라이언트 신뢰 등록에 사용할 공개 인증서는 mitmproxy-ca-cert.pem이다. mitmproxy-ca.pem은 CA 개인 키를 포함하므로 클라이언트에 전달할 인증서 파일과 구분한다.
- 실제 고객사에서는 TLS 검사 여부, 루트 CA 인증서(PEM), 검사 예외 도메인, CA 갱신 주기를 확인한다는 8-1 협의 항목을 설명한다. 고객사 요청·정책 변경은 수행하지 않았다.
- 현재 프록시·네트워크·certs를 유지한다. 8-2는 사용자 요청 후 CA 미신뢰 실패와 두 해결 방식 비교로 이어 간다.

## 다음에 이어 할 지점
Day 8의 8-1~8-4 실습·종료 정리·체크포인트 6문항 해설 완료. 사용자 독립 답변 평가는 미실시다. CA와 agent:0.2.0-ca 이미지는 Ubuntu에 보존돼 있다. PR #10은 사용자가 main에 병합했고 Windows main 갱신을 확인했다. 다음 학습은 사용자 요청 후 Day 9이며 자동 시작하지 않는다.

### 2026-10-01 — 8-2 시작·CA 미신뢰 실패 재현 안내
- 사용자 요청: "8-2를 진행하자". PROGRESS·환경·Day 8 기록·가이드 8-2·Compose·agent Dockerfile.ca 및 앱의 urllib 기반 egress 구현을 Windows에서 확인했다.
- 학습 순서: 가이드는 CA 병합 이미지 선행 빌드 후 세 경우를 비교하지만, 이번에는 원본 agent의 실패를 먼저 관찰하고 해결 1·2를 차례로 진행한다. 해당 절의 목표는 동일하다.
- 사용자 실행 위치: Ubuntu `/home/user/onprem-lab/day08`. 아래 명령은 안내만 했으며 실행 결과는 아직 없다.

```bash
cd /home/user/onprem-lab/day08
docker compose -p day08 up -d --pull never --no-build tls-proxy agent probe
```

- 기동 성공 후 약 5초 기다리고 다음을 실행하도록 안내한다. 기동 오류가 나면 멈추고 오류를 공유한다.

```bash
docker compose -p day08 ps -a
docker compose -p day08 exec -T probe curl --noproxy '*' -fsS -m 10 http://agent:8000/healthz
docker compose -p day08 exec -T probe curl --noproxy '*' -fsS -m 20 'http://agent:8000/egress?url=https://example.com' | jq '{ok,status,error_type,error}'
```

- healthz 정상은 agent의 HTTP 서비스 응답을 확인한다. egress는 probe→agent의 내부 HTTP 요청을 받아 agent가 TLS 프록시를 통해 example.com에 HTTPS로 접속하는 시험이다. 예상은 ok=false·SSLCertVerificationError이며 실제 원인 판정은 사용자 출력을 확인한 뒤 한다.
- agent-envca·agent-ca 기동, CA 병합 빌드 및 8-3 진단은 이번 첫 단계에서 수행하지 않는다. Codex는 Ubuntu를 직접 실행하지 않았다.

### 2026-10-01 — CA 미신뢰 실패 확인·해결 1 안내
- 사용자 출력으로 tls-proxy Running 유지 및 agent·probe Started를 확인했다. ps의 agent 상태는 Up 4 seconds (health: starting)이며 Docker healthcheck의 healthy 판정은 아직 확인하지 않았다.
- 직접 healthz 요청은 status=ok·version=0.2.0·host=66d155a02586. egress는 ok=false·SSLCertVerificationError·unable to get local issuer certificate다. jq에 표시된 status=null은 외부 HTTP 상태를 얻지 못한 경우이며 내부 agent API 미응답과 다르다.
- [실패 재현 증거](evidence/82-no-ca-user-2026-10-01.txt)에 사용자 출력을 보존했다. 알려진 CA 미등록 구성에서 예상한 오류를 확인했으며 오류 문자열만으로 모든 환경의 원인을 사내 CA로 단정하지 않는다.
- 다음 단계: 같은 agent:0.2.0 이미지에 certs를 읽기 전용으로 마운트하고 SSL_CERT_FILE·REQUESTS_CA_BUNDLE을 /certs/mitmproxy-ca-cert.pem으로 지정한 기존 Compose 서비스 agent-envca를 기동한다. 이번 앱은 urllib 기반이므로 실제 시험하는 CA 설정은 SSL_CERT_FILE이다. requests 라이브러리 동작은 시험하지 않는다.
- 아래 명령은 Ubuntu에서 사용자 실행을 안내했으며 결과는 아직 없다. 기동 성공 후 약 5초 기다리고 조회한다. 오류 시 기동 단계에서 멈춘다.

```bash
docker compose -p day08 up -d --pull never --no-build agent-envca
docker compose -p day08 ps -a
docker compose -p day08 exec -T probe curl --noproxy '*' -fsS -m 10 http://agent-envca:8000/healthz
docker compose -p day08 exec -T probe curl --noproxy '*' -fsS -m 10 http://agent-envca:8000/diag | jq '{ca}'
docker compose -p day08 exec -T probe curl --noproxy '*' -fsS -m 20 'http://agent-envca:8000/egress?url=https://example.com' | jq '{ok,status,error_type,error}'
```

- 예상은 ok=true·status=200이나 실제 사용자 결과를 확인하기 전 성공으로 기록하지 않는다. CA 병합 이미지 빌드와 8-3은 미진행이다.

### 2026-10-01 — CA 파일 지정 성공·이미지 병합 준비
- 사용자 출력으로 agent-envca Started, healthz status=ok·version=0.2.0·host=cb3d0488358f를 확인했다. ps의 원본 agent는 healthy, agent-envca는 health: starting이며 두 상태를 구분한다. 프록시·probe 포함 네 컨테이너를 유지한다.
- diag.ca에서 SSL_CERT_FILE·REQUESTS_CA_BUNDLE=/certs/mitmproxy-ca-cert.pem, CURL_CA_BUNDLE=(unset)을 확인했다. egress는 ok=true·status=200·error_type=null·error=null이다. [해결 1 증거](evidence/82-envca-user-2026-10-01.txt).
- 같은 이미지에서 CA 파일 지정으로 urllib 기반 HTTPS 요청이 성공했다. requests·curl의 CA 설정 동작, 검사 예외 경로·공인 CA 유지 여부는 시험하지 않았다. CA 파일 지정 방식이 성공했다고 OS 저장소에 CA가 병합됐다고 해석하지 않는다.
- 다음 단계는 CA를 이미지에 병합하는 해결 2다. Windows Dockerfile.ca SHA-256은 16414be114c4319b222f37fe6a0d539cbc866779b104696afa447281c1b51a36이다. Ubuntu 파일 일치와 기존 corp-ca.crt 유무를 먼저 확인한다. 해당 Dockerfile은 아직 수정하지 않았다.
- 안내 명령(사용자 Ubuntu day08, 결과 대기):

```bash
sha256sum ../agent/Dockerfile.ca
sed -n '1,16p' ../agent/Dockerfile.ca
docker compose -p day08 exec -T agent sh -c 'command -v update-ca-certificates; test -s /etc/ssl/certs/ca-certificates.crt && echo "CA bundle present"'
if [ -e ../agent/corp-ca.crt ]; then ls -l ../agent/corp-ca.crt; else echo 'corp-ca.crt 없음'; fi
```

- 목적: 두 사본의 Dockerfile 비교, 베이스 이미지의 CA 갱신 도구·기존 번들 확인, 기존 CA 파일 덮어쓰기 방지. 파일 복사·이미지 빌드·agent-ca 기동은 아직 미진행이다.

### 2026-10-01 — 빌드 사전 점검 확인·CA 병합 빌드 안내
- 사용자 Ubuntu Dockerfile.ca SHA-256이 Windows 원본 16414be114c4319b222f37fe6a0d539cbc866779b104696afa447281c1b51a36과 일치했다. 앞부분 내용도 동일하다.
- 원본 agent 컨테이너에서 /usr/sbin/update-ca-certificates와 비어 있지 않은 기존 /etc/ssl/certs/ca-certificates.crt를 확인했다. ../agent/corp-ca.crt는 없다는 사용자 출력을 받았다.
- 확인한 agent:0.2.0 베이스에 CA 도구·번들이 있으므로 apt-get update/install/목록 정리 세 줄을 RUN update-ca-certificates로 간소화한다. 다른 베이스 이미지에 도구가 없다면 이 Dockerfile을 그대로 적용할 수 없다는 전제다.
- Codex는 Windows agent/Dockerfile.ca에 위 변경을 반영했다. Ubuntu에는 다음 명령을 안내했으며 아직 수정·빌드 결과는 받지 않았다. 기존 가이드 원문·archives는 보존한다.

```bash
sed -i '/^RUN apt-get update /,+2c\RUN update-ca-certificates' ../agent/Dockerfile.ca
sha256sum ../agent/Dockerfile.ca
cp certs/mitmproxy-ca-cert.pem ../agent/corp-ca.crt
docker build --builder default --network=none \
  -f ../agent/Dockerfile.ca \
  --build-arg BASE_IMAGE=agent:0.2.0 \
  -t agent:0.2.0-ca ../agent
```

- 오류 시 중단하고 출력을 공유하도록 안내한다. default 빌더는 Day 7의 별도 desktop-linux 조회 오류를 피하기 위해 명시한다. --network=none은 빌드 RUN 단계의 네트워크를 비활성화한다.
- 공개 CA 인증서만 빌드 컨텍스트에 복사한다. CA 개인 키 파일은 사용하지 않는다. 임시 corp-ca.crt는 빌드 성공 확인 후 제거할 예정이며 8-1의 certs 원본은 유지한다. 새 이미지 기동·8-2 완료는 아직 미확인이다.

### 2026-10-01 — CA 병합 이미지 빌드 확인·새 이미지 시험 안내
- 사용자 출력으로 Ubuntu Dockerfile.ca 수정 후 SHA-256 0e0e31fe4b131800d944a924cf80d143d3312a9dadc34f8dbb7121e32d54cb78이 Windows 사본과 일치함을 확인했다.
- default 빌더의 8/8 FINISHED, 공개 CA COPY 및 RUN update-ca-certificates 성공, agent:0.2.0-ca 태그 생성·unpacking을 확인했다. --network=none은 RUN 네트워크 제한이며 빌드 전체의 모든 외부 통신 부재를 별도 검증한 것은 아니다. [빌드 증거](evidence/82-ca-build-user-2026-10-01.txt).
- 다음 사용자 명령은 Ubuntu day08에서 빌드 컨텍스트의 임시 공개 CA 사본만 제거하고 새 이미지를 기동한다. certs/ 원본은 유지한다. 제거·기동 결과는 아직 받지 않았다.

```bash
rm -- ../agent/corp-ca.crt
test ! -e ../agent/corp-ca.crt && echo '임시 CA 파일 정리 완료'
docker compose -p day08 up -d --pull never --no-build agent-ca
```

- 기동 성공 후 약 5초 기다리고 아래를 실행하도록 안내한다. 오류가 나면 해당 단계에서 멈추고 출력을 공유한다.

```bash
docker compose -p day08 ps -a
docker compose -p day08 exec -T probe curl --noproxy '*' -fsS -m 10 http://agent-ca:8000/healthz
docker compose -p day08 exec -T probe curl --noproxy '*' -fsS -m 10 http://agent-ca:8000/diag | jq '{uid,gid,ca}'
docker compose -p day08 exec -T probe curl --noproxy '*' -fsS -m 20 'http://agent-ca:8000/egress?url=https://example.com' | jq '{ok,status,error_type,error}'
```

- 기대 결과는 healthz 정상·uid=10001·CA 경로 /etc/ssl/certs/ca-certificates.crt·HTTPS HTTP 200이다. 실제 사용자 결과 전에는 통신 성공·8-2 완료로 기록하지 않는다. 8-3 인증서 진단은 미진행이다.

### 2026-10-01 — CA 병합 이미지 HTTPS 성공·8-2 완료
- 사용자 Ubuntu 출력으로 임시 ../agent/corp-ca.crt 제거 후 부재 확인 메시지를 받았다. certs 원본·이미지 내부 인증서를 제거한 것은 아니다.
- agent-ca Started와 후속 ps의 healthy, healthz status=ok·version=0.2.0·host=9654322c6bc3을 확인했다. agent·agent-envca도 이번 ps에서 healthy이며 probe·tls-proxy는 Up이다. 총 컨테이너 5개를 유지한다.
- agent-ca의 uid=10001·gid=0, SSL_CERT_FILE·REQUESTS_CA_BUNDLE·CURL_CA_BUNDLE 모두 /etc/ssl/certs/ca-certificates.crt를 확인했다. example.com HTTPS egress는 ok=true·status=200·error_type=null·error=null이다. [성공·정리 증거](evidence/82-ca-success-user-2026-10-01.txt).
- 8-2 완료: 원본 agent에서 인증서 검증 실패, 같은 이미지의 agent-envca에서 CA 파일 지정으로 200, 새 agent:0.2.0-ca 이미지의 agent-ca에서 병합 번들 지정으로 200을 각각 관찰했다. 결과는 순차 시험이며 마지막 시점에 세 외부 요청을 동시에 재시험한 것은 아니다.
- 실제 앱의 urllib 기반 HTTPS 성공을 확인했다. requests·curl 라이브러리의 개별 CA 동작, 공인 CA를 사용하는 검사 예외 목적지, 번들 내 특정 CA 검색·인증서 개수 비교는 별도 시험하지 않았다. 8-3·8-4와 독립 자기점검은 미진행이다.
- 학습 의미: CA 파일 지정과 이미지 내 병합 두 방식 모두 이번 검사 경로에서 성공했다. 병합 방식은 기존 공인 CA와 실습용 CA를 함께 담는 번들을 사용한다. 앱 healthcheck 정상과 외부 HTTPS 신뢰 성공은 별개이며 원본 agent도 healthy로 표시된다.
- 기록은 Windows에 반영했다. 컨테이너 5개·네트워크 2개·certs·원본 및 CA 이미지·기존 백업은 유지한다. Ubuntu 전체 동기화·커밋·push·Day 8 종료 정리는 수행하지 않았다.

### 2026-10-01 — 8-3 시작·프록시 경유 인증서 조회 안내
- 사용자 요청: "8-3으로 가자". 진행·환경·Day 8 기록·가이드 8-3·Compose를 확인했다. 현재 작업 범위는 8-3이며 8-4는 미포함이다.
- 가이드의 openssl s_client 진단에 SNI와 호스트 이름 검증 대상을 명시하고, timeout 15로 실행 시간을 제한했다. 검증 오류를 포함한 핵심 줄만 표시하며 세션 키 등 전체 출력은 요청하지 않는다.
- 안내 명령(사용자 Ubuntu day08, 아직 결과 없음):

```bash
cd /home/user/onprem-lab/day08
docker compose -p day08 ps -a
docker compose -p day08 exec -T probe sh -c '
  timeout 15 openssl s_client -connect example.com:443 -proxy tls-proxy:8080 -servername example.com -verify_hostname example.com </dev/null 2>&1 |
  grep -E "subject=|issuer=|Verify return code|verify error|error:|errno="
'
```

- probe는 실습 CA를 신뢰하도록 설정하지 않은 상태다. subject는 접속 대상 인증서의 주체, issuer는 발급자, Verify return code는 probe의 검증 결과로 해석한다. 예상 발급자는 mitmproxy이고 검증 오류가 예상되지만 코드 값은 실제 출력을 확인한다.
- s_client는 진단 도구로 기본적으로 인증서 검증 오류 후에도 진행할 수 있다. 연결·명령 종료만으로 검증 성공을 판단하지 않는다. [OpenSSL 공식 문서](https://docs.openssl.org/3.0/man1/openssl-s_client/). 별도 인증서 설치·설정 변경·8-3 완료 판정은 아직 없다.

### 2026-10-01 — 발급자·검증 오류 확인 및 CA 번들 비교 안내
- 사용자 Ubuntu ps 출력에서 세 agent healthy·probe 및 tls-proxy Up을 재확인했다. 프록시 경유 인증서는 subject=CN=example.com, issuer=CN=mitmproxy,O=mitmproxy다. probe의 검증 오류 20·21과 최종 Verify return code 21을 확인했다. [진단 증거](evidence/83-issuer-user-2026-10-01.txt).
- 알려진 실습 경로에서 프록시 CA가 발급한 목적지 인증서를 관찰한 결과다. 인증서 주체는 example.com이고 발급자는 mitmproxy임을 구분한다. 사내·공인 CA 이름만으로 모든 환경의 검사 여부를 단정하지 않는다.
- 다음 단계는 원본·병합 이미지의 실제 인증서 개수와 특정 CA 존재 확인이다. 가이드 예시 150·151을 고정 기대값으로 삼지 않는다. 특정 CA 조회에는 이미지의 Python 표준 ssl을 사용해 openssl 실행 파일 추가 설치 없이 지정한 번들만 읽는다.
- 다음은 사용자 Ubuntu day08 실행 안내이며 아직 결과는 없다.

```bash
docker compose -p day08 exec -T agent grep -c 'BEGIN CERTIFICATE' /etc/ssl/certs/ca-certificates.crt
docker compose -p day08 exec -T agent-ca grep -c 'BEGIN CERTIFICATE' /etc/ssl/certs/ca-certificates.crt
docker compose -p day08 exec -T agent-ca python - <<'PY'
import ssl
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.load_verify_locations(cafile='/etc/ssl/certs/ca-certificates.crt')
matches = []
for cert in ctx.get_ca_certs():
    subject = dict(item for rdn in cert['subject'] for item in rdn)
    if subject.get('commonName') == 'mitmproxy':
        matches.append(subject)
print('mitmproxy CA 개수:', len(matches))
for subject in matches:
    print(subject)
PY
```

- 설정 변경 없이 번들 내용을 읽는 명령이다. 개수 차이만으로 특정 CA 추가나 기존 모든 인증서 보존을 증명한다고 해석하지 않는다. 이름 조회는 CA 존재 확인이며 원본 공개 CA와의 지문 비교는 아직 하지 않았다.

### 2026-10-01 — CA 번들 비교 확인·curl 비교 안내
- 사용자 Ubuntu 출력으로 원본 agent의 PEM 인증서 개수 150, agent-ca의 개수 151을 확인했다. agent-ca의 해당 번들만 읽은 Python ssl 조회에서 commonName=mitmproxy·organizationName=mitmproxy인 CA 1개를 확인했다. [번들 증거](evidence/83-bundle-user-2026-10-01.txt).
- CA 병합 구성·빌드와 일치하는 결과다. 기존 150개 각각의 동일성 또는 실습 CA 원본과의 지문 비교까지 수행한 것은 아니다.
- 다음 명령은 사용자 Ubuntu day08에서 공개 CA를 probe의 임시 경로에 복사하고 같은 curl에서 --cacert 유무만 바꾸어 비교하는 단계다. OS 신뢰 저장소는 변경하지 않는다. 아래 명령은 아직 사용자 실행 결과를 받지 않았다.

```bash
docker compose -p day08 cp certs/mitmproxy-ca-cert.pem probe:/tmp/day08-corp-ca.pem
docker compose -p day08 exec -T probe curl --noproxy '' -sS -m 20 \
  -x http://tls-proxy:8080 -o /dev/null \
  -w 'CA 지정 전: HTTP=%{http_code}, exit=%{exitcode}\n' https://example.com
docker compose -p day08 exec -T probe curl --noproxy '' -sS -m 20 \
  -x http://tls-proxy:8080 --cacert /tmp/day08-corp-ca.pem -o /dev/null \
  -w 'CA 지정 후: HTTP=%{http_code}, exit=%{exitcode}\n' https://example.com
```

- 복사 오류가 나면 중단한다. 첫 curl의 인증서 오류는 예상된 비교 결과이며 다음 curl도 실행하도록 안내한다. --noproxy 빈 값은 이번 curl의 프록시 우회 목록을 비운다. -sS로 오류를 표시하고 HTTP와 curl 종료 코드를 구분한다.
- 기대값은 지정 전 HTTP=000·exit=60, 지정 후 HTTP=200·exit=0이다. 실제 결과 확인 전에는 8-3 완료로 처리하지 않는다. 복사된 공개 CA는 probe 내부 임시 파일로 남으며 원본 certs와 별개다.

### 2026-10-01 — curl 비교 확인 및 8-3 완료
- 사용자 Ubuntu 출력으로 공개 CA를 probe:/tmp/day08-corp-ca.pem에 복사한 결과를 확인했다. CA 개인 키를 복사한 것은 아니다.
- 동일한 probe·프록시·목적지에서 CA 미지정 curl은 SSL certificate problem: unable to get local issuer certificate, HTTP=000·exit=60이었다. --cacert 지정 후 HTTP=200·exit=0이었다. [curl 비교 증거](evidence/83-curl-user-2026-10-01.txt).
- 8-3 완료 범위: 프록시 경유 인증서 subject=example.com·issuer=mitmproxy와 probe 검증 코드 21 확인, 원본·병합 번들 150·151개 비교, 병합 번들의 mitmproxy CA 1개 조회, curl CA 지정 전후 실패·성공 비교.
- 의미: 네트워크 경로가 같은 조건에서 신뢰에 사용할 CA를 명시하자 검증을 유지한 HTTPS 요청이 성공했다. --cacert는 해당 curl 요청에 적용되며 probe의 OS 신뢰 저장소에 CA를 영구 등록한 것은 아니다.
- 현재 컨테이너 5개·네트워크 2개·certs·이미지와 probe의 임시 공개 CA 사본은 유지한다. Windows 기록만 갱신했으며 Ubuntu 자원 정리·동기화·8-4 시작·Git 커밋 또는 push는 수행하지 않았다. 별도 자기점검 평가는 미진행이다.

### 2026-10-01 — 8-4 시작·HTTPS 화면 관찰 안내
- 사용자 요청: "8-4로 가자". 최신 진행·환경·Day 8 기록, 가이드 8-4, 현재 Compose와 Day 7 웹 접속 기록을 확인했다.
- 가이드의 8081·token=lab 예시 대신 현재 mitmproxy 11.0.0 구성에 맞는 http://localhost:8082/를 Windows 브라우저에서 열도록 안내한다. 브라우저는 프록시 관리 화면을 여는 용도이며 브라우저의 프록시·신뢰 저장소를 변경하지 않는다.
- 웹 화면을 연 뒤 Ubuntu `/home/user/onprem-lab/day08`에서 아래 명령으로 agent-ca의 HTTPS 요청을 한 번 더 만들도록 안내한다. 아직 해당 요청 실행·응답 결과는 받지 않았다.

```bash
docker compose -p day08 exec -T probe curl --noproxy '*' -fsS -m 20 \
  'http://agent-ca:8000/egress?url=https://example.com' | jq '{ok,status,error_type,error}'
```

- 관찰 안내: 최신 example.com 요청을 선택하고 Request에서 https://example.com/·GET·User-Agent 등 헤더를, Response에서 HTTP 200·Content-Type 및 Example Domain HTML 본문을 확인한다. 기존 요청과 혼동하지 않도록 새 요청을 생성한다.
- 사용자에게 터미널 출력과 Request/Response의 관찰 내용을 공유하도록 요청한다. UI 접속 오류 시 표시 문구부터 확인하며 성공을 가정하지 않는다. 인증서 검증 성공과 웹 화면에서 본문을 실제로 본 결과를 구분한다.
- Day 7에서 직접 관찰한 것은 HTTP였고 이번 대상은 HTTPS다. 일반 CONNECT 터널과 TLS 검사 프록시를 구분해 설명한다. 이번 공개 예제 본문 관찰이 실제 LLM 프롬프트 전송이나 고객사 로그 저장 정책 검증을 뜻하지 않는다.
- Codex는 Ubuntu 요청·브라우저 조작을 대신 수행하지 않았다. 8-4 완료·자원 정리·Day 9 진행은 아직 없다.

### 2026-10-01 — 8-4 새 HTTPS 요청 성공·웹 화면 결과 대기
- 사용자가 Ubuntu day08에서 안내한 probe→agent-ca egress 명령을 실행하고 결과를 제공했다.
- 응답 원문: {"ok":true,"status":200,"error_type":null,"error":null}.
- 새 HTTPS 요청의 성공을 확인했다. 사용자는 아직 mitmweb 화면이나 Request/Response 내용을 제공하지 않았으므로 웹 UI 접속·HTTPS 본문 관찰·8-4 완료로 처리하지 않는다.
- 다음 안내: Windows http://localhost:8082/의 최신 example.com 요청을 선택하고 Request의 https 주소·GET·헤더, Response의 200·헤더·Example Domain HTML 본문을 확인해 공유한다. Codex 직접 브라우저 관찰은 하지 않았다.

### 2026-10-01 — Response 탭의 상태·헤더·본문 확인
- 사용자가 mitmweb Response 탭 내용을 텍스트로 제공했다. HTTP/1.1 200 OK, Content-Type=text/html; charset=utf-8, Date=Thu, 01 Oct 2026 14:12:11 GMT, Server=cloudflare 등 응답 헤더를 확인했다.
- HTML에는 title=Example Domain과 문서 예제용 도메인 설명·IANA 링크가 있다. [관찰 증거](evidence/84-https-observation-user-2026-10-01.txt)에 핵심 내용을 보존했다. HTML 본문의 링크·스크립트를 Codex가 방문하거나 실행하지 않았다.
- 의미: CLI의 200뿐 아니라 mitmweb에서 응답 헤더와 읽을 수 있는 HTML 본문을 관찰했다. 다만 같은 flow의 Request 주소·헤더는 아직 제공되지 않아 마지막으로 Request 탭의 https://example.com/·GET·User-Agent를 확인하도록 안내한다.
- UI의 http://localhost:8082는 관리 화면 주소이고, 관찰 대상 HTTPS 주소와 구분한다. 사용자 제공 텍스트를 확인한 것이며 Codex 직접 화면 검증은 아니다. 8-4 최종 완료와 정리는 아직 보류한다.

### 2026-10-01 — Request 탭 확인 및 8-4 완료
- 사용자가 같은 요청의 Request 탭 텍스트를 제공했다. GET https://example.com/ HTTP/1.1, Host=example.com, User-Agent=Python-urllib/3.12, Accept-Encoding=identity, Connection=close와 No content를 확인했다. [관찰 증거](evidence/84-https-observation-user-2026-10-01.txt)에 추가했다.
- HTTPS 주소와 Python urllib 사용자 에이전트는 앞선 agent-ca egress 명령 및 앱 구현과 일치한다. No content는 이 GET의 요청 본문이 없다는 뜻이며, 앞서 확인한 HTML 응답 본문과 구분한다.
- 8-4 완료: 사용자 제공 텍스트로 HTTPS 요청 주소·메서드·헤더, Response HTTP 200·응답 헤더·Example Domain HTML 본문 관찰을 확인했다. Codex가 브라우저를 직접 열거나 화면을 검증한 것은 아니다.
- 핵심 학습: 클라이언트↔프록시와 프록시↔원 서버의 TLS 연결 사이에서 검사 프록시는 내용을 읽을 수 있다. 이번에는 공개 예제 페이지의 GET·HTML 응답만 시험했다. LLM 프롬프트 원문도 TLS 검사 대상이 될 수 있다는 설계상 함의와 실제 저장·보관 여부는 구분하며, 이번에 프롬프트 전송이나 로그 영구 저장 정책은 시험하지 않았다.
- 8-1~8-4 실습을 마쳤지만 Day 전체 종료·자원 정리·별도 체크포인트 평가는 미진행이다. 컨테이너 5개·네트워크 2개·certs·이미지·probe 임시 공개 CA는 유지한다. 추가 실행·정리·Day 9 진행·Git 커밋·push는 하지 않았다.

### 2026-10-01 — 사용자 종료 정리 요청·실행 결과 대기
- 사용자 요청: "좋아 그러면 정리하자". 최신 기록 및 가이드의 Compose down·certs 보존 방침을 확인했다.
- 실행 위치: 사용자 Ubuntu WSL2 `/home/user/onprem-lab/day08`. 아래 명령은 안내만 했으며 Codex가 직접 실행하지 않았다.

```bash
cd /home/user/onprem-lab/day08 && docker compose -p day08 down
docker ps -a --filter label=com.docker.compose.project=day08 --format 'table {{.Names}}\t{{.Status}}'
docker network ls --filter label=com.docker.compose.project=day08
ls -l certs/mitmproxy-ca-cert.pem
docker image ls agent:0.2.0-ca
```

- 대상은 agent·agent-envca·agent-ca·probe·tls-proxy 컨테이너 5개와 closed·outside 네트워크 2개다. probe 내부 /tmp/day08-corp-ca.pem도 컨테이너 제거와 함께 사라진다. 파일 별도 삭제나 복구 불가능한 삭제를 뜻하지 않는다.
- certs 바인드 마운트 원본, 이미지·빌드 캐시·백업은 보존한다. -v·--rmi·전역 prune은 사용하지 않는다. 다른 Day와 koica 자원은 대상이 아니다.
- 기대 결과는 Day 8 자원 Removed 및 필터 목록에 헤더만 표시, 공개 CA 파일·agent:0.2.0-ca 이미지 존재다. 실제 사용자 출력 전에는 정리·종료 완료로 기록하지 않는다. 별도 체크포인트는 미진행으로 유지한다.

### 2026-10-01 — 종료 정리 확인 및 Day 8 종료
- 사용자 Ubuntu 출력으로 안내한 Compose down의 컨테이너 5개(agent·probe·agent-ca·agent-envca·tls-proxy)와 네트워크 2개(outside·closed) Removed를 확인했다. 후속 Day 8 프로젝트 필터 컨테이너·네트워크 목록은 헤더만 표시됐다.
- certs/mitmproxy-ca-cert.pem 존재(1172바이트), agent:0.2.0-ca 이미지 ID ebe1f3076bf2·DISK USAGE 182MB·CONTENT SIZE 44.3MB를 확인했다. [정리 증거](evidence/cleanup-user-2026-10-01.txt)에 사용자 출력을 보존했다.
- probe의 임시 공개 CA 사본은 제거된 컨테이너의 쓰기 계층에 있었다. certs 바인드 마운트 원본·이미지·빌드 캐시·백업은 삭제하지 않았다. certs 전체 파일 목록이나 원본 agent 이미지·다른 프로젝트 자원·8082 리스너는 이번 종료 출력에서 재조회하지 않았다.
- 종료 판정: 8-1~8-4 실습 및 지정 자원 정리 완료. 체크포인트 6문항 해설·독립 답변 평가는 미실시로 구분한다. 다음 Day를 자동 시작하지 않는다.
- Windows SESSION·PROGRESS·README·환경 기록을 종료 상태로 갱신했다. Ubuntu 명령은 사용자 실행이며 Codex 직접 실행·전체 동기화는 없다. Git 커밋·push·PR 생성·병합은 수행하지 않았다.

### 2026-10-01 — Day 8 복습·체크포인트 6문항 해설
- 사용자 요청으로 Day 8 학습 흐름과 6문항의 답변을 제공했다. 해설 제공이며 사용자 독립 답변 평가·통과로 처리하지 않는다. 새로운 Ubuntu 실행·자원 생성은 없다.
- 전체 흐름: mitmproxy로 TLS 검사 환경·CA 생성 → 원본 agent의 인증서 오류 → CA 파일 지정 및 CA 병합 이미지 각각 HTTPS 200 → issuer·CA 번들 150/151·curl 비교 → mitmweb HTTPS 헤더·본문 관찰 → 지정 자원 정리. 사용자 증거와 연결해 복습했다.
- 1번: 브라우저·OS·컨테이너·Python 라이브러리의 신뢰 저장소가 다를 수 있다. 회사가 브라우저에 배포한 CA가 컨테이너에 자동 반영되지 않는다. 이번 Linux urllib/ssl은 OpenSSL 기본 신뢰 경로를 사용하고 Requests는 일반적으로 certifi를 사용한다. 모든 Python 라이브러리가 동일한 저장소를 사용하는 것으로 설명하지 않는다. 이번 실습은 urllib이며 Requests 직접 시험은 없다.
- 2번: verify=False는 Requests의 서버 인증서 검증을 끄므로 호스트 이름 불일치·만료 등도 무시해 서버 사칭·중간자 공격에 취약해진다. 또한 CA 누락 등 원인을 해결하지 않은 채 우회 설정이 운영에 남을 수 있다. 암호화 자체가 반드시 사라진다는 뜻은 아니다. 검증을 유지하고 승인된 CA를 신뢰하도록 설정한다.
- 3번: SSL_CERT_FILE은 CA를 기존 파일에 자동 추가하는 설정이 아니라 사용할 CA 번들 파일 경로를 바꾼다. 사내 CA만 담긴 파일을 지정하면 공인 CA가 필요한 경로에서 실패할 수 있다. 라이브러리·다른 CA 디렉터리 참조에 따라 동작하므로 공인 CA가 무조건 전부 사라진다고 단정하지 않는다. 이번 권장 구성은 공인 CA와 사내 CA를 함께 담은 이미지 내 번들을 만들고 앱을 그 경로로 설정하는 방식이다. 마운트한 병합 번들도 가능하며 문제는 파일이 하나인 것이 아니라 필요한 신뢰 CA가 빠진 것이다. CA 교체 시 이미지 재빌드·배포가 필요하다.
- 4번: TLS 검사 여부 확인 후 보안팀에 루트 CA 공개 인증서(PEM, 필요한 경우 중간 인증서도), 검사 예외 도메인 목록, CA 갱신·교체 주기와 사전 통지 방법을 요청한다. CA 개인 키는 요청하지 않는다.
- 5번: 실제 프록시 경유 경로에서 s_client의 subject·issuer·체인을 확인한다. 이번에는 subject=example.com·issuer=mitmproxy가 알려진 검사 프록시 구성과 일치했고 verify code 21은 probe의 신뢰 실패를 나타냈다. 검증 실패 코드 자체는 TLS 검사 증거가 아니며 issuer 문자열만으로 모든 환경을 단정하지 않는다. 알려진 CA 정보·직접 경로와 비교하고, s_client 기본 동작은 검증 오류 후에도 진행할 수 있음을 구분한다.
- 6번: TLS가 클라이언트↔검사 프록시와 프록시↔원 서버 두 구간으로 나뉘므로 프록시는 LLM 프롬프트·응답·HTTP 인증 헤더를 읽을 수 있다. 저장 여부는 로그 정책에 달렸다. 고객사와 검사 대상/예외, 원문 저장·마스킹, 보관 기간·접근 권한을 협의한다. 실제 실습은 공개 HTML 관찰이며 LLM 프롬프트 전송·영구 저장은 시험하지 않았다.
- 공식 근거: [Python 3.12 ssl](https://docs.python.org/3.12/library/ssl.html), [Requests 인증서 검증·CA](https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification), [OpenSSL 기본 검증 경로](https://docs.openssl.org/3.0/man3/SSL_CTX_load_verify_locations/), [Docker CA 이미지 구성](https://docs.docker.com/engine/network/ca-certs/), [mitmproxy HTTPS 구조](https://docs.mitmproxy.org/stable/concepts/how-mitmproxy-works/), [s_client](https://docs.openssl.org/3.0/man1/openssl-s_client/).

### 2026-10-01 — main 대상 PR 생성 요청 및 준비
- 사용자 요청: GitHub에 main 대상 PR을 만들고 병합은 사용자가 수행한다.
- Codex 직접 확인: origin fetch 후 HEAD와 origin/main이 모두 b2dd34d240e734483681355481ffcba8b0d2be40이다. 열린 PR 목록은 비어 있었다. 현재 변경을 보존해 codex/day08-results 브랜치를 생성했다.
- 포함 범위: Day 8 SESSION·README·텍스트 증거 10개, PROGRESS·환경 기록, day08/compose.yaml의 web_password 제거·UI 포트 8082, agent/Dockerfile.ca의 이미 설치된 CA 도구 활용이다. Dockerfile은 CA 도구가 있는 검증된 agent:0.2.0을 전제로 한다.
- 검증: Windows 소스와 사용자 Ubuntu 수정 후 해시 일치, 사용자 출력으로 Compose config·이미지 빌드·HTTPS 비교·정리를 확인했다. Codex의 git diff --check는 통과했다. 실습 재실행·CA 개인 키 또는 인증서 원본 업로드는 없다.
- PR 대상은 main이며 자동 병합하지 않는다. 커밋·푸시·PR 생성 결과는 GitHub 이력에서 확인한다. Day 9는 이번 요청 범위에 포함하지 않는다.

### 2026-10-01 — PR #10 생성·사용자 병합 확인 및 Windows main 갱신
- 앞선 PR 생성 작업에서 Day 8 커밋 f2b5df96666b802e49bf4064cb6733166723d78d를 codex/day08-results에 push하고 [PR #10](https://github.com/shanis345/Deploy_Practice/pull/10)을 main 대상으로 생성했다. Codex는 병합하지 않았다.
- 사용자가 "완료했어"라고 알린 뒤 GitHub 직접 조회로 state=MERGED, base=main, merge commit=6801a098a0b4cd5b138e08aa707b7926a6f0c8bc를 확인했다. mergedAt=2026-10-01T14:58:34Z(Asia/Bangkok 21:58:34)다.
- Windows 작업 폴더가 깨끗한 상태에서 git fetch origin, git switch main, git merge --ff-only origin/main을 실행했다. HEAD와 origin/main 해시 일치 및 f2b5df9가 HEAD의 조상임을 확인했다.
- Ubuntu 사본은 갱신하지 않았고 실습을 재실행하지 않았다. 로컬·원격 브랜치는 삭제하지 않았다. Day 9도 시작하지 않았다.
- SESSION·PROGRESS에 병합 확인 메모를 추가했다. 이 두 기록 수정은 로컬 미커밋 상태이며 새 커밋·main 직접 push·추가 PR 생성은 수행하지 않았다.
