# Day 9 — 폐쇄망 이미지 반입: 오프라인 빌드 · save/load · 사내 레지스트리 · 스캔 · SBOM

## 진행 상태
- 상태: 9-1~9-5·실습 자원 정리 완료 (2026-10-05). 누적 점검·체크포인트 평가는 미진행이며 Day 9 전체 통과로 판정하지 않음.
- 완료한 범위: 9-1 오프라인 빌드, 9-2 파일 반입·격리 엔진 실행·정리, 9-3 사내 레지스트리 push/pull·UI·앱 실행·시험 정리, 9-4 DB 준비·오프라인 취약점 스캔·CycloneDX SBOM 생성과 요약 확인, 9-5 실측 산출물 기반 학습용 반입 신청서 작성
- 중단 지점: 사용자 출력으로 Compose 컨테이너·네트워크 제거와 압축 전 tar 삭제 명령 성공, regdata·이미지·반입 산출물·캐시 보존을 확인했다. [신청서](IMPORT-PACKAGE.md)는 Windows에 있고 Ubuntu 복사는 미진행이다.
- Codex 작업: 아직 별도 작업을 만들지 않음
- 실행 증거 기준: 사용자 제공 출력과 직접 검증 결과를 구분해 기록

## 목표와 이번 세션 범위
9-1~9-5 완료 후 사용자 요청으로 Day 9 실습 자원 정리를 진행한다. 레지스트리 데이터·이미지·반입 산출물·캐시는 보존하고 Compose 컨테이너·네트워크 및 압축 전 tar를 정리한다. 실제 고객사 제출·승인, 누적 점검 2차·다음 Day는 이번 실행 범위에 포함하지 않는다.

## 실행 기록
### 2026-10-02 — 9-1 시작·사전 점검 안내
- 사용자 요청: "좋아 그럼 9-1을 해보자". 진행·환경·Day 9 README/SESSION·가이드 9-1 및 Windows 실습 소스를 읽었다.
- Codex 직접 확인: Windows day09의 requirements.txt는 pyyaml==6.0.2이며 Dockerfile.offline은 python:3.12.14-slim과 wheels 디렉터리를 사용한다. --no-index로 로컬 wheel을 설치하며 최종 실행 사용자는 UID 10001·GID 0이다. Ubuntu 상태는 아직 확인하지 않았다.
- Windows SHA-256: Dockerfile.offline=d972cd67249eab2a2d5870ce8daf32810f7c19b95133a33bdd906b555814d7f0, requirements.txt=8320562585358eff824b13356c837a7ffb3faf7d8700823fbc014a3a8c8ec71a, app.py=fdab9fd80709fe7a7ff99527cdf1ff68d3c80ecaab72d148bf4dc5d76b9b01b0.
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day09. 아래 명령은 안내만 했으며 사용자 출력 대기 중이다. cd 실패 시 이후 명령을 실행하지 않는다.

```bash
cd /home/user/onprem-lab/day09
pwd
sha256sum Dockerfile.offline requirements.txt app.py ../agent/requirements.txt ../agent/app.py
docker version
docker context show
docker image inspect python:3.12.14-slim --format 'ID={{.Id}} OS={{.Os}} ARCH={{.Architecture}}'
docker image ls agent:0.2.0-offline
ls -ld wheels 2>/dev/null || true
```

- 목적: Windows·Ubuntu 사본과 agent 원본의 일치 여부, Docker 엔진 응답·컨텍스트, 베이스 이미지 존재·플랫폼 및 기존 산출물 유무를 확인한다. wheels 부재는 첫 실행 시 정상이다.
- 다운로드·빌드·컨테이너 실행·파일 복사·Ubuntu 동기화는 아직 수행하지 않았다. 기존 Day 8 병합 메모 변경을 보존했다.
- 후속 계획: 사전 점검 결과 확인 → 같은 Python·플랫폼에서 wheel 준비 → 네트워크를 제한한 빌드·기동 확인 → 온라인용 Dockerfile과 비교. 실제 명령은 각 단계에서 안내한다. 빌드 캐시가 비교 실패를 가리지 않도록 하고 빌드 RUN의 네트워크 제한과 빌더 전체의 외부 통신 차이를 구분한다.

## 오류와 해결
- 증상: python:3.12.14-slim inspect가 No such image로 실패했다.
- 확인한 원인: 현재 Docker 컨텍스트에서 해당 태그의 로컬 이미지를 찾지 못한다. 과거 이미지 존재 기록과 구분하며 삭제 경위는 미확인이다.
- 해결 방법: 온라인 준비 단계에서 정확한 태그·linux/amd64 이미지를 pull하도록 안내했다.
- 재확인 결과: 사용자 pull 성공 및 inspect의 OS=linux ARCH=amd64로 이미지 준비를 확인했다. 상세 증거는 아래 베이스 이미지 준비 기록에 있다.

## 배운 내용과 질문
- Day 9 핵심 개념과 Nexus의 Docker/PyPI 저장소 역할을 설명했다. 완성 이미지 반입 시 런타임 라이브러리 다운로드·레지스트리 의존을 줄일 수 있지만 첫 실행 다운로드·별도 의존 이미지·외부 설정은 준비해야 함을 설명했다. 개념 설명이며 실습 검증 결과가 아니다.

## 가이드와 실제 환경의 차이
공통 환경은 [환경 기록](../docs/environment.md)을 참고한다.

## 다음에 이어 할 지점
9-1~9-5·실습 자원 정리 완료. 다음 범위는 사용자 요청 후 정한다. 누적 점검 2차·체크포인트 평가는 미진행이다. registry·UI는 제거돼 사용하려면 재기동이 필요하고 regdata·이미지·반입 산출물·캐시는 보존돼 있다. 신청서는 Windows에 있고 Ubuntu 복사는 하지 않았다.

### 2026-10-02 — 사전 점검 확인·베이스 이미지 준비 안내
- 사용자 Ubuntu 출력으로 day09 Dockerfile.offline·requirements.txt·app.py의 Windows 해시 일치 및 agent 원본 두 파일과의 일치를 확인했다. 가이드의 cp는 동일 파일 덮어쓰기가 되므로 이 상태에서는 필요하지 않다.
- Client/Engine 29.8.0·API 1.56, Docker Desktop 4.92.0(240144), linux/amd64 및 default 컨텍스트 응답을 확인했다.
- python:3.12.14-slim은 No such image이며 agent:0.2.0-offline 목록에는 이미지 행이 없다. wheels 조회는 출력이 없었으나 오류를 숨긴 명령이므로 부재 원인을 단정하지 않는다. [사용자 증거](evidence/91-precheck-user-2026-10-02.txt).
- 아래 명령을 Ubuntu /home/user/onprem-lab/day09에서 사용자에게 안내했다. 인터넷이 되는 준비 단계이며 다운로드 성공·플랫폼 확인 결과는 아직 받지 않았다. &&는 pull 성공 시에만 inspect를 수행한다.

```bash
docker pull --platform linux/amd64 python:3.12.14-slim &&
docker image inspect python:3.12.14-slim --format 'ID={{.Id}} OS={{.Os}} ARCH={{.Architecture}}'
```

- 오프라인 빌드에는 Python 패키지뿐 아니라 베이스 이미지도 미리 있어야 한다고 설명했다. wheel 다운로드·빌드·컨테이너 실행 및 9-2 이후는 미진행이다. Codex는 Windows 기록만 갱신했다.

### 2026-10-02 — 베이스 이미지 준비 확인·wheel 다운로드 안내
- 사용자 Ubuntu 출력으로 python:3.12.14-slim pull 성공 및 OS=linux ARCH=amd64를 확인했다. 출력의 Digest와 inspect ID는 모두 sha256:f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f다. 이 출력의 일치 사실만 기록하며 다이제스트와 이미지 ID가 모든 저장 방식에서 같다고 일반화하지 않는다. [증거](evidence/91-base-image-user-2026-10-02.txt).
- 다음은 온라인 준비 단계에서 PyYAML 6.0.2 wheel을 받는 명령이다. 사용자 Ubuntu /home/user/onprem-lab/day09에서 실행하도록 안내했으며 결과 대기 중이다.

```bash
mkdir -p wheels &&
docker run --rm --pull=never --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD:/w" -w /w python:3.12.14-slim \
  python -m pip download --disable-pip-version-check --no-cache-dir \
  --only-binary=:all: --dest /w/wheels -r requirements.txt &&
ls -lh wheels/ &&
du -sh wheels/
```

- 가이드 보완: 명시적 플랫폼·기존 이미지 사용, 사용자 UID/GID로 호스트 wheel 소유권 유지, 소스 배포본 대신 wheel만 다운로드, 로그 표시 및 성공 시에만 목록 확인. 컨테이너는 종료 후 제거되며 바인드 마운트의 wheels 파일은 Ubuntu에 남는다. pip download는 패키지를 설치하는 명령이 아니다.
- 다운로드된 wheel 파일명·용량은 실제 출력으로 확인한다. 예상 cp312·x86_64이며 가이드의 파일명·용량을 실제 결과로 기록하지 않는다.
- Codex 직접 Ubuntu 실행·파일 동기화는 없다. wheel 다운로드·오프라인 빌드·앱 기동 검증 및 9-2 이후는 아직 미완료다.

### 2026-10-02 — wheel 준비 확인·오프라인 빌드 안내
- 사용자 출력으로 PyYAML 6.0.2 wheel 다운로드 성공을 확인했다. 파일명은 PyYAML-6.0.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl, ls 표시 750K·user:user·0644, wheels 디렉터리 사용량은 756K다. Python 3.12·x86_64 타깃과 일치한다. [증거](evidence/91-wheels-user-2026-10-02.txt).
- 사용자 Ubuntu /home/user/onprem-lab/day09에서 다음 빌드·이미지 확인을 안내했다. 실행 결과 대기 중이며 성공으로 처리하지 않는다.

```bash
docker build --builder default --platform linux/amd64 \
  --network=none --no-cache --pull=false --progress=plain \
  -f Dockerfile.offline --build-arg APP_VERSION=0.2.0 \
  -t agent:0.2.0-offline . &&
docker image inspect agent:0.2.0-offline \
  --format 'ID={{.Id}} OS={{.Os}} ARCH={{.Architecture}} USER={{.Config.User}}'
```

- default 빌더를 지정해 현재 엔진의 베이스 이미지를 사용하도록 한다. --no-cache로 설치 단계가 캐시 재사용으로 생략되지 않도록 하고 --progress=plain으로 실제 pip 출력을 확인한다. --pull=false는 항상 최신 베이스를 pull하는 동작을 끄는 옵션이며 외부 통신을 전부 차단하는 옵션은 아니다.
- --network=none은 Dockerfile RUN 단계의 네트워크를 제한한다. PC 전체 또는 빌더의 메타데이터 조회까지 단절한 시험으로 해석하지 않는다. 공식 근거: https://docs.docker.com/reference/cli/docker/buildx/build/ 및 https://docs.docker.com/build/builders/.
- Dockerfile의 --no-index·--find-links=/tmp/wheels로 로컬 wheel에서 설치하는 과정과 Successfully installed pyyaml-6.0.2, 최종 이미지 linux/amd64·USER=10001을 실제 결과에서 확인할 예정이다. 앱 기동 및 9-2 이후는 진행하지 않았다. Codex는 Windows 기록만 갱신했다.

### 2026-10-02 — 오프라인 빌드 확인·네트워크 없는 앱 기동 안내
- 사용자 출력으로 default docker 빌더에서 로컬 wheel Processing·Successfully installed pyyaml-6.0.2 및 이미지 생성 성공을 확인했다. 이미지 inspect ID=sha256:4c10e5ca549f993cb5d5271e24bb4ff28ae6426f3fd91a5f52b7172796dcf812, OS=linux ARCH=amd64 USER=10001이다. [빌드 증거](evidence/91-build-user-2026-10-02.txt).
- FROM·WORKDIR에는 CACHED가 보이지만 pip RUN은 설치 로그·실행 시간과 함께 실제 수행됐다. pip root 경고는 빌더 단계의 설치 사용자에 관한 것이며 최종 실행 사용자 설정과 구분한다. 실제 프로세스 UID는 다음 단계에서 확인한다. 베이스 메타데이터 단계가 있었으며 빌더 전체의 외부 통신 부재를 증명한 것은 아니다.
- 다음 명령은 사용자 Ubuntu /home/user/onprem-lab/day09에서 실행하도록 안내했다. 컨테이너는 network=none이며 호스트 포트 게시 없이 내부 loopback으로 healthz를 조회한다. 실행 결과는 아직 받지 않았다.

```bash
docker run -d --pull=never --network none \
  --name day09-offline-test agent:0.2.0-offline &&
sleep 2 &&
docker inspect day09-offline-test \
  --format 'STATUS={{.State.Status}} NETWORK={{.HostConfig.NetworkMode}}' &&
docker exec day09-offline-test python -c '
import os, urllib.request, yaml
print("UID=", os.getuid(), "GID=", os.getgid())
print("PyYAML=", yaml.__version__)
print(urllib.request.urlopen("http://127.0.0.1:8000/healthz", timeout=5).read().decode())
'
```

- 기대값은 running·none, UID=10001·GID=0, PyYAML=6.0.2, healthz status=ok·version=0.2.0이다. 이는 기동·해당 경로의 검증이며 외부 DB/LLM 통합 시험은 아니다. 이름 충돌 등 오류 시 자동 삭제하지 않고 출력부터 확인한다.
- 컨테이너는 결과 확인 후 정리할 예정이며 아직 생성 성공·정리 완료로 기록하지 않는다. 온라인용 Dockerfile 실패 비교 및 9-2 이후는 미진행이다. Codex는 Windows 기록만 갱신했다.

