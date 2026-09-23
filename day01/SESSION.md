# Day 1 — 가상화 계층과 vSphere: 물리 서버부터 컨테이너까지

## 진행 상태
- 상태: 주요 개념 학습·1-3 기능 검증 완료. 컨테이너 정리 확인·VM 신청서 초안·최종 자기점검 남음
- 완료한 범위: 가이드 검토·계획, VM 격리·연동·SSH/SAC·vSphere 계층 질의응답, 1-2 질문 12개 해설, 1-3 도구 준비·대상 생성·연결·첫 적용·멱등성·내부 결과 확인. 1-3 정리와 Day 전체 체크리스트 판정은 아직 미완료
- 중단 지점: 두 대상 내부 생성 결과 정상 확인. 실습 컨테이너 두 개 삭제·가상환경 비활성화 결과 대기
- Codex 작업: 아직 별도 작업을 만들지 않음
- 실행 증거 기준: 사용자 제공 출력과 직접 검증 결과를 구분해 기록

## 2026-09-23 — 세션 결과 요약

| 범위 | 확인한 결과 | 남은 항목 |
|---|---|---|
| 개념·1-1 | VM/컨테이너 격리, vSphere 계층·리소스 풀, SSH/SAC, 고객사 역할을 학습. 예시 VM 2대의 메모리 합계 32GB 해석 | 최종 개념 자기점검 및 계층·포트그룹 해석 체크리스트 |
| 1-2 | VM 신청 질문 12개의 목적·확인할 답·배포 영향을 정리 | E-1 신청서 초안; 담당자·리드타임은 고객사 확인 필요 |
| 1-3 | 두 컨테이너에 Ansible 적용: 첫 실행 changed=3, 재실행 changed=0, 두 번 모두 failed=0·unreachable=0. 내부 계정·권한·파일 확인 | 컨테이너 삭제·deactivate 실행 확인 |

- 실행 위치: 사용자 Ubuntu WSL2의 `/home/user/onprem-lab/day01`. Codex는 사용자 출력을 대조하고 Windows 문서와 증거를 정리했다.
- 오류 해결: python3.12-venv 누락으로 ensurepip 실패 → 사용자가 패키지를 설치 → 가상환경 생성·Python/pip 경로 재확인 성공.
- 환경: Python 3.12.3, Ansible core 2.21.4, community.docker 5.3.0, Docker Engine 29.8.0. Python 자동 탐색 및 facts 자동 주입 변경 예고는 남아 있다.
- 실습의 의미: 인벤토리로 관리 대상을 지정하고 플레이북으로 계정·디렉터리·파일의 상태를 일관되게 맞췄다. Ansible은 실행 시점에 상태를 맞추며 지속적으로 감시하는 도구는 아니다.
- 검증 범위: 대상은 실제 VM이 아니라 컨테이너다. 에이전트 애플리케이션 배포, 실제 Docker 데몬 설정 적용, 고객사 통신 검증은 이번 실습 결과에 포함되지 않는다.
- 증거: [사전 확인](evidence/day01-13-precheck-user-2026-09-23.txt), [첫 적용](evidence/day01-13-first-playbook-user-2026-09-23.txt), [재실행](evidence/day01-13-second-playbook-user-2026-09-23.txt), [내부 상태](evidence/day01-13-state-user-2026-09-23.txt). 모두 사용자 제공 출력의 주요 내용 발췌이며 각 파일의 미확인 항목은 해당 단계 당시 상태다.
- 아래 날짜별 기록은 당시의 안내와 후속 결과를 순서대로 보존한다. 최신 상태는 이 요약과 맨 아래 인수인계를 기준으로 한다.

## 목표와 이번 세션 범위
2026-09-23 사용자 요청: 저장소와 지정한 가이드북을 읽고 오늘 진행할 Day 1의 할 일을 정리한다. 이번 범위는 계획 수립이며, 사용자 학습 완료 판정이나 실습 실행은 포함하지 않는다.
이후 개념 질의응답을 진행했고 사용자가 「실습 1.1로 넘어가자」고 요청했다. 현재 허용 범위는 실습 1-1이며 1-2·1-3으로 넘어가지 않는다.
후속으로 사용자가 1-2의 질문 12개를 제시하며 항목별 의미 정리를 요청했다. 이에 따라 범위를 1-2 설명까지 확장한다. 1-1 전체 완료나 1-2 신청서 작성 완료를 뜻하지 않으며 1-3은 진행하지 않는다.
이어 사용자가 「1-3을 해보자. 순서대로 내가 따라갈 수 있게 알려줘」라고 요청했다. 현재 범위는 1-3이며 사용자가 직접 한 단계씩 실행하고 Codex가 출력 확인 후 다음 단계를 안내한다. 이전 절의 미완료 체크리스트는 유지한다.

## 2026-09-23 — 가이드 검토 및 오늘의 계획

### 확인한 자료와 현재 상태
- 확인 주체: Codex가 Windows 저장소의 AGENTS.md, PROGRESS.md, docs/environment.md, Day 0 인수인계, Day 1 README·SESSION·실습 소스, 가이드 Day 1 및 부록 E-1·A-7을 직접 읽었다.
- 사용자가 지정한 `11. Final guidebooks/Agent Deploy Guide/onprem-agent-deploy-guide.html`의 Day 1 본문을 읽고 저장소 HTML과 SHA-256을 비교했다. 두 파일 모두 `EBD54A4EA2C1419E91505736B865194133E539AC305F09655D4F7CE42F50ABDE`로 동일하다.
- 최신 PROGRESS.md와 Day 0 실행 기록 기준으로 0-1~0-5 실습은 완료다. 루트 README.md와 AGENTS.md의 「0-1만 완료」 문구는 과거 상태이며, 오늘 학습의 출발점은 최신 상세 기록을 따른다. 해당 두 파일은 이번에 수정하지 않았다.
- Windows의 `day01/inventory.ini`와 `day01/prepare-vm.yaml`이 존재한다. 인벤토리는 두 컨테이너와 `community.docker.docker` 연결을 사용한다. 플레이북은 계정·디렉터리·설정 예시 파일을 만들고 OS·자원 정보를 출력한다.
- Ubuntu 복사본의 파일 일치 여부와 현재 Docker 실행 상태, Ansible 설치 여부는 이번에 확인하지 않았다. 기존 환경 기록을 오늘 직접 재검증한 결과로 취급하지 않는다.
- 사용한 조회: PowerShell의 `Get-Content`, `Select-String`, `Get-FileHash`, `rg`, `git status --short`, `git branch --show-current`. 조회 당시 작업 트리는 깨끗했고 브랜치는 `codex/day00-completion`이었다. 설치·컨테이너 실행·정리 명령은 실행하지 않았다.

### 진행 순서와 산출물
가이드의 전체 소요 시간은 약 2시간이다. 아래 순서로 한 단계씩 진행하고 사용자 결과를 확인한다.

