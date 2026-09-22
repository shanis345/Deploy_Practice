# Day 0 — 환경 준비

## 진행 상태
- 날짜: 2026-09-23 (0-1 완료 기록은 2026-09-22)
- 상태: **Day 0 실습 완료 — 0-1~0-5 완료**
- 완료한 범위: WSL2 확인, Docker Desktop 연동·권한 해결, 실습 파일 복사, 부트스트랩 실행과 최종 점검, http-echo 실행, whoami HTTP 응답 확인 및 컨테이너 정리
- 추가 완료 범위: `agent:0.1.0` 이미지 빌드, healthz·diag·ask API 응답, UID/GID 확인 및 agent 컨테이너 정리
- 최종 완료 범위: lazydocker 0.25.2 교체 후 이미지·네트워크 화면 확인 및 0-5 실습 폴더 확인
- 중단 지점: Day 0 실습 완료. Day 1 미진행
- Codex 작업: 이 프로젝트를 준비한 기존 대화. 별도 Day 0 작업은 아직 생성하지 않음
- 실행 증거 기준: 2026-09-22 실습 및 2026-09-23의 0-2~0-5 실습은 사용자 제공 출력·화면이며, 2026-09-23 환경 재점검은 Codex 직접 실행 결과다.

## 목표와 이번 세션 범위
Windows의 Ubuntu WSL2와 Docker Desktop으로 실습 환경을 준비한다.
최초 범위는 0-1까지였으며, 2026-09-23 사용자 요청으로 0-2~0-5를 순차 안내하고 사용자 실행 결과를 확인했다. 0-4의 API 오류도 해결했다. Day 1은 아직 요청받지 않았다.
Day 0의 실습 절 0-1~0-5 및 마지막 실습 체크리스트 3개를 충족했다. 개념 자기점검 4문항에 대한 사용자 답변 평가는 별도 진행하지 않았다.

## 2026-09-23 — 실습 결과 요약

Day 0에서 수행한 흐름은 **준비된 소스 → Docker 이미지 빌드 → 컨테이너 실행 → HTTP 응답·실행 사용자 확인 → 컨테이너 정리 → 이미지·네트워크 관찰**이다. 에이전트 코드를 새로 작성한 것이 아니라 실습북에 포함된 프로그램을 패키징하고 배포·검증했다.

| 절 | 수행한 작업 | 성공을 판단한 결과 | 증거 기준 |
|---|---|---|---|
| 0-1 | WSL2·Docker 연결, 도구·이미지 확인 | Desktop 실행 후 check 전 항목 ✓, 종료 코드 0, 이미지 12개 존재 | 초기 사용자 출력 + Codex 직접 재점검 |
| 0-2 | http-echo 및 whoami 실행, HTTP 요청, 정리 | v1.0.0 출력, localhost:8081에서 컨테이너 정보 응답, hello 삭제 성공 | 사용자 터미널 출력 |
| 0-3 | agent:0.1.0 빌드·실행·API 검증·정리 | 빌드 FINISHED, healthz ok, ask offline 에코, UID 10001/GID 0, agent 삭제 성공 | 사용자 터미널 출력 |
| 0-4 | lazydocker 업데이트 후 리소스 확인 | 0.25.2에서 API 오류 해소, agent:0.1.0(189.09MB), bridge·host·none 표시 | 사용자 버전 출력·스크린샷 |
| 0-5 | Ubuntu 실습 폴더 목록 확인 | agent, bootstrap.sh, day01~day13, skeleton 존재 | 사용자 터미널 출력 |

남겨둔 산출물은 Ubuntu의 실습 소스와 Docker의 `agent:0.1.0` 이미지다. `hello`·`agent` 실습 컨테이너는 삭제했다. 다른 프로젝트의 컨테이너·이미지·네트워크·볼륨은 변경하지 않았다. Windows의 이 SESSION.md와 evidence는 학습 기록이며 Ubuntu 사본에 자동 반영되지 않는다.

## 실행 기록

### 2026-09-22 — WSL2 확인
실행 위치: Windows PowerShell.

```powershell
wsl --list --verbose
wsl -d Ubuntu
```

Ubuntu와 docker-desktop이 모두 VERSION 2, STATE Stopped로 표시됐다.
Stopped는 당시 실행 중이지 않다는 뜻이며 설치 실패가 아니다. Ubuntu 셸 진입을 확인했다.

### Docker Desktop 연결
Ubuntu에서 `docker version`과 `docker compose version`을 실행하자 Docker 명령을 찾을 수 없고 WSL integration 활성화를 권하는 메시지가 나왔다.
Docker Desktop의 Settings → Resources → WSL Integration에서 Ubuntu 연결을 활성화하도록 안내했다.
이후 사용자 출력에서 Docker CLI 29.7.2와 Compose v5.5.1이 실행되는 것을 확인했다. 설정 화면 자체를 직접 검증한 것은 아니다.