### 2026-10-03 — 네트워크 없는 기동 확인·정리 및 온라인 빌드 비교 안내
- 사용자 Ubuntu 출력에서 컨테이너 21519ca2ac3f의 running·NETWORK=none, exec Python의 UID=10001·GID=0, PyYAML=6.0.2 및 healthz status=ok·version=0.2.0을 확인했다. 출력 수신일을 기록했으며 실제 실행 시각은 미제공이다. [증거](evidence/91-runtime-user-2026-10-03.txt).
- 네트워크가 없는 컨테이너에서 패키지 로딩과 앱 기동·healthz 응답 성공을 확인했다. Docker health 상태 자체나 전체 기능·DB/LLM 통합 검증은 아니다.
- Codex가 읽은 Windows agent/Dockerfile은 기본 BASE=python:3.12.7-slim이며 pip install이 외부 인덱스를 사용한다. SHA-256=318eaab0d59bc5242bef1c2349d09fcdee9606ecbd3c1dd6c6a6d82a31be79c9. Ubuntu 사본 해시는 아직 미확인이다.
- 사용자 Ubuntu /home/user/onprem-lab/day09에서 아래 두 블록을 순서대로 실행하도록 안내했다. 첫 정리가 실패하면 비교 빌드로 넘어가지 않고 결과를 확인한다. 이미지는 유지한다.

```bash
docker rm -f day09-offline-test &&
docker ps -a --filter 'name=^/day09-offline-test$' --format 'table {{.Names}}\t{{.Status}}'
```

```bash
sha256sum ../agent/Dockerfile &&
docker build --builder default --platform linux/amd64 \
  --network=none --no-cache --pull=false --progress=plain \
  --build-arg BASE=python:3.12.14-slim --build-arg APP_VERSION=0.2.0 \
  -f ../agent/Dockerfile -t day09-online-check:expected-fail ../agent
echo "빌드 종료 코드=$?"
```

- 비교 조건: 같은 준비된 베이스·플랫폼·버전, RUN 네트워크 제한·캐시 미사용. 가이드 기본 BASE의 차이 때문에 생길 수 있는 불필요한 베이스 다운로드를 피한다. 성공한 agent:0.2.0-offline 태그는 유지하며 비교용 태그를 사용한다.
- 예상은 pip 인덱스 접속의 이름 해석 오류·패키지 다운로드 실패 및 빌드 종료 코드 1이다. grep으로 로그를 자르지 않고 실제 실패 단계와 종료 코드를 확인한다. 실패 자체만으로 예상된 원인이라고 판정하지 않는다. 예기치 않게 성공하면 새 비교 이미지의 확인·정리를 후속 처리한다.
- 정리·비교 명령은 안내만 했으며 아직 결과 대기 중이다. 컨테이너는 마지막 확인상 실행 중이다. 9-1 최종 완료·9-2 이후 진행·Codex 직접 Ubuntu 실행은 없다.

### 2026-10-03 — 시험 컨테이너 정리·온라인 빌드 실패 확인 및 9-1 완료
- 사용자 첨부 텍스트에서 docker rm -f day09-offline-test의 이름 출력과 정확한 이름 필터 목록의 NAMES STATUS 헤더만 남음을 확인했다. 시험 컨테이너 정리 완료다. [사용자 출력 원문](evidence/91-cleanup-online-failure-user-2026-10-03.txt).
- Ubuntu agent/Dockerfile의 SHA-256은 318eaab0d59bc5242bef1c2349d09fcdee9606ecbd3c1dd6c6a6d82a31be79c9로 Windows와 일치했다.
- 동일한 python:3.12.14-slim 베이스·linux/amd64·APP_VERSION=0.2.0 및 --network=none·--no-cache 조건에서 온라인용 Dockerfile의 pip install 단계가 재시도 후 실패했다. Temporary failure in name resolution, /simple/pyyaml/ 접속 재시도, No matching distribution found for pyyaml==6.0.2 및 빌드 종료 코드=1을 확인했다.
- 원인: 이번 조건에서는 패키지 인덱스에 접속하지 못해 설치할 배포본을 얻지 못했다. PyYAML 6.0.2가 존재하지 않는다는 뜻이 아니다. 앞서 동일 버전 wheel 다운로드·로컬 설치·import 성공을 확인했다. 베이스 메타데이터 단계는 성공했고 의도한 pip RUN에서 실패했다.
- 비교 빌드는 이미지 export에 도달하지 않았다. 비교 태그의 기존 이미지 유무를 별도 조회한 것은 아니며 빌드 캐시도 삭제하지 않았다. 성공 이미지 agent:0.2.0-offline·베이스 이미지·wheels는 삭제 명령의 대상이 아니었고 마지막 보존 목록을 다시 조회하지는 않았다.
- 9-1 완료 판정: 준비된 wheel을 사용한 RUN 네트워크 차단 빌드 성공, network=none 컨테이너 기동·UID/GID·PyYAML·healthz 성공, 온라인용 빌드의 예상 네트워크 실패 및 시험 컨테이너 정리까지 사용자 증거로 확인했다. 빌더 전체의 네트워크 단절이나 DB/LLM 통합을 시험한 것은 아니다.
- Windows SESSION·PROGRESS·README·환경 기록을 갱신했다. Codex 직접 Ubuntu 실행·동기화·Git 커밋·push는 없다. 요청 범위 9-1에서 멈추며 9-2 이후·Day 9 전체 종료·별도 체크포인트 평가는 미진행이다.

### 2026-10-03 — 9-2 시작·이미지 반입 파일 생성 안내
- 사용자 요청: "9-2로가자". 최신 진행·환경·Day 9 기록과 가이드 9-2를 읽었다. 이번 범위는 이미지 save/load 및 네트워크 없는 별도 Docker 데몬에서의 적재·기동 확인까지이며 9-3은 포함하지 않는다.
- 첫 단계로 사용자 Ubuntu /home/user/onprem-lab/day09에서 아래 명령을 안내했다. 동일한 이름의 파일이 이미 있으면 덮어쓰지 않고 메시지를 출력한다. 사용자는 오류 발생 시 출력을 공유하며 결과 확인 후 다음 단계로 넘어간다.

```bash
if [ -e agent-0.2.0-offline.tar ] || [ -e agent-0.2.0-offline.tar.gz ] || [ -e agent-0.2.0-offline.sha256 ]; then
  echo '같은 이름의 반입 파일이 이미 있습니다. 기존 파일부터 확인하겠습니다.'
else
  docker image inspect agent:0.2.0-offline --format 'ID={{.Id}}' &&
  docker save agent:0.2.0-offline -o agent-0.2.0-offline.tar &&
  gzip -9 -k agent-0.2.0-offline.tar &&
  sha256sum agent-0.2.0-offline.tar.gz > agent-0.2.0-offline.sha256 &&
  cat agent-0.2.0-offline.sha256 &&
  ls -lh agent-0.2.0-offline.tar agent-0.2.0-offline.tar.gz agent-0.2.0-offline.sha256
fi
```

- docker save는 이미지를 파일로 저장하며 원본 이미지를 제거하지 않는다. gzip -k는 tar를 보존하고 SHA-256 대상은 실제 전달할 tar.gz다. 파일 해시와 이미지 ID는 다른 대상의 식별값임을 설명한다. 가이드 예시의 크기·해시와 일치할 필요는 없다.
- 이후 복원 단계에서는 해시를 확인한 tar.gz 자체를 load해 검증 대상과 사용 파일을 일치시킬 계획이다. 로컬 이미지 제거 전에 패키지 검증 결과부터 확인한다. 별도 Docker 데몬 검증에 필요한 docker:27-dind 이미지·충돌 이름·실행 조건은 해당 단계에서 확인한다. 현재는 이미지 삭제·load·컨테이너 실행을 안내하거나 수행하지 않았다.
- .gitignore의 *.tar·*.tar.gz·*.sha256 제외 규칙을 확인했다. 이미지 덤프는 Ubuntu에 보존하고 비밀 없는 결과 증거만 Windows에 기록한다. 파일 생성은 안내만 했으며 사용자 결과 대기 중이다. Codex 직접 Ubuntu 실행·동기화는 없다.

### 2026-10-03 — 반입 파일 생성 확인·검증 및 load 복원 안내
- 사용자 출력으로 save 당시 이미지 ID=sha256:4c10e5ca549f993cb5d5271e24bb4ff28ae6426f3fd91a5f52b7172796dcf812가 9-1 빌드 결과와 일치함을 확인했다. tar 43M·tar.gz 42M·sha256 파일 93바이트이며 모두 user:user 소유다. tar와 tar.gz는 0600, sha256 파일은 0644다. 크기는 ls의 반올림 표시다. [사용자 증거](evidence/92-package-user-2026-10-03.txt).
- 압축 파일 SHA-256은 cd08d49e729c690a20925ecedb1284745c826534ebfd241314b327cb107c52e6이다. 현재까지는 생성 단계이며 sha256sum -c 검증·복원은 아직 미실행이다.
- 사용자 Ubuntu /home/user/onprem-lab/day09에서 다음 명령을 안내했다. gzip 검사와 파일 해시 검증이 성공해야만 이미지 제거가 실행되도록 &&로 연결한다. 정확한 agent:0.2.0-offline 태그만 제거하며 -f는 쓰지 않는다. 사용 중 오류 등이 나면 뒤 명령은 멈추고 결과부터 확인한다.

```bash
gzip -t agent-0.2.0-offline.tar.gz &&
sha256sum -c agent-0.2.0-offline.sha256 &&
docker image rm agent:0.2.0-offline &&
docker image ls agent:0.2.0-offline &&
docker load -i agent-0.2.0-offline.tar.gz &&
docker image inspect agent:0.2.0-offline \
  --format 'ID={{.Id}} OS={{.Os}} ARCH={{.Architecture}} USER={{.Config.User}}'
```

- gzip -t 성공은 보통 출력이 없으며 다음 sha256sum -c의 OK를 확인한다. 이미지 제거 후 목록의 빈 행, Loaded image 및 복원 ID·플랫폼·USER를 사용자 결과에서 확인할 예정이다. 검사한 tar.gz 자체를 load하며 별도 압축 해제는 하지 않는다.
- 동일 데몬의 이미지 제거·복원 시험은 완전히 빈 별도 데몬의 적재 시험과 구분한다. 공유 레이어·빌드 캐시를 전부 제거하지 않는다. 반입 파일·wheels·다른 이미지 삭제는 없다.
- 명령은 안내만 했고 사용자 결과 대기 중이다. 복원 성공·9-2 완료는 아직 아니다. Codex 직접 Ubuntu 실행·전체 동기화·9-3 진행은 없다.

### 2026-10-03 — 파일 검증·load 복원 확인 및 별도 데몬 사전 점검 안내
- 사용자 출력에서 gzip -t 이후 && 체인이 계속 실행됐고 sha256sum -c의 tar.gz: OK를 확인했다. gzip 검사·해시 검증 성공이다.
- agent:0.2.0-offline의 Untagged·Deleted 및 제거 후 이미지 목록에 행이 없음을 확인했다. 이어 검사한 tar.gz에서 Loaded image: agent:0.2.0-offline이 출력됐다. [사용자 증거](evidence/92-load-user-2026-10-03.txt).
- 복원 ID=sha256:4c10e5ca549f993cb5d5271e24bb4ff28ae6426f3fd91a5f52b7172796dcf812로 save 이전과 같으며 OS=linux ARCH=amd64 USER=10001도 유지됐다. 동일 데몬의 복원 성공이며 완전히 빈 별도 데몬의 실행은 아직 시험하지 않았다.
- 다음 사용자 실행 위치는 Ubuntu /home/user/onprem-lab/day09다. 별도 데몬용 이미지 존재·플랫폼 및 시험 이름 충돌 여부만 조회하도록 안내했다.

```bash
docker image inspect docker:27-dind --format 'ID={{.Id}} OS={{.Os}} ARCH={{.Architecture}}'
docker ps -a --filter 'name=^/day09-airgap$' --format 'table {{.Names}}\t{{.Status}}'
```

- 명령은 아직 안내 단계이며 결과 대기 중이다. 이미지가 없으면 온라인 준비 단계에서 먼저 준비하고 이름 충돌이 있으면 기존 자원을 확인한다. 현재 컨테이너 생성·privileged 실행·추가 pull은 하지 않았다.
- 가이드의 별도 Docker 데몬을 컨테이너 안에서 구동하는 dind 시험을 이어갈 예정이며 9-2 완료는 아직 아니다. 반입 파일과 복원 이미지는 유지한다. Codex 직접 Ubuntu 실행·동기화는 없다.

### 2026-10-03 — dind 이미지 부재 확인·다운로드 안내
- 사용자 출력에서 docker:27-dind는 No such image이며 day09-airgap 정확한 이름 필터 목록에는 헤더만 남음을 확인했다. [증거](evidence/92-dind-precheck-user-2026-10-03.txt).
- 다음은 시험 환경을 준비하는 온라인 다운로드다. 실제 폐쇄망을 흉내 내는 컨테이너는 이후 network=none으로 실행한다. 사용자 Ubuntu /home/user/onprem-lab/day09에서 아래 명령을 안내했으며 아직 결과 대기 중이다.

```bash
docker pull --platform linux/amd64 docker:27-dind &&
docker image inspect docker:27-dind \
  --format 'ID={{.Id}} OS={{.Os}} ARCH={{.Architecture}}'
```

