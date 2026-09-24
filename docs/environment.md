# 실습 환경

기준일: 2026-09-25. Day 2 실습·정리 결과는 사용자 제공 Ubuntu 출력에 근거한다. 2026-09-23 환경 재점검은 Codex 직접 조회, 후속 lazydocker 업데이트·화면 확인은 사용자 제공 출력과 스크린샷에 근거한다. 이전 결과는 별도 이력으로 구분한다.

## Day 2 종료 상태 (2026-09-25)
- 실습 2-1~2-7 완료. 사용자 정리 출력으로 who1·who2·lim·demo-net 삭제 및 빈 ip netns list를 확인했다. 기존 koica 프로젝트는 정리 대상에 포함하지 않았다.
- 첫 재확인 시 세 명령이 구분자 없이 한 줄로 붙어 sysctl 옵션 오류가 발생했으나 세미콜론으로 구분해 재실행했다. 후속 사용자 출력은 `net.ipv4.ip_forward = 0`, NAT는 `-P POSTROUTING ACCEPT`만 표시, 브리지 목록은 빈 출력이었다. 사전 전달 설정 복구와 실습 NAT·브리지 제거까지 확인해 정리를 완료했다.
- 아래 2026-09-24의 실행 중 구성은 실습 당시 관찰 이력이며 현재 잔존 상태를 뜻하지 않는다. [정리 증거](../day02/evidence/day02-cleanup-user-2026-09-25.txt), [전체 기록](../day02/SESSION.md).

## Day 2 실습 당시 상태 (2026-09-24)
- 2-6 사전 조회에서 Docker 명령 네 개 모두 WSL integration 안내 오류로 실패했으나, Desktop 실행 안내 후 사용자 docker version 출력으로 Client·Engine 29.8.0, API 1.56, Desktop 4.92.0 (240144), linux/amd64, Context default 및 Client·Server 응답을 확인해 복구됐다. Windows에서 수행한 조작 상세는 미제공이다. 이후 사전 조회와 2-6 실습도 사용자 출력으로 확인했다.
- 사용자 출력으로 2-1~2-7 완료를 확인했다. Day 전체 자원 정리·자기점검은 남아 있다. Ubuntu의 biz·db 네임스페이스, br-lab(10.42.0.1/24), veth 연결 및 biz(10.42.0.10/24)·db(10.42.0.20/24)의 통신을 확인했다. biz의 기본 경로는 10.42.0.1이며 db 기본 경로는 추가하지 않았다.
- 2-7에서 lim을 --memory=64m·--rm·sleep 3600으로 실행했다. stats는 416KiB / 64MiB, 0.63%, PIDS 1이며 cgroup 상한 조회는 67108864바이트였다. 제한 값 일치를 확인했으며 OOM은 시험하지 않았다. lim은 아직 수동 정리하지 않았다.
- 2-6의 Docker 엔진 관찰에서 demo-net(172.19.0.0/16·게이트웨이 172.19.0.1), who1(172.19.0.2/16), br-0256008dc546·veth 포트 및 해당 대역 MASQUERADE를 확인했다. who1은 DNS 127.0.0.11에서 자기 이름 조회 성공, 기본 bridge의 who2는 DNS 192.168.65.7에서 NXDOMAIN이었다. who1·who2는 --rm·sleep 3600으로 실행했고 demo-net과 함께 아직 수동 정리하지 않았다. 시간 경과 시 잔존 상태를 확인한다. 기존 koica 프로젝트는 정리 대상이 아니다.
- 2-5에서 tcpdump 미검출 후 설치를 안내했고 사용자 버전 출력으로 tcpdump 4.99.4·libpcap 1.10.4·OpenSSL 3.0.13을 확인했다. db TCP 5432의 nc 리스너로 접속하며 SYN·SYN-ACK와 TCP 연결 성공을 관찰했다. 이후 캡처 작업 종료 및 리스너 PID 2129 종료·LISTEN 해제를 확인했다. 실제 PostgreSQL 서버를 설치한 것은 아니다.
- iptables 명령 미검출 후 설치를 안내했고, 후속 출력에서 v1.8.10 (nf_tables)과 규칙 조회 성공을 확인했다. apt 설치 로그는 미제공이다. nc 경로는 /usr/bin/nc다.
- 설정 전 ip_forward=0, FORWARD 기본 ACCEPT·개별 규칙 없음, NAT POSTROUTING 개별 규칙 없음을 확인했다. 이후 사용자가 ip_forward=1과 `-s 10.42.0.0/24 ! -o br-lab -j MASQUERADE` 규칙 한 개를 설정했다.
- biz에서 `nc -zv -w3 1.1.1.1 443` 성공·종료 코드 0. DNS·TLS·HTTP 및 외부 ping 성공까지 검증한 것은 아니다. Ubuntu 경로 조회는 `via 172.18.48.1 dev eth0 src 172.18.60.227`이었다.
- 실습 구성은 유지 중이다. 최종 정리 시 실습 NAT·네트워크 제거 및 ip_forward의 사전 값 0 복구를 포함한다. 영구 설정은 추가하지 않았다. Codex가 Ubuntu 설정을 직접 변경하거나 재시험하지 않았다. 상세 명령·출력은 [Day 2 SESSION](../day02/SESSION.md)에 기록했다.

