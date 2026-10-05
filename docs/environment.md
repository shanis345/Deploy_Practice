# 실습 환경

아래 Day 10 기록은 최신 결과부터 배치한 시점별 이력이다. 과거 항목의 “대기/미진행”은 당시 상태를 뜻한다. PR 정리 중 Ubuntu 환경을 재실행하거나 두 사본을 동기화하지 않았다.

## Day 10 최종 정리 완료 (2026-10-05)
- 사용자 출력에서 probe 삭제 및 부재를 확인했다. 정상 agent 0.2.0은 READY 2/2·UP-TO-DATE 2·AVAILABLE 2다. pwrhg(10.42.0.7/agent-0)와 rslwh(10.42.1.8/agent-1)는 모두 1/1 Running·재시작 각각 1/0이다.
- Service agent는 ClusterIP 10.43.162.127:8000/TCP, selector app=agent다. 고장 예제와 probe는 정리됐고 앱·Namespace·클러스터·레지스트리·이미지는 유지한다. 이후 probe가 존재한다고 가정하지 않는다. 체크포인트 6개 해설은 제공했고 독립 이해도 평가는 미진행이다.

## Day 10 k9s 종료 확인 (2026-10-05)
- 사용자가 Service agent의 ClusterIP/10.43.162.127/8000 TCP 값 일치 및 k9s 종료를 텍스트로 확인했다. 종료 후 별도 리소스 조회는 하지 않았다. 앱/Service/클러스터/레지스트리 삭제는 하지 않았으며 probe 최종 정리는 아직이다.

## Day 10 k9s Describe 확인 (2026-10-05)
- 사용자 캡처: pwrhg는 0.2.0 이미지·Running/Ready=True·재시작 1이다. 직전 종료 Error/137은 과거 이력이며 앞서 확인한 liveness 재시작과 부합한다. /healthz readiness/liveness 설정 및 requests 100m/128Mi, limits 1 CPU/512Mi를 확인했다. 설정 변경은 하지 않았다.

## Day 10 k9s Pod 화면 확인 (2026-10-05)
- 사용자 캡처에서 Context/Cluster k3d-onprem, K9s v0.32.5, K8s v1.30.4+k3s1, Pods(ax-pilot)[3]을 확인했다. 앱 두 Pod는 1/1 Running·재시작 1/0, probe는 1/1 Running·AGE 59m다. UI 접속은 확인됐으며 리소스 변경은 하지 않았다.

## Day 10 k9s 사전 확인 (2026-10-05)
- 사용자 출력: /usr/local/bin/k9s v0.32.5, kubectl v1.31.0이다. 정상 agent 0.2.0은 2/2, pwrhg/rslwh는 1/1 Running·재시작 각각 1/0이다. probe는 1/1 Running·AGE 57m로 확인됐으며 이후 실행 시간 종료 가능성이 있다.
- k3d-onprem/ax-pilot의 읽기 전용 k9s 첫 화면 실행을 안내했고 UI 접속 결과는 대기 중이다. 추가 설치·리소스 변경은 하지 않았다.

## Day 10의 10-6 완료 상태 (2026-10-05)
- 사용자 출력에서 고장 Deployment 5개 삭제 및 b-* Deployment/ReplicaSet/Pod 부재를 확인했다. 정상 agent 0.2.0은 2/2, 활성 ReplicaSet 64c5d66bdf는 2/2/2, 이전 0.3.0 ReplicaSet 7f87967cf6는 0/0/0이다.
- pwrhg(10.42.0.7/agent-0)는 1/1 Running·재시작 1, rslwh(10.42.1.8/agent-1)는 1/1 Running·재시작 0이다. probe(10.42.2.9/server-0)는 1/1 Running·AGE 43m이며 Service agent는 10.43.162.127:8000/TCP를 유지한다.
- 10-1~10-6 완료, Day 10 전체는 미완료다. 클러스터·레지스트리는 삭제하지 않았으며 k9s 확인·probe 최종 정리·체크포인트는 사용자 요청 후 진행한다. 아래 정리 대기 문구는 이전 이력이다.

## Day 10의 10-6 NotReady 진단·정리 안내 (2026-10-05)
- 사용자 출력: b-notready-5cd84bc7c4-zts4l은 server-0/10.42.2.12에서 컨테이너 Running·재시작 0·Ready=False다. readiness는 /health:8000을 검사하며 초기 connection refused 이후 반복 HTTP 404를 기록했다. 소스의 정상 경로는 /healthz다.
- 다섯 고장 Deployment 및 종속 리소스만 삭제하도록 안내했고 실행 결과 대기 중이다. 아직 삭제 완료가 아니며 정상 앱·Service·probe·클러스터·레지스트리는 유지한다.

## Day 10의 10-6 ConfigError 진단 (2026-10-05)
- 사용자 출력: b-configerror-5d86b95c76-zxhmd는 agent-1/10.42.1.9에 배정됐고 이미지도 노드에 존재하지만 필수 Secret agent-secret-typo 부재로 Waiting/CreateContainerConfigError·재시작 0이다. PodScheduled=True이며 Events의 secret not found를 확인했다. Secret 값 조회·생성이나 설정 변경은 하지 않았다.

## Day 10의 10-6 Pending 진단 (2026-10-05)
- 사용자 출력: b-pending-7c74794f46-p2kgt는 cpu=64/memory=512Gi 요청으로 세 노드 모두 Insufficient cpu/memory다. Node/IP 없음·PodScheduled=False 및 FailedScheduling을 확인했다. 요청량이지 실제 사용량은 아니며 리소스 설정은 변경하지 않았다.

## Day 10의 10-6 CrashLoop 진단 (2026-10-05)
- 사용자 출력: b-crashloop-76f96fcdb-v9cp5는 server-0/10.42.2.11, Pod phase Running이나 컨테이너 Waiting/CrashLoopBackOff·Ready=False·재시작 6이다. 직전 종료는 Error/Exit Code 1이다.
- 노드에 이미 있는 0.2.0 이미지로 시작한 뒤 실행 명령의 sys.exit(1)로 종료한다. 이전 로그의 설정 누락 문구는 실제 파일 검사 결과가 아닌 예제의 고정 출력이다. 리소스 변경 없이 다음 Pending 진단으로 진행한다.

## Day 10의 10-6 레지스트리 추가 확인 (2026-10-05)
- 사용자 첨부 출력: server-0의 mirrors에 onprem-registry:5000/5001 모두 HTTP endpoint http://onprem-registry:5000 설정이 있다. 호스트 127.0.0.1:5001의 ax/agent/manifests/9.9.9 조회는 MANIFEST_UNKNOWN 및 HTTP 404다.
- containerd 발췌는 최종 HTTPS 요청/HTTP 응답 오류를 반복해서 보여 준다. HTTP mirror 설정 누락은 아니며 태그 부재 후 fallback 설명과 부합하지만 최초 HTTP 시도의 과정 자체는 발췌에 없다. 설정 변경 없이 다음 고장 예제 진단으로 진행한다. 아래 추가 진단 대기 문구는 이전 이력이다.

## Day 10의 10-6 이미지 다운로드 오류 (2026-10-05)
- 사용자 describe 출력: b-imagepull은 server-0에 배정됐으나 컨테이너 Waiting/ImagePullBackOff·재시작 0이다. Events의 9.9.9 manifest HTTPS 요청에 HTTP 응답 오류가 표시됐다. HTTP mirror 설정 및 태그 부재 후 fallback 여부는 추가 진단 대기 중이며 설정 변경은 하지 않았다.

## Day 10의 10-6 고장 예제 실행 상태 (2026-10-05)
- 사용자 출력에서 b-* Deployment 5개 생성 및 각각 READY 0/1을 확인했다. Pod는 b-imagepull=ErrImagePull, b-crashloop=CrashLoopBackOff(재시작 3), b-pending=Pending(Node/IP 없음), b-configerror=CreateContainerConfigError, b-notready=Running 0/1이다. 실제 원인은 Events/로그 진단 대기 중이다.
- 정상 agent 0.2.0 Deployment 2/2, pwrhg/rslwh 1/1 Running·재시작 1/0, probe 1/1 Running·10.42.2.9/server-0을 유지한다. 고장 리소스는 아직 정리하지 않았다. 아래 상태는 이전 이력이다.

## Day 10의 10-6 배포 전 상태 확인 (2026-10-05)
- 사용자 출력에서 고장 예제 YAML 5개 해시 일치 및 기존 b-* Deployment/Pod 부재를 확인했다. 정상 agent 0.2.0 Deployment 2/2, pwrhg/rslwh 모두 1/1 Running이며 재시작은 각각 1/0이다.
- probe는 1/1 Running·재시작 0·AGE 20m·10.42.2.9/server-0이다. 지정 고장 예제 5개 apply·상태 조회를 안내했고 결과 대기 중이며 생성 완료로 기록하지 않는다. 아래 상태는 이전 이력이다.

## Day 10의 10-5 완료·liveness 복구 확인 (2026-10-05)
- 사용자 출력에서 pwrhg UID=8a3bd410-edb6-4026-a2d6-affb4d3a8e1d 유지·RESTARTS 1 및 readiness/liveness timeout과 liveness에 따른 Killing·Created·Started 이벤트를 확인했다. 대상 10.42.0.7의 /healthz는 status ok/version 0.2.0/host pwrhg/HTTP 200이다. [증거](../day10/evidence/105-recovery-user-2026-10-05.txt).
- 최종 agent 0.2.0 Deployment 2/2, pwrhg(10.42.0.7/agent-0) 1/1 Running·재시작 1, rslwh(10.42.1.8/agent-1) 1/1 Running·재시작 0이다. 앱·클러스터·probe를 유지하며 10-1~10-5 완료·10-6 이후 미진행이다. 아래 상태는 이전 이력이다.

## Day 10의 10-5 무응답 후 재시작 관찰 (2026-10-05)
- 사용자 출력으로 pwrhg의 hang=true/HTTP 200 이후 READY 1/1→0/1→1/1 및 RESTARTS 0→1을 확인했다. 주입 전 UID는 8a3bd410-edb6-4026-a2d6-affb4d3a8e1d다. [증거](../day10/evidence/105-hang-watch-user-2026-10-05.txt).
- watch 종료 여부·사후 UID·liveness/Killing 이벤트·대상 HTTP 및 최종 Deployment/Pod 조회 결과 대기 중이다. liveness 원인/HTTP 복구 확정 및 10-5 완료는 아직이며 아래 상태는 이전 이력이다.

## Day 10의 10-5 probe 재준비 확인 (2026-10-05)
- 사용자 출력으로 probe 삭제·재생성·Ready 및 10.42.0.7의 /healthz 응답 status ok/version 0.2.0/host pwrhg/HTTP 200을 확인했다.
- pwrhg UID/재시작 기준 조회와 hang 1회·watch를 재안내했고 결과 대기 중이다. 장애 주입 성공이나 자동 복구로 기록하지 않으며 아래 상태는 이전 이력이다.

## Day 10의 10-5 probe 종료·무응답 미주입 (2026-10-05)
- 사용자 출력으로 pwrhg UID=8a3bd410-edb6-4026-a2d6-affb4d3a8e1d/RESTARTS=0과 probe Succeeded에 따른 exec 거부를 확인했다. 원격 curl과 뒤의 watch는 실행되지 않았으므로 이번 명령으로 앱에 무응답을 주입하지 않았다.
- probe 재생성·Ready 및 pwrhg의 /healthz 직접 조회를 안내했고 결과 대기 중이다. 앱 Pod 변경은 없으며 아래 상태는 이전 이력이다.