- docker:27-dind 태그의 실제 다이제스트·플랫폼은 다운로드 결과로 확인할 예정이다. 컨테이너 생성·privileged 실행은 아직 없고 기존 이미지·반입 파일·wheels는 유지한다. 9-2 완료·9-3 진행·Codex 직접 Ubuntu 실행은 없다.

### 2026-10-03 — dind 이미지 준비 확인·별도 엔진 기동 안내
- 사용자 출력으로 docker:27-dind pull 성공, ID 및 출력 Digest=sha256:aa3df78ecf320f5fafdce71c659f1629e96e9de0968305fe1de670e0ca9176ce, OS=linux ARCH=amd64를 확인했다. [증거](evidence/92-dind-image-user-2026-10-03.txt).
- 사용자 Ubuntu /home/user/onprem-lab/day09에서 아래 명령을 안내했다. 현재는 기동·내부 빈 이미지 목록 확인 단계이며 pull 실패 시험이나 반입 파일 복사는 다음 단계다.

```bash
docker run -d --pull=never --privileged --network none \
  --name day09-airgap docker:27-dind &&
sleep 12 &&
docker inspect day09-airgap \
  --format 'STATUS={{.State.Status}} NETWORK={{.HostConfig.NetworkMode}}' &&
docker exec day09-airgap docker -H unix:///var/run/docker.sock info \
  --format 'Server={{.ServerVersion}} images={{.Images}}'
```

- --privileged는 컨테이너 내부 Docker 데몬 구동에 필요한 확장 권한이다. host Docker 소켓·호스트 경로는 마운트하지 않고 호스트 포트도 게시하지 않는다. exec의 -H는 컨테이너 내부 엔진의 Unix 소켓을 지정한다. 내부 images=0으로 기존 호스트 이미지와 분리된 저장소를 확인할 예정이다.
- 12초는 초기 기동 대기이며 성공 보장이 아니다. info가 실패하면 사용자 출력으로 상태·로그를 진단하고 같은 이름으로 무작정 다시 run하지 않는다.
- 이 시험에서 생성되는 컨테이너와 연결된 익명 볼륨은 검증 후 해당 컨테이너만 docker rm -fv로 정리할 계획이다. 이미지·반입 파일·기존 볼륨에 대한 전역 정리는 하지 않는다. 현재 컨테이너 생성·내부 엔진 응답·익명 볼륨 존재는 아직 미확인이다.
- 공식 설명: https://docs.docker.com/engine/containers/run/ (privileged), https://docs.docker.com/reference/cli/docker/container/rm/ (컨테이너에 연결된 익명 볼륨 제거). 명령은 안내만 했으며 사용자 결과 대기 중이다. 9-2 완료·9-3 진행·Codex 직접 Ubuntu 실행은 없다.

### 2026-10-03 — 별도 엔진 기동 확인·외부 pull 실패 시험 안내
- 사용자 출력으로 day09-airgap(a1a9a7d2713e)의 STATUS=running NETWORK=none, 내부 Docker Server=27.5.1 images=0을 확인했다. 별도 엔진이 응답하며 이미지 저장소가 비어 있다. [증거](evidence/92-dind-start-user-2026-10-03.txt).
- 사용자 Ubuntu /home/user/onprem-lab/day09에서 아래 명령을 안내했다. 외부 pull은 예상 실패이므로 다음 echo 및 info를 &&로 묶지 않는다. 명령은 전체 블록을 순서대로 실행해 pull 직후 종료 코드를 확인한다.

```bash
docker exec day09-airgap docker -H unix:///var/run/docker.sock pull alpine:3.20
echo "pull 종료 코드=$?"
docker exec day09-airgap docker -H unix:///var/run/docker.sock info \
  --format 'Server={{.ServerVersion}} images={{.Images}}'
```

- 기대 결과는 Docker Hub 접속의 네트워크/이름 해석 오류·비정상 종료 코드와 images=0 유지다. 호스트 Docker 엔진의 pull이 아니라 컨테이너 내부 엔진에서 시도한다. 실제 실패 원인을 확인하기 전에는 검증 완료로 기록하지 않는다.
- 현재 day09-airgap은 실행 중이며 정리하지 않았다. 반입 파일 복사·내부 load·앱 기동은 아직 미진행이다. 다음은 파일 반입 시험이며 9-2 완료·9-3 진행·Codex 직접 Ubuntu 실행은 없다.

### 2026-10-03 — 외부 pull 실패 확인·파일 반입 및 내부 load 안내
- 사용자 출력에서 registry-1.docker.io 이름 조회를 위한 DNS 서버 192.168.65.7:53 접속이 network is unreachable로 실패하고 pull 종료 코드=1, 내부 Server=27.5.1 images=0이 유지됨을 확인했다. 레지스트리 인증·이미지 부재가 아니라 네트워크 경로 부재에 따른 예상 실패다. [증거](evidence/92-airgap-pull-user-2026-10-03.txt).
- 사용자 Ubuntu /home/user/onprem-lab/day09에서 아래 명령을 안내했다. tar.gz와 기존 해시 파일을 내부 /tmp에 같은 파일명으로 복사하고, 그 위치에서 해시 검증이 성공할 때에만 내부 Docker 엔진에 load한다.

```bash
docker cp agent-0.2.0-offline.tar.gz day09-airgap:/tmp/agent-0.2.0-offline.tar.gz &&
docker cp agent-0.2.0-offline.sha256 day09-airgap:/tmp/agent-0.2.0-offline.sha256 &&
docker exec -w /tmp day09-airgap sha256sum -c agent-0.2.0-offline.sha256 &&
docker exec day09-airgap docker -H unix:///var/run/docker.sock load \
  -i /tmp/agent-0.2.0-offline.tar.gz &&
docker exec day09-airgap docker -H unix:///var/run/docker.sock image inspect \
  agent:0.2.0-offline \
  --format 'ID={{.Id}} OS={{.Os}} ARCH={{.Architecture}} USER={{.Config.User}}'
```

- docker cp는 호스트 Docker 관리 경로를 통한 파일 전달이며 시험 컨테이너의 인터넷 연결을 활성화하지 않는다. 내부 검증의 기준 해시는 생성 때 보존한 cd08d49e729c690a20925ecedb1284745c826534ebfd241314b327cb107c52e6이다. 외부 파일은 그대로 유지한다.
- 기대값은 해시 OK, Loaded image: agent:0.2.0-offline, linux/amd64·USER=10001이다. 내부 이미지 ID는 실제 결과로 기록한다. 서로 다른 엔진의 이미지 저장 방식 차이가 있을 수 있어 표시 ID만으로 임의 판정하지 않는다.
- 안내만 했고 결과 대기 중이다. day09-airgap은 실행 중이며 내부 앱 기동·시험 자원 정리·9-2 완료는 아직 아니다. Codex 직접 Ubuntu 실행·9-3 진행은 없다.

### 2026-10-03 — docker cp 성공 표시 후 내부 해시 파일 조회 오류
- 사용자 출력으로 tar.gz 43.8MB·sha256 93B의 docker cp 성공 표시를 확인했지만, 바로 다음 docker exec -w /tmp의 sha256sum -c가 agent-0.2.0-offline.sha256: No such file or directory로 실패했다. [사용자 오류 증거](evidence/92-airgap-copy-error-user-2026-10-03.txt).
- && 체인이 검증 단계에서 중단돼 내부 docker load·image inspect는 실행되지 않았다. 복사 성공 메시지만으로 컨테이너 실행 환경에서 파일이 보인다고 판단하지 않는다. 압축 파일 손상·해시 불일치·네트워크 문제로 확정할 근거도 아직 없다.
- 원인은 미확정이다. 사용자 Ubuntu /home/user/onprem-lab/day09에서 다음 읽기 전용 명령을 안내했다.

```bash
docker exec -w /tmp day09-airgap sh -c 'pwd; ls -ld /tmp; ls -lah /tmp'
docker inspect day09-airgap \
  --format 'ID={{.Id}} STATUS={{.State.Status}} RESTARTS={{.RestartCount}} MOUNTS={{json .Mounts}}'
```

- 실제 작업 위치와 파일명·존재 여부, 컨테이너 동일성·실행 상태·마운트를 확인해 원인을 좁힌다. 기존 파일 삭제·컨테이너 재생성·네트워크 설정 변경은 하지 않는다. 복사 재시도·다른 경로 사용은 출력 확인 후 결정한다.
- 현재 진단 출력 대기 중이며 파일 검증 성공·내부 적재·앱 기동·9-2 완료는 아니다. Codex는 Windows 기록만 갱신했다.

### 2026-10-03 — 빈 /tmp·컨테이너 동일성 확인 및 반입 경로 변경 안내
- 사용자 출력의 pwd는 /tmp이고 ls에는 .·..만 있다. 컨테이너 ID는 최초 기동과 같고 STATUS=running RESTARTS=0이다. inspect Mounts에는 /var/lib/docker 익명 볼륨 ba9f80170ab1734fe7dee47dddf808470eb6e88a23b917896b374b42fed6b698만 표시됐다. [진단 증거](evidence/92-airgap-tmp-user-2026-10-03.txt).
- 공식 Moby v27.5.1 hack/dind 소스 51~53행에서 /tmp가 마운트 지점이 아니면 mount -t tmpfs none /tmp를 실행함을 확인했다: https://raw.githubusercontent.com/moby/moby/v27.5.1/hack/dind . 실행 중 내부 마운트 때문에 cp 경로와 내부 프로세스가 보는 경로가 달라졌을 가능성이 크다. 현재 사용자 환경의 /proc/self/mountinfo는 아직 받지 않았으므로 원인 확정과 구분한다. Docker inspect의 Mounts만으로 내부 동적 마운트 부재를 단정하지 않는다.
- 처음 안내한 /tmp 대신 전용 일반 디렉터리 /day09-import를 사용한다. 사용자 Ubuntu /home/user/onprem-lab/day09에서 아래 조회 및 재시도를 안내했다.

```bash
docker exec day09-airgap sh -c 'grep " /tmp " /proc/self/mountinfo || true'
```

```bash
docker exec day09-airgap mkdir -p /day09-import &&
docker cp agent-0.2.0-offline.tar.gz day09-airgap:/day09-import/ &&
docker cp agent-0.2.0-offline.sha256 day09-airgap:/day09-import/ &&
docker exec -w /day09-import day09-airgap sha256sum -c agent-0.2.0-offline.sha256 &&
docker exec day09-airgap docker -H unix:///var/run/docker.sock load \
  -i /day09-import/agent-0.2.0-offline.tar.gz &&
docker exec day09-airgap docker -H unix:///var/run/docker.sock image inspect \
  agent:0.2.0-offline \
  --format 'ID={{.Id}} OS={{.Os}} ARCH={{.Architecture}} USER={{.Config.User}}'
```

- 네트워크·컨테이너 재시작·호스트 파일은 변경하지 않는다. 해시 검증 성공 조건으로만 load를 실행한다. 기존 /tmp로 복사한 데이터의 실제 위치는 미확정이며 개별 삭제하지 않는다. 시험 종료 시 컨테이너 정리 대상에 포함된다.
- 사용자 실행 결과 대기 중이며 오류 해결·내부 load 성공·앱 기동·9-2 완료는 아직 아니다. Codex는 Windows 기록만 갱신했다.

### 2026-10-03 — /tmp tmpfs 확인·경로 변경 복구 성공 및 내부 앱 기동 안내
- 사용자 mountinfo에서 /tmp가 tmpfs 마운트임을 확인했다. /day09-import로 경로를 바꾸자 두 파일 복사·sha256sum -c OK·Loaded image: agent:0.2.0-offline이 성공했다. /tmp 전달 경로 오류는 경로 변경으로 해결했다. cp 데이터가 가려지는 내부 구현 경로를 직접 추적한 것은 아니다. [증거](evidence/92-airgap-load-user-2026-10-03.txt).
- 내부 이미지 ID=sha256:b7e1e28f346895634bd4c58e176bc9dc05c4c6b2522e65f1ec6044fc6b327db9, OS=linux ARCH=amd64 USER=10001이다. 이 ID는 9-1 빌드 로그의 exporting config 해시와 정확히 일치한다. 외부 엔진의 4c10e5...는 같은 빌드 로그의 manifest list 해시였다. 동일 파일의 해시 검증 성공 및 각 해시 대상 일치를 확인했으며 두 표시 ID 차이만으로 손상이라고 판단하지 않는다.
- 사용자 Ubuntu /home/user/onprem-lab/day09에서 다음 명령을 안내했다. 모든 내부 Docker 명령은 day09-airgap의 Unix 소켓을 명시한다. agent는 호스트가 아닌 내부 엔진에서 network=none·--pull=never로 실행한다.

```bash
docker exec day09-airgap docker -H unix:///var/run/docker.sock run \
  -d --pull=never --network none --name agent agent:0.2.0-offline &&
sleep 2 &&
docker exec day09-airgap docker -H unix:///var/run/docker.sock inspect agent \
  --format 'STATUS={{.State.Status}} NETWORK={{.HostConfig.NetworkMode}}' &&
docker exec day09-airgap docker -H unix:///var/run/docker.sock exec agent python -c '
import os, urllib.request, yaml
print("UID=", os.getuid(), "GID=", os.getgid())
print("PyYAML=", yaml.__version__)
print(urllib.request.urlopen("http://127.0.0.1:8000/healthz", timeout=5).read().decode())
'
```

