# 부록 D — 용어집 (고객사 대화용, 한↔영)

고객사 담당자가 쓰는 말과 문서에서 쓰는 말을 연결합니다. "뜻" 열은 정의가 아니라 **대화에서 그 말이 나왔을 때 무엇을 확인해야 하는가**에 가깝게 적었습니다.

## D-1. 조직·절차

| 한국어 | 영어 | 뜻 / 확인할 것 |
|---|---|---|
| 정보전략팀 / IT기획 | IT planning | 도입 승인·예산·표준 관리. 인프라 실행 권한은 없음 |
| 정보보호팀 / 보안팀 | information security | 방화벽·반입·심의 **승인** 주체 |
| IT운영 / 그룹 SI | IT operations / SI affiliate | 인프라 **실행** 주체. 변경관리 일정 별도 |
| 보안성 검토 / 보안심의 | security review | 설계서·데이터 흐름도·통제 항목 제출 → 승인. 가장 긴 리드타임 |
| 변경관리 / CAB | change management | 배포 가능 요일·시간대, 동결 기간 |
| 변경 동결 | freeze | 월말·결산·연말에 배포 금지 |
| 반입 / 반입 심사 | import / air-gap transfer | 폐쇄망으로 파일을 들여오는 절차. 해시·스캔·승인 |
| 반출 | export | 폐쇄망 밖으로 내보내기. 로그·데이터는 원칙 금지 |
| 서버접근제어 (SAC) | server access control / PAM | SSH를 대신하는 접속 통제. 파일 전송·포트 포워딩 제한 |
| 리드타임 | lead time | 신청부터 완료까지 영업일 |
| 스폰서 | sponsor | 예산·의사결정권자. 1주 차 리드타임 보고 대상 |

## D-2. 인프라

| 한국어 | 영어 | 뜻 / 확인할 것 |
|---|---|---|
| 하이퍼바이저 | hypervisor | 물리 서버를 VM으로 나누는 계층 (ESXi, KVM, Hyper-V, AHV) |
| vCenter | vCenter | ESXi 호스트를 묶어 관리하는 콘솔. HA·vMotion·DRS |
| 호스트 / 게스트 | host / guest | VM을 얹는 물리 서버 / VM 안의 OS |
| 클러스터 (vSphere) | cluster | HA·DRS로 묶인 호스트 그룹. 우리 VM이 HA 대상인지 |
| 데이터스토어 | datastore | VM 디스크 저장소. 용량·IOPS |
| 포트그룹 | port group | 가상 스위치의 VLAN 구획. **어느 존인지** 알려줌 |
| 템플릿 | template | 표준 OS 이미지. 사전 설치된 보안 에이전트 |
| 리소스 풀 | resource pool | 자원 상한. 증설 시 풀부터 |
| 스냅샷 | snapshot | 롤백 수단. 배포 전 요청 |
| 베어메탈 | bare metal | 가상화 없는 물리 서버 (GPU 서버가 흔히) |
| 고가용성 | HA (high availability) | 장애 시 서비스 유지. vSphere HA는 VM 재기동(중단 있음) |
| 이중화 | redundancy | 같은 기능을 둘 이상. 프록시 이중화 시 화이트리스트 동기화 확인 |
| 무중단 배포 | rolling update | 서비스를 멈추지 않고 버전 교체 |
| 수평/수직 확장 | scale out / scale up | 인스턴스 수 / 인스턴스 스펙 |
| DR | disaster recovery | 재해복구 사이트. 파일럿은 보통 대상 아님 |
| 컨테이너 런타임 | container runtime | containerd, Docker, CRI-O(OpenShift) |
| 오케스트레이터 | orchestrator | 쿠버네티스, OpenShift |
| IaC | infrastructure as code | Terraform(생성), Ansible(설정) |

## D-3. 네트워크·보안