### Docker 소켓 권한 해결
처음에는 `/var/run/docker.sock` 연결에서 permission denied가 발생했다.

```bash
id
ls -lL /var/run/docker.sock
getent group docker
```

- 소켓: `srw-rw---- 1 root docker ... /var/run/docker.sock`
- 그룹 등록: `docker:x:1001:user`
- 당시 `id`에는 docker 그룹이 없었음
- 결론: 사용자 등록은 되어 있지만 현재 셸에 그룹 변경이 반영되지 않음

```bash
newgrp docker
id
docker version
docker compose version
```

재확인한 `id`에는 `gid=1001(docker)`와 docker 그룹이 표시됐다.
Docker Client와 Server가 모두 출력됐고 Server는 Docker Desktop 4.90.0, Engine 29.7.2였다.
새 그룹 생성·사용자 추가·소켓 권한 변경은 하지 않았다.
`getnt` 오타와 붙여넣기 제어문자로 인한 실패는 정확한 `getent group docker` 재입력으로 해결했다.

### 실습 파일 복사와 사전 점검
실행 위치: Ubuntu 홈 폴더.

```bash
mkdir -p ~/onprem-lab
cp -rn "/mnt/c/Users/user/Desktop/Applications/25. BCG X/7. 준비/11. Final guidebooks/Agent Deploy Guide/onprem-lab/." ~/onprem-lab/
cd ~/onprem-lab
ls
chmod +x bootstrap.sh
./bootstrap.sh check
```

`ls`에서 agent, bootstrap.sh, day01~day13, skeleton을 확인했다.
`cp -n`의 이식성 경고는 있었지만 이후 파일 목록과 스크립트 실행으로 복사를 확인했다.
초기 점검에서는 k3d, helm, k9s, lazydocker, dive, jq가 없었고 나머지 항목은 통과했다.

### 부트스트랩 실행과 최종 점검
패키지 목록 갱신 명령 `sudo apt-get update`를 먼저 안내했다. 이 명령의 출력은 공유되지 않아 실행 성공 여부를 별도로 단정하지 않는다.
사용자는 다음 명령의 최종 출력을 제공했다.

```bash
./bootstrap.sh
```

[최종 점검 출력](evidence/bootstrap-final.txt)에 따르면 이미지 12개가 모두 `있음`이며 모든 도구 점검이 통과했다.
공유된 마지막 실행에는 개별 도구 설치 로그가 없으므로 어느 실행에서 설치됐는지는 단정하지 않는다.
최종 상태에서는 도구가 존재하고 Docker 엔진과 Compose가 응답한다.

## 오류와 해결

다음 표는 2026-09-22~23에 실제 겪은 문제를 모은 것이다. **같은 증상이라도 원인을 구분한 뒤 필요한 조치만 적용했다.** 실행 명령과 원본 출력은 아래 날짜별 기록 및 evidence 링크에서 확인한다.

| 증상 | 확인한 원인 또는 상태 | 해결·결과 |
|---|---|---|
| Ubuntu에서 docker를 찾지 못함 | WSL 연동 필요 메시지 | 연동 설정 안내 후 CLI 실행 확인 |
| docker.sock permission denied | 현재 셸에 docker 그룹 미반영 | newgrp docker 후 Server 응답 확인 |
| 다음 날 Docker·Compose 실행 실패, kubectl 미검출 | Docker Desktop 미실행. Docker·kubectl 링크 대상 `/mnt/wsl/docker-desktop/cli-tools`와 소켓이 없음. 현재 셸의 docker 그룹은 정상 | 사용자가 Desktop 실행 → check 종료 코드 0, Docker Client/Server 29.8.0 및 kubectl 1.36.1 확인. 재설치·그룹 변경 불필요 |
| lazydocker `client version 1.25 is too old`, 최소 API 1.40 요구 | lazydocker 0.23.3은 API 1.25를 고정 사용하여 현재 Docker와 호환되지 않음 | 공식 0.25.2 바이너리 다운로드 → 임시 폴더에서 버전 확인 → sudo install로 교체 → 실제 이미지·네트워크 화면 확인 |
| lazydocker 다운로드가 약 32KB에서 느려짐, 예상 시간이 2시간 이상으로 표시 | 약 4.8MB 파일의 당시 전송 속도가 매우 낮았음. 네트워크 저하의 근본 원인은 확인하지 않음 | 중단 후 연결 제한 15초·전체 제한 120초를 둔 curl로 재시도 → 100% 다운로드. 제한 시간이 속도를 높였다고 단정하지 않음 |
| Docker Desktop에서 만든 것이 안 보인다고 느낌 | 컨테이너는 실습 종료 시 삭제했으며 이미지와 별개임. UI 필터나 실제 조회 위치는 직접 확인하지 않음 | 이미지·컨테이너 차이 설명 후 사용자가 agent:0.1.0이 보인다고 응답. 재빌드·재실행하지 않음 |
| Ubuntu에 day14 폴더가 없음 | 가이드 예시와 bootstrap.sh 생성 목록이 다름. 실제 Day 14는 skeleton 사용 | 소스·가이드 대조 후 정상 구성으로 기록. 불필요한 폴더 생성 없음 |
| getnt 또는 제어문자가 포함된 명령 실패 | 오타·붙여넣기 문제 | 정확한 getent 재입력 |
| cp -n 경고 | 옵션 이식성 경고 | 파일 목록과 check 실행으로 복사 확인 |

