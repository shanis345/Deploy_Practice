# Day 10 — Kubernetes 기초: Pod · Deployment · Service · probe

- 가이드: [해당 Day 원문](../docs/guide/src/11-day10.md)
- 상세 이력: [SESSION.md](SESSION.md)
- 전체 진행: [PROGRESS.md](../PROGRESS.md)

## 완료 범위

2026-10-05 사용자 제공 출력·캡처 기준으로 **10-1~10-6, k9s 조회, 실습 자원 정리 완료**다. 체크포인트 6개 해설을 제공했으며 독립 이해도 평가는 하지 않았다. 실습은 사용자가 Ubuntu WSL2에서 실행했고, Codex가 이번 PR 준비 중 재실행한 결과가 아니다.

| 단계 | 한 일 | 확인한 결과 |
| --- | --- | --- |
| 10-1 | k3d 클러스터·레지스트리·이미지 준비 | 노드 3개 Ready, agent 0.2.0/0.3.0 push 및 태그 조회 성공 |
| 10-2 | Namespace·Deployment·Service 배포 | agent 0.2.0 Pod 2개 준비, Deployment 2/2 |
| 10-3 | Service와 port-forward 비교 | Service 요청 8회가 두 Pod에 5:3 분산, port-forward 4회는 같은 Pod 응답 |
| 10-4 | 자가 치유·확장/축소·업데이트/롤백 | 삭제한 Pod 대체, 복제본 2→4→2, 0.3.0 업데이트 후 0.2.0 복귀 |
| 10-5 | 무응답 장애와 probe 복구 | 같은 Pod UID에서 컨테이너 재시작 0→1, Ready 복귀 및 HTTP 200 |
| 10-6 | 고장 예제 5개 진단 | 이미지·프로세스·자원·Secret·readiness 오류 구분 후 고장 리소스 삭제 |
| k9s·정리 | 상태·로그 조회 후 진단 Pod 삭제 | k9s 종료, probe 부재, 정상 agent 2/2 및 Service 유지 |

롤링 업데이트 관찰에서는 HTTP **60회 성공·0회 실패**였다. 이는 해당 표본에서의 결과이며 모든 상황의 무중단을 보장하지 않는다. 롤백과 무응답 장애 중에는 지속적인 Service 요청 측정을 하지 않았다.

## 핵심 이해

**쿠버네티스는 앱을 한 번 실행하는 것을 넘어, 선언한 상태를 계속 유지하는 시스템이다.**

- **Node**는 Pod가 실행되는 곳이다. 이번 노드 3개는 한 PC 안의 Docker 컨테이너이므로 물리 서버 3대의 고가용성 실험은 아니다.
- **Namespace**는 리소스의 논리적 관리 구획이다. VM이나 Node의 상위 크기 단위가 아니며 그 자체로 네트워크 격리를 보장하지 않는다.
- **Pod**는 앱 컨테이너가 실행되는 단위다. Pod 교체와 같은 Pod 안의 컨테이너 재시작은 다르다.
- **Deployment**는 원하는 버전·복제본 수를 선언한다. ReplicaSet을 통해 Pod 수를 유지하고 버전 교체를 관리한다.
- **Service**는 바뀌는 Pod 앞에 안정적인 이름과 접속 주소를 제공한다. 일반적인 설정에서 준비된 대상 Pod로 요청을 전달한다.
- **readiness**는 “지금 요청을 받아도 되는가”, **liveness**는 “재시작이 필요한가”를 검사한다. Running만으로 요청 처리 가능 상태를 판단하지 않는다.
- **kubectl·k9s**는 같은 클러스터를 조회·관리하는 도구다. CI/CD는 변경을 검증하고 전달·배포하는 절차이며 이번에는 CI/CD 파이프라인을 구축하지 않았다.

## 장애 진단 요약