## Day 10의 10-5 사전 상태·실제 헬스체크 확인 (2026-10-05)
- 사용자 출력에서 agent 0.2.0 Deployment 2/2, pwrhg(10.42.0.7/agent-0)·rslwh(10.42.1.8/agent-1)·probe(10.42.2.7/server-0) 모두 1/1 Running·RESTARTS 0을 확인했다.
- 실제 readiness는 /healthz·5초 간격·1초 제한·실패 임계 3회, liveness는 /healthz·10초 간격·3초 제한·실패 임계 3회다. pwrhg만 대상으로 hang 호출·watch를 안내했고 결과 대기 중이며 장애 주입 완료로 기록하지 않는다. 아래 상태는 이전 이력이다.

## Day 10의 10-4 완료·최종 상태 (2026-10-05)
- 사용자 최종 출력에서 agent 0.2.0 Deployment 2/2 및 pwrhg(10.42.0.7/agent-0), rslwh(10.42.1.8/agent-1)만 1/1 Running·RESTARTS 0을 확인했다. 교체된 jlrdl/wz225는 사라졌고 0.3.0 ReplicaSet은 0/0/0으로 보존됐다. [증거](../day10/evidence/104-rollback-user-2026-10-05.txt).
- 10-1~10-4 완료. 앱·클러스터·probe는 종료/삭제하지 않았다. probe는 sleep 3600으로 재생성한 상태라 재개 시 현재 상태를 확인한다. 10-5 이후는 미진행이며 아래 상태는 이전 이력이다.

## Day 10의 10-4 0.2.0 롤백 성공 (2026-10-05)
- 사용자 출력으로 agent 0.2.0 Deployment 2/2, ReplicaSet agent-64c5d66bdf 2/2/2 및 agent-7f87967cf6 0/0/0을 확인했다. 새 0.2.0 Pod pwrhg(10.42.0.7/agent-0), rslwh(10.42.1.8/agent-1)는 1/1 Running·RESTARTS 0이다.
- Service 응답은 status ok/version 0.2.0/host rslwh/HTTP 200이다. 교체된 jlrdl/wz225는 Terminating이며 종료 완료 대기·최종 리소스 조회 결과를 기다린다. 아래 상태는 이전 이력이다.

## Day 10의 10-4 0.3.0 롤링 업데이트 성공 (2026-10-05)
- 사용자 출력으로 agent 0.3.0 Deployment 2/2 및 새 ReplicaSet agent-7f87967cf6 2/2/2를 확인했다. 구 ReplicaSet agent-64c5d66bdf는 0/0/0이다.
- 새 Pod jlrdl(10.42.2.8/server-0), wz225(10.42.1.7/agent-1)는 모두 1/1 Running·RESTARTS 0이다. 업데이트 전부터 완료 이후까지 관찰한 HTTP 60회 성공·실패 0 및 두 종료 코드 0을 확인했다. [증거](../day10/evidence/104-rollout-user-2026-10-05.txt).
- 이력 조회·직전 0.2.0 배포 롤백·최종 상태/HTTP 조회를 안내했고 결과 대기 중이다. 아직 롤백 성공으로 기록하지 않으며 아래 상태는 이전 이력이다.

## Day 10의 10-4 probe 재준비·업데이트 전 HTTP 확인 (2026-10-05)
- 사용자 출력으로 기존 probe 삭제·재생성·Ready 및 Service /healthz의 status ok/version 0.2.0/host stfrr/HTTP 200을 확인했다.
- HTTP 60회 관찰과 0.3.0 이미지 변경·rollout·최종 조회를 안내했고 결과 대기 중이다. 앱 업데이트 성공으로 기록하지 않는다. 아래 상태는 이전 이력이다.

## Day 10의 10-4 축소 정리 완료 (2026-10-05)
- 사용자 출력으로 7642s/kjbqb 삭제 완료 및 stfrr(10.42.2.5/server-0), zqnxs(10.42.0.6/agent-0)만 1/1 Running·RESTARTS 0임을 확인했다. agent 0.2.0 Deployment/ReplicaSet은 2개 준비다.
- Completed 상태였던 probe 삭제·재생성 및 Ready·Service HTTP 조회를 안내했고 결과 대기 중이다. probe 재기동 성공이나 앱 이미지 변경으로 기록하지 않는다. 아래 상태는 이전 이력이다.

## Day 10의 10-4 2개 복원·종료 중 Pod 확인 (2026-10-05)
- 사용자 출력에서 agent 0.2.0 Deployment/ReplicaSet 2개 준비, stfrr/zqnxs 1/1 Running 및 7642s/kjbqb Terminating을 확인했다. 목표 복제본은 2로 복원됐고 초과 Pod의 삭제 완료는 아직 확인하지 않았다.
- 두 Terminating Pod의 wait --for=delete 및 최종 목록 조회 결과 대기 중이다. probe의 마지막 확인 상태는 Completed이며 아래 상태는 이전 이력이다.

## Day 10의 10-4 복제본 4개 확장 확인 (2026-10-05)
- 사용자 출력에서 agent 0.2.0 Deployment/ReplicaSet 4개 준비 및 네 Pod 1/1 Running·RESTARTS 0을 확인했다. 기존 7642s·stfrr에 kjbqb(10.42.1.6/agent-1)·zqnxs(10.42.0.6/agent-0)가 추가됐다.
- replicas=2 복원·rollout·리소스 조회를 안내했고 결과 대기 중이다. 아직 2개 복원으로 기록하지 않는다. probe의 마지막 확인 상태는 Completed이며 아래 상태는 이전 이력이다.

## Day 10의 10-4 자가 치유 확인 (2026-10-05)
- 사용자 출력에서 d7qcb 삭제, 새 Pod 7642s 생성(10.42.1.5/agent-1), 기존 stfrr 유지(10.42.2.5/server-0), 두 Pod 1/1 Running·RESTARTS 0 및 Deployment/ReplicaSet 2개 준비를 확인했다. 이미지는 0.2.0이다.
- replicas=4 확장·rollout·리소스 조회를 안내했지만 결과는 아직 받지 않았다. probe의 마지막 확인 상태는 Completed다. 아래 상태는 이전 이력이다.

## Day 10의 10-4 사전 상태 확인 (2026-10-05)
- 사용자 출력으로 실습용 kubectl v1.31.0/Kustomize v5.4.2 및 agent 0.2.0 Deployment 2/2를 확인했다. 앱 Pod d7qcb와 stfrr는 모두 1/1 Running·RESTARTS 0이다.
- probe는 0/1 Completed·RESTARTS 0·AGE 65m이며 sleep 3600으로 생성한 진단 Pod다. HTTP 관찰 전에 재준비가 필요하다.
- d7qcb Pod 하나 삭제·rollout/리소스 조회를 안내했고 사용자 결과 대기 중이다. 이 안내를 삭제 실행 완료로 기록하지 않는다. 아래 상태는 이전 이력이다.

## Day 10의 10-3 완료·포워딩 종료 (2026-10-05)
- 사용자 출력으로 Ctrl+C 후 프롬프트 복귀 및 `ss -ltn '( sport = :39827 )'`의 헤더만 출력을 확인했다. 39827 리스너는 해제됐다. [증거](../day10/evidence/103-portforward-result-user-2026-10-05.txt).
- 내부 Service DNS·HTTP 분산과 port-forward 단일 Pod 응답 비교를 마쳐 10-3 완료다. 앱·클러스터 종료나 probe 삭제는 하지 않았다. probe의 현재 상태는 재조회하지 않았으며 sleep 3600 종료 가능성이 있다. 10-4 이후는 미진행이고 아래 상태는 이전 이력이다.

## Day 10의 10-3 포워딩 HTTP 성공·리스너 유지 (2026-10-05)
- 사용자 출력에서 127.0.0.1:39827/healthz HTTP 4회 모두 agent-64c5d66bdf-d7qcb 응답을 확인했다. 이어진 ss에는 127.0.0.1:39827 LISTEN이 남아 있다.
- 1번 포워딩 터미널에서 Ctrl+C 종료 후 ss 재확인 대기 중이다. 앱·클러스터 종료는 요청하지 않았다. 아래 대기 문구는 이전 이력이다.

## Day 10의 10-3 현재 포워딩 포트 확인 (2026-10-05)
- 사용자 제공 1번 Ubuntu 터미널의 최신 출력은 `Forwarding from 127.0.0.1:39827 -> 8000`이다. 앞선 curl은 이전 포트 45537을 호출했으며 현재 포트와 달랐다.
- 2번 Ubuntu 터미널에서 39827 HTTP 4회 재검증 및 성공 후 Ctrl+C·리스너 해제 확인 대기 중이다. 앱·클러스터 변경은 없으며 아래 원인 미확인 문구는 이전 이력이다.

## Day 10의 10-3 로컬 연결 실패 (2026-10-05)
- 사용자 제공 새 Ubuntu 터미널 출력에서 첫 curl이 127.0.0.1:45537 연결 오류 7로 실패했다. 앞선 Forwarding 출력은 기동 시점의 증거이며 현재 리스너 존속을 증명하지 않는다.
- 기존 포워딩 터미널 출력과 새 터미널의 ss·pgrep 결과 대기 중이다. 원인은 미확인이고 앱·클러스터 변경은 하지 않았다. 아래 상태는 이전 이력이다.

## Day 10의 10-3 port-forward 기동 확인 (2026-10-05)
- 사용자 Ubuntu 출력으로 `Forwarding from 127.0.0.1:45537 -> 8000`을 확인했다. 기존 터미널에서 전경 실행 중이며 HTTP 비교·종료·리스너 해제 확인은 아직이다. [증거](../day10/evidence/103-portforward-start-user-2026-10-05.txt).
- 다른 Ubuntu 터미널의 127.0.0.1:45537 HTTP 4회 호출 및 이후 Ctrl+C·ss 확인을 안내했다. 앱·probe·클러스터는 유지한다. 아래 대기 문구는 이전 이력이다.

## Day 10의 10-3 내부 Service 호출 확인 (2026-10-05)
- 사용자 출력으로 ax-pilot/probe 생성·Ready를 확인했다. 이미지 nicolaka/netshoot:v0.13·sleep 3600이며 아직 삭제하지 않았다. [증거](../day10/evidence/103-service-user-2026-10-05.txt).
- DNS 서버 10.43.0.10:53이 agent.ax-pilot.svc.cluster.local을 Service IP 10.43.162.127로 해석했다. probe에서 http://agent:8000/healthz 호출 8회가 stfrr Pod 5회·d7qcb Pod 3회로 분산됐다.
- Ubuntu 루프백 자동 포트의 port-forward 전경 실행을 안내했고 실제 포트·기동 출력은 대기 중이다. 앱·probe·클러스터를 유지하며 10-3 전체는 아직 미완료다.

## Day 10의 10-2 첫 배포 완료 (2026-10-05)
- 사용자 Ubuntu 출력에서 YAML 3개 체크섬 OK, Namespace ax-pilot·Deployment/Service agent 생성, rollout 성공을 확인했다. Deployment는 2/2이며 이미지 참조는 onprem-registry:5000/ax/agent:0.2.0이다. [증거](../day10/evidence/102-deploy-user-2026-10-05.txt).
- Pod agent-64c5d66bdf-d7qcb=10.42.0.5/agent-0, agent-64c5d66bdf-stfrr=10.42.2.5/server-0. 둘 다 1/1 Running·재시작 0이다. 관리 노드도 앱을 실행하며 배치 정책을 변경하지 않았다.
- Service agent=ClusterIP 10.43.162.127:8000·selector app=agent. readiness 통과·앱 기동은 확인했지만 Service HTTP/분산, 실제 컨테이너 imageID·pull 이벤트, liveness 장애 복구는 아직 별도 검증하지 않았다.
- 10-1·10-2 완료. 앱·클러스터·레지스트리·이미지는 유지한다. 다음은 사용자 요청 후 10-3이다. 아래 미배포 문구는 이전 이력이다.

