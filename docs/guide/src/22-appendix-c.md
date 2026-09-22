# 부록 C — 트러블슈팅 플레이북 (증상 → 원인)

증상에서 원인으로 가는 경로입니다. 첫 케이스에 프린트해서 들고 가세요. 각 행의 Day는 재현·해결 실습입니다.

## C-1. 컨테이너·Pod가 안 뜬다

| 증상 | 확인 | 원인과 조치 | Day |
|---|---|---|---|
| `ImagePullBackOff` / `ErrImagePull` | `describe pod` Events | 레지스트리 주소·태그 오타 / `imagePullSecrets` 누락 / 레지스트리 인증서(사내 CA) / **노드의 프록시 설정** / 노드 디스크 GC로 이미지 삭제 | 9, 10 |
| `CrashLoopBackOff` | `logs --previous` | 환경변수·설정 파일 누락, 권한(OpenShift UID), 포트 충돌, 실행 시 외부 다운로드 시도 | 10, 12 |
| `Pending` | `describe pod` Events | 자원 부족(requests 과다), ResourceQuota, nodeSelector 불일치, PVC 미바인딩 | 10 |
| `CreateContainerConfigError` | `describe pod` | ConfigMap/Secret 이름 오타 또는 미생성 | 11 |
| `Running` 이지만 `0/1` | probe 설정 | readiness 경로·포트 오류, 기동 시간 > `initialDelaySeconds` (모델 로딩은 startupProbe) | 10 |
| `OOMKilled` (Last State) | `describe pod` | `limits.memory` 초과. 상한 상향 또는 메모리 사용 조정 | 2, 10 |
| OpenShift에서만 기동 실패 | `logs` | 임의 UID로 인한 쓰기 권한. `chgrp -R 0` + `chmod -R g=u`, `HOME` 지정 | 12 |
| `permission denied` (포트) | 포트 번호 | non-root는 1024 미만 바인딩 불가(containerd/OpenShift). 8080 이상으로 | 12 |
| `exec format error` | 이미지 아키텍처 | 맥(arm64)에서 빌드한 이미지. `--platform linux/amd64`로 재빌드 | 9 |
| Compose 서비스가 `health: starting`에서 멈춤 | `docker compose logs` | 헬스체크 명령 오류, `start_period` 부족 | 5 |
| `Conflict. The container name is already in use` | `docker ps -a` | 이전 컨테이너 잔존. `docker rm -f` | 4 |
| `port is already allocated` | `ss -ltnp` | 호스트 포트 충돌. 다른 포트로 | 5 |

## C-2. 외부 연결이 안 된다

증상을 보고 분기합니다.

```text
"Temporary failure in name resolution" / gaierror   → 프록시 미설정(폐쇄망) 또는 DNS 차단. /diag 로 환경변수 확인.
                                                      NetworkPolicy egress에 DNS 규칙 누락 (k8s)
"Network is unreachable"                            → 프록시 미설정 (라우팅은 있고 default route 없음)
타임아웃 (아무 응답 없음)                              → 방화벽 미개방. nc -z <프록시> 3128
"403 Forbidden" (프록시 응답) / "Tunnel connection failed: 403" → 화이트리스트 미등록. 프록시 로그 TCP_DENIED
"407 Proxy Authentication Required"                 → 프록시 계정 필요. http://user:pass@proxy (특수문자 URL 인코딩)
"CERTIFICATE_VERIFY_FAILED" / "unable to get local issuer certificate" → 사내 CA 미설치
"self-signed certificate in certificate chain"      → 사내 CA 미설치 (검사 장비가 자체 서명 루트)
curl은 되는데 파이썬만 실패                            → certifi 번들. REQUESTS_CA_BUNDLE / SSL_CERT_FILE
파이썬은 되는데 curl만 실패                            → curl은 소문자 http_proxy만 읽음
HTTP는 되고 HTTPS만 실패                               → TLS 검사 + CA 문제
사내 API만 실패, 외부는 성공                           → NO_PROXY에 사내 주소 누락
DB는 되는데 내부 API만 실패                            → 위와 동일 (DB는 TCP 직결, API는 HTTP라 프록시를 탐)
어떤 사이트는 되고 어떤 사이트만 실패                   → 검사 예외 목록 + SSL_CERT_FILE로 번들 대체. 병합 번들로
간헐적 실패                                          → 프록시 이중화 중 한쪽만 화이트리스트 등록
되다가 어느 날부터 실패                                → 사내 CA 갱신, 프록시 정책 변경, 서비스 계정 만료
Node.js/Java만 실패                                  → 환경변수를 안 읽음. NODE_USE_ENV_PROXY / -Dhttp.proxyHost
docker build만 실패                                  → 빌드 시 프록시 별도 (--build-arg)
docker pull만 실패                                   → 데몬 프록시 설정 (daemon.json) 별도, 레지스트리 CA (/etc/docker/certs.d)
```