- 기대값은 running·none, UID=10001 GID=0, PyYAML=6.0.2, healthz status=ok·version=0.2.0이다. 실행 결과는 아직 받지 않았다. 이 시험은 패키지 로딩·앱 기동과 healthz 경로이며 외부 DB/LLM 통합은 아니다.
- day09-airgap과 내부 적재 이미지는 유지한다. 내부 앱 기동 성공·시험 정리·9-2 완료는 아직 아니다. Codex 직접 Ubuntu 실행·9-3 진행은 없다.

### 2026-10-03 — 별도 엔진의 반입 앱 기동 성공·시험 정리 안내
- 사용자 출력으로 내부 agent(4d55ca6f2f12)의 running·NETWORK=none, UID=10001 GID=0, PyYAML=6.0.2 및 healthz status=ok·version=0.2.0을 확인했다. [기동 증거](evidence/92-airgap-runtime-user-2026-10-03.txt).
- 검증 의미: 초기 이미지 0개·외부 pull 불가인 별도 엔진에 준비한 파일을 복사·검증·load한 후, 추가 다운로드 없이 앱 기동·패키지 import·healthz 응답을 확인했다. Docker health 상태 자체·DB/LLM 통합은 시험하지 않았다. 실행 검증은 완료했으며 시험 자원 정리는 아직이다.
- 사용자 Ubuntu /home/user/onprem-lab/day09에서 아래 명령을 안내했다. 먼저 내부 agent를 제거한 다음 day09-airgap을 연결된 익명 볼륨과 함께 제거한다. 정확한 이름의 호스트 컨테이너와 앞서 확인한 익명 볼륨만 후속 조회한다.

```bash
docker exec day09-airgap docker -H unix:///var/run/docker.sock rm -f agent &&
docker rm -fv day09-airgap &&
docker ps -a --filter 'name=^/day09-airgap$' --format 'table {{.Names}}\t{{.Status}}' &&
docker volume ls --filter 'name=^ba9f80170ab1734fe7dee47dddf808470eb6e88a23b917896b374b42fed6b698$' &&
docker image inspect agent:0.2.0-offline --format 'ID={{.Id}}' &&
sha256sum -c agent-0.2.0-offline.sha256 &&
ls -lh agent-0.2.0-offline.tar agent-0.2.0-offline.tar.gz agent-0.2.0-offline.sha256
```

- 삭제 대상은 시험 내부 agent·별도 엔진 컨테이너·해당 익명 볼륨이다. 내부 적재 이미지·반입 사본도 시험 환경 정리와 함께 제거된다. 호스트의 agent 이미지·dind 이미지·베이스 이미지·wheels·반입 파일·다른 프로젝트 자원·빌드 캐시는 유지한다. 전역 prune은 사용하지 않는다.
- 예상은 agent·day09-airgap 제거 이름, 컨테이너·익명 볼륨 목록의 헤더만 표시, 호스트 이미지 ID 유지 및 tar.gz: OK다. 실제 출력 전에는 정리 완료 또는 9-2 최종 완료로 처리하지 않는다. Codex 직접 Ubuntu 실행·9-3 진행은 없다.

### 2026-10-03 — 시험 자원 정리 확인 및 9-2 완료
- 사용자 출력으로 내부 agent와 day09-airgap의 제거를 확인했다. 정확한 day09-airgap 이름 필터의 컨테이너 목록과 익명 볼륨 ba9f80170ab1734fe7dee47dddf808470eb6e88a23b917896b374b42fed6b698 필터 목록에는 각각 헤더만 남았다. 시험 컨테이너와 해당 익명 볼륨 정리 완료다. [정리 증거](evidence/92-cleanup-user-2026-10-03.txt).
- 호스트 agent:0.2.0-offline의 ID=sha256:4c10e5ca549f993cb5d5271e24bb4ff28ae6426f3fd91a5f52b7172796dcf812 유지, tar.gz 해시 OK, tar 43M·tar.gz 42M·sha256 93바이트 파일 존재와 user:user 소유권을 확인했다. 크기는 ls 표시값이다.
- dind·베이스 이미지·wheels·다른 프로젝트 자원·빌드 캐시는 삭제 대상이 아니었다. 이들의 최종 목록은 재조회하지 않았다. 반입 파일은 Ubuntu에 보존하며 Windows에는 텍스트 증거만 기록했다.
- 9-2 완료: 이미지 save·압축·SHA-256 생성 및 검증, 동일 엔진 제거·복원, 인터넷 없는 빈 별도 엔진에서 pull 실패·파일 반입·해시 검증·load·앱 기동, 시험 자원 정리와 원본 이미지·반입 파일 보존까지 사용자 출력으로 확인했다.
- 오류 해결 기록: dind /tmp의 tmpfs를 확인하고 /day09-import로 반입 경로를 변경해 파일 조회 오류를 해결했다. 이미지 ID 표시 차이는 원본 빌드 로그의 manifest list 해시와 config 해시에 각각 대응함을 확인했다. 실제 고객사 반입 승인·DB/LLM 통합 시험은 수행하지 않았다.
- Windows SESSION·PROGRESS·README·환경 기록을 함께 갱신하고 요청 범위 9-2에서 멈춘다. 다음은 사용자 요청 후 9-3이다. Day 9 전체 완료·별도 체크포인트 평가·Codex 직접 Ubuntu 실행·전체 동기화·Git 커밋·push는 없다.

### 2026-10-03 — 9-1·9-2 복습 및 오류 분류 설명
- 사용자 요청으로 9-1은 필요한 재료를 갖춘 오프라인 빌드·기동, 9-2는 완성 이미지를 파일로 포장·무결성 확인·별도 엔진에 복원·실행하는 과정으로 설명했다. dind는 고객사 서버를 흉내 내는 시험 장치이며 에이전트 운영의 필수 구성 요소가 아니다.
- 인터넷 준비 구간의 베이스/dind 이미지 다운로드와, network=none 시험 구간을 구분했다. 동일 엔진의 remove/load만으로는 기존 레이어·캐시가 남을 수 있어 images=0인 별도 엔진에서도 검증한 이유를 설명했다.
- No such image는 준비 이미지 부재, pip/Docker pull의 네트워크 실패는 의도된 비교 결과, /tmp 파일 조회 실패는 실제 해결한 환경 문제, ID 차이는 서로 다른 해시 대상의 표시로 구분했다. pip root 경고는 빌드 단계와 런타임 UID를 구분해 설명한다.
- /tmp 문제는 가이드가 /agent.tar를 사용한 것과 달리 Codex가 반입 파일·해시 검증 경로를 /tmp로 변경한 안내에서 발생했다. 사용자 명령 오입력으로 돌리지 않는다. 내부 /tmp의 tmpfs 확인 및 /day09-import 경로 변경 후 성공은 검증됐으나 docker cp의 내부 쓰기 위치까지 추적한 것은 아니라는 범위를 유지한다.
- 최종 결과는 네트워크 없는 별도 엔진에서 패키지 로딩·앱 기동·healthz 성공이며 실제 고객사 승인이나 모든 DB/LLM 통합 검증까지 뜻하지 않는다. 9-1·9-2 완료를 유지하고 9-3은 시작하지 않았다. 이번 턴은 기록 대조·설명이며 Ubuntu 재실행은 없다.

### 2026-10-03 — 9-3 시작·레지스트리 사전 점검 안내
- 사용자 요청: "좋아 9-3으로가자". 최신 진행·환경·Day 9 README/SESSION 및 가이드 9-3·compose.yaml을 확인했다. 이번 범위는 레지스트리와 UI 기동·agent 및 진단 이미지 push·API/UI 확인·레지스트리에서 pull 후 앱 실행이며 실제 Harbor 설치나 9-4 스캔은 포함하지 않는다.
- Windows compose.yaml의 SHA-256은 7059c4fbd51eedfa6a349640aa7f3197078d1c9b8592c005a6f37c6e58a4025c다. registry:2.8.3과 joxit/docker-registry-ui:2.5.7, 호스트 127.0.0.1의 5000·8082 게시, regdata 볼륨을 사용한다. Windows 파일은 수정하지 않았다.
- Codex 직접 Windows 포트 조회: 샌드박스의 Get-NetTCPConnection은 액세스 거부였고 권한 승인 경로로 다시 실행해 종료 코드 0·해당 출력 행 없음으로 5000·8082·8000의 현재 TCP Listen 항목 부재를 확인했다. 포트 예약 전체 또는 향후 기동 성공까지 보장하는 것은 아니다. Ubuntu 명령은 실행하지 않았다.
- 사용자 Ubuntu /home/user/onprem-lab/day09에서 아래 읽기 전용 사전 점검을 안내했다. cd가 실패하면 중단한다. 명령별로 결과를 확인하며 이미지 미존재 오류는 준비 항목을 구분하는 근거다.

```bash
cd /home/user/onprem-lab/day09
sha256sum compose.yaml
docker compose -p day09 config -q && echo 'Compose 설정 정상'
docker image inspect registry:2.8.3 joxit/docker-registry-ui:2.5.7 \
  nicolaka/netshoot:v0.13 agent:0.2.0-offline \
  --format '{{json .RepoTags}} {{.Os}}/{{.Architecture}}'
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker volume ls --filter 'name=^day09_regdata$'
```

- 이미지 보유 상태·Compose 파일 일치와 설정 유효성, 기존 컨테이너/포트 매핑과 레지스트리 저장소 존재를 확인한 뒤 다음 단계를 안내한다. 기존 regdata가 있으면 새 빈 저장소로 가정하거나 삭제하지 않는다.
- 흐름은 반입 이미지를 사내 창고에 push하고 배포 서버에서 pull해 실행하는 것이다. 여기서는 실제 Harbor 대신 가벼운 registry와 UI로 재현한다. 실제 기업 환경의 인증·CA·스캔 정책은 이 실습 구성과 구분한다.
- 사전 점검 결과 대기 중이며 레지스트리 기동·이미지 다운로드·push·9-3 완료는 아직 아니다. 파일 동기화·기존 자원 삭제·Git 커밋·push·9-4 진행은 없다.

### 2026-10-03 — 9-3 사전 점검 확인·레지스트리 기동 안내
- 사용자 Ubuntu 출력의 compose.yaml 해시 7059c4fbd51eedfa6a349640aa7f3197078d1c9b8592c005a6f37c6e58a4025c가 Windows와 일치하고 Compose config -q가 성공했다. registry:2.8.3·joxit/docker-registry-ui:2.5.7·nicolaka/netshoot:v0.13·agent:0.2.0-offline은 모두 로컬에 linux/amd64로 존재한다. [사전 점검 증거](evidence/93-precheck-user-2026-10-03.txt).
- 기존 컨테이너 8개는 모두 Exited다. pub2는 8081 게시 설정이 남아 있지만 실행 중은 아니며 이번 대상 포트도 아니다. day09_regdata 정확한 이름 필터는 헤더만 표시해 기존 레지스트리 볼륨 부재를 확인했다. 다른 Day 및 koica 자원은 변경하지 않는다.
- 사용자 Ubuntu /home/user/onprem-lab/day09에서 아래 명령을 안내했다. 로컬 이미지만 사용해 registry·registry-ui를 기동하고 상태·레지스트리 API·UI HTTP 응답을 확인한다.

```bash
docker compose -p day09 up -d --pull never registry registry-ui &&
sleep 3 &&
docker compose -p day09 ps &&
curl --noproxy '*' -fsS -m 10 -w '\nRegistry HTTP=%{http_code}\n' http://localhost:5000/v2/ &&
curl --noproxy '*' -fsS -m 10 -w '\n' http://localhost:5000/v2/_catalog &&
curl --noproxy '*' -fsS -m 10 -o /dev/null -w 'UI HTTP=%{http_code}\n' http://localhost:8082/
```

- 신규 생성 예상 자원은 day09-registry-1·day09-registry-ui-1, day09_default 네트워크, day09_regdata 볼륨이다. 실제 결과로 확인한다. 3초 대기는 응답 성공을 보장하지 않으며 오류가 발생하면 출력으로 진단한다.
- 기대값은 두 서비스 Up, 127.0.0.1:5000·8082 게시, /v2/의 {}·HTTP 200, catalog의 빈 repositories, UI HTTP 200이다. curl UI 200은 HTML 응답 확인이며 브라우저의 목록·다이제스트 화면 관찰은 이후 단계다.
- 안내만 했으며 기동·볼륨 생성·HTTP 성공 결과는 아직 받지 않았다. agent/netshoot push·9-3 완료·9-4 진행 및 Codex 직접 Ubuntu 실행은 없다.

### 2026-10-03 — 레지스트리 기동 확인·agent 및 netshoot push 안내
- 사용자 출력으로 day09_default 네트워크·day09_regdata 볼륨 생성과 registry·registry-ui 컨테이너 Started를 확인했다. 두 서비스는 Up 3 seconds이며 각각 127.0.0.1:5000과 127.0.0.1:8082를 게시한다. [기동 증거](evidence/93-startup-user-2026-10-03.txt).
- /v2/는 {}·HTTP 200, /v2/_catalog는 {"repositories":[]}, UI는 HTTP 200을 반환했다. 빈 레지스트리와 웹 서버 응답을 확인했으며 브라우저 화면 내용 관찰은 아직 아니다.
- 다음 명령을 사용자 Ubuntu /home/user/onprem-lab/day09에서 안내했다. 기존 두 이미지에 사내 레지스트리 주소 형식의 태그를 추가한 뒤 localhost:5000으로 push한다. 원본 태그는 유지한다.