## 현재 상태 — Docker Desktop 실행 후 (2026-09-23)
- Day 1의 1-3 사용자 출력으로 Ansible core 2.21.4를 `/home/user/onprem-lab/day01/.venv/bin/ansible`에서 확인했다(Python 3.12.3, Jinja 3.1.6, PyYAML 6.0.3). community.docker 5.3.0은 `/home/user/.ansible/collections/ansible_collections`에 설치돼 있다. 후속 사용자 출력에서 두 대상 연결 SUCCESS·pong, 첫 플레이북 실행 ok=5·changed=3·failed=0·unreachable=0, 두 번째 실행 ok=5·changed=0·failed=0·unreachable=0을 확인했다. 내부 별도 조회에서도 appuser UID 10001·nologin, 디렉터리 appuser:root·0750, 예시 설정 파일 root:root·0644를 확인했다. [내부 상태 증거](../day01/evidence/day01-13-state-user-2026-09-23.txt). 컨테이너 삭제와 deactivate 실행 결과는 아직 없으며 현재 실행 여부를 재조회하지 않았다.
- Day 1의 1-3 사전 확인 사용자 출력: Docker Desktop 4.92.0(240144), Docker Client/Engine 29.8.0, API 1.56(서버 최소 1.40), linux/amd64, Python 3.12.3. Ubuntu day01의 inventory.ini·prepare-vm.yaml 두 파일은 Windows 사본과 SHA-256이 일치한다. 이번에는 사용자 제공 출력이며 Codex가 Ubuntu에서 직접 재실행한 것이 아니다. [증거](../day01/evidence/day01-13-precheck-user-2026-09-23.txt).
- 후속 0-4 실습에서 lazydocker 0.23.3의 API 1.25 고정 사용과 Docker 최소 API 1.40 사이의 호환 오류를 확인했다. 사용자가 `/usr/local/bin/lazydocker`를 공식 바이너리 0.25.2(linux/amd64)로 교체한 뒤 오류 없이 이미지·네트워크 목록이 표시되는 화면을 제공했다. `agent:0.1.0`은 화면상 189.09MB이며 기본 네트워크 bridge·host·none이 모두 보인다.
- lazydocker의 실제 설치 버전은 이제 0.25.2다. 가이드와 bootstrap.sh의 0.23.3 고정값은 수정하지 않았으므로 새 환경 설치 시 동일한 호환 오류가 재발할 수 있다. `check`의 버전 출력 성공만으로 TUI 동작을 보장할 수 없다.
- 사용자가 Docker Desktop 실행을 알린 뒤 Codex가 Ubuntu에서 직접 재점검했다. `./bootstrap.sh check` 전 항목 통과, 종료 코드 0이다.
- Docker Client / Server 모두 29.8.0, Docker Compose v5.5.1, kubectl Client v1.36.1. Docker Engine은 가이드의 27 이상 조건을 충족한다.
- 가이드 고정값과의 차이는 kubectl 1.36.1 대 1.31.0, dive 0.13.1 대 본문 0.12.0, Compose 5.5.1 대 v2 표기다. check는 실제 Compose 버전에 상관없이 성공 문구를 `docker compose v2`로 출력한다. 향후 실습 호환성을 검증한 것은 아니다.
- Docker 소켓은 root:docker, 660이고 현재 사용자 그룹에 docker가 포함돼 있다. 추가 권한 변경 없이 Docker 엔진이 응답한다.
- bootstrap.sh에 지정된 이미지 12개 모두 `docker image inspect`로 직접 존재를 확인했다. 다운로드나 컨테이너 실행은 하지 않았다.
- 이전 Docker·kubectl 미검출은 Desktop 실행 후 해소됐다. 아래 초기 점검 실패는 이력으로 보존한다.

