# Day 3 — Docker 이미지·레이어·컨테이너, 그리고 심의를 통과하는 이미지

## 진행 상태
- 상태: Day 3 완료(사용자 완료 확인). 별도 자기점검 문답 평가는 기록 없음
- 완료한 범위: 3-1 이미지 관찰, 3-2 보안 설정 확인, 3-3 취약점 개선·재검사, 3-4 레이어 잔존 관찰·정리, 3-5 반입 패키지 초안 작성
- 중단 지점: 실습·관찰·정리와 결과 요약 완료. 다음 Day는 사용자 요청 시 진행
- Codex 작업: 아직 별도 작업을 만들지 않음
- 실행 증거 기준: 사용자 제공 출력과 직접 검증 결과를 구분해 기록

## 목표와 이번 세션 범위
2026-09-27 사용자 요청으로 3-1~3-4를 완료했다. 이후 다음 단계 요청에 따라 3-5 반입 패키지 초안을 진행한다. 실습 증거를 재사용하되 새 이미지 정보와 미검증 항목을 구분한다. 실제 고객사 제출·승인이나 다음 Day 진행은 이번 범위에 포함하지 않는다.

## 실행 기록
### 2026-09-27 — 3-1 시작: 이미지 조회 안내
- Codex는 Windows의 진행·환경 기록, Day 3 README·SESSION·가이드와 agent/Dockerfile을 읽었다. Dockerfile 기본 베이스는 python:3.12.7-slim이다. Ubuntu 사본과 현재 엔진 상태는 직접 검증하지 않았다.
- 사용자 실행 위치: Ubuntu WSL2의 ~/onprem-lab/agent. Windows에서 Docker Desktop을 먼저 실행하도록 안내한다.
- 아래 명령은 안내만 했으며 사용자 출력 대기 중이다. 오류가 나면 해당 출력부터 확인한다.

```bash
cd ~/onprem-lab/agent
docker version
docker history agent:0.1.0 | head -12
docker image inspect agent:0.1.0 --format 'User={{.Config.User}} Exposed={{json .Config.ExposedPorts}} Layers={{len .RootFS.Layers}}'
docker image inspect python:3.12.7-slim --format '{{json .RepoDigests}}'
```

- 가이드의 RepoDigests 첫 항목 조회 대신 전체 목록을 JSON으로 조회해 비어 있는 경우도 확인한다. 이는 python 베이스 이미지의 레지스트리 다이제스트이며 agent 자체의 다이제스트와 구분한다.
- 설치·빌드·컨테이너 실행·삭제는 수행하지 않았다. dive 관찰과 3-1 완료 판정은 아직 하지 않았다.