```bash
docker tag agent:0.2.0-offline localhost:5000/ax/agent:0.2.0 &&
docker push localhost:5000/ax/agent:0.2.0 &&
docker tag nicolaka/netshoot:v0.13 localhost:5000/tools/netshoot:v0.13 &&
docker push localhost:5000/tools/netshoot:v0.13
```

- tag는 같은 이미지에 이름을 추가하는 것이며 재빌드가 아니다. push는 레지스트리에 이미지 내용을 업로드한다. ax/agent는 앱 저장소, tools/netshoot는 폐쇄망 진단에 사용할 도구 저장소다.
- 실제 push 결과의 digest를 다음 API/UI 조회와 대조한다. 저장소는 앞선 조회에서 비어 있었으며 원격 기존 태그 덮어쓰기 대상은 없었다. 명령은 안내만 했고 결과 대기 중이다. 레지스트리 컨테이너·네트워크·regdata는 유지한다.
- push 성공·API/UI 다이제스트 확인·pull 실행·9-3 완료·9-4 진행 및 Codex 직접 Ubuntu 실행은 아직 없다.

### 2026-10-03 — 두 이미지 push 성공·API 조회 안내
- 사용자 Ubuntu 출력으로 localhost:5000/ax/agent:0.2.0 및 localhost:5000/tools/netshoot:v0.13의 push 성공을 확인했다. [주요 출력](evidence/93-push-user-2026-10-03.txt). 복사된 대화의 줄 끝 이스케이프는 증거 요약에서 제외했다.
- agent의 push digest는 sha256:4c10e5ca549f993cb5d5271e24bb4ff28ae6426f3fd91a5f52b7172796dcf812, netshoot는 sha256:5a21d467fed653554bdc483ca5e7e866805c5b4c8f7ecb195a43f778c8d02fb8이다.
- netshoot는 전체 멀티플랫폼 콘텐츠 대신 로컬에 있는 단일 플랫폼 이미지만 push했다는 안내를 출력했다. 앞선 inspect에서 linux/amd64를 확인했으며 이번 amd64 실습 범위에 맞는다. 원본 멀티플랫폼 digest a20c253...과 실제 업로드 digest 5a21d46...의 차이를 오류로 처리하지 않는다. Mounted from ax/agent는 공유 레이어 재사용 출력이다.
- 다음 명령은 사용자 Ubuntu /home/user/onprem-lab/day09에서 실행하도록 안내한 것이며 API 결과는 아직 받지 않았다.

```bash
accept='application/vnd.oci.image.index.v1+json, application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.list.v2+json, application/vnd.docker.distribution.manifest.v2+json'

curl --noproxy '*' -fsS -m 10 -w '\n' http://localhost:5000/v2/_catalog &&
curl --noproxy '*' -fsS -m 10 -w '\n' http://localhost:5000/v2/ax/agent/tags/list &&
curl --noproxy '*' -fsS -m 10 -w '\n' http://localhost:5000/v2/tools/netshoot/tags/list &&
curl --noproxy '*' -fsSI -m 10 -H "Accept: $accept" http://localhost:5000/v2/ax/agent/manifests/0.2.0 &&
curl --noproxy '*' -fsSI -m 10 -H "Accept: $accept" http://localhost:5000/v2/tools/netshoot/manifests/v0.13
```

- 저장소 두 개·각 태그와 Docker-Content-Digest를 실제 push 출력에 대조할 예정이다. UI 관찰·로컬 태그 제거 후 pull 실행·9-3 완료는 아직 아니다. 레지스트리 자원과 이미지·반입 파일을 유지한다. Codex는 Windows 기록만 갱신했으며 Ubuntu 실행·9-4 진행은 없다.

### 2026-10-03 — API 검증 성공·브라우저 UI 관찰 안내
- 사용자 출력에서 catalog의 ax/agent·tools/netshoot, 각 태그 0.2.0·v0.13과 두 manifest HEAD의 HTTP 200을 확인했다. 두 Docker-Content-Digest 전체 값은 앞선 push와 정확히 일치한다. [API 증거](evidence/93-api-user-2026-10-03.txt).
- agent 응답은 OCI image index·856바이트, netshoot 응답은 OCI image manifest·3156바이트다. Content-Length는 해당 메타데이터 크기이며 이미지 전체 용량이 아니다.
- 다음은 사용자 Windows 브라우저에서 http://localhost:8082 접속, 저장소 목록의 두 항목과 ax/agent의 0.2.0 태그 상세에서 Content Digest·크기·플랫폼 표시를 관찰하는 단계다. 표시된 digest를 그대로 받아 비교하며 index digest와 하위 manifest digest를 혼동하지 않는다.
- UI 화면 또는 표시 텍스트 결과 대기 중이다. API 응답 성공만으로 UI 관찰 완료로 기록하지 않는다. 이후 레지스트리 pull·앱 실행 시험이 남아 있으며 9-3 완료·9-4 진행·자원 삭제는 없다. Windows 기록만 갱신했다.

### 2026-10-04 — 중단 후 재개·현재 상태 점검 안내
- 사용자 요청: 중간에 작업이 중단됐으므로 현재 상태부터 확인한 뒤 이어가기. 진행·환경·README·SESSION·가이드 9-3 및 Compose 설정을 다시 읽었다.
- 마지막 확인은 10월 3일 agent·netshoot push와 API의 저장소·태그·전체 digest 일치다. 현재 컨테이너 실행 여부나 데이터 보존은 이전 출력으로 단정하지 않는다. UI 관찰 및 레지스트리 pull·앱 실행은 미확인이다.
- 사용자 Ubuntu WSL2 /home/user/onprem-lab/day09에서 아래 읽기 전용 점검을 안내한다. cd 실패 시 중단하며 각 조회 오류도 결과로 전달받는다.

```bash
cd /home/user/onprem-lab/day09
docker context show
docker info --format 'Server={{.ServerVersion}}'
docker compose -p day09 ps -a
docker volume ls --filter 'name=^day09_regdata$'
docker image inspect agent:0.2.0-offline localhost:5000/ax/agent:0.2.0 localhost:5000/tools/netshoot:v0.13 --format '{{json .RepoTags}} ID={{.Id}} {{.Os}}/{{.Architecture}}'
curl --noproxy '*' -fsS -m 10 -w '\nRegistry HTTP=%{http_code}\n' http://localhost:5000/v2/_catalog
curl --noproxy '*' -fsS -m 10 -o /dev/null -w 'UI HTTP=%{http_code}\n' http://localhost:8082/
```

- 점검 결과 대기 중이다. 컨테이너 시작·재생성·이미지 삭제·재업로드는 아직 안내하거나 실행하지 않았다. 상태를 확인한 후 필요한 복구 또는 UI 관찰로 이어가며 범위는 9-3을 유지한다. Codex 직접 Ubuntu 실행은 없다.

### 2026-10-04 — 재개 점검 확인·UI 포트 진단 안내
- [사용자 출력](evidence/93-resume-user-2026-10-04.txt)으로 default·Docker 29.8.0, 두 컨테이너 Up 2 minutes, regdata 볼륨 및 세 로컬 이미지 이름 존재를 확인했다. 레지스트리 5000 API는 HTTP 200이며 ax/agent·tools/netshoot 목록이 남아 있다. 현재 모든 레이어의 무결성을 다시 검증한 것은 아니다.
- UI는 ps에 80/tcp만 표시되고 이전의 127.0.0.1:8082->80/tcp가 보이지 않는다. localhost:8082 curl은 연결 실패·HTTP 000이다. 컨테이너 실행 상태와 호스트 포트 접속 가능 여부가 다름을 설명한다. 재시작 때문에 게시가 누락됐다고 원인을 확정하지 않는다.
- 사용자 Ubuntu의 현재 day09 폴더에서 다음 읽기 전용 조회를 안내했다. Compose의 현재 설정, 컨테이너 생성 시 포트 바인딩과 런타임 게시, UI 로그를 대조한다.

```bash
docker compose -p day09 config
docker inspect day09-registry-ui-1 --format 'STATUS={{.State.Status}} ERROR={{json .State.Error}} CONFIG_PORTS={{json .HostConfig.PortBindings}} ACTUAL_PORTS={{json .NetworkSettings.Ports}}'
docker compose -p day09 logs --tail 30 registry-ui
```

- 진단 결과 대기. 아직 UI 재생성·이미지 재업로드·볼륨 삭제는 없다. 결과에 따라 UI 복구 후 화면 관찰·pull 실행으로 이어간다. 9-3 미완료·9-4 미진행을 유지한다.

### 2026-10-04 — UI 포트 불일치 확인·UI만 재생성 안내
- 사용자 출력에서 Compose 설정과 HostConfig.PortBindings 모두 127.0.0.1:8082→80을 지정하지만 NetworkSettings.Ports는 {"80/tcp":[]}임을 확인했다. State는 running·Error 빈 문자열이며 마지막 30줄은 nginx worker 시작 notice다. [진단 증거](evidence/93-ui-ports-user-2026-10-04.txt).
- 포트 설정과 실제 게시 불일치까지 확인한 상태다. Docker Desktop/엔진 재시작 시 특정 버그가 발생했다고 단정하지 않는다. 설정 파일 수정 없이 UI 컨테이너만 재생성해 게시를 다시 적용하도록 안내한다.
- 사용자 Ubuntu /home/user/onprem-lab/day09 실행 안내:

```bash
docker compose -p day09 up -d --no-deps --force-recreate --pull never registry-ui &&
sleep 3 &&
docker compose -p day09 ps &&
docker inspect day09-registry-ui-1 --format 'CONFIG_PORTS={{json .HostConfig.PortBindings}} ACTUAL_PORTS={{json .NetworkSettings.Ports}}' &&
curl --noproxy '*' -fsS -m 10 -o /dev/null -w 'UI HTTP=%{http_code}\n' http://localhost:8082/ &&
curl --noproxy '*' -fsS -m 10 -w '\nRegistry HTTP=%{http_code}\n' http://localhost:5000/v2/_catalog
```

- --no-deps로 registry를 재생성하지 않고 --pull never로 로컬 UI 이미지를 사용한다. registry의 regdata 볼륨은 유지한다. UI 복구 결과는 아직 받지 않았으며 이후 브라우저 관찰·pull 실행이 남아 있다. Codex 직접 Ubuntu 실행·9-4 진행은 없다.

### 2026-10-04 — UI 재생성의 포트 게시 실패·호스트 진단 안내
- [사용자 오류 출력](evidence/93-ui-recreate-error-user-2026-10-04.txt): UI 시작 중 ports are not available, 127.0.0.1:8082, /forwards/expose returned unexpected status: 500. 첫 명령 실패로 && 뒤 상태·HTTP 조회는 실행되지 않았다. UI 복구 성공으로 기록하지 않는다.
- 이는 Docker Desktop의 포트 게시 요청 실패이며 UI 웹 서버가 반환한 HTTP 500이 아니다. 구체적인 원인은 미확정이다. Windows 포트 점유·제외 범위와 Docker Desktop 전달 기능 문제를 구분할 증거를 수집한다.
- 공식 문서 https://docs.docker.com/desktop/features/networking/ 에서 Windows/WSL2의 호스트 포트 수신·전달을 Docker Desktop backend가 담당함을 확인했다. 문서는 이번 오류의 특정 원인을 입증하지 않는다.
- 다음 읽기 전용 명령을 사용자에게 안내하며 결과 대기 중이다.

Windows PowerShell:
```powershell
Get-NetTCPConnection |
  Where-Object { $_.LocalPort -eq 8082 } |
  Format-Table LocalAddress,LocalPort,State,OwningProcess -AutoSize
netsh interface ipv4 show excludedportrange protocol=tcp
netsh interface ipv6 show excludedportrange protocol=tcp
```

Ubuntu WSL2 /home/user/onprem-lab/day09:
```bash
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
curl --noproxy '*' -fsS -m 10 -w '\nRegistry HTTP=%{http_code}\n' http://localhost:5000/v2/_catalog
```

- 점유 프로세스 종료·포트 제외 삭제·Docker Desktop 전체 재시작·포트 변경은 아직 시행하지 않는다. UI 재생성 이후 현재 registry 응답도 별도로 재확인한다. 9-3 미완료·9-4 미진행이며 Codex 직접 Ubuntu 실행은 없다.

### 2026-10-04 — 재생성 실패 후 Ubuntu 상태 확인·Windows 결과 대기
- 사용자 docker ps -a 출력으로 day09-registry-ui-1은 Created, day09-registry-1은 Up 8 minutes·127.0.0.1:5000->5000/tcp임을 확인했다. 다른 기존 컨테이너 8개는 Exited이며 해당 출력에서 실행 중인 다른 컨테이너의 8082 게시는 없다.
- 사용자 curl 출력은 {"repositories":["ax/agent","tools/netshoot"]}·Registry HTTP=200이다. UI는 생성됐으나 시작하지 못했고 레지스트리 API와 저장소 목록은 유지됐다. 전체 이미지 레이어 검증을 의미하지 않는다.
- 앞서 안내한 Windows PowerShell의 Get-NetTCPConnection(로컬 8082)과 IPv4/IPv6 excludedportrange 결과는 아직 받지 않았다. 같은 조회 명령을 다시 안내하며 Windows 점유·예약·Docker Desktop 전달 문제 중 원인은 미확정이다. 추가 복구 명령 실행은 없다.

