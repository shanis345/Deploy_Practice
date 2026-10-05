# 진행 현황

- 기준일: 2026-10-05

## 최신 요약

- **Day 10: 10-1~10-6·k9s·정리 완료.** 체크포인트 6개 해설 제공, 독립 이해도 평가 미진행. [핵심 요약](day10/README.md) · [상세 기록](day10/SESSION.md).
- 최종 사용자 출력은 agent 0.2.0/2개 준비·Service 유지, 고장 예제·probe 삭제 상태다. 클러스터·레지스트리는 유지했으며 이번 PR 작업에서 Ubuntu 실습을 재실행하지 않는다.
- Day 10 기록을 `9329b74`로 커밋·push하고 [PR #12](https://github.com/shanis345/Deploy_Practice/pull/12)를 생성했다. `codex/day10-results` → `main`, OPEN·리뷰 대기 상태다. 다음 Day 진행과 main 병합은 별도다.

## 진행 이력

아래는 최신순으로 누적한 당시 상태다. 이전 항목의 “미완료/대기”를 현재 상태로 해석하지 않는다.

- Day 10 체크포인트 해설(2026-10-05): 사용자 요청으로 6개 문항의 복습 답안을 제공했다. Day 5 장애와 readiness/liveness, VM HA와 롤링 업데이트의 역할 차이 등을 구분했다. 실습·k9s·정리는 완료이며 해설 제공을 독립 이해도 평가 통과로 간주하지 않는다. [SESSION](day10/SESSION.md).
- **Day 10 최종 정리 완료(2026-10-05 사용자 출력):** probe 삭제·부재 및 정상 agent 0.2.0/2개 준비·Service 10.43.162.127:8000 유지를 확인했다. 10-1~10-6·k9s·정리 완료, 체크포인트는 미진행이다. 앱·클러스터·레지스트리는 Day 11을 위해 유지한다. [SESSION](day10/SESSION.md).
- Day 10 최종 정리 안내(2026-10-05): 사용자 요청으로 probe Pod만 일반 삭제 후 Deployment/Pod/Service 조회를 안내했다. 실행 결과 대기 중이며 앱·Service·Namespace·클러스터·레지스트리·이미지는 유지한다. 체크포인트/Day 10 전체 완료는 아직이다. [SESSION](day10/SESSION.md).
- **Day 10 k9s 조회 완료(2026-10-05):** 사용자 캡처로 Pod·Describe·로그·Deployment를 확인했고, 사용자 텍스트로 Service agent의 ClusterIP/10.43.162.127/8000 TCP 일치 및 k9s 종료를 확인했다. 10-1~10-6 및 k9s 완료, probe 최종 정리·체크포인트는 미진행이다. [SESSION](day10/SESSION.md).
- Day 10 k9s Deployment 확인(2026-10-05 사용자 캡처): agent의 READY 2/2·UP-TO-DATE 2·AVAILABLE 2를 확인했다. 다음은 k9s :svc·Enter로 Service 목록 조회이며 사용자 화면 대기 중이다. [SESSION](day10/SESSION.md).
- Day 10 k9s 로그 확인(2026-10-05 사용자 캡처): pwrhg 현재 로그에서 GET /healthz의 반복 HTTP 200을 확인했다. 다음은 k9s에서 Esc 후 :deploy·Enter로 Deployment 목록 확인이며 화면 대기 중이다. [SESSION](day10/SESSION.md).
- Day 10 k9s Describe 확인(2026-10-05 사용자 캡처): pwrhg의 0.2.0 이미지·현재 Running/Ready=True·재시작 1·/healthz probe 설정을 확인했다. 이전 종료 Error/137과 현재 상태를 구분했다. 다음은 Esc로 목록 복귀 후 l로 현재 로그 확인이며 화면 대기 중이다. [SESSION](day10/SESSION.md).
- Day 10 k9s 첫 화면 확인(2026-10-05 사용자 캡처): k3d-onprem/ax-pilot의 agent Pod 두 개 1/1 Running·재시작 1/0 및 probe Running·AGE 59m를 확인했다. 선택된 pwrhg에서 d로 Describe 화면을 열도록 안내했고 결과 대기 중이다. k9s 전체 실습은 아직 미완료다. [SESSION](day10/SESSION.md).
- Day 10 k9s 사전 확인 완료(2026-10-05 사용자 출력): /usr/local/bin/k9s v0.32.5, kubectl v1.31.0, 정상 agent 0.2.0/2개 준비, probe Running·AGE 57m를 확인했다. context/namespace를 지정한 --readonly Pod 화면 실행을 안내했고 첫 화면 확인 대기 중이다. [SESSION](day10/SESSION.md).
- Day 10 k9s 시작(2026-10-05): 사용자 요청으로 k9s 경로/버전 및 현재 Deployment/Pod 사전 조회를 안내했다. 결과 대기 중이며 설치·UI 실행·리소스 변경은 아직 하지 않았다. 10-1~10-6 완료, Day 전체 미완료를 유지한다. [SESSION](day10/SESSION.md).
- **Day 10의 10-6 완료(2026-10-05 사용자 출력):** 고장 Deployment 5개 삭제 및 b-* Deployment/ReplicaSet/Pod 부재, 정상 agent 0.2.0/2개 준비·Service 유지 확인. 10-1~10-6 완료, k9s·Day 전체 정리·체크포인트는 아직이다. probe·클러스터·레지스트리는 유지하며 다음 범위는 사용자 요청 대기다. [SESSION](day10/SESSION.md).
- Day 10의 10-6 NotReady 확인(2026-10-05 사용자 출력): 앱 Running·재시작 0이나 readiness /health에서 404가 반복돼 Ready=False다. 소스의 정상 경로 /healthz와 비교해 다섯 예제 진단을 확인했다. 지정 고장 리소스 삭제·정상 앱 유지 조회를 안내했고 결과 대기 중이다. 10-6 완료는 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-6 ConfigError 확인(2026-10-05 사용자 출력): b-configerror는 노드 배정·이미지 준비 후 필수 Secret agent-secret-typo 부재로 시작하지 못한다. 재시작 0, Events의 secret not found를 확인했다. 다음은 b-notready describe이며 마지막 진단·정리는 미완료다. [SESSION](day10/SESSION.md).
- Day 10의 10-6 Pending 확인(2026-10-05 사용자 출력): CPU 64/memory 512Gi 요청에 세 노드 모두 Insufficient cpu/memory, PodScheduled=False·Node/IP 없음이다. 고장 예제 3개 진단을 확인했고 다음은 b-configerror describe다. 나머지 진단·정리는 미완료다. [SESSION](day10/SESSION.md).
- Day 10의 10-6 CrashLoop 확인(2026-10-05 사용자 출력): b-crashloop는 명시적 sys.exit(1)로 종료, 재시작 6, 이전 로그에 설정 누락 문구가 있다. 실제 파일 검사 실패가 아닌 오류 재현용 명령이다. 다음은 b-pending describe이며 10-6 나머지 진단·정리는 미완료다. [SESSION](day10/SESSION.md).
- Day 10의 10-6 이미지 태그 확인(2026-10-05 사용자 첨부 출력): HTTP mirror 설정 존재 및 9.9.9 manifest의 MANIFEST_UNKNOWN/404를 확인했다. containerd 로그에는 최종 HTTPS 오류가 있으며 fallback 설명과 부합한다. 다음은 b-crashloop describe·logs --previous이며 수정·정리는 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-6 이미지 진단(2026-10-05 사용자 출력): b-imagepull은 노드 배정 후 Waiting/ImagePullBackOff이며 Events에 HTTPS 요청/HTTP 응답 오류가 있다. 태그 부재 후 fallback인지 구분하기 위해 HTTP mirror 설정·manifest 응답·server-0 containerd 로그 조회를 안내했다. 결과 대기 중이며 수정·정리는 하지 않았다. [SESSION](day10/SESSION.md).
- Day 10의 10-6 고장 재현(2026-10-05 사용자 출력): 예제 5개 Deployment 생성 완료. ErrImagePull, CrashLoopBackOff, Pending, CreateContainerConfigError, Running 0/1을 관찰했고 정상 agent는 2/2다. 다음은 b-imagepull describe/Events 확인이며 원인 진단·정리는 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-6 사전 확인(2026-10-05 사용자 출력): 예제 5개 체크섬 OK·정상 agent 2/2·기존 b-* Deployment/Pod 부재·probe Running을 확인했다. 지정 파일 5개 apply 후 60초 대기·리소스 조회를 안내했고 결과 대기 중이다. 고장 재현·진단·정리·10-6 완료는 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-6 시작(2026-10-05): 사용자 요청으로 고장 예제 5개를 검토하고 Windows SHA-256을 계산했다. Ubuntu 지정 파일 체크섬 및 현재 Deployment/Pod 조회를 안내했고 결과 대기 중이다. 고장 예제 배포·진단·정리는 아직이며 정상 앱을 유지한다. [SESSION](day10/SESSION.md).
- **Day 10의 10-5 완료(2026-10-05 사용자 출력):** pwrhg 동일 UID 유지·재시작 1, readiness/liveness timeout과 liveness에 따른 Killing 이벤트, 대상 HTTP 200/0.2.0 및 Deployment 2/2를 확인했다. 다른 Pod rslwh는 재시작 0이다. 10-1~10-5 완료이며 다음은 사용자 요청 후 10-6, Day 10 전체는 미완료다. [SESSION](day10/SESSION.md).
- Day 10의 10-5 재시작 관찰 확인(2026-10-05 사용자 출력): pwrhg hang=true/HTTP 200 후 READY 1→0→1·RESTARTS 0→1을 확인했다. watch 종료 후 UID·이벤트·대상 HTTP·최종 리소스 조회를 안내했고 결과 대기 중이다. liveness 원인 증거·HTTP 복구·10-5 완료는 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-5 probe 재준비 확인(2026-10-05 사용자 출력): probe 삭제·재생성·Ready 및 pwrhg의 status ok/version 0.2.0/HTTP 200을 확인했다. 기준 UID/재시작 조회 후 해당 Pod hang 1회·watch를 다시 안내했고 결과 대기 중이다. 자동 복구·10-5 완료는 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-5 probe 종료 확인(2026-10-05 사용자 출력): pwrhg UID·재시작 0 조회 후 probe Succeeded로 exec가 실패했다. hang 요청과 watch는 실행되지 않았다. 진단 Pod 재생성·Ready·pwrhg healthz 조회를 안내했고 결과 대기 중이다. 장애 주입·복구 성공·10-5 완료는 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-5 사전 상태 확인(2026-10-05 사용자 출력): 앱 두 개·probe 정상 및 실제 readiness/liveness 설정을 확인했다. pwrhg UID 조회 후 해당 Pod IP의 hang 1회 호출·watch를 안내했고 결과 대기 중이다. 자동 재시작·복구 성공·10-5 완료는 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-5 시작(2026-10-05): 사용자 다음 절 요청으로 무응답 앱의 liveness 복구 실습을 시작했다. Deployment·Pod 전체·실제 readiness/liveness 설정 조회를 안내했고 결과 대기 중이다. 장애 주입·복구 확인은 아직이며 10-1~10-4 완료를 유지한다. [SESSION](day10/SESSION.md).
- **Day 10의 10-4 완료(2026-10-05 사용자 출력):** 자가 치유·복제본 2→4→2·0.3.0 업데이트 관찰 HTTP 60회 성공·이력/0.2.0 롤백·HTTP 200 및 교체 Pod 정리를 확인했다. 최종 pwrhg/rslwh만 Running·Deployment 2/2이며 0.3.0 ReplicaSet은 0/0/0이다. 10-1~10-4 완료, 다음은 사용자 요청 후 10-5. Day 10 전체는 미완료다. [SESSION](day10/SESSION.md).
- Day 10의 10-4 롤백 성공(2026-10-05 사용자 출력): 이력 1/2·undo/rollout 성공·Deployment 0.2.0/2개 준비·새 Pod pwrhg/rslwh Running·HTTP 200/version 0.2.0을 확인했다. 교체된 0.3.0 Pod jlrdl/wz225는 Terminating이라 종료 완료 조회 결과 대기 중이다. 10-4 최종 마무리는 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-4 롤링 업데이트 성공(2026-10-05 사용자 출력): HTTP 60회 성공/실패 0·0.2.0 응답 11회/0.3.0 응답 49회·두 종료 코드 0·최종 0.3.0 Deployment 2/2 및 새 Pod 두 개 Running을 확인했다. 이력 조회와 직전 0.2.0 배포로 롤백·HTTP 재확인을 안내했고 결과 대기 중이다. 10-4 전체 완료는 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-4 probe 준비 확인(2026-10-05 사용자 출력): 진단 Pod 재생성·Ready 및 stfrr의 status ok/version 0.2.0/HTTP 200 응답을 확인했다. HTTP 60회 관찰과 0.3.0 이미지 변경·rollout·최종 조회를 안내했고 결과 대기 중이다. 업데이트 성공·롤백·10-4 완료는 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-4 축소 정리 확인(2026-10-05 사용자 출력): 초과 Pod 두 개가 사라지고 agent 0.2.0의 stfrr/zqnxs만 1/1 Running이며 Deployment/ReplicaSet 2개 준비를 확인했다. Completed probe 재생성·Ready·업데이트 전 HTTP 응답 조회를 안내했고 결과 대기 중이다. 업데이트·롤백·10-4 전체 완료는 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-4 2개 복원 확인(2026-10-05 사용자 출력): scale/rollout 성공·Deployment/ReplicaSet 2개 준비 및 stfrr/zqnxs Running을 확인했다. 7642s/kjbqb는 Terminating이며 삭제 완료 대기·최종 조회 결과를 기다린다. 업데이트·롤백·10-4 전체 완료는 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-4 확장 확인(2026-10-05 사용자 출력): replicas=4 적용 후 Deployment/ReplicaSet 4개 준비·앱 Pod 네 개 1/1 Running을 확인했다. 기존 두 Pod에 kjbqb·zqnxs가 추가됐다. replicas=2 복원·rollout·리소스 조회를 안내했고 결과 대기 중이다. 업데이트·롤백·10-4 전체 완료는 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-4 자가 치유 확인(2026-10-05 사용자 출력): d7qcb 삭제 후 새 Pod 7642s가 agent-1에 생성되고 기존 stfrr를 유지하며 2/2로 복구됐다. replicas=4 확장·rollout·리소스 조회를 안내했고 결과 대기 중이다. 2개 복원·업데이트·롤백은 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-4 사전 상태 확인(2026-10-05 사용자 출력): kubectl v1.31.0·agent 0.2.0 Deployment 2/2·앱 Pod 두 개 1/1 Running·probe Completed를 확인했다. d7qcb Pod 하나 삭제 후 rollout/리소스 조회를 안내했고 결과 대기 중이다. 확장·업데이트·롤백은 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-4 시작(2026-10-05): 사용자 다음 절 진행 요청으로 자가 치유·확장·롤링 업데이트·롤백을 한 단계씩 진행한다. 먼저 실습용 kubectl 선택 및 Deployment/Pod 조회를 안내했고 결과 대기 중이다. Pod 삭제 등 변경은 아직 없으며 10-1~10-3 완료를 유지한다. [SESSION](day10/SESSION.md).
- **Day 10의 10-3 완료(2026-10-05 사용자 출력):** Service DNS·내부 HTTP 8회 5:3 분산, port-forward HTTP 4회 동일 Pod 응답 및 Ctrl+C 후 39827 리스너 해제를 확인했다. 10-1~10-3 완료이며 10-4 이후·Day 10 전체는 미완료다. 다음은 사용자 요청 후 10-4. [SESSION](day10/SESSION.md).
- Day 10의 10-3 포워딩 HTTP 확인(2026-10-05 사용자 출력): 39827 호출 4회 모두 agent-64c5d66bdf-d7qcb 응답을 확인했다. ss에는 해당 포트 LISTEN이 남아 있어 1번 터미널 Ctrl+C 종료 후 리스너 해제 확인 대기 중이다. 10-3 전체 완료는 아직 아니다. [SESSION](day10/SESSION.md).
- Day 10의 10-3 포트 불일치 원인 확인(2026-10-05 사용자 출력): 1번 터미널의 현재 포워딩은 39827이며 실패한 curl은 이전 포트 45537을 호출했다. 현재 포트로 HTTP 4회 재검증 후 포워딩 종료·리스너 해제 확인 대기 중이다. 추가 프로세스 진단은 보류하며 10-3 미완료. [SESSION](day10/SESSION.md).
- Day 10의 10-3 진단 중간 확인(2026-10-05 사용자 출력): 새 Ubuntu 터미널에서 45537 리스너는 없고 port-forward PID 2495는 존재한다. 원래 터미널 최신 출력 및 ps·전체 ss·네트워크 네임스페이스 비교 결과 대기 중이다. 원인 미확인·10-3 미완료. [SESSION](day10/SESSION.md).
- Day 10의 10-3 로컬 연결 실패(2026-10-05 사용자 출력): 45537 기동 출력 후 새 Ubuntu 터미널의 첫 curl이 오류 7로 연결 실패했다. 기존 포워딩 터미널 출력·ss·pgrep 확인 대기 중이며 원인은 미확인이다. HTTP 비교·종료 확인·10-3 완료는 아직 아니다. [SESSION](day10/SESSION.md).
- Day 10의 10-3 포워딩 기동 확인(2026-10-05 사용자 출력): 127.0.0.1:45537 -> 8000을 확인했다. 다른 Ubuntu 터미널에서 HTTP 4회 비교 후 Ctrl+C 종료·ss 리스너 해제 확인 결과 대기 중이다. 10-3 완료·10-4 진행은 아직 아니다. [SESSION](day10/SESSION.md).
- Day 10의 10-3 내부 호출 확인(2026-10-05 사용자 출력): probe Ready·Service DNS 10.43.162.127 일치·HTTP 8회 응답에서 stfrr 5회/d7qcb 3회 분산을 확인했다. 루프백 자동 포트의 port-forward 전경 실행을 안내했고 기동 출력 대기 중이다. 비교·포워딩 종료·10-3 완료·10-4는 아직 아니다. [SESSION](day10/SESSION.md).
- Day 10의 10-3 시작(2026-10-05): 사용자 요청으로 ax-pilot의 진단 Pod probe 생성·Ready 대기·Service DNS와 HTTP 8회 조회를 안내했다. 실행 결과 대기 중이며 10-1·10-2 완료를 유지한다. port-forward 비교·10-3 완료·10-4 이후는 아직 아니다. [SESSION](day10/SESSION.md).
- **Day 10의 10-2 완료(2026-10-05 사용자 출력):** YAML 3개 체크섬 OK·ax-pilot/agent 배포 성공·Deployment 2/2·Pod 두 개 1/1 Running(워커 agent-0 및 관리 server-0)·Service 10.43.162.127:8000을 확인했다. 10-1·10-2 완료이며 앱과 클러스터를 유지한다. 다음은 사용자 요청 후 10-3이고 Service 통신·분산은 아직 미검증이다. [SESSION](day10/SESSION.md), [배포 증거](day10/evidence/102-deploy-user-2026-10-05.txt).
- Day 10의 10-2 시작(2026-10-05): 사용자 다음 절 요청으로 YAML 3개 체크섬 확인 후 ax-pilot Namespace·agent Deployment(0.2.0, Pod 2개)·ClusterIP Service 적용과 rollout 상태 조회를 안내했다. 사용자 실행 결과 대기 중이며 10-1 완료를 유지한다. 10-2 완료·10-3 이후는 아직 아니다. [SESSION](day10/SESSION.md).
- **Day 10의 10-1 완료(2026-10-05 사용자 출력):** 클러스터·시스템 준비에 이어 agent 0.2.0·0.3.0 push 성공, 각 digest와 로컬 ID 일치 및 태그 API HTTP 200을 확인했다. 클러스터·레지스트리·이미지는 유지한다. 다음은 사용자 요청 후 10-2이며 앱 배포·Day 10 전체 완료는 아직 아니다. [SESSION](day10/SESSION.md), [push 증거](day10/evidence/101-push-user-2026-10-05.txt). 아래 대기 문구는 이전 이력이다.
- Day 10의 10-1 이미지 빌드 확인(2026-10-05 사용자 출력): agent:0.3.0 빌드 성공·ID 3b2b9765...와 두 이미지의 linux/amd64·USER=10001·각 APP_VERSION 0.2.0/0.3.0을 확인했다. localhost:5001/ax/agent에 두 이미지 push와 태그 API 조회를 안내했고 결과 대기 중이다. 10-1 전체 완료·10-2 배포는 아직 아니다. [SESSION](day10/SESSION.md).
- Day 10의 10-1 시스템·레지스트리 확인(2026-10-05 사용자 출력): 시스템 Deployment 4개 준비·설치 Pod Completed·레지스트리 HTTP 200·실제 게시 포트·빌드 소스 3개 Windows/Ubuntu 해시 일치를 확인했다. agent:0.3.0 빌드 및 0.2.0/0.3.0 이미지 식별 정보 조회 결과 대기 중이다. 레지스트리 등록·10-1 완료·10-2 배포는 아직 아니다. [SESSION](day10/SESSION.md).
- Day 10의 10-1 클러스터 기동 확인(2026-10-05 사용자 출력): onprem 생성 성공·Kubernetes v1.30.4+k3s1·노드 3개 Ready·새 네트워크 172.21.0.0/16을 확인했다. 생성 직후 시스템 설치 Pod는 ContainerCreating이며 후속 시스템 상태·레지스트리 HTTP·빌드 소스 해시 조회 결과 대기 중이다. 0.3.0 빌드·이미지 등록·10-1 전체 완료·10-2는 아직 아니다. [SESSION](day10/SESSION.md).
- Day 10의 10-1 클러스터 생성 안내(2026-10-05): 사용자 출력으로 Ubuntu available 13Gi·디스크 가용 951G 표시·Docker 32 CPU/약 15GiB·기존 컨테이너 모두 Exited·8080/5001 리스너 부재·Day 10 파일 3개 존재를 확인했다. agent:0.2.0은 있고 0.3.0은 없다. onprem 클러스터 생성과 노드·시스템 Pod·새 대역 조회 결과 대기 중이다. 기존 WSL/koica 대역 겹침은 유지하며 생성 성공·10-1 완료는 아직 아니다. [SESSION](day10/SESSION.md).
- Day 10의 10-1 Windows 포트 확인(2026-10-05 사용자 출력): 8080·5001·대안 18080·15001 TCP 사용 행 없음 및 IPv4/IPv6 제외 범위 밖을 확인했다. 기본 8080·5001을 사용할 계획이며 Ubuntu 자원·컨테이너·이미지·주소 대역·파일 존재 조회 결과 대기 중이다. 실제 바인딩·클러스터 생성은 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-1 kubectl 준비 확인(2026-10-05 사용자 출력): 체크섬 OK·사용자 경로의 kubectl v1.31.0 선택·Kustomize v5.4.2를 확인했다. Windows TCP 점유(8080·5001·대안 18080·15001)와 IPv4/IPv6 제외 포트 범위 조회 결과 대기 중이다. 클러스터 생성은 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-1 첫 점검 확인(2026-10-05 사용자 출력): Docker 29.8.0 연결 정상·k3d v5.7.4·기본 k3s 1.30.4·kubectl 1.36.1·등록 k3d 클러스터 부재를 확인했다. 버전 차이 대응으로 가이드 kubectl 1.31.0의 사용자 경로 별도 설치·체크섬 검증·현재 셸 선택을 안내했고 결과 대기 중이다. 클러스터 생성은 아직이다. [SESSION](day10/SESSION.md).
- Day 10의 10-1 시작 요청 확인(2026-10-05): 핵심 개념·Namespace와 VM 차이·기업 인프라 도식 설명 후 사용자가 10-1 진행을 명시했다. Ubuntu Docker·k3d·kubectl 버전 및 기존 클러스터 조회를 첫 단계로 재안내했다. 결과 대기 중이며 클러스터 생성·10-1 완료·10-2 진행은 아직 아니다. [SESSION](day10/SESSION.md).
- Day 10 시작 안내(2026-10-05): 사용자 다음 챕터 진행 요청에 따라 10-1의 도구·Docker 연결·기존 클러스터 읽기 전용 점검을 안내했다. 사용자 Ubuntu 출력 대기 중이며 설치·클러스터 생성·10-2 이후 진행은 없다. [SESSION](day10/SESSION.md).
- Day 9 저장소 반영 완료: [PR #11](https://github.com/shanis345/Deploy_Practice/pull/11)의 사용자 main 병합을 확인했고 Windows main을 2a0de14로 fast-forward했다. 원격 main과 HEAD 일치 및 Day 9 커밋 ad5a241 포함을 확인했다. Ubuntu는 갱신하지 않았다. 이 병합 확인 메모는 로컬 미커밋 변경이다.
- **Day 9 실습 자원 정리 완료(2026-10-05 사용자 출력):** 압축 파일 검사·체크섬 OK, registry·UI 컨테이너 및 day09_default 제거·Compose 목록 부재를 확인했다. 압축 전 tar 삭제 명령도 성공했다. regdata·agent 이미지·압축 반입 파일·체크섬·보고서·SBOM·wheels 756K·DB 캐시 1.4G는 보존했다. 9-1~9-5와 자원 정리 완료, 누적 점검·체크포인트 평가는 미진행이다. [정리 증거](day09/evidence/cleanup-user-2026-10-05.txt). 아래는 이전 이력이다.
- **Day 9의 9-5 완료(2026-10-05):** 사용자 출력으로 반입 파일 해시 OK·첨부 3종의 정확한 크기·보고서/SBOM 해시·이미지 식별 정보를 확인하고 Windows에 [학습용 반입 신청서](day09/IMPORT-PACKAGE.md)를 작성했다. HIGH 51·CRITICAL 0과 수정 버전 제공 항목, 고객사 정보·승인 미확인을 반영했다. 9-1~9-5 완료이며 누적 점검·전체 정리·Day 9 전체 완료는 아직이다. 실제 제출·Ubuntu 문서 복사는 미진행이다. [SESSION](day09/SESSION.md). 아래 대기 문구는 이전 이력이다.
- **Day 9의 9-4 완료(2026-10-05 사용자 출력):** DB 준비·network none 취약점 스캔(HIGH 51·CRITICAL 0)·CycloneDX 1.6 SBOM 생성 및 구성 요소 90개·pip/PyYAML 확인을 마쳤다. 보고서 54K·SBOM 197K와 DB 캐시는 Ubuntu에 보존한다. 9-1~9-4 완료, 다음은 사용자 요청 후 9-5이며 Day 9 전체는 미완료다. [SBOM 증거](day09/evidence/94-sbom-user-2026-10-05.txt). 아래 대기 문구는 이전 이력이다.
- Day 9의 9-4 오프라인 스캔 성공: 사용자 첨부에서 Debian 13.7·OS 패키지 87개 탐지, HIGH 51·CRITICAL 0과 호스트 보고서 54K·user:user 소유를 확인했다. 수정 버전이 있는 항목도 있으며 취약점 해소로 기록하지 않는다. 동일 이미지의 CycloneDX SBOM 생성·요약 조회 결과 대기 중이다. [증거](day09/evidence/94-scan-user-2026-10-05.txt).
- Day 9의 9-4 DB 준비 확인: 사용자 첨부에서 DB v2 다운로드 성공·캐시 1.4G·user:user 소유와 갱신 메타데이터를 확인했다. network none·로컬 Docker 이미지·DB 갱신 중지로 HIGH/CRITICAL 스캔 및 호스트 보고서 저장을 안내했으며 결과 대기 중이다. [증거](day09/evidence/94-db-user-2026-10-05.txt).
- Day 9의 9-4 사전 점검 확인: 사용자 출력에서 Trivy 0.56.2·대상 agent linux/amd64 존재, 기존 캐시/보고서/SBOM 부재와 Ubuntu 가용 952G 표시를 확인했다. 사용자 소유 캐시에 취약점 DB만 다운로드하고 메타데이터를 조회하도록 안내했으며 결과 대기 중이다. [증거](day09/evidence/94-precheck-user-2026-10-05.txt).
- Day 9의 9-4 시작: 사용자 요청으로 Docker 연결·Trivy 및 대상 이미지·디스크·기존 캐시/보고서/SBOM 조회를 안내했다. 사전 점검 결과 대기 중이며 DB 다운로드·스캔·SBOM 생성은 아직 미실행이다. 9-1~9-3 완료를 유지하고 9-5는 미진행이다. [SESSION](day09/SESSION.md).
- **Day 9의 9-3 완료(2026-10-05 사용자 정리 출력 확인):** 레지스트리 push·API/UI·digest 연결 검증·포트 오류 복구·pull·앱 실행 후 from-reg 제거·원래 offline 태그 복원·반입 파일 해시 OK를 확인했다. registry·UI·regdata는 유지하며 UI는 http://localhost:18082다. 9-1~9-3 완료, 9-4 이후·Day 9 전체는 미완료다. [정리 증거](day09/evidence/93-cleanup-user-2026-10-05.txt). 아래 대기 문구는 이전 이력이다.
- Day 9의 9-3 실행 검증 성공: 사용자 출력에서 사내 레지스트리 이미지의 running·NETWORK=none·UID=10001·PyYAML=6.0.2·healthz ok 및 version=0.2.0을 확인했다. from-reg 정리·원래 offline 태그 복원·보존 확인 결과 대기 중이다. [증거](day09/evidence/93-runtime-user-2026-10-04.txt).
- Day 9의 9-3 pull 성공: 사용자 출력으로 반입 파일 해시 OK·로컬 태그 두 개 제거·사내 레지스트리 pull 성공과 이전 digest 일치·linux/amd64·USER=10001을 확인했다. from-reg의 포트 없는 실행·내부 healthz 조회를 안내했고 결과 대기 중이다. [증거](day09/evidence/93-pull-user-2026-10-04.txt).
- Day 9의 9-3 index 연결 확인: 사용자 API 본문의 linux/amd64 manifest가 UI·원본 빌드와 일치한다. 반입 파일 해시 검사 후 로컬 agent 태그 제거·사내 레지스트리 pull·inspect를 안내했고 결과 대기 중이다. 앱 실행·9-3 완료는 아직이다. [증거](day09/evidence/93-index-user-2026-10-04.txt).
- Day 9의 9-3 UI 관찰 확인: 사용자 텍스트에서 agent 0.2.0·43 MB·amd64 및 manifest digest 0fc1da16...를 확인했고 원본 빌드 로그와 일치한다. push/API index 4c10e5ca...와의 연결을 index 본문에서 확인하도록 안내했다. pull 실행·9-3 완료는 아직이다. [증거](day09/evidence/93-ui-observation-user-2026-10-04.txt).
- Day 9의 9-3 UI HTTP 복구 성공: 사용자 출력에서 Ubuntu Compose 해시 일치, 두 서비스 Up·18082 게시·UI/registry HTTP 200·새 CORS·저장소 두 개 유지를 확인했다. Windows 브라우저 http://localhost:18082 관찰 결과 대기 중이며 pull 실행·9-3 완료는 아직이다. [증거](day09/evidence/93-ui-recovery-user-2026-10-04.txt).
- Day 9의 9-3 대안 포트 적용 안내: 사용자 출력으로 18082 TCP 사용 항목 없음을 확인했다. Windows Compose UI 게시·CORS를 18082로 수정했고 Ubuntu 별도 변경·두 서비스 재생성·HTTP/CORS/catalog 조회를 안내했다. 실제 복구 결과 대기 중이다. [SESSION](day09/SESSION.md).
- Day 9의 9-3 Windows 진단 확인: 8082 TCP 사용 항목은 없으나 IPv4/IPv6 제외 범위 7987–8086에 포함된다. UI 게시 실패의 유력한 원인으로 보고 제외 범위 밖인 18082의 점유 조회를 안내했다. 결과 대기이며 Compose 포트·CORS 변경과 복구는 아직이다. [증거](day09/evidence/93-windows-ports-user-2026-10-04.txt).
- Day 9의 9-3 추가 상태 확인: 사용자 출력에서 UI Created·registry Up 및 catalog HTTP 200·저장소 두 개 유지를 확인했다. Ubuntu 점검은 받았으며 Windows 8082 점유·IPv4/IPv6 제외 범위 결과만 대기 중이다. 추가 복구는 아직 시행하지 않았다. [SESSION](day09/SESSION.md).
- Day 9의 9-3 UI 복구 시도 실패: 재생성 중 8082 포트 게시의 /forwards/expose HTTP 500 오류를 사용자 출력으로 확인했다. 뒤의 && 조회는 미실행이다. Windows 포트 점유·제외 범위 및 현재 Docker 컨테이너·registry 응답 조회 결과 대기 중이다. [증거](day09/evidence/93-ui-recreate-error-user-2026-10-04.txt).
- Day 9의 9-3 UI 포트 진단: Compose·컨테이너 설정의 8082 바인딩과 달리 실제 게시 목록이 비어 있음을 사용자 출력으로 확인했다. UI만 --no-deps·--force-recreate·--pull never로 재생성하고 포트·HTTP를 확인하도록 안내했으며 결과 대기 중이다. 발생 계기는 미확정이다. [증거](day09/evidence/93-ui-ports-user-2026-10-04.txt).
- Day 9의 9-3 재개 점검 확인: 레지스트리 catalog HTTP 200·저장소 두 개, regdata 및 로컬 이미지 존재를 사용자 출력으로 확인했다. UI는 Up이나 8082 게시가 ps에 보이지 않고 curl 연결 실패다. Compose 설정·inspect 포트·로그 조회 결과 대기 중이다. [증거](day09/evidence/93-resume-user-2026-10-04.txt).
- Day 9의 9-3 중단 후 재개: 마지막 확인은 10월 3일 push·API digest 일치다. 사용자 요청으로 현재 Docker 연결·Compose 상태·regdata·로컬 이미지·API/UI HTTP 읽기 전용 점검을 안내했으며 결과 대기 중이다. 현재 실행 상태는 미확인이고 UI 관찰·pull 실행은 남아 있다. [SESSION](day09/SESSION.md).
- Day 9의 9-3 API 검증 성공: 사용자 출력에서 저장소 두 개·각 태그·HTTP 200과 push 대비 전체 digest 일치를 확인했다. Windows 브라우저 UI 관찰 결과 대기 중이며 pull 실행·9-3 완료는 아직이다. [증거](day09/evidence/93-api-user-2026-10-03.txt).
- Day 9의 9-3 이미지 push 성공: 사용자 출력으로 agent·netshoot 업로드와 각 digest를 확인했다. netshoot의 단일 플랫폼 push 안내는 앞서 확인한 linux/amd64 실습 범위에 맞는다. 저장소·태그·digest API 조회 결과를 기다리며 UI 관찰·pull 실행·9-3 완료는 아직이다. [증거](day09/evidence/93-push-user-2026-10-03.txt). 아래 대기 문구는 이전 이력이다.
- Day 9의 9-3 레지스트리 기동 확인: 사용자 출력으로 컨테이너 2개 Up·루프백 5000/8082 게시·day09_default 및 day09_regdata 생성, /v2/와 UI HTTP 200·빈 catalog를 확인했다. agent·netshoot의 태그 추가·push를 안내했으며 결과 대기 중이다. 자원은 유지하고 9-3 완료·9-4 이후는 아직 아니다. [증거](day09/evidence/93-startup-user-2026-10-03.txt).
- Day 9의 9-3 사전 점검 확인: 사용자 출력으로 Compose 파일 Windows·Ubuntu 해시 일치·config 통과, 필요 이미지 4개 linux/amd64 존재, 기존 컨테이너 8개 Exited·day09_regdata 부재를 확인했다. registry·registry-ui 기동과 API·UI HTTP 검사를 안내했으며 결과 대기 중이다. push와 9-4 이후는 미진행이다. [증거](day09/evidence/93-precheck-user-2026-10-03.txt).
- Day 9의 9-3 시작: 사용자 요청으로 레지스트리 실습 사전 점검을 안내했다. Windows TCP Listen 조회에서 5000·8082·8000 항목 부재를 직접 확인했다. Ubuntu Compose 파일 해시·구성·필요 이미지·기존 컨테이너와 regdata 볼륨 결과 대기 중이다. 기동·다운로드·push는 아직 미진행이며 이번 범위는 9-3이다. [SESSION](day09/SESSION.md).
- Day 9 복습: 사용자 요청으로 9-1·9-2의 준비→파일 반입→복원·기동 흐름과 dind 시험의 목적을 설명했다. 이미지 부재·의도된 네트워크 실패·실제 /tmp 경로 오류·ID 표시 차이를 구분했다. 설명 제공이며 별도 독립 평가는 아니다. 9-1·9-2 완료를 유지하고 9-3 진행·실습 재실행은 없다.
- **Day 9의 9-2 완료(2026-10-03 사용자 출력):** 이미지 save·압축·해시 검증·복원, 빈 별도 엔진의 외부 pull 실패·파일 적재·앱 기동 및 시험 컨테이너·익명 볼륨 정리를 확인했다. 호스트 agent:0.2.0-offline·tar 43M·tar.gz 42M·sha256 파일 보존과 해시 OK도 확인했다. 다음은 사용자 요청 후 9-3이며 Day 9 전체는 미완료다. [정리 증거](day09/evidence/92-cleanup-user-2026-10-03.txt), [SESSION](day09/SESSION.md). 아래 대기 문구는 이전 이력이다.
- Day 9의 9-2 실행 검증 완료: 사용자 출력으로 별도 엔진 내부 agent의 running·NETWORK=none, UID=10001·GID=0·PyYAML=6.0.2·healthz ok를 확인했다. 내부 agent·day09-airgap·해당 익명 볼륨 정리 및 호스트 이미지·반입 파일 보존 확인을 안내했으며 결과 대기 중이다. 9-2 최종 완료·9-3 진행은 아직 아니다. [증거](day09/evidence/92-airgap-runtime-user-2026-10-03.txt).
- Day 9의 9-2 내부 적재 성공: 사용자 출력으로 /tmp tmpfs와 /day09-import 경로 변경 후 해시 OK·load 성공을 확인했다. 내부 ID b7e1e28...는 앞선 빌드의 config 해시와 일치하며 linux/amd64·USER=10001이다. 내부 agent 기동·UID·PyYAML·healthz 확인을 안내했으며 결과 대기 중이다. 정리·9-2 완료는 아직 아니다. [증거](day09/evidence/92-airgap-load-user-2026-10-03.txt).
- Day 9의 9-2 복사 경로 진단: 사용자 출력에서 내부 /tmp가 비어 있고 동일 컨테이너 running·재시작 0임을 확인했다. 공식 dind 스크립트의 /tmp tmpfs 마운트를 원인 후보로 좁혔다. 내부 mountinfo 조회와 /day09-import 경로의 복사·해시 검증·load 재시도를 안내했으며 결과 대기 중이다. [증거](day09/evidence/92-airgap-tmp-user-2026-10-03.txt).
- Day 9의 9-2 내부 파일 조회 오류: 사용자 출력에서 tar.gz·sha256의 docker cp 성공 표시 후 내부 sha256sum이 No such file or directory로 실패했다. &&에 따라 load는 실행되지 않았다. 내부 /tmp·작업 위치·컨테이너 상태·마운트 조회를 안내했고 결과 대기 중이다. 원인은 미확정이며 기존 파일·컨테이너는 유지한다. [증거](day09/evidence/92-airgap-copy-error-user-2026-10-03.txt).
- Day 9의 9-2 외부 pull 실패 확인: 사용자 출력으로 내부 Docker의 DNS 서버 접속 network is unreachable·종료 코드 1 및 images=0 유지를 확인했다. tar.gz·해시 파일의 day09-airgap 복사·내부 검증·load를 안내했으며 결과 대기 중이다. 내부 앱 기동·정리·9-2 완료는 아직 아니다. [증거](day09/evidence/92-airgap-pull-user-2026-10-03.txt).
- Day 9의 9-2 별도 엔진 기동 확인: 사용자 출력으로 day09-airgap의 running·NETWORK=none 및 내부 Docker 27.5.1·images=0을 확인했다. 내부 alpine:3.20 pull 실패 시험·종료 코드·이미지 수 조회를 안내했으며 결과 대기 중이다. 컨테이너는 유지하고 파일 반입·앱 기동은 아직 미진행이다. [증거](day09/evidence/92-dind-start-user-2026-10-03.txt).
- Day 9의 9-2 dind 이미지 준비 확인: 사용자 출력으로 docker:27-dind pull 성공·linux/amd64를 확인했다. day09-airgap을 privileged·network=none으로 기동하고 내부 Docker 버전·images=0을 확인하도록 안내했으며 결과 대기 중이다. 별도 엔진 적재·앱 기동 및 9-2 완료는 아직 아니다. [증거](day09/evidence/92-dind-image-user-2026-10-03.txt).
- Day 9의 9-2 별도 데몬 사전 점검: 사용자 출력으로 docker:27-dind 이미지 부재와 day09-airgap 컨테이너 부재를 확인했다. linux/amd64 이미지 pull·inspect를 안내했으며 결과 대기 중이다. 컨테이너 생성은 아직 없다. [증거](day09/evidence/92-dind-precheck-user-2026-10-03.txt).
- Day 9의 9-2 파일 검증·복원 성공: 사용자 출력으로 gzip·SHA-256 검사, 해당 이미지 제거·목록 부재, tar.gz load 및 복원 전후 ID·linux/amd64·USER=10001 일치를 확인했다. docker:27-dind 이미지·day09-airgap 이름 사전 점검을 안내했고 결과 대기 중이다. 별도 데몬 시험·9-2 완료는 아직 아니다. [증거](day09/evidence/92-load-user-2026-10-03.txt).
- Day 9의 9-2 반입 파일 생성 확인: 사용자 출력으로 이미지 ID 일치, tar 43M·tar.gz 42M·파일 SHA-256 생성을 확인했다. gzip·해시 검증 성공 조건으로 해당 이미지 제거·검사한 tar.gz의 load 복원을 안내했으며 결과 대기 중이다. 별도 Docker 데몬 시험·9-2 완료는 아직 아니다. [증거](day09/evidence/92-package-user-2026-10-03.txt).
- Day 9의 9-2 시작: 사용자 요청으로 agent:0.2.0-offline의 save·gzip 압축·파일 SHA-256 생성을 안내했으며 사용자 출력 대기 중이다. 원본 이미지 제거·load·별도 Docker 데몬 시험은 아직 미진행이다. 9-1은 완료 상태를 유지하고 이번 범위는 9-2다. [SESSION](day09/SESSION.md).
- **Day 9의 9-1 완료(2026-10-03 사용자 출력):** wheel 준비·오프라인 빌드·network=none 기동(UID=10001·PyYAML=6.0.2·healthz ok), 시험 컨테이너 제거 및 온라인용 pip 빌드의 이름 해석 실패·종료 코드 1을 확인했다. 이미지·wheels는 삭제하지 않았다. 다음은 사용자 요청 후 9-2이며 Day 9 전체 완료는 아니다. [마지막 증거](day09/evidence/91-cleanup-online-failure-user-2026-10-03.txt), [SESSION](day09/SESSION.md). 아래 대기 문구는 이전 이력이다.
- Day 9의 9-1 네트워크 없는 기동 확인(2026-10-03 수신): 사용자 출력으로 day09-offline-test의 running·NETWORK=none, UID=10001·GID=0, PyYAML=6.0.2, healthz ok·version=0.2.0을 확인했다. 시험 컨테이너 정리와 같은 베이스의 온라인용 Dockerfile 실패 비교를 안내했으며 결과 대기 중이다. 9-1은 아직 미완료다. [증거](day09/evidence/91-runtime-user-2026-10-03.txt).
- Day 9의 9-1 오프라인 빌드 확인: 사용자 출력으로 로컬 wheel의 PyYAML 6.0.2 설치와 agent:0.2.0-offline 생성(linux/amd64·USER=10001)을 확인했다. network=none 컨테이너의 실제 UID·패키지·healthz 검증을 안내했으며 결과 대기 중이다. 온라인 빌드 비교·9-1 완료 및 9-2 이후는 아직 아니다. [증거](day09/evidence/91-build-user-2026-10-02.txt).
- Day 9의 9-1 wheel 준비 확인: 사용자 출력으로 PyYAML 6.0.2의 cp312·x86_64 wheel 다운로드, user:user 소유권·wheels 756K를 확인했다. default 빌더의 --network=none·--no-cache 빌드와 이미지 확인을 안내했으며 결과 대기 중이다. 앱 기동·온라인 빌드 비교 및 9-2 이후는 미진행이다. [증거](day09/evidence/91-wheels-user-2026-10-02.txt).
- Day 9의 9-1 베이스 이미지 준비 확인: 사용자 pull·inspect 출력으로 python:3.12.14-slim 존재·linux/amd64를 확인했다. 같은 이미지의 임시 컨테이너에서 wheel 다운로드를 안내했으며 결과 대기 중이다. 오프라인 빌드·앱 기동 검증은 미진행이다. [증거](day09/evidence/91-base-image-user-2026-10-02.txt). 아래 대기 문구는 이전 단계 이력이다.
- Day 9의 9-1 사전 점검 확인: 사용자 출력으로 Windows·Ubuntu 파일 해시 일치와 Docker Client/Engine 29.8.0·default 연결을 확인했다. python:3.12.14-slim 부재로 linux/amd64 베이스 이미지 pull·inspect를 안내했으며 결과 대기 중이다. wheel 다운로드·빌드·기동은 아직 미진행이다. [증거](day09/evidence/91-precheck-user-2026-10-02.txt).
- Day 9의 9-1 시작(2026-10-02): 사용자 요청으로 오프라인 빌드 실습의 사전 점검을 안내했다. Ubuntu 파일 해시·Docker 연결·베이스 이미지 및 기존 산출물 확인 결과 대기 중이다. 다운로드·빌드·컨테이너 실행은 아직 미진행이며 9-2 이후는 범위 밖이다. [SESSION](day09/SESSION.md).
- Day 8 [PR #10](https://github.com/shanis345/Deploy_Practice/pull/10) 병합 확인: GitHub 직접 조회로 main 병합 커밋 6801a098a0b4cd5b138e08aa707b7926a6f0c8bc, 병합 시각 2026-10-01 14:58:34 UTC를 확인했다. Windows main을 fast-forward 갱신하고 Day 8 커밋 f2b5df9 포함을 확인했다. Ubuntu 사본과 브랜치 삭제는 이번 작업에서 다루지 않았다. 이 병합 확인 메모는 로컬 변경이며 별도 커밋·push하지 않았다.
- Day 8 GitHub 반영 요청: 사용자 요청으로 codex/day08-results 브랜치에서 main 대상 PR을 만든다. 병합은 사용자가 수행한다. origin fetch 후 시작점과 origin/main이 b2dd34d로 일치함을 직접 확인했다. 실습 재실행·Day 9 진행은 없다.
- Day 8 체크포인트: 사용자 요청으로 실습 복습과 6문항 해설을 제공했다. Python 라이브러리별 신뢰 저장소, CA 파일 지정의 한계, 검증 오류와 TLS 검사 판별의 차이를 공식 문서로 보완했다. 해설 제공과 사용자 독립 평가를 구분하며 독립 평가는 미실시다.
- **Day 8 종료(2026-10-01): 8-1~8-4 실습·지정 자원 정리 완료.** 사용자 출력으로 컨테이너 5개·네트워크 2개 제거와 Day 8 잔존 목록 부재를 확인했다. 공개 CA 파일 및 agent:0.2.0-ca 이미지 보존도 확인했다. 체크포인트 6문항 해설·독립 평가는 미실시다. [정리 증거](day08/evidence/cleanup-user-2026-10-01.txt), [SESSION](day08/SESSION.md). 아래 실행 중·대기 문구는 이전 단계 이력이다.
- Day 8 종료 정리 안내: 사용자 요청으로 Day 8 Compose down·잔존 목록 확인·공개 CA 및 CA 이미지 보존 확인 명령을 안내했다. 사용자 실행 결과 대기 중이며 정리 완료로 처리하지 않는다. 8-1~8-4 실습은 완료, 체크포인트는 미진행이다.
- **Day 8의 8-4 완료(2026-10-01 사용자 텍스트):** GET https://example.com/·Python-urllib/3.12 요청 헤더와 Response HTTP 200·헤더·Example Domain HTML 본문을 관찰했다. No content는 GET 요청 본문 부재다. **8-1~8-4 실습 완료·자원 정리와 체크포인트 미진행.** 컨테이너·CA·이미지는 유지한다. [관찰 증거](day08/evidence/84-https-observation-user-2026-10-01.txt). 아래 대기 문구는 이전 이력이다.
- Day 8의 8-4 Response 관찰 확인: 사용자 제공 텍스트에서 HTTP 200·응답 헤더·Example Domain HTML 본문을 확인했다. 같은 요청의 Request 탭 URL·메서드·헤더를 확인한 결과는 대기 중이다. [관찰 증거](day08/evidence/84-https-observation-user-2026-10-01.txt).
- Day 8의 8-4 요청 성공 확인: 사용자 출력으로 새 agent-ca HTTPS 요청의 ok=true·HTTP 200을 확인했다. mitmweb Request/Response 화면 내용은 아직 받지 않았으며 8-4 완료로 처리하지 않는다.
- Day 8의 8-4 시작: 사용자 요청으로 mitmweb HTTPS 관찰을 시작한다. Windows http://localhost:8082/ 접속 후 agent-ca로 새 HTTPS 요청을 만들고 Request/Response를 관찰하도록 안내했다. 사용자 명령·화면 결과 대기 중이며 8-4 완료·전체 정리는 아직 아니다.
- **Day 8의 8-3 완료(2026-10-01 사용자 출력):** 프록시 인증서 발급자·검증 코드 21, CA 번들 150→151개·mitmproxy CA 1개, curl 미지정 HTTP=000·exit=60과 --cacert 지정 후 HTTP=200·exit=0을 확인했다. 컨테이너·CA·이미지는 유지하며 다음은 사용자 요청 후 8-4다. [curl 증거](day08/evidence/83-curl-user-2026-10-01.txt). 아래 대기 문구는 이전 단계 이력이다.
- Day 8의 8-3 번들 확인: 사용자 출력으로 원본 150개·병합 151개, 병합 번들 내 mitmproxy CA 1개를 확인했다. probe에서 curl의 CA 지정 전후 비교를 안내했고 결과 대기 중이다. [증거](day08/evidence/83-bundle-user-2026-10-01.txt).
- Day 8의 8-3 첫 진단 확인: 사용자 출력에서 subject=example.com·issuer=mitmproxy와 probe 검증 오류 20·21, 최종 코드 21을 확인했다. 세 agent healthy·나머지 서비스 Up이다. 다음은 원본·병합 이미지의 CA 개수 비교와 mitmproxy CA 조회이며 결과 대기 중이다. [증거](day08/evidence/83-issuer-user-2026-10-01.txt).
- Day 8의 8-3 시작: 사용자 요청으로 인증서 진단을 시작한다. Compose 상태와 probe의 프록시 경유 openssl subject·issuer·검증 결과 조회를 안내했으며 사용자 출력 대기 중이다. 8-4는 미진행이다.
- **Day 8의 8-2 완료(2026-10-01 사용자 출력):** 원본 CA 미신뢰 실패와 두 해결 방식의 HTTPS 200을 확인했다. agent-ca는 uid=10001·gid=0 및 병합 CA 번들 경로를 사용한다. 임시 corp-ca.crt 제거·부재, 세 agent healthy를 확인했다. 컨테이너 5개·네트워크·CA·이미지는 유지한다. 다음은 사용자 요청 후 8-3이며 Day 8 전체 완료는 아니다. [최종 성공 증거](day08/evidence/82-ca-success-user-2026-10-01.txt). 아래 결과 대기 문구는 이전 단계 이력이다.
- Day 8의 8-2 CA 병합 빌드 성공: 사용자 출력으로 수정한 Dockerfile.ca 해시 일치와 default 빌더의 agent:0.2.0-ca 빌드 성공을 확인했다. 임시 공개 CA 사본 제거·agent-ca 기동·healthz·CA 경로·HTTPS 응답 확인을 안내했으며 결과 대기 중이다. [빌드 증거](day08/evidence/82-ca-build-user-2026-10-01.txt).
- Day 8의 8-2 해결 2 준비: 사용자 출력으로 Dockerfile.ca 두 사본 일치·베이스 이미지 내 CA 갱신 도구와 번들·corp-ca.crt 부재를 확인했다. Windows Dockerfile.ca는 apt 설치 대신 CA 갱신만 하도록 수정했고 Ubuntu 동일 수정·공개 CA 복사·default 빌더 이미지 빌드를 안내했다. 빌드 결과 대기 중이다.
- Day 8의 8-2 해결 1 성공: 사용자 출력으로 agent-envca healthz 정상, CA 환경변수 설정 및 HTTPS egress HTTP 200을 확인했다. 원본 agent는 healthy이고 agent-envca는 ps 당시 health: starting이다. 네 컨테이너를 유지하며 CA 병합 이미지 준비를 위한 Ubuntu Dockerfile·도구·기존 CA 파일 확인 결과 대기 중이다. [증거](day08/evidence/82-envca-user-2026-10-01.txt).
- Day 8의 8-2 실패 재현 확인: 사용자 출력으로 agent·probe 기동, healthz 정상 및 HTTPS egress의 SSLCertVerificationError를 확인했다. agent의 Docker health 상태는 당시 starting이었다. 다음은 agent-envca 기동·CA 환경변수·HTTPS 응답 확인이며 사용자 결과 대기 중이다. [증거](day08/evidence/82-no-ca-user-2026-10-01.txt).
- Day 8의 8-2 시작(2026-10-01): 사용자 추가 요청으로 CA 미신뢰 실패 재현부터 진행한다. tls-proxy·agent·probe 기동 및 healthz·HTTPS egress 비교 명령을 안내했고 결과 대기 중이다. CA 파일 지정·병합 이미지 시험은 아직 미진행이다. 8-3 이후는 범위 밖이다.
- **Day 8의 8-1 완료(2026-10-01 사용자 출력):** day08 네트워크 2개와 tls-proxy 기동·Up, 호스트 127.0.0.1:8082 게시, CA 파일 생성과 subject·issuer·유효기간을 확인했다. 프록시·네트워크·certs는 유지한다. HTTPS 실패·복구와 8-2 이후는 미진행이다. [증거](day08/evidence/81-startup-user-2026-10-01.txt), [SESSION](day08/SESSION.md). 아래 사전 점검 대기 문구는 기동 전 이력이다.
- Day 8 설정 검증(2026-10-01): 사용자 출력으로 web_password 제거·호스트 8082 변경, Compose config 통과 및 수정 후 Windows·Ubuntu 해시 일치를 확인했다. tls-proxy만 기동하고 CA 메타데이터를 확인하는 명령을 안내했으며 결과 대기 중이다. 8-1 완료·8-2 시작으로 처리하지 않는다.
- Day 8 후속 점검: 사용자 Docker Desktop 실행 후 Client/Engine 29.8.0·Desktop 4.92.0 연결 복구, mitmproxy:11.0.0 이미지 존재와 기존 컨테이너 모두 Exited를 확인했다. Windows Compose의 web_password 제거·호스트 8082 변경을 반영하고 Ubuntu에도 같은 수정·구성 검증을 안내했다. 사용자 결과 대기 중이며 프록시 기동·CA 생성은 미진행이다.
- Day 8 시작(2026-10-01): 사용자 요청 범위는 8-1이다. 사용자 출력으로 Compose 파일의 Windows·Ubuntu 해시 일치와 OpenSSL 3.0.13을 확인했다. Docker 명령은 WSL Integration 안내 오류로 실패해 Desktop 실행·연동 복구 후 재확인을 기다린다. 컨테이너 기동·CA 생성은 미진행이다. [SESSION](day08/SESSION.md).
- Day 7 체크포인트: 사용자 요청으로 6문항 해설과 실습 복습을 제공했다. Node.js의 버전별 환경변수 프록시 지원과 Java 설정은 공식 문서로 보완했다. 해설 제공과 사용자 독립 답변 평가는 구분하며 평가 통과로 기록하지 않는다.
- Day 7 질의응답: 기업 프록시의 콘솔·설정 파일 관리 방식과 클라이언트 HTTP_PROXY/NO_PROXY 설정의 차이를 설명했다. 질의응답 당시 새 실습은 진행하지 않았다. 이후 7-4~7-5와 종료 정리까지 완료했다.
- Day 7 종료(2026-09-30): **7-1~7-5 학습·정리·체크포인트 해설 완료·독립 평가 미실시.** 프록시 미설정 시 DNS 실패·지정 후 200, no_proxy 누락 시 내부 API 403·지정 후 200 및 프록시 로그 불변을 사용자 출력으로 확인했다. 실패 3은 대문자 HTTP_PROXY만 지정 시 DNS 실패·exit=6, 소문자 http_proxy 지정 시 HTTP 200·exit=0을 확인했다. 사례 4는 임시 이미지 히스토리에서 일반 ARG의 공개 더미 값 노출과 예약 HTTP_PROXY 부재를 확인했다. 사용자 출력으로 day07-buildargs:lab 삭제·이미지 목록 부재 및 /tmp/day07-buildargs.YTZNch 폴더 제거를 확인했다. 실제 빌드 프록시 통신 장애는 시험하지 않았다. 별도 desktop-linux 조회 오류는 미해결로 보존한다. 사용자 출력으로 Day 7 컨테이너 4개·네트워크 2개 제거와 프로젝트 잔존 목록 부재를 확인했다. [정리 증거](day07/evidence/cleanup-user-2026-09-30.txt). 기록 브랜치는 `codex/day07-results`다. [SESSION](day07/SESSION.md).
- Day 6 결과 [PR #8](https://github.com/shanis345/Deploy_Practice/pull/8)은 2026-09-30 main에 병합됐다(커밋 `b3a34c5`, GitHub 직접 조회). Windows main 갱신 및 main 포함 여부 검증 후 완료한 로컬 브랜치 7개·원격 브랜치 8개를 삭제했다. 커밋·PR 이력은 유지한다. Ubuntu 사본은 갱신하지 않았다.
- **Day 6 종료(2026-09-30). 실습·학습용 신청서 작성 및 설명·누적 장애 5개 복구·자원 정리 완료.** 사용자 출력으로 Day 6 컨테이너 7개·네트워크 3개 제거, 프로젝트 잔존 목록 없음·8080 리스너 부재를 확인했다. 이미지·볼륨·백업 삭제는 요청·실행하지 않았으며 잔존 목록은 별도 재조회하지 않았다. 독립 진단 4/5 및 자기점검 문답 평가는 미실시로 남긴다. [SESSION](day06/SESSION.md), [정리 증거](day06/evidence/cleanup-user-2026-09-30.txt).
- Day 6 누적 장애 1~5번 재현·안내에 따른 진단·복구 완료(2026-09-30 사용자 출력): 마지막 5번은 agent DMZ 연결 제거 후 biz·dbzone만 남음, healthz 정상, 외부 요청 ok=false·gaierror·1ms를 확인했다. 이후 자원 정리까지 완료했다. 독립 진단 4/5 통과와 별도 개념 자기점검 평가는 미실시다.
- Day 6 화면 관찰 완료(2026-09-30 사용자 화면·출력): 정리 전 lazydocker에서 서비스 7개 running, agent·postgres healthy, 3개 존 목록을 확인했다. Containers: none 표시를 CLI로 보완해 세 존의 internal 값과 소속 일치를 확인했다. 동일 증상의 공식 버그 보고를 찾았으나 설치된 바이너리의 내부 원인은 확정하지 않았다.
- Day 6의 6-4 학습용 초안 작성·설명 완료: Codex가 Windows에 가이드 E-2 기반 신청서 7행·흐름도·근거를 담은 [초안](day06/FIREWALL-REQUEST.md)을 작성했다. 가상 IP·미정 항목과 실습 검증 범위를 구분했다. 고객사 제출·정책 적용·사용자 독립 작성 평가는 수행하지 않았다.
- **Day 6의 6-3 완료**(사용자 출력): DMZ 추가 시 healthy·healthz 정상과 외부 HTTP 200·105ms를 확인했고, 백업 원복 후 원본 해시 일치·biz/dbzone만 연결·healthy·healthz 정상·외부 요청 gaierror(7ms)를 확인했다. /tmp/day06-compose.OTTiFi 백업은 삭제하지 않았다. [원복 증거](day06/evidence/63-restored-user-2026-09-29.txt).
- **Day 6의 6-2 완료**(2026-09-29 사용자 출력): gateway 경유 healthz 정상, agent→postgres:5432 TCP 성공(1ms). ③ probe-dmz→postgres는 DNS 실패했고 IP 172.22.0.4:5432 직접 시도도 3초 타임아웃·종료코드 1이었다. ④ probe-biz의 example.com 이름 해석 실패와 IPv4 기본 경로 부재를 확인했다. ⑤ 실제 agent→ERP HTTP 200·erp-api 응답을 확인했다. ⑥ agent의 외부 요청은 ok=false·gaierror·8ms로 이름 해석 실패를 확인했다. ⑦ probe-db→agent(172.22.0.3):8000의 새 TCP 연결도 성공·종료코드 0으로 확인했다. 7개 경로를 모두 기록했다. DB 인증·SQL은 미시험이다. 후속 6-3 진행 상태는 위 항목을 참고한다.
- **Day 6의 6-1 완료**(2026-09-29 사용자 Ubuntu 출력): 사전 점검 후 네트워크 3개·컨테이너 7개 기동, agent·postgres healthy 및 gateway의 127.0.0.1:8080 게시를 확인했다. internal 값과 네트워크 소속도 일치한다. 6-1 완료 당시 구성은 실행 중이었다. 이후 통신 시험은 위 6-2 기록을 참고한다. 기존 Day 4·koica 자원은 변경하지 않았다. [SESSION](day06/SESSION.md), [기동 증거](day06/evidence/startup-user-2026-09-29.txt).
- Day 5 체크포인트: 사용자 요청으로 5문항 해설을 제공했다. Compose도 정식 운영에 사용할 수 있음을 공식 문서로 보완했다. 사용자 독립 답변의 평가·통과 기록과 구분하며 자기점검 통과로 처리하지 않는다.
- Day 5: **종료(2026-09-29). 5-1~5-4·지정 자원 정리 완료.** 사용자 출력으로 세 컨테이너·day05_default 제거, 8080 리스너 부재 및 day05_pgdata 보존을 확인했다. lazydocker 정상 상태·로그 표시와 체크포인트 해설까지 진행했다. Stats·TUI 상태 변화 화면과 별도 자기점검 평가는 미확인으로 남긴다. 이미지·임시 백업은 삭제 대상이 아니었다. [SESSION](day05/SESSION.md), [정리 증거](day05/evidence/cleanup-user-2026-09-29.txt).
- Day 4 정리 상태 재확인(2026-09-29): 이전 완료 진술과 달리 사전 점검에서 실습 컨테이너 7개가 존재했다. 이후 pub를 중지해 8080을 해제했고, lazydocker 화면에는 pub2·web·web2 실행 및 lab-net·other-net 잔존이 보였다. Day 4 자원 정리 완료로 간주하지 않으며, 과거 진술과 다른 경위는 미확인이다. Day 5 종료 시 이 자원들은 재조회하지 않았다.
- Day 3: 완료(2026-09-27 사용자 완료 확인). 실습 3-1~3-5·반입 초안·lazydocker 관찰·종료 정리는 사용자 증거로 확인했다. 새 이미지 스캔은 HIGH 44·CRITICAL 0, 수정 버전 미제공 항목 제외 시 0건이다. 별도 자기점검 문답 평가 기록은 없다. [Day 3 요약](day03/README.md), [SESSION](day03/SESSION.md), [반입 패키지 초안](day03/IMPORT-PACKAGE.md).
- 현재 상태: **Day 0 실습 완료. Day 1 주요 학습 완료·마무리 남음. Day 2 실습·정리 완료. Day 3 완료. Day 4 실습 완료·9/29 잔존 자원 확인. Day 5 종료. Day 6 실습·누적 장애 복구·정리 완료 및 종료. Day 7 종료·7-1~7-5 학습·정리·체크포인트 해설 완료·독립 평가 미실시. Day 8 종료·8-1~8-4 실습·정리·체크포인트 해설 완료·독립 평가 미실시.**
- Day 4: 완료(2026-09-28 사용자 마무리 요청 및 자원 정리 완료 확인). 4-1~4-6·lazydocker 관찰은 사용자 출력·화면으로 확인했다. 마지막 정리는 사용자 진술이며 삭제 후 목록·포트 출력은 미제공이다. 별도 자기점검 5문항 평가는 미진행이다. [결과 요약](day04/README.md), [SESSION](day04/SESSION.md).
- Day 4 남은 관찰 사항: Ubuntu IP와 기존 koica Docker 대역의 겹침, 컨테이너의 Ubuntu IP 직접 요청 시간 초과, lazydocker 0.25.2의 Containers: none 표시 불일치. 세부 원인은 미확정이며 koica 자원·Docker 전역 설정은 변경하지 않았다. 임시 Python 서버 종료는 출력으로 확인했고 임시 폴더와 이미지는 삭제하지 않았다.
- Day 2: 수동 네트워크·라우팅·NAT·패킷 관찰, Docker 네트워크·DNS, 64MiB 메모리 제한과 cgroup 값 일치를 확인했다. 사용자 출력으로 who1·who2·lim·demo-net 삭제, 빈 네임스페이스·브리지 목록, 실습 NAT 제거, ip_forward=0 복구를 확인했다. 개념 질의응답은 진행했으며 가이드 자기점검 5문항의 별도 평가는 미진행이다. [Day 2 SESSION](day02/SESSION.md).
- Day 1 세션 결과: VM/컨테이너·vSphere·SSH/SAC·고객사 역할 및 VM 신청 질문 12개를 학습했다. Ansible 두 대상 모두 첫 실행 changed=3, 재실행 changed=0, failed=0·unreachable=0이며 내부 계정·권한·설정 예시 파일도 확인했다.
- 완료 근거: 사용자 제공 Ubuntu 출력. Codex가 Windows 기록·증거를 대조했다. 상세 명령·질의응답·오류 해결은 [Day 1 SESSION](day01/SESSION.md), 버전·호환성은 [환경 기록](docs/environment.md)에 보존한다.
- Day 1 남은 항목: 컨테이너 삭제·deactivate 실행 확인, E-1 VM 신청서 초안, 최종 개념 자기점검. Day 1 전체 완료로 처리하지 않는다.
- Day 1 마지막 확인 상태: vm-agent-01·02 내부 조회 성공. 이후 정리 결과는 받지 않았으며 현재 컨테이너 상태를 새로 조회하지 않았다.
- Windows 프로젝트와 Ubuntu `/home/user/onprem-lab`은 별도 복사본이다. 이번 기록 정리에서 Ubuntu 동기화·실습 재실행은 하지 않았다.
- Day 0의 이미지 빌드·API·UID/GID·정리·TUI 확인 결과는 [Day 0 SESSION](day00/SESSION.md)에 있다. 개념 자기점검 4문항의 별도 평가는 미진행이다.
- 남은 환경 차이: kubectl·Compose·dive의 가이드 버전 차이, 가이드 lazydocker 고정값과 실제 설치 버전 차이, Ansible 인터프리터 탐색·facts 자동 주입 경고. 현재 실습 성공을 향후 모든 실습의 호환성 보장으로 해석하지 않는다.
- GitHub 저장소: [Deploy_Practice](https://github.com/shanis345/Deploy_Practice). 초기 구성 PR #1 및 [Day 0 PR #2](https://github.com/shanis345/Deploy_Practice/pull/2)는 main에 병합됐다. PR #2 병합 커밋은 `065e7b9`이며 2026-09-23 GitHub 조회로 확인했다.
- Day 1 기록의 [PR #3](https://github.com/shanis345/Deploy_Practice/pull/3)은 main에 병합됐다. 2026-09-25 원격 갱신으로 병합 커밋 `abb2ffb`를 확인했다. Day 1 전체 완료 판정과는 별개다.
- Day 2 기록의 [PR #4](https://github.com/shanis345/Deploy_Practice/pull/4)는 main에 병합됐다. 2026-09-27 원격 갱신으로 병합 커밋 `18b805e`를 확인했다.
- Day 3 기록의 [PR #5](https://github.com/shanis345/Deploy_Practice/pull/5)는 main에 병합됐다. 2026-09-28 원격 조회로 병합 커밋 `027012d`를 확인했다.
- Day 4 기록의 [PR #6](https://github.com/shanis345/Deploy_Practice/pull/6)은 main에 병합됐다. 2026-09-28 GitHub 조회로 병합 커밋 `f316ff8`을 확인하고 Windows 로컬 main을 fast-forward 갱신했다. 당시 남긴 병합 확인 메모는 이번 Day 5 기록 변경에 포함한다. Ubuntu 복사본은 갱신하지 않았다.
- Codex 프로젝트 등록과 별도 Day별 작업 생성은 수행하지 않았다.
- Day 5 기록 [PR #7](https://github.com/shanis345/Deploy_Practice/pull/7)은 병합됐다. 2026-09-30 GitHub 조회로 병합 커밋 `077b241`을 확인했고 Day 6 PR 브랜치를 해당 main에서 분기했다.

| Day | 주제 | 상태 | 기록 |
|---|---|---|---|
| 00 | 환경 준비 | 실습 완료 · 0-1~0-5 | [SESSION](day00/SESSION.md) |
| 01 | 가상화 계층과 vSphere: 물리 서버부터 컨테이너까지 | 주요 학습·1-3 검증 완료 · 마무리 남음 | [SESSION](day01/SESSION.md) |
| 02 | 리눅스 네트워크 기초: 네임스페이스·브리지·라우팅·DNS | 실습·정리 완료 · 별도 자기점검 미진행 | [SESSION](day02/SESSION.md) |
| 03 | Docker 이미지·레이어·컨테이너, 그리고 심의를 통과하는 이미지 | 완료(사용자 확인) · 별도 자기점검 평가 기록 없음 | [SESSION](day03/SESSION.md) |
| 04 | Docker 네트워크와 진단 3단계 | 실습 완료 · 9/29 자원 잔존 확인 · 별도 자기점검 미진행 | [SESSION](day04/SESSION.md) |
| 05 | Docker Compose: 다중 서비스와 그 한계 | 종료 · 5-1~5-4·정리 완료 · 일부 화면 관찰·별도 평가 미확인 | [SESSION](day05/SESSION.md) |
| 06 | 망분리 재현: DMZ · 업무망 · DB존, 그리고 방화벽 신청서 | 종료 · 실습·신청서 초안·장애 5개 복구·정리 완료 · 별도 평가 미실시 | [SESSION](day06/SESSION.md) |
| 07 | 포워드 프록시, 화이트리스트, HTTP_PROXY/NO_PROXY 함정 | 종료 · 7-1~7-5 학습·정리·체크포인트 해설 완료·독립 평가 미실시 | [SESSION](day07/SESSION.md) |
| 08 | 사내 CA와 TLS 검사(SSL 인스펙션) | 종료 · 8-1~8-4 실습·정리·체크포인트 해설 완료 · 독립 평가 미실시 | [SESSION](day08/SESSION.md) |
| 09 | 폐쇄망 이미지 반입: 오프라인 빌드 · save/load · 사내 레지스트리 · 스캔 · SBOM | 9-1~9-5·자원 정리 완료 · 누적 점검·평가 미진행 | [SESSION](day09/SESSION.md) |
| 10 | Kubernetes 기초: Pod · Deployment · Service · probe | 실습·k9s·정리 완료 · 체크포인트 해설 제공·이해도 평가 미진행 | [SESSION](day10/SESSION.md) |
| 11 | 설정 · 비밀 · 수신 · Helm: ConfigMap, Secret, Ingress, 차트 | 미시작 | [SESSION](day11/SESSION.md) |
| 12 | NetworkPolicy로 존 분리, 그리고 OpenShift의 차이 | 미시작 | [SESSION](day12/SESSION.md) |
| 13 | LLM 게이트웨이 · 감사 로그 · 관측성 기초 | 미시작 | [SESSION](day13/SESSION.md) |
| 14 | Walking Skeleton 종합: 전 구간 관통, 검증 스크립트, 런북, 이관 | 미시작 | [SESSION](day14/SESSION.md) |

## 다음 실습을 시작할 때

현재 인수인계(2026-10-05, Day 10 PR 생성): [PR #12](https://github.com/shanis345/Deploy_Practice/pull/12)의 리뷰 대기 중이다. 병합 또는 다음 Day 진행은 사용자 요청에 따른다. Ubuntu에서 실습용 kubectl PATH와 클러스터·앱 상태를 다시 확인하며 probe는 삭제된 상태를 기준으로 한다. 아래 시작 지점은 과거 이력이다.

최신 시작 지점(2026-10-05, Day 10 체크포인트 해설 후): 사용자에게 6개 답안 해설을 제공했다. 직접 답해 보는 평가는 아직이며 필요한 경우 사용자 요청으로 진행한다. 다음 Day를 임의로 시작하지 않는다. 앱·클러스터·레지스트리는 유지하고 probe는 삭제된 상태다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10 최종 정리 완료): 다음은 사용자 요청 후 체크포인트 이해도 점검이다. probe와 고장 예제는 삭제 완료, 정상 agent 0.2.0/2개 준비·Service 유지 확인 완료다. 앱·Namespace·클러스터·레지스트리는 Day 11을 위해 유지한다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10 최종 정리 요청 후): probe 일반 삭제·전체 Deployment/Pod/Service 조회의 사용자 출력을 확인한다. probe 부재 및 agent 2/2·앱 Pod 준비·Service 유지를 확인하기 전 정리 완료로 기록하지 않는다. 체크포인트는 아직이다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10 k9s 완료): Service 값 일치와 k9s 종료를 사용자 확인으로 기록했다. 다음은 사용자 요청 후 probe 최종 정리·정상 앱 유지 확인 및 체크포인트다. 앱/Service/Namespace/클러스터/레지스트리는 유지하며 Day 10 전체 완료는 아직 아니다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10 k9s Deployment 확인 후): k9s에서 :svc·Enter로 연 Service 목록의 agent Type/Cluster-IP/Ports를 확인한다. Deployment 2/2·최신 템플릿 복제본 2·가용 2는 확인 완료다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10 k9s 로그 확인 후): Esc로 Pod 목록 복귀 후 :deploy·Enter로 연 Deployment 화면의 agent 복제본 상태를 확인한다. 이후 Service 조회로 이어 가며 리소스를 변경하지 않는다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10 k9s Describe 확인 후): Esc로 Pod 목록 복귀 후 pwrhg 선택·소문자 l로 연 현재 로그 화면을 확인한다. 이후 Deployment/Service 조회를 진행한다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10 k9s Pod 화면 확인 후): k9s 화면 안에서 pwrhg 선택 후 d를 눌러 연 Describe 화면을 확인한다. 이후 로그/Deployment/Service 조회로 한 단계씩 진행하며 편집·삭제는 하지 않는다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10 k9s 사전 확인 후): k9s --context k3d-onprem -n ax-pilot --readonly -c pod 첫 화면을 확인한다. 사용자 캡처/표시 내용을 받은 뒤 조회 조작으로 진행한다. 옵션 오류 시 읽기 전용 옵션을 제거하지 말고 도움말을 확인한다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10 k9s 시작): Ubuntu k9s 경로/버전 및 현재 Deployment/Pod 조회 결과를 확인한다. 기존 정상 리소스로 화면 조회를 진행하며 고장 예제를 다시 만들지 않는다. 설치 여부/버전을 확인한 뒤 다음 명령을 안내한다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-6 완료): 고장 리소스 정리와 정상 앱 유지 확인 완료. 다음은 사용자 요청 후 k9s 확인 범위를 합의한다. Day 전체 정리(probe 삭제) 및 체크포인트는 아직이다. 앱·Service·probe·클러스터·레지스트리를 유지하며 재개 시 probe 상태를 확인한다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-6 진단 후): 지정 broken YAML 5개 foreground 삭제 및 전체 리소스 조회의 사용자 출력을 확인한다. b-* Deployment/ReplicaSet/Pod 부재와 정상 agent 2/2·Service 유지를 확인하기 전까지 10-6 완료로 기록하지 않는다. probe·클러스터·레지스트리는 유지한다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-6 ConfigError 진단 후): b-notready describe의 State·Ready·Readiness·Events 사용자 출력을 확인한다. 고장 예제 4개 진단 완료, 마지막 NotReady 및 정리는 아직이다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-6 Pending 진단 후): b-configerror describe의 설정 참조·State·Events 사용자 출력을 확인한다. ImagePull/CrashLoop/Pending 진단 완료, ConfigError/NotReady와 정리는 아직이다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-6 CrashLoop 진단 후): b-pending describe의 Requests·PodScheduled·Events 사용자 출력을 확인한다. ImagePull/CrashLoop 두 예제 진단 완료, 나머지 세 예제 진단 및 정리는 미완료다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-6): 이미지 9.9.9 태그 부재와 HTTP mirror 설정을 확인했다. b-crashloop의 describe 및 logs --previous 사용자 출력을 확인한다. 나머지 고장 진단·정리는 아직이며 정상 앱과 클러스터를 유지한다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-6 이미지 진단): SESSION 마지막 항목의 읽기 전용 조회 결과를 확인한다. Events의 HTTPS 오류만으로 HTTP mirror 설정 누락이나 태그 부재를 확정하지 않는다. b-imagepull 추가 진단 후 나머지 고장 예제를 진행한다.