## Day 10의 10-1 완료·이미지 등록 확인 (2026-10-05)
- 사용자 출력으로 localhost:5001/ax/agent:0.2.0·0.3.0 push 성공과 태그 목록 두 개·HTTP 200을 확인했다. digest는 각각 a4ef49ae142efb1a03fe43c30d4a6f68ceee1c649578c33407827e8f6f4185a3, 3b2b97652b5db89e15b8750375cef5d163bd2a72405902dcda882e6cde5c6ec6이며 앞서 확인한 로컬 ID와 일치한다. [증거](../day10/evidence/101-push-user-2026-10-05.txt).
- 10-1 완료. onprem 클러스터·레지스트리·네트워크·볼륨·이미지와 기존 자원은 유지한다. 앱 Pod 배포·클러스터 노드의 이미지 pull·새 이미지 런타임 검증은 아직 없다. 다음은 사용자 요청 후 10-2다.
- 현재 셸은 실습용 kubectl 1.31.0을 사용한다. 재개 시 PATH와 context를 확인한다. Day 10 YAML은 존재만 확인했으며 적용 전 Windows/Ubuntu 내용 일치 확인이 남아 있다.

## Day 10 agent:0.3.0 빌드 확인 (2026-10-05)
- 사용자 출력으로 python:3.12.14-slim 기반 agent:0.3.0 빌드 성공을 확인했다. 로컬 ID는 sha256:3b2b97652b5db89e15b8750375cef5d163bd2a72405902dcda882e6cde5c6ec6이며 빌드 manifest list digest와 일치한다. [증거](../day10/evidence/101-build-user-2026-10-05.txt).
- agent:0.2.0(a4ef49ae...)·0.3.0 모두 linux/amd64·USER=10001·APP_VERSION 각 0.2.0/0.3.0을 확인했다. 설정 조회이며 새 앱 실행·스캔 결과와 구분한다.
- 두 버전의 localhost:5001/ax/agent 태그 추가·push·태그 API 조회를 안내했고 결과를 기다린다. 클러스터는 유지하고 앱 Pod 배포는 아직 하지 않았다.

## Day 10 시스템 준비·레지스트리 HTTP 확인 (2026-10-05)
- 사용자 출력으로 coredns·local-path-provisioner·metrics-server·traefik Deployment 모두 1/1·AVAILABLE 1, svclb Pod 3개 2/2 Running, 설치 Pod 두 개 Completed를 확인했다. Traefik 설치 Pod의 재시작 1회 원인은 미조사다. [증거](../day10/evidence/101-system-registry-user-2026-10-05.txt).
- Docker 컨테이너 6개가 Up이며 tools도 실행 중이다. serverlb 게시: 127.0.0.1:8080->80, 0.0.0.0:37327->6443(API). 레지스트리 게시: 127.0.0.1:5001->5000. /v2/는 {}·HTTP 200이다. 외부 PC 접근과 이미지 push/pull은 아직 미검증이다.
- agent/Dockerfile·app.py·requirements.txt의 Windows/Ubuntu SHA-256이 일치한다. agent:0.3.0 빌드를 안내했으며 실제 빌드 결과는 대기 중이다. 클러스터를 유지하고 앱 배포는 아직 하지 않았다.

## Day 10 클러스터 생성·노드 Ready 확인 (2026-10-05)
- 사용자 출력으로 onprem 클러스터 생성과 서버 1·워커 2 모두 Ready를 확인했다. Kubernetes v1.30.4+k3s1·containerd 1.7.20-k3s1이며 k3d-onprem context의 API 조회가 성공했다. [증거](../day10/evidence/101-cluster-user-2026-10-05.txt).
- 네트워크 k3d-onprem=172.21.0.0/16, server-0=172.21.0.3·agent-0=172.21.0.5·agent-1=172.21.0.4다. 앞서 조회한 대역과 새 대역은 겹치지 않지만 기존 WSL/koica 겹침은 유지된다.
- 이미지 볼륨·레지스트리·노드·로드밸런서 생성/기동 로그를 확인했다. 생성 직후 kube-system 설치 Pod 2개는 AGE 0s·ContainerCreating이다. 시스템 초기화 완료·실제 게시 포트·레지스트리 HTTP 응답은 후속 조회 결과 대기 중이다. 클러스터를 유지하며 앱 이미지 등록·배포는 아직 없다.

## Day 10 Ubuntu 자원·파일 확인 (2026-10-05)
- 사용자 출력: Ubuntu 메모리 available 13Gi, /dev/sdc 가용 951G(WSL 가상 디스크 표시), Docker CPUs=32·MemoryBytes=16334528512. Ubuntu 8080·5001 리스너는 없고 기존 컨테이너 8개는 모두 Exited다. [증거](../day10/evidence/101-resources-user-2026-10-05.txt).
- agent:0.2.0은 a4ef49ae142e·181MB이며 offline·ca·0.1.0 태그도 있다. agent:0.3.0은 없다. Day 10 YAML 3개 존재·0755는 확인했으나 Windows 사본과의 내용 일치는 미검증이다.
- WSL 172.18.48.0/20·IP 172.18.60.227과 koica Docker 172.18.0.0/16의 겹침이 유지된다. 다른 Docker 대역은 bridge 172.17.0.0/16, lab-net 172.19.0.0/16, other-net 172.20.0.0/16이다. 기존 자원은 변경하지 않았다.
- onprem 생성 명령을 안내했다. k3s v1.30.4-k3s1·서버 1/워커 2·레지스트리 127.0.0.1:5001·웹 127.0.0.1:8080을 지정하며 API 포트는 기본 자동 할당이다. 실제 기동·새 네트워크 대역·포트 바인딩 결과는 아직 대기 중이다.

## Day 10 Windows 포트 점검 확인 (2026-10-05)
- 사용자 Windows 출력에서 8080·5001·18080·15001 TCP 사용 행이 없고 네 포트 모두 IPv4/IPv6 제외 범위 밖임을 확인했다. 기본 8080·5001을 사용할 계획이다. [증거](../day10/evidence/101-windows-ports-user-2026-10-05.txt).
- Day 9의 7987~8086 제외 범위는 이번 목록에 없다. 변경 원인·시점은 미확정이며 Windows 설정을 변경하지 않았다. 실제 포트 바인딩 성공·Ubuntu 리스너 상태는 아직 확인하지 않았다.
- Ubuntu 자원·Docker 목록·네트워크 대역·Day 10 파일 존재 조회 결과를 기다린다. 클러스터는 아직 생성하지 않았다.

## Day 10 실습용 kubectl 설치 확인 (2026-10-05)
- 사용자 Ubuntu 출력으로 공식 파일 체크섬 OK, /home/user/.local/share/onprem-lab/kubectl-v1.31.0/bin/kubectl 선택, Client v1.31.0·Kustomize v5.4.2를 확인했다. [증거](../day10/evidence/101-kubectl-user-2026-10-05.txt).
- PATH 선택은 현재 셸에만 적용했으며 시스템 kubectl·셸 설정 파일을 변경하지 않았다. 새 터미널에서는 export PATH="$HOME/.local/share/onprem-lab/kubectl-v1.31.0/bin:$PATH" 후 hash -r 및 버전 확인이 필요하다.
- 기본 k3s 1.30과의 마이너 버전 차이 조건을 충족한다. 실제 클러스터 생성·통신은 아직 미검증이며 Windows 포트 점검 결과 대기 중이다. 아래 설치 대기 문구는 이전 이력이다.

## Day 10의 10-1 첫 점검 (2026-10-05)
- 사용자 Ubuntu 출력: Docker Client/Server 29.8.0 연결 정상, k3d v5.7.4·기본 k3s v1.30.4-k3s1, kubectl v1.36.1·Kustomize v5.8.1. k3d cluster list는 헤더만 표시됐다. [증거](../day10/evidence/101-precheck-user-2026-10-05.txt).
- 기본 k3s 버전은 생성 예정 값이며 실행 중인 클러스터 버전이 아니다. 다른 방식의 클러스터 유무·포트·자원 상태는 미조회다.
- kubectl/API 서버의 공식 지원 버전 차이는 마이너 1 이내이므로 1.36/1.30은 범위 밖이다. 가이드 kubectl v1.31.0을 ~/.local/share/onprem-lab/kubectl-v1.31.0/bin/kubectl에 별도 설치하고 현재 셸 PATH에서 선택하도록 안내했다. 설치·체크섬·선택 결과는 아직 대기 중이며 기존 시스템 kubectl은 변경하지 않는다.

## Day 9 실습 자원 정리·보존 확인 (2026-10-05)
- 사용자 Ubuntu 출력으로 day09-registry-ui-1·day09-registry-1·day09_default 제거 및 Compose 컨테이너 목록 부재를 확인했다. UI는 종료 상태다. 압축 전 agent-0.2.0-offline.tar 삭제 명령도 성공했다.
- day09_regdata 볼륨과 agent:0.2.0-offline 이미지(ID 4c10e5ca...)를 보존했다. 압축 파일은 gzip 검사·체크섬 OK이며 tar.gz 42M·체크섬 93 bytes·보고서 54K·SBOM 197K·wheels 756K·trivy-cache 1.4G가 남아 있다. 크기는 사용자 ls/du 표시값이다.
- Codex의 Ubuntu 직접 실행 결과가 아닌 사용자 출력 기준이다. [정리 증거](../day09/evidence/cleanup-user-2026-10-05.txt). 아래 서비스 실행 상태는 정리 전 이력이다.

## Day 9의 9-5 첨부 식별·문서 보관 상태 (2026-10-05)
- 사용자 Ubuntu 출력으로 agent-0.2.0-offline.tar.gz 체크섬 OK·43,776,190 bytes, trivy-agent-0.2.0.txt 55,261 bytes, sbom-agent-0.2.0.cdx.json 201,644 bytes와 각 보고서 해시를 확인했다. [식별 증거](../day09/evidence/95-artifacts-user-2026-10-05.txt).
- [학습용 반입 신청서](../day09/IMPORT-PACKAGE.md)는 Windows 프로젝트에 새로 작성했다. 원본 3종은 Ubuntu /home/user/onprem-lab/day09에 있으며 Windows로 복사하지 않았다. 신청서도 Ubuntu로 복사하지 않았다.
- 이번 작업은 식별 조회와 문서화이며 기존 컨테이너·이미지·볼륨·캐시 상태를 변경하지 않았다. 9-1~9-5 완료, 누적 점검·전체 정리·Day 전체 완료는 아직이다. 아래 항목의 다음 절 안내는 당시 이력이다.

## Day 9의 9-4 완료·스캔 및 SBOM 보존 (2026-10-05)
- 사용자 Ubuntu 출력으로 aquasec/trivy:0.56.2의 DB v2 준비·캐시 1.4G, network none 취약점 스캔 및 SBOM 생성을 확인했다. 대상은 localhost:5000/ax/agent:0.2.0이다.
- /home/user/onprem-lab/day09/trivy-agent-0.2.0.txt는 user:user·54K, Debian 13.7·HIGH 51·CRITICAL 0이다. sbom-agent-0.2.0.cdx.json은 user:user·197K, CycloneDX 1.6·구성 요소 90개·pip 25.0.1·PyYAML 6.0.2가 확인됐다. 크기는 ls 표시값이다.
- DB 파일은 trivy-cache/trivy/db/에 보존하며 UpdatedAt=2026-10-04T14:28:15.152965452Z·DownloadedAt=2026-10-04T15:36:41.35690486Z다. Docker 소켓의 로컬 이미지 조회를 이용한 스캐너 네트워크 차단 시험이며 Docker 호스트 전체 격리는 아니다.
- 기존 레지스트리 자원·이미지·반입 파일도 유지한다. 다음은 사용자 요청 후 9-5다. [스캔 증거](../day09/evidence/94-scan-user-2026-10-05.txt), [SBOM 증거](../day09/evidence/94-sbom-user-2026-10-05.txt).

