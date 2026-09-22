# On-prem Agent Lab

온프렘·망분리 환경의 에이전트 배포 실습을 Day별로 수행하고, 소스와 학습 기록을 함께 관리하는 로컬 프로젝트다.

**현재 상태: Day 0의 0-1 부트스트랩 완료. Day 0 전체 완료는 아니다.**

## 먼저 읽기
- [진행 현황](PROGRESS.md): 완료 범위와 정확한 중단 지점, Day별 기록 링크
- [환경 기록](docs/environment.md): WSL2·Docker·도구 버전과 가이드 대비 차이
- [Codex 진행 규칙](AGENTS.md): 한 단계씩 진행하고 지정한 범위에서 멈추는 규칙
- [Day 0 기록](day00/SESSION.md): 현재까지의 실행 과정과 오류 해결
- [가이드북 HTML](docs/guide/onprem-agent-deploy-guide.html): 브라우저에서 여는 원본 가이드

## 구조
| 위치 | 용도 |
|---|---|
| bootstrap.sh | 제공된 설치·점검 스크립트 |
| agent/ | 공통 학습용 에이전트 소스 |
| day00/ ~ day14/ | 각 Day의 README, SESSION 기록과 기존 실습 코드 |
| skeleton/ | 종합 배포 템플릿 |
| docs/guide/ | 가이드 HTML·Markdown·테마·이미지·빌드 도구 |
| templates/ | Day 기록 양식 |
| archives/ | 제공받은 ZIP 원본과 체크섬 |

## Day별 작업 방식
1. 같은 Codex 프로젝트에서 Day별 작업 하나를 사용한다. 예: `Day 00 — 환경 준비`.
2. 시작할 때 AGENTS.md, PROGRESS.md, 해당 Day의 README.md와 SESSION.md를 읽는다.
3. 사용자가 정한 절만 진행한다. 실습 명령은 Ubuntu WSL2에서 실행한다.
4. 실행 결과와 오류 해결을 해당 Day의 SESSION.md에 기록한다.
5. 중단·종료 시 정확한 다음 시작 지점과 PROGRESS.md를 갱신한다.

GitHub 저장소: [https://github.com/shanis345/Deploy_Practice](https://github.com/shanis345/Deploy_Practice)

초기 자료는 `codex/initial-practice-setup` 브랜치의 PR로 관리한다. 실습 진도는 Day 0의 0-1 완료 상태다.
Codex 프로젝트 등록 및 Day별 작업 생성은 아직 수행하지 않았다.

## Windows 프로젝트와 Ubuntu 실습 폴더
이 프로젝트 루트는 사용자가 지정한 Windows의 `12. Deploy Practice` 폴더다.
현재 실행 환경은 Ubuntu의 `/home/user/onprem-lab`이며 두 폴더는 자동 동기화되지 않는다.
현재 Ubuntu 실습 파일은 이동하거나 덮어쓰지 않았다. 이후 소스를 수정할 때 실행에 쓰는 복사본에 반영됐는지 확인한다.
기존 스크립트와 Compose의 상대 경로를 유지하기 위해 agent, skeleton, dayXX를 같은 루트에 둔다.

## 자료와 버전 관리 준비
소스, 문서, 학습 기록, 원본 ZIP을 보관한다. 실제 `.env`, 개인 키, kubeconfig, 이미지 덤프, 캐시는 .gitignore로 제외한다.
기존 .env.example과 Secret 예시는 유지한다. 가이드 빌드 방법은 [가이드 README](docs/guide/README.md)를 참고한다.
셸 스크립트는 Linux에서 실행하며 필요한 실행 권한을 확인한다. .gitattributes는 향후 Git 사용 시 LF 줄바꿈을 유지하도록 준비했다.