### 재현 가능한 해결 순서

- **연결 실패:** Windows의 Docker Desktop 실행 상태 확인 → Ubuntu의 `docker version`에서 Client와 Server 확인 → 소켓 오류가 남으면 `id`, `ls -lL /var/run/docker.sock`, `getent group docker`로 현재 그룹과 소켓 소유권 비교. `newgrp docker`는 그룹 등록이 이미 되어 있고 현재 셸에만 미반영된 경우에 사용했다.
- **lazydocker API 오류:** Docker 명령 자체의 동작과 TUI 동작을 구분 → 오류에 나온 요청 API와 최소 API 비교 → 공식 소스에서 고정 API 사용 확인 → lazydocker만 업데이트 → `--version`뿐 아니라 실제 화면까지 재확인.
- **느린 다운로드:** 진행률·파일 크기·전송 속도를 읽고 대기 예상치를 해석 → 중단 후 같은 URL로 제한 시간을 두고 재시도 → 완료 출력 확인 → 압축 해제·임시 바이너리 확인 후 설치. 실제 사용한 명령은 아래 업데이트 기록에 보존했다.

## 핵심 Lessons

1. **실행 위치와 파일 위치를 먼저 구분한다.** 실습 명령은 Ubuntu WSL2에서 실행한다. Windows 프로젝트와 `~/onprem-lab`은 별도 복사본이다. Windows 파일을 수정했다고 Ubuntu 실행 소스가 바뀌지는 않는다.
2. **Docker Engine, Docker CLI, lazydocker의 역할은 다르다.** 엔진이 컨테이너를 실행하고 CLI는 엔진에 명령을 보낸다. lazydocker는 상태 조회와 관리를 돕는 TUI다. TUI 오류가 곧 에이전트나 엔진의 실패를 뜻하지 않는다. 이번 환경은 Docker Desktop 실행이 Ubuntu 연결의 전제다.
3. **소스·이미지·컨테이너는 서로 다른 산출물이다.** `docker build -t agent:0.1.0 .`은 소스를 이미지로 패키징한다. `docker run`은 이미지로 새 컨테이너를 만든다. `docker rm -f agent`는 컨테이너를 삭제하며 이미지는 유지한다. Docker Desktop에서도 Images와 Containers를 구분해 본다.
4. **성공은 실제 응답으로 확인한다.** 빌드 FINISHED는 이미지 생성 성공, 긴 컨테이너 ID는 실행 요청 성공, `/healthz`의 ok는 서버 응답 성공이다. 이 증거들은 서로 대체되지 않는다. `/healthz`가 외부 LLM·DB 연결까지 보장하는 것도 아니다.
5. **포트 매핑은 호스트에서 컨테이너로 읽는다.** `127.0.0.1:8081:8080`은 내 PC의 루프백 주소·8081 포트를 컨테이너의 8080에 연결한다. 컨테이너 IP와 내 PC 접속 주소는 다르며 호스트명·IP·접속 원본 포트는 가이드 예시와 달라도 정상이다.
6. **권한의 등록 상태와 현재 적용 상태를 구분한다.** docker 그룹에 사용자가 등록돼 있어도 현재 셸에는 반영되지 않을 수 있다. 컨테이너 내부의 `UID=10001, GID=0`은 appuser 실행이며 GID 0만으로 root 사용자(UID 0)가 되는 것은 아니다.
7. **설치 확인과 런타임 호환성은 다르다.** bootstrap.sh check의 ✓는 버전 고정값 일치와 후속 기능 동작을 보장하지 않는다. 실제로 lazydocker는 check를 통과했지만 API 오류가 났고, 업데이트 후 화면 검증으로 해결했다. Compose의 check 문구 `v2`도 실제 버전 출력과 구분한다.
8. **실행 중인 리소스와 전체 보유 리소스를 구분한다.** 기본 네트워크는 bridge·host·none이며 화면의 null은 none의 드라이버다. 다른 프로젝트의 종료된 컨테이너나 추가 네트워크가 보여도 이번 실습 오류로 단정하거나 정리 대상으로 삼지 않는다.
9. **시간·속도·재시도 결과로 판단한다.** 다운로드 예상 시간은 당시 속도로 계산한 값이다. 재시도가 성공했다고 원인을 확정하거나 timeout 옵션 자체가 속도를 개선했다고 기록하지 않는다.
10. **실습의 목적은 배포와 운영 검증이다.** 이번에는 실습북에 미리 준비된 작은 에이전트를 빌드하고 실행했다. 이후 같은 프로그램으로 네트워크·프록시·인증서·Kubernetes·관측성을 학습한다.