| 진단 명령 | 무엇을 알려주나 |
|---|---|
| `curl -s localhost:8000/diag` | 컨테이너가 실제로 받은 프록시·CA 환경변수 |
| `docker compose exec proxy tail /var/log/squid/access.log` | 허용(`TCP_TUNNEL`/`TCP_MISS`) vs 차단(`TCP_DENIED`) |
| `openssl s_client -proxy <p>:3128 -connect <h>:443` | issuer가 사내 CA인지 공인 CA인지 |
| `nc -zv <프록시> 3128` | 프록시까지 방화벽이 열렸는지 |

## C-3. 응답이 끊긴다 · 느리다

| 증상 | 원인 | 조치 | Day |
|---|---|---|---|
| 정확히 60초쯤에 502/504 | LB·Ingress·nginx 타임아웃 기본값 | `proxy_read_timeout 300s`, Ingress 어노테이션, **사내 LB·WAF도** | 5, 11 |
| 스트리밍이 끝에 한 번에 나옴 | 프록시 버퍼링 | `proxy_buffering off`, Ingress `proxy-buffering: "off"` | 5, 11 |
| 긴 요청만 실패 | 프록시·WAF 타임아웃 | 경로별 예외 요청 | 7, 11 |
| 응답은 오는데 매우 느림 | 프록시 + TLS 검사 오버헤드 | 정상. 예상 지연을 설계에 반영 | 8 |
| 일정 시간 후 연결 끊김 | 방화벽 idle timeout | keepalive, 재시도 로직 | 6 |
| 정상 Pod가 재시작됨 | liveness가 LLM 대기 중인 Pod를 죽임 | `/healthz`는 LLM과 무관하게 즉시 응답, `timeoutSeconds` 여유 | 10 |
| 살아 있는데 무응답 (Compose) | 데드락·대기 누적 | Compose는 자동 복구 없음. 재시작. 정식은 liveness probe | 5, 10 |

## C-4. 배포 후 동작이 다르다

| 증상 | 원인 | 조치 | Day |
|---|---|---|---|
| 로컬은 되는데 고객 환경만 실패 | 환경변수 차이 | `/diag` 출력을 양쪽에서 비교 | 0, 7 |
| 설정을 바꿨는데 반영 안 됨 | 환경변수는 재시작 필요 / ConfigMap `subPath` 마운트 | `rollout restart`, 디렉터리 마운트로 | 11 |
| `.env` 바꿨는데 반영 안 됨 | `restart`는 환경변수를 다시 안 읽음 | `docker compose up -d` (재생성) | 14 |
| 한글이 깨짐 | 로케일 | `LANG=C.UTF-8`, `PYTHONIOENCODING=utf-8` | |
| 시간이 9시간 다름 | 타임존 | `TZ=Asia/Seoul` (로그 시각과 감사 로그 대조 시 중요) | 13 |
| 데이터가 예상과 다름 | 샘플 vs 운영 데이터 스키마·인코딩 차이 | 운영 데이터 접근 심의를 일찍 | 부록 A |
| DB 쿼리가 느림 | 운영 데이터 볼륨 | 인덱스, 페이지네이션 | |
| 메모리 부족으로 재시작 | `limits.memory` 과소 | 상향 + 실제 사용량 측정 | 2 |
| 디스크가 찬다 | 로그 로테이션 미설정, `<none>` 이미지 누적 | `logging` 옵션, `docker image prune` | 3, 5 |
| 반입해 둔 이미지가 사라짐 | kubelet image GC (디스크 85% 초과) | 디스크 확보, tar 보관, 레지스트리에서 재pull | 10 |
| 이미지 재빌드 후 취약점 급증 | 베이스 태그 고정이 오래됨 | 최신 패치 태그로 `--build-arg BASE` | 3 |

## C-5. 진단 결과를 전달하는 양식

고객 인프라팀에 "안 됩니다"라고 말하는 대신 이 형식으로 전달하세요. 해결 속도가 눈에 띄게 빨라집니다.

```text
[문제] 에이전트 VM(10.20.5.11)에서 LLM 게이트웨이(llm-gw.corp.local:4000) 도달 불가

[확인 내역]
  1) 이름 해석: 성공 (nslookup llm-gw.corp.local → 10.20.7.30)
  2) 포트 연결: 실패 (nc -zv llm-gw.corp.local 4000 → timeout 5초)        ← 패킷이 버려짐
  3) 같은 대역 내 다른 서버: 성공 (nc -zv 10.20.7.31 22 → OPEN)              ← 라우팅은 정상
  4) 게이트웨이 서버에서 자체 확인: 리슨 중 (ss -ltnp | grep 4000 → 0.0.0.0:4000)

[추정 원인] 방화벽 정책 #5 (AGENT-VM → llm-gw:4000) 미적용 (승인은 완료, 작업 미반영 추정)

[요청] 정책 #5의 적용 상태 확인 요청
[영향] 파일럿 기능 검증 대기 중. 예상 지연 (영업일 기준) 2일
```

마지막 두 줄이 중요합니다. **영향과 지연을 함께 적으면 우선순위가 올라갑니다.** 그리고 2)와 3)의 대비(같은 대역의 다른 서버는 되는데 이것만 안 됨)가 "라우팅이 아니라 방화벽"이라는 근거입니다.