최신 시작 지점(2026-10-05, Day 10의 10-6 고장 재현): 예제 5개 생성·증상 확인 완료. b-imagepull-6c78958d45-mg7rs의 describe/Events 출력을 확인하고 나머지 예제를 하나씩 진단한다. 정상 앱은 2/2이며 수정·삭제는 아직 하지 않았다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-6 사전 확인): 예제 5개 해시 일치·agent 2/2·기존 b-* Deployment/Pod 없음 확인 완료. 지정 YAML 5개 apply 후 상태 조회의 사용자 출력을 확인하고 Events/로그 진단으로 이어 간다. apply 오류 시 부분 생성 가능성을 확인한다. 정상 앱은 유지하며 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-6 시작): Ubuntu broken YAML 5개 체크섬과 ax-pilot Deployment/Pod 조회의 사용자 출력을 확인한다. 파일 일치와 기존 정상 앱·b-* 리소스 유무를 확인한 뒤 지정 고장 예제를 배포하도록 안내한다. apply·진단·정리는 아직이며 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-5 완료): pwrhg는 동일 Pod에서 liveness로 재시작 1 후 HTTP 200/Ready 복구했고 rslwh는 재시작 0이다. 최종 앱 0.2.0·Deployment 2/2를 유지한다. 다음은 사용자 요청 후 10-6이며 아직 진행하지 않는다. 재개 시 kubectl PATH/context·probe 상태 및 10-6 자료/사본을 확인한다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-5 재시작 관찰 확인): pwrhg가 재시작 1 후 1/1 Running으로 돌아왔다. watch 종료 후 UID·기준 UID의 이벤트·대상 HTTP·최종 리소스 조회 출력을 확인한다. hang을 다시 호출하지 않으며 10-5 완료는 아직이다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-5 probe 재준비 확인): 대상 pwrhg의 0.2.0/HTTP 200을 확인했다. UID/재시작 기준 조회·hang 1회·watch의 사용자 출력을 확인한다. 재시작 후 Ready 복귀 시 watch만 종료하며 오류 시 hang을 반복하지 않는다. 이후 UID·이벤트·HTTP 복구 확인이 필요하다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-5 probe 종료 확인): probe Succeeded로 exec가 거부돼 hang/watch는 실행되지 않았다. probe 재생성·Ready 및 pwrhg IP 10.42.0.7의 /healthz 응답을 먼저 확인한다. pwrhg 기준 UID는 SESSION에 기록했으며 RESTARTS=0이다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-5 사전 상태 확인): pwrhg(10.42.0.7)의 UID 기준값·hang 1회 응답·watch 출력을 확인한다. 재시작 후 Ready 복귀 시 watch만 Ctrl+C로 종료한다. 복구되지 않거나 curl 오류가 나면 hang을 반복하지 않고 진단한다. 이후 UID·이벤트·HTTP 확인이 필요하며 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-5 시작): 사용자 Deployment/Pod 상태·실제 readiness/liveness 설정 조회 출력을 확인한다. 앱 두 개 정상 및 probe 실행 상태를 확인한 뒤 대상 Pod 하나를 지정해 무응답/재시작 복구를 실습한다. 장애 주입·10-5 완료는 아직이며 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-4 완료): 0.2.0 앱 Pod pwrhg/rslwh만 Running이며 교체 Pod 정리까지 확인했다. 다음은 사용자 요청 후 10-5이고 아직 진행하지 않는다. 앱·클러스터·probe를 유지하며 재개 시 실습용 kubectl PATH/context와 probe 상태를 확인한다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-4 롤백 성공): agent 0.2.0 두 Pod 준비 및 HTTP 200 확인 완료. 교체된 jlrdl/wz225의 wait --for=delete 및 최종 리소스 조회 결과를 확인하고 10-4를 마무리한다. 추가 undo는 하지 않는다. 앱·클러스터·probe를 유지하며 10-5는 미진행이다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-4 롤링 업데이트 성공): agent 0.3.0 두 Pod 준비·HTTP 60회 성공을 확인했다. rollout history/undo/status 및 최종 리소스·HTTP 출력으로 직전 버전 0.2.0 복원을 확인한다. 오류 시 undo를 무조건 반복하지 않는다. 롤백 성공·10-4 완료는 아직이며 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-4 probe 준비 확인): probe Ready·업데이트 전 0.2.0 HTTP 200 확인 완료. HTTP 60회 관찰과 0.3.0 이미지 변경 명령 묶음의 출력을 확인한다. SUMMARY·종료 코드·응답 버전 전환·최종 리소스 상태를 검토하며 업데이트 성공·롤백은 아직이다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-4 축소 정리 확인): 앱 Pod stfrr/zqnxs만 남고 Deployment/ReplicaSet 2개 준비를 확인했다. 진단 Pod probe 재생성·Ready 및 Service /healthz HTTP 응답의 사용자 출력을 확인한다. 이후 롤링 업데이트 관찰로 이어 가되 현재 이미지 변경·롤백은 아직이다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-4 2개 복원 확인): stfrr/zqnxs가 Running이고 Deployment/ReplicaSet은 2개 준비다. 7642s/kjbqb의 wait --for=delete와 최종 리소스 조회 결과를 확인한다. 이후 probe 재준비가 필요하며 업데이트·롤백은 아직이다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-4 확장 확인): Deployment/ReplicaSet 4개 준비·앱 Pod 네 개 Running 확인 완료. replicas=2 복원·rollout·리소스 조회의 사용자 출력을 확인한다. probe Completed이며 HTTP 관찰 전에 재준비해야 한다. 업데이트·롤백은 아직이고 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-4 자가 치유 확인): 새 Pod 7642s 생성·기존 stfrr 유지 및 2/2 복구 확인 완료. replicas=4 명령과 rollout/리소스 조회의 사용자 출력을 확인한 뒤 2개 복원을 별도로 안내한다. probe Completed·업데이트·롤백 미진행 상태이며 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-4 사전 상태 확인): d7qcb Pod 하나 삭제·rollout status·리소스 조회의 사용자 출력을 확인한다. 새 이름의 Pod와 2개 Ready 복구 여부를 판단한다. probe는 Completed이므로 추후 HTTP 관찰 전에 재준비한다. 확장·업데이트·롤백은 아직이며 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-4 시작): 사용자 실습용 kubectl 버전·Deployment agent·Pod 전체 조회 출력을 확인한다. 준비된 앱 Pod와 현재 이름을 확인한 뒤 삭제할 Pod 하나를 지정해 자가 치유를 실습한다. Pod 삭제·확장·업데이트·롤백은 아직이며 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-3 완료): 포워딩 종료·39827 리스너 해제까지 확인했다. 다음은 사용자 요청 후 10-4이며 아직 진행하지 않는다. 앱·클러스터를 종료하거나 probe를 삭제하지 않았다. 재개 시 실습용 kubectl PATH·context와 필요한 Pod 상태를 확인한다. probe는 sleep 3600 종료 가능성이 있다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-3 HTTP 비교 성공): 포워딩 HTTP 4회 모두 같은 Pod 응답을 확인했다. 39827 리스너는 아직 LISTEN이다. 1번 터미널 Ctrl+C 종료 후 ss에서 리스너 해제를 확인한다. 10-3 전체 완료·10-4 진행은 아직 아니다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-3 포트 불일치 확인): 현재 포워딩은 39827이다. 1번 터미널을 유지하고 2번 Ubuntu 터미널에서 해당 포트로 HTTP 4회를 재검증한다. 성공 후 Ctrl+C 종료·ss 리스너 해제를 확인한다. 이전 포트 45537 및 추가 프로세스 진단 안내는 최신 시작 지점이 아니다. 10-3 미완료.

