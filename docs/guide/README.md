# 가이드 원본과 빌드

- `onprem-agent-deploy-guide.html`: 사용자가 제공한 HTML 원본. 원본과 바이트가 동일하다.
- `src/`, `theme/`, `shots/`: 제공된 가이드 소스·테마·이미지. 원본을 복사했다.
- `build.py`: 현재 프로젝트 구조에 맞게 수정한 빌드 도구.
- `lab-files.txt`: 부록 F에 수록할 실습 파일 목록. 경로는 프로젝트 루트 기준이다.
- `requirements.txt`: 원본 README에 명시된 가이드 빌드 의존성. 버전 고정은 원본에 없었다.

## 구조 변경
원본은 build.py 옆 lab/을 순회했다. 여기서는 프로젝트 루트의 기존 실습 소스를 참조한다.
명시적 파일 목록을 사용하므로 dayXX/SESSION.md, evidence, archives 등은 부록에 들어가지 않는다.
원본 소스 전체와 원래 build.py는 ../../archives/onprem-guide-src.zip에 보존돼 있다.
새 실습 코드를 부록에 포함하려면 lab-files.txt에 해당 상대 경로를 추가한다.

## 선택적 재생성 방법
실습 부트스트랩과 별개다. 가이드를 수정해 재생성할 때만 Ubuntu에서 실행한다.

```bash
cd docs/guide
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 build.py
```

결과는 `dist/onprem-agent-deploy-guide.html`에 생성되어 제공된 HTML 원본을 덮어쓰지 않는다.
원본의 `--check` 옵션은 문서 내 YAML·셸 블록의 기계 검사를 추가한다. 실제 실습 성공을 검증하는 기능은 아니다.
프로젝트 정리 중에는 실습 명령을 실행하지 않는다.

## 이번 정리 작업의 검증 범위
- 수정한 build.py의 Python 구문을 검사했다.
- 부록 F가 수집하는 77개 파일 목록이 원본과 동일함을 확인했다.
- 새로운 학습 기록과 evidence가 부록 파일 목록에 포함되지 않음을 확인했다.
- 현재 작업용 Python에는 가이드 빌드 의존성이 없어 HTML 전체 재생성은 실행하지 않았다. 제공된 원본 HTML은 그대로 보존했다.