### 2026-10-04 — PowerShell 명령을 Ubuntu에서 실행한 오류
- 사용자 프롬프트는 user@DESKTOP-6KJVBND:~/onprem-lab/day09$이며 Get-NetTCPConnection·Where-Object·Format-Table·netsh가 command not found로 끝났다. Windows PowerShell용 명령을 Ubuntu Bash에서 실행한 셸 불일치다. 이 결과로 Windows 포트 점유·제외 범위를 판단할 수 없다.
- Windows 시작 메뉴에서 PowerShell을 열고 PS C:\...> 프롬프트를 확인한 뒤 기존 세 조회를 실행하도록 안내한다. 패키지 설치나 자원 변경은 필요하지 않다. Windows 결과 대기와 9-3 미완료 상태를 유지한다.

### 2026-10-04 — Windows 제외 범위 확인·대안 포트 점검 안내
- [사용자 Windows 출력](evidence/93-windows-ports-user-2026-10-04.txt)에서 로컬 8082 TCP 조회는 행·오류가 없으며 IPv4와 IPv6 모두 7987–8086을 제외 범위로 표시했다. 8082 포함을 확인했으며 UI 게시 실패의 유력한 원인으로 판단한다. 예약 생성 주체와 시점, 중단 전후 변경 경위는 확인하지 않았다.
- 대안 포트 18082는 제공된 제외 범위에 포함되지 않는다. 현재 Windows PowerShell에서 아래 점유 조회를 안내했으며 결과 대기 중이다.

```powershell
$uiPortCheck = @(Get-NetTCPConnection -ErrorAction Stop | Where-Object { $_.LocalPort -eq 18082 })
if ($uiPortCheck.Count -eq 0) {
  '18082: 현재 TCP 사용 항목 없음'
} else {
  $uiPortCheck | Format-Table LocalAddress,LocalPort,State,OwningProcess -AutoSize
}
```

- 사용 가능 확인 후 UI 게시를 127.0.0.1:18082:80으로, registry의 CORS 허용 Origin을 http://localhost:18082로 함께 변경할 예정이다. registry API의 5000은 유지한다. CORS 적용에는 registry 서비스 갱신도 필요하며 regdata 볼륨은 보존한다. Windows·Ubuntu 사본을 별도로 다룬다.
- 이번 턴에는 포트 조회만 안내했고 Compose 수정·컨테이너 재생성·Windows 예약 해제는 없다. 복구 후 UI 관찰·pull 실행을 이어가며 9-4는 미진행이다.

### 2026-10-04 — 18082 점유 없음·Compose 변경 및 복구 안내
- 사용자 Windows PowerShell 출력: "18082: 현재 TCP 사용 항목 없음". 이전 제외 범위에도 18082는 없지만 실제 바인딩 성공은 이후 실행으로 확인한다.
- Codex는 Windows day09/compose.yaml에서 UI 게시를 127.0.0.1:18082:80, registry CORS Origin을 http://localhost:18082로 수정했다. diff에서 두 줄만 바뀜을 확인했다. Windows 파일 SHA-256: a9b2ef288660930816cc97d63b37eef06b828ac7ed653df8848d0cb3b59f8282. Ubuntu 사본은 별도이며 자동 반영하지 않았다.
- 사용자 Ubuntu WSL2에서 아래 명령을 안내한다. sed는 지정한 두 문자열만 변경하며 config 검증 성공 후 서비스를 재생성한다. registry 환경 변수 변경 적용을 위해 이번에는 두 서비스가 재생성 대상이고 regdata 볼륨은 그대로 연결한다.

```bash
cd /home/user/onprem-lab/day09 &&
sed -i \
  -e 's|http://localhost:8082|http://localhost:18082|g' \
  -e 's|127.0.0.1:8082:80|127.0.0.1:18082:80|g' compose.yaml &&
docker compose -p day09 config -q &&
sha256sum compose.yaml &&
docker compose -p day09 up -d --force-recreate --pull never registry registry-ui &&
sleep 3 &&
docker compose -p day09 ps &&
curl --noproxy '*' -fsS -m 10 -o /dev/null -w 'UI HTTP=%{http_code}\n' http://localhost:18082/ &&
curl --noproxy '*' -fsS -m 10 -D - \
  -H 'Origin: http://localhost:18082' \
  -w '\nRegistry HTTP=%{http_code}\n' http://localhost:5000/v2/_catalog
```

- 기대값: UI 18082 게시·HTTP 200, registry HTTP 200·저장소 두 개 유지·Access-Control-Allow-Origin: http://localhost:18082. 실제 결과는 대기 중이다. Windows 변경은 두 줄 diff와 git diff --check로 검사하며 Docker Compose 실행 검증은 사용자 Ubuntu 결과로 확인한다. UI 화면 관찰·pull 실행 및 9-3 완료는 아직 아니다.

### 2026-10-04 — 18082 복구 성공·브라우저 UI 확인 재개
- [사용자 복구 출력](evidence/93-ui-recovery-user-2026-10-04.txt): Ubuntu compose.yaml 해시가 Windows 수정본 a9b2ef288660930816cc97d63b37eef06b828ac7ed653df8848d0cb3b59f8282와 일치하며 config 검증 후 두 서비스 Started·Up 3 seconds를 확인했다.
- registry는 127.0.0.1:5000, UI는 127.0.0.1:18082를 게시한다. UI·registry 모두 HTTP 200, CORS Origin http://localhost:18082, catalog의 ax/agent·tools/netshoot 유지를 확인했다. 기존 regdata를 연결한 서비스 재생성으로 저장소 목록이 유지됐다.
- Windows 제외 범위에 있던 8082에서 범위 밖인 18082로 변경 후 게시·HTTP가 정상화됐다. Windows 예약 생성 주체와 시점은 여전히 미확정이다. HTTP 복구와 실제 브라우저 UI 동작 확인은 구분한다.
- 다음은 사용자 Windows 브라우저 http://localhost:18082 접속, 저장소 두 개 확인 및 ax/agent → 0.2.0의 Content Digest·크기·플랫폼 표시 관찰이다. 화면이나 텍스트 결과를 기다리며 하위 manifest와 index digest가 다를 수 있으므로 표시값 그대로 대조한다. 레지스트리 pull·앱 실행·9-3 완료는 아직 아니다. 9-4는 미진행이다.

### 2026-10-04 — agent UI 태그 관찰·index와 manifest 구분
- 사용자 제공 [UI 텍스트](evidence/93-ui-observation-user-2026-10-04.txt)에서 ax/agent 저장소의 태그 1개, 0.2.0·43 MB·amd64, Content Digest sha256:0fc1da16c9e87eb64374d9df2afb60b17ebac802955e9238e6aeb441ac4323b4를 확인했다. Codex 직접 브라우저 관찰은 아니다. 전체 저장소 목록 화면은 제공되지 않았으나 두 저장소는 앞선 API로 확인됐다.
- 해당 digest가 9-1 빌드 증거의 exporting manifest와 정확히 일치함을 직접 대조했다. push/API HEAD의 4c10e5ca...는 OCI index다. 상위 index와 하위 플랫폼 manifest는 해시 대상이 다르므로 값 차이만으로 이미지 변경을 판단하지 않는다. OCI 공식 규격 https://github.com/opencontainers/image-spec/blob/main/image-index.md 에서 index가 플랫폼별 manifest를 참조함을 확인했다.
- 사용자 Ubuntu에서 다음 읽기 전용 조회를 안내한다. JSON의 manifests 중 linux/amd64 descriptor가 UI의 0fc1da16...를 가리키는지 확인할 예정이다.

```bash
curl --noproxy '*' -fsS -m 10 \
  -H 'Accept: application/vnd.oci.image.index.v1+json' \
  http://localhost:5000/v2/ax/agent/manifests/0.2.0 |
  python3 -m json.tool
```

- index 본문 결과는 대기 중이며 로컬 태그 제거·pull·앱 실행은 아직 안내하지 않았다. 향후 실행 검증 시 Windows 제외 범위에 포함되는 기존 가이드 8000 게시도 피해야 한다. 명시적 pull 후 network none 컨테이너에서 docker exec로 healthz를 조회하는 방식 등을 사용할 수 있다. 9-3 미완료·9-4 미진행을 유지한다.

### 2026-10-04 — index 연결 확인·사내 레지스트리 pull 안내
- [사용자 index 출력](evidence/93-index-user-2026-10-04.txt)의 linux/amd64 descriptor가 UI 및 원본 빌드와 동일한 sha256:0fc1da16c9e87eb64374d9df2afb60b17ebac802955e9238e6aeb441ac4323b4를 참조한다. 두 번째 e32ef14d...는 attestation-manifest로 표시되며 같은 manifest를 reference.digest로 참조한다.
- unknown/unknown은 실행 플랫폼을 추가하는 항목이 아니라 attestation에 쓰이는 표시다. Docker 공식 설명 https://docs.docker.com/build/metadata/attestations/attestation-storage/ 에서 확인했다. 실제 attestation 본문은 조회하지 않았으므로 SBOM 생성 완료나 서명 검증으로 기록하지 않는다.
- 다음 사용자 Ubuntu /home/user/onprem-lab/day09 명령을 안내했다. 기존 반입 파일 해시 확인이 성공해야 로컬 태그 두 개를 제거한다. 강제 삭제하지 않으며 사용 중 오류가 나면 중단된다. 레지스트리 저장본·반입 파일은 삭제하지 않는다.

```bash
sha256sum -c agent-0.2.0-offline.sha256 &&
docker image rm localhost:5000/ax/agent:0.2.0 agent:0.2.0-offline &&
docker image ls localhost:5000/ax/agent:0.2.0 &&
docker image ls agent:0.2.0-offline &&
docker pull --platform linux/amd64 localhost:5000/ax/agent:0.2.0 &&
docker image inspect localhost:5000/ax/agent:0.2.0 \
  --format 'ID={{.Id}} OS={{.Os}} ARCH={{.Architecture}} USER={{.Config.User}} DIGESTS={{json .RepoDigests}}'
```

- pull 결과와 저장소 digest·linux/amd64·USER=10001을 확인한 뒤 앱 실행으로 이어간다. 기존 레이어·빌드 캐시가 남을 수 있으므로 모든 바이트를 새로 내려받는 시험이라고 표현하지 않는다. 명령은 아직 안내만 했으며 태그 제거·pull 성공·9-3 완료는 미확인이다. 9-4는 미진행이다.

### 2026-10-04 — 사내 레지스트리 pull 성공·앱 실행 안내
- [사용자 pull 출력](evidence/93-pull-user-2026-10-04.txt)에서 반입 파일 해시 OK, 로컬 태그 두 개 제거·목록 부재, localhost:5000/ax/agent:0.2.0 pull 성공을 확인했다. index digest 4c10e5ca...의 전체 값이 이전 push/API와 일치하며 linux/amd64·USER=10001, RepoDigests의 로컬 레지스트리 주소를 확인했다.
- 일부 레이어 Already exists가 보이므로 완전히 빈 엔진의 다운로드라고 해석하지 않는다. 현재 로컬 이미지에는 registry 태그가 있으며 agent:0.2.0-offline 태그는 제거된 상태다. 실행 시험 후 정리 단계에서 같은 이미지에 원래 태그를 다시 추가할 예정이다.
- 사용자 Ubuntu /home/user/onprem-lab/day09에서 다음 실행 검증을 안내한다. Windows 제외 범위에 8000도 포함되므로 가이드의 호스트 8000 게시 대신 포트 없이 --network none으로 실행하고 내부 loopback의 healthz를 조회한다. --pull=never로 방금 받은 로컬 이미지를 사용한다.

```bash
docker run -d --pull=never --platform linux/amd64 --network none \
  --name from-reg localhost:5000/ax/agent:0.2.0 &&
sleep 2 &&
docker inspect from-reg \
  --format 'STATUS={{.State.Status}} IMAGE={{.Config.Image}} NETWORK={{.HostConfig.NetworkMode}}' &&
docker exec from-reg python -c '
import os, urllib.request, yaml
print("UID=", os.getuid(), "GID=", os.getgid())
print("PyYAML=", yaml.__version__)
print(urllib.request.urlopen("http://127.0.0.1:8000/healthz", timeout=5).read().decode())
'
```

- 기대값은 running·사내 레지스트리 이미지 이름·NETWORK=none·UID=10001·GID=0·PyYAML=6.0.2·healthz status=ok 및 version=0.2.0이다. 실행 결과를 받은 뒤 시험 컨테이너만 정리하며 registry·UI·regdata는 다음 학습을 위해 유지한다. 아직 앱 실행·9-3 완료·9-4 진행은 아니다.

### 2026-10-04 — 사내 레지스트리 이미지 실행 성공·시험 정리 안내
- [사용자 실행 출력](evidence/93-runtime-user-2026-10-04.txt)에서 from-reg(d629057921c9)의 running·IMAGE=localhost:5000/ax/agent:0.2.0·NETWORK=none을 확인했다. 실제 UID=10001·GID=0·PyYAML=6.0.2이며 내부 healthz는 status=ok·version=0.2.0·host=d629057921c9를 반환했다.
- 반입 이미지 push → API/UI 확인 → 로컬 태그 제거 → 사내 레지스트리 pull → 앱 실행까지 사용자 출력으로 검증했다. 실제 고객사 Harbor 인증·CA·정책이나 외부 DB/LLM 연결 시험은 포함하지 않는다.
- 다음 사용자 Ubuntu /home/user/onprem-lab/day09 정리 명령을 안내한다. from-reg만 제거하며 registry·UI·regdata는 유지한다. 받아온 동일 이미지에 원래 agent:0.2.0-offline 태그를 다시 추가해 앞선 실습 산출물 이름을 복원한다. 재빌드는 없다.

