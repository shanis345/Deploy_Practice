# 진행 현황

- 기준일: 2026-10-05
- Day 9 저장소 반영: 사용자 요청으로 codex/day09-results에서 main 대상 PR을 준비한다. 실습 기록·증거·신청서·UI 포트 수정 및 기존 Day 8 병합 확인 메모를 포함하며, 누적 점검 미진행 상태를 유지한다. 실제 커밋·push·PR 결과는 GitHub 이력에서 확인한다.
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
| 10 | Kubernetes 기초: Pod · Deployment · Service · probe | 미시작 | [SESSION](day10/SESSION.md) |
| 11 | 설정 · 비밀 · 수신 · Helm: ConfigMap, Secret, Ingress, 차트 | 미시작 | [SESSION](day11/SESSION.md) |
| 12 | NetworkPolicy로 존 분리, 그리고 OpenShift의 차이 | 미시작 | [SESSION](day12/SESSION.md) |
| 13 | LLM 게이트웨이 · 감사 로그 · 관측성 기초 | 미시작 | [SESSION](day13/SESSION.md) |
| 14 | Walking Skeleton 종합: 전 구간 관통, 검증 스크립트, 런북, 이관 | 미시작 | [SESSION](day14/SESSION.md) |

## 다음 실습을 시작할 때

최신 시작 지점(2026-10-05): Day 9의 9-1~9-5·실습 자원 정리 완료. registry·UI는 제거됐고 regdata·이미지·반입 산출물·캐시는 보존했다. 신청서는 Windows에 저장돼 있다. 다음 범위는 사용자 요청 후 정하며 누적 점검 2차·체크포인트 평가·고객사 제출은 미진행이다. Day 9 전체 통과로 판정하지 않는다. 아래 시작 지점들은 이전 이력이다.

최신 시작 지점(2026-10-01): Day 8 종료·PR #10 main 병합 및 Windows main 갱신 완료(6801a09). 8-1~8-4 실습·지정 자원 정리·공개 CA와 CA 이미지 보존을 확인했다. 체크포인트 해설은 제공했으며 독립 평가는 미실시다. Ubuntu 전체 동기화는 하지 않았다. 다음 학습은 사용자 요청 후 Day 9이며 아직 시작하지 않았다. 병합 확인 메모는 로컬 미커밋 변경이다. 아래 2026-09-30 시작 지점은 이전 이력이다.

최신 시작 지점(2026-09-30): Day 7은 7-1~7-5 학습·정리를 마치고 종료했다. 사용자 출력으로 컨테이너 4개·네트워크 2개 제거 및 프로젝트 잔존 목록 부재를 확인했다. 관찰용 mitm과 임시 빌드 이미지·폴더도 앞서 제거 확인했다. 이미지·볼륨·빌드 캐시 전역 정리는 수행하지 않았다. 체크포인트 6문항은 해설을 제공했으며 독립 답변 평가는 미실시다. 실제 빌드 프록시 통신 장애 재현 및 HTTPS/CA 시험도 미실시로 구분한다. 다음은 사용자 요청 후 Day 8 사내 CA와 TLS 검사이며 아직 시작하지 않았다. Day 7 기록은 Windows 사본에 갱신했다. 사용자가 완료·push를 요청해 codex/day07-results 브랜치에서 커밋·원격 반영을 진행한다. Ubuntu 동기화와 main 병합은 별도다.

1. Day 6 컨테이너·네트워크 제거와 8080 리스너 부재를 확인했다. 6-4 문서는 학습용 초안이며 실제 고객사 제출·정책 적용은 없다. 이미지·볼륨·/tmp/day06-compose.OTTiFi 백업은 삭제하지 않았다. 별도 자기점검·독립 진단 평가는 미실시다. Day 5 Stats·TUI 관찰 미확인, 5-2 ③ 최초 무응답 원인 및 Day 4 잔존 자원·미해결 사항은 유지한다.
2. Day 1의 정리 결과 확인·E-1 신청서 초안·최종 자기점검은 미완료로 유지하며 사용자가 재개할 때 이어 간다.
3. kubectl 고정 버전 불일치 등 미해결 사항을 완료로 간주하지 않는다.