## Day 9의 9-3 완료·보존 상태 (2026-10-05)
- 사용자 출력으로 from-reg 제거·부재, agent:0.2.0-offline 및 localhost:5000/ax/agent:0.2.0 두 태그 복원·동일 ID 4c10e5ca...와 반입 tar.gz 해시 OK를 확인했다.
- registry·registry-ui는 Up 4 hours이며 각각 127.0.0.1:5000·127.0.0.1:18082를 게시한다. regdata 볼륨은 삭제하지 않고 유지한다. 다음은 사용자 요청 후 9-4다. [정리 증거](../day09/evidence/93-cleanup-user-2026-10-05.txt). 아래 대기·복원 전 문구는 이전 이력이다.

## Day 9 사내 레지스트리 pull 확인 (2026-10-04)
- 사용자 출력으로 agent 로컬 태그 두 개 제거 후 localhost:5000/ax/agent:0.2.0 pull 성공·index digest 4c10e5ca... 일치·linux/amd64·USER=10001을 확인했다. 반입 파일 해시 OK이며 agent:0.2.0-offline 태그는 아직 복원 전이다.
- from-reg 실행 결과 대기. Windows 8000도 제외 범위에 있어 호스트 게시 없이 내부 healthz를 조회하도록 안내했다. [pull 증거](../day09/evidence/93-pull-user-2026-10-04.txt).

## Day 9 UI 18082 복구 확인 (2026-10-04)
- 사용자 Ubuntu 출력으로 수정 Compose 해시가 Windows와 일치함을 확인했다. 두 서비스 Up, registry 127.0.0.1:5000·UI 127.0.0.1:18082 게시 및 HTTP 200, CORS http://localhost:18082, 저장소 목록 두 개 유지를 확인했다.
- UI 주소는 http://localhost:18082다. 브라우저 관찰·pull 실행은 아직 미확인이다. [복구 증거](../day09/evidence/93-ui-recovery-user-2026-10-04.txt). 아래 적용 대기는 이전 이력이다.

## Day 9 UI 대안 18082 적용 준비 (2026-10-04)
- 사용자 Windows TCP 조회에서 18082 사용 항목 없음 확인. Codex는 Windows day09/compose.yaml의 UI 게시·registry CORS Origin을 18082로 수정했다. Ubuntu 사본 변경·서비스 재생성·HTTP 응답은 사용자 실행 결과 대기 중이다.
- 적용 후 UI 주소는 http://localhost:18082, registry API는 http://localhost:5000이다. 실제 복구 완료로 기록하지 않는다.

## Day 9 UI 포트의 Windows 제외 범위 포함 확인 (2026-10-04)
- 사용자 Windows 조회에서 8082 TCP 사용 항목은 없으나 IPv4/IPv6 모두 7987–8086 제외 범위를 표시했다. 8082가 이 범위에 포함돼 UI 게시 실패의 유력한 원인으로 판단한다. 생성 주체·시점은 미확정이다.
- 대안 18082는 제공된 제외 범위 밖이며 점유 조회 결과 대기 중이다. Compose 포트·CORS 변경은 아직 하지 않았다. [증거](../day09/evidence/93-windows-ports-user-2026-10-04.txt).

## Day 9의 9-3 중단 후 재개 점검 (2026-10-04)
- 사용자 출력: Docker default·29.8.0, registry 및 registry-ui Up 2 minutes, day09_regdata와 로컬 이미지 태그 존재. 레지스트리 catalog HTTP 200·저장소 두 개 확인.
- UI는 ps에 80/tcp만 표시되며 localhost:8082 연결 실패·HTTP 000이다. 원인은 미확정이며 Compose 설정·포트 inspect·UI 로그 조회 결과 대기 중이다. [증거](../day09/evidence/93-resume-user-2026-10-04.txt).

## Day 9의 9-3 push·API 검증 확인 (2026-10-03)
- 사용자 출력으로 localhost:5000에 ax/agent:0.2.0·tools/netshoot:v0.13 등록과 API digest의 push 결과 일치를 확인했다. agent는 OCI index, netshoot는 단일 플랫폼 OCI manifest 응답이다. [API 증거](../day09/evidence/93-api-user-2026-10-03.txt).
- 레지스트리 자원은 유지하며 UI 관찰·pull 실행은 아직 미확인이다. 아래 빈 catalog·push 대기는 이전 기동 시점의 기록이다.

## Day 9의 9-3 레지스트리 기동 확인 (2026-10-03)
- 사용자 출력으로 registry:2.8.3·joxit/docker-registry-ui:2.5.7을 사용하는 컨테이너 2개가 Up이며 호스트 127.0.0.1:5000·8082 게시를 확인했다. day09_default 네트워크·day09_regdata 볼륨이 새로 생성됐다.
- /v2/는 {}·HTTP 200, catalog는 빈 repositories, UI는 HTTP 200이다. agent·netshoot push 결과 대기 중이며 모든 Day 9 레지스트리 자원을 유지한다. 사전 조회의 다른 컨테이너 8개는 모두 Exited였고 변경하지 않았다. [기동 증거](../day09/evidence/93-startup-user-2026-10-03.txt).

## Day 9의 9-2 완료·시험 자원 제거 및 산출물 보존 확인 (2026-10-03)
- 사용자 출력으로 내부 agent와 day09-airgap 제거를 확인했다. 호스트의 정확한 컨테이너 이름 및 익명 볼륨 ba9f80170ab1734fe7dee47dddf808470eb6e88a23b917896b374b42fed6b698 조회에는 헤더만 남았다.
- 호스트 agent:0.2.0-offline ID=sha256:4c10e5ca549f993cb5d5271e24bb4ff28ae6426f3fd91a5f52b7172796dcf812, tar 43M·tar.gz 42M·sha256 93바이트 존재 및 압축 파일 해시 OK를 확인했다. dind·베이스 이미지·wheels·캐시·다른 프로젝트 자원은 삭제하지 않았고 이번 최종 출력에서는 재조회하지 않았다.
- 9-1·9-2 완료이며 9-3 이후는 미진행이다. 아래 실행 중·대기 기록은 이전 이력이다. Codex 직접 Ubuntu 실행·전체 동기화는 없다. [정리 증거](../day09/evidence/92-cleanup-user-2026-10-03.txt).

## Day 9의 9-2 별도 엔진 앱 기동 성공·정리 대기 (2026-10-03)
- 사용자 출력으로 내부 agent(4d55ca6f2f12)의 running·network=none, UID=10001·GID=0, PyYAML=6.0.2 및 healthz ok·version=0.2.0을 확인했다. 외부 pull 불가인 빈 엔진에 파일을 적재한 뒤의 실행 결과다.
- 내부 agent·day09-airgap 및 연결된 익명 볼륨 제거, 호스트 이미지·반입 파일 보존 확인을 안내했으며 결과 대기 중이다. 현재 정리 완료로 기록하지 않는다. [기동 증거](../day09/evidence/92-airgap-runtime-user-2026-10-03.txt).

## Day 9의 9-2 별도 엔진 파일 적재 성공 (2026-10-03)
- 사용자 출력으로 내부 pull이 network is unreachable·종료 코드 1로 실패하고 images=0을 유지함을 확인했다. /tmp 반입 경로에서 해시 파일이 보이지 않았으나 mountinfo의 tmpfs 마운트를 확인하고 /day09-import로 바꿔 해시 OK·load 성공을 확인했다.
- 내부 Docker 27.5.1의 이미지 ID=sha256:b7e1e28f346895634bd4c58e176bc9dc05c4c6b2522e65f1ec6044fc6b327db9는 원본 빌드의 config 해시와 일치한다. linux/amd64·USER=10001이다. 호스트 엔진의 ID=4c10e5...는 원본 빌드의 manifest list 해시와 일치했다.
- day09-airgap은 실행 중이며 /var/lib/docker 익명 볼륨 ba9f80170ab1734fe7dee47dddf808470eb6e88a23b917896b374b42fed6b698을 사용한다. 내부 앱 기동 결과 대기 중이며 정리는 아직 미진행이다. [사용자 증거](../day09/evidence/92-airgap-load-user-2026-10-03.txt).

## Day 9의 9-2 별도 Docker 엔진 기동 확인 (2026-10-03)
- 사용자 출력으로 docker:27-dind의 linux/amd64 다운로드와 ID=sha256:aa3df78ecf320f5fafdce71c659f1629e96e9de0968305fe1de670e0ca9176ce를 확인했다.
- day09-airgap(a1a9a7d2713e)이 privileged·network=none으로 기동됐으며 STATUS=running, 내부 Docker Server=27.5.1 images=0을 확인했다. 컨테이너는 유지 중이며 내부 pull 실패 시험 결과 대기 중이다. 내부 적재·앱 기동·정리는 미진행이다. [기동 증거](../day09/evidence/92-dind-start-user-2026-10-03.txt).

## Day 9의 9-2 이미지 복원 성공 (2026-10-03)
- 사용자 출력으로 gzip 검사·sha256sum -c OK, agent:0.2.0-offline 제거·목록 부재 및 압축 파일 load 성공을 확인했다. 복원 ID는 sha256:4c10e5ca549f993cb5d5271e24bb4ff28ae6426f3fd91a5f52b7172796dcf812로 원본과 같으며 linux/amd64·USER=10001도 유지됐다.
- 반입 파일·wheels는 유지한다. 별도 Docker 데몬 시험은 사전 점검 안내 후 결과 대기 중이며 컨테이너 생성은 아직 없다. [사용자 증거](../day09/evidence/92-load-user-2026-10-03.txt).

## Day 9의 9-2 반입 파일 생성 확인 (2026-10-03)
- 사용자 Ubuntu 출력으로 day09/agent-0.2.0-offline.tar 43M·tar.gz 42M·sha256 파일 93바이트 생성을 확인했다. 크기는 ls의 표시값이다. 압축 파일 해시는 cd08d49e729c690a20925ecedb1284745c826534ebfd241314b327cb107c52e6이며 save 당시 이미지 ID는 9-1 빌드 결과와 일치한다.
- gzip·파일 SHA-256 검증 후 해당 이미지 제거·load 복원을 안내했으며 결과 대기 중이다. 파일은 Ubuntu 사본에 있고 Windows에는 사용자 증거만 기록했다. [증거](../day09/evidence/92-package-user-2026-10-03.txt).

## Day 9의 9-1 완료·시험 컨테이너 정리 확인 (2026-10-03)
- 사용자 첨부 출력으로 day09-offline-test 제거 및 정확한 이름 필터 목록에 컨테이너 행이 없음을 확인했다. 앞서 network=none 기동·UID=10001·GID=0·PyYAML=6.0.2·healthz ok를 확인했다.
- 온라인용 agent/Dockerfile의 Windows·Ubuntu 해시가 일치하며 같은 베이스로 --network=none·--no-cache 빌드 시 pip 단계에서 이름 해석 실패·종료 코드 1을 확인했다. 앞선 로컬 wheel 설치 성공과 비교해 9-1을 완료했다.
- agent:0.2.0-offline·베이스 이미지·wheels는 삭제하지 않았다. 비교 빌드는 export 이전에 실패했고 기존 비교 태그 유무·캐시·다른 자원은 별도 재조회하지 않았다. 9-2 이후는 미진행이며 아래 대기·실행 중 문구는 이전 이력이다. [사용자 증거](../day09/evidence/91-cleanup-online-failure-user-2026-10-03.txt).

## Day 9의 9-1 네트워크 없는 기동 확인 (2026-10-03 수신)
- 사용자 출력으로 day09-offline-test(21519ca2ac3f)의 running·NETWORK=none, UID=10001·GID=0, PyYAML=6.0.2 및 컨테이너 내부 loopback healthz의 ok·version=0.2.0을 확인했다. Docker health 상태 자체·외부 DB/LLM 통합은 미검증이다.
- 해당 컨테이너 정리·잔존 목록 확인과 온라인용 Dockerfile 비교를 안내했으며 결과 대기 중이다. 이미지와 wheels는 보존한다. 현재 컨테이너 제거 완료로 처리하지 않는다. [사용자 증거](../day09/evidence/91-runtime-user-2026-10-03.txt).

