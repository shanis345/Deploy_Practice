# 에이전트 파일럿 배포 런북

대상: 고객사 운영 담당자 / 다음 FDE. 이 문서만으로 배포·점검·롤백이 가능해야 한다.

## 1. 사전 조건 (배포 전 확보)
- [ ] VM 1대 (권장 vCPU 4 / 메모리 8GB / 디스크 100GB), 업무망, RHEL 9 또는 Ubuntu 22.04
- [ ] Docker Engine 또는 containerd 설치 승인 (sudo 또는 docker 그룹)
- [ ] 방화벽 개방 (신청서 #1~#7 — docs/방화벽-신청서.md)
- [ ] 사내 레지스트리 프로젝트(`ax`)와 로봇 계정, 또는 반입된 이미지 tar
- [ ] 사내 CA 인증서 파일 (TLS 검사 환경인 경우) → 이미지 `agent:<ver>-ca`
- [ ] 프록시 주소·포트, LLM 목적지 화이트리스트 등록 완료
- [ ] DB 조회 전용 계정 (`ro_user`) 발급
- [ ] LLM API 키 (또는 사내 모델 엔드포인트)
- [ ] 사내 DNS 등록: `agent-pilot.corp.local` → 사내 LB VIP → VM:8080

## 2. 배포 절차
1. 이미지 준비: `docker load -i agent-<ver>.tar` 또는 `docker pull harbor.corp.local/ax/agent:<ver>`
   - 반입 tar의 SHA256이 반입 신청서와 일치하는지 `sha256sum -c` 로 확인
2. `.env` 작성: `cp .env.example .env` 후 비밀값 입력 (이 파일은 서버에만 존재, 백업 시 제외)
3. `gateway/config.yaml` 의 모델 목적지·`gateway/squid.conf` 의 화이트리스트를 고객사 값으로
4. `docker compose config --quiet` (문법·치환 확인)
5. `docker compose up -d`
6. `./verify.sh` — 전 항목 OK 여야 배포 완료. 출력을 배포 확인서에 첨부
7. `http://<VM>:4000/ui` 에서 부서별 가상 키 발급 (LiteLLM 대시보드)

## 3. 검증 항목 (verify.sh)
| # | 항목 | 기대 |
|---|---|---|
| 1 | `/healthz`, 버전, 실습용 엔드포인트 차단 | 200 / 버전 일치 / 403 |
| 2 | `/diag` — 게이트웨이 주소, 프롬프트 마운트, non-root | 의도와 일치 |
| 3 | 에이전트 인터넷 직접 접근 | 차단 |
| 4 | DB 조회 전용 계정 | 읽기 성공, 쓰기 거부 |
| 5 | 게이트웨이 경유 LLM 호출, 잘못된 키 거부 | llm / 401 |
| 6 | 감사 로그 적재 | 요청당 1행 |
| 7 | 프록시 화이트리스트 | 허용 200, 비허용 403 |

## 4. 운영 절차
| 작업 | 명령 |
|---|---|
| 상태 확인 | `docker compose ps`, `lazydocker` |
| 로그 | `docker compose logs -f --tail 100 agent` (JSON Lines) |
| 프롬프트·rubric 변경 | `config/prompt.txt` 수정 → 5초 내 자동 반영 (재시작 불필요). `curl localhost:8080/prompt` 로 확인 |
| 로그 레벨·모델 변경 | `.env` 수정 → `docker compose up -d agent` |
| 화이트리스트 변경 | `gateway/squid.conf` 수정 → `docker compose restart proxy` |
| 버전 업 | 이미지 반입 → `.env`의 `AGENT_IMAGE` 태그 수정 → `docker compose up -d` → `./verify.sh` |
| 롤백 | `.env`의 태그를 이전 버전으로 → `docker compose up -d` → `./verify.sh` |
| 감사 로그 조회 | `docker compose exec audit-db psql -U audit -d auditdb -c 'SELECT ... FROM "LiteLLM_SpendLogs"'` |
| 디스크 정리 | `docker system df` → `docker image prune -f` (사용 중 이미지는 안 지움) |

## 5. 장애 대응
| 증상 | 1차 확인 | 조치 |
|---|---|---|
| 사용자 502/504 | `docker compose ps` (agent healthy?) | `docker compose restart agent`; LB·nginx 타임아웃 300초 확인 |
| 응답 없음, 컨테이너는 Up | `curl localhost:8080/healthz -m 3` | 무응답이면 `docker compose restart agent` (Compose는 자동 복구 못 함) |
| LLM 응답 없음 | `docker compose logs llm-gateway`, 프록시 로그 `TCP_DENIED` 여부 | 화이트리스트·키·`/diag`의 게이트웨이 주소 확인 |
| 인증서 오류 | `/diag`의 `ca` 항목, `openssl s_client -proxy` | 사내 CA 재적용 (`agent:<ver>-ca` 재빌드) |
| DB 연결 실패 | `curl 'localhost:8080/tcp?host=<DB>&port=5432'` | 방화벽 #3, 계정 만료 확인 |
| 디스크 부족 | `df -h`, `docker system df` | `docker image prune -f`, 로그 로테이션 확인 |
| 이미지가 사라짐 | `docker images` | 반입 tar 재적재 (`docker load`) |

## 6. 이관 시 인수 항목
- [ ] 이미지와 태그 이력, 반입 신청서·다이제스트
- [ ] `compose.yaml`, `nginx/`, `gateway/`, `config/` 전체와 `.env.example` (비밀값 제외)
- [ ] 이 런북과 `verify.sh`
- [ ] 방화벽 신청 내역과 회수 예정일
- [ ] 감사 로그 스키마(`LiteLLM_SpendLogs`)와 보관·백업 정책
- [ ] 가상 키 목록과 예산 설정
- [ ] 정식 전환 조건 목록 (아래)

## 7. 정식 서비스 전환 조건 (파일럿에서 미충족)
| 항목 | 현재 (파일럿) | 정식 요건 |
|---|---|---|
| 고가용성 | VM 1대 (단일 장애점) | 쿠버네티스/OpenShift 2노드 이상, replicas ≥ 2, liveness probe |
| 무응답 복구 | 사람이 재시작 | liveness probe 자동 재시작 |
| 인증 | 없음 (사내망 신뢰) | SSO(OIDC) 연동, 사용자별 권한·가상 키 |
| 부하 | 동시 5명 수준 검증 | 목표 동시 사용자 수 부하 시험, HPA |
| 관제 | 컨테이너 로그·`/metrics` | 사내 로그 수집·Grafana 연동, 알람 |
| 비밀 관리 | `.env` 평문 | Vault/KMS 연동 또는 Secret + RBAC |
| 백업 | 없음 | 감사 로그·설정 백업 정책, DR 대상 여부 |
| 배포 | 수동 `compose up` | Helm 차트 + 파이프라인(ArgoCD/Jenkins), 변경관리 절차 |
| 운영 주체 | FDE 팀 | 고객사 운영 조직 (지정 필요) + SLA |