| 순서 | 범위 | 해야 할 일 | 완료 판단 / 산출물 |
|---|---|---|---|
| 1 | 핵심 개념 | 물리 서버 → 하이퍼바이저 → 게스트 OS → 컨테이너 → 앱의 관계, ESXi·vCenter와 HA·vMotion·DRS, VM/컨테이너 격리 및 namespace/cgroup 이해 | 다섯 계층과 VM 복구·앱 복구의 차이를 자신의 말로 설명 |
| 2 | 조직·접근 방식 | 현업·IT기획·보안팀·IT운영의 역할, 승인과 실제 작업의 구분, SAC의 파일 전송·접속·sudo 제약 정리 | 항목별 담당자와 실제 소요 기간을 물을 질문 목록, 부록 A-7 리드타임 표 초안 |
| 3 | 실습 1-1 | 가이드의 모의 vSphere 화면에서 호스트·클러스터·데이터스토어·포트그룹·리소스 풀·VM Summary 읽기 | VM의 사양·HA·네트워크 존·저장소에 대해 확인할 질문을 설명 |
| 4 | 실습 1-2 | VM 신청 질문 12개를 정리하고 부록 E-1 신청서로 옮기기 | VM 신청서 초안. 확인한 값·학습용 가정·고객사 확인 필요 항목을 구분 |
| 5 | 실습 1-3 (선택) | Ubuntu에서 파일 확인 후 Ansible 환경 준비, 컨테이너 2개에 플레이북을 두 번 적용 | 두 대상 모두 실패/접속 실패 없이 수행되고 재실행 시 `changed=0`; 생성 결과 확인 후 실습 컨테이너 정리 |
| 6 | 자기점검·기록 | 가이드의 6문항과 필수 체크리스트 확인, 선택 실습 수행 여부 구분 | SESSION.md와 PROGRESS.md에 실제 완료 범위·증거·다음 시작점 기록 |

실제 고객사 정보가 없으므로 담당자·망 정보·소요 기간을 임의로 확정하지 않는다. 가이드 E-1의 사양은 예시이며 현재 PC의 요구 사양이나 고객사의 승인 사양으로 취급하지 않는다. vSphere 화면 실습에는 실제 vSphere 접속·설치가 필요하지 않다.

### 실습 1-2에서 준비할 질문 12개
1. vCPU·메모리·디스크, 증설 절차와 소요 기간
2. 표준 OS 종류와 버전
3. 배치할 망/존과 포트그룹
4. 인터넷 아웃바운드와 프록시 주소·포트·인증 여부
5. 사내 패키지 미러 주소
6. 허용하는 컨테이너 런타임과 설치 담당자
7. root/sudo 권한과 허용 범위
8. 백업 주기·HA·스냅샷 정책
9. SSH/SAC 접속 방식·파일 전송·세션 타임아웃
10. 보안 에이전트와 런타임의 충돌/예외 처리 여부
11. NTP와 타임존
12. DNS 서버와 사내 도메인

특히 7·9·10번을 VM 발급 전에 확인한다. 조직별 승인·작업 소요 기간, 변경관리 일정과 배포 가능 시간은 A-7 표와 함께 정리한다.

### 선택 실습 전에 확인할 사항
- 실행 위치는 Ubuntu WSL2의 `/home/user/onprem-lab/day01`이다. Windows 저장소와 자동 동기화된다고 가정하지 않는다.
- Ansible과 `community.docker` 설치, 컨테이너 생성은 1-3을 진행할 때 사용자에게 한 단계씩 안내한다. 이번 계획 정리에서는 실행하지 않았다.
- 이 실습의 `/etc/docker-daemon.json`은 대상 컨테이너 안에 쓰는 설정 예시 파일이다. 실제 Docker 데몬 설정 적용이나 프록시 연결 검증을 의미하지 않는다.
- 가이드에 실린 성공 출력은 참고값이며 이 PC의 성공 증거가 아니다. 실제 `changed`·`failed`·`unreachable` 결과를 별도로 기록한다.
- kubectl·dive·Compose 버전 차이는 환경 기록의 미해결 사항으로 유지한다. 1-1·1-2를 위해 이 도구를 변경할 필요는 없다.

## 배운 내용과 질문

### 2026-09-23 — VM 분리와 서버 접근 통제 질의응답
- 전용 VM에는 두 맥락이 있다. 기존 업무 시스템과 에이전트 전체를 분리하는 경우, 에이전트 본체와 신뢰하기 어려운 코드 실행·파일 처리 작업자를 추가로 분리하는 경우다.
- 별도 VM에서도 승인된 DB/API에 연결할 수 있다. 네트워크 도달 가능성, 계정 인증, 데이터·기능 접근 권한을 구분했다. VM 분리만으로 무거운 DB 조회의 영향이나 과도한 데이터 접근 권한이 해결되지는 않는다.
- 공용 에이전트 VM에 여러 에이전트를 컨테이너로 배포하고 이후 분리하는 방안을 논의했다. 함께 운영할 기준은 운영 담당·보안 요구·부하·허용 중단 시간이며, 에이전트 개수만으로 정하지 않는다. 자격 증명·데이터·네트워크·자원 제한을 구분하고 VM 추가와 서비스 이중화를 구별했다.
- SSH는 원격 서버의 셸에 암호화된 통신으로 접속하는 방식이다. 현재 PC 안의 WSL 셸과 원격 고객사 VM의 셸을 구분했다.
- 사용자 경험: KOICA에서는 신규 전용 VM을 요구했고 서버실의 인가 개발 PC에서만 배포가 가능했다고 설명했다. 사용자 진술이며 실제 고객사 구성·정책을 Codex가 검증한 것은 아니다.
- 인가 PC 제한은 접속 출발지 통제, SAC는 개인별 서버 접근과 작업 이력의 중앙 관리라는 차이를 설명했다. 둘은 함께 적용할 수 있다. KOICA의 SAC 사용 여부는 확인되지 않았다.
- SAC의 기능·세션 기록 범위는 제품과 정책에 따라 다르며, 서버 접속 허가와 OS 내부의 sudo·파일 권한은 별개다. 사용자도 「누가 언제 무엇을 했고 누구에게 어떤 권한을 줄지 통제」하는 취지로 이해를 정리했다.
- 이 질의응답은 학습 대화 기록이다. 실습 명령 실행이나 가이드 전체 자기점검 통과를 의미하지 않는다.

### 2026-09-23 — 실습 1-1 진행 방식 안내
- 사용자 요청: 실습 1-1로 이동하며 읽기만 하는 절인지, 로컬에서 실행 가능한지 질문.
- 가이드 원문은 실제 vSphere 조작 대신 모의 인벤토리 화면에서 어디를 보고 무엇을 물을지 익히도록 명시한다. 실행 명령이나 1-1용 프로그램은 제공하지 않는다.
- 현재 기록된 WSL2·Docker 환경은 vSphere 화면 실습 환경이 아니다. 실제 조작에는 별도 ESXi/vCenter 학습 환경이 필요하며 이번에는 설치하지 않는다.
- 가이드 예시의 `vm-ai-agent-01` 행에서 OS·vCPU·메모리·포트그룹을 읽는 것부터 진행한다. 이름으로 네트워크 존을 추정할 수 있지만 실제 연결·접근 허가는 별도 확인 대상이다.
- 확인 주체: Codex가 Windows 가이드 원문·기록을 읽고 안내. 사용자의 화면 해석 답변은 아직 받지 않았으므로 1-1 미완료.