## Day 9의 9-1 오프라인 빌드 확인 (2026-10-02)
- 사용자 Ubuntu 출력으로 Docker Client/Engine 29.8.0·Desktop 4.92.0(240144)·default 연결과 Windows/Ubuntu 실습 파일 해시 일치를 확인했다.
- python:3.12.14-slim은 최초 조회 시 없었으며 이후 pull·linux/amd64 확인을 마쳤다. PyYAML 6.0.2 cp312·x86_64 wheel(user:user, wheels 756K)을 준비했다.
- default 빌더에서 --network=none·--no-cache로 로컬 wheel 설치와 agent:0.2.0-offline 생성에 성공했다. inspect ID=sha256:4c10e5ca549f993cb5d5271e24bb4ff28ae6426f3fd91a5f52b7172796dcf812, linux/amd64, USER=10001이다. 빌드 RUN의 네트워크 제한과 빌더 전체의 외부 통신 차단은 구분한다.
- 앱의 network=none 기동·실제 UID·PyYAML·healthz 조회는 안내 후 사용자 결과 대기 중이다. 기존 자원은 재조회하지 않았다. Codex 직접 Ubuntu 실행·전체 동기화는 없다. [SESSION](../day09/SESSION.md), [빌드 증거](../day09/evidence/91-build-user-2026-10-02.txt).

## Day 8 종료 — 지정 자원 제거 확인 (2026-10-01)
- 사용자 Ubuntu 출력으로 Day 8 컨테이너 5개·네트워크 2개 제거와 프로젝트 필터 잔존 목록 부재를 확인했다. probe 내부 임시 공개 CA 사본도 해당 컨테이너와 함께 제거됐다.
- certs/mitmproxy-ca-cert.pem(1172바이트) 및 agent:0.2.0-ca 이미지(ID ebe1f3076bf2, DISK USAGE 182MB·CONTENT SIZE 44.3MB) 보존을 확인했다. 이미지·볼륨 삭제 옵션이나 전역 prune은 사용하지 않았다. certs 전체 목록·기존 백업·다른 프로젝트 자원·8082 리스너는 재조회하지 않았다.
- 8-1~8-4 실습·정리·체크포인트 해설 완료, 독립 평가는 미실시다. [종료 정리 증거](../day08/evidence/cleanup-user-2026-10-01.txt). 아래 실행 중·유지 문구는 종료 전 이력이다. Codex 직접 Ubuntu 실행·전체 동기화가 아닌 사용자 출력 확인이다.

## Day 8의 8-4 완료 — 자원 유지 (2026-10-01)
- 사용자 텍스트로 mitmweb의 GET https://example.com/·Python-urllib/3.12 요청 헤더와 HTTP 200·응답 헤더·Example Domain HTML 본문을 확인했다. CLI의 새 agent-ca HTTPS 요청도 HTTP 200이었다. [관찰 증거](../day08/evidence/84-https-observation-user-2026-10-01.txt).
- 8-1~8-4 실습 완료. 컨테이너 5개·네트워크 2개·CA·이미지·probe 임시 공개 CA 사본을 유지하며 전체 정리는 미진행이다. Codex 직접 브라우저 조작이나 Ubuntu 재실행은 하지 않았다.

## Day 8의 8-3 완료 — 인증서 진단 확인 (2026-10-01)
- 사용자 출력으로 프록시 경유 subject=example.com·issuer=mitmproxy 및 probe 검증 코드 21, CA 번들 150·151개와 mitmproxy CA 1개를 확인했다. 이후 probe curl은 CA 미지정 exit=60·HTTP=000, 지정 후 exit=0·HTTP=200이었다.
- 컨테이너 5개·네트워크 2개·certs·이미지를 유지한다. probe의 /tmp/day08-corp-ca.pem은 공개 CA 임시 사본이며 삭제하지 않았다. OS 신뢰 저장소는 변경하지 않았다. [curl 증거](../day08/evidence/83-curl-user-2026-10-01.txt). 8-4와 전체 정리는 미진행이다.

## Day 8의 8-2 완료 — 컨테이너 5개 유지 (2026-10-01)
- 사용자 Ubuntu 출력으로 agent:0.2.0-ca의 agent-ca healthy·healthz 정상·uid=10001·gid=0·CA 환경변수의 병합 번들 경로 및 example.com HTTPS 200을 확인했다. agent·agent-envca도 healthy, probe·tls-proxy는 Up이다. tls-proxy UI는 127.0.0.1:8082 게시를 유지한다.
- 임시 ../agent/corp-ca.crt 제거와 부재 메시지를 확인했다. certs 원본·이미지·네트워크는 유지한다. Windows·Ubuntu Dockerfile.ca 수정 후 해시는 일치했다. [사용자 성공 증거](../day08/evidence/82-ca-success-user-2026-10-01.txt).
- 8-3 이후 및 Day 8 전체 정리는 미진행이다. 아래 기동·결과 대기 문구는 이전 관찰 이력이다. Codex가 Ubuntu에서 직접 실행한 결과가 아니다.

## Day 8 CA 병합 이미지 빌드 성공 (2026-10-01)
- 사용자 Ubuntu 출력으로 간소화한 Dockerfile.ca의 Windows·Ubuntu 해시 일치와 agent:0.2.0-ca 빌드를 확인했다. default 빌더, RUN 네트워크 비활성화, 공개 CA COPY 및 update-ca-certificates 성공이다.
- agent-ca 실행·통신 시험과 임시 ../agent/corp-ca.crt 제거는 안내 후 결과 대기 중이다. certs 원본은 유지한다. [빌드 증거](../day08/evidence/82-ca-build-user-2026-10-01.txt).

## Day 8의 8-2 CA 파일 지정 성공 (2026-10-01)
- 사용자 출력으로 agent-envca의 CA 파일 지정과 example.com HTTPS HTTP 200을 확인했다. healthz 정상·원본 agent healthy, agent-envca의 Docker health 상태는 당시 starting이다. 현재 agent·agent-envca·probe·tls-proxy 네 컨테이너 유지 중이다.
- CA 병합 이미지 빌드·agent-ca 기동은 아직 하지 않았다. [해결 1 증거](../day08/evidence/82-envca-user-2026-10-01.txt). 아래 기록은 이전 단계의 관찰이다.

## Day 8의 8-2 실패 재현 확인 (2026-10-01)
- 사용자 출력으로 tls-proxy·agent·probe 실행과 agent healthz 정상(version=0.2.0)을 확인했다. ps 당시 agent는 health: starting이며 healthy 판정을 확인한 것은 아니다.
- agent의 example.com HTTPS 요청은 SSLCertVerificationError·unable to get local issuer certificate로 실패했다. 현재 세 컨테이너·네트워크·CA를 유지한다. 다음 agent-envca 기동·CA 파일 지정 시험은 안내만 했고 결과 대기 중이다. [증거](../day08/evidence/82-no-ca-user-2026-10-01.txt).

## Day 8의 8-1 완료 — 프록시 실행 중 (2026-10-01)
- 사용자 Ubuntu 출력으로 day08_closed·day08_outside 생성과 day08-tls-proxy-1의 Up 상태를 확인했다. mitmproxy/mitmproxy:11.0.0, UI 게시 127.0.0.1:8082→8081/tcp다. 다른 Day 8 서비스는 아직 기동하지 않았다.
- certs/의 CA 관련 파일 6개와 공개 인증서의 subject·issuer(CN=mitmproxy, O=mitmproxy), 유효기간 2026-09-29 13:29:25 GMT~2036-09-28 13:29:25 GMT를 확인했다. 프록시·네트워크·CA는 유지한다. HTTPS 통신·웹 화면·클라이언트 신뢰 등록은 아직 시험하지 않았다.
- Codex 직접 Ubuntu 실행이 아닌 사용자 출력 확인이다. [8-1 증거](../day08/evidence/81-startup-user-2026-10-01.txt). 아래 사전 점검의 결과 대기 문구는 기동 전 이력이다.

## Day 8 사전 점검 — Docker 연결 복구 (2026-10-01)
- 사용자 Ubuntu 출력으로 Desktop 실행 전 Docker 명령 사용 불가를 확인했다. 사용자가 Desktop 미실행을 확인하고 실행한 뒤 Client/Engine 29.8.0·Desktop 4.92.0(240144)·API 1.56·default context 응답을 제공했다. 별도 WSL 설정 변경은 보고되지 않았다.
- 기존 컨테이너 8개 모두 Exited이며 pub2에는 호스트 8081 게시 설정이 남아 있다. mitmproxy/mitmproxy:11.0.0 이미지가 존재한다. Ubuntu ss 출력의 8081·8082 리스너는 없었다. 기존 자원 변경이나 Windows 전체 포트 조회는 하지 않았다.
- OpenSSL 3.0.13 확인. Windows·Ubuntu Compose에서 web_password 제거·호스트 8082 변경을 반영했고, 사용자 출력으로 Compose config 성공 및 두 사본의 수정 후 SHA-256 일치를 확인했다. 프록시 기동·CA 생성 명령은 안내했으며 실행 결과 대기 중이다. [Day 8 SESSION](../day08/SESSION.md).

## 최신 Day 7 상태 — 종료 정리 후 (2026-09-30)
- 사용자 Ubuntu 출력으로 docker compose -p day07 down의 컨테이너 4개(agent·internal-api·probe·proxy)·네트워크 2개(closed·outside) 제거를 확인했다. 프로젝트 필터 컨테이너·네트워크 목록은 헤더만 표시됐다.
- 관찰용 mitm 제거·8082 리스너 부재와 임시 빌드 이미지·폴더 제거는 앞서 확인했다. 이미지·볼륨 삭제 옵션 및 전역 prune은 사용하지 않았다. 다른 프로젝트 자원은 이번에 재조회하지 않았다.
- Codex 직접 Ubuntu 실행·동기화가 아닌 사용자 출력 확인이다. 아래 Day 7 기동·관찰 기록은 종료 전 이력이다. [종료 정리 증거](../day07/evidence/cleanup-user-2026-09-30.txt).

## Day 7 mitm 관찰·정리 완료 (2026-09-30)
- 사용자 출력으로 mitmproxy/mitmproxy:11.0.0의 mitm 컨테이너 running을 확인했다. 초기에는 outside만 연결됐으나 후속 사용자 network connect·inspect 출력으로 day07_closed·day07_outside 양쪽 연결을 확인했다.
- 웹 포트는 호스트 127.0.0.1:8082→컨테이너 8081이다. 가이드의 8081 호스트 포트는 기존 pub2가 사용 중이어서 변경했다. v11.0.0 공식 웹 옵션에 없는 web_password는 제외하고 실행했다.
- 초기 로그는 usermod: no changes만 반환했으나 후속 사용자 출력으로 probe에서 mitm:8080을 명시한 HTTP 요청이 via mitm: 200임을 확인했다. 후속 사용자 제공 Request 탭 텍스트에서 GET http://example.com/·curl/8.7.1 등 헤더와 요청 본문 없음을 확인했다. Response 텍스트에서 HTTP 200·HTML 응답 헤더·Example Domain 본문도 확인했다. Timing에서 요청 첫 바이트→응답 완료 223ms를 관찰했다. 후속 사용자 출력으로 mitm 종료·자동 제거·8082 리스너 부재를 확인했다. 기존 Compose 네 서비스는 모두 실행 중이며 agent는 healthy다. Codex의 직접 브라우저 검증은 아니다. 기존 Compose 서비스는 유지한다. [Day 7 SESSION](../day07/SESSION.md).