```bash
docker rm -f from-reg &&
docker tag localhost:5000/ax/agent:0.2.0 agent:0.2.0-offline &&
docker ps -a --filter 'name=^/from-reg$' --format 'table {{.Names}}\t{{.Status}}' &&
docker image inspect agent:0.2.0-offline \
  --format 'TAGS={{json .RepoTags}} ID={{.Id}}' &&
sha256sum -c agent-0.2.0-offline.sha256 &&
docker compose -p day09 ps
```

- 정리·태그 복원·반입 파일 해시 OK·레지스트리 두 서비스 유지 결과 대기 중이다. 9-3 실행 검증 성공과 최종 정리 완료를 구분한다. 사용자 출력 후 9-3 완료로 갱신하며 9-4는 요청 전 진행하지 않는다. Codex 직접 Ubuntu 실행은 없다.

### 2026-10-05 — 시험 정리·태그 복원 확인 및 9-3 완료
- [사용자 정리 출력](evidence/93-cleanup-user-2026-10-05.txt)에서 from-reg 제거와 정확한 이름 조회의 헤더만 남음을 확인했다. agent:0.2.0-offline·localhost:5000/ax/agent:0.2.0 두 태그가 같은 ID sha256:4c10e5ca549f993cb5d5271e24bb4ff28ae6426f3fd91a5f52b7172796dcf812를 가리킨다. 반입 tar.gz의 sha256sum -c 결과는 OK다.
- registry·registry-ui는 Up 4 hours이며 각각 127.0.0.1:5000·127.0.0.1:18082를 게시한다. 두 서비스와 regdata는 유지 대상으로 볼륨 삭제를 실행하지 않았다. 이번 출력으로 별도 볼륨 상태를 재검사한 것으로 기록하지 않는다.
- 9-3 완료: 가벼운 registry와 UI로 사내 레지스트리를 재현하고 agent·netshoot push, API 저장소·태그·digest 확인, agent UI 43 MB·amd64 관찰 및 상위 index/하위 manifest 연결 확인, 로컬 태그 제거 후 pull·동일 digest 확인, 네트워크 없는 앱 실행·healthz ok·UID 10001·PyYAML 6.0.2, 시험 컨테이너 제거·태그 복원까지 검증했다.
- 오류 해결: Windows 제외 범위 7987–8086에 포함된 UI 8082 대신 18082로 게시하고 CORS Origin도 변경해 복구했다. Windows·Ubuntu Compose 해시 일치를 확인했다. 예약 생성 주체·시점은 미확정이며 호스트 8000도 같은 범위라 앱 실행은 내부 loopback으로 검증했다.
- 범위 한계: 실제 Harbor 설치·인증·CA·권한·스캔 정책, 외부 DB/LLM 연결 및 9-4 스캔/SBOM 실습은 수행하지 않았다. index에 attestation이 있다는 것만으로 SBOM 실습 완료로 간주하지 않는다.
- Windows SESSION·PROGRESS·README·환경 기록을 갱신했다. 사용자 제공 결과이며 Codex 직접 Ubuntu 실행은 없다. 전체 사본 동기화·Git 커밋·push는 하지 않았다. 9-1~9-3 완료, Day 9 전체는 미완료이며 다음은 사용자 요청 후 9-4다.

### 2026-10-05 — 9-4 시작·사전 점검 안내
- 사용자 요청: "그럼 9-4로가자". PROGRESS·환경·Day 9 README/SESSION·가이드 9-4 및 .gitignore를 읽었다. 9-1~9-3 완료를 유지하며 범위는 9-4 취약점 스캔·CycloneDX SBOM 생성까지다. 9-5 신청서는 시작하지 않는다.
- 가이드의 aquasec/trivy:0.56.2를 기준으로 준비한다. Day 3에 사용한 기록은 있으나 현재 로컬 존재 여부는 별도로 확인한다. 공식 v0.56 문서 https://trivy.dev/docs/v0.56/advanced/air-gap/ 와 https://trivy.dev/docs/v0.56/supply-chain/sbom/ 에서 오프라인 플래그와 CycloneDX 지원을 확인했다.
- 가이드 ②의 --output trivy-agent-0.2.0.txt는 현재 명령상 호스트에 연결되지 않은 컨테이너 경로다. --rm 이후 보고서를 잃을 수 있으므로 실제 안내에서는 호스트 출력 폴더 마운트와 명시적인 출력 경로를 사용한다. 가이드의 취약점 44건·구성 요소 90개·DB 용량은 예시이며 이번 실제 결과를 별도로 기록한다.
- 먼저 사용자 Ubuntu WSL2에서 아래 읽기 전용 점검을 안내한다. cd 실패 시 중단한다. 이미지 부재 오류나 파일 존재 결과를 받아 다운로드·출력 경로를 결정한다.

```bash
cd /home/user/onprem-lab/day09
docker info --format 'Server={{.ServerVersion}}'
docker image inspect aquasec/trivy:0.56.2 localhost:5000/ax/agent:0.2.0 \
  --format '{{json .RepoTags}} ID={{.Id}} {{.Os}}/{{.Architecture}}'
df -h .
for path in trivy-cache trivy-agent-0.2.0.txt sbom-agent-0.2.0.cdx.json; do
  if [ -e "$path" ]; then
    ls -ld -- "$path"
  else
    printf '없음: %s\n' "$path"
  fi
done
```

- 사용자 결과 대기 중이다. DB 다운로드·캐시 생성·스캔·SBOM 생성이나 Codex 직접 Ubuntu 실행은 아직 없다. 이후 스캔 단계에는 DB 갱신 중지·오프라인 조회 설정·network none을 적용하며 보고서를 호스트에 보존한다. registry·UI·regdata 및 이미지·반입 파일은 유지한다.

### 2026-10-05 — 사전 점검 확인·취약점 DB 다운로드 안내
- [사용자 사전 점검](evidence/94-precheck-user-2026-10-05.txt)에서 Docker 29.8.0, aquasec/trivy:0.56.2 및 대상 agent 이미지의 linux/amd64 존재를 확인했다. Trivy ID는 26245f36...이며 대상 ID 4c10e5ca...는 이전 검증과 일치한다. Ubuntu df는 /dev/sde의 가용 공간 952G를 표시했다. Windows 물리 디스크 여유량을 직접 검증한 것은 아니다.
- day09/trivy-cache·trivy-agent-0.2.0.txt·sbom-agent-0.2.0.cdx.json은 없었다. 이번에는 DB 준비만 진행하며 스캔은 다음 단계다. 공식 DB-only 옵션은 https://trivy.dev/docs/v0.56/configuration/db/ 에서 확인했다.
- 사용자 Ubuntu /home/user/onprem-lab/day09에서 아래 명령을 안내한다. 로컬 Trivy 이미지로 인터넷에 연결해 DB를 받고, 캐시는 호스트 사용자 UID/GID로 생성한다. Docker 소켓 마운트는 이 단계에 필요 없다.

```bash
mkdir -p trivy-cache &&
docker run --rm --pull=never --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/trivy-cache:/cache" \
  aquasec/trivy:0.56.2 image \
  --cache-dir /cache/trivy --download-db-only &&
du -sh trivy-cache &&
ls -lh trivy-cache/trivy/db/ &&
python3 -m json.tool trivy-cache/trivy/db/metadata.json
```

- 컨테이너의 /cache/trivy가 Ubuntu day09/trivy-cache/trivy에 대응한다. 이후 스캔·SBOM에서도 같은 마운트와 --cache-dir를 사용해야 한다. --download-db-only는 이미지 검사 없이 DB만 준비한다. --pull=never는 Trivy 이미지 재다운로드를 막고 DB 네트워크 통신은 허용한다.
- 다운로드·DB 파일 존재·메타데이터 결과 대기 중이다. 메타데이터의 갱신 시각과 실제 크기를 확인한 후 오프라인 스캔을 안내한다. DB 크기와 취약점 개수를 가이드 예시와 같다고 가정하지 않는다. Codex 직접 Ubuntu 실행·9-4 완료·9-5 진행은 없다.

### 2026-10-05 — DB 준비 확인·오프라인 취약점 스캔 안내
- 사용자 첨부 텍스트를 직접 읽고 [DB 증거 요약](evidence/94-db-user-2026-10-05.txt)을 저장했다. ghcr.io/aquasecurity/trivy-db:2의 121.00 MiB 전송·Artifact successfully downloaded, 캐시 1.4G, user:user 소유 trivy.db와 metadata.json을 확인했다. 가이드 예시와 별도로 실제 표시값을 기록했다.
- metadata Version=2, UpdatedAt=2026-10-04T14:28:15.152965452Z, DownloadedAt=2026-10-04T15:36:41.35690486Z, NextUpdate=2026-10-05T14:28:15.15296468Z다. 한국 시각 다운로드는 10월 5일 00:36:41이다. Version 2는 DB 형식 버전이며 Trivy 실행 버전과 구분한다.
- 공식 v0.56 CLI https://trivy.dev/docs/v0.56/references/configuration/cli/trivy_image/ 에서 --image-src docker·--offline-scan·DB 갱신 중지 옵션을 확인했다. 사용자 Ubuntu의 현재 day09 폴더에서 다음 스캔을 안내한다.

```bash
docker run --rm --pull=never --platform linux/amd64 --network none \
  --user "$(id -u):$(id -g)" \
  --group-add "$(stat -c '%g' /var/run/docker.sock)" -e HOME=/tmp \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$PWD/trivy-cache:/cache" \
  -v "$PWD:/out" \
  aquasec/trivy:0.56.2 image \
  --cache-dir /cache/trivy --image-src docker \
  --scanners vuln --severity HIGH,CRITICAL \
  --skip-db-update --skip-java-db-update --offline-scan \
  --format table --output /out/trivy-agent-0.2.0.txt \
  localhost:5000/ax/agent:0.2.0 &&
ls -lh trivy-agent-0.2.0.txt &&
cat trivy-agent-0.2.0.txt
```

- 동일 사용자 UID/GID와 Docker 소켓 그룹을 추가해 로컬 이미지 조회·사용자 소유 캐시/보고서 쓰기를 허용한다. localhost:5000/ax/agent:0.2.0은 로컬 태그이며 --image-src docker로 소켓의 로컬 이미지에서만 읽는다. network none은 스캐너 컨테이너 네트워크를 차단하며 Docker 엔진 전체가 격리됐다는 뜻은 아니다.
- /out은 Ubuntu day09 디렉터리에 연결돼 --rm 후에도 보고서가 남는다. 스캔은 vuln·HIGH/CRITICAL 범위이며 --ignore-unfixed는 지정하지 않는다. 성공 종료가 취약점 0건을 뜻하지 않으며 실제 보고서 개수를 확인한다. 대상 agent 앱은 실행하지 않는다.
- 명령은 안내만 했고 스캔 성공·보고서 생성은 결과 대기 중이다. SBOM 생성·9-4 완료·9-5 진행은 아직 아니다. 기존 레지스트리 자원은 유지한다.

### 2026-10-05 — 오프라인 스캔 성공·CycloneDX SBOM 생성 안내
- 사용자 첨부를 읽고 전체 명령·로그·보고서 텍스트를 [스캔 증거](evidence/94-scan-user-2026-10-05.txt)로 보존했다. network none, --image-src docker, DB 갱신 중지 및 --offline-scan 명령 뒤 ls·cat이 실행돼 스캔 성공과 호스트 출력 보존을 확인했다. 별도 echo 종료 코드 출력은 없었다.
- 대상 localhost:5000/ax/agent:0.2.0의 OS는 Debian 13.7, OS 패키지 탐지는 87개이며 Python 패키지 탐지 로그도 있다. 보고서 OS 섹션은 Total 51(HIGH 51, CRITICAL 0)이다. 파일은 user:user 소유·54K로 표시됐다. Python 취약점 별도 요약은 출력에 없으며 전체 위험 부재를 뜻하지 않는다.
- 가이드 예시 44건과 다른 실제 51건을 기록했다. 별개의 CVE 51종이라고 해석하지 않는다. libpcre2-8-0은 Installed 10.46-1~deb13u2·Fixed 10.46-1~deb13u3, OpenSSL 관련 항목은 Installed 3.5.7-1~deb13u2·Fixed 3.5.7-1~deb13u3로 표시된다. fixed 상태는 수정 버전 제공을 뜻하며 현재 이미지가 이미 수정됐다는 뜻이 아니다. 일부 항목은 Fixed Version이 비어 있다. 자동 업그레이드·재빌드는 수행하지 않는다.
- 심각도 출처 관련 경고와 Python 라이선스 관련 INFO는 있었으나 스캔 실패는 아니다. 스캔 범위는 HIGH/CRITICAL 취약점이며 실사용 영향 평가나 배포 승인을 완료한 것으로 취급하지 않는다.
- 다음은 사용자 Ubuntu의 동일 day09 폴더에서 동일 이미지의 CycloneDX SBOM을 생성하고 요약을 확인하는 명령이다. 공식 생성 방법 https://trivy.dev/docs/v0.56/supply-chain/sbom/ 을 참조했다. 취약점 필터를 적용하지 않고 구성 요소 목록을 기록한다.

