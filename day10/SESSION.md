# Day 10 — Kubernetes 기초: Pod · Deployment · Service · probe

## 진행 상태
- 상태: 10-1~10-6·k9s·최종 정리 완료 · 체크포인트 6개 해설 제공·이해도 평가 미진행
- 완료한 범위: 10-1 클러스터·이미지 준비, 10-2 첫 배포, 10-3 Service/port-forward 비교, 10-4 자가 치유·확장/축소·업데이트/롤백, 10-5 liveness 복구 확인, 10-6 고장 예제 5개 진단·정리, k9s 조회·종료, probe 삭제
- 중단 지점: 실습 기록을 정리해 GitHub PR을 생성하는 단계. 체크포인트 해설은 제공했으나 독립 이해도 평가는 하지 않았다.
- Codex 작업: 아직 별도 작업을 만들지 않음
- 실행 증거 기준: 사용자 제공 출력과 직접 검증 결과를 구분해 기록

## 목표와 이번 세션 범위
10-1~10-6 및 사용자 요청에 따른 k9s 조회를 완료했다. 이어 "좋아 정리하자" 요청에 따라 probe만 삭제하고 정상 앱/Service 유지까지 확인했다. 체크포인트 평가는 아직 미진행이며 다음 Day나 추가 리소스 변경으로 임의 확장하지 않는다. 실습 명령은 사용자가 Ubuntu에서 직접 실행한다.

## 실행 기록
사용자 제공 Ubuntu 실행 결과와 Codex의 Windows 기록 작업을 아래 날짜별 이력에 구분한다.

현재 결과는 [Day 10 요약](README.md)을 먼저 읽고, 실행 명령과 중간 상태는 아래 날짜별 이력을 따른다. 과거 항목의 “대기 중/미완료”는 해당 시점의 상태이며 현재 상태가 아니다.

## 오류와 해결
- kubectl 버전 차이: 시스템 1.36.1 대신 실습용 1.31.0을 별도 설치·체크섬 검증하고 현재 셸에서 선택했다.
- port-forward 연결 거절: 재실행 후 포트가 45537에서 39827로 바뀌었다. 현재 출력의 포트로 요청해 성공했다.
- probe exec 실패: `sleep 3600` 종료로 Pod가 Completed 상태였다. 진단 Pod를 재생성하고 Ready 후 다시 실행했다.
- Python 구문을 Bash에 입력한 오류: 장애 컨테이너의 명령 설명과 사용자 셸 실행 명령을 구분했다.
- 고장 예제 5개: 원인을 진단한 후 예제를 삭제했다. 각 예제 설정을 수정해 정상화하는 실습을 완료한 것은 아니다.

## 배운 내용과 질문
- 핵심 개념: 원하는 상태를 유지하는 조정 루프, Pod·Deployment·Service·probe, Namespace·권한·외부 통신을 설명했다.
- 사용자 질문 "네임스페이스가 일종의 VM인가 그보다 더 큰 단위인가?"에 대해 Node는 실행 위치, Namespace는 리소스의 논리적 관리 구획임을 설명했다. 하나의 Namespace의 Pod가 여러 Node에 배치되고 하나의 Node에서 여러 Namespace의 Pod가 실행될 수 있다.
- 기업 인프라를 물리 서버·가상화·VM/Node·컨테이너 실행 기반·Pod로 도식화했다. Control Plane의 관리 경로와 사용자 요청 경로를 구분했다. 설명 제공이며 독립 평가 통과로 기록하지 않는다.

## 가이드와 실제 환경의 차이
공통 환경은 [환경 기록](../docs/environment.md)을 참고한다.

## 다음에 이어 할 지점
실습·k9s·정리를 완료하고 체크포인트 6개 해설을 제공했다. 자가 설명/이해도 평가가 필요하면 사용자 요청으로 진행하며 해설 열람을 평가 통과로 기록하지 않는다. 앱 0.2.0/2개 준비·Service·Namespace·클러스터·레지스트리는 유지한다. probe는 삭제됐다. 다음 Day는 사용자 요청 전 시작하지 않는다.

### 2026-10-05 — Day 10 시작·사전 점검 안내
- 사용자 요청: "자 이제 다음 챕터로 넘어가자 Day 10인가?"
- Codex는 Windows의 PROGRESS·환경 기록·Day 10 README/SESSION·가이드 핵심 개념과 10-1, Day 9 종료 기록을 확인했다. Day 9는 9-1~9-5·자원 정리·PR #11 병합 확인까지 완료했으며 누적 점검·체크포인트 평가는 미진행이다.
- Day 10은 Pod·Deployment·Service·probe를 학습한다. 첫 단계는 k3d 클러스터 생성 전 환경 확인이다.
- 실행 위치: 사용자 Ubuntu WSL2. 다음 명령은 안내만 했으며 실행 결과 대기 중이다.

```bash
cd /home/user/onprem-lab
docker version --format 'Client={{.Client.Version}} Server={{.Server.Version}}'
k3d version
kubectl version --client
k3d cluster list
```

- 이전 kubectl 1.36.1과 가이드 k3s 1.30의 버전 차이를 확인할 필요가 있다. 현재 버전·기존 클러스터 상태는 아직 미확인이다.
- 설치·클러스터 생성·이미지 다운로드·Ubuntu 동기화·별도 Codex 작업 생성은 수행하지 않았다. 다음은 사용자 출력 확인이다.

### 2026-10-05 — 사용자 10-1 시작 요청·첫 점검 재안내
- 사용자 요청: "좋아 그러면 10-1부터 시작해보자". Codex는 PROGRESS·환경·Day 10 README/SESSION·가이드 10-1을 다시 확인했다.
- 위 사전 점검 명령의 사용자 실행 결과는 아직 받지 않았다. 동일한 Ubuntu WSL2 조회 명령 5줄을 첫 단계로 다시 안내한다.
- 점검 목적: Docker 엔진 연결, k3d 및 기본 k3s 버전, kubectl 클라이언트 버전, 기존 클러스터 존재 여부 확인. 현재 버전이나 클러스터 부재를 이전 기록만으로 확정하지 않는다.
- 다음 단계: 사용자 출력 확인 후 버전 호환성과 Windows 포트 점유·제외 범위 등을 점검한다. 가이드 8080·5001 포트와 실제 사용 포트는 아직 확정하지 않았다.
- Windows 학습 기록만 갱신했다. 실습 실행·설치·클러스터 생성·이미지 등록·Ubuntu 파일 복사는 아직 하지 않았다. 10-1 미완료, 사전 점검 결과 대기 상태다.