## Day 7 임시 빌드 정리 완료 — 7-3 종료 (2026-09-30)
- 사용자 출력으로 default 빌더(docker 드라이버, 사전 조회 BuildKit v0.33.0)의 임시 이미지 day07-buildargs:lab 빌드 성공을 확인했다. 후속 사용자 출력으로 day07-buildargs:lab 삭제·이미지 목록 부재 및 /tmp/day07-buildargs.YTZNch 폴더 제거를 확인했다. 빌드 캐시는 정리하지 않았다. Alpine 3.20 기반 RUN echo build만 수행했다.
- 예약 프록시 인자와 일반 ARG 비교용 공개 더미 값을 사용했다. 사용자 히스토리 출력에서 일반 ARG의 더미 값이 남고 예약 HTTP_PROXY는 표시되지 않음을 확인했다. 임시 이미지·폴더 정리는 완료했으며 실제 프록시 네트워크 장애·pip 설치를 시험한 것은 아니다. [정리 증거](../day07/evidence/73-cleanup-user-2026-09-30.txt).
- buildx ls의 별도 desktop-linux 항목은 protocol not available이다. 해당 항목은 변경하지 않았고 원인은 미확정이다. 이번 빌드는 default를 명시해 성공했다. 기존 Day 7 Compose 구성은 유지한다.

## Day 7 상태 이력 — 7-1·7-2 완료 (2026-09-30)
- 사용자 Ubuntu 출력 기준: /home/user/onprem-lab/day07에서 로컬 이미지로 네 서비스를 기동했다. agent healthy 및 probe→agent healthz status=ok·version=0.2.0을 확인했다.
- day07_closed internal=true: internal-api·proxy·agent·probe. day07_outside internal=false: proxy만 연결. 호스트 포트 게시 없음.
- agent의 HTTP_PROXY·HTTPS_PROXY·http_proxy·https_proxy는 http://proxy:3128, NO_PROXY·no_proxy는 localhost,127.0.0.1,proxy,internal-api,.corp.local로 전달됐다. 7-2 사용자 출력으로 example.com HTTP/HTTPS 200(331ms/191ms), www.google.com HTTP 403·HTTPError·1ms 및 HTTPS OSError·터널 403 거부·1ms를 확인했다. Squid 접근 로그의 외부 요청 네 행(TCP_MISS/200, TCP_TUNNEL/200, TCP_DENIED/403 두 행)이 앱 결과와 일치한다. internal-api는 200·11ms이고 해당 로그에 없어 우회 설정과 일치한다. [응답·로그 증거](../day07/evidence/72-requests-and-log-user-2026-09-30.txt).
- 컨테이너 4개·네트워크 2개 유지. 사전 조회에서 기존 Day 4 pub2·web2·web은 실행 중이었고 나머지 Day 4 컨테이너 및 koica 앱은 중지 상태였다. 해당 자원은 변경하지 않았다.
- Codex 직접 Ubuntu 실행·동기화가 아닌 사용자 출력 확인이다. [Day 7 기록](../day07/SESSION.md), [검증 증거](../day07/evidence/71-config-user-2026-09-30.txt).

## 최신 Day 6 상태 — 종료 정리 후 (2026-09-30)
- 사용자 출력으로 docker compose -p day06 down의 컨테이너 7개·네트워크 3개 제거를 확인했다. Day 6 프로젝트 필터 컨테이너·네트워크 목록 및 Ubuntu의 8080 리스너 조회는 헤더만 표시됐다.
- 이미지·볼륨·임시 백업 삭제는 하지 않았다. 해당 목록과 다른 프로젝트 상태를 이번에 다시 조회한 것은 아니다. Codex 직접 Ubuntu 실행 결과와 구분한다. [정리 증거](../day06/evidence/cleanup-user-2026-09-30.txt).

## Day 6 상태 이력 — 누적 장애 복구 후, 정리 전 (2026-09-30)
- 사용자 출력 기준으로 장애 1~5번 개별 복구를 확인했다. 마지막 agent 소속은 biz·dbzone이며 healthz 정상·외부 요청 gaierror(1ms)다. 4번 복구 후 healthy·FailingStreak=0·최근 검사 5회 성공도 확인했다.
- 실습 컨테이너·네트워크와 /tmp/day06-compose.OTTiFi 백업을 유지한다. 전체 자원 정리나 마지막 시점의 모든 경로 재시험은 하지 않았다. Ubuntu에서 Codex가 직접 실행한 결과가 아니다. 상세 이력은 [Day 6 SESSION](../day06/SESSION.md) 참고.

기준일: 2026-09-29. Day 2~5 실습·정리 결과는 사용자 제공 출력과 스크린샷에 근거한다. 2026-09-23 환경 재점검은 Codex 직접 조회이며 이전 결과는 별도 이력으로 구분한다.

## Day 6 6-3 완료·원복 상태 (2026-09-29)
- 사용자 출력으로 compose.yaml과 `/tmp/day06-compose.OTTiFi`의 SHA-256이 원본 1c2e71cf3ac308e285d14ed3a2a3ab5d7dd7f0db86a82294b610bad4e69db3cb와 일치함을 확인했다.
- agent는 재생성 후 healthy이며 실제 연결은 day06_biz·day06_dbzone만 남았다. healthz status=ok·version=0.2.0·host=f4298542de49, 외부 요청은 ok=false·gaierror·7ms다. 원복 후 DB·ERP는 재시험하지 않았다.
- 6-3 원복까지 완료했다. Day 6 구성은 유지하고 백업 파일도 보존한다. 6-4 이후 및 Day 전체 정리는 미진행이다. [원복 증거](../day06/evidence/63-restored-user-2026-09-29.txt), [SESSION](../day06/SESSION.md).

## Day 6 6-3 DMZ 추가 당시 상태 (2026-09-29, 원복 전 이력)
- 사용자 출력으로 백업 `/tmp/day06-compose.OTTiFi`와 원본 compose.yaml의 SHA-256 일치를 확인한 뒤 agent의 networks 한 줄만 변경·재적용했다. Windows 실습 소스는 원본을 유지한다.
- DMZ 추가 당시 agent는 biz·dbzone·dmz에 연결됐으며 healthy였다. gateway 경유 healthz는 status=ok·version=0.2.0·host=8faa0748aa9d, 외부 example.com 요청은 ok=true·HTTP 200·105ms였다.
- 이후 원복을 확인했으므로 이 구성은 과거 재현 이력이다. [재현 증거](../day06/evidence/63-dmz-added-user-2026-09-29.txt), [SESSION](../day06/SESSION.md).

## Day 6 6-2 완료·통신 확인 (2026-09-29, DMZ 추가 전 이력)
- 사용자 Ubuntu 출력으로 gateway 경유 healthz status=ok·version=0.2.0·host=b03497230cb3 및 agent→postgres:5432 TCP ok=true·elapsed_ms=1을 확인했다. DB 인증·SQL은 미시험이다.
- ③ DMZ→DB 이름 기반 접속은 getaddrinfo Try again·종료코드 1로 실패했다. DB IP 172.22.0.4:5432 직접 시도도 3초 타임아웃·종료코드 1이다. 예상한 접근 제한은 확인했으며 특정 방화벽 규칙을 조회한 것은 아니다. ④ probe-biz에서 example.com DNS 실패·코드 1을 확인했고 IPv4 라우팅에는 172.21.0.0/16 직접 연결 경로(src 172.21.0.2)만 있고 default가 없다. 외부 IP 직접 연결·IPv6는 미시험이다. ⑤ 실제 agent→ERP HTTP 200·Name: erp-api를 확인했다. ERP IP는 172.21.0.5, 요청 RemoteAddr는 172.21.0.3:57002다. ⑥ agent의 example.com 요청은 ok=false·gaierror·이름 해석 실패·8ms다. 모든 외부 IP·포트를 시험한 것은 아니다. ⑦ probe-db→agent(172.22.0.3):8000 신규 TCP 연결은 succeeded·종료코드 0이다. 6-2 완료이며 실습 구성은 유지한다. 6-3 이후는 미진행이다. [⑦ 증거](../day06/evidence/connectivity-07-user-2026-09-29.txt). [⑥ 증거](../day06/evidence/connectivity-06-user-2026-09-29.txt). [⑤ 증거](../day06/evidence/connectivity-05-user-2026-09-29.txt). [④ 증거](../day06/evidence/connectivity-04-user-2026-09-29.txt). [①② 증거](../day06/evidence/connectivity-01-02-user-2026-09-29.txt), [③ DNS 증거](../day06/evidence/connectivity-03-dns-user-2026-09-29.txt), [③ IP 증거](../day06/evidence/connectivity-03-ip-user-2026-09-29.txt).

## Day 6 6-1 완료·실행 상태 (2026-09-29)
- 사용자 up·ps·network inspect 출력으로 네트워크 3개와 컨테이너 7개 생성·기동을 확인했다. 모두 Up이고 agent·postgres는 healthy다. gateway가 127.0.0.1:8080→80을 게시한다.
- day06_dmz internal=false: gateway·probe-dmz. day06_biz internal=true: gateway·erp·agent·probe-biz. day06_dbzone internal=true: agent·postgres·probe-db. 소속이 구성과 일치한다.
- 6-1 완료이며 구성은 실행 중이다. 6-2 실제 통신·차단 시험은 미진행이다. Codex 직접 Ubuntu 실행·재조회와 구분한다. [기동 증거](../day06/evidence/startup-user-2026-09-29.txt), [SESSION](../day06/SESSION.md).

## Day 6 사전 점검 (2026-09-29, 기동 전 이력)
- 사용자 Ubuntu 출력으로 Day 6 파일 3개(compose.yaml·gateway.conf·break.sh)의 SHA-256이 Windows 사본과 일치함을 확인했다. break.sh는 755이며 동일 해시의 Windows 파일은 LF다.
- Docker Client/Engine 29.8.0, Desktop 4.92.0(240144), Compose v5.5.1, Compose 문법 검사 성공 및 필요 이미지 5개의 linux/amd64 로컬 존재를 확인했다.
- Ubuntu 8080 리스너와 Docker의 8080 게시가 없다. pub2(8081 게시)·web·web2는 실행 중이고 pub·isolated·client·client2·기존 koica 앱은 중지 상태로 남아 있다. 기존 자원 변경·파일 동기화는 수행하지 않았다.
- 이 사전 점검 뒤 6-1 기동을 안내했고 후속 출력으로 위 실행 상태를 확인했다. [사전 점검 증거](../day06/evidence/precheck-user-2026-09-29.txt), [SESSION](../day06/SESSION.md).

## Day 5 종료 상태 (2026-09-29)
- 사용자 compose down 출력으로 day05-nginx-1·day05-agent-1·day05-postgres-1 및 day05_default 제거를 확인했다. compose ps -a·해당 네트워크 목록은 헤더만 남았고 Ubuntu ss에 8080 LISTEN 행이 없다.
- day05_pgdata 볼륨은 local로 존재한다. 이미지와 프롬프트 임시 백업 /tmp/day05-prompt.GrrBHr는 삭제 대상으로 지정하지 않았으며 이번 단계에서 재조회하지 않았다. 프롬프트 원복은 앞선 파일 비교·API·해시로 확인했다.
- Day 4 잔존 자원·기존 koica 자원은 정리 범위에 포함하지 않았다. 아래 실행 중 상태는 실습 당시 이력이며 Day 5의 현재 컨테이너 실행 상태가 아니다.
- 5-1~5-4·지정 자원 정리를 완료해 사용자 요청에 따라 Day 5를 종료했다. 일부 TUI 상세 관찰과 별도 자기점검 평가는 미확인으로 남긴다. [정리 증거](../day05/evidence/cleanup-user-2026-09-29.txt), [SESSION](../day05/SESSION.md).