### 후속 질문에서 정리한 에이전트의 의미

- `agent:0.1.0`은 빈 이미지가 아니다. 소스에 상태 확인, 설정 진단, 외부 HTTP/TCP 연결 검사, 프롬프트 파일 재적재, 요청 수 지표, LLM 호출과 실습용 장애 재현 기능이 구현돼 있다.
- 이번에 실제 검증한 것은 healthz·diag·offline ask·실행 사용자다. 다른 엔드포인트는 소스에서 존재를 확인했지만 아직 실행 검증한 것은 아니다.
- `(echo) 안녕`, `mode: offline`은 LLM 설정이 없어 입력을 돌려주는 분기다. 실제 LLM 답변은 아니다. LLM 연결 설정 시 질문을 전달하는 코드가 있지만 RAG, 대화 이력 저장, 자율적인 계획·도구 선택 로직은 없다.
- `/diag`의 비밀 처리 범위도 정확히 읽는다. 현재 코드에서 LLM 키·DB DSN은 설정 여부만 반환하지만 LLM 주소·프록시·CA 경로 등 일부 항목은 값을 반환한다. 가이드의 설명을 모든 값이 가려진다는 보장으로 해석하지 않는다. 이번 출력의 LLM·프록시 설정은 `(unset)`이었다.
- 사용자가 Docker Desktop에서 이미지가 안 보인다고 질문한 뒤 `agent:0.1.0`을 찾았다고 응답했다. 제안한 `docker image ls agent` 명령의 출력은 받지 않았으므로 실행 완료로 기록하지 않는다.

## 가이드와 실제 환경의 차이
- kubectl: 가이드 v1.31.0, 실제 v1.36.1. 기존 설치를 스크립트가 유지함.
- dive: 가이드 본문 0.12.0, 첨부 스크립트 설정과 실제 설치는 0.13.1.
- Compose: 가이드 표기는 v2, 실제 출력은 v5.5.1. `docker compose` 실행이 확인됐으며 이후 실습 호환성 검증을 뜻하지는 않음.
- lazydocker: 가이드·bootstrap.sh 0.23.3, 실제 설치는 API 호환 오류 해결을 위해 0.25.2로 변경했다. bootstrap.sh의 고정값은 그대로다.
- 디렉터리: Ubuntu는 day01~day13과 skeleton으로 구성된다. 가이드 예시의 day14는 없지만 Day 14 실습 경로는 skeleton이다.
- [전체 환경 기록](../docs/environment.md)을 참고한다. lazydocker 외 버전 차이는 조정하지 않았다.