| 관찰 상태 | 이번 예제의 근거 | 해석 |
| --- | --- | --- |
| ImagePullBackOff | 9.9.9 manifest 조회가 HTTP 404 / MANIFEST_UNKNOWN | 해당 태그가 없음. 최종 HTTPS 오류만 보고 인증서 문제로 단정하지 않음 |
| CrashLoopBackOff | 명령의 `sys.exit(1)`, 이전 로그, 재시작 증가 | 실행 후 종료 반복. 설정 누락 문구는 재현용 출력이며 실제 파일 검사는 아님 |
| Pending | CPU 64·메모리 512Gi 요청, FailedScheduling | 배치 가능한 노드가 없음. 실제 사용량이 아니라 요청량 문제 |
| CreateContainerConfigError | 필수 Secret `agent-secret-typo` not found | 컨테이너 시작에 필요한 설정을 만들 수 없음 |
| Running / Ready=False | readiness `/health`에서 반복 HTTP 404 | 앱은 실행 중이나 검사 경로 오류. 정상 경로는 `/healthz` |

## 체크포인트 복습

1. **온프렘 LoadBalancer Pending:** 외부 IP를 할당할 구현·연동이 없거나 설정 문제가 있을 수 있다. MetalLB, 사내 LB 연동, NodePort 등을 환경에 맞춰 구성한다. Ingress도 외부에서 Controller에 도달할 경로가 필요하다.
2. **readiness와 liveness:** DB 장애처럼 앱 재시작으로 해결되지 않는 문제는 readiness로 요청 수신 여부를 판단하도록 설계한다. 앱 무응답은 liveness 재시작 대상이 될 수 있다. 이번 `/healthz`는 DB 연결 상태를 검사하지 않는다.
3. **vSphere HA와 롤링 업데이트:** HA는 주로 호스트 장애 시 VM을 다른 호스트에서 재시작하는 인프라 복구다. 롤링 업데이트는 앱 버전을 점진적으로 교체하는 배포 방식이다. 서로 대체하지 않는다.
4. **CrashLoop 첫 진단:** `kubectl describe pod <Pod명>`으로 상태·Events를, `kubectl logs <Pod명> -c <컨테이너명> --previous`로 직전 컨테이너 로그를 본다. 대상 context·namespace도 지정한다.
5. **방화벽 출발지 IP:** CNI·SNAT·egress gateway·프록시·중간 NAT에 따라 Pod IP와 다를 수 있다. 플랫폼팀에 목적지별 실제 경로와 방화벽에서 보이는 주소를 확인한다.
6. **port-forward의 한계:** 로컬 프로세스·연결 유지에 의존하고 선택된 Pod 하나로 연결한다. Service의 정상 운영 경로·부하 분산을 대체하지 못하며 대상 Pod 종료 시 다시 연결해야 한다.

## 다음 시작 시 참고

- 마지막 사용자 출력: context `k3d-onprem`, namespace `ax-pilot`, agent 이미지 `onprem-registry:5000/ax/agent:0.2.0`, 복제본 2개 준비.
- Service: `agent`, ClusterIP `10.43.162.127`, `8000/TCP`. 주소는 당시 관찰값이며 재생성 후 같다고 가정하지 않는다.
- 고장 예제와 진단용 `probe`는 삭제했다. 앱·Service·Namespace·클러스터·레지스트리·이미지는 유지했다.
- 실습용 kubectl은 `$HOME/.local/share/onprem-lab/kubectl-v1.31.0/bin`에 있다. 새 Ubuntu 터미널에서는 PATH 선택을 다시 확인한다.
- Windows 저장소와 Ubuntu `/home/user/onprem-lab`은 별도 사본이다. 이번 기록·PR 작업은 Ubuntu 동기화를 의미하지 않는다.
- 다음 Day는 사용자 요청 후 시작한다. 재개 시 현재 환경을 다시 조회하고 진단 Pod가 남아 있다고 가정하지 않는다.

## 실습 파일과 증거

- 기본 배포: [Namespace](00-namespace.yaml), [Deployment](10-deployment.yaml), [Service](20-service.yaml)
- 고장 예제: [이미지](broken/01-imagepull.yaml), [CrashLoop](broken/02-crashloop.yaml), [Pending](broken/03-pending.yaml), [ConfigError](broken/04-configerror.yaml), [NotReady](broken/05-notready.yaml)
- 사용자 출력: [evidence/](evidence/). 발췌·요약 여부와 확인 주체를 각 파일에 표시했다.
- [진단·k9s·최종 정리 요약](evidence/106-final-summary-user-2026-10-05.txt). 원본 캡처는 저장소에 복사하지 않았으며 상세 명령과 판단 근거는 [SESSION.md](SESSION.md)에 남겼다.