## Day 5 사전 점검 및 Day 4 자원 잔존 (2026-09-29)
- 사용자 Ubuntu 출력에서 Docker Client/Engine 29.8.0, Desktop 4.92.0(240144), Compose v5.5.1 및 Compose 문법 검사 성공을 확인했다. Day 5 실습 파일 5개의 SHA-256은 Windows 사본과 일치한다.
- 사전 점검에서 이전 Day 4 정리 완료 진술과 달리 pub·pub2·web·web2가 실행 중이며 isolated·client·client2도 중지된 상태로 남아 있었다. 이후 pub 중지를 확인했고 lazydocker 화면에는 lab-net·other-net도 보였다. 과거 진술과 다른 경위는 미확인이다. Day 4 자원 정리 완료로 간주하지 않는다.
- 사전 점검에서 pub는 127.0.0.1:8080→80, pub2는 8081→80을 게시했고 Ubuntu ss에도 127.0.0.1:8080 LISTEN이 표시됐다. 후속 사용자 출력으로 pub 중지 및 ss의 8080 리스너 부재를 확인했다. 실행 중 목록에는 pub2·web2·web이 남아 있다.
- Day 5 적용 이미지는 agent:0.2.0·postgres:16.4-alpine·nginx:1.27-alpine이다. 후속 사용자 up·ps 출력으로 day05_default 네트워크·day05_pgdata 볼륨 생성, agent·postgres healthy 및 nginx 실행·127.0.0.1:8080→80 게시 성공을 확인했다.
- 후속 API 출력으로 healthz의 status=ok·version=0.2.0, prompt_exists=true·prompt_sha=258e1f7baff4·rubric 내용·db_dsn_set=true, postgres:5432의 TCP ok=true·elapsed_ms=1을 확인해 5-1 완료. DB 인증·SQL·영속성 시험은 미진행이다.
- 5-2 ① 사용자 출력으로 agent의 /_lab/exit 후 RestartCount 0→1, health starting→healthy 및 healthz 정상 응답을 확인했다. 컨테이너 생성 시각과 host a105f231277a는 유지됐다.
- ② 사용자 출력에서 postgres 중단(Exited 0) 중에도 agent healthy·healthz ok이나 DB TCP는 gaierror(Temporary failure in name resolution)였다. postgres 재기동 후 Up 12 seconds (healthy)·TCP ok=true·elapsed_ms=0을 확인했다.
- ③ 첫 조회부터 RestartCount=1·unhealthy였고 hang 요청은 10초 타임아웃이었다. 40초 후에도 횟수 1·unhealthy 및 healthz 3초 타임아웃(코드 28)을 확인했다. 수동 restart 후 agent Up 12 seconds (healthy)·healthz ok·DB TCP ok=true로 복구됐다. 처음 무응답의 원인은 미확정이다.
- ③ 재확인에서는 RestartCount=0·healthy → hang=true 응답 → 40초 후 RestartCount=0·unhealthy 및 healthz 3002ms 타임아웃(코드 28)을 확인했다. 수동 restart 후 agent Up 10 seconds (healthy), nginx Up 31 minutes, postgres Up 11 minutes (healthy) 및 healthz ok로 복구돼 5-2 완료. 마지막 복구 후 DB TCP는 재조회하지 않았다. Day 5 서비스·네트워크·볼륨은 유지 중이다.
- 5-3 사용자 출력으로 Ubuntu config/prompt.txt의 한 줄 추가가 /prompt에 반영되고 prompt_reloaded sha가 258e1f7baff4→a9099fd31924로 바뀐 것을 확인했다. 이미지 ID a4ef49ae142e… 및 StartedAt=2026-09-29T00:48:28.108529054Z, RestartCount=0·healthy는 유지됐다. 후속 cp·cmp·API 출력으로 백업 /tmp/day05-prompt.GrrBHr와 파일 일치, 원본 두 문장·sha=258e1f7baff4 복귀를 확인해 5-3 완료. 임시 백업은 삭제하지 않았고 Windows prompt.txt는 원본을 유지한다.
- 기존 koica 앱은 사전 조회에서 Exited (143) 2 weeks ago이며 변경하지 않았다. Codex가 Ubuntu 명령을 직접 실행하거나 파일을 동기화하지 않았다. 상세는 [Day 5 SESSION](../day05/SESSION.md)을 참고한다.

## Day 4 종료 상태와 네트워크 관찰 (2026-09-28)
- Day 4 컨테이너 web·client·web2·client2·isolated·pub·pub2 및 lab-net·other-net의 삭제와 목록·포트 조회를 안내했고 사용자가 “완료했어”라고 확인했다. 종료 출력 원문은 미제공이므로 현재 목록·리스너 부재를 Codex가 검증한 것은 아니다. 아래 주소·연결 정보는 실습 당시 관찰이다. 기존 koica 자원·이미지·볼륨은 정리 대상에 포함하지 않았다.
- lazydocker 0.25.2의 사용자 lab-net·other-net 화면은 모두 Containers: none 및 서브넷 미표시였지만, Docker inspect는 lab-net의 client·web·isolated와 other-net의 isolated를 보고했다. 양쪽 연결은 직접 조회 출력으로 확인했으며 두 화면을 증거로 보존해 관찰을 마쳤다. 화면 표시 불일치의 내부 원인은 미확정이다. 업데이트·설정 변경은 수행하지 않았다.
- Ubuntu IP는 `172.18.60.227`, Docker bridge는 `172.17.0.0/16`, 기존 koica-oda-local-test_default는 `172.18.0.0/16`, lab-net은 `172.19.0.0/16`, other-net은 `172.20.0.0/16`이다. Ubuntu IP와 기존 koica Docker 대역의 겹침을 확인했다. koica 자원은 변경하지 않았다.
- Ubuntu의 Python 9999 서버를 127.0.0.1에서 0.0.0.0으로 바꾸자 Ubuntu 자체의 비루프백 IP 요청은 코드 7에서 HTTP 200으로 바뀌었다. 컨테이너의 Ubuntu IP 직접 요청은 변경 전후 모두 연결 시간 초과(코드 28)였다. 대역 겹침은 경로 충돌 후보이며 패킷 경로·방화벽의 상세 원인은 미검증이다.
- Docker Desktop 기본 host.docker.internal 경로는 Ubuntu 서버가 루프백에 바인딩된 상태에서도 실습 본문·HTTP 200을 반환했다. getent의 IPv6 결과는 `fdc4:f303:9324::254`였으나 0.0.0.0으로 바인딩을 바꾼 뒤 마지막 curl은 HTTP 200과 실제 remote_ip `192.168.65.254`를 반환했다. 이름 조회 결과와 실제 접속 주소를 구분하며 가이드 Linux Docker Engine의 실패 예상과도 구분한다.
- 4-4 임시 Python 서버(PID 1904)는 종료했다. 사용자 출력의 ps·ss에 헤더만 남아 프로세스 및 Ubuntu 9999 리스너 부재를 확인했다. 임시 폴더 `/tmp/day04-http.fdpmdu`와 로그는 삭제 대상에 포함하지 않았다. Docker 실습 자원 정리는 위 사용자 완료 진술과 구분해 기록한다. 상세 명령·범위는 [Day 4 SESSION](../day04/SESSION.md)에 있다.

## Day 3 종료 상태 (2026-09-27)
- 사용자 출력으로 Docker Client/Engine 29.8.0, Desktop 4.92.0(240144), API 1.56 및 화면으로 lazydocker 0.25.2의 정상 작동을 확인했다. 시작 시 WSL 연동 오류가 있었으나 후속 명령 성공으로 복구를 확인했다. Windows 조작 상세는 미제공이다.
- agent:0.2.0을 python:3.12.14-slim으로 빌드했다. Python 3.12.14, 스캔 식별 OS Debian 13.7, linux/amd64, UID 10001·GID 0, 이미지 크기 181278388바이트를 확인했다.
- Trivy 0.56.2의 사용자 결과: 초기 agent:0.1.0은 HIGH 95·CRITICAL 9, 새 이미지는 HIGH 44·CRITICAL 0, --ignore-unfixed 적용 시 0건. 실제 영향 평가·예외 승인과 구분한다.
- 종료 조회로 agent:0.1.0·0.2.0 보존, 정확한 이름 agent의 컨테이너와 leak:1 이미지 부재를 확인했다. 앞서 day03/leak/x·leak.tar 제거도 확인했다. [정리 증거](../day03/evidence/cleanup-user-2026-09-27.txt).
- day03/leak의 가짜 비밀 연습 소스와 day03의 스캔 로그·trivy-cache는 삭제 대상으로 지정하지 않았다. 캐시 전체 삭제나 비밀의 복구 불가능한 삭제를 수행한 것은 아니다. 화면의 기존 koica 자원은 이번 실습 정리 대상이 아니다.
- Windows 기록과 Ubuntu 실습 폴더는 별도다. 전체 결과와 범위는 [Day 3 SESSION](../day03/SESSION.md), [반입 초안](../day03/IMPORT-PACKAGE.md)을 참고한다.

## Day 2 종료 상태 (2026-09-25)
- 실습 2-1~2-7 완료. 사용자 정리 출력으로 who1·who2·lim·demo-net 삭제 및 빈 ip netns list를 확인했다. 기존 koica 프로젝트는 정리 대상에 포함하지 않았다.
- 첫 재확인 시 세 명령이 구분자 없이 한 줄로 붙어 sysctl 옵션 오류가 발생했으나 세미콜론으로 구분해 재실행했다. 후속 사용자 출력은 `net.ipv4.ip_forward = 0`, NAT는 `-P POSTROUTING ACCEPT`만 표시, 브리지 목록은 빈 출력이었다. 사전 전달 설정 복구와 실습 NAT·브리지 제거까지 확인해 정리를 완료했다.
- 아래 2026-09-24의 실행 중 구성은 실습 당시 관찰 이력이며 현재 잔존 상태를 뜻하지 않는다. [정리 증거](../day02/evidence/day02-cleanup-user-2026-09-25.txt), [전체 기록](../day02/SESSION.md).

## Day 2 실습 당시 상태 (2026-09-24)
- 2-6 사전 조회에서 Docker 명령 네 개 모두 WSL integration 안내 오류로 실패했으나, Desktop 실행 안내 후 사용자 docker version 출력으로 Client·Engine 29.8.0, API 1.56, Desktop 4.92.0 (240144), linux/amd64, Context default 및 Client·Server 응답을 확인해 복구됐다. Windows에서 수행한 조작 상세는 미제공이다. 이후 사전 조회와 2-6 실습도 사용자 출력으로 확인했다.
- 사용자 출력으로 2-1~2-7 완료를 확인했다. Day 전체 자원 정리·자기점검은 남아 있다. Ubuntu의 biz·db 네임스페이스, br-lab(10.42.0.1/24), veth 연결 및 biz(10.42.0.10/24)·db(10.42.0.20/24)의 통신을 확인했다. biz의 기본 경로는 10.42.0.1이며 db 기본 경로는 추가하지 않았다.
- 2-7에서 lim을 --memory=64m·--rm·sleep 3600으로 실행했다. stats는 416KiB / 64MiB, 0.63%, PIDS 1이며 cgroup 상한 조회는 67108864바이트였다. 제한 값 일치를 확인했으며 OOM은 시험하지 않았다. lim은 아직 수동 정리하지 않았다.
- 2-6의 Docker 엔진 관찰에서 demo-net(172.19.0.0/16·게이트웨이 172.19.0.1), who1(172.19.0.2/16), br-0256008dc546·veth 포트 및 해당 대역 MASQUERADE를 확인했다. who1은 DNS 127.0.0.11에서 자기 이름 조회 성공, 기본 bridge의 who2는 DNS 192.168.65.7에서 NXDOMAIN이었다. who1·who2는 --rm·sleep 3600으로 실행했고 demo-net과 함께 아직 수동 정리하지 않았다. 시간 경과 시 잔존 상태를 확인한다. 기존 koica 프로젝트는 정리 대상이 아니다.
- 2-5에서 tcpdump 미검출 후 설치를 안내했고 사용자 버전 출력으로 tcpdump 4.99.4·libpcap 1.10.4·OpenSSL 3.0.13을 확인했다. db TCP 5432의 nc 리스너로 접속하며 SYN·SYN-ACK와 TCP 연결 성공을 관찰했다. 이후 캡처 작업 종료 및 리스너 PID 2129 종료·LISTEN 해제를 확인했다. 실제 PostgreSQL 서버를 설치한 것은 아니다.
- iptables 명령 미검출 후 설치를 안내했고, 후속 출력에서 v1.8.10 (nf_tables)과 규칙 조회 성공을 확인했다. apt 설치 로그는 미제공이다. nc 경로는 /usr/bin/nc다.
- 설정 전 ip_forward=0, FORWARD 기본 ACCEPT·개별 규칙 없음, NAT POSTROUTING 개별 규칙 없음을 확인했다. 이후 사용자가 ip_forward=1과 `-s 10.42.0.0/24 ! -o br-lab -j MASQUERADE` 규칙 한 개를 설정했다.
- biz에서 `nc -zv -w3 1.1.1.1 443` 성공·종료 코드 0. DNS·TLS·HTTP 및 외부 ping 성공까지 검증한 것은 아니다. Ubuntu 경로 조회는 `via 172.18.48.1 dev eth0 src 172.18.60.227`이었다.
- 실습 구성은 유지 중이다. 최종 정리 시 실습 NAT·네트워크 제거 및 ip_forward의 사전 값 0 복구를 포함한다. 영구 설정은 추가하지 않았다. Codex가 Ubuntu 설정을 직접 변경하거나 재시험하지 않았다. 상세 명령·출력은 [Day 2 SESSION](../day02/SESSION.md)에 기록했다.