| 한국어 | 영어 | 뜻 / 확인할 것 |
|---|---|---|
| 망분리 | network separation / segmentation | ① 서버 존을 방화벽으로 분리 ② 업무 PC망과 인터넷 PC망 분리 (규제). 어느 쪽인지 |
| 폐쇄망 | air-gapped / closed network | 인터넷 없음. 반입으로만 |
| 존 | zone | 보안 등급별 네트워크 구획 (DMZ / 업무망 / DB존 / 관리망 / 개발망) |
| DMZ | DMZ | 외부(또는 사용자)가 직접 닿는 서버. 에이전트를 두면 안 되는 곳 |
| 업무망 / 내부망 | internal network | 에이전트가 있어야 할 곳 |
| 관리망 | management network | 모니터링·백업·SAC. 감사 로그 저장소가 여기인 경우 |
| 인바운드 / 아웃바운드 | inbound / outbound | 들어오는 / 나가는. 인바운드가 훨씬 어려움 |
| 방화벽 정책 | firewall rule | 출발지 → 목적지 → 포트 → 방향 → 기간 |
| 방향성 | direction | 같은 두 지점이라도 방향이 다르면 다른 정책 |
| 포워드 프록시 | forward proxy | 나가는 트래픽 통제 (Squid, Zscaler). `HTTP_PROXY` |
| 리버스 프록시 | reverse proxy | 들어오는 트래픽 분배 (nginx, L7 스위치, API GW) |
| 화이트리스트 / 허용 목록 | allowlist | 프록시가 허용하는 목적지. FQDN 단위인지 |
| TLS 검사 / SSL 인스펙션 | TLS inspection / SSL interception | 프록시가 HTTPS를 풀어 검사. 사내 CA 필요 |
| 사내 CA / 루트 인증서 | corporate CA / root certificate | 검사 프록시가 서명에 쓰는 CA. 신뢰 목록에 추가해야 함 |
| 신뢰 저장소 | trust store | OS·언어·도구마다 따로 있음 |
| PAC | proxy auto-config | 브라우저용 프록시 설정 스크립트. 컨테이너에서는 못 씀 |
| SNI | server name indication | HTTPS에서 프록시가 볼 수 있는 유일한 정보(도메인) |
| WAF | web application firewall | L7 방어. 긴 요청·SSE에서 타임아웃 |
| L4/L7 스위치 | load balancer | 사내 LB. 타임아웃 확인 |
| 전용선 | dedicated line / Direct Connect | 클라우드 ↔ 사내. 있어도 방화벽 협의 별건 |
| 프라이빗 엔드포인트 | private endpoint / PrivateLink | 인터넷을 거치지 않는 클라우드 서비스 접점 |
| 세그멘테이션 | segmentation | 네트워크를 잘게 나눠 통제. NetworkPolicy |
| egress IP | egress IP | Pod가 밖으로 나갈 때 보이는 IP (OpenShift). 방화벽 출발지 |
| 최소 권한 | least privilege | 조회 전용 계정, 특정 스키마 |
| 취약점 스캔 | vulnerability scan | Trivy, Harbor 내장. 기준(CRITICAL 0 등) 확인 |
| SBOM | software bill of materials | 구성 요소 목록 (CycloneDX/SPDX) |
| 다이제스트 | digest | 이미지 내용 해시. 심의본 = 반입본 증명 |

## D-4. 컨테이너·쿠버네티스