### 2026-10-05 — 첫 점검 확인·kubectl 버전 차이 대응 안내
- [사용자 출력](evidence/101-precheck-user-2026-10-05.txt): Docker Client/Server 29.8.0 연결 정상, k3d v5.7.4, 기본 k3s v1.30.4-k3s1, kubectl v1.36.1·Kustomize v5.8.1. k3d cluster list는 헤더만 표시돼 등록된 k3d 클러스터가 없다. 다른 방식의 Kubernetes 클러스터 부재까지 확인한 것은 아니다.
- k3s 출력은 생성 예정 기본 버전이며 실행 중인 서버 버전이 아니다. 클러스터는 아직 생성하지 않았다.
- Codex가 [공식 버전 정책](https://kubernetes.io/releases/version-skew-policy/#kubectl)을 확인했다. kubectl과 API 서버는 마이너 버전 차이 1 이내가 지원 범위이므로 1.36/1.30 조합은 범위 밖이다. 실제 연결 실패를 관찰한 것은 아니다.
- 가이드와 bootstrap.sh의 kubectl v1.31.0을 실습 전용 사용자 경로에 설치하도록 안내한다. 기본 k3s 1.30과의 버전 차이 조건을 충족한다. 이 구버전 구성은 가이드 재현용이며 운영용 버전 권장이나 전체 호환성 검증과 구분한다.
- [공식 Linux 설치 방법](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)에 따라 공식 바이너리와 SHA-256을 내려받고 검증 후 설치한다. 실행 위치: 사용자 Ubuntu WSL2. 다음은 안내 명령이며 결과 대기 중이다.

```bash
(
  lab_kubectl_tmp=$(mktemp -d) &&
  cd "$lab_kubectl_tmp" &&
  curl -fSLO https://dl.k8s.io/release/v1.31.0/bin/linux/amd64/kubectl &&
  curl -fSLO https://dl.k8s.io/release/v1.31.0/bin/linux/amd64/kubectl.sha256 &&
  echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check &&
  install -D -m 0755 kubectl "$HOME/.local/share/onprem-lab/kubectl-v1.31.0/bin/kubectl"
) &&
export PATH="$HOME/.local/share/onprem-lab/kubectl-v1.31.0/bin:$PATH" &&
hash -r &&
command -v kubectl &&
kubectl version --client
```

- 시스템 kubectl과 셸 설정 파일은 수정하지 않는다. PATH는 현재 셸에서만 선택하며 다운로드 임시 폴더는 이번 명령에서 삭제하지 않는다. 실제 설치·체크섬 성공·선택 경로는 아직 미확인이다.
- 다음은 사용자 설치 결과 확인 후 포트·자원 점검이다. 클러스터 생성·이미지 등록·10-1 완료·10-2 진행은 아직 아니다.

### 2026-10-05 — kubectl 설치 확인·Windows 포트 조회 안내
- [사용자 Ubuntu 출력](evidence/101-kubectl-user-2026-10-05.txt): kubectl: OK, /home/user/.local/share/onprem-lab/kubectl-v1.31.0/bin/kubectl, Client Version v1.31.0, Kustomize v5.4.2를 확인했다. 공식 파일 체크섬 검증·사용자 경로 설치·현재 셸 선택 성공이다.
- 기존 시스템 kubectl이나 셸 설정 파일을 변경하는 명령은 실행하지 않았다. 설치 시 임시 다운로드 폴더는 삭제하지 않았으며 경로는 사용자 출력에 없다. 새 Ubuntu 터미널에서는 PATH 선택을 다시 적용해야 한다.
- 버전 차이 조건을 충족하는 클라이언트를 준비한 것이며 아직 생성하지 않은 클러스터와의 실제 통신 성공을 뜻하지 않는다.
- Day 9에서 Windows 제외 포트 범위에 의한 게시 실패가 있었으므로 클러스터 생성 전 Windows 포트를 조회한다. 가이드의 8080(향후 Ingress 진입)·5001(이미지 레지스트리)과 대안 18080·15001을 함께 조회하도록 안내했다.
- 실행 위치: Windows PowerShell. 아래 명령은 안내만 했고 결과 대기 중이다. 포트를 예약하거나 해제하는 명령이 아니다.

```powershell
Get-NetTCPConnection |
  Where-Object { $_.LocalPort -in 8080,5001,18080,15001 } |
  Format-Table LocalAddress,LocalPort,State,OwningProcess -AutoSize
netsh interface ipv4 show excludedportrange protocol=tcp
netsh interface ipv6 show excludedportrange protocol=tcp
```

- 기본·대안 포트의 사용 가능 여부는 아직 미확인이다. 다음은 사용자 Windows 출력 검토 후 Ubuntu 자원·파일 점검이다. 클러스터 생성·이미지 등록·10-1 완료·10-2 진행은 아직 아니다.

### 2026-10-05 — Windows 포트 확인·Ubuntu 최종 사전 조회 안내
- [사용자 Windows 출력](evidence/101-windows-ports-user-2026-10-05.txt): 8080·5001·18080·15001 TCP 사용 행이 없고 네 포트 모두 IPv4/IPv6 제외 범위 밖이다. IPv4와 IPv6 제외 범위 목록은 서로 같다.
- Day 9에서 관찰한 7987~8086 범위는 이번 목록에 없다. 현재 8080은 제외되지 않으며 목록 변화의 원인·시점은 미확정이다. 실제 포트 바인딩 성공을 검증한 것은 아니다.
- 가이드의 8080(향후 Ingress용)·5001(레지스트리)을 사용할 계획이다. 대안 포트 적용·Windows 설정 변경은 하지 않았다.
- 다음 사용자 실행 위치: 기존 실습용 kubectl PATH가 선택된 Ubuntu WSL2 터미널. 아래 조회는 안내만 했으며 결과 대기 중이다.

```bash
cd /home/user/onprem-lab && pwd
free -h
df -h .
docker info --format 'CPUs={{.NCPU}} MemoryBytes={{.MemTotal}}'
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker image ls --filter 'reference=agent:*' --format 'table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}'
ss -ltn '( sport = :8080 or sport = :5001 )'
ip -4 route
docker network inspect $(docker network ls -q) --format '{{.Name}}: {{range .IPAM.Config}}{{.Subnet}} {{end}}'
ls -l day10/00-namespace.yaml day10/10-deployment.yaml day10/20-service.yaml
```

- 목적: Ubuntu 메모리·디스크 여유와 Docker 엔진 할당 자원, 기존 컨테이너 이름·게시 포트, agent 이미지 태그, Ubuntu 리스너·라우팅·Docker 주소 대역 및 Day 10 파일 존재를 확인한다. Ubuntu free와 Docker 엔진 메모리를 동일 환경 값으로 단정하지 않는다. 파일 존재 조회는 Windows/Ubuntu 내용 일치 검증과 구분한다.
- 클러스터 생성·이미지 다운로드·파일 동기화·기존 자원 변경은 아직 없다. 결과 검토 후 생성 단계로 이어 간다. 10-1 미완료, 10-2 미진행이다.

### 2026-10-05 — Ubuntu 사전 점검 확인·클러스터 생성 안내
- [사용자 출력](evidence/101-resources-user-2026-10-05.txt): Ubuntu 메모리 총 15Gi·available 13Gi, /dev/sdc 가용 951G, Docker CPUs=32·MemoryBytes=16334528512를 확인했다. WSL 가상 디스크 표시값은 실제 Windows 디스크 여유와 구분한다.
- 기존 컨테이너 8개는 모두 Exited다. agent:0.2.0(a4ef49ae142e)·0.2.0-offline·0.2.0-ca·0.1.0이 있고 0.3.0 태그는 없다. 0.3.0 빌드·등록은 클러스터 기동 확인 뒤 진행한다. 기존 자원은 변경하지 않는다.
- Ubuntu의 8080·5001 리스너 조회는 헤더만 표시됐다. WSL 172.18.48.0/20과 기존 koica Docker 172.18.0.0/16의 겹침은 여전히 존재한다. 새 클러스터의 Docker 네트워크는 자동 할당 후 확인한다. 기존 대역 겹침 해소·전체 경로 무충돌로 판단하지 않는다.
- Ubuntu Day 10 YAML 3개 존재·user:docker·0755를 확인했다. 파일 내용의 Windows/Ubuntu 일치는 아직 검증하지 않았으며 이번 생성 명령은 이 YAML을 적용하지 않는다.
- [k3d 5.7.4 명령 문서](https://k3d.io/v5.7.4/usage/commands/k3d_cluster_create/)에서 image·registry-create·port·wait·timeout 및 기본 kubeconfig 갱신/전환 동작을 확인했다. 가이드 재현용 k3s 이미지를 명시하고 웹/레지스트리 게시 주소는 127.0.0.1로 제한한다. API 포트는 k3d 기본 자동 할당을 사용하며 이 명령에서 API 바인딩 주소는 별도 지정하지 않는다.
- 실행 위치: 사용자 Ubuntu WSL2. 다음은 실제 자원을 만드는 안내 명령이며 Codex는 실행하지 않았다. 필요한 이미지 다운로드, 노드·레지스트리·로드밸런서 및 네트워크·볼륨 생성, kubeconfig 갱신과 current-context 전환이 발생할 수 있다.

```bash
cd /home/user/onprem-lab/day10 &&
k3d cluster create onprem \
  --image rancher/k3s:v1.30.4-k3s1 \
  --servers 1 --agents 2 \
  --registry-create onprem-registry:127.0.0.1:5001 \
  --port "127.0.0.1:8080:80@loadbalancer" \
  --wait --timeout 300s &&
kubectl --context k3d-onprem get nodes -o wide &&
kubectl --context k3d-onprem get pods -n kube-system &&
docker network inspect k3d-onprem --format '{{.Name}}: {{range .IPAM.Config}}{{.Subnet}} {{end}}'
```

- 사용자 생성 로그와 조회 결과 대기 중이다. --wait는 서버 준비 대기이며 모든 워커·시스템 Pod 정상 여부는 후속 출력으로 따로 확인한다. 오류 시 같은 생성 명령을 바로 재실행하지 않고 로그를 확인한다.
- 10-1 이미지 등록·완료, 10-2 배포는 아직 아니다. kubeconfig 본문이나 토큰 등 비밀 자료는 증거로 요청하지 않는다.

### 2026-10-05 — 클러스터 생성·노드 Ready 확인 및 초기화 조회 안내
- [사용자 생성 출력](evidence/101-cluster-user-2026-10-05.txt): 43초 시점의 생성 성공 로그와 서버 1·워커 2 모두 Ready를 확인했다. Kubernetes는 v1.30.4+k3s1, 런타임은 containerd 1.7.20-k3s1이다. 기존 실습용 kubectl로 명시한 k3d-onprem context의 API 조회가 성공했다.
- 노드 IP: server-0 172.21.0.3, agent-0 172.21.0.5, agent-1 172.21.0.4. 새 k3d-onprem 네트워크는 172.21.0.0/16이며 앞서 조회한 WSL·Docker 대역과 겹치지 않는다. 기존 WSL/koica 겹침은 해결한 것이 아니다.
- k3d-onprem-images 볼륨, onprem-registry, 서버/워커/로드밸런서 생성·기동 로그와 registry:2·k3s·k3d tools/proxy 다운로드를 확인했다. 도구 컨테이너의 최종 잔존 여부와 실제 포트 게시 목록은 아직 별도 조회하지 않았다.
- kube-system 조회에는 AGE 0s의 helm-install-traefik-crd·helm-install-traefik 두 Pod만 보였고 둘 다 ContainerCreating이다. 초기화 직후 관찰로 기록하며 모든 시스템 구성 요소가 준비됐다고 판단하지 않는다. 설치 작업의 Completed는 정상 완료 상태가 될 수 있다.
- Codex는 Windows 빌드 소스 3종을 직접 조회했다. SHA-256: agent/Dockerfile=318eaab0d59bc5242bef1c2349d09fcdee9606ecbd3c1dd6c6a6d82a31be79c9, agent/app.py=fdab9fd80709fe7a7ff99527cdf1ff68d3c80ecaab72d148bf4dc5d76b9b01b0, agent/requirements.txt=8320562585358eff824b13356c837a7ffb3faf7d8700823fbc014a3a8c8ec71a. Ubuntu 대응 해시는 아직 미확인이다.
- 다음 사용자 Ubuntu WSL2 읽기 전용 조회를 안내했다. 결과 대기 중이며 0.3.0 빌드·push·앱 배포는 아직 하지 않았다.

```bash
kubectl --context k3d-onprem get pods -n kube-system -o wide
kubectl --context k3d-onprem get deployments -n kube-system
docker ps --filter network=k3d-onprem --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
curl --noproxy '*' -fsS --max-time 10 -w '\nHTTP %{http_code}\n' http://127.0.0.1:5001/v2/
sha256sum /home/user/onprem-lab/agent/Dockerfile /home/user/onprem-lab/agent/app.py /home/user/onprem-lab/agent/requirements.txt
```

- 클러스터는 유지한다. 레지스트리 HTTP 응답·이미지 등록은 미검증이므로 10-1 전체 완료로 처리하지 않는다. 10-2도 미진행이다.

### 2026-10-05 — 시스템 초기화·레지스트리·소스 일치 확인 및 0.3.0 빌드 안내
- [사용자 출력](evidence/101-system-registry-user-2026-10-05.txt): coredns·local-path-provisioner·metrics-server·traefik Deployment 모두 READY 1/1·AVAILABLE 1이다. 해당 Pod는 Running·재시작 0, svclb-traefik Pod 3개도 2/2 Running·재시작 0이다. 설치 Job Pod 두 개는 Completed이며 helm-install-traefik의 재시작 1회 원인은 조사하지 않았다.
- Docker onprem 네트워크의 컨테이너 6개가 Up 3 minutes다. k3d-onprem-tools도 실행 중임을 확인했다. serverlb는 127.0.0.1:8080->80 및 0.0.0.0:37327->6443, 레지스트리는 127.0.0.1:5001->5000을 게시한다. API 포트는 루프백 제한이 아니다. 외부 PC에서의 접근 가능 여부는 확인하지 않았다.
- Ubuntu의 레지스트리 /v2/ 요청이 {}·HTTP 200으로 성공했다. 이미지 push/pull 검증은 아직 아니다. Pod IP는 10.42.x.x이고 Node 네트워크는 172.21.0.0/16으로 서로 구분한다.
- agent/Dockerfile·app.py·requirements.txt의 Ubuntu SHA-256이 앞서 Codex가 직접 조회한 Windows 해시와 모두 일치했다. 세 파일에 대한 일치 검증이며 전체 소스나 Day 10 매니페스트 일치 검증은 아니다.
- Windows Dockerfile·app.py에서 APP_VERSION 빌드 인자가 환경변수로 들어가고 앱의 버전 응답에 사용됨을 확인했다. 가이드 10-1에 따라 BASE=python:3.12.14-slim·APP_VERSION=0.3.0으로 별도 이미지를 빌드한다. 베이스 이미지 태그는 가변이므로 기존 0.2.0과 모든 레이어가 동일하다고 단정하지 않는다.
- 다음 사용자 Ubuntu WSL2 명령을 안내했다. 필요한 베이스/의존성 다운로드가 발생할 수 있고 Docker 이미지·빌드 캐시가 생성된다. 기존 0.2.0 태그는 바꾸지 않는다. 실제 실행 결과 대기 중이다.

```bash
cd /home/user/onprem-lab/agent &&
docker build \
  --build-arg BASE=python:3.12.14-slim \
  --build-arg APP_VERSION=0.3.0 \
  -t agent:0.3.0 . &&
docker image inspect agent:0.2.0 agent:0.3.0 |
  jq '.[] | {tags: .RepoTags, id: .Id, platform: (.Os + "/" + .Architecture), user: .Config.User, app_version: [.Config.Env[] | select(startswith("APP_VERSION="))]}'
```

- 두 버전의 이미지 ID·플랫폼·USER·APP_VERSION 결과를 확인한 뒤 레지스트리 태그 추가·push를 안내한다. 전체 환경변수를 출력하지 않고 APP_VERSION만 선택한다. 0.3.0 빌드 성공·push·10-1 완료·10-2 배포는 아직 아니다. 클러스터는 유지한다.

### 2026-10-05 — 0.3.0 빌드 확인·두 이미지 push 안내
- [사용자 빌드 출력](evidence/101-build-user-2026-10-05.txt): 13/13 FINISHED·1.5초, builder 의존성 단계 캐시 재사용, agent:0.3.0 저장을 확인했다. base digest는 f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f다.
- agent:0.2.0 ID=a4ef49ae142efb1a03fe43c30d4a6f68ceee1c649578c33407827e8f6f4185a3, agent:0.3.0 ID=3b2b97652b5db89e15b8750375cef5d163bd2a72405902dcda882e6cde5c6ec6. 둘 다 linux/amd64·USER=10001이며 APP_VERSION은 각각 0.2.0·0.3.0이다.
- 0.3.0의 로컬 ID는 빌드 manifest list digest와 일치한다. 플랫폼 manifest e453bdc4...·config 9e7d30ae...와 구분하며 전체 식별자는 증거에 보존했다. 기존 0.2.0 ID는 사전 점검의 짧은 ID와 일치한다.
- 이미지 설정을 확인한 것이며 새 이미지의 앱 기동·healthz·취약점 검사까지 검증한 것은 아니다. 베이스 태그 재해석이나 레이어 동일성은 이 출력만으로 단정하지 않는다.
- 다음 사용자 Ubuntu WSL2 실행을 안내했다. 로컬 레지스트리용 태그를 추가하고 Docker 엔진에서 레지스트리로 두 버전을 업로드한 뒤 HTTP API로 태그 목록을 조회한다.

```bash
cd /home/user/onprem-lab/day10 &&
docker tag agent:0.2.0 localhost:5001/ax/agent:0.2.0 &&
docker push localhost:5001/ax/agent:0.2.0 &&
docker tag agent:0.3.0 localhost:5001/ax/agent:0.3.0 &&
docker push localhost:5001/ax/agent:0.3.0 &&
curl --noproxy '*' -fsS --max-time 10 \
  -w '\nHTTP %{http_code}\n' \
  http://127.0.0.1:5001/v2/ax/agent/tags/list
```

- 호스트 업로드 주소는 localhost:5001, 이후 클러스터 노드에서 받을 주소는 onprem-registry:5000이다. 두 주소는 같은 레지스트리를 서로 다른 위치에서 가리킨다. 실제 클러스터 이미지 pull 검증은 아직 없다.
- 사용자 push·태그 조회 결과 대기 중이다. 이미지 등록 완료·10-1 완료·10-2 배포로 기록하지 않는다. 기존 agent 태그·Day 9 산출물·클러스터를 유지한다.

### 2026-10-05 — 두 이미지 등록 확인·10-1 완료
- [사용자 push·태그 출력](evidence/101-push-user-2026-10-05.txt)으로 localhost:5001/ax/agent의 0.2.0·0.3.0 push 성공과 HTTP 200, tags=[0.3.0, 0.2.0]을 확인했다. 태그 순서는 의미가 없다.
- push digest: 0.2.0=sha256:a4ef49ae142efb1a03fe43c30d4a6f68ceee1c649578c33407827e8f6f4185a3, 0.3.0=sha256:3b2b97652b5db89e15b8750375cef5d163bd2a72405902dcda882e6cde5c6ec6. 이번 Docker 저장 방식에서 앞서 조회한 각 로컬 이미지 ID와 일치한다. 이를 모든 Docker 환경의 ID/digest 관계로 일반화하지 않는다.
- 두 push의 size: 856은 push가 보고한 manifest/index 객체 크기이며 전체 이미지 크기가 아니다. 0.3.0의 Layer already exists는 레지스트리에 이미 있는 공유 레이어를 재사용한 정상 출력이다.
- 10-1 완료 범위: 실습용 kubectl 1.31.0 준비, 포트·자원 점검, k3d onprem 생성, 노드 3개 Ready 및 시스템 Deployment 4개 준비, 레지스트리 HTTP 확인, agent:0.3.0 빌드, 두 버전의 linux/amd64·USER=10001·APP_VERSION 및 레지스트리 등록 확인.
- 실습 검증 근거는 사용자 Ubuntu/Windows 출력이다. Codex는 Windows 문서·빌드 소스 해시·사용자 출력 식별자를 대조하고 기록했다. 새 이미지의 앱 기동·클러스터 노드 pull·healthz·스캔은 아직 검증하지 않았다.
- 유지할 상태: onprem 클러스터와 onprem-registry, k3d-onprem 네트워크·이미지 볼륨, Docker 이미지·추가 레지스트리 태그, 실습용 kubectl. 기존 Day 9 산출물 및 다른 프로젝트 자원은 이번 과정에서 정리하지 않았다.
- SESSION·PROGRESS·README·환경 기록을 갱신했다. 10-2 이후·Day 10 전체 완료·실습 자원 정리·Git 커밋/push는 수행하지 않았다. 다음은 사용자 요청 후 10-2 첫 배포다.

### 2026-10-05 — 10-2 시작·파일 검증과 첫 배포 안내
- 사용자 요청: "다음으로 넘어가자". Codex는 PROGRESS·환경·Day 10 README/SESSION·가이드 10-2 및 YAML 3개를 읽었다. 이번 요청은 10-2까지로 해석하고 10-3 명령은 안내하지 않는다.
- Windows YAML SHA-256 직접 확인: 00-namespace.yaml=48f8bf06dd1d67dbffccba0330e24b0ea3b132730eef4b9a092068c499f0a741, 10-deployment.yaml=b65fb5c9e7c8c34898a2c1775d9dcf4c94c62b93dc6ec038f447282dcc6ffa0e, 20-service.yaml=6770b2a51d624c552cd384924aa5a1ac8d74da4071cdb1904eebbaafe7a1619b.
- 내용 확인: Namespace ax-pilot·zone=biz, Deployment agent·replicas=2·onprem-registry:5000/ax/agent:0.2.0·app=agent 라벨, Service agent·ClusterIP·8000→컨테이너 http 포트(8000)다. Service는 Deployment 이름이 아니라 Pod 라벨을 selector로 사용한다.
- 보안 설정은 UID 10001·GID 0·runAsNonRoot·권한 상승 금지·capabilities ALL 제거·RuntimeDefault seccomp·읽기 전용 루트 파일시스템·/app/tmp emptyDir다. Pod당 requests CPU 100m/메모리 128Mi, limits CPU 1/메모리 512Mi이며 /healthz readiness/liveness를 지정한다.
- replicas=2만으로 서로 다른 노드 배치를 보장하지 않는다. 이 YAML에는 강제 anti-affinity나 topology spread 설정이 없으므로 실제 노드 배치를 출력에서 확인한다. 보안 필드 설정 자체를 고객사 심의 통과나 외부 의존성 정상의 증거로 취급하지 않는다.
- 사용자 실행 위치: 기존 kubectl v1.31.0을 선택한 Ubuntu WSL2 터미널. 아래 명령은 체크섬을 통과할 때만 실제 리소스를 적용한다. 하나라도 실패하면 뒤의 && 명령을 중단한다. Windows/Ubuntu 파일 자동 동기화는 하지 않는다.

```bash
cd /home/user/onprem-lab/day10 &&
printf '%s\n' \
  '48f8bf06dd1d67dbffccba0330e24b0ea3b132730eef4b9a092068c499f0a741  00-namespace.yaml' \
  'b65fb5c9e7c8c34898a2c1775d9dcf4c94c62b93dc6ec038f447282dcc6ffa0e  10-deployment.yaml' \
  '6770b2a51d624c552cd384924aa5a1ac8d74da4071cdb1904eebbaafe7a1619b  20-service.yaml' |
sha256sum --check &&
kubectl --context k3d-onprem apply \
  -f 00-namespace.yaml \
  -f 10-deployment.yaml \
  -f 20-service.yaml &&
kubectl --context k3d-onprem -n ax-pilot \
  rollout status deployment/agent --timeout=120s &&
kubectl --context k3d-onprem -n ax-pilot get all -o wide
```

- 3개의 체크섬 OK, 리소스 생성/적용 성공, deployment successfully rolled out·2/2 및 Pod 두 개 1/1 Running을 기대한다. 실제 출력은 아직 받지 않았다. timeout 시 apply가 자동 취소되는 것은 아니며 실패 로그와 현재 리소스를 확인한다.
- 10-2 배포 성공·완료, Service 통신·분산 검증, 10-3 진행은 아직 아니다. 클러스터와 기존 자원은 유지한다.

### 2026-10-05 — 첫 배포 성공·10-2 완료
- [사용자 배포 출력](evidence/102-deploy-user-2026-10-05.txt): YAML 3개 체크섬 OK, Namespace ax-pilot·Deployment agent·Service agent created, rollout successfully rolled out를 확인했다. Windows에서 검토한 YAML과 Ubuntu 적용 파일이 일치한다.
- Pod agent-64c5d66bdf-d7qcb는 10.42.0.5·k3d-onprem-agent-0, agent-64c5d66bdf-stfrr는 10.42.2.5·k3d-onprem-server-0에 배치됐다. 둘 다 1/1 Running·RESTARTS 0·AGE 6s다.
- Deployment agent는 READY 2/2·UP-TO-DATE 2·AVAILABLE 2, ReplicaSet agent-64c5d66bdf는 DESIRED/CURRENT/READY 2다. 이미지 참조는 onprem-registry:5000/ax/agent:0.2.0이다. 실제 컨테이너 imageID나 pull 이벤트는 별도 조회하지 않았다.
- Service agent는 ClusterIP 10.43.162.127·8000/TCP·selector app=agent이며 EXTERNAL-IP는 없다. 클러스터 내부 접속 창구가 생성된 것이고 HTTP 전달·분산은 아직 시험하지 않았다.
- 이번에는 워커와 관리 노드에 각각 배치됐다. [K3s 구조 문서](https://docs.k3s.io/architecture)의 server도 kubelet·컨테이너 런타임을 실행하는 기본 구성과 부합한다. 관리 역할이 앱 배치를 자동 금지하는 것은 아니며 현재 출력으로 관리 노드에서 앱이 실행되는 것을 확인했다. 노드 taint 전체나 운영 환경의 배치 정책은 따로 조회하지 않았다.
- replicas=2만으로 서로 다른 노드 배치를 항상 보장하지 않는다. 이번 배치는 서로 다른 노드이지만 둘 다 같은 PC의 Docker 컨테이너이므로 물리 서버 장애 이중화 실험으로 해석하지 않는다.
- 보안 설정 설명: UID 10001로 non-root 실행, 루트 파일시스템 읽기 전용, /app/tmp는 emptyDir 쓰기 허용, 권한 상승 금지·capabilities ALL 제거·RuntimeDefault seccomp다. 이 설정을 담은 파일로 기동 성공을 확인했으며 컨테이너 내부 UID/capability를 별도 조회하거나 고객사 보안 심의를 통과한 것은 아니다.
- readiness가 지정된 Pod 두 개의 Ready 상태로 /healthz 준비 검사 통과를 확인했다. 관찰 시점은 AGE 6s여서 initialDelaySeconds=10인 liveness의 반복 검사나 장애 복구 시험 완료를 주장하지 않는다. 외부 DB/API 정상도 이 검사로 입증하지 않는다.
- 10-2 첫 배포 완료로 SESSION·PROGRESS·README·환경 기록을 갱신했다. 근거는 사용자 Ubuntu 출력이며 Codex는 Windows 기록과 출력 내용을 대조했다. 앱·클러스터·레지스트리·이미지를 유지하고 10-3 이후, Day 10 전체 완료, 자원 정리·커밋/push는 진행하지 않았다.

### 2026-10-05 — 10-3 시작·내부 Service 호출 안내
- 사용자 요청: "10-3으로 가자". PROGRESS·환경·README·SESSION·가이드 10-3을 읽고 내부 Service 호출부터 단계적으로 진행한다. port-forward 비교·종료는 후속 단계이며 10-4는 이번 범위 밖이다.
- 진단용 probe Pod를 ax-pilot에 생성한다. 이미지 nicolaka/netshoot:v0.13, restartPolicy Never, sleep 3600이다. 호스트 Docker에 이미지가 있어도 각 K3s 노드의 containerd에 자동 공유되는 것은 아니므로 이미지 다운로드가 발생할 수 있다. 생성 결과는 아직 미확인이다.
- 앱의 readiness/liveness probe와 진단 Pod 이름 probe는 다른 개념이라고 설명한다. 이번 probe는 클러스터 내부의 테스트 클라이언트다.
- 다음 사용자 Ubuntu WSL2 명령을 안내했다. 고정된 k3d-onprem context·ax-pilot Namespace를 사용하고 Pod Ready 후 DNS·Service HTTP를 조회한다. curl 실패 또는 .host 파싱 실패 시 내부 sh -e가 중단하도록 응답을 변수에 받은 뒤 jq -er로 추출한다. 각 요청을 별도로 보내고 응답 이름 8줄을 확인한다.

```bash
kubectl --context k3d-onprem -n ax-pilot run probe \
  --image=nicolaka/netshoot:v0.13 \
  --restart=Never --command -- sleep 3600 &&
kubectl --context k3d-onprem -n ax-pilot \
  wait --for=condition=Ready pod/probe --timeout=120s &&
kubectl --context k3d-onprem -n ax-pilot \
  exec probe -- nslookup agent.ax-pilot.svc.cluster.local &&
kubectl --context k3d-onprem -n ax-pilot exec probe -- sh -ec '
  for i in 1 2 3 4 5 6 7 8; do
    response=$(curl --noproxy "*" -fsS --max-time 5 http://agent:8000/healthz)
    printf "%s\n" "$response" | jq -er .host
  done
'
```

- 기대: Service FQDN이 10.43.162.127로 해석되고 앱 Pod 이름 8줄이 나온다. 두 이름이 나오면 이번 표본에서 분산을 관찰한 것이며 정확한 4:4 또는 두 이름 출현을 보장하지 않는다. 한 이름만 보이면 표본·서비스 대상 상태를 확인한 뒤 해석한다.
- 사용자 출력 대기 중이다. probe 기동·Service DNS/HTTP·분산 성공은 아직 기록하지 않는다. port-forward 실행·10-3 완료·10-4 이후도 미진행이다. 생성 후 probe는 sleep 3600으로 최대 약 1시간 실행되며 자동 삭제되지는 않는다.

### 2026-10-05 — Service DNS·HTTP 분산 확인 및 port-forward 안내
- [사용자 출력](evidence/103-service-user-2026-10-05.txt): probe created·condition met를 확인했다. 클러스터 DNS 서버 10.43.0.10:53이 agent.ax-pilot.svc.cluster.local을 10.43.162.127로 해석했고 앞서 Service IP와 일치한다.
- probe 내부에서 http://agent:8000/healthz를 각각 별도 curl로 8회 호출한 결과 stfrr Pod 5회·d7qcb Pod 3회 응답했다. 두 응답 이름은 10-2에서 생성한 Pod 이름과 일치한다. 이번 표본에서 Service DNS·HTTP 전달 및 두 대상에 대한 분산을 확인했다. 응답 본문 전체는 출력하지 않아 version/status 값의 직접 확인과는 구분한다.
- 5:3은 정상적인 관찰값이며 4:4 균등 분배를 보장하는 시험이 아니다. probe와 앱은 유지한다.
- [공식 port-forward 문서](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_port-forward/)에서 Service 지정 시 Pod 하나 선택, 선택 Pod 종료 시 세션 종료, :REMOTE_PORT의 로컬 자동 할당 및 --address 설정을 확인했다. 가이드의 고정 로컬 8000·백그라운드 &·kill %1 대신 루프백 자동 할당·전경 실행·Ctrl+C 종료를 사용한다.
- 사용자 실행 위치: 기존 Ubuntu WSL2 터미널. 아래 명령을 실행한 상태로 유지하고 Forwarding 출력 한 줄을 보내도록 안내했다. 아직 실제 할당 포트·포워딩 기동·대상 Pod·HTTP 결과는 미확인이다.

```bash
kubectl --context k3d-onprem -n ax-pilot \
  port-forward --address 127.0.0.1 svc/agent :8000
```

- 다음은 표시된 실제 포트에 다른 Ubuntu 터미널에서 HTTP 4회를 요청해 응답 Pod를 비교하는 단계다. 현재 포트를 추측하거나 포워딩 성공으로 기록하지 않는다. 비교 후 포워딩만 종료하고 probe·앱·클러스터는 유지할 계획이다. 10-3 완료·10-4 이후는 아직 아니다.

### 2026-10-05 — 10-3 port-forward 기동 확인·비교 호출 안내
- 확인 주체: 사용자 제공 Ubuntu WSL2 출력. Codex가 클러스터에서 직접 실행한 결과가 아니다. [증거](evidence/103-portforward-start-user-2026-10-05.txt).
- 기존 전경 명령에서 `Forwarding from 127.0.0.1:45537 -> 8000`을 확인했다. 자동 할당 로컬 포트는 45537이며 HTTP 응답은 아직 확인하지 않았다.
- 다른 Ubuntu 터미널에서 아래 명령으로 HTTP 4회 응답의 host를 조회하도록 안내한다. Service를 지정한 port-forward는 선택한 Pod 하나로 연결하므로 같은 세션에서는 동일 Pod 응답을 예상한다.

```bash
sh -ec '
  for i in 1 2 3 4; do
    response=$(curl --noproxy "*" -fsS --max-time 5 http://127.0.0.1:45537/healthz)
    printf "%s\n" "$response" | jq -er .host
  done
'
```

- 4회 성공 후 기존 포워딩 터미널에서 Ctrl+C로 종료하고 `ss -ltn '( sport = :45537 )'`로 리스너 해제를 확인하도록 안내한다. 두 명령의 결과는 대기 중이다. probe·앱·클러스터는 유지하며 10-3 완료·10-4 이후 진행은 아직 아니다.

### 2026-10-05 — 10-3 로컬 연결 실패·상태 점검 안내
- 확인 주체: 사용자 제공 새 Ubuntu WSL2 터미널 출력, 작업 디렉터리 ~. 앞서 안내한 sh -ec 루프의 첫 curl에서 `curl: (7) Failed to connect to 127.0.0.1 port 45537 after 0 ms: Couldn't connect to server`가 발생하고 프롬프트로 복귀했다. Pod 이름 출력은 없으며 4회 성공으로 기록하지 않는다.
- 로컬 TCP 연결 실패이며 앱의 HTTP 오류 응답은 아니다. 포워딩 종료·터미널 간 환경 차이 등의 원인은 아직 확인하지 않았다. 작업 디렉터리 차이 자체는 절대 URL 호출 실패 원인이 아니다.
- 기존 포워딩 터미널의 Forwarding 이후 출력과 프롬프트 복귀 여부를 요청한다. 새 Ubuntu 터미널에서 아래 읽기 전용 점검을 안내했으며 결과 대기 중이다.

```bash
ss -ltnp '( sport = :45537 )'
pgrep -af '[k]ubectl.*port-forward'
```

- 포워딩 재실행·Ctrl+C 종료·앱이나 클러스터 변경은 아직 안내하지 않았다. 내부 Service 검증 결과는 유지하며 10-3은 미완료다.

### 2026-10-05 — 10-3 프로세스 존재·45537 리스너 부재 확인
- 확인 주체: 사용자 제공 새 Ubuntu 터미널 출력. `ss -ltnp '( sport = :45537 )'`는 헤더만 출력했고, pgrep은 `2495 kubectl --context k3d-onprem -n ax-pilot port-forward --address 127.0.0.1 svc/agent :8000`을 출력했다.
- 해당 터미널에서 보이는 네트워크 공간에 45537 TCP 리스너가 없고 포워딩 명령의 프로세스는 존재한다. 프로세스 존재만으로 정상 포워딩을 판단하지 않는다. 기존 터미널 출력은 아직 받지 않았다.
- 원인 확인을 위해 기존 터미널의 최신 Forwarding/오류 출력과 프롬프트 복귀 여부를 다시 요청한다. 새 Ubuntu 터미널에서 아래 읽기 전용 점검을 안내하며 실행 결과는 대기 중이다. 재실행으로 할당 포트가 바뀌었는지, 프로세스 상태와 네트워크 공간이 다른지 등을 확인하되 원인으로 단정하지 않는다.

```bash
ps -p 2495 -o pid,ppid,stat,etime,args
ss -ltnp
readlink /proc/$$/ns/net /proc/2495/ns/net
```

- 클러스터·앱 변경이나 포워딩 종료/재실행은 하지 않았다. 10-3 미완료 상태를 유지한다.

### 2026-10-05 — 10-3 현재 포트 39827 확인·이전 포트 호출 원인 파악
- 확인 주체: 사용자 제공 1번 Ubuntu 터미널 출력. 동일한 자동 포트 명령의 최신 출력은 `Forwarding from 127.0.0.1:39827 -> 8000`이다.
- 앞선 curl 대상 45537과 현재 포워딩 포트 39827이 다르다. 45537 리스너 부재와 연결 실패는 이전 포트 호출로 설명된다. `:8000`은 로컬 포트 자동 할당이므로 실행마다 최신 Forwarding 출력을 사용해야 한다. 이전 프로세스 종료 경위는 확인하지 않았다.
- 앞서 제안한 ps·전체 ss·readlink 추가 진단은 실행 결과가 없으며 현재는 불필요하다. 1번 터미널을 유지하고 2번 Ubuntu 터미널에서 아래 재검증을 안내한다.

```bash
sh -ec '
  for i in 1 2 3 4; do
    response=$(curl --noproxy "*" -fsS --max-time 5 http://127.0.0.1:39827/healthz)
    printf "%s\n" "$response" | jq -er .host
  done
'
```

- 4회 성공 후 1번 터미널에서 Ctrl+C 종료 및 `ss -ltn '( sport = :39827 )'` 확인을 안내한다. HTTP 응답·종료 결과는 아직 대기 중이며 10-3 미완료다. 앱·probe·클러스터는 유지한다.

### 2026-10-05 — 10-3 port-forward 동일 Pod 응답 확인·종료 대기
- 확인 주체: 사용자 제공 2번 Ubuntu 터미널 출력. 127.0.0.1:39827/healthz 호출 4회 모두 `agent-64c5d66bdf-d7qcb`를 출력했다. 앞선 내부 Service 호출의 5:3 분산과 달리 이번 포워딩 세션은 하나의 Pod로 연결됨을 확인했다.
- 이어 실행한 `ss -ltn '( sport = :39827 )'`에서 `LISTEN 0 4096 127.0.0.1:39827 0.0.0.0:*`가 확인됐다. 이 시점에는 리스너가 남아 있으므로 포워딩 종료 완료로 기록하지 않는다.
- 다음 사용자 단계: 1번 포워딩 터미널에서 Ctrl+C를 눌러 프롬프트 복귀를 확인하고 같은 ss 명령을 다시 실행한다. 헤더만 출력되는지 확인 후 10-3 완료를 판단한다. 앱·probe·클러스터는 유지하고 10-4로 진행하지 않는다.

### 2026-10-05 — 10-3 포워딩 종료 확인·절 완료
- 확인 주체: 사용자 제공 1번 Ubuntu 터미널 출력. Ctrl+C 후 프롬프트로 돌아왔고 `ss -ltn '( sport = :39827 )'`는 헤더만 출력했다. 해당 로컬 TCP 리스너 해제를 확인했다. [비교·종료 증거](evidence/103-portforward-result-user-2026-10-05.txt).
- 완료 근거: probe Ready, Service FQDN이 10.43.162.127로 해석됨, 내부 HTTP 8회가 두 Pod에 5:3 분산, port-forward HTTP 4회는 d7qcb Pod로 고정, 포워딩 종료 후 39827 리스너 부재.
- 오류 학습: 자동 할당 포트를 사용하는 명령에서는 최신 Forwarding 출력을 기준으로 호출해야 한다. 이전 포트 45537 호출 실패는 현재 포트 39827 사용으로 해결됐다.
- 10-1·10-2·10-3 완료. 10-4 이후 및 Day 10 전체는 미완료다. 앱·클러스터 종료나 probe 삭제는 하지 않았다. 현재 probe 상태를 재조회한 것은 아니며 sleep 3600 종료 가능성은 다음 시작 시 확인한다.
- Codex는 Windows 학습 기록만 갱신했다. Ubuntu 직접 실행·두 사본 동기화·커밋·push는 하지 않았다.

### 2026-10-05 — 10-4 시작·자가 치유 전 현재 상태 조회 안내
- 사용자 요청: "다음을 진행하자". 10-4 진행 요청으로 이해하고 PROGRESS·환경 기록·Day 10 README/SESSION·가이드 10-4 및 Deployment YAML을 읽었다.
- 이번 순서: 앱 Pod 하나 삭제 후 재생성 확인, replicas 2→4→2 확인, 0.2.0→0.3.0 업데이트와 HTTP 관찰, 이력 조회와 0.2.0 롤백. 10-5나 노드 drain 실습은 진행하지 않는다.
- 핵심 설명: Deployment가 관리하는 ReplicaSet은 원하는 Pod 수 2개를 유지한다. Pod 하나를 삭제하면 같은 Pod를 되살리는 것이 아니라 새 Pod를 생성한다. 이후 관찰할 실습 목적이며 아직 재생성을 검증하지 않았다.
- 첫 단계는 Ubuntu WSL2의 읽기 전용 상태 확인이다. 새 터미널에서도 실습용 kubectl을 사용하도록 PATH를 선택하고 실제 배포/Pod 상태 및 probe의 종료 여부를 확인한다.

```bash
export PATH="$HOME/.local/share/onprem-lab/kubectl-v1.31.0/bin:$PATH" &&
hash -r &&
kubectl version --client &&
kubectl --context k3d-onprem -n ax-pilot get deployment agent -o wide &&
kubectl --context k3d-onprem -n ax-pilot get pods -o wide
```

- 사용자 출력 대기 중이다. 다음 단계는 확인된 앱 Pod 하나를 지정해 삭제하고 새 이름의 Pod 및 복제본 수 복구를 확인하는 것이다. 아직 삭제·scale·set image·rollout undo를 안내하거나 실행하지 않았다.

### 2026-10-05 — 10-4 사전 상태 확인·앱 Pod 하나 삭제 안내
- 확인 주체: 사용자 제공 Ubuntu WSL2 출력. kubectl v1.31.0/Kustomize v5.4.2, Deployment agent READY 2/2·UP-TO-DATE 2·AVAILABLE 2, 이미지 onprem-registry:5000/ax/agent:0.2.0을 확인했다.
- 앱 Pod agent-64c5d66bdf-d7qcb(10.42.0.5, agent-0), agent-64c5d66bdf-stfrr(10.42.2.5, server-0)는 모두 1/1 Running·RESTARTS 0·AGE 82m이다.
- probe는 0/1 Completed·RESTARTS 0·AGE 65m·10.42.2.6/server-0이다. 앞서 sleep 3600으로 생성한 진단 Pod의 종료와 부합한다. 현재 자가 치유 관찰에는 필요 없으므로 그대로 두고 롤링 업데이트 통신 관찰 전에 재준비한다.
- 다음 사용자 실행 위치: 같은 Ubuntu 터미널. 확인된 앱 Pod d7qcb 하나만 삭제하고 Deployment의 상태 및 새 Pod 이름/Ready를 확인하도록 안내한다. Deployment·Service·다른 앱 Pod 삭제나 강제 종료 옵션은 사용하지 않는다.

```bash
kubectl --context k3d-onprem -n ax-pilot \
  delete pod agent-64c5d66bdf-d7qcb --timeout=120s &&
kubectl --context k3d-onprem -n ax-pilot \
  rollout status deployment/agent --timeout=120s &&
kubectl --context k3d-onprem -n ax-pilot \
  get deployment,replicaset,pods -l app=agent -o wide
```

- 실행 결과는 아직 대기 중이다. 삭제된 이름 대신 새 Pod가 있고 기존 stfrr가 유지되며 Deployment/ReplicaSet/Pod 준비 수가 2로 복구되는지 확인한다. rollout 메시지만으로 재생성을 단정하지 않고 마지막 리소스 목록도 확인한다. 자가 치유 단계·10-4 완료·무중단 통신은 아직 검증하지 않았다.

### 2026-10-05 — 10-4 자가 치유 확인·복제본 4개 확장 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. d7qcb Pod 삭제 성공·rollout 성공, Deployment READY/AVAILABLE 2 및 ReplicaSet agent-64c5d66bdf DESIRED/CURRENT/READY 모두 2를 확인했다. 이미지는 0.2.0 그대로다.
- 새 Pod agent-64c5d66bdf-7642s는 1/1 Running·RESTARTS 0·AGE 30s·IP 10.42.1.5·노드 agent-1이다. 기존 stfrr는 1/1 Running·RESTARTS 0·AGE 87m·IP 10.42.2.5·노드 server-0으로 유지됐다.
- 삭제된 Pod는 agent-0에 있었고 새 Pod는 agent-1에 배치됐다. 이는 기존 Pod 이동/컨테이너 재시작이 아니라 같은 ReplicaSet의 새 Pod 생성이다. 재생성 및 원하는 수 2개 복구를 확인했지만 이 과정의 HTTP 무중단 여부는 측정하지 않았다.
- 다음 사용자 실행 위치: 같은 Ubuntu 터미널. 아래 명령은 앱 복제본 수를 2에서 4로 변경한다. 노드 수나 이미지 버전은 바꾸지 않는다. 가이드의 고정 sleep 8 대신 rollout status와 최종 목록으로 준비 상태를 확인한다.

```bash
kubectl --context k3d-onprem -n ax-pilot \
  scale deployment/agent --replicas=4 &&
kubectl --context k3d-onprem -n ax-pilot \
  rollout status deployment/agent --timeout=120s &&
kubectl --context k3d-onprem -n ax-pilot \
  get deployment,replicaset,pods -l app=agent -o wide
```

- 4개 확장 실행 결과는 대기 중이다. Deployment 4/4·ReplicaSet 4/4·앱 Pod 네 개 준비를 확인한 뒤 2개 복원을 별도로 안내한다. YAML 파일은 수정하지 않았다. probe 재준비·업데이트·롤백·10-4 완료는 아직이다.

### 2026-10-05 — 10-4 복제본 4개 확장 확인·2개 복원 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. scale 성공, 가용 복제본 2/4→3/4 후 rollout 성공을 확인했다. Deployment READY/UP-TO-DATE/AVAILABLE 모두 4, ReplicaSet agent-64c5d66bdf DESIRED/CURRENT/READY 모두 4다. 이미지는 0.2.0으로 유지됐다.
- 기존 7642s(10.42.1.5/agent-1), stfrr(10.42.2.5/server-0)에 kjbqb(10.42.1.6/agent-1), zqnxs(10.42.0.6/agent-0)가 추가됐다. 네 Pod 모두 1/1 Running·RESTARTS 0이다. 새 두 Pod의 AGE는 6s였다. 노드 확장이 아니라 Pod 수평 확장을 확인했다.
- 다음 사용자 실행 위치: 같은 Ubuntu 터미널. 아래 명령으로 목표 복제본을 다시 2로 변경한다. 제거할 Pod 이름은 직접 지정하지 않으며 어떤 두 Pod가 남을지 미리 단정하지 않는다.

```bash
kubectl --context k3d-onprem -n ax-pilot \
  scale deployment/agent --replicas=2 &&
kubectl --context k3d-onprem -n ax-pilot \
  rollout status deployment/agent --timeout=120s &&
kubectl --context k3d-onprem -n ax-pilot \
  get deployment,replicaset,pods -l app=agent -o wide
```

- 2개 복원 실행 결과는 아직 대기 중이다. 축소 직후 목록에 Terminating Pod가 남을 수 있으며 출력으로 상태를 확인한다. YAML 파일은 수정하지 않았다. probe 재준비·업데이트·롤백·10-4 전체 완료는 아직이다.

### 2026-10-05 — 10-4 복제본 2개 복원 확인·초과 Pod 종료 관찰
- 확인 주체: 사용자 제공 Ubuntu 출력. replicas=2 scale 및 rollout 성공, Deployment READY/UP-TO-DATE/AVAILABLE 모두 2, ReplicaSet DESIRED/CURRENT/READY 모두 2를 확인했다. 이미지는 0.2.0 그대로다.
- stfrr(10.42.2.5/server-0)와 zqnxs(10.42.0.6/agent-0)는 1/1 Running이다. 7642s(10.42.1.5/agent-1)와 kjbqb(10.42.1.6/agent-1)는 1/1 Terminating이다. 네 행 모두 RESTARTS 0이며 종료 중 두 행이 남아 있다고 목표 복제본이 4인 것은 아니다.
- 원하는 복제본 2개 복원은 확인했지만 초과 Pod 두 개의 삭제 완료는 아직 확인하지 않았다. 같은 Ubuntu 터미널에서 아래 읽기 전용 대기/조회를 안내한다. 추가 삭제나 강제 종료 명령이 아니다.

```bash
kubectl --context k3d-onprem -n ax-pilot wait --for=delete \
  pod/agent-64c5d66bdf-7642s \
  pod/agent-64c5d66bdf-kjbqb --timeout=120s &&
kubectl --context k3d-onprem -n ax-pilot \
  get deployment,replicaset,pods -l app=agent -o wide
```

- 결과 대기 중이다. 종료가 제한 시간 안에 끝나지 않으면 상태/이벤트를 진단하며 무조건 강제 삭제하지 않는다. 정리 확인 후 Completed 상태 probe를 다시 준비하고 롤링 업데이트 통신 관찰로 이어 간다. 업데이트·롤백·10-4 전체 완료는 아직이다.

### 2026-10-05 — 10-4 축소 정리 완료·롤링 업데이트용 probe 재준비 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. wait --for=delete 이후 &&로 연결된 조회가 실행됐고 앱 Pod 목록에서 7642s/kjbqb가 사라졌다. wait 자체의 성공 메시지는 출력되지 않았지만 명령 연결과 최종 목록으로 삭제 완료를 확인했다.
- Deployment READY/UP-TO-DATE/AVAILABLE 및 ReplicaSet DESIRED/CURRENT/READY 모두 2, 이미지 0.2.0이다. 남은 stfrr(10.42.2.5/server-0, AGE 110m), zqnxs(10.42.0.6/agent-0, AGE 21m)는 모두 1/1 Running·RESTARTS 0이다. 자가 치유와 확장/축소 단계의 상태 확인을 마쳤다. HTTP 연속성은 아직 측정하지 않았다.
- Windows agent/app.py를 읽어 /healthz 응답이 status/version/host를 제공함을 확인했다. 이것은 소스 확인이며 실행 중 응답의 확인과 구분한다.
- 다음 사용자 실행 위치: 같은 Ubuntu 터미널. 마지막 확인에서 Completed였던 진단 Pod probe만 삭제·재생성하고 Service의 업데이트 전 응답을 확인하도록 안내한다. 앱 Deployment·이미지·복제본은 변경하지 않는다.

```bash
kubectl --context k3d-onprem -n ax-pilot \
  delete pod probe --timeout=120s &&
kubectl --context k3d-onprem -n ax-pilot run probe \
  --image=nicolaka/netshoot:v0.13 \
  --restart=Never --command -- sleep 3600 &&
kubectl --context k3d-onprem -n ax-pilot \
  wait --for=condition=Ready pod/probe --timeout=120s &&
kubectl --context k3d-onprem -n ax-pilot exec probe -- \
  curl --noproxy '*' -fsS --max-time 5 \
  -w '\nHTTP %{http_code}\n' http://agent:8000/healthz
```

- probe 재생성·Ready·HTTP 200/status ok/version 0.2.0 확인 결과는 대기 중이다. 이후 업데이트 중 HTTP 응답을 관찰하며 0.3.0으로 변경하는 단계를 별도로 안내한다. 현재 set image·업데이트 이력·롤백은 실행하지 않았다.

### 2026-10-05 — 10-4 probe 준비 확인·롤링 업데이트 관찰 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. 기존 probe 삭제·새 probe 생성·Ready 성공 및 Service /healthz 응답 status=ok, version=0.2.0, host=agent-64c5d66bdf-stfrr, HTTP 200을 확인했다.
- 다음 사용자 실행 위치: 같은 Ubuntu 터미널. 아래 명령 묶음은 진단 Pod에서 HTTP 60회를 요청하는 동시에 앱 이미지를 0.3.0으로 바꾼다. 관찰 프로세스 PID를 저장해 해당 작업의 종료 코드를 기다리고 이미지 변경/rollout 실패도 따로 보존한다. Pod 수 목표는 2로 유지한다.
- 가이드의 30회 단순 파이프 대신 60회·요청 후 1초 간격·curl 2초 제한·HTTP/JSON 실패 집계를 사용한다. 정상 응답 시 약 1분, timeout이 있으면 더 길다. 실패를 숨기지 않으며 최종 SUMMARY와 UPDATE_EXIT/MONITOR_EXIT를 확인한다.

```bash
(
  kubectl --context k3d-onprem -n ax-pilot exec probe -- sh -c '
    ok=0; fail=0
    for i in $(seq 1 60); do
      if body=$(curl --noproxy "*" -fsS --max-time 2 http://agent:8000/healthz) &&
         version=$(printf "%s\n" "$body" | jq -er .version); then
        printf "%02d OK version=%s\n" "$i" "$version"
        ok=$((ok + 1))
      else
        printf "%02d FAIL\n" "$i"
        fail=$((fail + 1))
      fi
      sleep 1
    done
    printf "SUMMARY success=%s failure=%s\n" "$ok" "$fail"
    [ "$fail" -eq 0 ]
  ' &
  monitor_pid=$!
  sleep 3
  update_rc=0
  kubectl --context k3d-onprem -n ax-pilot set image deployment/agent \
    agent=onprem-registry:5000/ax/agent:0.3.0 &&
  kubectl --context k3d-onprem -n ax-pilot \
    rollout status deployment/agent --timeout=120s || update_rc=$?
  monitor_rc=0
  wait "$monitor_pid" || monitor_rc=$?
  printf "UPDATE_EXIT=%s MONITOR_EXIT=%s\n" "$update_rc" "$monitor_rc"
  kubectl --context k3d-onprem -n ax-pilot \
    get deployment,replicaset,pods -l app=agent -o wide &&
  [ "$update_rc" -eq 0 ] && [ "$monitor_rc" -eq 0 ]
)
```

- 실행 결과는 아직 대기 중이다. 기대값은 0.2.0에서 0.3.0으로 응답 전환, success=60/failure=0, 두 종료 코드 0, 최종 이미지 0.3.0 및 두 새 Pod 준비다. 응답 비율은 고정하지 않는다. 60회 샘플 성공을 모든 요청/모든 상황의 무중단 보장으로 일반화하지 않으며 관찰 종료보다 rollout이 늦으면 전체 전환 구간 관찰로 단정하지 않는다.
- 기존 YAML 파일은 수정하지 않았다. 실제 이미지 변경 성공·업데이트 이력 조회·롤백·10-4 완료는 아직 확인하지 않았다. 오류가 있으면 동일 업데이트를 무조건 재실행하지 말고 출력을 확인하도록 안내한다.

### 2026-10-05 — 10-4 롤링 업데이트 성공·이력/롤백 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. [요약 증거](evidence/104-rollout-user-2026-10-05.txt). 이미지 변경·rollout 성공, SUMMARY success=60 failure=0 및 UPDATE_EXIT=0 MONITOR_EXIT=0을 확인했다.
- 요청 01~09, 12, 14는 0.2.0으로 총 11회, 10~11, 13, 15~60은 0.3.0으로 총 49회 응답했다. 이미지 변경 전 3회 응답이 있었고 rollout 성공 메시지는 요청 14와 15 사이에 있다. 관찰은 업데이트 전부터 완료 이후까지 이어졌다. 혼합 버전 응답은 교체 중 양 버전 Pod가 응답한 관찰값이며 롤백 발생으로 해석하지 않는다.
- 관찰한 60회의 HTTP/버전 파싱은 모두 성공했다. 이 결과를 샘플 사이의 모든 요청이나 모든 환경의 무중단 보장으로 일반화하지 않는다.
- 최종 Deployment agent 이미지 0.3.0, READY/UP-TO-DATE/AVAILABLE 모두 2. 구 ReplicaSet agent-64c5d66bdf(0.2.0)는 0/0/0, 새 agent-7f87967cf6(0.3.0)는 2/2/2다.
- 새 Pod agent-7f87967cf6-jlrdl(10.42.2.8/server-0, AGE 56s), agent-7f87967cf6-wz225(10.42.1.7/agent-1, AGE 50s)는 모두 1/1 Running·RESTARTS 0이다. 구버전 앱 Pod는 최종 목록에 없다.
- 다음 사용자 실행 위치: 같은 Ubuntu 터미널. 이력을 조회하고 직전 배포로 롤백한 뒤 준비 상태와 Service의 실제 응답을 확인한다. 이 실습에서 확인된 직전 앱 버전은 0.2.0이며 실제 revision 번호는 아직 조회하지 않았다.

```bash
kubectl --context k3d-onprem -n ax-pilot \
  rollout history deployment/agent &&
kubectl --context k3d-onprem -n ax-pilot \
  rollout undo deployment/agent &&
kubectl --context k3d-onprem -n ax-pilot \
  rollout status deployment/agent --timeout=120s &&
kubectl --context k3d-onprem -n ax-pilot \
  get deployment,replicaset,pods -l app=agent -o wide &&
kubectl --context k3d-onprem -n ax-pilot exec probe -- \
  curl --noproxy '*' -fsS --max-time 5 \
  -w '\nHTTP %{http_code}\n' http://agent:8000/healthz
```

- 롤백 실행 결과 대기 중이다. 기대값은 Deployment 이미지 0.2.0·2개 준비 및 Service 응답 status ok/version 0.2.0/HTTP 200이다. 종료 중 신버전 Pod가 남는지 최종 목록도 확인한다. 오류가 나면 undo를 무조건 반복하지 않고 출력부터 확인하도록 안내한다. 롤백·10-4 전체 완료·10-5 진행은 아직 아니다.

### 2026-10-05 — 10-4 롤백 성공·교체된 Pod 종료 확인 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. rollout history는 REVISION 1/2 및 각각 CHANGE-CAUSE <none>을 표시했다. rolled back 및 rollout 성공 메시지를 확인했다. 롤백 이후 revision 번호는 아직 조회하지 않았으므로 추정해 기록하지 않는다.
- Deployment agent는 이미지 0.2.0으로 복원됐고 READY/UP-TO-DATE/AVAILABLE 모두 2다. ReplicaSet agent-64c5d66bdf는 2/2/2, agent-7f87967cf6(0.3.0)는 0/0/0이다.
- 0.2.0 Pod agent-64c5d66bdf-pwrhg(10.42.0.7/agent-0, AGE 11s)와 agent-64c5d66bdf-rslwh(10.42.1.8/agent-1, AGE 6s)는 1/1 Running·RESTARTS 0이다. 이전 버전 템플릿으로 새 Pod가 생성된 것이며 과거 Pod 이름 자체를 복구한 것은 아니다.
- Service /healthz 응답은 status=ok, version=0.2.0, host=agent-64c5d66bdf-rslwh, HTTP 200이다. 롤백 후 단일 요청의 정상 응답을 확인했으며 롤백 과정 전체의 연속 HTTP 성공을 측정한 것은 아니다.
- 교체된 0.3.0 Pod jlrdl(10.42.2.8/server-0), wz225(10.42.1.7/agent-1)는 여전히 Terminating이다. 롤백 성공과 별도로 최종 정리 확인을 위해 같은 Ubuntu 터미널에서 아래 대기/조회를 안내한다.

```bash
kubectl --context k3d-onprem -n ax-pilot wait --for=delete \
  pod/agent-7f87967cf6-jlrdl \
  pod/agent-7f87967cf6-wz225 --timeout=120s &&
kubectl --context k3d-onprem -n ax-pilot \
  get deployment,replicaset,pods -l app=agent -o wide
```

- 종료 확인 결과 대기 중이며 추가 delete나 undo는 수행하지 않는다. 0.2.0 앱 Pod 두 개만 남는지 확인한 뒤 10-4를 마무리한다. 앱·클러스터·probe는 유지하고 10-5는 아직 진행하지 않는다.

### 2026-10-05 — 10-4 교체 Pod 정리 확인·절 완료
- 확인 주체: 사용자 제공 Ubuntu 출력. wait --for=delete 이후 &&로 연결된 최종 조회가 실행됐고 jlrdl/wz225는 앱 Pod 목록에서 사라졌다. [롤백·최종 정리 증거](evidence/104-rollback-user-2026-10-05.txt).
- 최종 Deployment agent는 이미지 onprem-registry:5000/ax/agent:0.2.0, READY/UP-TO-DATE/AVAILABLE 모두 2다. ReplicaSet agent-64c5d66bdf는 2/2/2이고 agent-7f87967cf6(0.3.0)는 0/0/0으로 보존됐다.
- 남은 앱 Pod agent-64c5d66bdf-pwrhg(10.42.0.7/agent-0, AGE 6m1s), agent-64c5d66bdf-rslwh(10.42.1.8/agent-1, AGE 5m56s)는 모두 1/1 Running·RESTARTS 0이다. Terminating 앱 Pod는 최종 목록에 없다.
- 10-4 완료 근거: 삭제한 앱 Pod의 새 Pod 대체, 복제본 2→4→2 및 초과 Pod 정리, 0.3.0 업데이트 전/중/후 관찰한 HTTP 60회 성공·실패 0, 이력 조회·0.2.0 롤백·HTTP 200 및 교체 Pod 정리를 확인했다. 롤백 과정의 연속 HTTP 요청이나 노드 drain은 검증하지 않았다.
- 10-1~10-4 완료이며 10-5 이후·Day 10 전체는 미완료다. 앱·클러스터·레지스트리·이미지와 probe는 유지한다. probe의 현재 상태는 이번 최종 조회에서 재확인하지 않았으며 다음 절 시작 시 확인한다.
- Codex는 Windows 기록과 증거 파일만 갱신했다. Ubuntu 직접 실행·두 사본 동기화·커밋·push는 수행하지 않았다.

### 2026-10-05 — 10-5 시작·무응답 복구 실습 전 조회 안내
- 사용자 요청: "다음으로 가자". 10-4 완료 후 10-5 진행 요청으로 이해했다. PROGRESS·환경·Day 10 README/SESSION·가이드 10-5·Deployment YAML과 agent/app.py의 실습용 동작을 확인했다.
- Windows 소스 확인: /_lab/hang은 _hang 플래그를 켜고 최초 호출에 hang=true를 반환한다. 이후 GET 요청은 3600초 대기해 /healthz도 무응답이 된다. 프로세스 시작 시 플래그는 false다. 이는 소스 확인이며 아직 실행 중 이미지에 장애를 주입한 결과가 아니다.
- YAML의 readiness는 /healthz·주기 5초, liveness는 /healthz·주기 10초·timeout 3초·failureThreshold 3이다. 실제 클러스터 설정도 조회 후 확인한다. 가이드의 sleep 50만으로 복구를 단정하지 않으며 실제 재시작 횟수·상태·이벤트 및 HTTP로 판단할 계획이다.
- 개념 설명: 10-4는 삭제한 Pod를 새 Pod로 대체했고, 이번에는 같은 Pod 안의 컨테이너 재시작을 확인한다. readiness는 트래픽 수신 준비 여부, liveness는 컨테이너 재시작 판단에 사용된다. 실제 실패 순서/이벤트는 출력으로 확인하기 전 단정하지 않는다.
- 첫 단계 사용자 실행 위치: 실습용 kubectl v1.31.0을 선택했던 같은 Ubuntu 터미널. 아래는 읽기 전용 조회다.

```bash
kubectl --context k3d-onprem -n ax-pilot get deployment agent -o wide &&
kubectl --context k3d-onprem -n ax-pilot get pods -o wide &&
kubectl --context k3d-onprem -n ax-pilot get deployment agent -o json |
  jq '.spec.template.spec.containers[] | {name, image, readinessProbe, livenessProbe}'
```

- 결과 대기 중이다. 앱 두 개 Ready·probe Running·실제 헬스체크 설정을 확인한 다음 앱 Pod 하나의 IP를 지정해 장애를 주입할 계획이다. Service 주소로 무응답 요청을 반복하거나 두 앱에 동시에 장애를 주입하지 않는다. 현재 장애 주입·Pod 삭제·재시작·10-5 완료는 아직 아니다.

### 2026-10-05 — 10-5 사전 상태 확인·pwrhg 단일 Pod 무응답 관찰 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. Deployment agent 이미지 0.2.0·READY/UP-TO-DATE/AVAILABLE 모두 2. pwrhg(10.42.0.7/agent-0)와 rslwh(10.42.1.8/agent-1)는 1/1 Running·RESTARTS 0·AGE 13m이다. probe(10.42.2.7/server-0)는 1/1 Running·RESTARTS 0·AGE 23m이다.
- 실제 readinessProbe: HTTP /healthz/이름 http 포트, initialDelaySeconds 3, periodSeconds 5, timeoutSeconds 1, failureThreshold 3, successThreshold 1. 실제 livenessProbe: 같은 경로/포트, initialDelaySeconds 10, periodSeconds 10, timeoutSeconds 3, failureThreshold 3, successThreshold 1.
- 다음 사용자 실행 위치: 같은 Ubuntu 터미널. 대상을 pwrhg로 고정하며 확인된 Pod IP 10.42.0.7에만 실습용 /_lab/hang을 1회 호출한다. Service 주소로 호출하지 않고 rslwh에는 장애를 주입하지 않는다. UID를 먼저 출력해 추후 같은 Pod인지 비교한다.

```bash
kubectl --context k3d-onprem -n ax-pilot \
  get pod agent-64c5d66bdf-pwrhg \
  -o custom-columns='NAME:.metadata.name,UID:.metadata.uid,RESTARTS:.status.containerStatuses[0].restartCount' &&
kubectl --context k3d-onprem -n ax-pilot exec probe -- \
  curl --noproxy '*' -fsS --max-time 5 \
  -w '\nHTTP %{http_code}\n' http://10.42.0.7:8000/_lab/hang &&
kubectl --context k3d-onprem -n ax-pilot get pods -l app=agent -w
```

- 예상 최초 응답은 hang=true/HTTP 200이며 이는 장애 주입 응답이지 정상 healthz 응답이 아니다. watch에서 pwrhg READY 저하·RESTARTS 0→1·READY 1/1 복귀를 관찰할 계획이다. 상태 변화 순서를 실제 출력 전에 검증된 것으로 기록하지 않는다.
- pwrhg가 재시작 후 1/1 Running으로 복귀하면 Ctrl+C로 watch만 종료하고 UID/응답/관찰 출력을 보내도록 안내한다. 약 2분이 지나도 복구되지 않으면 watch를 종료하고 출력으로 진단하며 hang 재호출·Pod 삭제·수동 재시작은 하지 않는다. curl 오류가 나도 재호출하지 말고 출력부터 확인한다.
- 사용자 결과 대기 중이며 실제 장애 주입·자동 재시작·이벤트·HTTP 복구·10-5 완료는 아직 확인하지 않았다. 다음에는 동일 UID 여부·readiness/liveness/Killing 이벤트와 HTTP를 확인해 원인을 검증한다.

### 2026-10-05 — 10-5 probe 종료로 exec 실패·진단 Pod 재준비 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. pwrhg의 UID=8a3bd410-edb6-4026-a2d6-affb4d3a8e1d, RESTARTS=0을 확인했다.
- 다음 exec 명령은 `error: cannot exec into a container in a completed pod; current phase is Succeeded`로 실패했다. exec 대상은 probe이며 앱 pwrhg가 종료됐다는 의미가 아니다. 원격 curl이 실행되기 전에 거부돼 이번 /_lab/hang 요청은 전송되지 않았고 && 뒤의 watch도 실행되지 않았다.
- probe는 sleep 3600으로 생성했던 진단 Pod다. 현재 Succeeded는 해당 대기 명령의 정상 종료와 부합하지만 종료 시각/컨테이너 상세 상태를 별도로 조회하지는 않았다. 앱 장애나 liveness 실패로 기록하지 않는다.
- 다음 사용자 실행 위치: 같은 Ubuntu 터미널. 종료된 probe만 삭제·재생성한 뒤 Ready를 기다리고 대상 Pod의 /healthz를 직접 조회한다. 앱 Pod나 Deployment는 삭제/재시작하지 않으며 /_lab/hang도 호출하지 않는다.

```bash
kubectl --context k3d-onprem -n ax-pilot \
  delete pod probe --timeout=120s &&
kubectl --context k3d-onprem -n ax-pilot run probe \
  --image=nicolaka/netshoot:v0.13 \
  --restart=Never --command -- sleep 3600 &&
kubectl --context k3d-onprem -n ax-pilot \
  wait --for=condition=Ready pod/probe --timeout=120s &&
kubectl --context k3d-onprem -n ax-pilot exec probe -- \
  curl --noproxy '*' -fsS --max-time 5 \
  -w '\nHTTP %{http_code}\n' http://10.42.0.7:8000/healthz
```

- 재준비 및 status ok/version 0.2.0/host pwrhg/HTTP 200 확인 결과 대기 중이다. 정상 응답 확인 후 별도 단계로 무응답 주입을 다시 안내한다. 10-5는 미완료이며 10-6 이후로 진행하지 않는다.

### 2026-10-05 — 10-5 probe 재준비 확인·무응답 관찰 재안내
- 확인 주체: 사용자 제공 Ubuntu 출력. probe 삭제·생성·Ready 성공을 확인했다. 대상 IP 10.42.0.7의 /healthz는 status=ok, version=0.2.0, host=agent-64c5d66bdf-pwrhg, HTTP 200을 반환했다. 이전 exec 실패 뒤 진단용 Pod 접근과 대상 앱 정상 응답을 재확인했다.
- 다음 사용자 실행 위치: 같은 Ubuntu 터미널. pwrhg의 기준 상태를 재출력하고 이 Pod에만 hang 1회 호출 후 앱 두 개의 상태를 watch한다. 앞선 hang 시도는 exec 전에 실패했으므로 확인된 성공 호출을 반복하는 상황이 아니다.

```bash
kubectl --context k3d-onprem -n ax-pilot \
  get pod agent-64c5d66bdf-pwrhg \
  -o custom-columns='NAME:.metadata.name,UID:.metadata.uid,RESTARTS:.status.containerStatuses[0].restartCount' &&
kubectl --context k3d-onprem -n ax-pilot exec probe -- \
  curl --noproxy '*' -fsS --max-time 5 \
  -w '\nHTTP %{http_code}\n' http://10.42.0.7:8000/_lab/hang &&
kubectl --context k3d-onprem -n ax-pilot get pods -l app=agent -w
```

- 예상 관찰은 hang=true/HTTP 200 후 pwrhg READY 저하·재시작 증가·1/1 Running 복귀다. 복귀하면 Ctrl+C로 watch만 종료해 출력 전체를 보내도록 안내했다. 약 2분이 지나도 복구되지 않거나 curl 오류가 나면 hang을 반복하지 않고 현재 출력으로 진단한다.
- 사용자 실행 결과 대기 중이다. 아직 무응답 주입 성공이나 자동 복구로 기록하지 않는다. 이후 같은 UID인지, liveness/Killing 이벤트가 있는지, HTTP가 복구됐는지 확인할 계획이다. 10-5 미완료·10-6 미진행이다.

### 2026-10-05 — 10-5 무응답 주입·재시작/Ready 복귀 관찰 확인
- 확인 주체: 사용자 제공 Ubuntu 출력. 주입 직전 pwrhg UID=8a3bd410-edb6-4026-a2d6-affb4d3a8e1d, RESTARTS=0을 재확인했고 /_lab/hang에서 hang=true 및 HTTP 200을 받았다. [관찰 증거](evidence/105-hang-watch-user-2026-10-05.txt).
- watch 초기 pwrhg/rslwh는 1/1 Running·RESTARTS 0·AGE 5h26m이었다. 이후 pwrhg만 0/1 Running·RESTARTS 0, 이어 0/1 Running·RESTARTS 1(0s ago), 마지막 1/1 Running·RESTARTS 1(7s ago)·AGE 5h27m을 출력했다.
- 같은 Pod 이름에서 재시작 횟수 증가와 Ready 복귀를 확인했다. UID의 사후 일치·liveness/Killing 이벤트·재시작 후 HTTP는 아직 조회하지 않았다. 트래픽 분산 변화나 장애 중 무중단 HTTP를 측정한 것으로 기록하지 않는다. 사용자 출력에 Ctrl+C/프롬프트 복귀가 없어 watch 종료도 아직 확인하지 않았다.
- 다음 사용자 단계: watch가 실행 중이면 Ctrl+C로 조회만 종료하고 같은 Ubuntu 터미널에서 아래 읽기 전용 검증을 실행한다. 이벤트는 주입 전 확인한 UID로 범위를 제한한다.

```bash
kubectl --context k3d-onprem -n ax-pilot \
  get pod agent-64c5d66bdf-pwrhg \
  -o custom-columns='NAME:.metadata.name,UID:.metadata.uid,RESTARTS:.status.containerStatuses[0].restartCount' &&
kubectl --context k3d-onprem -n ax-pilot get events \
  --field-selector involvedObject.uid=8a3bd410-edb6-4026-a2d6-affb4d3a8e1d \
  --sort-by=.metadata.creationTimestamp &&
kubectl --context k3d-onprem -n ax-pilot exec probe -- \
  curl --noproxy '*' -fsS --max-time 5 \
  -w '\nHTTP %{http_code}\n' http://10.42.0.7:8000/healthz &&
kubectl --context k3d-onprem -n ax-pilot \
  get deployment,pods -l app=agent -o wide
```

- 기대 확인: 같은 UID·RESTARTS 1, readiness/liveness 실패와 liveness에 따른 Killing 메시지, 대상 pwrhg의 정상 HTTP 200/0.2.0, Deployment 2/2 및 다른 앱 Pod 정상 상태. 이벤트가 없거나 HTTP 오류가 나면 확인 가능한 범위만 기록하고 추가 진단한다. hang 재주입·Pod 삭제·수동 재시작 없이 결과를 기다린다. 10-5 미완료·10-6 미진행이다.

### 2026-10-05 — 10-5 동일 Pod liveness 재시작·HTTP 복구 확인·절 완료
- 확인 주체: 사용자 제공 Ubuntu 출력. Ctrl+C 뒤 후속 조회가 실행됐고 대상 UID는 주입 전과 동일한 8a3bd410-edb6-4026-a2d6-affb4d3a8e1d, RESTARTS는 1이다. [최종 검증 증거](evidence/105-recovery-user-2026-10-05.txt).
- 대상 UID의 이벤트에 readiness와 liveness의 /healthz timeout, `Container agent failed liveness probe, will be restarted`인 Killing, 이어 Pulled/Created/Started가 확인됐다. liveness 실패에 따른 컨테이너 재시작을 검증했다. 동일 UID이므로 Pod 교체와 구분된다.
- 이벤트 표의 LAST SEEN은 마지막 관찰 시점이므로 readiness/liveness 첫 실패 시각이나 모든 이벤트 발생 순서를 이 열만으로 단정하지 않는다. 앞선 watch로 Ready 저하 후 재시작·Ready 복귀를 확인했고 이번 이벤트로 실패/재시작 원인을 확인했다.
- 대상 10.42.0.7의 /healthz 응답은 status=ok, version=0.2.0, host=agent-64c5d66bdf-pwrhg, HTTP 200이다. Deployment agent 이미지 0.2.0·READY/UP-TO-DATE/AVAILABLE 모두 2다.
- 최종 pwrhg는 1/1 Running·RESTARTS 1(6m25s ago)·IP 10.42.0.7/agent-0, rslwh는 1/1 Running·RESTARTS 0·IP 10.42.1.8/agent-1이다. 둘 다 AGE 5h34m으로 표시됐다. 다른 앱 Pod를 변경하지 않았고 수동 삭제/재시작 없이 대상이 복구됐다.
- 10-5 완료 근거: 무응답 주입 성공, Ready 저하·재시작·Ready 복귀, 동일 UID 유지, liveness/Killing 이벤트, 대상 HTTP 200 및 Deployment 2/2를 확인했다. 장애 중 Service 라우팅 전환이나 연속 HTTP 무중단은 별도 측정하지 않았다.
- 10-1~10-5 완료, 10-6 이후 및 Day 10 전체는 미완료다. 앱·클러스터·probe는 유지한다. probe는 이번 exec에 사용됐지만 향후 sleep 3600 종료 가능성이 있으므로 재개 시 상태를 확인한다.
- Codex는 Windows 학습 기록과 증거만 갱신했다. Ubuntu 직접 실행·사본 동기화·커밋·push는 하지 않았다.

### 2026-10-05 — 10-6 시작·고장 예제 검토와 사본 확인 안내
- 사용자 요청: "좋아 시작하자". 앞선 10-6 설명에 대한 시작 요청으로 이해했다. PROGRESS·환경·Day 10 README/SESSION·가이드 10-6 및 broken YAML 5개와 Service 파일을 읽었다. day10/docs 아래 별도 AGENTS.md는 파일 검색에서 발견하지 못했다.
- Codex 직접 확인(Windows): 예제는 ax-pilot의 별도 Deployment b-imagepull, b-crashloop, b-pending, b-configerror, b-notready로 각각 replicas=1 및 app=b-* 레이블을 사용한다. 정상 Service 파일의 selector app=agent와 구분되며 정상 Deployment를 수정하지 않는다. 기존 소스/예제 파일은 변경하지 않았다.
- 예제 내용: 존재하지 않는 이미지 태그 9.9.9, 설정 누락 문구 출력 후 명시적 exit(1), requests cpu=64/memory=512Gi, agent-secret-typo 참조, readiness 경로 /health 오타다. crashloop 예제는 실제 파일 존재를 검사하는 코드가 아니라 오류 메시지와 종료를 재현하는 코드임을 구분한다. 실제 실패 원인은 배포 후 Events/로그로 확인한다.
- 이번 순서: 사본/현재 상태 확인 → 지정 예제 5개 배포 → 상태·Events·이전 컨테이너 로그 확인 → 해당 실습 리소스만 삭제 → 정상 앱 유지 확인. 가이드의 Harbor 자격 증명 생성은 설명용 예시라 실행하지 않으며 k9s 설치/실행도 현재 범위에 포함하지 않는다.
- Windows 예제 5개의 SHA-256을 직접 계산했다. 아래 Ubuntu 명령으로 사본 일치 및 기존 리소스를 확인하도록 안내한다. 이 명령은 파일 확인과 조회만 하며 클러스터를 변경하지 않는다.

```bash
cd /home/user/onprem-lab/day10 &&
printf '%s\n' \
  '11f2c1caf8bc8a866aa6fd605a40e6e1f332291f53871c2dc2ee14b0af98a39d  broken/01-imagepull.yaml' \
  '4fc29253a3b564ca9ab4bf85e0a1d87ad57488019c50441856a9825c1db38b2c  broken/02-crashloop.yaml' \
  'c669a881a09881c265661a6f1adb38b8980f751df1920b4d0db6b0489c36d548  broken/03-pending.yaml' \
  'e4bdbdbcabf034cabe39a70ed0253b89a09138d8f4779d952b36b620c808e1ad  broken/04-configerror.yaml' \
  '40d7eb66096e2eb9a0a974e5be10b718752c15b4493e32def75c991f8b654b51  broken/05-notready.yaml' |
sha256sum --check &&
kubectl --context k3d-onprem -n ax-pilot get deployment,pods -o wide
```

- 사용자 결과 대기 중이다. 체크섬 불일치가 있으면 차이를 확인하기 전 apply하지 않는다. 기존 b-* 리소스가 있으면 소유/상태를 확인하고 덮어쓰기나 삭제를 단정하지 않는다. 앱 정상 상태와 자료 일치를 확인한 뒤 실습 배포를 안내한다. 10-6 완료·Day 10 전체 완료는 아직 아니다.

### 2026-10-05 — 10-6 사본/사전 상태 확인·고장 예제 배포 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. broken/01-imagepull.yaml~05-notready.yaml의 지정 SHA-256 다섯 개가 모두 OK로 Windows 검토본과 일치했다.
- ax-pilot 전체 Deployment/Pod 조회에 정상 agent Deployment만 있고 READY/UP-TO-DATE/AVAILABLE 모두 2, 이미지 0.2.0이다. b-* Deployment/Pod는 없다. pwrhg는 1/1 Running·재시작 1(17m ago)·10.42.0.7/agent-0, rslwh는 1/1 Running·재시작 0·10.42.1.8/agent-1이다.
- probe는 1/1 Running·재시작 0·AGE 20m·IP 10.42.2.9/server-0으로 확인됐다. 앞선 probe 재생성 이전 IP 10.42.2.7과 구분한다. pwrhg의 재시작 1은 앞선 liveness 실습의 알려진 결과다.
- 다음 사용자 실행 위치: /home/user/onprem-lab/day10, Ubuntu WSL2. 검토·체크섬 확인한 파일 다섯 개만 명시해 apply한다. 정상 agent YAML이나 다른 파일을 함께 적용하지 않는다.

```bash
cd /home/user/onprem-lab/day10 &&
kubectl --context k3d-onprem -n ax-pilot apply \
  -f broken/01-imagepull.yaml \
  -f broken/02-crashloop.yaml \
  -f broken/03-pending.yaml \
  -f broken/04-configerror.yaml \
  -f broken/05-notready.yaml &&
sleep 60 &&
kubectl --context k3d-onprem -n ax-pilot get deployment,pods -o wide
```

- 실행 결과 대기 중이다. 고장 예제이므로 모든 Deployment의 rollout/Ready 성공을 기다리지 않는다. 60초는 첫 관찰 시점일 뿐 상태 수렴 보장이 아니다. ErrImagePull/ImagePullBackOff, Error/CrashLoopBackOff, Pending, CreateContainerConfigError, Running 0/1 등 실제 상태를 확인하고 이후 Events/로그로 원인을 검증한다.
- apply 자체가 오류라면 일부만 생성됐을 수 있으므로 무조건 반복하지 말고 출력을 확인한다. 원인 진단 전 이미지를 고치거나 Secret을 생성하지 않는다. 정상 앱은 유지하며 고장 예제 생성 성공·10-6 완료·정리는 아직 확인하지 않았다.

### 2026-10-05 — 10-6 고장 예제 생성·증상 확인
- 확인 주체: 사용자 제공 Ubuntu WSL2 출력. /home/user/onprem-lab/day10에서 위의 지정 파일 5개 apply, sleep 60, get deployment,pods -o wide를 실행했다. 다섯 Deployment가 모두 created이며 AGE 61s에 각각 READY 0/1, UP-TO-DATE 1, AVAILABLE 0이다.
- 관찰한 Pod 상태:

| Pod | READY / STATUS | 재시작 | IP / Node |
| --- | --- | --- | --- |
| b-imagepull-6c78958d45-mg7rs | 0/1 ErrImagePull | 0 | 10.42.2.10 / server-0 |
| b-crashloop-76f96fcdb-v9cp5 | 0/1 CrashLoopBackOff | 3 | 10.42.2.11 / server-0 |
| b-pending-7c74794f46-p2kgt | 0/1 Pending | 0 | 없음 / 없음 |
| b-configerror-5d86b95c76-zxhmd | 0/1 CreateContainerConfigError | 0 | 10.42.1.9 / agent-1 |
| b-notready-5cd84bc7c4-zts4l | 0/1 Running | 0 | 10.42.2.12 / server-0 |

- 정상 agent는 0.2.0 Deployment 2/2를 유지했다. pwrhg/rslwh는 모두 1/1 Running, 재시작 각각 1/0이며 probe도 1/1 Running(AGE 23m, 10.42.2.9/server-0)이다. 이번 출력만으로 HTTP 응답을 재확인한 것은 아니다.
- 다음은 이미지 다운로드 실패의 실제 Events 확인이다. YAML의 태그 9.9.9와 관찰한 ErrImagePull만으로 실패 메시지까지 단정하지 않는다. 앱 컨테이너가 시작되기 전 단계이므로 우선 describe를 사용한다.

```bash
kubectl --context k3d-onprem -n ax-pilot \
  describe pod b-imagepull-6c78958d45-mg7rs
```

- 위 describe는 안내만 했으며 출력 대기 중이다. 고장 예제 원인 진단·수정·정리 및 10-6 완료는 아직 아니다. Codex는 Windows 기록만 갱신했고 Ubuntu 실행·동기화·커밋·push는 하지 않았다.

### 2026-10-05 — b-imagepull Events 확인·HTTPS fallback 가설
- 확인 주체: 사용자 제공 Ubuntu 출력. 안내한 describe pod b-imagepull-6c78958d45-mg7rs 실행 결과를 확인했다. PodScheduled=True, Node=server-0/172.21.0.3, Pod phase=Pending, container Waiting/ImagePullBackOff, Ready=False, Restart Count=0, Container ID/Image ID 비어 있음이다. 노드 배정은 됐지만 이미지 다운로드 단계에서 멈춘 상태다.
- Events: 이미지 onprem-registry:5000/ax/agent:9.9.9를 Pulling한 뒤 HEAD https://onprem-registry:5000/v2/ax/agent/manifests/9.9.9 요청에서 `http: server gave HTTP response to HTTPS client` 발생. ErrImagePull 및 ImagePullBackOff/BackOff가 기록됐다. 이번 출력에는 manifest unknown/not found가 없다.
- Codex 문서 확인: https://docs.k3s.io/installation/private-registry 의 Default Endpoint Fallback 및 Troubleshooting Image Pulls에 따르면 mirror 시도 후 기본 HTTPS endpoint를 사용할 수 있고 kubelet 오류에는 마지막 실패만 표시될 수 있다. 따라서 'HTTP에서 없는 태그 조회 실패 후 HTTPS fallback'은 현재 가설이며 설정 누락 가능성과 구분해야 한다. TLS 검증 생략이나 레지스트리 변경을 안내하지 않는다.
- 다음 사용자 실행 위치: Ubuntu WSL2. 아래는 읽기 전용 진단이며 아직 결과를 받지 않았다. manifest 조회는 오류 본문을 보기 위해 curl -f를 사용하지 않는다. 설정은 인증 정보가 아닌 mirrors 구간만 조회한다.

```bash
docker exec k3d-onprem-server-0 \
  sed -n '/^mirrors:/,/^configs:/p' /etc/rancher/k3s/registries.yaml

curl --noproxy '*' -sS --max-time 10 \
  -H 'Accept: application/vnd.oci.image.index.v1+json, application/vnd.docker.distribution.manifest.list.v2+json, application/vnd.docker.distribution.manifest.v2+json' \
  -w '\nHTTP %{http_code}\n' \
  http://127.0.0.1:5001/v2/ax/agent/manifests/9.9.9

docker exec k3d-onprem-server-0 \
  grep -F 'ax/agent:9.9.9' /var/lib/rancher/k3s/agent/containerd/containerd.log | tail -n 20
```

- 실제 추가 조회 결과와 원인 확정은 대기 중이다. 정상 앱의 최신 상태는 이번 describe로 재확인하지 않았다. Windows 기록만 갱신했으며 실습 실행·설정 변경·리소스 삭제는 하지 않았다.

### 2026-10-05 — 이미지 태그 부재 확인·CrashLoop 진단 안내
- 확인 주체: 사용자 첨부 텍스트의 Ubuntu 실행 결과. 위의 읽기 전용 조회 세 가지를 실행했다. Codex는 첨부 파일과 Windows 학습 자료를 읽었으며 Ubuntu 명령을 직접 실행하지 않았다.
- registries.yaml의 mirrors에는 onprem-registry:5000 및 onprem-registry:5001이 모두 endpoint http://onprem-registry:5000으로 설정돼 있고 configs는 빈 객체다. HTTP mirror 설정 자체가 누락된 것은 아니다.
- 호스트 HTTP manifest 조회 결과: {"errors":[{"code":"MANIFEST_UNKNOWN","message":"manifest unknown","detail":{"Tag":"9.9.9"}}]}, HTTP 404. 해당 저장소의 9.9.9 태그 부재를 확인했다.
- server-0 containerd 발췌 로그는 12:49:22~12:55:05 UTC 사이 반복 PullImage 실패 및 최종 HTTPS 요청/HTTP 응답 오류를 보여 준다. 최초 HTTP 요청의 404 과정은 이 발췌에 없으므로 전체 순서를 직접 관측했다고 기록하지 않는다. mirror 설정·직접 HTTP 결과·앞서 확인한 공식 문서를 종합하면 태그 부재 후 HTTPS fallback으로 해석할 수 있다.
- 이미지 이름을 존재하는 태그로 바꾸는 것이 이 예제의 수정 방향이나 이번 실습은 증상 진단이므로 변경하지 않는다. TLS 검증 생략·레지스트리 재설정·클러스터 재생성은 하지 않는다. 마지막 정상 앱 조회는 2/2였으며 이번 결과로 최신 앱 상태를 재확인하지는 않았다.
- 다음 사용자 실행 위치: Ubuntu WSL2. b-crashloop의 컨테이너 종료 상태와 직전 종료된 컨테이너 로그를 확인한다. 아래 명령은 안내만 했으며 결과 대기 중이다.

```bash
kubectl --context k3d-onprem -n ax-pilot \
  describe pod -l app=b-crashloop

kubectl --context k3d-onprem -n ax-pilot \
  logs -l app=b-crashloop -c agent --previous --tail=50
```

- Windows 예제 소스는 설정 누락 문구 출력 후 sys.exit(1)을 실행한다. 실제 파일 존재를 검사하는 코드가 아닌 오류 재현용 코드다. 런타임 Exit Code 및 로그는 사용자 출력으로 확인할 예정이다. 10-6 전체 진단·정리는 아직 미완료이며 Windows 기록 외 파일 변경·Ubuntu 동기화·커밋·push는 하지 않았다.

### 2026-10-05 — CrashLoop 종료 원인·이전 로그 확인
- 확인 주체: 사용자 제공 Ubuntu WSL2 출력. 위 describe 및 logs --previous 명령을 실행했다. 대상 b-crashloop-76f96fcdb-v9cp5는 server-0/10.42.2.11에 있으며 이미지 0.2.0의 Image ID가 확인된다.
- Pod phase는 Running이지만 컨테이너는 Waiting/CrashLoopBackOff, Ready=False, Restart Count=6이다. Last State=Terminated, Reason=Error, Exit Code=1이며 직전 Started/Finished가 모두 2026-10-05 21:54:53 +0900이다. Pod phase Running만으로 앱 정상 동작을 판단할 수 없다.
- Events에는 이미지가 노드에 이미 존재한다는 Pulled, Created/Started, Back-off restarting failed container가 있다. 이번 출력은 레지스트리에서 새로 다운로드한 증거가 아니라 로컬 이미지로 컨테이너를 시작한 증거다.
- 이전 컨테이너 로그: `설정 파일 없음: /app/config/required.yaml`. 실제 Command는 `import sys; print('설정 파일 없음: /app/config/required.yaml'); sys.exit(1)`이다. 따라서 설정 파일 부재를 검사해 발생한 오류가 아니라 고정 문구 출력·명시적 실패 종료로 재현한 예제임을 확인했다. 파일을 생성하는 것만으로 이 명령의 종료 동작이 바뀌지는 않는다.
- 다음 사용자 실행 위치: Ubuntu WSL2. 아래 읽기 전용 조회를 안내하며 결과 대기 중이다. Windows 소스의 requests cpu=64/memory=512Gi와 실제 Requests 및 FailedScheduling 메시지를 비교한다. 아직 런타임 스케줄 실패 원인은 확정하지 않는다.

```bash
kubectl --context k3d-onprem -n ax-pilot \
  describe pod -l app=b-pending
```

- ImagePull/CrashLoop 두 예제 진단을 확인했고 나머지 세 예제 및 정리는 미완료다. 정상 앱 최신 상태는 이번 출력에 없다. Codex는 Windows 기록만 갱신했으며 실습 리소스 수정·삭제·Ubuntu 동기화·커밋·push는 하지 않았다.

### 2026-10-05 — 설명용 Python 코드를 Bash에 입력한 오류
- 사용자 제공 Ubuntu 출력: 설명용 `print('설정 파일 없음: /app/config/required.yaml')` 및 `sys.exit(1)`을 Bash 프롬프트에 입력했고 두 줄 모두 syntax error가 발생했다. Python 실행이나 Kubernetes 리소스 변경은 발생하지 않았다.
- Codex 설명에서 실행 명령과 예시 코드를 충분히 구분하지 못했음을 안내했다. Python 코드를 실행할 필요는 없으며 복구 작업도 필요하지 않다. 이후 설명용 코드는 실행 대상이 아님을 명확히 표시한다.
- 다음 사용자 실행 명령은 `kubectl --context k3d-onprem -n ax-pilot describe pod -l app=b-pending` 한 줄이다. 아직 Pending 진단 출력은 받지 않았으며 기존 진행 상태를 유지한다.

### 2026-10-05 — Pending 자원 부족 확인·ConfigError 진단 안내
- 확인 주체: 사용자 제공 Ubuntu WSL2 출력. `kubectl --context k3d-onprem -n ax-pilot describe pod -l app=b-pending` 실행 결과를 확인했다.
- b-pending-7c74794f46-p2kgt: Status Pending, Node 없음, IP 없음, PodScheduled=False. 컨테이너 Requests는 cpu=64, memory=512Gi다.
- Events는 FailedScheduling: `0/3 nodes are available: 3 Insufficient cpu, 3 Insufficient memory.` 및 `3 No preemption victims found for incoming pod.`다. 세 노드 모두 요청을 수용할 수 없고 선점으로 배치를 해결할 대상도 찾지 못했다.
- 의미: 이 Pod는 아직 실행되지 않았으며 64 CPU/512Gi를 실제 소비하고 있는 것이 아니다. 스케줄러가 요청량을 수용할 단일 노드를 찾지 못한 것이다. 단일 Pod의 요청량을 여러 노드에 나눠 배치하지 않는다. 적정 requests 또는 이를 수용할 노드가 수정 방향이나 실습에서는 변경하지 않는다.
- 다음은 b-configerror의 Environment 참조와 컨테이너 State/Events를 확인한다. Windows 예제는 agent-secret-typo의 LLM_API_KEY를 참조하지만 실제 런타임 오류는 아직 확인 전이다. 아래 한 줄만 Ubuntu에서 실행하도록 안내하며 출력 대기 중이다.

```bash
kubectl --context k3d-onprem -n ax-pilot describe pod -l app=b-configerror
```

- Secret 값 조회·생성 및 리소스 변경은 안내하지 않았다. 고장 예제 3개 진단 확인, 나머지 2개와 정리는 미완료다. 정상 앱 최신 상태는 이번 출력에 없으며 Codex는 Windows 기록만 갱신했다.

### 2026-10-05 — ConfigError 필수 Secret 부재 확인
- 확인 주체: 사용자 제공 Ubuntu WSL2 출력. 위 b-configerror describe 명령을 실행했다. 대상 b-configerror-5d86b95c76-zxhmd는 agent-1/172.21.0.4에 배정됐고 Pod IP는 10.42.1.9, PodScheduled=True다.
- Pod phase Pending, 컨테이너 Waiting/CreateContainerConfigError, Ready=False, Restart Count=0, Container ID/Image ID 비어 있음이다. Events에는 정상 Scheduled 및 이미지 0.2.0이 노드에 이미 있다는 Pulled가 있으나 컨테이너 Created/Started는 없다.
- Environment의 LLM_API_KEY는 Secret agent-secret-typo의 LLM_API_KEY 키를 Optional:false로 참조한다. Events의 `Error: secret "agent-secret-typo" not found`로 같은 Namespace에서 필요한 Secret을 찾지 못해 시작 설정을 구성하지 못함을 확인했다. Secret 내 특정 키 부재나 API 키 인증 실패로 해석하지 않는다.
- 앞선 b-pending과 Pod phase는 같아도 이번에는 노드 배정은 완료됐다. CrashLoop처럼 앱 실행 후 실패한 것도 아니다. 실무 수정 방향은 의도한 Secret 이름·Namespace 및 배포 순서를 확인하는 것이며 이번 실습에서는 Secret 생성이나 자격 증명 입력 없이 유지한다.
- 다음 사용자 실행 위치: Ubuntu WSL2. 아래 한 줄의 출력에서 State/Ready/Readiness/Events를 확인한다. Windows 예제는 /health 경로를 사용하지만 실제 런타임 응답은 아직 확인하지 않았다.

```bash
kubectl --context k3d-onprem -n ax-pilot describe pod -l app=b-notready
```

- 위 명령은 안내만 했으며 결과 대기 중이다. 고장 예제 4개 진단 확인, 마지막 NotReady 진단 및 정리는 미완료다. 정상 앱 최신 상태는 이번 출력에 없고 Codex는 Windows 기록만 갱신했다. 실습 리소스 변경·Ubuntu 동기화·커밋·push는 하지 않았다.

### 2026-10-05 — NotReady 경로 오류 확인·고장 리소스 정리 안내
- 확인 주체: 사용자 제공 Ubuntu WSL2 출력. 위 b-notready describe 실행 결과, b-notready-5cd84bc7c4-zts4l은 server-0/10.42.2.12에서 컨테이너 Running, Ready=False, Restart Count=0이다. 이미지 0.2.0으로 Created/Started됐다.
- Readiness는 http://:8000/health, delay=0s, timeout=1s, period=5s, success=1/failure=3이다. Events에 초기 connection refused 1건 및 HTTP statuscode 404 반복(x194 over 18m)이 있다. 초기 거부는 앱의 포트 수신 준비 전 검사와 부합하지만 지속되는 준비 실패의 증거는 반복 404다.
- Codex Windows 소스 확인: agent/app.py는 /healthz에서 200을 반환하고 미등록 경로는 404를 반환한다. broken/05-notready.yaml은 /health로 설정돼 있다. 런타임 readiness 경로와 404가 소스의 경로 오타와 일치한다. 해당 Pod에 /healthz를 직접 요청한 결과는 이번에 측정하지 않았다.
- 의미: 앱 프로세스 실행과 요청 처리 준비 판정은 다르다. readiness 실패 자체로 컨테이너를 재시작하지 않는다. 이 예제에는 livenessProbe가 없다. 또한 b-notready는 정상 Service의 app=agent selector와 맞지 않으므로 기존 Service에서 제외되는 원인을 readiness 하나로 설명하지 않는다.
- 다섯 예제 진단 확인: ImagePull=없는 태그, CrashLoop=명시적 exit(1), Pending=과도한 requests, ConfigError=필수 Secret 부재, NotReady=readiness 경로 오타/404. 수정 실습은 하지 않았고 다음은 합의된 고장 리소스 정리다.
- 다음 사용자 실행 위치: Ubuntu WSL2 /home/user/onprem-lab/day10. 지정 파일의 Deployment 및 종속 리소스만 foreground 삭제 후 전체 조회한다. 아래는 안내만 했으며 삭제 성공·정상 앱 유지 결과는 아직 받지 않았다.

```bash
cd /home/user/onprem-lab/day10 &&
kubectl --context k3d-onprem -n ax-pilot delete \
  -f broken/01-imagepull.yaml \
  -f broken/02-crashloop.yaml \
  -f broken/03-pending.yaml \
  -f broken/04-configerror.yaml \
  -f broken/05-notready.yaml \
  --cascade=foreground --wait=true --timeout=120s &&
kubectl --context k3d-onprem -n ax-pilot \
  get deployment,replicaset,pods,service -o wide
```

- 정상 agent·Service·probe·Namespace·클러스터·레지스트리 및 로컬 YAML은 삭제 대상이 아니다. 오류/시간 초과 시 출력부터 확인하며 강제 삭제하지 않는다. 10-6 정리 및 Day 10 전체 완료는 아직 아니고 k9s/다음 절로 넘어가지 않는다. Codex는 Windows 기록만 갱신했다.

### 2026-10-05 — 10-6 고장 리소스 정리 확인·절 완료
- 확인 주체: 사용자 제공 Ubuntu WSL2 출력. /home/user/onprem-lab/day10에서 위 지정 YAML 5개 delete --cascade=foreground --wait=true --timeout=120s 및 전체 조회를 실행했다. b-imagepull/b-crashloop/b-pending/b-configerror/b-notready Deployment가 모두 deleted이며 조회에 b-* Deployment/ReplicaSet/Pod가 없다.
- 정상 Deployment agent: image onprem-registry:5000/ax/agent:0.2.0, READY 2/2, UP-TO-DATE 2, AVAILABLE 2, AGE 8h. 활성 ReplicaSet agent-64c5d66bdf는 2/2/2, 이전 0.3.0 ReplicaSet agent-7f87967cf6는 0/0/0으로 유지된다.
- 정상 Pod pwrhg는 1/1 Running·재시작 1(40m ago)·10.42.0.7/agent-0, rslwh는 1/1 Running·재시작 0·10.42.1.8/agent-1이다. pwrhg 재시작 1은 10-5 liveness 실습에서 확인한 이력이다.
- probe는 1/1 Running·재시작 0·AGE 43m·10.42.2.9/server-0이다. Service agent는 ClusterIP 10.43.162.127:8000/TCP, selector app=agent로 유지된다. 이번 조회는 준비 상태/리소스 유지 확인이며 HTTP 요청을 새로 측정한 것은 아니다.
- 10-6 완료 근거: 고장 예제 사본 확인·5개 배포·각 상태와 원인 진단·해당 리소스 정리·정상 앱 및 Service 유지 확인. 개별 고장 수정/복구 실습은 하지 않았다. 10-1~10-6 완료이며 k9s 확인·Day 전체 정리·체크포인트 등은 미진행으로 Day 10 전체 미완료를 유지한다.
- Codex는 Windows 기록만 갱신했다. Ubuntu 직접 실행·동기화·추가 리소스 삭제·설치·커밋·push는 하지 않았다. 다음 절은 사용자 요청 전 시작하지 않는다.

### 2026-10-05 — k9s 시작·사전 확인 안내
- 사용자 요청: 다음 할 일로 k9s 확인을 안내한 후 "그럼 시작하자"라고 요청했다. PROGRESS·환경 기록·Day README/SESSION 및 가이드 k9s 항목을 읽었다. 10-1~10-6 완료를 유지한다.
- 다음 사용자 실행 위치: Ubuntu WSL2. k9s 실행 파일이 PATH에 있는지와 버전을 확인하고, 실습용 kubectl 1.31.0을 선택해 현재 Deployment/Pod를 조회한다. 아래는 안내만 했으며 실행 결과 대기 중이다.

```bash
if command -v k9s; then
  k9s version
else
  printf 'k9s: not found in PATH\n'
fi

export PATH="$HOME/.local/share/onprem-lab/kubectl-v1.31.0/bin:$PATH" &&
hash -r &&
kubectl version --client &&
kubectl --context k3d-onprem -n ax-pilot get deployment,pods -o wide
```

- k9s가 PATH에서 없다는 결과만으로 시스템 전체 미설치를 확정하지 않는다. 설치가 필요한 경우 플랫폼/설치 경로와 공식 배포물을 검토한 뒤 별도 단계로 안내한다. 이번에는 설치·k9s UI 실행·고장 예제 재배포·probe 삭제를 하지 않는다. Codex는 Windows 학습 기록만 갱신했다.

### 2026-10-05 — k9s 설치 확인·읽기 전용 첫 화면 안내
- 확인 주체: 사용자 제공 Ubuntu WSL2 출력. k9s 경로 /usr/local/bin/k9s, Version v0.32.5, Commit 1440643e8d1a101a38d9be1933131ddf5c863940, 빌드 날짜 2024-06-15T17:11:02Z다. kubectl v1.31.0/Kustomize v5.4.2도 확인했다. 추가 설치나 업그레이드는 필요하다고 판단하지 않았다.
- 정상 agent 0.2.0 Deployment READY 2/2·UP-TO-DATE 2·AVAILABLE 2다. pwrhg는 1/1 Running·재시작 1(54m ago)·10.42.0.7/agent-0, rslwh는 1/1 Running·재시작 0·10.42.1.8/agent-1이다. probe는 1/1 Running·AGE 57m·10.42.2.9/server-0이며 곧 sleep 3600이 종료될 수 있다.
- Codex 확인: 공식 https://k9scli.io/topics/commands/ 에서 --context, -n, -c pod, --readonly 및 종료 :q/Ctrl+C를 확인했다. v0.32.5 특정 소스 페이지는 웹 조회 실패로 읽지 못했다. 따라서 설치된 버전의 옵션 실행 성공은 아직 확인하지 않았으며 오류 시 k9s help로 확인한다.
- 다음 사용자 실행 위치: Ubuntu WSL2. 아래 한 줄로 대상 context/namespace와 Pod 뷰를 명시하고 변경 명령을 비활성화한다. 이는 k9s의 UI 동작 제한이며 계정 RBAC 권한을 변경하는 것은 아니다.

```bash
k9s --context k3d-onprem -n ax-pilot --readonly -c pod
```

- 첫 화면에서 context k3d-onprem·namespace ax-pilot, 정상 agent Pod 두 개의 READY 1/1을 확인하도록 안내했다. 사용자 화면 캡처 또는 표시 내용 대기 중이다. 종료는 k9s 안에서 :q 입력 후 Enter 또는 Ctrl+C이며 앱 종료와 클러스터 리소스 삭제는 다르다.
- k9s 조회 실습 완료는 아직 아니다. 옵션 오류 시 --readonly를 빼고 실행하지 않는다. Codex는 Windows 기록만 갱신했으며 Ubuntu 실행·추가 설치·고장 예제 재배포·probe 삭제·커밋·push는 하지 않았다.

### 2026-10-05 — k9s 첫 화면 캡처 확인·Describe 안내
- 확인 주체: 사용자 제공 이미지 k9s-1005.png. 원본 위치는 Windows의 별도 가이드 폴더 communications이며 프로젝트로 복사하거나 수정하지 않았다. Codex는 첨부 화면을 읽었고 현재 터미널을 직접 조작하지 않았다.
- 캡처에서 Context/Cluster=k3d-onprem, User=admin@k3d-onprem, K9s Rev=v0.32.5, K8s Rev=v1.30.4+k3s1, Pods(ax-pilot)[3]을 확인했다. 다른 버전 표시를 현재 설치 버전으로 해석하거나 업그레이드를 진행하지 않는다.
- pwrhg는 1/1 Running·재시작 1·10.42.0.7/agent-0, rslwh는 1/1 Running·재시작 0·10.42.1.8/agent-1이다. probe는 1/1 Running·재시작 0·AGE 59m·10.42.2.9/server-0이다. 첫 행 pwrhg가 선택돼 있고 상단에 d=Describe, l=Logs, y=YAML 안내가 보인다.
- 앞서 --readonly 실행을 안내했으며 이번 캡처로 k9s UI 접속 성공을 확인했다. 캡처 자체에는 실행 명령줄이 없으므로 플래그 적용 여부를 별도 검증한 것으로 기록하지 않는다.
- 다음 사용자 동작: k9s 화면 안에서 현재 선택된 pwrhg에 소문자 d를 누른다. Bash에 입력하거나 Enter를 누르는 명령이 아니다. Describe의 이미지·State/Ready·Restart Count·readiness/liveness 설정을 확인하고 화면을 보내도록 안내한다. 이전 화면으로 돌아가는 키는 Esc다.
- Describe 화면 확인은 아직 대기 중이다. 앱/클러스터 변경·추가 설치·probe 삭제 없이 Windows 기록만 갱신했다. k9s 전체 조회 실습 및 Day 10 전체 완료는 아직 아니다.

### 2026-10-05 — k9s Describe 확인·현재 로그 안내
- 확인 주체: 사용자 제공 pod_2.png 캡처. Describe(ax-pilot/agent-64c5d66bdf-pwrhg) 화면을 확인했다. 사용자 원본 이미지는 수정/복사하지 않았고 Codex가 터미널을 직접 조작하지 않았다.
- Node=agent-0/172.21.0.5, Pod IP=10.42.0.7, Controlled By=ReplicaSet/agent-64c5d66bdf, image=onprem-registry:5000/ax/agent:0.2.0이다. 현재 컨테이너 State=Running, Ready=True, Restart Count=1이며 Pod Conditions도 화면상 모두 True다.
- Last State=Terminated/Reason Error/Exit Code 137, 종료 시각 21:29:29 +0900이다. 현재 컨테이너 Started도 21:29:29다. 현재 상태와 이전 종료 이력을 구분한다. 앞서 10-5에서 liveness 실패에 따른 Killing 이벤트를 확인했으므로 해당 재시작 이력과 부합한다. 137만으로 메모리 부족/OOMKilled라고 단정하지 않는다. 이번 캡처에는 Events가 보이지 않는다.
- Requests cpu=100m/memory=128Mi, Limits cpu=1/memory=512Mi다. readiness/liveness 경로는 모두 /healthz이며 각각 period=5s/10s, timeout=1s/3s, failure=3이다. 표시된 URL의 http 포트 이름은 기존 Deployment의 이름 있는 포트 설정이며 경로 오류로 해석하지 않는다.
- 다음 사용자 동작: k9s에서 Esc로 Pod 목록으로 돌아와 pwrhg 선택을 확인한 뒤 소문자 l(영문 엘)을 누른다. 현재 컨테이너 로그 화면을 연 후 캡처를 보내도록 안내한다. 셸 명령이나 Enter 입력이 필요하지 않다. 이전 로그(p)는 이번 단계가 아니다.
- 현재 로그 화면 확인은 대기 중이다. 정상 앱/클러스터 변경 없이 Windows 기록만 갱신했고 k9s 전체 실습 및 Day 10 전체 완료로 기록하지 않는다.

### 2026-10-05 — k9s 현재 로그 확인·Deployment 조회 안내
- 확인 주체: 사용자 제공 k9s-l.png 캡처. Logs(ax-pilot/agent-64c5d66bdf-pwrhg:agent)[tail] 화면을 확인했다. Autoscroll=On, Wrap=Off이며 오른쪽 타임스탬프 일부가 잘려 있다. 보이지 않는 시간이나 전체 로그 내용을 추정하지 않는다.
- 화면에 보이는 JSON 로그는 event=request, method=GET, path=/healthz, status=200이 반복되며 ms는 주로 0, 일부 1이다. 현재 표시 범위에서 healthz 응답 성공을 확인했으며 모든 시간·모든 기능·Service 전체의 정상 동작을 보장하는 증거로 확대하지 않는다.
- 앞서 확인한 readiness 5초/liveness 10초의 /healthz 검사 설정과 부합하는 반복 요청이다. 로그에 요청 주체 구분이 없으므로 각 행을 특정 probe에 확정 대응하지 않는다. 애플리케이션 로그의 event=request와 Kubernetes Events는 서로 다른 기록임을 구분한다.
- 다음 사용자 동작: k9s에서 Esc로 Pod 목록에 돌아가 :deploy를 입력하고 Enter를 누른다. 이는 Bash 명령이 아닌 k9s 내부 화면 전환이다. Deployment agent의 READY/UP-TO-DATE/AVAILABLE 표시를 확인할 예정이다. 아직 화면 결과는 받지 않았다.
- Codex는 Windows 기록만 갱신했으며 원본 캡처 수정·터미널 조작·클러스터 변경은 하지 않았다. Deployment/Service 화면 확인 및 k9s 실습 완료는 아직이다.

### 2026-10-05 — k9s Deployment 확인·Service 조회 안내
- 확인 주체: 사용자 제공 k9s-deploy.png 캡처. Context/Cluster k3d-onprem, Deployments(ax-pilot)[1] 화면에서 agent 한 개를 확인했다. READY=2/2, UP-TO-DATE=2, AVAILABLE=2, AGE=8h다.
- 의미: 원하는 복제본 2개에 대해 Ready 2개, 현재 Deployment Pod 템플릿을 반영한 복제본 2개, 가용 복제본 2개다. UP-TO-DATE는 외부 레지스트리의 가장 최신 릴리스라는 뜻이 아니다. 이번 화면에는 이미지 버전이 표시되지 않으며 앞선 Describe/CLI의 0.2.0 확인과 구분한다.
- 다음 사용자 동작: 현재 k9s 화면에서 :svc 입력 후 Enter를 눌러 Service 목록으로 전환한다. 셸 명령이 아니며 리소스 변경은 없다. agent의 Type/Cluster-IP/Ports를 확인할 예정으로 화면 결과 대기 중이다.
- Codex는 Windows 기록만 갱신했다. 원본 캡처 복사/수정·터미널 직접 조작·클러스터 변경은 하지 않았다. Service 조회와 k9s 종료 확인, Day 최종 정리/체크포인트는 아직이다.

### 2026-10-05 — Service 값 일치·k9s 종료 확인 및 조회 실습 완료
- 확인 주체: 사용자 텍스트 확인. Service 화면에 대해 "제대로 되고잇어"라고 답한 뒤, 안내한 TYPE=ClusterIP, CLUSTER-IP=10.43.162.127, PORT=8000/TCP와 일치하는지 확인하도록 요청했다. 사용자는 "값은 일치하고 이제 종료했어"라고 확인했다.
- Service 값과 k9s 종료는 사용자 진술로 확인했으며 이번 Service 화면 캡처나 종료 후 CLI 조회를 Codex가 직접 확인한 것은 아니다. k9s 종료는 UI 종료이며 클러스터/앱 리소스 삭제를 의미하지 않는다.
- k9s 조회 실습 완료: 기존 설치/버전 확인, 대상 context/namespace 접속, Pod 목록, d Describe, l 현재 로그, :deploy Deployment, :svc Service 및 종료. Pod/Describe/로그/Deployment는 사용자 캡처, Service/종료는 사용자 텍스트를 근거로 구분했다.
- 10-1~10-6 및 k9s 조회 완료. probe 최종 정리와 가이드 체크포인트 평가는 아직 미진행으로 Day 10 전체 미완료를 유지한다. 고장 리소스는 이미 삭제됐고 앱/Service/Namespace/클러스터/레지스트리는 유지한다. probe의 현재 phase는 이번에 재확인하지 않았다.
- 다음은 사용자 요청 후 probe 정리·정상 앱 유지 확인 및 이해도 점검이다. 이번 턴에는 삭제 명령을 안내하거나 직접 실행하지 않았다. Codex는 Windows 기록만 갱신했고 Ubuntu 동기화·커밋·push는 하지 않았다.

### 2026-10-05 — 사용자 최종 정리 요청·probe 삭제 안내
- 사용자 요청: "좋아 정리하자". 이번 정리 범위는 진단용 probe Pod 삭제 및 정상 앱/Service 유지 확인이다. 가이드 정리·체크포인트를 읽었으며 이미 삭제한 고장 예제를 다시 삭제하지 않는다.
- 다음 사용자 실행 위치: Ubuntu WSL2 터미널(k9s 종료 후). 아래는 안내만 했으며 실행 결과 대기 중이다. probe만 이름으로 지정하고 정상 종료를 기다린다. 이미 없으면 --ignore-not-found=true로 처리하며 API/권한 등 다른 오류는 숨기지 않는다.

```bash
kubectl --context k3d-onprem -n ax-pilot \
  delete pod probe --ignore-not-found=true --wait=true --timeout=120s &&
kubectl --context k3d-onprem -n ax-pilot \
  get deployment,pods,service -o wide
```

- 가이드의 --force/--grace-period=0 및 오류 출력 숨김은 사용하지 않는다. 시간 초과나 오류가 있으면 출력을 확인하고 무조건 강제 삭제하지 않는다. 정상 agent·Service·Namespace·클러스터·레지스트리·이미지와 로컬 파일은 삭제 대상이 아니다.
- 정리 성공·probe 부재는 아직 확인하지 않았다. 체크포인트 평가 및 Day 10 전체 완료도 아직이다. Codex는 Windows 기록만 갱신했고 Ubuntu 실행·동기화·커밋·push는 하지 않았다.

### 2026-10-05 — probe 삭제·정상 앱 유지 확인 및 최종 정리 완료
- 확인 주체: 사용자 제공 Ubuntu WSL2 출력. 위 probe 일반 삭제 및 전체 Deployment/Pod/Service 조회를 실행했다. `pod "probe" deleted`와 최종 목록의 probe 부재를 확인했다.
- Deployment agent는 image onprem-registry:5000/ax/agent:0.2.0, READY 2/2, UP-TO-DATE 2, AVAILABLE 2다. Pod는 agent-64c5d66bdf-pwrhg와 agent-64c5d66bdf-rslwh 두 개만 1/1 Running이며 재시작은 각각 1(71m ago)/0이다. IP/Node는 각각 10.42.0.7/agent-0, 10.42.1.8/agent-1이다.
- Service agent는 ClusterIP 10.43.162.127, 8000/TCP, selector app=agent로 유지된다. 이번 출력에서 새 HTTP 응답을 측정한 것은 아니다. 정상 앱과 Service 유지 및 진단 Pod 정리 결과를 확인했다.
- 10-1~10-6·k9s 조회·최종 리소스 정리 완료다. 이해도 체크포인트는 아직 시행하지 않았으므로 Day 10 전체 완료로 표시하지 않는다. 이후 사용자 요청으로 점검하며 Day 11을 임의로 시작하지 않는다.
- 고장 예제는 앞서 정리됐고 이번에는 probe만 삭제했다. 앱·Namespace·클러스터·레지스트리·이미지는 삭제하지 않았다. Codex는 Windows 기록만 갱신했으며 Ubuntu 직접 실행·동기화·커밋·push는 하지 않았다.

### 2026-10-05 — 체크포인트 6개 복습 해설
- 사용자 요청: 체크포인트 답변을 이해하기 쉽게 정리. Day 10 원문 및 Day 5의 의존 서비스 장애/무응답 장애 기록을 확인하고 Kubernetes·Broadcom·MetalLB·Red Hat 공식 자료를 참조했다. 실습 명령 실행 요청이 아닌 개념 설명 요청이다.
- 해설 요지: LoadBalancer 외부 IP는 연동 구현/설정이 필요하며 온프렘 자체가 불가능 조건은 아니다. MetalLB 또는 사내 LB와 Ingress Controller 연동 등을 구분한다. readiness는 요청 처리 가능 여부, liveness는 재시작 필요 여부를 판단한다. 현재 /healthz는 DB 상태를 검사하지 않아 DB 장애를 자동 판별하지 않는다.
- vSphere HA는 VM 단위 장애 복구, Deployment RollingUpdate는 앱 버전의 점진적 교체다. 롤링 업데이트 자체를 서버 장애 복구 기능이라고 설명하지 않으며 VM/앱 감시 기능의 설정 가능성과 무중단 보장 조건도 구분한다.
- CrashLoop 첫 진단은 describe pod 및 logs --previous다. 네트워크 외부 출발지는 Pod IP/노드 SNAT/egress IP/후단 NAT 등에 따라 달라 플랫폼팀 및 해당 방화벽 관측으로 확인한다. port-forward는 로컬 실행 세션 의존 및 선택 Pod 고정으로 운영 진입점과 구분한다.
- 명령 예시는 복습용 형식이며 현재 실행하도록 요청하지 않았다. 체크포인트 해설 제공은 완료했지만 사용자 독립 답변/평가 통과는 확인하지 않았다. 리소스나 실습 소스를 변경하지 않고 Windows 학습 기록만 갱신했다.

### 2026-10-05 — Day 10 기록 정리·PR 준비
- 사용자 요청: "Day10을 정리해서 github repo에 PR을 생성하자". 실행 위치는 Windows 프로젝트 사본이며 Ubuntu 실습 명령은 재실행하지 않았다.
- README를 단계별 결과·핵심 개념·장애 진단·체크포인트 답안·인수인계로 재구성했다. SESSION의 날짜별 이력은 보존하고 과거의 미완료 상태와 최종 상태를 구분했다.
- [진단·k9s·최종 정리 증거 요약](evidence/106-final-summary-user-2026-10-05.txt)을 추가했다. 사용자 출력/캡처/텍스트 확인을 출처로 표시했으며 Codex 직접 실습 검증으로 기록하지 않는다.
- Codex 직접 확인: 원격 fetch 후 main과 origin/main 차이 0/0, 열린 PR 없음. `codex/day10-results` 브랜치를 만들었다. 기존 `day09/SESSION.md` 수정은 보존하고 이번 PR 대상에서 제외한다.
- 문서 점검: 상대 링크 대상 272개 존재, `git diff --check` 통과, 지정 문서·증거의 일반적인 자격 증명 패턴 검색에서 일치 없음. 패턴 검사가 모든 비밀 노출을 보장해 탐지하는 것은 아니며 증거 내용도 검토했다.
- 변경 범위는 Day 10 기록·증거와 공통 진행/환경 기록이다. 실습 소스·가이드·셸 스크립트는 변경하지 않았고 런타임 테스트·컨테이너 실행·Ubuntu 동기화·main 병합은 하지 않았다.
- 커밋·push·PR 생성 결과는 성공을 확인한 뒤 별도로 기록한다. 다음 Day와 독립 이해도 평가는 미진행 상태를 유지한다.
