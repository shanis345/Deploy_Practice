# Day 9 이미지 반입 신청서

기준일: 2026-10-05. 9-5 학습용 신청서 작성 완료. 사용자 Ubuntu 실행 결과를 바탕으로 반입 대상과 검증 범위를 정리했다. 실제 고객사 제출·승인은 미진행이며 담당자와 고객사 환경은 미정이다. 취약점 스캔에서는 HIGH 51건이 남아 있다.

양식은 [Day 3 초안](../day03/IMPORT-PACKAGE.md)과 [부록 E-4](../docs/guide/src/24-appendix-e.md)를 따르되, 값은 Day 9 실측 결과를 사용했다. 이 문서는 Windows 프로젝트에 저장했고, 이미지 압축 파일·보고서·SBOM 원본은 Ubuntu `/home/user/onprem-lab/day09`에 있다. 원본 파일의 Windows 복사나 실제 제출 묶음 생성은 수행하지 않았다.

## 신청 내용

| 항목 | 값 또는 상태 | 근거·확인 범위 |
|---|---|---|
| 용도 | 파일럿 에이전트 배포 및 폐쇄망 반입 실습 | 고객사 운영 배포는 미진행 |
| 이미지명:태그 | `ax/agent:0.2.0` | 실습 레지스트리 주소 포함 시 `localhost:5000/ax/agent:0.2.0` |
| 파일 적재 시 태그 | `agent:0.2.0-offline` | save/load 검증에 사용한 태그 |
| 이미지 다이제스트 | `sha256:4c10e5ca549f993cb5d5271e24bb4ff28ae6426f3fd91a5f52b7172796dcf812` | OCI index. [레지스트리 응답](evidence/93-api-user-2026-10-03.txt)·[pull](evidence/93-pull-user-2026-10-04.txt)·[현재 inspect](evidence/95-artifacts-user-2026-10-05.txt) 일치 |
| 반입 파일 | `agent-0.2.0-offline.tar.gz` | gzip 검사·파일 해시 검사·별도 엔진 load 완료 |
| 압축 파일 크기 | 43,776,190 bytes | [2026-10-05 stat 출력](evidence/95-artifacts-user-2026-10-05.txt). 이미지 UI의 크기와 구분 |
| 파일 SHA-256 | `cd08d49e729c690a20925ecedb1284745c826534ebfd241314b327cb107c52e6` | [생성 당시 해시](evidence/92-package-user-2026-10-03.txt)·2026-10-05 재검사 OK |
| 베이스 이미지 | `python:3.12.14-slim` / Debian 13.7 | [빌드](evidence/91-build-user-2026-10-02.txt)·[OS 탐지](evidence/94-scan-user-2026-10-05.txt). 고객사 승인 목록 대조는 미진행 |
| 베이스 다이제스트 | `sha256:f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f` | 빌드 로그의 FROM 식별자 |
| 플랫폼 | `linux/amd64` | 실습 환경 검증 완료. 고객 서버와의 일치 여부는 미확인 |
| 실행 사용자 | UID 10001 / GID 0 | [실제 실행](evidence/93-runtime-user-2026-10-04.txt). UID는 non-root이며 그룹은 root 그룹 |
| 선언 포트 | `8000/TCP` | inspect의 ExposedPorts. 이번 앱 시험은 호스트 포트 게시 없이 진행 |
| 외부 통신 | 고객사 목적지·포트·허용 목록 미정 | network none에서 기동·로컬 `/healthz` 확인. 실제 LLM·DB 연결 및 모든 기능의 무통신 동작을 검증한 것은 아님 |
| 실행 시 외부 다운로드 | 검증한 기동·PyYAML import·`/healthz` 경로에서 불필요 | [격리 엔진 실행](evidence/92-airgap-runtime-user-2026-10-03.txt). 추가 패키지 다운로드 없이 성공 |
| 취약점 스캔 | Trivy 0.56.2 / HIGH 51 / CRITICAL 0 | 2026-10-05 KST 실행. HIGH·CRITICAL 필터 결과이며 보안 승인·취약점 해소 판정은 아님 |
| SBOM | CycloneDX 1.6 / 구성 요소 90개 | [생성·요약](evidence/94-sbom-user-2026-10-05.txt). Python 항목: pip 25.0.1, PyYAML 6.0.2 |
| 동반 이미지·DB | 아래 동반 항목 표 참조 | 실제 확보·등록·파일 포장 상태를 구분 |
| 반입자 / 승인자 | 미정 / 미정 | 실습 계정 `user`를 실제 담당자 이름으로 간주하지 않음 |
| 제출·승인 상태 | 미제출 / 미승인 | 고객사 심사 기준·예외 승인 여부 미확인 |