## 가이드와 실제 환경의 차이
공통 환경은 [환경 기록](../docs/environment.md)을 참고한다.

## 2026-09-23 — 실습 1-1 후속 이해 확인과 1-2 항목 해설

- 사용자 답변: 모의 화면의 에이전트 VM은 2대, 메모리 합계는 32GB라고 정확히 읽었다. Codex는 vCPU 합계 8개도 설명했다.
- 리소스 풀의 128GB에서 VM 설정 합계 32GB를 뺀 96GB는 가이드의 단순 예산 계산으로 설명했다. 실제 vSphere의 추가 할당 가능량은 예약량·상한·오버헤드·물리 호스트 상태 등에 따라 달라지므로 그 값으로 확정하지 않는다. CPU 상한의 vCPU 개수 표기도 가이드의 단순화이며 실제 자원 설정과 구분한다.
- 리소스 풀은 VPC가 아니며 CPU·메모리 배분 단위라는 점, 네트워크는 포트그룹·가상 스위치 등으로 별도 관리한다는 점을 설명했다.
- vCenter → 논리적 Datacenter → 클러스터의 관계와, 클러스터의 호스트에서 VM이 실행되고 리소스 풀이 VM의 자원 배분을 관리한다는 차이를 설명했다. 기업당 vCenter 1개로 고정되지 않으며 VM 안의 OS에서 컨테이너를 실행하는 것은 선택이다.
- 사용자 요청에 따라 1-2 표의 질문 목적·받아야 할 답·이해할 개념을 정리한다. 고객사 담당자의 실제 답은 아직 없으며 확인한 구성으로 기록하지 않는다.

| 항목 | 확인하려는 답 | 학습상 핵심 |
|---|---|---|
| 1. 사양·증설 | 초기/최대 사양, 디스크 구성·성능, 증설 담당·기간·중단 여부 | VM 사양과 실제 부하를 비교하고 자원 부족에 대응할 시간 확보 |
| 2. OS | 표준 배포판·정확한 버전·CPU 아키텍처·지원/패치 정책·승인 이미지 | VM OS와 이미지 내부 사용자 공간을 구분; 커널·지원 정책 호환성 확인 |
| 3. 망/포트그룹 | 존·IP/대역·포트그룹·필요 통신 상대·방화벽 신청 주체 | 배치 위치만으로 통신 허용이 보장되지 않음 |
| 4. 아웃바운드/프록시 | 허용 목적지·포트, 프록시 주소·인증 방식, 승인 절차, 사내 CA 필요 여부 | 애플리케이션의 외부 API 호출과 Docker 데몬의 이미지 다운로드 경로를 각각 확인 |
| 5. 패키지 미러 | OS/Python/Node 저장소 주소, 필요한 버전·인증·추가 요청, 이미지 레지스트리 | 라이브러리 저장소와 컨테이너 이미지 저장소는 다름; 빌드·반입 방식 결정 |
| 6. 런타임 | 허용 제품·버전, 설치/유지보수 담당, Compose 등 배포 방식 지원 여부 | Docker·containerd·Podman을 동일한 명령 체계로 가정하지 않음 |
| 7. 관리자 권한 | 계정·허용 sudo 명령·컨테이너 관리 범위·대행 변경 절차 | 로그인 권한과 설정 변경 권한 구분; 일반 rootful Docker 관리 권한의 영향 고려 |
| 8. 복구 | 백업 대상·주기·보관·복원 시간, HA 범위, 스냅샷 승인·보관 | HA는 가용성 복구, 스냅샷은 단기 되돌리기, 백업은 별도 복구 수단이며 서로 대체하지 않음 |
| 9. 접속/전송 | 인가 PC·SSH/SAC·파일 반입·세션 종료·긴 작업·자동배포 지원 | 개발 산출물이 실제 서버에 도달하는 배포 경로를 설계 |
| 10. 보안 에이전트 | 설치 제품·버전·차단 정책·호환 사례·로그 확인/예외 승인 담당 | 애플리케이션 오류와 보안 제품의 차단/파일 잠금 구분; 보안 기능을 임의로 끄지 않음 |
| 11. 시간 | NTP 서버·동기 상태·담당자·표준 타임존·로그 표기 | NTP는 시계 정확도, 타임존은 시각 표시 기준 |
| 12. DNS | 내부 DNS·FQDN·도메인 접미사·신규 이름 등록·컨테이너 조회 | 이름→IP 변환과 네트워크 도달/서비스 인증을 구분 |

- 확인 주체: 대화의 사용자 답변과 Codex의 문서 기반 설명. 설치·컨테이너 실행·클러스터 생성·Ubuntu 동기화는 하지 않았다. Windows의 학습 기록만 갱신했다.

## 다음에 이어 할 지점
사용자의 컨테이너 삭제·목록 확인·가상환경 비활성화 출력을 확인한다. 기능·멱등성·생성 결과 검증은 완료했지만 정리는 아직 확인하지 않았다. 정리 확인 후 1-3 완료를 기록한다. 1-1 전체 체크리스트 판정과 1-2 신청서 완성은 미완료이며 Day 1 전체 완료가 아니다.

## 2026-09-23 — 실습 1-3 시작: 사전 확인 안내

- 사용자 실행 위치: Ubuntu WSL2. Windows에서는 Docker Desktop을 실행해 둔다.
- 목표: 컨테이너 두 개를 관리 대상 서버처럼 취급해 Ansible로 같은 설정을 적용하고, 재실행 시 변경이 없는지 확인한다. 실제 VM이나 vSphere 클러스터를 생성하는 실습은 아니다.
- 순서: 사전 확인 → Python 가상환경·Ansible 및 연결 플러그인 준비 → 대상 컨테이너 2개 생성 → 파일 내용 확인·플레이북 적용 → 재실행 `changed=0` 및 생성 결과 확인 → 실습 컨테이너 정리.
- 이번에 안내한 명령(아직 사용자 결과 없음):

```bash
cd ~/onprem-lab/day01 && pwd && ls -l inventory.ini prepare-vm.yaml && sha256sum inventory.ini prepare-vm.yaml
python3 --version
docker version
```

- 목적: Ubuntu 파일 존재·Windows 사본과 일치 여부, Python 버전, Docker Client/Server 응답을 확인한다. 경로 누락 시 임의로 빈 폴더를 만들거나 Windows 파일을 덮어쓰지 않고 원인을 먼저 확인한다.
- 확인 주체: Codex는 Windows의 가이드·기록·실습 소스만 읽고 Windows 파일 해시를 조회했다. Ubuntu 확인, Ansible 설치, 컨테이너 생성은 직접 실행하지 않았다. 이후 출력은 사용자 제공 실행 증거로 기록한다.