최신 시작 지점(2026-10-05, Day 10의 10-3 프로세스 확인): 45537 리스너 부재·kubectl PID 2495 존재까지 확인했다. 기존 포워딩 터미널의 최신 출력과 새 터미널의 ps·ss·readlink 결과를 받아 원인을 좁힌다. 10-3은 미완료이며 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-3 로컬 연결 실패): 첫 curl이 127.0.0.1:45537 연결에 실패했다. 기존 포워딩 터미널의 후속 출력과 프롬프트 복귀 여부, 새 Ubuntu 터미널의 ss·pgrep 출력을 확인한다. 원인 미확인·10-3 미완료이며 다음 절로 진행하지 않는다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-3 포워딩 기동 확인): 기존 Ubuntu 터미널의 포워딩을 유지하고 다른 Ubuntu 터미널에서 127.0.0.1:45537/healthz를 4회 호출한다. 성공 후 기존 터미널에서 Ctrl+C 종료 및 ss로 리스너 해제를 확인한다. 결과 대기 중이며 10-3 완료·10-4 진행은 아직 아니다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-3 내부 호출 확인): Service DNS·HTTP 8회 5:3 분산 확인 완료. 사용자 port-forward의 Forwarding 출력에서 실제 자동 할당 포트를 확인하고 다른 Ubuntu 터미널에서 비교 호출한다. 포워딩 종료·10-3 완료는 아직이다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-3 시작): 사용자 probe 생성·Ready·Service DNS·HTTP 8회 응답 Pod 이름 출력을 확인한다. 이후 port-forward 비교·종료로 이어 간다. 10-1·10-2 완료, 10-3 완료·10-4 진행은 아직 아니다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-2 완료): k3d-onprem/ax-pilot에 agent:0.2.0 Pod 두 개 Ready·Deployment 2/2 및 ClusterIP Service 생성 확인 완료. 앱·클러스터를 유지하고 사용자 요청 후 10-3 Service 접근으로 이어 간다. Service 통신·분산·port-forward 검증은 아직이다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-2 시작): 사용자 YAML 체크섬·apply·rollout·get all 출력을 확인한다. 대상은 k3d-onprem/ax-pilot의 agent 0.2.0 Pod 2개와 Service다. 10-1 완료를 유지하며 10-2 성공·완료·10-3 진행은 아직 아니다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10의 10-1 완료): onprem 클러스터·시스템·레지스트리와 agent 0.2.0/0.3.0 이미지 등록 확인 완료. 클러스터를 유지하고 사용자 요청 후 10-2 첫 배포로 이어 간다. 재개 시 실습용 kubectl PATH·k3d-onprem context·노드/레지스트리 상태 및 적용할 YAML의 두 사본 일치를 확인한다. 앱 배포·노드 이미지 pull·Day 10 전체 완료는 아직 아니다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10 이미지 등록 안내): 0.3.0 빌드와 두 이미지의 설정 확인 완료. 사용자 localhost:5001/ax/agent:0.2.0·0.3.0 push 로그/digest 및 태그 API 응답을 확인한다. 이미지 등록·10-1 완료·10-2 배포는 아직이며 클러스터는 유지한다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10 이미지 빌드 안내): 시스템 초기화·레지스트리 HTTP 200·빌드 소스 3개 일치 확인 완료. 사용자 agent:0.3.0 빌드 및 두 버전의 이미지 식별 정보·APP_VERSION 출력을 확인한 뒤 localhost:5001/ax/agent에 push한다. 10-1 전체는 미완료이며 클러스터를 유지한다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10 노드 Ready 확인): onprem 생성 성공·노드 3개 Ready 확인 완료. 사용자 시스템 Pod/Deployment·Docker 게시 포트·레지스트리 HTTP·agent 소스 해시 출력을 확인한 뒤 0.3.0 빌드와 이미지 등록으로 이어 간다. 클러스터는 유지하고 10-1 전체는 미완료다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10 클러스터 생성 안내): 사용자 onprem 클러스터 생성 로그·노드 상태·kube-system Pod·새 Docker 대역 출력을 확인한다. 이후 레지스트리와 0.2.0/0.3.0 이미지 준비·등록으로 이어 간다. 클러스터 생성 성공·10-1 완료·10-2 배포는 아직 아니다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10 Windows 포트 확인): 기본 8080·5001은 현재 Windows 점유·예약 제외 목록에 없다. Ubuntu 자원·Docker 컨테이너/이미지·리스너·주소 대역·Day 10 파일 존재 출력을 확인한 뒤 클러스터 생성으로 이어 간다. 아직 생성 명령은 안내하지 않았다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10 kubectl 준비 확인): 실습용 kubectl v1.31.0 설치·현재 셸 선택 확인 완료. Windows TCP 점유·IPv4/IPv6 제외 포트 범위 출력을 기다린다. 이후 Ubuntu 파일·이미지·자원 확인과 클러스터 생성으로 이어 간다. 새 Ubuntu 터미널에서는 실습용 PATH 재선택이 필요하다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10 첫 점검 확인): 사용자 kubectl v1.31.0 별도 설치 결과를 확인한다. 설치 후 현재 셸 PATH 선택이 필요하며 이후 포트·파일·자원을 점검한다. Docker 연결·k3d 버전·등록 클러스터 부재는 사용자 출력으로 확인했다. 아래 시작 지점은 이전 이력이다.

