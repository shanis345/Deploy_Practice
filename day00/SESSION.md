# Day 0 — 환경 준비

## 진행 상태
- 날짜: 2026-09-22
- 상태: 진행 중 — **0-1 부트스트랩 완료**
- 완료한 범위: WSL2 확인, Docker Desktop 연동·권한 해결, 실습 파일 복사, 부트스트랩 실행과 최종 점검
- 중단 지점: 0-1 검증 후 사용자 요청으로 정지. 이후 절은 미진행
- Codex 작업: 이 프로젝트를 준비한 기존 대화. 별도 Day 0 작업은 아직 생성하지 않음
- 실행 증거 기준: 아래 실습 결과는 사용자가 직접 실행한 후 대화에 제공한 출력에 근거함

## 목표와 이번 세션 범위
Windows의 Ubuntu WSL2와 Docker Desktop으로 실습 환경을 준비한다.
사용자는 명시적으로 0-1까지만 진행하도록 제한했다.
이 기록은 Day 0 전체 완료나 학습용 에이전트 이미지 빌드 완료를 뜻하지 않는다.

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
| 증상 | 확인한 원인 또는 상태 | 해결·결과 |
|---|---|---|
| Ubuntu에서 docker를 찾지 못함 | WSL 연동 필요 메시지 | 연동 설정 안내 후 CLI 실행 확인 |
| docker.sock permission denied | 현재 셸에 docker 그룹 미반영 | newgrp docker 후 Server 응답 확인 |
| getnt 또는 제어문자가 포함된 명령 실패 | 오타·붙여넣기 문제 | 정확한 getent 재입력 |
| cp -n 경고 | 옵션 이식성 경고 | 파일 목록과 check 실행으로 복사 확인 |

## 배운 내용과 질문
- PowerShell과 Ubuntu 셸을 구분한다. 실습 명령은 Ubuntu에서 실행한다.
- Docker CLI 실행과 엔진 연결 성공은 별개다. Client와 Server를 함께 확인한다.
- 사용자 그룹 등록과 현재 세션의 적용 상태는 다를 수 있다.
- bootstrap.sh의 check는 도구 존재와 기본 응답을 확인하며 고정 버전 일치를 검증하지 않는다.

## 가이드와 실제 환경의 차이
- kubectl: 가이드 v1.31.0, 실제 v1.36.1. 기존 설치를 스크립트가 유지함.
- dive: 가이드 본문 0.12.0, 첨부 스크립트 설정과 실제 설치는 0.13.1.
- Compose: 가이드 표기는 v2, 실제 출력은 v5.5.1. `docker compose` 실행이 확인됐으며 이후 실습 호환성 검증을 뜻하지는 않음.
- [전체 환경 기록](../docs/environment.md)을 참고한다. 버전 차이는 기록만 했으며 수정하지 않았다.

## 프로젝트 정리
후속 사용자 요청으로 Windows의 `12. Deploy Practice` 폴더에 실습 소스·가이드·원본 ZIP·기록을 복사해 배치했다.
원본과 Ubuntu의 `/home/user/onprem-lab`은 그대로 유지했다. 이 작업에서 실습 명령을 재실행하지 않았다.
이후 사용자가 만든 [https://github.com/shanis345/Deploy_Practice](https://github.com/shanis345/Deploy_Practice)에 자료를 PR로 제출하도록 요청했다.
Git 초기화와 `codex/initial-practice-setup` 브랜치 준비는 프로젝트 관리 작업이며 실습 진도에 포함하지 않는다.
Codex 프로젝트 등록과 Day별 작업 생성은 아직 하지 않았다.

## 다음에 이어 할 지점
**0-1 완료 지점에서 중단.** 사용자에게 다음 범위를 지정받기 전까지 실습을 진행하지 않는다.
다음 세션은 이 기록과 환경 차이를 읽고 시작한다. Day 0의 나머지 절은 미진행이다.
