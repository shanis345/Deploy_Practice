# 실습 환경

기준일: 2026-09-22. 사용자가 공유한 실행 출력에 근거하며 이 프로젝트 정리 작업에서 환경을 재검사하지 않았다.

## 실행 위치와 파일 위치
- 호스트: Windows, 컴퓨터 이름 DESKTOP-6KJVBND. Windows 버전·RAM·디스크 여유는 확인하지 않음.
- 리눅스: Ubuntu WSL2, linux/amd64. Ubuntu 배포판 버전은 확인하지 않음.
- Ubuntu 사용자: user
- 현재 실습 디렉터리: `/home/user/onprem-lab`
- Windows 프로젝트 디렉터리: `C:\Users\user\Desktop\Applications\25. BCG X\7. 준비\12. Deploy Practice`
- Windows 폴더와 Ubuntu 폴더는 별도 복사본이며 자동 동기화되지 않는다. 이후 코드 변경 시 어느 쪽을 수정했는지 기록하고 반영한다.
- bootstrap.sh 원본의 LAB은 `${HOME}/onprem-lab`이다. 이 프로젝트를 Windows에 배치했다고 실습 위치가 변경되지는 않는다.
- Docker Desktop은 Windows에서 실행하고 Ubuntu WSL Integration을 사용한다.

## 확인된 도구
| 도구 | 실제 결과 | 비고 |
|---|---|---|
| Docker Desktop | 4.90.0 (238679) | Server 출력 |
| Docker Engine / CLI | 29.7.2 | Client와 Server 응답 |
| Docker Compose | v5.5.1 | docker compose 명령 확인 |
| kubectl | v1.36.1 | 가이드 고정값 v1.31.0과 다름; 미조정 |
| k3d | v5.7.4 | 설치 확인; 클러스터는 아직 만들지 않음 |
| helm | v3.16.2+g13654a5 | 설치 확인 |
| k9s | v0.32.5 | 설치 확인 |
| lazydocker | 0.23.3 | 설치 확인 |
| dive | 0.13.1 | 첨부 스크립트 설정과 일치, 본문의 0.12.0과 다름 |
| jq | 1.7 | 설치 확인 |
| curl | 8.5.0 | 설치 확인 |
| git | 2.43.0 | Ubuntu 출력 |
| python3 | 3.12.3 | Ubuntu 출력 |
| iproute2 | ip 명령 존재 | 버전 미기록 |

## 알려진 차이와 남은 확인
- check의 ✓는 고정 버전 일치나 모든 후속 실습의 호환성을 보장하지 않는다.
- kubectl 버전 차이는 해결되지 않은 항목으로 유지한다.
- 가이드의 k3s v1.30 클러스터는 아직 생성·검증하지 않았다.
- 실제 소켓 권한은 root:docker, 660이었고 user는 docker 그룹에 등록돼 있었다. newgrp docker로 현재 셸에 적용한 뒤 연결됐다.
- 실습 이미지 12개 존재는 [최종 사용자 출력](../day00/evidence/bootstrap-final.txt)에 기록했다. 이미지 바이트는 이 프로젝트 폴더로 복사하지 않았다.
- 원본 가이드의 검증 주장과 이 PC에서 실제 확인한 결과를 구분한다.