최신 시작 지점(2026-10-05, Day 10): 10-1 클러스터 생성 전 사용자 Ubuntu 도구 버전·Docker 연결·기존 클러스터 조회 결과를 기다린다. 이후 버전 호환성·Windows 포트·Ubuntu 파일 상태를 확인한다. 클러스터 생성 및 10-2 이후는 아직 미진행이다. 아래는 이전 이력이다.

최신 시작 지점(2026-10-05): Day 9의 9-1~9-5·실습 자원 정리와 PR #11 main 병합 확인 완료. Windows main은 2a0de14이며 병합 확인 메모만 로컬 미커밋 상태다. registry·UI는 제거됐고 regdata·이미지·반입 산출물·캐시는 보존했다. Ubuntu는 동기화하지 않았다. 다음 범위는 사용자 요청 후 정하며 누적 점검 2차·체크포인트 평가·고객사 제출은 미진행이다. Day 9 전체 통과로 판정하지 않는다. 아래 시작 지점들은 이전 이력이다.

최신 시작 지점(2026-10-01): Day 8 종료·PR #10 main 병합 및 Windows main 갱신 완료(6801a09). 8-1~8-4 실습·지정 자원 정리·공개 CA와 CA 이미지 보존을 확인했다. 체크포인트 해설은 제공했으며 독립 평가는 미실시다. Ubuntu 전체 동기화는 하지 않았다. 다음 학습은 사용자 요청 후 Day 9이며 아직 시작하지 않았다. 병합 확인 메모는 로컬 미커밋 변경이다. 아래 2026-09-30 시작 지점은 이전 이력이다.