## 초기 재점검 결과 — Docker Desktop 실행 전 (2026-09-23)
- Windows 11 Pro 10.0.26200, 물리 RAM 약 31.18GiB, C: 여유 약 454.53GiB. 가이드의 PC 자원 권장치 이상이다.
- Ubuntu 24.04.1 LTS, WSL2, 커널 `5.15.167.4-microsoft-standard-WSL2`. WSL 메모리는 약 15GiB, `/`의 가상 디스크 여유 표시는 954GiB다. 실제 호스트 여유와 구분한다.
- 초기 `wsl --list --verbose`에서 Ubuntu와 docker-desktop은 모두 Stopped, VERSION 2였다. 조회를 위해 Ubuntu를 실행했다. Windows에서 Docker Desktop과 com.docker.backend 프로세스는 검출되지 않았다.
- Ubuntu의 `./bootstrap.sh check` 결과는 종료 코드 1: kubectl 미검출, Docker 데몬 연결 실패, Compose 실행 실패. Docker 줄의 ✓는 Windows 측 안내용 명령이 PATH에 있다는 뜻이며 정상 동작을 입증하지 않는다.
- `/usr/bin/docker`와 `/usr/local/bin/kubectl`은 `/mnt/wsl/docker-desktop/cli-tools/...`를 가리키지만 현재 해당 마운트 경로가 없다. `/var/run/docker.sock`도 없다. 현재 사용자 그룹에는 docker가 포함돼 있다.
- k3d v5.7.4, helm v3.16.2, k9s v0.32.5, lazydocker 0.23.3, dive 0.13.1, jq 1.7, curl 8.5.0, git 2.43.0, Python 3.12.3, iproute2 6.1.0을 직접 확인했다.
- `/home/user/onprem-lab/bootstrap.sh`는 755, LF이며 Windows 사본과 SHA-256이 일치한다. agent, day01~day13, skeleton 디렉터리도 존재한다. 전체 소스의 일치 여부까지 검사한 것은 아니다.
- 이 초기 점검에서는 엔진에 연결되지 않아 이미지 12개를 재확인하지 못했다. 이후 Desktop 실행 후 모두 확인했다(위 현재 상태 참고).
- 설치·다운로드·버전 변경·컨테이너 실행은 하지 않았다. [직접 점검 증거](../day00/evidence/local-check-2026-09-23.txt)를 참고한다.

## 실행 위치와 파일 위치
- 호스트: Windows 11 Pro, 컴퓨터 이름 DESKTOP-6KJVBND. RAM·디스크는 위 재점검 결과 참고.
- 리눅스: Ubuntu 24.04.1 LTS, WSL2, linux/amd64.
- Ubuntu 사용자: user
- 현재 실습 디렉터리: `/home/user/onprem-lab`
- 2026-09-23 사용자 제공 0-5 목록: agent, bootstrap.sh, day01~day13, skeleton 존재. Ubuntu에 day14는 없으며 Day 14 실습 시작 경로는 skeleton이다. Windows의 Day별 기록 폴더와 구분한다.
- Windows 프로젝트 디렉터리: `C:\Users\user\Desktop\Applications\25. BCG X\7. 준비\12. Deploy Practice`
- Windows 폴더와 Ubuntu 폴더는 별도 복사본이며 자동 동기화되지 않는다. 이후 코드 변경 시 어느 쪽을 수정했는지 기록하고 반영한다.
- bootstrap.sh 원본의 LAB은 `${HOME}/onprem-lab`이다. 이 프로젝트를 Windows에 배치했다고 실습 위치가 변경되지는 않는다.
- Docker Desktop은 Windows에서 실행하고 Ubuntu WSL Integration을 사용한다.

## 이전에 확인된 도구 (2026-09-22 사용자 제공 출력)
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
- Ansible 2.21.4의 Day 1 첫 실행에서 Python 인터프리터 자동 탐색 경고와 INJECT_FACTS_AS_VARS 변경 예고가 표시됐다. 후자는 가이드 prepare-vm.yaml의 top-level facts 참조 방식 때문이며 출력은 2.24에서 제거 예정이라고 알린다. 현재 실행은 성공했으며 향후에는 ansible_facts 사전 참조로 수정할 필요가 있다. 이번에는 동일 플레이북 재실행 확인을 위해 소스를 변경하지 않았다.
- Day 1의 1-3에서 `python3 -m venv .venv`가 ensurepip 불가로 실패했다. 이후 사용자 출력으로 `python3.12-venv` 3.12.3-1ubuntu0.17, `python3-pip-whl` 24.0+dfsg-1ubuntu1.3, `python3-setuptools-whl` 68.1.2-2ubuntu1.2 설치 완료를 확인했다. 기존 패키지 업그레이드는 없었다. 재실행 후 가상환경 생성·활성화에 성공했고 Python은 `/home/user/onprem-lab/day01/.venv/bin/python`, pip 24.0은 같은 .venv의 Python 3.12 경로를 가리켰다. ensurepip 오류 해소 확인. 후속 Ansible·community.docker 설치 버전도 사용자 출력으로 확인했다(위 현재 상태 참고). [오류·대응 기록](../day01/SESSION.md) 참고.
- check의 ✓는 고정 버전 일치나 모든 후속 실습의 호환성을 보장하지 않는다.
- kubectl 버전 차이는 해결되지 않은 항목으로 유지한다.
- 가이드의 k3s v1.30 클러스터는 아직 생성·검증하지 않았다.
- 실제 소켓 권한은 root:docker, 660이었고 user는 docker 그룹에 등록돼 있었다. newgrp docker로 현재 셸에 적용한 뒤 연결됐다.
- 실습 이미지 12개 존재는 [최종 사용자 출력](../day00/evidence/bootstrap-final.txt)에 기록했다. 이미지 바이트는 이 프로젝트 폴더로 복사하지 않았다.
- 원본 가이드의 검증 주장과 이 PC에서 실제 확인한 결과를 구분한다.