## 프로젝트 정리
후속 사용자 요청으로 Windows의 `12. Deploy Practice` 폴더에 실습 소스·가이드·원본 ZIP·기록을 복사해 배치했다.
원본과 Ubuntu의 `/home/user/onprem-lab`은 그대로 유지했다. 이 작업에서 실습 명령을 재실행하지 않았다.
이후 사용자가 만든 [https://github.com/shanis345/Deploy_Practice](https://github.com/shanis345/Deploy_Practice)에 자료를 PR로 제출하도록 요청했다.
Git 초기화와 `codex/initial-practice-setup` 브랜치 준비는 프로젝트 관리 작업이며 실습 진도에 포함하지 않는다.
Codex 프로젝트 등록과 Day별 작업 생성은 아직 하지 않았다.

## 2026-09-23 — Windows 프로젝트의 GitHub 연결

- 범위: 사용자가 현재 폴더를 기존 GitHub 저장소에 연결하도록 요청했다. 실습 진도는 0-1 완료 상태를 유지한다.
- 실행 위치: Windows PowerShell, 이 프로젝트 폴더. Codex가 직접 실행·검증했다.
- 시작 상태: `codex/initial-practice-setup`은 커밋이 없는 로컬 브랜치였으며 원격 저장소는 미설정이었다.
- `git remote add origin https://github.com/shanis345/Deploy_Practice.git`과 `git fetch origin`으로 원격 이력을 가져왔다.
- GitHub 기본 브랜치는 `main`, 최신 커밋은 `3c8a290`(초기 구성 PR #1 병합)이었다.
- `git read-tree origin/main`으로 파일을 덮어쓰지 않고 인덱스를 등록했다. `git diff origin/main`과 미추적 파일 조회 결과 차이가 없었다.
- `git branch --track main origin/main`과 `git symbolic-ref HEAD refs/heads/main`으로 로컬 `main`을 연결했다. 연결 직후 `git status --short --branch`는 `## main...origin/main`만 출력했다.
- Git 메타데이터 소유자가 샌드박스 계정이라 일반 사용자 명령에서 `dubious ownership`이 발생했다. 연결 명령에는 현재 폴더에 한정한 `safe.directory`를 적용했고, 이후 일반 사용자 Git 전역 설정에도 이 프로젝트의 절대 경로만 신뢰 경로로 등록했다.
- 일반 샌드박스의 원격 조회는 자격 증명 오류가 있었으며, 승인된 일반 사용자 실행으로 기본 브랜치와 원격 접근을 확인했다.
- 이 연결 작업에서는 커밋·푸시를 실행하지 않았다. 연결 확인 후 `PROGRESS.md`와 이 기록을 갱신했다. Ubuntu 복사본에는 변경하지 않았다.
- 다음 시작 지점: 아래와 같이 0-1 완료 상태에서 사용자 지정 범위를 기다린다.

## 2026-09-23 — Day 0의 0-1 로컬 상태 재점검

- 사용자 요청: 제시한 Day 0 준비 및 0-1 완료 상태와 현재 로컬 환경이 맞는지 확인.
- 실행 위치: Windows PowerShell에서 호스트·WSL 상태 조회, `wsl -d Ubuntu`로 Ubuntu 내부 도구·파일 조회. 설치 작업은 하지 않았다.
- Windows 자원은 RAM 31.18GiB, C: 여유 454.53GiB로 권장치 이상이다. Ubuntu 24.04.1 LTS 및 WSL2를 직접 확인했다.
- Ubuntu 실습 폴더와 bootstrap.sh 실행 권한 755, LF, Windows 사본과 동일한 SHA-256을 확인했다.
- 실제 점검: `wsl -d Ubuntu --cd /home/user/onprem-lab --exec ./bootstrap.sh check`. 종료 코드 1이며 kubectl, Docker 데몬, Compose 항목이 실패했다. 최초 묶음 명령의 출력 내 종료 코드 표시는 셸 전달 과정 때문에 신뢰하지 않고, 이 단독 실행의 종료 코드로 판단했다.
- 원인 증거: Docker Desktop 프로세스가 없고 docker-desktop 배포판은 Stopped. Docker·kubectl의 심볼릭 링크 대상인 `/mnt/wsl/docker-desktop/cli-tools`와 Docker 소켓이 없다. 현재 셸에는 docker 그룹이 적용돼 있어 이전 그룹 미반영 문제와 다르다.
- 도구 버전은 k3d 5.7.4, helm 3.16.2, k9s 0.32.5, lazydocker 0.23.3으로 본문과 일치했다. dive는 0.13.1로 스크립트와 일치하지만 본문 0.12.0과 다르다. kubectl의 이전 버전 1.36.1은 현재 재검증하지 못했다.
- Docker 엔진이 꺼져 있어 실습 이미지 12개는 현재 재확인 불가다. 삭제됐다고 판단하지 않는다.
- 샌드박스의 WSL 조회는 E_ACCESSDENIED로 실패했고 승인된 일반 사용자 실행으로 재조회했다.
- [주요 명령과 출력](evidence/local-check-2026-09-23.txt)을 저장하고 환경 기록과 진행 현황을 함께 갱신했다.
- 다음 사용자 단계: Windows에서 Docker Desktop을 실행하고 엔진이 준비되면 알려주기. 이후 같은 0-1 범위에서 check와 버전·이미지를 재조회한다. 0-2 이후는 진행하지 않았다.

## 2026-09-23 — Docker Desktop 실행 후 0-1 재확인

- 사용자 제공 상태: Docker Desktop을 실행했다고 알림.
- Codex 직접 실행: Windows PowerShell에서 `wsl -d Ubuntu --cd /home/user/onprem-lab --exec ./bootstrap.sh check`. 모든 항목 ✓, 종료 코드 0.
- Ubuntu에서 Docker Client / Server 29.8.0, Compose v5.5.1, kubectl v1.36.1을 직접 확인했다. 기존 Docker 29.7.2 기록보다 버전이 높지만, 업데이트 시점이나 경로는 확인하지 않았다.
- Docker 소켓 root:docker 660, 현재 사용자의 docker 그룹 적용 및 데몬 응답을 확인했다. Desktop 실행 전의 Docker·kubectl 미검출은 해소됐다.
- `wsl -d Ubuntu --exec docker image inspect`에 bootstrap.sh의 12개 이미지 태그를 직접 전달했다. 12개 모두 RepoTags가 출력됐으며 종료 코드 0이다.
- 첫 이미지 조회용 셸 반복문은 변수 전달 문제로 빈 이름을 조회했으므로 그 결과는 이미지 유무 판단에서 제외했다. 위 직접 명령으로 재검증했다.
- 결론: 0-1 부트스트랩 점검 및 이미지 준비를 현재 환경에서 재확인했다. 고정 버전까지 완전히 일치하는 상태는 아니며 kubectl·dive·Compose 차이를 유지한다.
- 설치·이미지 다운로드·버전 조정·컨테이너 실행은 하지 않았다. 0-2 이후는 미진행이다.
- [점검 증거](evidence/local-check-2026-09-23.txt)에 후속 결과를 이어 쓰고 PROGRESS.md와 환경 기록을 갱신했다.

## 2026-09-23 — 0-2 Docker 동작 확인 및 정리 완료

실행 위치: Ubuntu WSL2 터미널, 사용자 홈 디렉터리(`~`). 모든 명령은 사용자가 직접 실행하고 출력을 공유했다. Codex는 명령을 안내하고 제공된 결과를 검토했으며 이 실습 명령을 대신 실행하지 않았다.

1. `docker run --rm hashicorp/http-echo:1.0 -version`: `http-echo v1.0.0 (866d8f8313e92d96f940c2f0cf807abe934ab145)`와 빌드 시각 출력 후 프롬프트 복귀. 컨테이너에서 프로그램 실행·종료 성공.
2. `docker run --rm -d --name hello -p 127.0.0.1:8081:8080 traefik/whoami:v1.10 --port 8080`: 컨테이너 ID `0b247fc16c3ab5ed74ee4f97d67cfdea167c5929fd48e6383e807646258db4bd` 출력.
3. `sleep 1` 후 `curl -s localhost:8081`: Hostname `0b247fc16c3a`, IP `127.0.0.1`, `::1`, `172.17.0.2`, RemoteAddr `172.17.0.1:60770`, `GET / HTTP/1.1`, `Host: localhost:8081` 응답. 호스트 8081 → 컨테이너 8080 전달과 HTTP 응답 성공.
4. `docker rm -f hello`: `hello` 출력 후 프롬프트 복귀. 사용자 제공 출력 기준 컨테이너 정리 성공. 이미지 삭제 명령은 실행하지 않았다.

- 배운 내용: 이미지로 컨테이너 실행, `--rm`의 종료 후 자동 삭제, `-d`의 백그라운드 실행, 호스트 포트와 컨테이너 포트의 구분, HTTP 응답에서 컨테이너 식별, `docker rm -f`로 실행 중인 실습 컨테이너 정리.
- 가이드 예시와 호스트명·접속 원본 포트가 달라도 정상이며, `::1`은 IPv6 루프백 주소다.
- 오류: 공유된 실행 결과에서 오류 없음. 이 절의 남은 질문은 현재 없다.
- [사용자 제공 실행 증거](evidence/day00-02-user-output-2026-09-23.txt)를 저장했다. 0-2는 완료했으며 Day 0 전체 완료는 아니다.

## 2026-09-23 — 0-3 학습용 에이전트 이미지 빌드·검증·정리 완료

실행 위치: Ubuntu WSL2의 `/home/user/onprem-lab/agent`. 사용자가 직접 명령을 실행하고 결과를 제공했다. Codex는 빌드나 컨테이너 실행을 대신 수행하지 않았다.

1. `ls -la`: app.py, requirements.txt, Dockerfile, .dockerignore와 Dockerfile.ca 존재 확인. 이번 빌드는 기본 Dockerfile을 사용했다.
2. `docker build -t agent:0.1.0 .`: `Building 3.1s (13/13) FINISHED`, Python 3.12.7-slim 기반 빌드 및 의존성 설치 성공, `naming to docker.io/library/agent:0.1.0` 확인.
3. `docker run -d --rm --name agent -p 127.0.0.1:8000:8000 agent:0.1.0`: 컨테이너 ID `88a08d0a5b632b4f81be7dc41b9ba973bbfa7fe17096fe6b139e37713f961338` 출력.
4. `sleep 2` 후 `curl -s localhost:8000/healthz`: status `ok`, version `0.1.0`, host `88a08d0a5b63` 확인.
5. `/diag` 결과를 jq로 추린 사용자 출력: uid 10001, gid 0, llm_base_url 및 대소문자 프록시 환경 변수 6개 모두 `(unset)`.
6. `curl -s -X POST localhost:8000/ask -H 'Content-Type: application/json' -d '{"question":"안녕"}'`: answer `(echo) 안녕`, mode `offline`, prompt_sha `e3b0c44298fc`. LLM 미연결 상태에서 에코 응답하는 경로를 확인했으며 실제 LLM 호출을 검증한 것은 아니다.
7. 사용자 제공 실행 사용자 출력: `uid=10001(appuser) gid=0(root) groups=0(root)`. UID 0이 아닌 사용자로 실행하며 GID 0인 구성을 확인했다. GID 0은 UID 0과 동일하지 않다.
8. `docker rm -f agent`: `agent` 출력 후 프롬프트 복귀. 컨테이너 정리 성공이며 이미지 삭제 명령은 실행하지 않았다.

- 붙여넣은 명령 줄에는 `/diag` jq 식 뒤의 중복 따옴표와 `docker exec agent idd` 표기가 있지만 이어진 출력은 정상 결과다. 정확한 실행 문자열은 별도 확인하지 않았으며, 이를 실제 실행 오류로 단정하지 않는다. 가이드의 정상 명령은 `docker exec agent id`이다.
- 오류·남은 질문: 공유된 결과에서 빌드·API·정리 오류 없음. 이 절의 남은 질문은 현재 없다.
- [사용자 제공 출력 발췌](evidence/day00-03-user-output-2026-09-23.txt)를 저장하고 PROGRESS.md를 함께 갱신했다. Windows 기록만 수정했으며 Ubuntu 소스는 변경하지 않았다.

## 2026-09-23 — 0-4 lazydocker API 호환 오류

- 사용자에게 Ubuntu에서 `cd ~/onprem-lab`, `lazydocker` 실행을 안내했다. 사용자가 오류 화면을 첨부했다.
- 화면 하단 버전은 0.23.3. 오류: `client version 1.25 is too old. Minimum supported API version is 1.40`. Retry count 32, 이미지·네트워크 목록은 비어 있었다. 목록 미표시는 리소스 삭제 증거가 아니다.
- 원본 사용자 스크린샷: `C:/Users/user/Desktop/Applications/25. BCG X/7. 준비/11. Final guidebooks/Agent Deploy Guide/communications/lazydocker오류.png`. Codex가 첨부 이미지를 판독했으며 Ubuntu에서 오류를 직접 재현한 것은 아니다.
- 공식 v0.23.3 소스의 APIVersion 상수는 1.25이고 클라이언트 생성 시 명시적으로 고정한다. 환경 변수만으로 바꾸는 해결책은 안내하지 않았다.
- 공식 v0.25.2 소스는 API 버전 협상을 사용한다. 오류 진단 당시 임시 바이너리 검증 → 교체 → TUI 재확인 순서로 진행하기로 했다. 실제 완료 결과는 바로 아래 업데이트 기록에 구분했다.
- 확인 자료: https://raw.githubusercontent.com/jesseduffield/lazydocker/v0.23.3/pkg/commands/docker.go , https://raw.githubusercontent.com/jesseduffield/lazydocker/v0.25.2/pkg/commands/docker.go , https://github.com/jesseduffield/lazydocker/releases/tag/v0.25.2
- 의미: bootstrap.sh check는 도구 존재·버전 출력만 확인하므로 이번 런타임 호환 오류를 검출하지 못했다. 가이드 고정 버전과 실제 Docker 조합의 추가 차이로 기록한다.

## 2026-09-23 — lazydocker 업데이트 및 0-4 완료

- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`. 사용자가 직접 다운로드·교체하고 출력 및 화면을 제공했다. Codex가 Ubuntu 설치를 대신 수행한 것은 아니다.
- 최초 다운로드는 약 4.8MB 중 32KB 수신 후 속도가 낮아졌다. Ctrl+C 후 `curl -fL --connect-timeout 15 --max-time 120 -o "$lab_tmp/lazydocker.tar.gz" https://github.com/jesseduffield/lazydocker/releases/download/v0.25.2/lazydocker_0.25.2_Linux_x86_64.tar.gz`로 재시도하도록 안내했다. 사용자 출력은 `100 4818k`, 평균 약 10.2MB/s로 다운로드 완료였다.
- `tar -xzf "$lab_tmp/lazydocker.tar.gz" -C "$lab_tmp" lazydocker && "$lab_tmp/lazydocker" --version`으로 임시 바이너리 실행 확인.
- `sudo install -m 0755 "$lab_tmp/lazydocker" /usr/local/bin/lazydocker && hash -r && lazydocker --version` 실행 후 Version 0.25.2, BuildSource binaryRelease, OS linux, Arch amd64, Commit `7e7aadc2071d58031bf2daafca1fbd4093efc23f` 출력. 임시 폴더 정리는 아직 확인하지 않았다.
- 재실행 후 사용자 첨부 `버전교체 후.png`에서 API 오류 창이 사라졌고 오른쪽 아래 버전 0.25.2를 확인했다. Images에 agent / 0.1.0 / 189.09MB와 실습 이미지들이 보인다.
- Networks에서 bridge(드라이버 bridge), host(드라이버 host), none(드라이버 null)을 확인했다. 추가로 기존 다른 프로젝트의 네트워크·볼륨·종료된 컨테이너가 표시됐다. 이 리소스는 이번 실습 대상이 아니며 삭제·변경하지 않았다.
- 이미지와 기본 네트워크의 시각적 확인으로 0-4 완료. 화면의 Images 단축키는 4, Networks는 6으로 기존 가이드 예시와 다르다. 종료 키 q는 화면 하단에서 확인했으며 종료는 아직 사용자 실행 결과를 받지 않았다.
- [업데이트 출력 및 화면 판독 기록](evidence/day00-04-user-result-2026-09-23.txt)을 저장했다. Windows의 PROGRESS.md·환경 기록을 갱신했으며 bootstrap.sh와 가이드 원문은 수정하지 않았다.

## 2026-09-23 — 0-5 디렉터리 확인 및 Day 0 실습 완료

- 실행 위치: Ubuntu WSL2 `/home/user/onprem-lab`. 사용자가 `ls -la ~/onprem-lab/` 출력 제공.
- agent, bootstrap.sh, day01~day13, skeleton이 모두 존재한다. bootstrap.sh는 사용자 출력에서 `-rwxr-xr-x`, 5903바이트다. 오류 없이 셸 프롬프트로 복귀했다.
- 가이드 0-5 예시에는 day14가 있지만 bootstrap.sh의 make_dirs는 day01~day13까지 생성한다. Day 14 원문의 시작 경로도 `~/onprem-lab/skeleton`이므로 이번 폴더 확인은 통과로 판단했다. day14 폴더를 새로 만들지는 않았다.
- 이번 확인은 최상위 폴더 목록 확인이며 모든 내부 파일의 무결성이나 Windows 복사본과의 동기화를 확인한 것은 아니다.
- [사용자 제공 목록](evidence/day00-05-user-output-2026-09-23.txt)을 저장했다.

### Day 0 실습 체크리스트 판정
- [x] bootstrap.sh check 전 항목 ✓ — Docker Desktop 실행 후 Codex 직접 확인. lazydocker 교체 후 check 전체를 다시 돌린 것은 아니며 교체 버전·TUI는 사용자 제공 결과로 확인.
- [x] agent:0.1.0 빌드 및 /healthz 응답 — 사용자 제공 빌드·API 출력 확인.
- [x] lazydocker 이미지 목록 — 사용자 스크린샷에서 agent:0.1.0 및 기본 네트워크 확인.

### 남은 차이 및 인수인계
- kubectl 1.36.1 대 가이드 1.31.0, dive 0.13.1 대 본문 0.12.0, Compose 5.5.1 대 v2 표기는 남아 있다. 이후 Kubernetes 등 실습 호환성을 완료로 단정하지 않는다.
- lazydocker는 실제 0.25.2지만 bootstrap.sh·가이드에는 0.23.3이 남아 있다. 이번에는 실제 설치만 교체했으며 소스 고정값은 수정하지 않았다.
- Windows 저장소와 Ubuntu 실습 폴더는 별도 복사본이다. 이번 기록은 Windows에만 반영했다. 학습용 이미지와 소스는 유지한다.
- Day 0 개념 자기점검 4문항의 사용자 답변 평가는 아직 하지 않았다. 현재 0-5 오류나 별도 질문은 없다.

## 2026-09-23 — 세션 회고 및 기록 정리

사용자 요청으로 기존 날짜별 실행 기록을 보존하면서 실습 결과 요약, 오류·해결 표, 재진단 순서, 핵심 Lessons와 후속 질문의 답을 보강했다. Docker Desktop에서의 이미지 확인과 학습용 에이전트의 역할을 추가했다. 이 정리는 Windows 프로젝트의 기록 파일 수정이며 실습 재실행·새 설치·Ubuntu 파일 동기화는 수행하지 않았다.

## 2026-09-23 — 세션 종료 및 PR 제출 준비

- 사용자 요청으로 Day 0 세션을 종료하고 기록을 GitHub PR로 제출한다. 실습 범위는 0-1~0-5 완료이며 Day 1은 미진행이다.
- 제출 브랜치: `codex/day00-completion`, 대상: `main`, 저장소: `shanis345/Deploy_Practice`.
- 제출 범위: PROGRESS.md, 이 SESSION.md, docs/environment.md, evidence의 직접 재점검 1개 및 사용자 실습 결과 4개. 소스·가이드·bootstrap.sh·원본 ZIP은 변경하지 않았다.
- 문서의 실행 증거 기준과 미검증 항목을 확인했다. 문서 정리 중 실습 명령을 재실행하지 않았다. GitHub 병합과 Ubuntu 사본 동기화는 이번 종료 작업 범위에 포함하지 않는다.

## 다음에 이어 할 지점
**Day 0 실습 완료.** 다음 시작 후보는 Day 1이며 사용자 요청 전까지 진행하지 않는다. 시작 시 이 기록과 docs/environment.md의 환경 차이를 읽는다.