## 첨부 대상 파일

보관 위치는 Ubuntu `/home/user/onprem-lab/day09`다. 크기와 보고서·SBOM 해시는 [사용자 조회 결과](evidence/95-artifacts-user-2026-10-05.txt)에 근거한다.

| 파일명 | 크기(bytes) | SHA-256 |
|---|---:|---|
| `agent-0.2.0-offline.tar.gz` | 43,776,190 | `cd08d49e729c690a20925ecedb1284745c826534ebfd241314b327cb107c52e6` |
| `trivy-agent-0.2.0.txt` | 55,261 | `94ebfe6ccc9ab5f441beb409753677470393105a431f53764dbb517c7d80e7c2` |
| `sbom-agent-0.2.0.cdx.json` | 201,644 | `4c331693d41f69b03b92affdab09a01df3961d3a3d9c748a9c68f54e62109a42` |

기존 `agent-0.2.0-offline.sha256`은 압축 이미지 파일의 검사 파일이다. 보고서와 SBOM까지 검사하는 통합 체크섬 파일은 아직 만들지 않았다. 파일 해시는 각 파일의 바이트를 식별하며, 이미지 다이제스트와 다른 값이다.

## 이미지 식별자 대조

| 구분 | SHA-256 | 확인한 의미 |
|---|---|---|
| OCI index | `4c10e5ca549f993cb5d5271e24bb4ff28ae6426f3fd91a5f52b7172796dcf812` | 레지스트리 태그가 가리키는 목록. 현재 호스트의 image ID 표시와 같음 |
| linux/amd64 manifest | `0fc1da16c9e87eb64374d9df2afb60b17ebac802955e9238e6aeb441ac4323b4` | index 안의 실행 이미지 항목. UI에 표시된 digest |
| image config | `b7e1e28f346895634bd4c58e176bc9dc05c4c6b2522e65f1ec6044fc6b327db9` | 원본 빌드 config. 9-2 별도 Docker 엔진의 image ID 표시와 같음 |

[빌드 출력](evidence/91-build-user-2026-10-02.txt), [index 본문](evidence/93-index-user-2026-10-04.txt), [격리 엔진 적재](evidence/92-airgap-load-user-2026-10-03.txt)로 연결을 확인했다. 서로 다른 구조의 해시이므로 값이 다르다는 이유만으로 이미지 변조로 판정하지 않는다.

## 스캔 결과와 남은 조치

Trivy DB는 Version 2이며 UpdatedAt은 `2026-10-04T14:28:15.152965452Z`, DownloadedAt은 `2026-10-04T15:36:41.35690486Z`다. 각각 한국 시각 10월 4일 23:28, 10월 5일 00:36에 해당한다. [DB 증거](evidence/94-db-user-2026-10-05.txt)

로컬 Docker 이미지를 대상으로 `--scanners vuln --severity HIGH,CRITICAL`을 사용했고, 스캐너는 `--network none`, `--skip-db-update`, `--skip-java-db-update`, `--offline-scan`으로 실행했다. HIGH 51은 패키지별 보고 항목 수이며 고유 CVE 51개라는 의미는 아니다. 비밀 정보·설정 오류 검사나 전체 심각도 검사를 완료했다고 보지 않는다. [스캔 증거](evidence/94-scan-user-2026-10-05.txt)

보고서에는 수정 버전이 제공된 항목도 있다. 예를 들어 libpcre2-8-0은 설치 버전 `10.46-1~deb13u2`와 수정 버전 `10.46-1~deb13u3`, OpenSSL 관련 패키지는 설치 버전 `3.5.7-1~deb13u2`와 수정 버전 `3.5.7-1~deb13u3`가 표시된다. 보고서의 `fixed`는 수정 버전 제공 상태이며 현재 이미지에 패치가 적용됐다는 뜻은 아니다.

후속 조치는 수정 버전을 반영한 이미지 재빌드·재스캔, 잔여 항목의 영향과 완화 방안 검토, 필요한 경우 고객사 예외 심사다. 이번 9-5에서는 이를 수행하거나 예외를 승인하지 않았다. 가이드 예시의 “HIGH 44·전부 패치 미제공”은 이번 결과에 적용하지 않는다.