## 현재 상태 — Docker Desktop 실행 후 (2026-09-23)
- Day 1의 1-3 사용자 출력으로 Ansible core 2.21.4를 `/home/user/onprem-lab/day01/.venv/bin/ansible`에서 확인했다(Python 3.12.3, Jinja 3.1.6, PyYAML 6.0.3). community.docker 5.3.0은 `/home/user/.ansible/collections/ansible_collections`에 설치돼 있다. 후속 사용자 출력에서 두 대상 연결 SUCCESS·pong, 첫 플레이북 실행 ok=5·changed=3·failed=0·unreachable=0, 두 번째 실행 ok=5·changed=0·failed=0·unreachable=0을 확인했다. 내부 별도 조회에서도 appuser UID 10001·nologin, 디렉터리 appuser:root·0750, 예시 설정 파일 root:root·0644를 확인했다. [내부 상태 증거](../day01/evidence/day01-13-state-user-2026-09-23.txt). 컨테이너 삭제와 deactivate 실행 결과는 아직 없으며 현재 실행 여부를 재조회하지 않았다.
- Day 1의 1-3 사전 확인 사용자 출력: Docker Desktop 4.92.0(240144), Docker Client/Engine 29.8.0, API 1.56(서버 최소 1.40), linux/amd64, Python 3.12.3. Ubuntu day01의 inventory.ini·prepare-vm.yaml 두 파일은 Windows 사본과 SHA-256이 일치한다. 이번에는 사용자 제공 출력이며 Codex가 Ubuntu에서 직접 재실행한 것이 아니다. [증거](../day01/evidence/day01-13-precheck-user-2026-09-23.txt).
- 후속 0-4 실습에서 lazydocker 0.23.3의 API 1.25 고정 사용과 Docker 최소 API 1.40 사이의 호환 오류를 확인했다. 사용자가 `/usr/local/bin/lazydocker`를 공식 바이너리 0.25.2(linux/amd64)로 교체한 뒤 오류 없이 이미지·네트워크 목록이 표시되는 화면을 제공했다. `agent:0.1.0`은 화면상 189.09MB이며 기본 네트워크 bridge·host·none이 모두 보인다.
- lazydocker의 실제 설치 버전은 이제 0.25.2다. 가이드와 bootstrap.sh의 0.23.3 고정값은 수정하지 않았으므로 새 환경 설치 시 동일한 호환 오류가 재발할 수 있다. `check`의 버전 출력 성공만으로 TUI 동작을 보장할 수 없다.
- 사용자가 Docker Desktop 실행을 알린 뒤 Codex가 Ubuntu에서 직접 재점검했다. `./bootstrap.sh check` 전 항목 통과, 종료 코드 0이다.
- Docker Client / Server 모두 29.8.0, Docker Compose v5.5.1, kubectl Client v1.36.1. Docker Engine은 가이드의 27 이상 조건을 충족한다.
- 가이드 고정값과의 차이는 kubectl 1.36.1 대 1.31.0, dive 0.13.1 대 본문 0.12.0, Compose 5.5.1 대 v2 표기다. check는 실제 Compose 버전에 상관없이 성공 문구를 `docker compose v2`로 출력한다. 향후 실습 호환성을 검증한 것은 아니다.
- Docker 소켓은 root:docker, 660이고 현재 사용자 그룹에 docker가 포함돼 있다. 추가 권한 변경 없이 Docker 엔진이 응답한다.
- bootstrap.sh에 지정된 이미지 12개 모두 `docker image inspect`로 직접 존재를 확인했다. 다운로드나 컨테이너 실행은 하지 않았다.
- 이전 Docker·kubectl 미검출은 Desktop 실행 후 해소됐다. 아래 초기 점검 실패는 이력으로 보존한다.

## 초기 재점검 결과 — Docker Desktop 실행 전 (2026-09-23)
- Windows 11 Pro 10.0.26200, 물리 RAM 약 31.18GiB, C: 여유 약 454.53GiB. 가이드의 PC 자원 권장치 이상이다.
- Ubuntu 24.04.1 LTS, WSL2, 커널 `5.15.167.4-microsoft-standard-WSL2`. WSL 메모리는 약 15GiB, `/`의 가상 디스크 여유 표시는 954GiB다. 실제 호스트 여유와 구분한다.
- 초기 `wsl --list --verbose`에서 Ubuntu와 docker-desktop은 모두 Stopped, VERSION 2였다. 조회를 위해 Ubuntu를 실행했다. Windows에서 Docker Desktop과 com.docker.backend 프로세스는 검출되지 않았다.
- Ubuntu의 `./bootstrap.sh check` 결과는 종료 코드 1: kubectl 미검출, Docker 데몬 연결 실패, Compose 실행 실패. Docker 줄의 ✓는 Windows 측 안내용 명령이 PATH에 있다는 뜻이며 정상 동작을 입증하지 않는다.
- `/usr/bin/docker`와 `/usr/local/bin/kubectl`은 `/mnt/wsl/docker-desktop/cli-tools/...`를 가리키지만 현재 해당 마운트 경로가 없다. `/var/run/docker.sock`도 없다. 현재 사용자 그룹에는 docker가 포함돼 있다.
- k3d v5.7.4, helm v3.16.2, k9s v0.32.5, lazydocker 0.23.3, dive 0.13.1, jq 1.7, curl 8.5.0, git 2.43.0, Python 3.12.3, iproute2 6.1.0을 직접 확인했다.
- `/home/user/onprem-lab/bootstrap.sh`는 755, LF이며 Windows 사본과 SHA-256이 일치한다. agent, day01~day13, skeleton 디렉터리도 존재한다. 전체 소스의 일치 여부까지 검사한 것은 아니다.
- 이 초기 점검에서는 엔진에 연결되지 않아 이미지 12개를 재확인하지 못했다. 이후 Desktop 실행 후 모두 확인했다(위 현재 상태 참고).
- 설치·다운로드·버전 변경·컨테이너 실행은 하지 않았다. [직접 점검 증거](../day00/evidence/local-check-2026-09-23.txt)를 참고한다.

## 실행 위치와 파일 위치
- 호스트: Windows 11 Pro, 컴퓨터 이름 DESKTOP-6KJVBND. RAM·디스크는 위 재점검 결과 참고.
- 리눅스: Ubuntu 24.04.1 LTS, WSL2, linux/amd64.
- Ubuntu 사용자: user
- 현재 실습 디렉터리: `/home/user/onprem-lab`
- 2026-09-23 사용자 제공 0-5 목록: agent, bootstrap.sh, day01~day13, skeleton 존재. Ubuntu에 day14는 없으며 Day 14 실습 시작 경로는 skeleton이다. Windows의 Day별 기록 폴더와 구분한다.
- Windows 프로젝트 디렉터리: `C:\Users\user\Desktop\Applications\25. BCG X\7. 준비\12. Deploy Practice`
- Windows 폴더와 Ubuntu 폴더는 별도 복사본이며 자동 동기화되지 않는다. 이후 코드 변경 시 어느 쪽을 수정했는지 기록하고 반영한다.
- bootstrap.sh 원본의 LAB은 `${HOME}/onprem-lab`이다. 이 프로젝트를 Windows에 배치했다고 실습 위치가 변경되지는 않는다.
- Docker Desktop은 Windows에서 실행하고 Ubuntu WSL Integration을 사용한다.

## 이전에 확인된 도구 (2026-09-22 사용자 제공 출력)
| 도구 | 실제 결과 | 비고 |
|---|---|---|
| Docker Desktop | 4.90.0 (238679) | Server 출력 |
| Docker Engine / CLI | 29.7.2 | Client와 Server 응답 |
| Docker Compose | v5.5.1 | docker compose 명령 확인 |
| kubectl | v1.36.1 | 가이드 고정값 v1.31.0과 다름; 미조정 |
| k3d | v5.7.4 | 설치 확인; 클러스터는 아직 만들지 않음 |
| helm | v3.16.2+g13654a5 | 설치 확인 |
| k9s | v0.32.5 | 설치 확인 |
| lazydocker | 0.23.3 | 설치 확인 |
| dive | 0.13.1 | 첨부 스크립트 설정과 일치, 본문의 0.12.0과 다름 |
| jq | 1.7 | 설치 확인 |
| curl | 8.5.0 | 설치 확인 |
| git | 2.43.0 | Ubuntu 출력 |
| python3 | 3.12.3 | Ubuntu 출력 |
| iproute2 | ip 명령 존재 | 버전 미기록 |

## 알려진 차이와 남은 확인
- Ansible 2.21.4의 Day 1 첫 실행에서 Python 인터프리터 자동 탐색 경고와 INJECT_FACTS_AS_VARS 변경 예고가 표시됐다. 후자는 가이드 prepare-vm.yaml의 top-level facts 참조 방식 때문이며 출력은 2.24에서 제거 예정이라고 알린다. 현재 실행은 성공했으며 향후에는 ansible_facts 사전 참조로 수정할 필요가 있다. 이번에는 동일 플레이북 재실행 확인을 위해 소스를 변경하지 않았다.
- Day 1의 1-3에서 `python3 -m venv .venv`가 ensurepip 불가로 실패했다. 이후 사용자 출력으로 `python3.12-venv` 3.12.3-1ubuntu0.17, `python3-pip-whl` 24.0+dfsg-1ubuntu1.3, `python3-setuptools-whl` 68.1.2-2ubuntu1.2 설치 완료를 확인했다. 기존 패키지 업그레이드는 없었다. 재실행 후 가상환경 생성·활성화에 성공했고 Python은 `/home/user/onprem-lab/day01/.venv/bin/python`, pip 24.0은 같은 .venv의 Python 3.12 경로를 가리켰다. ensurepip 오류 해소 확인. 후속 Ansible·community.docker 설치 버전도 사용자 출력으로 확인했다(위 현재 상태 참고). [오류·대응 기록](../day01/SESSION.md) 참고.
- check의 ✓는 고정 버전 일치나 모든 후속 실습의 호환성을 보장하지 않는다.
- kubectl 버전 차이는 해결되지 않은 항목으로 유지한다.
- 가이드의 k3s v1.30 클러스터는 아직 생성·검증하지 않았다.
- 실제 소켓 권한은 root:docker, 660이었고 user는 docker 그룹에 등록돼 있었다. newgrp docker로 현재 셸에 적용한 뒤 연결됐다.
- 실습 이미지 12개 존재는 [최종 사용자 출력](../day00/evidence/bootstrap-final.txt)에 기록했다. 이미지 바이트는 이 프로젝트 폴더로 복사하지 않았다.
- 원본 가이드의 검증 주장과 이 PC에서 실제 확인한 결과를 구분한다.