```bash
docker run --rm --pull=never --platform linux/amd64 --network none \
  --user "$(id -u):$(id -g)" \
  --group-add "$(stat -c '%g' /var/run/docker.sock)" -e HOME=/tmp \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$PWD/trivy-cache:/cache" \
  -v "$PWD:/out" \
  aquasec/trivy:0.56.2 image \
  --cache-dir /cache/trivy --image-src docker \
  --skip-db-update --skip-java-db-update --offline-scan \
  --format cyclonedx --output /out/sbom-agent-0.2.0.cdx.json \
  localhost:5000/ax/agent:0.2.0 &&
ls -lh sbom-agent-0.2.0.cdx.json &&
python3 -c '
import json
with open("sbom-agent-0.2.0.cdx.json", encoding="utf-8") as f:
    d = json.load(f)
assert d.get("bomFormat") == "CycloneDX", "SBOM 형식 확인 필요"
c = d.get("components", [])
print("형식:", d["bomFormat"], "규격:", d.get("specVersion"))
print("대상:", d.get("metadata", {}).get("component", {}).get("name"))
print("구성 요소 수:", len(c))
print("Python 패키지:", [(x.get("name"), x.get("version")) for x in c if x.get("purl", "").startswith("pkg:pypi/")])
'
```

- SBOM 출력은 호스트 day09에 남기며 캐시·보고서·이미지·registry 자원을 유지한다. 사용자 생성·JSON 요약 결과 대기 중이고 SBOM 완료·9-4 완료·9-5 진행은 아직 아니다. 전체 JSON 스키마 검증은 이번 요약 검사와 구분한다.

### 2026-10-05 — SBOM 생성 확인·9-4 완료
- [사용자 SBOM 출력](evidence/94-sbom-user-2026-10-05.txt)에서 network none 생성 성공과 user:user 소유의 sbom-agent-0.2.0.cdx.json 197K 보존을 확인했다. JSON 파싱 및 bomFormat 확인 후 CycloneDX 1.6, 대상 localhost:5000/ax/agent:0.2.0, 구성 요소 90개, pip 25.0.1·PyYAML 6.0.2가 출력됐다.
- "--format cyclonedx disables security scanning"은 해당 명령이 구성 목록을 생성하며 취약점 검사 결과를 포함하지 않는다는 INFO다. 앞서 생성한 별도 취약점 보고서의 HIGH 51·CRITICAL 0 결과는 그대로 보존한다. 이번 SBOM 파일 생성이 취약점 해결을 뜻하지 않는다.
- 9-4 완료 범위: 인터넷 연결 준비 단계에서 취약점 DB v2를 다운로드하고 메타데이터·캐시 1.4G를 확인했다. 이후 두 Trivy 명령을 network none으로 실행해 취약점 보고서와 CycloneDX SBOM을 호스트 경로에 남겼다. 보고서는 54K, SBOM은 197K이며 둘 다 사용자 소유다. 검사기 임시 컨테이너는 --rm으로 실행됐고 별도의 잔존 컨테이너 목록 검사는 하지 않았다.
- 가이드 예시와 달리 취약점 결과는 HIGH 51·CRITICAL 0이며 일부 수정 버전 제공 항목이 있다. SBOM 총 구성 요소는 90개이나 출력만으로 모두를 OS 패키지/Python 패키지로 정확히 분류하지 않는다. 스캔 로그의 OS 패키지 탐지 수는 87개다. 전체 JSON 스키마 검증·패키지 완전성 검증·취약점 수정·고객사 승인 절차는 수행하지 않았다.
- 보존할 Ubuntu 산출물: trivy-cache/trivy/db/의 DB 및 metadata.json, trivy-agent-0.2.0.txt, sbom-agent-0.2.0.cdx.json. 기존 이미지·반입 tar/gzip·해시 파일·registry·UI·regdata도 삭제하지 않는다. Windows에는 학습 기록과 사용자 텍스트 증거를 저장했으며 DB와 SBOM 원본을 복사하지 않았다.
- SESSION·PROGRESS·README·환경 기록을 함께 갱신했다. 사용자 제공 실행 결과와 Codex의 기록 검사를 구분한다. 9-1~9-4 완료이며 다음은 사용자 요청 후 9-5다. 9-5·Day 9 전체 완료·Git 커밋 및 push는 아직 아니다.

### 2026-10-05 — 9-5 시작·신청서 첨부 식별 정보 확인 안내
- 사용자 요청: "9-5로 가자". PROGRESS·환경·README·SESSION, 가이드 9-5와 부록 E-4, Day 3 IMPORT-PACKAGE.md 초안, Day 9 Dockerfile.offline·app.py 관련 설정을 읽었다. 기존 초안을 Day 9 실제 이미지와 산출물로 갱신할 계획이다.
- 학습용 문서는 실제 반입 승인 문서와 구분한다. 가이드 예시의 HIGH 44·전부 패치 미제공 문구를 복사하지 않고 이번 HIGH 51·CRITICAL 0·수정 버전 제공 항목 존재를 반영한다. LLM/DB 통신과 의존 이미지 전체 반입·신청자/승인자·고객 서버 아키텍처는 실제 확인 범위에 맞게 미정 또는 조건부로 기록한다.
- 파일 SHA-256, 레지스트리 index digest 4c10e5ca..., UI linux/amd64 manifest digest 0fc1da16...를 서로 구분한다. 알려진 tar.gz 해시 cd08d49e...와 크기 42M은 기존 증거에 있지만 이번에 정확한 바이트 크기와 보고서/SBOM 해시도 확인한다.
- 다음 사용자 Ubuntu WSL2 조회를 안내했다. 기존 산출물을 읽는 명령이며 파일을 재생성하거나 이미지를 갱신하지 않는다.

```bash
cd /home/user/onprem-lab/day09 &&
sha256sum -c agent-0.2.0-offline.sha256 &&
stat -c '%n | %s bytes' \
  agent-0.2.0-offline.tar.gz trivy-agent-0.2.0.txt sbom-agent-0.2.0.cdx.json &&
sha256sum trivy-agent-0.2.0.txt sbom-agent-0.2.0.cdx.json &&
docker image inspect localhost:5000/ax/agent:0.2.0 \
  --format 'ID={{.Id}} DIGESTS={{json .RepoDigests}} OS={{.Os}} ARCH={{.Architecture}} USER={{.Config.User}} PORTS={{json .Config.ExposedPorts}}'
```

- 결과 대기 중이며 Day 9 신청서 파일은 아직 작성하지 않았다. 기존 Day 3 문서와 Ubuntu 산출물은 보존한다. 누적 점검 리허설·전체 정리·9-5 완료·실제 고객사 제출은 아직 아니다.

### 2026-10-05 — 9-5 첨부 식별 정보 확인·학습용 신청서 완료
- 사용자 Ubuntu 출력: 반입 tar.gz 체크섬 OK, 압축 파일 43,776,190 bytes·스캔 보고서 55,261 bytes·SBOM 201,644 bytes를 확인했다. 보고서 SHA-256은 94ebfe6ccc9ab5f441beb409753677470393105a431f53764dbb517c7d80e7c2, SBOM은 4c331693d41f69b03b92affdab09a01df3961d3a3d9c748a9c68f54e62109a42다. 명령과 원문은 [증거](evidence/95-artifacts-user-2026-10-05.txt)에 보관했다.
- 현재 이미지 ID·RepoDigests의 index는 기존 4c10e5ca...와 일치하고 linux/amd64·USER=10001·ExposedPorts=8000/tcp를 확인했다. 기존 압축 파일 해시 cd08d49e...는 생성 증거와 이번 체크섬 OK로 연결했다.
- Codex 작업: Day 3 형식·가이드 9-5·E-4와 실제 증거를 대조해 Windows [IMPORT-PACKAGE.md](IMPORT-PACKAGE.md)를 작성했다. 파일/이미지 식별자, 첨부 목록, DB 시점과 스캔 범위, 동반 항목, 설계 점검을 담았다. pages:write-page의 문서 작성 규칙을 참고하고 기존 저장소 형식·경로를 유지했다.
- HIGH 51·CRITICAL 0을 그대로 기록하고 수정 버전 제공 항목도 있음을 명시했다. 패치 적용·재스캔·고객사 예외 승인 완료로 표기하지 않았다. 담당자·고객 서버 아키텍처·통신 허용 목록·의존 이미지 실제 반입 여부는 미정/미확인으로 남겼다.
- 확인 구분: 사용자 실행 결과로 Ubuntu 상태를 기록했고 Codex는 Windows 문서·링크·식별자와 변경 형식을 점검했다. 실제 원본 보고서/SBOM/압축 파일을 Windows로 복사하거나 컨테이너를 실행·정리하지 않았다.
- 9-5 학습용 신청서 작성 완료, 9-1~9-5 완료로 SESSION·PROGRESS·README·환경 기록을 갱신했다. 누적 점검 2차·Day 전체 정리·체크포인트 평가·실제 고객사 제출·Git 커밋/push는 수행하지 않았다. 다음 범위는 사용자 요청 후 정한다.

### 2026-10-05 — Day 9 요약·실습 자원 정리 안내
- 사용자에게 오프라인 빌드 → 파일 반입 → 사내 레지스트리 배포 → 취약점 검사/SBOM → 신청서의 연결을 설명했다. 이후 "그럼 정리하자" 요청에 따라 진행·환경·README·SESSION·가이드 정리 절·Compose를 확인했다.
- 가이드의 일반 이름 airgap/from-reg/off 일괄 삭제는 사용하지 않는다. 이 세션에서 사용한 시험 컨테이너는 기존 출력에서 제거를 확인했다. 현재 프로젝트 day09의 Compose 자원과 압축 전 tar만 정리하도록 안내한다.
- 실행 위치: 사용자 Ubuntu WSL2 /home/user/onprem-lab/day09. 다음 명령은 제안 상태이며 Codex가 직접 실행하지 않았다.

```bash
cd /home/user/onprem-lab/day09 &&
gzip -t agent-0.2.0-offline.tar.gz &&
sha256sum -c agent-0.2.0-offline.sha256 &&
docker compose -p day09 down &&
rm -f -- agent-0.2.0-offline.tar &&
docker compose -p day09 ps -a &&
docker volume ls --filter 'name=^day09_regdata$' &&
docker image inspect agent:0.2.0-offline --format 'ID={{.Id}}' &&
ls -lh agent-0.2.0-offline.tar.gz agent-0.2.0-offline.sha256 \
  trivy-agent-0.2.0.txt sbom-agent-0.2.0.cdx.json &&
du -sh wheels trivy-cache
```

- down에는 -v/--rmi를 넣지 않는다. regdata·로컬 이미지·압축 반입 파일·체크섬·보고서·SBOM·wheels·Trivy DB 캐시는 보존한다. UI는 컨테이너 제거 후 접속되지 않는 것이 정상이다.
- 사용자 실행 결과 대기 중이다. 정리 완료·Day 전체 완료·누적 점검 통과로 기록하지 않는다. SESSION·PROGRESS·README의 현재 시작 지점을 갱신했고 환경 기록은 실제 결과 확인 후 갱신한다.

### 2026-10-05 — 실습 자원 정리 완료·산출물 보존 확인
- 사용자 Ubuntu 실행 결과를 [정리 증거](evidence/cleanup-user-2026-10-05.txt)에 보관했다. gzip 검사 이후 체크섬 OK, registry-ui·registry·day09_default Removed와 빈 Compose 목록을 확인했다.
- && 체인이 마지막 du까지 진행해 압축 전 agent-0.2.0-offline.tar의 rm -f 명령 성공을 확인했다. 별도 삭제 후 부재 조회는 하지 않았다.
- 보존 확인: day09_regdata 볼륨, agent:0.2.0-offline 이미지 ID 4c10e5ca549f993cb5d5271e24bb4ff28ae6426f3fd91a5f52b7172796dcf812, tar.gz 42M·sha256 93 bytes·보고서 54K·SBOM 197K, wheels 756K·trivy-cache 1.4G. 크기는 이번 ls/du 표시값이다.
- 의미: 실행 중인 Day 9 Compose 자원은 제거했고 다시 사용할 데이터와 반입 산출물은 유지했다. UI 컨테이너는 제거 상태이며 HTTP 응답은 별도 재조회하지 않았다.
- Codex는 사용자 출력에 근거해 SESSION·PROGRESS·README·환경 기록을 갱신했다. Ubuntu 직접 조작·전역 prune·추가 삭제·커밋/push는 하지 않았다. 9-1~9-5·실습 자원 정리는 완료했으며 누적 리허설·체크포인트 평가는 미진행으로 유지한다.

### 2026-10-05 — main 대상 PR 준비
- 사용자 요청: "repo main branch에 push해서 PR을 만들어줘". 작업 브랜치 codex/day09-results를 push하고 main을 대상으로 PR을 만드는 흐름으로 진행한다. main 병합은 이번 작업에서 수행하지 않는다.
- 포함 범위: Day 9 실습 9-1~9-5·정리 기록, 텍스트 증거 37개, 학습용 반입 신청서, Compose UI 포트/CORS의 8082→18082 변경, 진행·환경 문서, 기존 Day 8 PR #10 병합 확인 메모다.
- Codex 직접 확인: 원격 fetch 후 HEAD와 origin/main 차이 0/0, 기존 열린 PR 없음, git diff --check 통과, 기록 파일 자격 증명 패턴 검사 통과. Compose SHA-256은 a9b2ef288660930816cc97d63b37eef06b828ac7ed653df8848d0cb3b59f8282로 사용자 Ubuntu 검증본과 같다.
- 실습 검증 근거는 사용자 Ubuntu 출력이다. 컨테이너·스캔 재실행이나 Ubuntu 동기화는 하지 않았다. 이미지 덤프·캐시·원본 SBOM·자격 증명은 커밋 대상에 포함하지 않는다.
- PR에는 9-1~9-5와 실습 자원 정리 완료, 누적 점검·체크포인트 평가 미진행 및 HIGH 51 잔여를 명시한다. 커밋·push·PR 생성의 최종 결과는 GitHub 이력에서 확인한다.