SBOM은 구성 요소 목록으로 생성했다. 생성 시 보안 스캔 비활성 안내는 정상이며 취약점 정보는 별도 보고서로 제공한다. JSON 읽기·형식명·구성 요소 요약을 확인했지만 전체 CycloneDX 스키마 검증이나 목록의 완전성 검증은 수행하지 않았다.

## 동반 항목

| 항목 | Day 9에서 확인한 상태 | 실제 반입 전 남은 사항 |
|---|---|---|
| `nicolaka/netshoot:v0.13` | 진단용. `localhost:5000/tools/netshoot:v0.13`에 linux/amd64 이미지 push 및 API 확인 | 별도 반입 파일·해시·스캔·승인 미확인 |
| netshoot 레지스트리 digest | `sha256:5a21d467fed653554bdc483ca5e7e866805c5b4c8f7ecb195a43f778c8d02fb8` | 단일 플랫폼으로 push한 값. 원본 멀티플랫폼 index와 구분 |
| `aquasec/trivy:0.56.2` 및 Trivy DB | 로컬 도구 이미지와 Ubuntu DB 캐시 확보·오프라인 스캔에 사용 | 도구·DB의 별도 전달 파일 포장 및 해시 미확인 |
| `registry:2.8.3`, `joxit/docker-registry-ui:2.5.7` | 실습 레지스트리·UI 기동에 사용 | 고객사 기존 레지스트리 사용 여부에 따라 반입 필요성 결정 |
| nginx·PostgreSQL·LLM 게이트웨이·프록시 | 가이드의 동반 의존 이미지 예시 | 고객사 배포 구성·필요 버전 확정 및 파일 반입 여부 미확인 |

등록 근거: [push](evidence/93-push-user-2026-10-03.txt)·[API](evidence/93-api-user-2026-10-03.txt). 이 항목들이 모두 agent 압축 파일에 포함된 것은 아니다.

## 반입 횟수를 줄이는 설계 점검

소스 항목은 Windows의 [app.py](app.py)·[Dockerfile.offline](Dockerfile.offline) 검토 기준이며, 이번 실행 검증과 구분한다.

| 점검 항목 | 상태·범위 |
|---|---|
| 프롬프트 외부화 | `PROMPT_PATH` 지원·파일 변경 재적재 코드 확인. 고객사 볼륨/ConfigMap 미구성 |
| rubric·임계값 외부화 | `RUBRIC_PATH`로 YAML 읽기 지원. 고객사 파일 내용·임계값 적용은 미검증 |
| LLM 엔드포인트·모델 | `LLM_BASE_URL`, `LLM_MODEL` 지원. 실제 목적지는 미정 |
| DB·API 접속 정보 | `DB_DSN`, `LLM_API_KEY` 환경변수 지원. 실제 DB 업무 쿼리·고객사 시크릿 연동은 미검증 |
| 로그 레벨 | `LOG_LEVEL` 지원·INFO에서 DEBUG 억제 코드 확인 |
| 기능 on/off 플래그 | 일반 기능 플래그 구성은 이번 코드 점검에서 확인하지 않음 |
| 진단 엔드포인트 | `/diag`, `/egress`, `/tcp` 코드 존재. 고객사 통신 정책은 별도 확정 필요 |
| 진단 이미지 | netshoot를 위 동반 목록에 기록. 레지스트리 등록 확인 |
| 의존 이미지 | 실제 배포 구성 확정 후 목록·버전·전달 파일 보완 필요 |
| 인터넷 없는 빌드·기동 | 9-1에서 준비된 베이스·wheel로 RUN 네트워크 차단 빌드 성공. 9-2에서 외부 네트워크 없는 빈 별도 엔진에 파일 load 후 기동 성공 |
| non-root | UID 10001 실행 확인. GID는 0 |
| 취약점 심사 | 스캔 수행 완료. HIGH 51 잔여, 통과 기준·예외 승인 미확인 |
| SBOM | 생성 및 요약 확인 완료 |
| 고객 서버 아키텍처 | 실습 linux/amd64 확인. 실제 고객 서버와 대조는 미진행 |

9-5의 완료 범위는 실측 근거가 있는 학습용 신청서 작성까지다. 고객사 필수 정보 확정, 취약점 조치·심사, 실제 제출·승인과 Day 9 누적 점검은 남아 있다.