## 2026-09-23 — 실습 1-3: 1단계 통과 및 Python 가상환경 안내

- 확인 주체: 사용자 제공 Ubuntu 실행 결과. [주요 출력](evidence/day01-13-precheck-user-2026-09-23.txt).
- `/home/user/onprem-lab/day01` 경로, inventory.ini(122바이트), prepare-vm.yaml(1344바이트)을 확인했다. 두 파일 모두 SHA-256이 Windows 사본과 일치한다. 두 파일은 실행하는 셸 스크립트가 아니라 Ansible이 읽는 설정 파일이므로 표시된 실행 비트는 이번 실습의 필수 조건이 아니다.
- Python 3.12.3, Docker Client/Engine 29.8.0, API 1.56, linux/amd64, Docker Desktop 4.92.0(240144)을 사용자 출력으로 확인했다. Docker Client와 Server가 모두 응답했다.
- 다음 단계는 같은 Ubuntu 터미널의 day01 폴더에서 `.venv`를 생성하고 활성화하는 것이다. 가상환경은 Python 패키지용 별도 환경이며 VM 생성이 아니다.
- 안내 명령(아직 실행 결과 없음):

```bash
python3 -m venv .venv && source .venv/bin/activate
which python && python -m pip --version
```

- 첫 줄 오류 시 설치 단계로 넘어가지 않고 오류를 확인한다. 정상 시 Python 경로는 `/home/user/onprem-lab/day01/.venv/bin/python`이고 pip도 해당 `.venv` 경로를 가리켜야 한다. Ansible·community.docker 설치 및 대상 컨테이너 생성은 아직 하지 않았다.

## 2026-09-23 — 실습 1-3: ensurepip 오류 대응