## 오류와 해결
### 2026-09-27 — Docker WSL 연동 오류
- 확인 주체: 사용자 제공 Ubuntu 출력. 프롬프트는 ~/onprem-lab/agent로 이동했다.
- docker version·history·image inspect 두 개 모두 다음 안내를 출력했다: `The command 'docker' could not be found in this WSL 2 distro.` 및 WSL integration 활성화 권고.
- 현재 Ubuntu에서 Docker CLI 연동을 사용할 수 없음을 확인했다. Desktop 미실행·기동 중·연동 설정 문제 중 어느 원인인지는 아직 확정하지 않았다. 이미지 존재 여부·레이어·설정·다이제스트는 확인하지 못했다.
- 안내: Windows에서 Docker Desktop 실행·엔진 기동을 기다린 뒤 Ubuntu에서 docker version만 재실행한다. 같은 오류가 지속되면 Settings > Resources > WSL Integration에서 Ubuntu 활성화 및 Apply 후 재확인한다.
- 근거: [Docker 공식 WSL 문서](https://docs.docker.com/desktop/features/wsl/). 기존 환경에서도 Desktop 실행 후 복구된 이력이 있다.
- 재확인 결과: 후속 사용자 출력으로 Client·Server 정상 응답과 이미지 조회 성공을 확인했다(아래 기록). 사용자가 Windows에서 수행한 조작 상세는 미제공이므로 정확한 최초 원인은 확정하지 않는다. Codex가 설치·설정 변경·Ubuntu 명령 실행을 수행하지 않았다.

### 2026-09-27 — Docker 연결 복구·3-1 이미지 조회 성공
- 확인 주체: 사용자 제공 Ubuntu 출력. 위치는 ~/onprem-lab/agent.
- docker version: Client/Engine 29.8.0, API 1.56(서버 최소 1.40), Docker Desktop 4.92.0 (240144), linux/amd64, Context default. containerd v2.3.5, runc 1.5.1, docker-init 0.19.0.
- docker history의 최상단 이미지 표시: ff0088b950ca. CMD·HEALTHCHECK·EXPOSE·USER·ENV는 0B, COPY app.py는 20.5kB, COPY 의존성은 3.1MB, WORKDIR /app은 4.1kB, 사용자 생성 등의 RUN은 65.5kB였다. head -12 출력이므로 전체 이력을 조회한 것은 아니다.

```text
User=10001 Exposed={"8000/tcp":{}} Layers=8
["python@sha256:60d9996b6a8a3689d36db740b49f4327be3be09a21122bd02fb8895abb38b50d"]
```

- 결과 의미: agent:0.1.0 이미지의 기본 실행 사용자 설정은 UID 10001, 선언 포트는 8000/tcp, 파일시스템 레이어는 8개다. 컨테이너의 실제 실행 사용자나 호스트 포트 공개를 검증한 것은 아니다. history에는 설정 이력도 포함돼 행 수가 파일시스템 레이어 수와 같지 않다.
- RepoDigests 출력은 로컬 python:3.12.7-slim 이미지에 기록된 레지스트리 다이제스트다. agent 자체의 다이제스트가 아니며 이 조회만으로 agent의 빌드 출처까지 입증하지 않는다.
- 다음 안내(실행 결과 대기): Ubuntu에서 `dive --version`, 이어 `dive agent:0.1.0`. COPY app.py와 의존성 COPY 레이어의 파일 변경을 관찰한다. 정상 진입 여부와 화면 또는 관찰 결과를 받아 3-1 완료 여부를 판단한다.

## 배운 내용과 질문
### 2026-09-27 — dive 화면 확인과 실행한 작업의 의미
- 확인 주체: 사용자 제공 스크린샷 `스크린샷 2026-09-27 170240.png`. 이미지는 프로젝트 밖에 있으며 증거 폴더로 복사하지 않았다.
- 화면의 Image name은 agent:0.1.0이다. 레이어 목록 8개와 선택된 첫 행 `FROM blobs`(75 MB), Layer Details의 Debian bookworm 생성 명령 및 오른쪽 /etc 등의 파일 트리를 확인했다.
- dive 화면 표시: Total Image size 126 MB, Potential wasted space 4.8 MB, Image efficiency score 97%. 이 값은 도구 화면의 관찰값이며 다른 도구의 이미지 크기와 차이가 나는 원인은 검증하지 않았다. dive 버전 출력은 미제공이다.
- 사용자 질문: “우리가 구체적으로 뭘 실행한거지?” Docker 연결 조회 → 기존 이미지의 생성 이력·설정 조회 → dive로 기존 이미지의 파일시스템 레이어 분석 순서임을 설명한다. 화면의 RUN·COPY는 과거 빌드 작업의 이력으로, 지금 다시 실행하는 명령이 아니다. 이번에 agent 앱을 실행하거나 새 이미지를 빌드한 것은 아니다.
- 현재 선택한 것은 베이스 OS 파일 레이어다. Python 베이스 이미지에 포함된 Debian 사용자 공간 파일이며, 별도 VM 또는 커널을 실행한 화면이 아니다.
- 다음 관찰: 왼쪽 마지막 COPY app.py 행을 선택해 /app/app.py를 확인하고, COPY /build/deps 행에서 의존성 파일을 확인한다. 현재 스크린샷만으로 두 행을 선택·관찰했다고 판정하지 않는다.

### 2026-09-27 — 의존성 레이어 관찰 확인
- 확인 주체: 사용자 제공 `package확인.png` 스크린샷. 프로젝트 밖의 원본은 복사하지 않았다.
- 선택 행은 `COPY /build/deps /app/deps # buildkit`이며 크기는 dive 표시 기준 3.0 MB다. 오른쪽 /app/deps에 녹색으로 PyYAML-6.0.2.dist-info, _yaml, yaml 및 관련 파일이 보인다. 의존성 복사 레이어의 패키지 파일 관찰 성공으로 기록한다.
- UID:GID의 0:0은 표시된 파일 소유권이며 앱 실행 사용자가 root라는 뜻이 아니다. 앞서 이미지 설정 User=10001을 별도로 확인했다.
- COPY app.py 레이어 관찰은 아직 확인하지 않았다. 다음은 왼쪽 목록에서 아래 한 칸의 COPY app.py를 선택해 /app/app.py 추가를 확인한다.

### 2026-09-27 — 앱 코드 관찰 확인·3-1 완료, 3-2 첫 단계 안내
- 사용자가 COPY app.py의 /app/app.py 추가 관찰 안내에 “확인되었어”라고 응답했다. 앱 코드 관찰의 근거는 사용자 확인이며 별도 스크린샷이나 Codex 직접 조회가 아니다.
- 기존 텍스트 출력과 베이스·의존성 스크린샷, 이번 앱 코드 확인을 합쳐 3-1 완료로 기록한다. Day 3 전체 완료는 아니다.
- 사용자가 다음 단계를 요청해 Ctrl+C로 dive 종료 후 Ubuntu에서 `docker run --rm agent:0.1.0 id`를 실행하도록 안내한다. 기존 이미지로 임시 컨테이너를 생성해 기본 CMD 대신 id를 실행하고 종료 시 컨테이너를 자동 제거하는 명령이다. 이미지는 유지한다.
- 예상 출력은 `uid=10001(appuser) gid=0(root) groups=0(root)`이다. UID와 GID를 구분해 해석하며 실제 출력은 아직 받지 않았다. Codex가 명령을 대신 실행하지 않았다.

### 2026-09-27 — 3-2 실행 사용자 확인 성공
- 확인 주체: 사용자 제공 Ubuntu 출력. 위치는 ~/onprem-lab/agent.
- 실행 명령: `docker run --rm agent:0.1.0 id`.
- 실제 출력: `uid=10001(appuser) gid=0(root) groups=0(root)`이며 프롬프트로 돌아왔다.
- 결과 의미: 해당 컨테이너의 id 프로세스는 UID 10001로 실행됐다. GID 0 소속과 root 사용자(UID 0)를 구분한다. 앱 기능 실행이나 보안 요건 전체를 검증한 것은 아니다.
- 다음 안내(결과 대기): `docker run --rm agent:0.1.0 sh -c 'touch /etc/test; rc=$?; echo "종료코드=$rc"; exit "$rc"'`. 가이드의 touch 후 echo에 종료 코드 보존을 추가해 컨테이너 종료 상태에도 쓰기 시도 결과를 반영한다. 예상은 Permission denied와 종료코드=1이다.
- 명령은 새 임시 컨테이너 내부의 /etc/test에 쓰기를 시도하고 종료 시 컨테이너를 자동 제거한다. 호스트 경로 마운트는 없다. 아직 사용자 실행 결과를 받지 않았고 Codex가 대신 실행하지 않았다.

### 2026-09-27 — 3-2 시스템 디렉터리 쓰기 거부 확인
- 확인 주체: 사용자 제공 Ubuntu 출력. 위치는 ~/onprem-lab/agent.
- 안내한 /etc/test 생성 명령의 실제 출력은 `touch: cannot touch '/etc/test': Permission denied` 및 `종료코드=1`이다. 예상된 권한 제한 관찰에 성공했다. 복구가 필요한 오류로 처리하지 않는다.
- 다음 안내(사용자 실행 결과 대기):

```bash
docker run --rm --read-only agent:0.1.0 sh -c 'touch /app/x; rc=$?; echo "종료코드=$rc"; exit "$rc"'
docker run --rm --read-only --tmpfs /app/tmp agent:0.1.0 sh -c 'touch /app/tmp/x && echo "tmpfs 쓰기 OK"'
```

- 첫 명령은 읽기 전용 루트에서 Read-only file system·종료코드 1, 두 번째는 별도 tmpfs 쓰기 성공을 예상한다. 각각 별도의 임시 컨테이너에서 실행하고 종료 시 제거한다. Codex는 직접 실행하지 않았다.

### 2026-09-27 — 3-2 읽기 전용 루트·tmpfs 비교 성공
- 확인 주체: 사용자 제공 Ubuntu 출력. 위치는 ~/onprem-lab/agent.
- 첫 명령은 `touch: cannot touch '/app/x': Read-only file system`과 `종료코드=1`을 출력했다. 읽기 전용 루트에서의 쓰기 거부를 확인했다.
- 첫 tmpfs 명령 입력에는 ^C가 있고 성공 출력이 없다. 이 시도를 성공으로 기록하지 않는다. 같은 명령을 다시 실행한 출력은 `tmpfs 쓰기 OK`이며 프롬프트로 돌아왔다.
- 결과: --read-only 상태에서도 별도 --tmpfs /app/tmp 마운트에 파일을 쓸 수 있었다. 앱 서버를 실행한 것은 아니므로 이 결과만으로 전체 앱이 읽기 전용 환경에서 정상 동작한다고 판정하지 않는다.
- 다음 안내(결과 대기): `docker image inspect agent:0.1.0 --format '{{json .Config.Healthcheck.Test}}'`. 이미지에 정의된 헬스체크 명령을 조회한다. 예상은 CMD-SHELL과 Python urllib.request를 사용한 http://127.0.0.1:8000/healthz 요청이다. 실제 헬스체크 실행 성공 여부와는 구분한다.

### 2026-09-27 — 헬스체크 설정 확인·3-2 완료
- 확인 주체: 사용자 제공 Ubuntu 출력. 실행 명령은 `docker image inspect agent:0.1.0 --format '{{json .Config.Healthcheck.Test}}'`.
- 사용자 메시지에서 CMD-SHELL, Python urllib.request.urlopen 및 http://127.0.0.1:8000/healthz를 확인했다. 메시지에는 URL 링크화와 따옴표 이스케이프 변형이 있어 원시 JSON 바이트와 동일한 출력으로 보존하지 않는다. 명령 실행 오류는 제시되지 않았다.
- 의미: 컨테이너 내부의 로컬 HTTP /healthz 요청을 사용하는 헬스체크 명령이 이미지에 정의돼 있다. 이번에는 설정 조회만 했으며 실제 헬스체크 실행·healthy 상태·업무 기능을 검증한 것은 아니다.
- 앞선 UID 10001 실행, /etc 쓰기 거부, 읽기 전용 루트 쓰기 거부 및 tmpfs 쓰기 성공과 합쳐 가이드 3-2 항목 완료로 판정한다. Day 3 전체 완료 또는 보안 심의 통과를 뜻하지 않는다.
- 3-3 취약점 스캔은 시작하지 않았으며 스캔·다운로드·이미지 빌드를 수행하지 않았다.

### 2026-09-27 — OS 실행 권한과 앱 사용자 권한 구분
- 사용자 질문에 UID 10001은 앱 프로세스의 Linux 사용자이며 UID 0(root)과 구분된다고 설명했다. GID 0은 그룹 권한이며 root 사용자와 동일하지 않다.
- non-root는 앱 오류·침해 시 가능한 작업 범위를 줄이는 최소 권한 설정이다. 앱 로그인 사용자별 인증·인가와는 다른 계층이며 이번 실습에서 사용자별 역할·접근 제어를 구현하거나 시험한 것은 아니다.

### 2026-09-27 — 3-3 초기 취약점 스캔 안내
- 사용자 후속 요청으로 가이드 3-3과 Windows의 scan.sh를 확인했다. 가이드 고정 Trivy 이미지 aquasec/trivy:0.56.2를 사용하며 최신 버전이라고 표현하지 않는다. Ubuntu scan.sh의 동기화 여부를 가정하지 않고 명령을 직접 안내한다.
- 실행 위치: 사용자 Ubuntu WSL2 ~/onprem-lab/day03. 아래는 안내만 했고 결과 대기 중이다.

```bash
mkdir -p ~/onprem-lab/day03 && cd ~/onprem-lab/day03
mkdir -p trivy-cache
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$PWD/trivy-cache:/root/.cache/" \
  aquasec/trivy:0.56.2 image --severity HIGH,CRITICAL --scanners vuln agent:0.1.0 2>&1 | tee trivy-agent-0.1.0.log
echo "스캔 종료코드=${PIPESTATUS[0]}"
```

- 가이드의 tail -40 대신 tee로 전체 출력·오류를 화면과 Ubuntu 로그에 보존하고 Bash PIPESTATUS[0]으로 docker run 종료코드를 바로 확인한다. 해당 로그·캐시는 Windows에 자동 동기화되지 않는다.
- Trivy 컨테이너가 Docker 소켓으로 이미지에 접근하고 캐시에 취약점 DB를 저장한다. 필요하면 Trivy 이미지와 DB가 다운로드된다. 스캔 대상 agent 앱을 실행하거나 이미지를 갱신하는 단계는 아니다.
- HIGH·CRITICAL 결과만 표시한다. 종료코드 0은 취약점 0건과 같지 않으며 별도 --exit-code 기준은 설정하지 않았다. 결과의 실제 Total·패키지·수정 버전을 보고 다음 대응을 결정한다. 가이드 예시 건수는 현재 스캔 결과로 간주하지 않는다.
- 참고: [Trivy v0.56 심각도 필터](https://trivy.dev/v0.56/docs/configuration/filtering/). Codex가 Ubuntu 명령·스캔·다운로드·빌드를 직접 실행하지 않았다.

### 2026-09-27 — 3-3 초기 스캔 성공·결과 해석
- 확인 주체: 사용자 첨부 텍스트. 주요 발췌는 [스캔 증거](evidence/trivy-agent-0.1.0-user-2026-09-27.txt)에 보존한다.
- Trivy DB 117.74 MiB 다운로드 성공 후 Debian 12.8·OS 패키지 105개를 탐지했다. Debian 대상 결과는 Total 104(HIGH 95, CRITICAL 9), 스캔 종료코드 0이다. Python 패키지 탐지 로그도 있으나 별도 결과 요약은 없다.
- 일부 취약점에 다른 공급자의 심각도 평가를 사용한다는 WARN은 있지만 스캔은 정상 종료했다. 종료코드 0은 취약점 없음이나 보안 심의 통과를 뜻하지 않는다. 104는 보고서의 패키지별 검출 건수이며 고유 CVE 수 또는 실제 악용 가능 건수로 단정하지 않는다.
- 보고서에는 libcap2·libssl3 등의 fixed 항목과 perl-base의 affected, zlib1g의 will_not_fix가 함께 있다. non-root 검증과 패키지 취약점 검사는 별개의 항목이다. 가이드 예시와 수치는 같지만 이번 판정은 사용자 실제 출력에 근거한다.
- 다음은 베이스 이미지 변경 후 agent:0.2.0 재빌드·재스캔이다. Windows Dockerfile에는 ARG BASE와 두 FROM 사용이 있으나 Ubuntu와 자동 동기화되지 않으므로 사용자에게 `cd ~/onprem-lab/agent && cat Dockerfile`을 먼저 안내한다. Ubuntu 파일 내용 확인 결과는 대기 중이다.
- 가이드 지정 python:3.12.14-slim 태그의 Docker Hub API를 웹 도구로 조회하려 했으나 접근 불가였다. 현재 사용 가능 여부는 검증하지 못했으며 최신 버전이라고 단정하지 않는다. 실제 재빌드 단계에서 확인한다.
- Codex가 스캔·다운로드·빌드를 직접 실행하거나 Ubuntu 소스를 변경하지 않았다. 3-3 전체는 아직 미완료다.

### 2026-09-27 — Trivy의 국내 기업 실무 활용 질문
- 사용자 질문: 국내 대기업 위주로 Trivy가 실제 업계에서 쓰이는 도구인지.
- 공식 공개 자료로 카카오클라우드 Container Registry의 Trivy 기반 이미지 취약점 자동 스캔 제공을 확인했다. 이는 국내 상용 서비스 적용 근거이며 카카오 모든 조직 또는 국내 대기업 전체의 사내 표준이라는 뜻은 아니다. [카카오클라우드](https://kakaocloud.com/services/container-registry/intro).
- GitLab 공식 문서는 컨테이너 취약점 분석에 Trivy를 통합한다고 명시한다. Harbor 공식 2.0 발표도 기본 이미지 스캐너를 Trivy로 전환했다고 설명한다. 이 자료는 제품 통합 근거이며 특정 국내 기업의 도입 증거로 확대 해석하지 않는다. [GitLab](https://docs.gitlab.com/user/application_security/container_scanning/), [Harbor 2.0](https://goharbor.io/blog/harbor-2.0/).
- 삼성·LG·SK 등 각 대기업의 현재 전사 표준 도구·채택률은 이번 공개자료 조사로 확인하지 못했다. 실무에서는 고객사 지정 스캐너와 반입 판정 기준을 먼저 확인하고, 자체 사전 검사 결과와 고객사 최종 승인을 구분하도록 설명한다.
- 추가 실습 실행 없음. 다음 시작 지점은 여전히 Ubuntu Dockerfile 확인 후 재빌드·재스캔이다.

### 2026-09-27 — Ubuntu Dockerfile 확인·베이스 변경 빌드 안내
- 확인 주체: 사용자 제공 `cd ~/onprem-lab/agent && cat Dockerfile` 출력. ARG BASE=python:3.12.7-slim, 빌드·실행 단계의 FROM ${BASE}, APP_VERSION 빌드 인자와 ENV 전달, USER 10001 등을 확인했다. 메시지의 Markdown 이스케이프·링크 변형은 파일 바이트가 손상됐다는 근거로 해석하지 않는다. Windows 사본과 바이트 단위 일치까지 검증한 것은 아니다.
- 가이드 지정 python:3.12.14-slim으로 BASE를 덮어써 agent:0.2.0을 빌드하도록 안내한다. 최신 태그라고 단정하지 않으며 레지스트리 사용 가능 여부는 실제 빌드 결과로 확인한다.
- 실행 위치: 사용자 Ubuntu WSL2 ~/onprem-lab/agent. 아래 명령은 안내만 했으며 실행 결과 대기 중이다.

```bash
docker build --build-arg BASE=python:3.12.14-slim --build-arg APP_VERSION=0.2.0 -t agent:0.2.0 .
```

- 빌드가 성공한 경우에만 다음 명령을 실행하도록 안내한다.

```bash
docker run --rm agent:0.2.0 python --version
```

- BASE는 두 FROM에 적용되고 APP_VERSION은 앱 버전 환경변수에 전달된다. -t는 새 이미지 태그, 마지막 점은 현재 폴더를 빌드 컨텍스트로 지정한다. Dockerfile과 앱 소스는 수정하지 않으며 기존 agent:0.1.0 태그도 유지한다.
- 예상 Python 버전은 3.12.14다. 빌드 성공만으로 취약점 해소를 판정하지 않으며 이후 같은 DB 캐시로 재스캔할 예정이다. Codex는 빌드·다운로드·컨테이너 실행을 대신 수행하지 않았다.

### 2026-09-27 — agent:0.2.0 빌드 성공·재스캔 안내
- 확인 주체: 사용자 첨부 빌드 출력. [주요 증거](evidence/build-agent-0.2.0-user-2026-09-27.txt).
- 빌드 인자 BASE=python:3.12.14-slim, APP_VERSION=0.2.0으로 14/14 FINISHED(10.4초), agent:0.2.0 이름 지정·unpacking 성공을 확인했다. 베이스 메타데이터 조회와 레이어 다운로드도 성공해 해당 태그의 실제 사용 가능 여부를 확인했다.
- 후속 `docker run --rm agent:0.2.0 python --version` 출력은 Python 3.12.14다. 앱 서버 기동이나 기능 검증은 수행한 것이 아니다. 이미지의 취약점 감소 여부는 아직 확인하지 않았다.
- 다음 안내: 사용자 Ubuntu ~/onprem-lab/day03에서 아래 재스캔을 수행한다. --skip-db-update로 앞서 다운로드한 캐시 DB를 사용한다. DB 캐시가 다른 작업으로 갱신되지 않았다는 전제에서 초기 스캔과 비교한다.

```bash
cd ~/onprem-lab/day03
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$PWD/trivy-cache:/root/.cache/" \
  aquasec/trivy:0.56.2 image --severity HIGH,CRITICAL --scanners vuln --skip-db-update agent:0.2.0 2>&1 | tee trivy-agent-0.2.0.log
echo "스캔 종료코드=${PIPESTATUS[0]}"
```

- 재스캔 명령은 안내만 했으며 결과 대기 중이다. 초기 비교 기준은 Debian 12.8의 HIGH 95·CRITICAL 9다. 새 OS·실제 건수는 사용자 출력으로 확인한다. 패치 미제공 항목 제외 검사는 이후에 안내한다.

### 2026-09-27 — agent:0.2.0 재스캔 성공
- 확인 주체: 사용자 첨부 출력. [주요 증거](evidence/trivy-agent-0.2.0-user-2026-09-27.txt).
- --skip-db-update를 사용한 재스캔이 종료코드 0으로 완료됐다. Debian 13.7·OS 패키지 87개, Debian 대상 Total 44(HIGH 44, CRITICAL 0)를 확인했다. PyYAML 6.0.2·pip 25.0.1 탐지 로그와 심각도 출처 관련 WARN이 있다.
- 초기 Debian 12.8·패키지 105개·HIGH 95·CRITICAL 9와 비교해 HIGH 51건 및 CRITICAL 9건이 감소했다. Python 패치 버전뿐 아니라 기반 Debian과 패키지 구성이 바뀐 결과다. 각 항목이 패치로 해소됐는지 패키지 제거 등으로 미검출됐는지는 개별 대조하지 않았다.
- 남은 표에는 affected·fix_deferred와 Fixed Version 빈칸이 보인다. 다음은 수정 버전 미제공 항목을 제외하는 필터로 확인하며, 필터 후 0건이어도 기존 HIGH 44건의 위험이 해소되는 것은 아니다.
- 다음 안내(사용자 Ubuntu ~/onprem-lab/day03, 실행 결과 대기):

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$PWD/trivy-cache:/root/.cache/" \
  aquasec/trivy:0.56.2 image --severity HIGH,CRITICAL --scanners vuln --skip-db-update --ignore-unfixed agent:0.2.0 2>&1 | tee trivy-agent-0.2.0-fixed.log
echo "스캔 종료코드=${PIPESTATUS[0]}"
```

- 원래 필터 없는 HIGH·CRITICAL 리포트를 유지하며 별도 로그에 저장한다. 아직 필터 검사 결과를 받지 않았으며 보안 예외 승인·반입 승인·3-3 전체 완료로 판정하지 않는다.

### 2026-09-27 — 수정 가능 항목 필터 확인·3-3 완료
- 확인 주체: 사용자 제공 Ubuntu 출력. [필터 검사 증거](evidence/trivy-agent-0.2.0-fixed-user-2026-09-27.txt).
- agent:0.2.0(Debian 13.7)에서 --skip-db-update --ignore-unfixed 결과 Total 0(HIGH 0, CRITICAL 0), 종료코드 0을 확인했다. 심각도 공급자 관련 WARN은 표시됐지만 검사는 완료됐다.
- 초기 0.1.0은 HIGH 95·CRITICAL 9, 베이스 변경 후 0.2.0은 HIGH 44·CRITICAL 0, 수정 버전 미제공 항목 제외 시 0건이다. 이번 DB·스캔 범위에서 잔여 HIGH 44건은 해당 필터로 제외되는 항목이다. 제거·해결되거나 실제 영향이 없다는 뜻은 아니다.
- 실무 대응 원칙: 미필터 리포트를 함께 보존하고 실제 사용 경로·권한·영향·완화 조치를 검토한 뒤 필요하면 고객사 예외 승인을 요청한다. 도구의 수정 버전 정보는 시점·데이터 범위에 한정되며 패치 발표 후 갱신·재검사를 수행한다. 앱이 해당 기능을 사용하지 않는다는 근거는 이번 실습에서 검증하지 않았다.
- 초기 스캔, 가이드 지정 베이스로 새 이미지 빌드, 재스캔·필터 비교·잔여 항목 대응 원칙 정리까지 확인해 3-3 실습 완료로 기록한다. 고객사 기준 통과·예외 승인·전체 취약점 0건으로 기록하지 않는다.
- 3-4·3-5와 Day 3 전체 마무리는 미진행이다. Codex가 사용자 Ubuntu 환경을 직접 수정하거나 스캔을 재실행하지 않았다.

### 2026-09-27 — 기업 반입 사전 점검과 3-2 범위 복습
- 사용자 질문에 3-1은 이미지 구성 관찰, 3-2는 OS 실행 권한·쓰기 제한·헬스체크 정의 확인, 3-3은 패키지 취약점 검사·개선·재검사라고 설명했다. 실제 고객사 심의나 배포를 수행한 것은 아니다.
- 3-2의 파일 쓰기 관찰만으로 읽기 전용 환경에서 앱 전체가 정상 동작한다고 판정하지 않으며, 헬스체크 정의와 실제 성공도 구분했다.

### 2026-09-27 — 3-4 연습 이미지 준비·빌드 안내
- 사용자 요청으로 가이드 3-4를 확인했다. agent 이미지와 별개로 leak:1을 만들어 파일 삭제와 레이어 잔존을 비교한다.
- 실행 위치: 사용자 Ubuntu WSL2 ~/onprem-lab/day03/leak. 아래 명령은 안내만 했고 결과 대기 중이다. 실제 자격 증명 대신 DEMO_ONLY 문자열을 사용한다.

```bash
mkdir -p ~/onprem-lab/day03/leak && cd ~/onprem-lab/day03/leak
echo 'DEMO_ONLY_FILE_SECRET' > secret.txt
cat > Dockerfile <<'EOF'
FROM alpine:3.20
ENV API_KEY=DEMO_ONLY_ENV_SECRET
COPY secret.txt /root/secret.txt
RUN rm /root/secret.txt
EOF
docker build -t leak:1 .
```

- 생성·빌드 과정은 사용자가 Ubuntu에서 수행한다. Windows agent/Dockerfile 등 기존 실습 소스는 변경하지 않았다. mkdir 또는 cd 실패 시 후속 명령을 진행하지 않도록 안내한다.
- COPY로 넣은 파일과 RUN rm의 삭제가 서로 다른 레이어에 기록되는 구성을 만든다. ENV의 메타데이터 잔존과 파일 레이어 잔존은 빌드 후 별도로 확인할 예정이며 아직 확인하지 않았다.
- 다음은 빌드 결과 확인 후 컨테이너의 최종 파일 목록·이미지 ENV 조회, 이어 docker save로 레이어 내용을 관찰하는 것이다. 이미지 내보내기·파일 추출·정리 명령은 아직 안내·실행하지 않았다.

### 2026-09-27 — leak:1 빌드 성공·ENV 경고 확인
- 확인 주체: 사용자 제공 Ubuntu 출력. 위치는 ~/onprem-lab/day03/leak.
- docker build -t leak:1 . 결과 8/8 FINISHED(0.8초), COPY secret.txt와 RUN rm 실행 및 leak:1 이름 지정·unpacking 성공을 확인했다. 베이스는 alpine:3.20, 출력된 다이제스트는 sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc다.
- 경고 1개: `SecretsUsedInArgOrEnv: Do not use ARG or ENV instructions for sensitive data (ENV "API_KEY") (line 2)`. Docker 공식 문서상 민감한 값을 암시하는 ENV·ARG 키를 지적하는 검사다. 실제 유효한 API 키를 탐지했다는 뜻은 아니며 이번 값은 DEMO_ONLY_ENV_SECRET이다. [공식 설명](https://docs.docker.com/reference/build-checks/secrets-used-in-arg-or-env/).
- 다음 안내(아직 실행 결과 없음):

```bash
docker run --rm leak:1 ls -la /root/
docker image inspect leak:1 --format '{{json .Config.Env}}'
```

- 첫 명령은 컨테이너의 최종 /root 목록에서 secret.txt가 없는지 확인하고, 두 번째는 이미지 설정에 API_KEY=DEMO_ONLY_ENV_SECRET이 남는지 확인한다. 파일 레이어에서 원문 추출은 이후 단계이며 아직 수행하지 않았다. Codex는 Ubuntu 명령을 직접 실행하지 않았다.

### 2026-09-27 — 최종 파일 부재·이미지 ENV 잔존 확인
- 확인 주체: 사용자 제공 Ubuntu 출력. 위치는 ~/onprem-lab/day03/leak.
- `docker run --rm leak:1 ls -la /root/` 출력에 .과 ..만 있고 secret.txt는 없다. `docker image inspect leak:1 --format '{{json .Config.Env}}'`에는 PATH와 API_KEY=DEMO_ONLY_ENV_SECRET이 표시됐다.
- 결과: 최종 파일시스템에서 파일 삭제를 확인했고, 가짜 ENV 값은 이미지 설정에서 직접 읽을 수 있다. 삭제 파일의 과거 레이어 잔존은 아직 관찰하지 않았다.
- 다음 안내(사용자 실행 결과 대기): 현재 Ubuntu 실습 폴더에서 내보내기·압축 해제를 성공한 뒤 루프를 실행한다.

```bash
docker save leak:1 -o leak.tar && mkdir -p x && tar -xf leak.tar -C x
```

```bash
for blob in x/blobs/sha256/*; do
  if tar -tf "$blob" 2>/dev/null | grep -Fxq 'root/secret.txt'; then
    echo "발견한 레이어: $(basename "$blob")"
    tar -xOf "$blob" root/secret.txt
  fi
done
```

- 가이드와 현재 Docker containerd 이미지 저장소를 기준으로 blobs/sha256 안의 tar 레이어를 조회한다. JSON 메타데이터 등 tar가 아닌 blob의 오류는 숨기지만 추출 결과는 숨기지 않는다. 출력이 없으면 성공으로 간주하지 않고 아카이브 구조를 확인한다.
- 예상은 레이어 해시와 DEMO_ONLY_FILE_SECRET 출력이다. 원본 secret.txt를 읽는 명령이 아니라 내보낸 이미지 레이어 내부의 파일 내용을 stdout으로 읽는다. 실제 자격 증명은 사용하지 않는다.
- leak.tar·x는 Ubuntu 실습 폴더에 생성될 예정이며 Windows나 Git으로 옮기지 않는다. 아직 내보내기·추출·정리를 실행한 증거는 없고 Codex가 대신 실행하지 않았다.

### 2026-09-27 — 삭제 파일의 레이어 잔존 확인·정리 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. [주요 관찰 증거](evidence/leak-layer-user-2026-09-27.txt).
- docker save·tar 추출 명령이 오류 출력 없이 프롬프트로 돌아왔고, 후속 레이어 탐색에서 `99815a1743a4f6f7249688c7a3d804cc85632cd5015ef3c3d3ecfbcc1bc2ccd4`와 `DEMO_ONLY_FILE_SECRET`이 출력됐다.
- 최종 컨테이너 목록에서는 파일이 없지만 COPY 시점의 레이어에서 원문이 읽힘을 확인했다. 뒤의 RUN rm은 앞 레이어의 원문을 지운 것이 아니다. ENV 값 노출과 삭제 파일의 레이어 잔존이라는 두 경로를 모두 관찰했다. 3-4 핵심 관찰 완료이며 정리 확인이 남아 있다.
- 다음 정리 안내(사용자 Ubuntu, 결과 대기):

```bash
cd ~/onprem-lab/day03/leak && rm -rf -- ./x ./leak.tar
docker image rm leak:1
test ! -e x && test ! -e leak.tar && echo "임시 파일 정리 확인"
docker image ls --filter reference=leak:1
```

- 디렉터리 이동에 성공한 경우에만 해당 실습 경로의 x·leak.tar를 제거한다. 사용자 출력으로 현재 경로와 생성 대상을 확인했다. 가짜 문자열이 든 연습 소스 Dockerfile·secret.txt는 남기며 agent 이미지, 타 프로젝트, 빌드 캐시 전체는 정리하지 않는다. 이미지 삭제는 강제 옵션 없이 수행하고 실패 시 원인을 확인한다.
- 이 정리는 임시 산출물·이미지 태그 정리이며 모든 캐시의 비밀 데이터 완전 삭제를 입증하는 절차가 아니다. 실제 비밀을 사용하지 않았고 Codex가 삭제 명령을 대신 실행하지 않았다.

### 2026-09-27 — 3-4 정리 확인·절 완료
- 확인 주체: 사용자 제공 Ubuntu 출력. 위치는 ~/onprem-lab/day03/leak.
- `cd ~/onprem-lab/day03/leak && rm -rf -- ./x ./leak.tar` 실행 후 `test ! -e x && test ! -e leak.tar`의 성공 문구 `임시 파일 정리 확인`을 확인했다.
- `docker image rm leak:1`은 `Untagged: leak:1` 및 `Deleted: sha256:a0166d5a9bfdb92ca132ac47645f5f8daf69d7b42c938cd2a4d6c8e4ea9ebd0b`를 출력했다. 후속 `docker image ls --filter reference=leak:1`에는 헤더만 있고 이미지 행이 없어 해당 태그 부재를 확인했다.
- 가짜 ENV 잔존과 삭제 파일의 이전 레이어 원문 추출, 임시 산출물·실습 이미지 정리까지 확인해 3-4 완료로 기록한다. 연습용 Dockerfile·secret.txt를 삭제하는 명령은 실행하지 않았다. 빌드 캐시 전체 삭제·실제 비밀 완전 삭제 검증은 수행하지 않았다.
- Codex가 Ubuntu 정리를 대신 수행하지 않았다. 3-5 반입 패키지 초안 및 Day 3 전체 마무리는 미진행이다.

### 2026-09-27 — 실습 정리와 비밀 완전 삭제의 차이
- 사용자가 3-4에서 비밀을 완전히 삭제한 것인지 물었다. x·leak.tar·leak:1 정리는 임시 산출물 정리이며, 빌드 캐시·원본 secret.txt·Dockerfile은 별도로 제거하지 않았고 복구 불가능한 삭제를 검증하지 않았다고 설명했다.

### 2026-09-27 — 3-5 반입 패키지 초안 시작
- 사용자 후속 요청으로 3-5 및 부록 E-4를 읽었다. Windows에 [반입 패키지 초안](IMPORT-PACKAGE.md)을 생성하고 기존 빌드·스캔 증거를 연결했다. Ubuntu 파일이나 실제 고객사 시스템에는 쓰지 않았다.
- 가이드의 `Base={{index .Config.Env 0}}`는 첫 환경변수를 반환하므로 베이스 이미지 근거로 사용하지 않는다. 베이스는 이미 확보한 빌드 로그를 사용한다. 이미지 ID·manifest·manifest list·RepoDigests를 구분한다.
- 가이드의 Trivy --output은 호스트 출력 폴더 마운트 없이 --rm 컨테이너 안에 파일을 생성하므로 그대로 사용하지 않는다. 이미 tee로 호스트에 보존한 검사 로그를 재사용하며 동일 조건 스캔을 반복하지 않는다.
- 3-2의 동작 검사는 agent:0.1.0 대상이었다. 새 이미지 0.2.0의 사용자·포트·크기·헬스체크 정의 등을 아래 명령으로 확인한다. 실행 위치는 사용자 Ubuntu이며 결과 대기 중이다.

```bash
docker image inspect agent:0.2.0 --format 'ID={{.Id}}
RepoDigests={{json .RepoDigests}}
User={{.Config.User}}
Exposed={{json .Config.ExposedPorts}}
SizeBytes={{.Size}}
Platform={{.Os}}/{{.Architecture}}
Healthcheck={{json .Config.Healthcheck}}'
docker run --rm agent:0.2.0 id
```

- 첫 명령은 이미지 조회, 두 번째는 임시 컨테이너에서 실제 UID·GID 조회다. 앱을 기동하거나 외부 포트를 공개하지 않는다. 실제 비밀 값이 포함될 수 있는 ENV 전체 출력은 이번 수집 명령에서 요구하지 않는다.
- Ubuntu와 Windows 자동 동기화를 가정하지 않으며, 새 이미지 비밀 미포함·읽기 전용 앱 정상 동작·보안 승인 등을 근거 없이 확정하지 않는다. 고객사 승인 기준은 미정으로 둔다.

### 2026-09-27 — 새 이미지 정보 확인·3-5 초안 작성 완료
- 확인 주체: 사용자 제공 Ubuntu inspect·id 출력. [조회 증거](evidence/image-agent-0.2.0-user-2026-09-27.txt).
- ID는 sha256:a4ef49ae142efb1a03fe43c30d4a6f68ceee1c649578c33407827e8f6f4185a3이며 RepoDigests에도 agent@와 같은 해시가 있다. 이는 빌드의 manifest list 해시와 같고 config 해시와 다르다. 실제 값을 그대로 기록하며 원격 push를 했다고 추정하지 않는다.
- User=10001, 선언 포트 8000/tcp, 크기 181278388바이트(약 172.9 MiB), linux/amd64를 확인했다. id 출력은 UID 10001(appuser)·GID 0(root)다.
- Healthcheck의 간격 15초·시작 유예 5초·제한시간 3초·재시도 3회 및 Python urllib.request를 통한 /healthz 요청 정의를 확인했다. 메시지의 URL 링크화·따옴표 변형을 원시 JSON 오류로 간주하지 않는다. 실제 healthy 상태를 검증한 것은 아니다.
- IMPORT-PACKAGE.md에 위 결과를 반영했다. 이전 사용자 첨부에서 새 이미지 HIGH 44건의 검사 결과 표 전체를 발췌해 근거로 연결했다. 원본 로그를 재스캔하거나 Ubuntu와 자동 동기화한 것이 아니다.
- 미검증 항목(새 이미지의 비밀 미포함·읽기 전용 앱 기능·고객사 승인 기준 등)을 명시한 학습용 반입 초안 작성으로 3-5 완료 처리한다. 실제 반입용 tar·SBOM·파일 해시 생성과 고객사 제출·승인은 수행하지 않았다.
- Day 3 실습 3-1~3-5 완료와 Day 전체 마무리를 구분한다. 별도 최종 자기점검, lazydocker 새 이미지 관찰 및 종료 시 자원 상태 확인은 아직 수행하지 않았다. 광범위한 image prune이나 타 프로젝트 자원 정리는 실행하지 않았다.

### 2026-09-27 — 눈으로 확인: lazydocker 시작 안내
- 사용자 요청으로 가이드의 “눈으로 확인 — lazydocker에서 이미지와 레이어”를 진행한다. 환경 기록의 마지막 정상 버전은 0.25.2이며 이번 실행 버전·화면을 새로 확인한 것은 아니다.
- 사용자 Ubuntu 터미널에서 `lazydocker`를 실행하고 왼쪽 Images 패널에서 agent:0.2.0을 선택하도록 안내했다. 현재 어느 실습 폴더인지와 무관하게 같은 Docker 엔진의 이미지 목록을 조회한다.
- 관찰 항목: agent:0.2.0 표시 여부, 이미지 크기, COPY app.py·의존성 복사 등 레이어/이력, 태그 없는 <none> 항목 유무. inspect의 기존 Size는 181278388바이트(약 181.3 MB / 172.9 MiB)이며 도구의 집계·표시 단위 차이 가능성을 구분한다.
- 화면 캡처 또는 관찰 결과 대기 중이다. 이번 안내는 관찰 단계이며 삭제 키나 image prune을 실행하도록 안내하지 않았다. <none> 존재만으로 제거 대상을 확정하지 않는다.
- 별도 최종 자기점검과 종료 상태 확인은 아직 미진행이다.

### 2026-09-27 — lazydocker 이미지·이력 관찰 완료
- 확인 주체: 사용자 제공 스크린샷 눈으로.png·눈으로2.png. 원본은 프로젝트 밖에 있고 복사하지 않았다. 화면 하단에서 lazydocker 0.25.2를 확인했다.
- 첫 화면은 Containers 선택 상태이고, 두 번째 화면은 Images의 agent:0.2.0 선택 상태다. 오른쪽 Config에 tag agent:0.2.0, 기존 조회와 같은 a4ef49ae… ID, Size 181.28MB가 표시돼 가이드의 200MB 아래 관찰 기준을 만족했다. 크기는 기존 inspect 값과 반올림 범위에서 일치한다.
- 이력에 COPY app.py 20.00KiB, COPY /build/deps /app/deps 2.95MiB, 사용자 생성 RUN, USER 10001, EXPOSE 8000/tcp, HEALTHCHECK, CMD, PYTHON_VERSION=3.12.14와 Debian trixie 바탕을 확인했다. 이력의 0B 설정 행과 파일 레이어를 구분한다.
- 화면에 보이는 이미지 목록에 agent:0.1.0·0.2.0이 있고 <none> 태그는 보이지 않는다. 이는 표시 범위의 관찰이며 전체 빌드 캐시가 비었다는 뜻은 아니다. 이력의 <missing> 표시는 이미지 목록의 <none> 태그와 구분한다.
- Containers에 exited(143) 상태의 기존 koica-oda-local-test-oda-app-1이 있고 관련 볼륨·네트워크도 보인다. 이번 실습 이미지의 오류로 해석하거나 정리 대상으로 지정하지 않았다. 종료 원인은 이 화면만으로 확정하지 않았다.
- 이미지·컨테이너 삭제나 prune 없이 가이드의 눈으로 확인 단계를 완료했다. 화면 하단의 q: quit 안내에 따라 q로 종료할 수 있다. 최종 자기점검과 별도 종료 상태 확인은 아직 미진행이다.

### 2026-09-27 — 사용자 종료 정리 명령·상태 재확인 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. 위치는 ~/onprem-lab/day03/leak.
- 사용자가 `docker rm -f agent 2>/dev/null; docker rmi leak:1 2>/dev/null` 및 `docker image prune -f >/dev/null; echo "정리 완료 (agent:0.1.0, agent:0.2.0은 유지)"`를 실행한 프롬프트를 제공했다. 이 명령은 이번 turn에서 Codex가 실행하거나 사전에 안내한 것이 아니다.
- 출력은 마지막 정리 문구뿐이다. 오류·삭제 목록이 숨겨져 있고 echo는 앞 명령 성공과 무관하게 실행되므로 각 명령의 성공·실제 제거 목록·보존 이미지 상태를 이 문구만으로 확정하지 않는다. leak:1 삭제 자체는 앞선 3-4 출력으로 이미 확인한 이력이 있다.
- 다음은 사용자 Ubuntu에서 읽기 전용 상태 조회를 안내한다(결과 대기):

```bash
docker image inspect agent:0.1.0 agent:0.2.0 --format '{{json .RepoTags}}'
docker ps -a --filter 'name=^/agent$' --format '{{.Names}} {{.Status}}'
docker image ls --filter reference=leak:1 --format '{{.Repository}}:{{.Tag}}'
```

- 기대 결과는 두 agent 이미지 태그 확인, 이름이 정확히 agent인 컨테이너 및 leak:1 이미지 조회의 빈 출력이다. 다른 프로젝트의 자원을 삭제하거나 prune을 반복하지 않는다. 최종 자기점검은 아직 진행하지 않았다.

### 2026-09-27 — 종료 상태 확인 완료
- 확인 주체: 사용자 제공 Ubuntu 출력. [정리 증거](evidence/cleanup-user-2026-09-27.txt).
- 두 이미지 inspect에서 ["agent:0.1.0"], ["agent:0.2.0"]이 각각 출력됐다. 정확한 이름 agent의 컨테이너 조회와 leak:1 이미지 조회는 출력 없이 프롬프트로 돌아왔다.
- 두 agent 이미지 보존과 실습 종료 대상 부재를 확인했다. 앞선 x·leak.tar 제거 확인과 합쳐 Day 3 실습 자원 정리 완료로 기록한다. image prune의 개별 삭제 목록은 숨겨져 확인하지 못한 상태를 유지한다.
- 실습 3-1~3-5·반입 패키지 초안·lazydocker 관찰·종료 정리까지 완료했다. 별도 최종 자기점검 5문항은 미진행이며 Day 전체 학습 완료와 구분한다. Day 4를 시작하거나 새 작업을 생성하지 않았다.

### 2026-09-27 — 사용자 완료 확인·Day 3 요약
- 사용자 발언: “좋아. 다 완료했어. Day3에서 우리가 뭘한건지 정리해줘.” 이를 Day 3 학습 종료·완료 확인으로 기록한다. 별도 자기점검 5문항의 답변이나 평가 결과가 제공된 것으로 확대 해석하지 않는다.
- 실제 실행 증거로 3-1~3-5·lazydocker 관찰·종료 정리를 이미 확인했다. 사용자의 완료 확인을 반영해 Day 3 완료 상태로 갱신하고 README에 단계별 결과 요약을 추가했다.
- 핵심 흐름: 이미지 구성 관찰 → 실행 권한·설정 확인 → 취약점 검사·베이스 변경·재검사 → 비밀의 레이어 잔존 관찰 → 반입 근거 문서화.
- 최종 결과: agent:0.2.0, Python 3.12.14·Debian 13.7, HIGH 44·CRITICAL 0. 필터 후 0건은 잔여 위험 해소가 아니며 실제 영향 평가·예외 승인은 하지 않았다. 실제 심의·반입·운영 배포도 수행하지 않았다.
- 기록은 Windows에 정리했고 Ubuntu와 자동 동기화하지 않았다. Git 커밋·PR 생성·Day 4 실습은 요청받지 않아 수행하지 않았다.

### 2026-09-27 — Day 3 마무리·저장소 제출
- 사용자 요청: Day 3를 마무리하고 저장소 업데이트 PR을 만든다.
- Codex가 Windows 기록과 사용자 제공 증거를 대조했다. 실습 결과 요약, 반입 패키지 초안, 빌드·스캔·비밀 잔존·정리 출력 및 환경 차이를 제출 대상으로 정리했다.
- 원격 갱신으로 Day 2 PR #4의 main 병합(`18b805e`)을 확인하고 `codex/day03-results` 브랜치를 만들었다. Ubuntu 실습은 재실행하거나 동기화하지 않았다.
- 별도 자기점검 평가, 실제 고객사 승인·운영 배포, Day 4 실습은 진행하지 않았다.
- Codex 직접 문서 검증: 제출 대상 13개 파일의 LF 유지, Markdown 상대 링크 53개 대상 존재, `git diff --check` 통과를 확인했다. agent·skeleton·day03/scan.sh·가이드 원문 변경은 없다. 문서 변경이므로 앱 테스트·이미지 빌드는 재실행하지 않았다.

## 가이드와 실제 환경의 차이
공통 환경은 [환경 기록](../docs/environment.md)을 참고한다.

## 다음에 이어 할 지점
Day 3 완료(사용자 확인). 다음 학습은 사용자 요청 시 Day 4 README·SESSION·가이드부터 확인한다. 자기점검 복습을 요청하면 5문항을 별도로 진행할 수 있다. 저장소 제출 결과는 위 마무리 기록에서 확인한다.