최신 시작 지점(2026-09-30): Day 7은 7-1~7-5 학습·정리를 마치고 종료했다. 사용자 출력으로 컨테이너 4개·네트워크 2개 제거 및 프로젝트 잔존 목록 부재를 확인했다. 관찰용 mitm과 임시 빌드 이미지·폴더도 앞서 제거 확인했다. 이미지·볼륨·빌드 캐시 전역 정리는 수행하지 않았다. 체크포인트 6문항은 해설을 제공했으며 독립 답변 평가는 미실시다. 실제 빌드 프록시 통신 장애 재현 및 HTTPS/CA 시험도 미실시로 구분한다. 다음은 사용자 요청 후 Day 8 사내 CA와 TLS 검사이며 아직 시작하지 않았다. Day 7 기록은 Windows 사본에 갱신했다. 사용자가 완료·push를 요청해 codex/day07-results 브랜치에서 커밋·원격 반영을 진행한다. Ubuntu 동기화와 main 병합은 별도다.

1. Day 6 컨테이너·네트워크 제거와 8080 리스너 부재를 확인했다. 6-4 문서는 학습용 초안이며 실제 고객사 제출·정책 적용은 없다. 이미지·볼륨·/tmp/day06-compose.OTTiFi 백업은 삭제하지 않았다. 별도 자기점검·독립 진단 평가는 미실시다. Day 5 Stats·TUI 관찰 미확인, 5-2 ③ 최초 무응답 원인 및 Day 4 잔존 자원·미해결 사항은 유지한다.
2. Day 1의 정리 결과 확인·E-1 신청서 초안·최종 자기점검은 미완료로 유지하며 사용자가 재개할 때 이어 간다.
3. kubectl 고정 버전 불일치 등 미해결 사항을 완료로 간주하지 않는다.