- 확인 주체: 사용자 제공 실행 결과. Ubuntu `/home/user/onprem-lab/day01`에서 `python3 -m venv .venv && source .venv/bin/activate` 실행.
- 주요 오류: `The virtual environment was not created successfully because ensurepip is not available.` 실패 명령 경로는 `/home/user/onprem-lab/day01/.venv/bin/python3`. Ubuntu 오류 안내는 `apt install python3.12-venv`를 제시했다.
- 결과 의미: Python 자체는 실행되지만 새 가상환경에 pip를 준비하는 구성요소가 부족해 생성이 끝나지 않았다. `&&` 뒤 활성화는 실행되지 않았다. `.venv`는 일부 생성되었을 수 있으므로 완성된 가상환경으로 간주하지 않는다.
- 공식 근거: [Ubuntu 패키지 파일 목록](https://packages.ubuntu.com/noble/amd64/python3.12-venv/filelist)에 ensurepip 포함. [Python venv 문서](https://docs.python.org/3.12/library/venv.html)는 기본 생성 시 ensurepip로 pip를 준비하고 기존 디렉터리를 재사용한다고 설명한다.
- 해결 안내(사용자 실행 예정, 아직 완료 아님): 같은 Ubuntu 터미널에서 `sudo apt update && sudo apt install python3.12-venv`. 목록 갱신 후 필요한 패키지와 의존성을 설치한다. sudo 비밀번호는 터미널에만 입력하며 기록하지 않는다.
- 다음: 설치 출력 확인 후 기존 `.venv` 경로에서 생성·활성화 재시도. 임의 삭제·전역 pip 설치·Ansible 설치·컨테이너 생성은 하지 않았다.

## 2026-09-23 — 실습 1-3: venv 패키지 설치 완료

- 실행 위치·주체: 사용자 Ubuntu WSL2 `/home/user/onprem-lab/day01`.
- 실행 명령: `sudo apt update && sudo apt install python3.12-venv`.
- 사용자 출력: Ubuntu noble/noble-updates/noble-security/noble-backports 목록 조회 후 신규 패키지 3개 설치. `python3.12-venv` 3.12.3-1ubuntu0.17, `python3-pip-whl` 24.0+dfsg-1ubuntu1.3, `python3-setuptools-whl` 68.1.2-2ubuntu1.2 모두 `Setting up` 완료 후 셸 프롬프트 복귀.
- `0 upgraded, 3 newly installed, 0 to remove and 71 not upgraded.` 기존 패키지 업그레이드는 수행하지 않았고 `71 not upgraded`는 이번 설치 오류가 아니다.
- 결과 의미: 가상환경 생성에 필요한 OS 패키지 보완 완료. 원래 ensurepip 오류의 해소 판정은 가상환경 생성 재시도 결과로 확인한다.
- 다음 안내(아직 결과 없음): sudo 없이 `python3 -m venv .venv && source .venv/bin/activate`, 성공 후 `which python`과 `python -m pip --version`. 기존 `.venv`는 삭제하지 않고 재사용한다.
- Ansible 설치·컨테이너 생성은 아직 미진행이며 Codex는 Ubuntu 명령을 직접 실행하지 않았다.

## 2026-09-23 — 실습 1-3: 가상환경 확인 및 Ansible 설치 안내

- 확인 주체: 사용자 제공 Ubuntu 실행 결과. `python3 -m venv .venv && source .venv/bin/activate` 재실행 후 프롬프트에 `(.venv)` 표시.
- `which python`: `/home/user/onprem-lab/day01/.venv/bin/python`.
- `python -m pip --version`: `pip 24.0 from /home/user/onprem-lab/day01/.venv/lib/python3.12/site-packages/pip (python 3.12)`.
- 판정: 가상환경 생성·활성화 성공, Python·pip 모두 실습용 .venv 사용. 앞선 ensurepip 오류는 재실행 결과로 해소를 확인했다.
- 다음 안내(아직 설치 결과 없음):

```bash
python -m pip install ansible-core && ansible-galaxy collection install community.docker
ansible --version
ansible-galaxy collection list community.docker
```

- 실행 위치: 같은 Ubuntu WSL2 day01 폴더, 활성화된 .venv. sudo 없이 실행한다. ansible-core는 .venv에 설치되며 컬렉션은 기본적으로 사용자 홈의 `~/.ansible/collections`에 설치된다. 실제 설치 위치·버전은 사용자 출력으로 확인한다.
- 공식 [지원표](https://docs.ansible.com/projects/ansible/latest/reference_appendices/release_and_maintenance.html)에서 ansible-core 2.21의 관리 노드 Python 3.12 지원을 확인했다. [연결 플러그인 문서](https://docs.ansible.com/projects/ansible/latest/collections/community/docker/docker_connection.html)에서 community.docker 컬렉션 설치 명령을 확인했다. 가이드와 같이 버전 미고정 설치를 안내하며 실제 선택된 버전을 이후 기록한다.
- 설치가 실패하면 후속 명령·컨테이너 생성으로 넘어가지 않고 출력에 따라 진단한다. Codex가 설치를 대신 실행하지 않았다.

## 2026-09-23 — 실습 1-3: Ansible 설치 확인 및 대상 생성 전 조회

- 확인 주체: 사용자 제공 Ubuntu WSL2 출력. 활성화된 .venv, 현재 폴더 `/home/user/onprem-lab/day01`.
- 실행한 확인 명령: `ansible --version`, `ansible-galaxy collection list community.docker`.
- Ansible core 2.21.4, 실행 경로 `/home/user/onprem-lab/day01/.venv/bin/ansible`, Python 3.12.3(`/home/user/onprem-lab/day01/.venv/bin/python`) 확인. Jinja 3.1.6, PyYAML 6.0.3(libyaml 0.2.5).
- 컬렉션 `community.docker` 5.3.0, 컬렉션 루트 `/home/user/.ansible/collections/ansible_collections` 확인. `config file = None`은 별도 ansible.cfg를 읽지 않았다는 표시이며 설치 실패가 아니다.
- 판정: 도구 설치와 실행 위치 정상. 실제 컨테이너 연결·플레이북 실행은 아직 검증하지 않았다. 설치 명령의 전체 로그는 받지 않았으며 위 조회 결과로 버전·존재를 확인했다.
- 다음 사용자 안내(아직 결과 없음):

```bash
docker ps -a --filter "name=vm-agent-"
docker image inspect python:3.12.7-slim --format '{{.RepoTags}} {{.Os}}/{{.Architecture}}'
```

- 목적: 사용할 이름 vm-agent-01·vm-agent-02와 기존 컨테이너의 충돌 여부, 실습 이미지의 로컬 존재와 플랫폼 확인. 조회만 수행하며 컨테이너 생성·삭제·이미지 다운로드는 아직 하지 않는다.

## 2026-09-23 — 실습 1-3: 이름·이미지 확인 후 컨테이너 생성 안내

- 확인 주체: 사용자 제공 Ubuntu 실행 출력.
- `docker ps -a --filter "name=vm-agent-"`: 표 머리글만 출력, 해당 이름 패턴의 실행/중지 컨테이너 없음. 이번 실습의 vm-agent-01·vm-agent-02 이름 충돌이 없는 상태로 확인했다.
- `docker image inspect python:3.12.7-slim --format '{{.RepoTags}} {{.Os}}/{{.Architecture}}'`: `[python:3.12.7-slim] linux/amd64`. 로컬 실습 이미지 존재 확인.
- 다음 사용자 실행 안내(아직 생성 결과 없음):

```bash
docker run -d --rm --name vm-agent-01 python:3.12.7-slim sleep infinity
docker run -d --rm --name vm-agent-02 python:3.12.7-slim sleep infinity
docker ps -a --filter "name=vm-agent-"
```

- 각 컨테이너는 Python 이미지로 생성하고 `sleep infinity`를 실행해 관리 작업을 받을 동안 유지한다. 실제 VM·에이전트 애플리케이션이 아니라 Ansible 관리 대상 서버를 흉내 내는 컨테이너다.
- `-d`는 백그라운드 실행, `--name`은 인벤토리와 일치하는 대상 이름, `--rm`은 종료 시 컨테이너 자동 제거다. 이 실습에서 컨테이너 내부에 만든 파일은 컨테이너 제거 시 함께 사라진다. 포트 공개나 호스트 경로 마운트는 지정하지 않는다.
- 성공 기준은 두 생성 명령의 컨테이너 ID 출력과 목록의 두 이름 모두 `Up` 상태다. 사용자 결과 전에는 생성 완료로 기록하지 않는다. 플레이북은 아직 실행하지 않았다.

## 2026-09-23 — 실습 1-3: 대상 두 개 실행 확인 및 Ansible 연결 안내

- 확인 주체: 사용자 제공 Ubuntu WSL2 출력. 생성 명령 두 개 모두 컨테이너 ID 반환.
- vm-agent-01: `1489c9e5b2ed02f49042ada2604f8be5dffc1be4a34603bbc10b467eec10d794`.
- vm-agent-02: `fbda1d2fbdbbb9d8f5b4fe96f73e8bfc67668e4a246e911d1dab62bc399c672e`.
- 후속 `docker ps -a --filter "name=vm-agent-"`에서 두 컨테이너 모두 이미지 python:3.12.7-slim, 명령 sleep infinity, 상태 Up 12 seconds, 공개 포트 없음 확인.
- 판정: 대상 생성·실행 확인 완료. Ansible 연결과 플레이북 적용 여부는 아직 미확인.
- 다음 사용자 안내(아직 결과 없음):

```bash
cat inventory.ini
ansible -i inventory.ini agent_vms -m ansible.builtin.ping
```

- 인벤토리의 agent_vms 그룹에 vm-agent-01·vm-agent-02가 포함돼 있고 community.docker.docker 연결을 사용한다. 실제 SSH가 아니라 Docker CLI를 통한 컨테이너 접속으로 작업한다.
- Ansible ping은 ICMP 네트워크 ping이 아니라 대상 연결과 Python 모듈 실행을 확인하는 검사다. 두 대상 모두 SUCCESS, ping: pong이어야 다음 설정 적용 단계로 넘어간다. [공식 모듈 문서](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/ping_module.html).
- 실습 컨테이너 두 개가 실행 중이며 아직 정리하지 않았다. 실패 시 무조건 삭제하지 않고 출력에 따라 연결·Python·플러그인을 진단한다.

## 2026-09-23 — 실습 1-3: Ansible 연결 통과 및 플레이북 첫 실행 안내

- 확인 주체: 사용자 제공 Ubuntu 출력. cat inventory.ini로 agent_vms 그룹의 두 대상과 community.docker.docker 연결을 확인했다.
- `ansible -i inventory.ini agent_vms -m ansible.builtin.ping`: vm-agent-01·vm-agent-02 모두 SUCCESS, changed: false, ping: pong.
- 두 대상 모두 discovered_interpreter_python은 `/usr/local/bin/python3.12`. 다른 Python 설치 시 자동 탐색 결과가 바뀔 수 있다는 경고가 나왔지만 현재 모듈 실행은 성공했다. 관리 노드 .venv 경로와 대상 컨테이너의 Python 경로는 서로 다르다. 경고를 숨기거나 인벤토리를 변경하지 않았다.
- 다음 사용자 실행 안내(아직 결과 없음):

```bash
cat prepare-vm.yaml
ansible-playbook -i inventory.ini prepare-vm.yaml
```

- 플레이북은 agent_vms 두 대상에 계정 appuser(UID 10001, nologin), /opt/agent/config·data·logs(owner appuser, 0750), /etc/docker-daemon.json 예시 파일(0644)을 만들고 수집한 OS·메모리·CPU 정보를 출력한다.
- /etc/docker-daemon.json은 대상 컨테이너 내부의 연습용 파일이다. 실제 Docker Desktop 데몬에 설정을 적용하거나 예시 프록시에 연결하는 작업은 없다. CPU·메모리 facts는 컨테이너가 관찰한 값이며 전용 VM 할당 사양으로 해석하지 않는다.
- 첫 실행의 예상 요약은 각 대상 ok=5, changed=3, unreachable=0, failed=0이며 실제 성공 판단은 사용자 출력으로 한다. 파일 task의 디렉터리 3개는 loop로 처리되므로 changed 작업 수와 생성 파일/디렉터리 개수는 다르다.
- 오류가 나면 그 상태에서 진단하고 재실행·정리 단계로 넘어가지 않는다. 대상은 여전히 실행 중이다.

## 2026-09-23 — 실습 1-3: 플레이북 첫 실행 성공

- 확인 주체: 사용자 제공 Ubuntu 출력. `cat prepare-vm.yaml` 확인 후 `ansible-playbook -i inventory.ini prepare-vm.yaml` 실행.
- [주요 실행 결과와 경고](evidence/day01-13-first-playbook-user-2026-09-23.txt).
- 두 대상 모두 PLAY RECAP `ok=5 changed=3 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0`. 계정 생성·디렉터리 loop·설정 예시 파일 작성이 changed, facts 수집·debug가 ok다. changed=3은 변경한 작업 수이며 디렉터리 3개를 개별 작업 3개로 세지 않는다.
- 두 대상 모두 debug 결과 `Debian 12.8, mem 15577MB, cpu 32`. 해당 컨테이너가 관찰한 OS/호스트 자원 정보이며 각각 전용 메모리 15577MB·CPU 32개를 보장받았다는 뜻은 아니다. 이번 docker run에는 CPU·메모리 제한을 지정하지 않았다.
- 기존 인터프리터 자동 탐색 경고 외에 INJECT_FACTS_AS_VARS 기본값 True의 deprecation 경고가 추가됐다. 사용자 출력은 ansible-core 2.24에서 제거 예정이라고 알리며 prepare-vm.yaml 39행의 top-level fact 참조를 지적한다. 현재 2.21.4에서는 실행 성공이다.
- 향후 호환성 대응은 `ansible_distribution` 등의 참조를 `ansible_facts['distribution']` 등으로 변경하는 것이다. 이번에는 동일 파일의 멱등성 확인을 위해 소스와 경고 설정을 변경하지 않았다. Windows·Ubuntu 사본 모두 실습 시작 시 확인한 소스를 유지한다.
- 다음 안내(아직 두 번째 실행 결과 없음): 같은 Ubuntu day01 폴더의 .venv 활성화 상태에서 `ansible-playbook -i inventory.ini prepare-vm.yaml` 재실행. 출력을 tail로 자르지 않고 두 대상의 작업·경고·PLAY RECAP을 확인한다.
- 다음 성공 기준: 두 대상 모두 changed=0, failed=0, unreachable=0. 대상 컨테이너는 계속 실행 중이며 정리하지 않았다.

## 2026-09-23 — 실습 1-3: 재실행 멱등성 확인

- 확인 주체: 사용자 제공 Ubuntu 출력. 동일한 `ansible-playbook -i inventory.ini prepare-vm.yaml` 재실행.
- 두 대상 모두 `ok=5 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0`. 모든 작업과 디렉터리 loop 항목이 ok. [주요 출력](evidence/day01-13-second-playbook-user-2026-09-23.txt).
- 첫 실행 changed=3 → 두 번째 changed=0으로 이번 플레이북의 멱등성을 확인했다. 가이드의 선택 체크포인트 「플레이북 두 번 실행, 두 번째 changed=0」 충족. 모든 Ansible 명령이나 플레이북이 자동으로 멱등이라는 뜻은 아니다.
- 인터프리터 자동 탐색 및 facts 자동 주입 변경 경고는 동일하게 남았으나 실패는 없다. 이번 확인을 위해 소스나 경고 설정을 변경하지 않았다.
- 다음은 Ansible이 만든 상태를 직접 관찰하는 학습 단계다. 아래 읽기 명령을 두 컨테이너 각각에 안내했으며 아직 조회 출력은 받지 않았다.

```bash
docker exec vm-agent-01 sh -c 'getent passwd appuser && ls -ld /opt/agent/* /etc/docker-daemon.json && cat /etc/docker-daemon.json'
docker exec vm-agent-02 sh -c 'getent passwd appuser && ls -ld /opt/agent/* /etc/docker-daemon.json && cat /etc/docker-daemon.json'
```

- 관찰점: appuser UID 10001·nologin, config/data/logs 소유자 appuser·0750, 예시 설정 파일 0644 및 로그 10m/3·예시 프록시 설정. 그룹 ID는 플레이북에서 고정하지 않았으므로 특정 숫자를 요구하지 않는다.
- 내부 결과 확인 후 정리할 예정이다. vm-agent-01·02는 계속 실행 중이며 .venv도 활성 상태다.

## 2026-09-23 — 실습 1-3: 생성 결과 확인 및 정리 안내

- 확인 주체: 사용자 제공 두 컨테이너의 docker exec 조회 출력. [주요 출력](evidence/day01-13-state-user-2026-09-23.txt).
- 두 대상 모두 appuser UID/GID 10001, 홈 /home/appuser, 셸 /usr/sbin/nologin. config/data/logs는 appuser:root, 0750. /etc/docker-daemon.json은 root:root, 0644, 274바이트.
- 설정 내용은 json-file, max-size 10m, max-file 3, 가이드의 예시 프록시 주소와 no-proxy 목록으로 일치한다. 실제 데몬 적용·프록시 연결은 이번 실습 범위가 아니다.
- 디렉터리 그룹 root는 플레이북에 group 설정이 없어서 유지된 값으로 오류가 아니다. 계정의 기본 그룹과 파일의 그룹 소유권을 구분한다.
- 판정: 두 대상 설정 적용·멱등성·생성 결과 관찰까지 완료. 마지막 정리만 남았다.
- 다음 사용자 안내(아직 정리 결과 없음):

```bash
docker rm -f vm-agent-01 vm-agent-02
docker ps -a --filter "name=vm-agent-"
deactivate
```

- 사용자 요청으로 수행 중인 1-3의 정리 단계다. 이번 실습에서 만든 이름 두 개만 제거하고 내부 연습용 계정·파일도 함께 제거된다. 이미지·Ubuntu의 day01 소스·.venv·사용자 Ansible 컬렉션은 삭제하지 않는다.
- 성공 기준: 삭제 출력에 두 이름, 후속 목록은 표 머리글만, deactivate 후 프롬프트에서 (.venv) 제거. 삭제 오류가 나면 결과를 보고 원인을 확인한다. 사용자 결과 전에는 정리 완료로 기록하지 않는다.

## 2026-09-23 — Day 1 회고: 실제로 수행한 일과 의미

사용자가 「lab1에서 무엇을 했는지, 특히 마지막 실습이 구체적으로 무엇인지」 정리를 요청했다. 아래는 완료된 사용자 실행 결과에 근거한 설명이다. 정리 명령은 안내만 했고 아직 실행 결과가 없다는 상태를 유지한다.

### Day 1 학습 흐름
- 1-1: 고객사 vSphere의 VM 사양·자원 배분·실행 위치를 읽는 법. vCenter·Datacenter·클러스터·ESXi 호스트·리소스 풀·VM의 관계와 네트워크/스토리지 관점의 차이를 다뤘다.
- 1-2: VM 발급 전에 사양뿐 아니라 OS·통신 경로·설치 권한·파일 반입·복구·보안·시간·DNS 조건을 확인해야 하는 이유를 설명했다. 고객사의 실제 답을 채운 VM 신청서를 완성한 것은 아니다.
- 1-3: 두 관리 대상에 같은 초기 설정을 자동 적용하고, 동일 상태에서 다시 실행하면 변경하지 않는다는 것을 검증했다.

### 1-3의 구성요소
| 구성요소 | 실제 위치/역할 |
|---|---|
| .venv | Ubuntu day01 폴더 안의 Python 패키지 환경. Ansible 설치에 사용하며 VM이 아님 |
| Ansible | Ubuntu에서 실행한 설정 자동화 도구. 인벤토리와 플레이북을 읽고 각 대상에 작업 수행 |
| inventory.ini | 어디에 작업할지 정의. vm-agent-01·02와 community.docker.docker 연결 방식 |
| prepare-vm.yaml | 어떤 상태를 만들지 정의. 계정·디렉터리·설정 파일과 정보 출력 |
| Docker 컨테이너 두 개 | Docker Desktop 엔진이 실행하는 연습 대상. 실제 VM을 생성한 것은 아님 |

동작 흐름: Ubuntu의 Ansible → Docker CLI/연결 플러그인 → 각 컨테이너 내부 Python 모듈 실행. 이번에는 SSH나 SAC를 통과하지 않았다. Ansible 자체는 관리하는 Ubuntu의 .venv에 설치했고 대상 이미지에는 Python이 들어 있었다.

### 대상 안에 만든 상태
- appuser 계정: UID 10001, nologin, /home/appuser. 서비스 실행에 사용할 계정을 준비한 것이며 이번 실습에서 실제 에이전트를 그 계정으로 실행한 것은 아니다.
- /opt/agent/config·data·logs: 설정·데이터·로그를 둘 디렉터리, 소유자 appuser·0750. 아직 애플리케이션 데이터나 로그를 채우지는 않았다.
- /etc/docker-daemon.json: root:root·0644, json-file 및 로그 크기 10m/파일 수 3, 예시 프록시 값을 담은 파일. 실제 Docker 데몬의 /etc/docker/daemon.json에 적용하거나 Docker를 재시작한 것이 아니다.
- OS·메모리·CPU 정보는 관찰/출력만 했다. 컨테이너마다 독립 VM 수준의 자원을 할당한 것으로 해석하지 않는다.

### 두 번 실행한 이유와 결과
- 첫 실행: 원하는 계정·디렉터리·파일이 없어 만들었고 두 대상 모두 changed=3·failed=0.
- 두 번째: 이미 지정한 상태이므로 두 대상 모두 changed=0·failed=0. 이번 플레이북의 멱등성을 확인했다.
- 후속 docker exec 조회: Ansible 성공 메시지와 실제 대상 내부 결과가 일치하는지 계정·소유자·권한·파일 내용을 직접 관찰했다.
- 실무 연결: 여러 VM을 받은 뒤 같은 준비 작업을 수동 반복하는 대신, 인벤토리로 대상을 지정하고 검토 가능한 플레이북으로 상태를 맞추는 방식이다. 실제 VM에 옮길 때는 SSH/SAC 접근·계정 권한·배포판·설정 경로·서비스 반영 방법을 별도로 조정해야 한다.

핵심 산출물은 두 대상에 일관되게 적용된 초기 설정과 그 실행 증거다. VM 발급 자동화, 에이전트 애플리케이션 배포, 사내 DB/API 연결, 실제 프록시 적용, vSphere HA 구성은 수행하지 않았다. 1-3의 기능 검증은 끝났고 삭제·가상환경 비활성화는 아직 사용자 확인 대기다.

## 2026-09-23 — Ansible의 역할과 고객사 적용 방식 질의응답

- 사용자가 원하는 상태를 선언해 환경을 맞추는 도구인지 질문했다. 이번 user/file/copy 모듈의 동작이 이에 해당한다고 설명했다. 실행 시점에 상태를 맞추며 지속 감시는 아니고, 임의 shell/command 작업까지 자동으로 멱등이 되는 것은 아니다.
- 후속 질문은 실제 고객 환경에서 Ansible을 어떻게 사용하는지다. 초기 계정·디렉터리·런타임·CA 설정, 애플리케이션 배포/버전 변경, 반복 운영 작업·상태 확인을 플레이북으로 관리하는 역할을 설명한다. 이는 사용 사례이며 이번 실습에서 모두 실행했다는 뜻이 아니다.
- 실제 적용 예: 인프라팀이 VM·통신 경로·계정 권한을 제공 → 개발자가 inventory/playbook과 필요한 설정·이미지 버전을 준비 → 테스트 및 고객사의 검토·승인 → 인가된 실행 환경에서 운영팀 또는 승인된 배포 주체가 수행 → 결과 확인·이력 보관.
- Ansible 관리 노드는 승인된 Linux 실행 환경·자동화 서버 등이 될 수 있고 일반적인 Linux 대상에는 SSH로 접속한다. 전용 상주 Ansible 프로그램은 대상마다 필요하지 않지만 다수 Linux 모듈에는 대상 Python과 적절한 권한이 필요하다. 이번 실습에서는 Docker 연결을 사용했다.
- KOICA 사례의 인가 PC 제한을 지키면서 실행 환경과 서버 접근 경로를 정해야 한다. SAC의 자동화용 비대화형 접속 지원을 확인해야 하며 웹 터미널만 허용된다는 이유로 Ansible 자동 실행까지 가능하다고 가정하지 않는다. 허용되지 않으면 승인된 운영팀 실행 환경 등을 협의한다.
- Ansible은 고객사 접근 권한·sudo·방화벽 승인 자체를 만들어 주지 않는다. 승인된 자격 증명과 권한으로 작업한다. 일반 ansible-core 실행과 조직 차원의 승인/감사 시스템도 구분한다.
- 근거: [Ansible 설치/agentless 구조](https://docs.ansible.com/projects/ansible/latest/installation_guide/intro_installation.html), [관리 노드·대상 개념](https://docs.ansible.com/projects/ansible/latest/getting_started/index.html), [플레이북 실행](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_execution.html).
- 추가 설치·실습 실행은 하지 않았다. 컨테이너 정리 및 deactivate 결과 대기 상태도 유지한다.

## 2026-09-23 — 실제 컨테이너 배포 순서와 FDE·고객사 역할

- 사용자 질문: 만든 에이전트를 Docker 컨테이너로 실제 배포하는 순서와 각 단계 담당자가 누구인지.
- Codex가 Windows의 agent/Dockerfile·app.py·requirements.txt와 Day 1 조직 역할 가이드를 직접 읽었다. 이미지 빌드·컨테이너 실행 등 새 실습은 수행하지 않았다.
- 현재 agent는 학습용 더미다. Dockerfile은 Python 기반 이미지에 PyYAML과 app.py를 포함하고 USER 10001, 기본 8000 포트, CMD python app.py, /healthz 검사를 정의한다. app.py는 LLM_BASE_URL이 없으면 /ask에서 에코를 반환한다. DB_DSN의 설정 여부를 진단하지만 업무 DB 조회 로직을 구현한 것은 아니다.
- 배포 개념: 소스·의존성·Dockerfile → 버전이 식별되는 이미지 빌드·검증 → 승인된 레지스트리 또는 오프라인 반입 → 대상 VM의 Docker가 이미지와 런타임 설정으로 새 컨테이너 생성·실행 → 기능·연동·운영 검증 및 이관.
- 역할 분담은 고객사 정책·계약에 따라 정한다. FDE가 설계·배포 산출물·검증·문제 해결을 주도하더라도 인프라 발급·보안 승인·DB 권한·운영 변경 권한까지 자동으로 갖는 것은 아니다.
- 예시 역할: 현업은 업무 요구·인수 기준, FDE는 데이터 흐름·요구 자원·Dockerfile/이미지·배포 설정·검증·런북, 인프라팀은 VM/OS/기반 환경, 보안팀은 보안성·반입·통신 정책 승인, 네트워크 운영은 승인된 통신 설정, 데이터 소유자/DBA는 DB 접근 승인·계정 발급, IT운영/플랫폼팀은 승인된 런타임·운영 배포·모니터링 등을 담당.
- Docker 실행 단계는 승인된 FDE가 수행하거나, 운영팀이 FDE 산출물로 실행하거나, 고객사 CI/CD·자동화 계정으로 수행할 수 있다. KOICA 인가 PC 규칙은 실행 위치 제한이며 FDE에게 모든 권한이 있다는 의미는 아니다.
- 이미지에 비밀 값을 포함하지 않고 고객사가 승인한 방식으로 실행 시 자격 증명을 제공한다. 실제 포트 공개·영속 데이터 연결·재시작 정책·로그 수집·헬스체크와 기능/연동 검증은 배포 정의에 포함한다. 컨테이너 Up 또는 /healthz 성공만으로 업무 기능 완료를 단정하지 않는다.
- Day 1 Ansible 실습과의 연결: 관리 대상 준비 작업의 일부를 자동화했다. 실제 배포 플레이북이라면 승인된 이미지 수신·컨테이너 구성/갱신·검증까지 자동화할 수 있지만 이번 prepare-vm.yaml에는 해당 작업이 없다. 실제 환경의 호스트 설정과 컨테이너 이미지 내부 설정도 구분한다.
- 참고: [Docker 이미지 빌드·배포](https://docs.docker.com/get-started/docker-concepts/building-images/build-tag-and-publish-an-image/), [컨테이너 실행](https://docs.docker.com/engine/containers/run/). 설치·배포·네트워크 변경은 설명만 했고 실행하지 않았다. 기존 1-3 컨테이너 정리 출력은 여전히 대기 중이다.

## 2026-09-23 — Day 1 완료 여부 확인

- 사용자 질문: 「좋아 그러면 day1끝인가」. 가이드의 마지막 체크리스트와 실제 기록을 대조했다. 종료나 컨테이너 정리 실행의 명시적 확인으로 해석하지 않는다.
- 주요 개념 및 vSphere 계층·사양 읽기는 대화로 진행했다. 가이드 최종 자기점검 6문항과 다섯 계층·포트그룹 해석의 전체 완료 판정은 별도로 하지 않았다.
- 1-2는 질문 12개의 의미를 설명했지만 부록 E-1 양식에 옮긴 신청서 초안은 아직 없다. 고객사 실제 정보를 받을 필요 없이 연습용 가정과 확인 필요 항목을 구분해 작성할 수 있다. 담당자·리드타임 정보도 실제 확인값 없이 확정하지 않는다.
- 1-3은 두 대상의 첫 적용 changed=3, 재실행 changed=0, 실패 없음과 내부 생성 결과까지 확인해 핵심 실습·선택 멱등성 체크포인트를 충족했다. 컨테이너 삭제와 deactivate 출력은 아직 받지 않았다.
- 남은 마무리: 정리 실행 확인, E-1 신청서 초안, 최종 개념 자기점검. Day 1 전체를 완료로 표시하지 않으며 다음 Day로 넘어가지 않는다.

## 2026-09-23 — 세션 기록 정리 및 PR 인수인계

- 사용자 요청: Day 1 결과를 로컬 리포에 정리하고 SESSION·PROGRESS를 갱신한 뒤 GitHub PR을 만든다.
- Windows에서 결과 요약·상세 학습 이력·오류 해결·사용자 출력 증거 4개를 정리했다. PROGRESS는 현재 상태 중심으로 정리하고 환경 기록의 내부 조회 상태를 갱신했다.
- GitHub 조회로 Day 0 PR #2의 main 병합(`065e7b9`)을 확인했다. 같은 파일 트리를 기준으로 새 브랜치 `codex/day01-results`에서 Day 1 변경만 제출한다.
- 이번 작업은 기록 정리와 Git 제출이다. Ubuntu 소스 동기화, 패키지 설치, 컨테이너 실행·삭제, 플레이북 재실행은 수행하지 않았다. 실습 소스와 가이드 원문도 변경하지 않았다.
- 다음 시작 지점: 사용자의 컨테이너 정리 결과를 확인하고, 지정한 범위에서 E-1 신청서 초안과 최종 자기점검을 진행한다. 고객사의 실제 구성·담당자·리드타임은 확인값과 학습용 가정을 구분한다.
- `docker rm -f vm-agent-01 vm-agent-02`, `docker ps -a --filter "name=vm-agent-"`, `deactivate`는 앞서 안내한 명령이며 실행 완료 증거는 아직 없다. 다음 세션에서는 실제 상태와 기존 터미널의 가상환경 활성 여부부터 확인한다.
- PR 제출을 Day 1 전체 완료나 main 병합으로 간주하지 않는다. 제출 결과는 아래에 이어 기록한다.

### 제출 결과

- [PR #3 — Day 1 학습·Ansible 실습 결과와 인수인계 정리](https://github.com/shanis345/Deploy_Practice/pull/3)를 생성했다. `codex/day01-results` → `main`, 생성 시 open·미병합 상태다.
- 본문·환경·증거 7개 파일을 커밋 `abd5a71`로 제출했고, PR 링크와 제출 결과는 후속 문서 커밋으로 기록한다.
- 검증: `git diff --cached --check` 통과, 변경 문서의 로컬 링크 정상, 실습 파일 두 개의 SHA-256은 사전 확인값과 일치. Ubuntu 실습을 재실행한 결과는 아니다.
- GitHub CLI 조회는 인증 오류가 있어 연결된 GitHub 도구로 PR 상태 조회·생성을 수행했다. 로컬 Git 작성자 설정은 기존 커밋의 작성자 정보를 명령 단위로 적용했으며 전역 설정은 변경하지 않았다. Git push는 성공했다.