| 한국어 | 영어 | 뜻 / 확인할 것 |
|---|---|---|
| 이미지 / 레이어 | image / layer | 파일시스템 스냅샷의 쌓임. 비밀은 지워도 남음 |
| 레지스트리 | registry | 이미지 저장소 (Harbor, Nexus, Artifactory). 프로젝트·로봇 계정 |
| 태그 / 다이제스트 | tag / digest | 이름 / 내용 해시. `latest` 금지 |
| 파드 | Pod | 최소 실행 단위. IP 하나 |
| 디플로이먼트 | Deployment | Pod 수 유지·롤링 업데이트 |
| 서비스 | Service | Pod 묶음의 고정 이름·IP. ClusterIP/NodePort/LoadBalancer |
| 인그레스 / 라우트 | Ingress / Route (OpenShift) | 외부 HTTP 진입. 컨트롤러 종류 확인 |
| 네임스페이스 / 프로젝트 | Namespace / Project (OpenShift) | 논리 구획. 권한·쿼터 단위 |
| 컨피그맵 / 시크릿 | ConfigMap / Secret | 설정 / 비밀값(base64, 암호화 아님) |
| 프로브 / 헬스체크 | probe / health check | readiness(트래픽) / liveness(재시작) / startup |
| 네트워크 정책 | NetworkPolicy | Pod 간 통신 제어. CNI 지원 필요 |
| CNI | container network interface | 네트워크 플러그인 (Calico, Cilium, OVN, Flannel) |
| SCC | Security Context Constraints | OpenShift의 Pod 보안 정책. 임의 UID |
| 임의 UID | arbitrary/random UID | OpenShift가 강제하는 실행 UID. GID 0 쓰기 권한으로 대응 |
| 헬름 차트 / values | Helm chart / values | 매니페스트 템플릿 / 환경별 값 |
| 롤아웃 / 롤백 | rollout / rollback | 배포 진행 / 되돌리기 |
| 자가 치유 | self-healing | 죽은 것을 자동으로 되살림 |
| 선언형 | declarative | 원하는 상태를 적고 시스템이 맞춤 |
| 쿼터 / 리밋레인지 | ResourceQuota / LimitRange | 네임스페이스 자원 상한. `resources` 필수 |
| kubelet 이미지 GC | image garbage collection | 디스크 85% 초과 시 미사용 이미지 삭제 |
| kustomize | kustomize | 매니페스트 묶음. `kubectl apply -k` |
| ArgoCD | ArgoCD | git의 차트/매니페스트를 자동 배포 (GitOps) |

## D-5. AI 배포

| 한국어 | 영어 | 뜻 / 확인할 것 |
|---|---|---|
| 추론 | inference | 학습된 모델로 결과를 얻는 것. 추론 서버(vLLM) |
| LLM 게이트웨이 | LLM gateway | 모델 호출을 한 곳으로 모으는 중계 (LiteLLM). 감사·키·비용 |
| 가상 키 | virtual key | 게이트웨이가 발급하는 부서·용도별 키. 예산 상한 |
| 데이터 미보관 | ZDR (zero data retention) | 제공사가 요청·응답을 저장하지 않는 계약 |
| 데이터 레지던시 | data residency | 데이터가 저장되는 지리적 위치 |
| 국외 이전 | cross-border transfer | 개인정보를 해외로 보내는 것. 동의·고지 |
| 감사 로그 | audit log | 누가·언제·무엇을. 프롬프트 원문 저장 여부는 합의 |
| 프롬프트 주입 | prompt injection | 입력에 섞인 지시로 모델을 조종하는 공격 |
| 사람 승인 | human-in-the-loop | 실행 전 사람이 확인 |
| 근거 제시 | grounding / citation | 답변의 출처를 데이터에 연결 |
| 사내 모델 호스팅 | self-hosted model | vLLM 등. GPU 필요 |
| 모델 파일 반입 | model import | 수십 GB. 실행 시 다운로드 금지 |
| 관측성 | observability | 로그·메트릭·추적. 파일럿 성과 측정의 전제 |
| 구조화 로그 | structured logging | JSON Lines. 수집 시스템 연동 |
| 요청 ID | request ID / correlation ID | 여러 시스템의 로그를 하나로 묶는 키 |
| walking skeleton | walking skeleton / tracer bullet | 전 구간을 관통하는 최소 시스템 |
| 런북 | runbook | 배포·운영·장애 절차서. 이관의 핵심 |
