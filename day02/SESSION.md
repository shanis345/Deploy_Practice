# Day 2 — 리눅스 네트워크 기초: 네임스페이스·브리지·라우팅·DNS

## 진행 상태
- 상태: 실습 2-1~2-7 및 자원 정리 완료. 별도 자기점검 미진행
- 완료한 범위: 수동 네트워크·NAT·외부 TCP·패킷 관찰, Docker 자동 구성·DNS 비교, 64MiB 메모리 제한과 cgroup 값 확인
- 중단 지점: 2026-09-25 기록 정리·PR 제출. 컨테이너·demo-net·네임스페이스·브리지·실습 NAT 제거와 ip_forward=0 복구 확인
- Codex 작업: 아직 별도 작업을 만들지 않음
- 실행 증거 기준: 사용자 제공 출력과 직접 검증 결과를 구분해 기록

## 목표와 이번 세션 범위
사용자가 Ubuntu에서 2-1~2-7을 직접 실행하고 Codex가 출력을 대조했다. 2026-09-25 사용자는 Day 2 기록 정리와 GitHub PR을 요청했고, 이어 실습 정리 명령의 출력을 제공했다. 현재 작업은 기록·증거 정리와 PR 제출이다. Day 3이나 새 실습을 시작하지 않는다. Day 1의 미완료 마무리 항목은 유지한다.

## 결과 요약 — 2026-09-24 실습 / 2026-09-25 인수인계

| 절 | 실제 확인한 결과 | 배운 점 |
|---|---|---|
| 2-1 | 빈 biz에 lo DOWN만 존재, 외부 ping은 Network is unreachable·코드 2 | 네트워크 공간을 만들기만 해서는 연결되지 않는다 |
| 2-2 | biz→브리지·db ping 각 1회 송수신·손실 0%, veth 두 개 forwarding | 같은 대역을 브리지·가상 랜선으로 연결하면 통신한다 |
| 2-3 | 기본 경로 없음 → 코드 2, 추가 후 응답 없음 → 코드 1 | 경로 선택 실패와 응답 미수신을 구분한다 |
| 2-4 | ip_forward 0→1, 실습 MASQUERADE 한 개, 1.1.1.1:443 TCP 성공·코드 0 | 경로·패킷 전달·주소 변환은 각각 다른 역할이다 |
| 2-5 | db에서 SYN·SYN-ACK 관찰, TCP 성공, 리스너·캡처 정리 | 실제 패킷을 보고 통신이 진행된 단계를 판별한다 |
| 2-6 | Docker의 브리지·veth·IP·경로·NAT 자동 구성, who1 이름 조회 성공·who2 NXDOMAIN | Docker가 Linux 구성을 자동화하며 네트워크 종류에 따라 DNS 기능이 다르다 |
| 2-7 | 사용량 416KiB / 상한 64MiB, cgroup 값 67108864바이트 | Docker 메모리 제한이 커널의 cgroup 설정에 반영된다 |

- 실행 증거: [사용자 출력 주요 발췌](evidence/day02-results-user-2026-09-24.txt), [정리 출력](evidence/day02-cleanup-user-2026-09-25.txt). 모두 사용자 제공 출력이며 Codex 직접 실습 검증과 구분한다.
- Windows 프로젝트와 Ubuntu `/home/user/onprem-lab`은 별도 복사본이다. 이번 PR은 Windows 기록 변경이며 실습 소스 동기화·재실행은 하지 않았다.
- **미검증 범위:** OOM 재현, DNS·TLS·HTTP를 포함한 외부 업무 통신, NAT 전후 패킷 캡처는 수행하지 않았다. cgroup 조회의 대체 경로가 있으므로 출력 값만으로 cgroup 버전을 확정하지 않는다.
- 2-3은 ICMP ping, 2-4는 TCP 443 시험이다. 두 결과를 비교해 외부 ping까지 성공했다고 쓰지 않는다. 기본 경로·forwarding·NAT를 하나씩 분리한 모든 원인 실험을 한 것도 아니다.
- 아래 실행 기록의 “결과 대기”는 해당 시점의 안내 이력이다. 최신 상태는 이 요약·진행 상태·맨 아래 인수인계를 따른다.

## 구성과 변경 전후

| 실행 환경 | 주요 구성 | 종료 시 확인할 항목 |
|---|---|---|
| Ubuntu WSL2 수동 실습 | biz 10.42.0.10/24, db 10.42.0.20/24, br-lab 10.42.0.1/24, veth 두 쌍, biz 기본 경로 | 네임스페이스·브리지·실습 NAT 제거, ip_forward 사전 값 0 복구 |
| Docker Desktop 엔진 | demo-net 172.19.0.0/16, who1 172.19.0.2, 기본 bridge의 who2, 64MiB 제한 lim | 이번 실습 컨테이너 세 개와 demo-net만 제거 |
| 기존 다른 프로젝트 | koica-oda-local-test 네트워크·컨테이너 | 이번 실습 정리 대상 아님 |

리스너 PID 2129와 캡처 작업은 2-5에서 종료를 확인했다. 종료된 PID를 다음 세션의 삭제 대상으로 재사용하지 않는다. Docker 실습 컨테이너는 --rm·sleep 3600을 사용했으므로 오래 지난 뒤에는 존재 여부부터 확인한다.

## 실행 기록
### 2026-09-24 — 실습 2-1 사전 조회
- 실행 위치: Ubuntu WSL2. 사용자 프롬프트는 `~/onprem-lab/day02`다. 별도 안내한 pwd 및 command -v 출력은 아직 받지 않았다.
- 확인 주체: 사용자 제공 출력. Codex가 Ubuntu에서 직접 실행한 결과가 아니다.
- 실행 명령·주요 출력:

```text
$ ip -brief addr
lo               UNKNOWN        127.0.0.1/8 10.255.255.254/32 ::1/128
eth0             UP             172.18.60.227/20 fe80::215:5dff:fe6d:af41/64
$ ip netns list
(출력 없음)
$ ip -brief link show type bridge
(출력 없음)
```

- 결과와 의미: Ubuntu eth0는 UP이며 IPv4는 172.18.60.227/20이다. 이름이 등록된 네트워크 네임스페이스와 현재 네임스페이스의 브리지는 조회되지 않았다. 이 결과만으로 Docker Desktop 엔진의 네트워크 유무를 판정하지 않는다.
- 기존 biz·db·br-lab이 조회되지 않아 가이드의 사전 삭제 명령은 안내하지 않는다.
- 다음 안내(아직 실행 결과 없음): `sudo ip netns add biz` 후 `sudo ip netns exec biz ip -brief addr`. 생성 명령 오류 시 멈추고 오류를 확인한다.
- Windows 기록만 갱신했다. Ubuntu 파일 동기화·설치·네트워크 생성·삭제는 Codex가 수행하지 않았다.

### 2026-09-24 — 실습 2-1: biz 생성·내부 인터페이스 확인
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 결과가 아니다.
- 사용자는 기존 네임스페이스·브리지 조회에서 출력이 없음을 재확인한 뒤 아래 명령을 실행했다.

```text
$ sudo ip netns add biz
$ sudo ip netns exec biz ip -brief addr
lo               DOWN
```

- 결과와 의미: biz 생성과 내부 조회 성공. 새 네트워크 네임스페이스에는 lo만 DOWN 상태로 있으며 eth0와 IP 주소가 없다. Ubuntu 호스트의 eth0·IP 구성이 자동으로 복사되지 않음을 관찰했다.
- 다음 안내(아직 실행 결과 없음): `sudo ip netns exec biz ping -c1 -W1 8.8.8.8` 직후 `echo "종료코드=$?"`. 예상은 `Network is unreachable`과 종료 코드 2이며 실제 출력으로 확인한다.
- 2-2의 브리지·veth 연결은 아직 진행하지 않았다. biz는 생성된 상태로 다음 단계에 사용한다.

### 2026-09-24 — 실습 2-1: 외부 통신 실패 확인·절 완료
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 결과가 아니다.

```text
$ sudo ip netns exec biz ping -c1 -W1 8.8.8.8; echo "종료코드=$?"
ping: connect: Network is unreachable
종료코드=2
```

- 결과와 의미: 빈 biz에는 외부 통신용 인터페이스와 경로가 없어 통신을 시작하지 못한다. 예상한 실패와 종료 코드를 확인했으므로 2-1 완료다. 외부 서버 장애나 중간 방화벽 차단을 입증한 출력은 아니다.
- biz는 다음 절에 사용하기 위해 유지한다. br-lab·veth·db 생성, 주소 설정, 라우팅·NAT 변경은 아직 수행하지 않았다.
- 다음 시작 지점: 2-2의 브리지 생성부터 한 단계씩 진행. Day 2 전체 완료로 표시하지 않는다.

### 2026-09-24 — 2-1 개념 확인 및 실습 2-2 시작 안내
- 사용자가 2-1의 목적을 질문했다. 새 네트워크 공간이 Ubuntu의 인터페이스·IP·경로를 자동으로 물려받지 않음을 설명했다. 이번 실패는 인터페이스·IP도 없는 상태에서 관찰했으므로 경로만 누락된 경우를 따로 검증한 것은 아니라고 구분했다.
- 사용자가 2-2 진행을 요청했다. Codex는 PROGRESS·환경·Day 2 README·SESSION·가이드 2-2를 확인했다.
- 실행 위치: 사용자의 Ubuntu WSL2 `~/onprem-lab/day02`.
- 아래는 안내만 한 명령이며 실행 완료로 기록하지 않는다.

```bash
sudo ip link add br-lab type bridge
sudo ip addr add 10.42.0.1/24 dev br-lab
sudo ip link set br-lab up
ip addr show dev br-lab
```

- 확인할 내용: br-lab 생성, IPv4 10.42.0.1/24, 관리상 UP 플래그. 아직 활성 포트를 연결하지 않았으므로 NO-CARRIER·state DOWN이 표시될 수 있다. 오류가 나면 후속 명령을 멈추고 출력을 확인한다.
- 다음은 조회 결과 확인 후 veth 쌍으로 biz를 연결하는 단계다. db·방화벽 규칙 설정은 아직 안내하지 않았다.
- Codex는 Windows 기록만 수정했으며 Ubuntu 네트워크 명령을 직접 실행하지 않았다.

### 2026-09-24 — 실습 2-2: br-lab 설정 확인
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 결과가 아니다.
- 제공된 명령: `sudo ip addr add 10.42.0.1/24 dev br-lab`, `sudo ip link set br-lab up`, `ip addr show dev br-lab`.
- 주요 출력: `br-lab: <NO-CARRIER,BROADCAST,MULTICAST,UP> ... state DOWN`, `inet 10.42.0.1/24 scope global br-lab`.
- 생성 명령 자체는 이번 붙여넣기에 없지만 조회 결과로 br-lab의 존재와 주소·활성화 설정을 확인했다. 관리상 UP과 링크 동작 상태 DOWN을 구분하며, 아직 활성 포트를 연결하지 않은 현재 단계의 예상 상태다.
- 다음 안내(아직 실행 결과 없음):

```bash
sudo ip link add veth-biz type veth peer name eth0 netns biz
sudo ip link set veth-biz master br-lab
sudo ip link set veth-biz up
sudo ip netns exec biz ip addr add 10.42.0.10/24 dev eth0
sudo ip netns exec biz ip link set eth0 up
sudo ip netns exec biz ip link set lo up
sudo ip netns exec biz ping -c1 -W1 10.42.0.1
```

- 목표: veth 한쪽은 Ubuntu의 br-lab에, 다른 쪽은 biz 안의 eth0로 연결하고 10.42.0.10에서 10.42.0.1로 통신되는지 확인한다.
- 오류 발생 시 후속 명령을 멈추고 확인한다. db 생성과 네임스페이스 간 통신은 이후 단계다.

### 2026-09-24 — 실습 2-2: biz에서 브리지까지 ping 성공
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 결과가 아니다.

```text
$ sudo ip netns exec biz ping -c1 -W1 10.42.0.1
64 bytes from 10.42.0.1: icmp_seq=1 ttl=64 time=0.377 ms
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.377/0.377/0.377/0.000 ms
```

- 결과와 의미: biz에서 브리지 주소까지 통신 성공. 사용자는 설정 명령 각각의 출력 대신 최종 ping 결과를 제공했다. 안내 구성에서 연결이 동작함을 확인했으며 개별 IP·링크 속성을 별도 조회한 것은 아니다. 외부 통신이나 biz와 db 간 통신 완료로 해석하지 않는다.
- 다음 안내(아직 실행 결과 없음):

```bash
sudo ip netns add db
sudo ip link add veth-db type veth peer name eth0 netns db
sudo ip link set veth-db master br-lab
sudo ip link set veth-db up
sudo ip netns exec db ip addr add 10.42.0.20/24 dev eth0
sudo ip netns exec db ip link set eth0 up
sudo ip netns exec db ip link set lo up
sudo ip netns exec biz ping -c1 -W1 10.42.0.20
bridge link
```

- 가이드는 Docker가 FORWARD 기본 정책을 DROP으로 설정한 호스트를 가정해 허용 규칙을 먼저 추가한다. 현재 Docker Desktop 엔진과 사용자 Ubuntu는 실행 환경이 다르므로 Ubuntu의 정책이 DROP이라고 단정하지 않는다. 우선 통신 결과를 보고 실패하면 링크·주소·방화벽 상태를 확인한 뒤 필요한 규칙을 안내한다. 아직 iptables 규칙을 추가하지 않았다.
- 설정 명령 오류 시 멈추고 확인한다. ping 무응답 시에는 bridge link 조회 결과도 함께 확인한다.

### 2026-09-24 — 실습 2-2: biz에서 db까지 통신·절 완료
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 결과가 아니다.
- 사용자는 앞서 안내한 db 생성, veth-db 생성·br-lab 연결·활성화, db의 eth0에 10.42.0.20/24 부여, eth0·lo 활성화 명령을 실행한 결과를 제공했다. 표시된 설정 오류는 없다.

```text
$ sudo ip netns exec biz ping -c1 -W1 10.42.0.20
64 bytes from 10.42.0.20: icmp_seq=1 ttl=64 time=0.143 ms
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.143/0.143/0.143/0.000 ms
$ bridge link
4: veth-biz@eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 master br-lab state forwarding priority 32 cost 2
5: veth-db@eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 master br-lab state forwarding priority 32 cost 2
```

- 결과와 의미: 같은 대역의 biz와 db를 veth·브리지로 연결해 ping 왕복 성공. 두 호스트 쪽 포트 모두 br-lab에 속하며 forwarding 상태임을 확인했다. 2-2 완료로 판정한다.
- 이번 실습에서는 추가 iptables 허용 규칙 없이 통신했다. FORWARD 기본 정책이나 bridge netfilter 설정은 조회하지 않았으므로 성공 원인을 특정 설정으로 단정하지 않는다.
- biz·db·br-lab·veth는 다음 절을 위해 유지한다. 기본 경로·NAT 설정이나 외부 연결 검증은 아직 수행하지 않았다.
- 다음 시작 지점은 2-3의 biz 라우팅 테이블과 외부 통신 실패 관찰이다. 현재 요청 범위는 2-2까지이므로 다음 절의 실행 명령은 아직 안내하지 않았다.

### 2026-09-24 — 2-2 개념 확인 및 2-3 시작 안내
- 사용자와 2-2를 온프렘 업무 서버·DB 서버의 연결에 비유했다. 네임스페이스 설정은 분리됐지만 현재 같은 브리지·같은 대역에 연결돼 있으므로 서로 다른 보안망을 방화벽으로 분리한 구성은 아니라고 설명했다. 외부 통신은 2-2 이후 아직 시험하지 않았음을 구분했다.
- 사용자가 다음 절 진행을 요청해 2-3으로 범위를 확장했다. 가이드 2-3과 현재 기록을 확인했다.
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`.
- 아래 명령은 안내만 했으며 사용자 실행 결과 대기다.

```bash
sudo ip netns exec biz ip route
sudo ip netns exec biz ping -c1 -W1 1.1.1.1; echo "종료코드=$?"
```

- 관찰점: 같은 대역의 직접 연결 경로와 default 경로 유무. 가이드 예상은 `10.42.0.0/24 dev eth0 proto kernel scope link src 10.42.0.10`, `Network is unreachable`, 종료 코드 2다. 실제 출력으로 판단한다.
- 설정 변경은 아직 안내하지 않았다. 결과 확인 후 기본 경로 추가와 재시험을 안내한다. NAT·IP forwarding 변경은 다음 절 범위다.

### 2026-09-24 — 실습 2-3: 기본 경로 없는 상태 확인
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 결과가 아니다.

```text
$ sudo ip netns exec biz ip route
10.42.0.0/24 dev eth0 proto kernel scope link src 10.42.0.10
$ sudo ip netns exec biz ping -c1 -W1 1.1.1.1; echo "종료코드=$?"
ping: connect: Network is unreachable
종료코드=2
```

- 결과와 의미: 같은 대역의 직접 연결 경로만 있고 default 경로는 없다. 2-2에서 같은 대역 통신은 성공했지만 1.1.1.1로 보낼 경로가 없어 통신을 시작하지 못했다. 2-3의 변경 전 관찰 완료.
- 다음 안내(아직 실행 결과 없음):

```bash
sudo ip netns exec biz ip route add default via 10.42.0.1
sudo ip netns exec biz ip route
sudo ip netns exec biz ping -c1 -W1 1.1.1.1; echo "종료코드=$?"
```

- 추가할 경로의 의미: 더 구체적인 경로가 없는 목적지의 패킷을 Ubuntu 브리지 주소 10.42.0.1로 전달한다. 10.42.0.0/24 직접 연결 경로는 유지된다. IP forwarding·NAT·방화벽 규칙은 이 단계에서 변경하지 않는다.
- 가이드 예상은 default 경로 추가 후 100% packet loss·종료 코드 1이다. 실제 결과는 사용자 출력으로 확인하며, ping 실패만으로 호스트 밖 전달 여부나 차단 지점을 단정하지 않는다.
- 경로 추가 명령에서 오류가 나면 후속 명령을 멈추고 확인한다. 2-3은 아직 미완료다.

### 2026-09-24 — 실습 2-3: 기본 경로 추가 전후 비교·절 완료
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 결과가 아니다.

```text
$ sudo ip netns exec biz ip route add default via 10.42.0.1
$ sudo ip netns exec biz ip route
default via 10.42.0.1 dev eth0
10.42.0.0/24 dev eth0 proto kernel scope link src 10.42.0.10
$ sudo ip netns exec biz ping -c1 -W1 1.1.1.1; echo "종료코드=$?"
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
1 packets transmitted, 0 received, 100% packet loss, time 0ms
종료코드=1
```

- 결과와 의미: 기본 경로 추가 성공. 변경 전 Network is unreachable·종료 코드 2에서 변경 후 응답 미수신·손실 100%·종료 코드 1로 바뀌었다. 경로 없음과 응답 없음의 차이를 관찰했으므로 2-3 완료다.
- ping의 transmitted 표시는 요청 송신 시도를 나타내며, 이 출력만으로 패킷이 Ubuntu 밖까지 전달됐다고 단정하지 않는다. 호스트의 IP forwarding·방화벽·NAT 및 응답 경로 상태는 아직 조회하지 않았다.
- 실습에서 IP forwarding·NAT 설정은 아직 변경하지 않았다. 기존 호스트에 관련 설정이 전혀 없다고 확인한 것은 아니다.
- biz의 기본 경로와 biz·db·br-lab·veth는 유지한다. db에는 기본 경로를 추가하지 않았다.
- 다음 시작 지점은 2-4의 호스트 전달·NAT 설정과 외부 TCP 연결 확인이다. 현재 요청 범위인 2-3까지만 완료했으며 2-4 명령은 아직 안내하지 않았다.

### 2026-09-24 — 실습 2-4 시작: 호스트 설정 사전 조회 안내
- 사용자가 2-3의 실패 단계와 교훈을 질문했다. 기본 경로가 없을 때의 경로 선택 실패와 추가 후 응답 미수신을 구분하고, 후자만으로 실제 차단 지점을 확정할 수 없다고 설명했다.
- 후속 2-4 요청에 따라 가이드·진행·환경·Day 2 기록을 확인했다. Ubuntu에서 전달·NAT를 구성하기 전에 기존 설정을 확인한다.
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`, biz 내부가 아닌 Ubuntu 기본 네트워크 공간.
- 아래는 조회 안내이며 아직 결과는 없다. Codex가 Ubuntu에서 실행하거나 설정을 변경하지 않았다.

```bash
sysctl net.ipv4.ip_forward
ip route get 1.1.1.1
sudo iptables -S FORWARD
sudo iptables -t nat -S POSTROUTING
command -v nc
```

- 확인할 내용: 기존 전달 설정 0/1(정리 시 복구 기준), Ubuntu의 외부 경로·출발지 IP, FORWARD 정책·규칙, 기존 NAT 및 실습 규칙 중복 여부, TCP 연결 시험 도구 nc의 경로.
- 조회 결과에 따라 필요한 전달·NAT 설정을 안내하고 외부 TCP 443 연결을 확인할 예정이다. 아직 sysctl 쓰기·iptables 규칙 추가·TCP 시험은 안내하지 않았다.

### 2026-09-24 — 실습 2-4: 전달 비활성·iptables 명령 미검출
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`.
- 확인 주체: 사용자 제공 사전 조회 출력. Codex 직접 실행 결과가 아니다.

```text
$ sysctl net.ipv4.ip_forward
net.ipv4.ip_forward = 0
$ ip route get 1.1.1.1
1.1.1.1 via 172.18.48.1 dev eth0 src 172.18.60.227 uid 1000
    cache
$ sudo iptables -S FORWARD
sudo: iptables: command not found
$ sudo iptables -t nat -S POSTROUTING
sudo: iptables: command not found
$ command -v nc
/usr/bin/nc
```

- 결과: Ubuntu의 IPv4 전달이 비활성이다. 변경 전 값 0은 실습 정리 시 복구 기준으로 기록한다. 외부 목적지 경로는 eth0·게이트웨이 172.18.48.1·출발지 172.18.60.227이다. 경로 조회만으로 외부 연결 성공을 확인한 것은 아니다.
- sudo에서 iptables 명령을 찾지 못해 FORWARD·NAT 규칙 조회가 실패했다. 규칙이 없다는 뜻으로 해석하지 않는다. nc는 /usr/bin/nc에서 확인됐다.
- 다음 안내는 가이드에서 사용하는 iptables 패키지 설치와 재조회다. 아래 명령은 아직 실행 결과가 없으며 설치 완료로 기록하지 않는다.

```bash
sudo apt update
sudo apt install iptables
iptables --version
sudo iptables -S FORWARD
sudo iptables -t nat -S POSTROUTING
```

- apt 오류 시 후속 명령을 멈추고 출력을 확인한다. IP forwarding 활성화·NAT 추가는 아직 안내하지 않았다. Codex가 패키지를 설치하거나 Ubuntu 설정을 직접 변경하지 않았다.

### 2026-09-24 — 실습 2-4: iptables 실행 확인 및 NAT 설정 안내
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`.
- 확인 주체: 사용자 제공 출력. apt 설치 로그는 제공되지 않았지만 다음 출력으로 iptables 명령이 실행 가능해졌음을 확인했다.

```text
$ iptables --version
iptables v1.8.10 (nf_tables)
$ sudo iptables -S FORWARD
-P FORWARD ACCEPT
$ sudo iptables -t nat -S POSTROUTING
-P POSTROUTING ACCEPT
```

- 결과: 조회한 FORWARD 체인은 기본 정책 ACCEPT이고 개별 규칙이 없다. NAT POSTROUTING 체인에도 개별 규칙이 없다. 모든 nftables 규칙이나 Windows 방화벽까지 조회한 결과는 아니다.
- 다음 안내(아직 실행 결과 없음):

```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -s 10.42.0.0/24 ! -o br-lab -j MASQUERADE
sudo iptables -t nat -S POSTROUTING
sudo ip netns exec biz nc -zv -w3 1.1.1.1 443
echo "종료코드=$?"
```

- 전달 설정은 현재 실행 환경에 적용하며 영구 설정 파일은 수정하지 않는다. 기존 값은 0이다. NAT는 실습 대역에서 br-lab 이외로 나가는 트래픽에 적용하며 FORWARD 규칙은 추가하지 않는다.
- 기대 결과: sysctl 값 1, POSTROUTING의 실습 MASQUERADE 규칙 한 개, TCP 연결 succeeded 및 종료 코드 0. 성공하더라도 해당 IP·포트의 TCP 연결 검증이며 DNS·HTTPS 응용 통신 전체 검증은 아니다.
- 설정 명령 오류 시 멈춘다. NAT 추가 명령은 한 번만 실행해 중복을 피한다. Codex는 Ubuntu 설정을 직접 변경하지 않았다.

### 2026-09-24 — 실습 2-4: NAT 설정·외부 TCP 연결 성공·절 완료
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 결과가 아니다.

```text
$ sudo sysctl -w net.ipv4.ip_forward=1
net.ipv4.ip_forward = 1
$ sudo iptables -t nat -A POSTROUTING -s 10.42.0.0/24 ! -o br-lab -j MASQUERADE
$ sudo iptables -t nat -S POSTROUTING
-P POSTROUTING ACCEPT
-A POSTROUTING -s 10.42.0.0/24 ! -o br-lab -j MASQUERADE
$ sudo ip netns exec biz nc -zv -w3 1.1.1.1 443
Connection to 1.1.1.1 443 port [tcp/https] succeeded!
$ echo "종료코드=$?"
종료코드=0
```

- 결과: IP forwarding 활성화, 실습 대역 MASQUERADE 규칙 한 개, biz에서 1.1.1.1:443 TCP 연결 성공을 확인해 2-4 완료로 판정한다. DNS·TLS·HTTP 검증 또는 외부 ping 성공을 의미하지 않는다.
- 앞서 확인한 경로를 기준으로 실습 NAT는 biz 출발지 주소를 Ubuntu eth0의 172.18.60.227로 변환하는 구성이다. 변환 전후 패킷을 캡처한 결과는 아니며 Windows·상위 네트워크의 추가 주소 변환 여부는 조회하지 않았다.
- 현재 biz·db·br-lab·veth, biz 기본 경로, 실습 NAT 및 ip_forward=1을 유지한다. db 기본 경로는 추가하지 않았다. FORWARD 허용 규칙도 별도로 추가하지 않았다.
- 최종 정리 시 실습 NAT 한 개와 실습 네트워크를 제거하고, 다른 용도로 변경되지 않았는지 확인한 뒤 ip_forward를 사전 값 0으로 복구한다. 아직 정리는 실행하지 않았다. 영구 sysctl·방화벽 저장 설정도 추가하지 않았다.
- 다음 시작 지점은 2-5의 db 리스너와 tcpdump 패킷 관찰이다. 해당 절은 아직 시작하지 않았다.

### 2026-09-24 — 실습 2-5 시작: 관찰 도구·포트 사전 조회 안내
- 사용자 요청에 따라 가이드 2-5와 진행·환경·Day 2 기록을 확인했다. 이번에는 외부 연결 대신 같은 브리지의 biz→db TCP 5432 요청·응답을 관찰한다. 실제 DB를 설치하지 않고 nc 리스너로 접속을 받는다.
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`.
- 아래는 조회 안내이며 아직 실행 결과가 없다. Codex는 Ubuntu 명령을 직접 실행하지 않았다.

```bash
command -v tcpdump nc timeout ss
tcpdump --version
sudo ip netns exec db ss -ltnp 'sport = :5432'
```

- 확인할 내용: 관찰·접속·제한 시간·소켓 조회 도구의 경로, tcpdump 버전, db의 TCP 5432가 이미 사용 중인지. 리스너가 없다면 ss는 표 머리글만 표시할 수 있다.
- 준비 확인 후 db에 리스너를 실행하고 tcpdump와 biz의 접속을 조합해 SYN·SYN-ACK를 관찰한다. 리스너 실행·패킷 캡처는 아직 안내하지 않았다.

### 2026-09-24 — 실습 2-5: tcpdump 미검출·리스너 없음 확인
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 결과가 아니다.
- `command -v tcpdump nc timeout ss`는 `/usr/bin/nc`, `/usr/bin/timeout`, `/usr/bin/ss`만 출력했다. `tcpdump --version`은 `Command 'tcpdump' not found` 및 apt/snap 설치 안내를 출력했다. 안내에 표시된 버전을 실제 설치 버전으로 기록하지 않는다.
- `sudo ip netns exec db ss -ltnp 'sport = :5432'`는 표 머리글만 출력했다. db의 TCP 5432 리스너는 조회되지 않았다.
- 다음 안내(아직 실행 결과 없음): `sudo apt install tcpdump` 후 `tcpdump --version`. 앞서 iptables 설치 준비에서 apt update를 안내했으므로 우선 설치를 시도하고 오류 발생 시 확인한다.
- 설치 오류 시 멈추고 출력 확인. 리스너 실행·패킷 캡처는 아직 진행하지 않았다.

### 2026-09-24 — 실습 2-5: tcpdump 실행 확인·리스너 안내
- 확인 주체: 사용자 제공 Ubuntu `tcpdump --version` 출력. tcpdump 4.99.4, libpcap 1.10.4 (with TPACKET_V3), OpenSSL 3.0.13 30 Jan 2024를 확인했다. apt 설치 로그는 제공되지 않았지만 명령 미검출은 해소됐다.
- 다음 안내 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`. 아래 명령은 아직 실행 결과가 없다.

```bash
sudo ip netns exec db sh -c 'nc -l -k 10.42.0.20 5432 >/dev/null & echo "리스너 PID=$!"'
sudo ip netns exec db ss -ltnp 'sport = :5432'
```

- nc는 실제 DB 대신 TCP 접속만 받는 연습용 리스너다. -l은 접속 대기, -k는 연결 종료 후 계속 대기, &는 백그라운드 실행이다. stdout만 숨기고 오류는 표시한다.
- 기대 결과는 PID 출력과 ss의 LISTEN·10.42.0.20:5432·nc 프로세스다. PID 출력만으로 성공을 판정하지 않는다. 확인된 PID는 이 절 종료 시 해당 리스너만 정리하는 데 사용한다.
- 조회 확인 후 tcpdump 관찰과 biz의 접속을 안내한다. 아직 패킷 캡처는 진행하지 않았다.

### 2026-09-24 — 실습 2-5: 리스너 확인·패킷 관찰 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. 리스너 실행 명령은 PID=2129를 출력했고, `ss -ltnp 'sport = :5432'`는 `LISTEN ... 10.42.0.20:5432 ... users:(("nc",pid=2129,fd=3))`를 표시했다. db 리스너 실행을 확인했다.
- 다음 안내: 같은 Ubuntu 터미널에 아래 블록을 한 번에 실행한다. 아직 실행 결과는 없다.

```bash
sudo -v
sudo ip netns exec db timeout 10 tcpdump -nn -l -i eth0 -c 2 'tcp port 5432' &
lab_capture_pid=$!
sleep 1
sudo ip netns exec biz nc -zv -w3 10.42.0.20 5432
echo "접속 종료코드=$?"
wait "$lab_capture_pid"
```

- sudo 인증을 먼저 갱신하고 db의 eth0에서 TCP 5432만 관찰한다. 패킷 2개 또는 최대 10초 후 캡처를 종료하며, nc 접속에는 3초 제한을 둔다. wait는 이번 캡처 작업만 기다린다.
- 확인할 결과: biz→db의 Flags [S], db→biz의 Flags [S.], nc succeeded·접속 종료 코드 0. 캡처는 첫 두 패킷이므로 세 번째 ACK까지 출력할 것을 요구하지 않는다. 사용자 출력으로 실제 관찰 결과를 판정한다.
- 리스너 PID 2129는 캡처 후에도 유지한다. 관찰 완료 뒤 해당 프로세스의 정리를 안내한다. 이번에는 네트워크·NAT·전달 설정을 변경하지 않는다.

### 2026-09-24 — 실습 2-5: SYN·SYN-ACK 관찰 성공
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 결과가 아니다. 앞서 안내한 캡처 블록을 실행했고 캡처 작업 번호는 [1], PID는 2136이었다.

```text
Connection to 10.42.0.20 5432 port [tcp/postgresql] succeeded!
접속 종료코드=0
22:43:22.114615 IP 10.42.0.10.45566 > 10.42.0.20.5432: Flags [S], seq 27501029, win 64240, options [mss 1460,sackOK,TS val 1626502515 ecr 0,nop,wscale 7], length 0
22:43:22.114691 IP 10.42.0.20.5432 > 10.42.0.10.45566: Flags [S.], seq 1257938297, ack 27501030, win 65160, options [mss 1460,sackOK,TS val 78116929 ecr 1626502515,nop,wscale 7], length 0
2 packets captured
6 packets received by filter
0 packets dropped by kernel
[1]+ Done sudo ip netns exec db timeout 10 tcpdump -nn -l -i eth0 -c 2 'tcp port 5432'
```

- 결과: db의 eth0에서 biz 임시 포트 45566의 접속 요청 SYN과 db 5432의 응답 SYN-ACK를 확인했다. nc의 succeeded·종료 코드 0으로 TCP 연결 성공도 확인했다. -c 2에 따라 캡처는 두 패킷으로 끝났고 작업 종료가 표시됐다.
- postgresql은 포트 5432에 대한 서비스 이름 표기이며 실제 PostgreSQL 서버를 실행하거나 DB 질의를 수행한 것은 아니다. 응답 프로그램은 nc다.
- 핵심 관찰은 완료했으며 이 절에서 실행한 리스너 정리 확인만 남았다. 다음 안내(아직 결과 없음):

```bash
sudo kill 2129
sudo ip netns exec db ss -ltnp 'sport = :5432'
```

- 직전 ss 조회에서 확인한 이번 실습의 nc PID 2129만 종료한다. 삭제·종료 오류가 나면 결과를 확인하며 다른 프로세스를 임의로 종료하지 않는다. ss가 표 머리글만 출력하면 LISTEN 해제를 확인한다. 네임스페이스·브리지·NAT·전달 설정은 유지한다.

### 2026-09-24 — 실습 2-5: 리스너 정리·절 완료
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 결과가 아니다.

```text
$ sudo kill 2129
$ sudo ip netns exec db ss -ltnp 'sport = :5432'
State Recv-Q Send-Q Local Address:Port Peer Address:Port Process
```

- 결과: kill 명령에 오류가 표시되지 않았고 db TCP 5432의 LISTEN 항목이 사라졌다. nc 리스너 정리를 확인했다. 앞서 SYN·SYN-ACK 및 접속 성공, 캡처 작업 종료를 확인했으므로 2-5 전체 완료로 판정한다.
- 리스너 PID 2129는 이후 종료 대상으로 재사용하지 않는다. 실습 네트워크·biz 기본 경로·NAT·ip_forward=1은 유지한다. 최종 네트워크 정리는 아직 하지 않았다.
- 다음 시작 지점은 2-6이다. Docker Desktop 엔진과 Ubuntu의 네트워크·PID 관찰 위치가 다를 수 있으므로 가이드의 호스트 ip/iptables/nsenter 명령을 실행하기 전에 관찰 위치를 확인한다. 이번에는 2-6을 시작하지 않았다.

### 2026-09-24 — 실습 2-6 시작: Docker 사전 조회 안내
- 사용자 요청으로 2-6에 진입했다. 진행·환경·Day 2 기록·가이드 2-6을 확인했다. 앞선 수동 구성과 Docker가 만드는 브리지·veth·경로·NAT·DNS를 비교할 예정이다.
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`. Docker CLI로 연결된 엔진을 조회한다.
- 아래 명령은 안내만 했으며 실행 결과 대기다. 생성·삭제·다운로드는 수행하지 않는다.

```bash
docker info --format 'Name={{.Name}} OS={{.OperatingSystem}} Type={{.OSType}}'
docker network ls
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Networks}}'
docker image inspect alpine:3.20 nicolaka/netshoot:v0.13 --format '{{join .RepoTags ", "}}'
```

- 확인할 내용: 엔진 응답·Docker Desktop 환경, demo-net과 who1·who2 이름의 기존 사용 여부, 컨테이너용 Alpine 및 관찰용 netshoot 이미지 존재. 미존재 이미지 오류는 다운로드 완료로 해석하지 않는다.
- Docker Desktop의 엔진과 사용자 Ubuntu는 관찰 위치를 구분해야 한다. 가이드의 Ubuntu 호스트 ip/iptables 명령이나 Docker PID를 이용한 nsenter를 그대로 적용하지 않고, 실제 엔진 정보에 따라 관찰 방법을 정한다.
- 아직 demo-net·who1·who2 생성은 안내하지 않았다. 기존 수동 네트워크·NAT는 유지한다. 가이드의 sleep 300은 대화 중 종료될 수 있으므로 생성 단계에서 학습 시간에 맞는 실행 시간을 정한다.

### 2026-09-24 — 실습 2-6: Docker WSL 연동 오류
- 확인 주체: 사용자 제공 Ubuntu 출력. 사전 조회 네 명령 모두 `The command 'docker' could not be found in this WSL 2 distro.`와 Docker Desktop의 WSL integration 활성화 안내를 출력했다.
- 결과: 엔진·네트워크·컨테이너·이미지 상태를 아직 조회하지 못했다. 기존 이미지나 컨테이너가 없다는 증거는 아니다. demo-net·who1·who2는 이번 실습에서 생성하지 않았다.
- 가능한 원인: Docker Desktop 미실행·준비 미완료 또는 Ubuntu WSL 연동 문제. 현재 프로세스·설정은 직접 조회하지 않았으므로 원인을 확정하지 않는다. 2026-09-23에는 Desktop 실행 후 유사한 문제가 해소된 기록이 있다.
- 공식 문서 확인: https://docs.docker.com/desktop/features/wsl/ . Windows에서 Desktop 실행 및 Settings > Resources > WSL Integration의 배포판 연동 경로를 확인했다.
- 다음 안내(아직 결과 없음): Windows 시작 메뉴에서 Docker Desktop 실행 → 엔진 준비 완료 확인 → 기존 Ubuntu 터미널에서 `docker version`. 먼저 실행 상태를 확인하고, 동일 오류가 지속되면 Ubuntu WSL Integration 설정을 확인한다.
- 이번 단계에서는 apt로 별도 Docker Engine을 설치하거나 WSL을 종료·초기화하지 않는다. 기존 Ubuntu 실습 네트워크·NAT·전달 설정은 유지하며 현재 상태를 새로 검증한 것은 아니다.

### 2026-09-24 — 실습 2-6: Docker 연동 복구 확인
- 확인 주체: 사용자 제공 Ubuntu `docker version` 출력. Codex가 Desktop을 실행하거나 Ubuntu에서 직접 재조회한 결과가 아니다.
- Client/Engine 29.8.0, API 1.56(서버 최소 1.40), linux/amd64, Context default, Server Docker Desktop 4.92.0 (240144)를 확인했다. Client·Server 모두 응답하므로 현재 명령 실행·엔진 접근은 정상이다. 사용자가 수행한 Windows 조작의 상세는 별도 제공되지 않았다.
- 다음 안내는 앞서 실패한 나머지 조회다. 아직 실행 결과가 없다.

```bash
docker network ls
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Networks}}'
docker image inspect alpine:3.20 nicolaka/netshoot:v0.13 --format '{{join .RepoTags ", "}}'
```

- Docker Desktop 여부는 version에서 확인했으므로 같은 목적의 info 조회는 반복하지 않는다. demo-net·who1·who2 이름과 이미지 존재를 확인한 뒤 생성 단계로 진행한다. 아직 실습 컨테이너·네트워크를 생성하지 않았다.

### 2026-09-24 — 실습 2-6: 사전 조회 확인·생성 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. 네트워크 목록은 bridge·host·none 및 기존 koica-oda-local-test_default다. 컨테이너 목록은 koica-oda-local-test-oda-app-1(Exited (143) 12 days ago) 한 개다. demo-net·who1·who2는 조회되지 않았다.
- 이미지 조회에서 alpine:3.20과 nicolaka/netshoot:v0.13을 확인했다. 기존 프로젝트 네트워크·컨테이너는 실습 대상이 아니다. 이번 확인은 생성·삭제를 수행한 결과가 아니다.
- 다음 안내(아직 실행 결과 없음):

```bash
docker network create demo-net
docker run -d --rm --name who1 --network demo-net alpine:3.20 sleep 3600
docker network inspect demo-net --format 'Driver={{.Driver}} IPAM={{json .IPAM.Config}}'
docker exec who1 ip addr
docker exec who1 ip route
```

- 실행 위치: 사용자 Ubuntu WSL2 터미널에서 Docker Desktop 엔진에 요청한다. 가이드의 sleep 300 대신 설명·출력 확인 시간을 확보하도록 sleep 3600을 사용한다. --rm이므로 프로세스 종료 시 컨테이너가 자동 제거되며 필요 시 상태를 재확인한다.
- 관찰 목표: Docker가 bridge 네트워크 대역·게이트웨이를 정하고, 컨테이너에 eth0·IP·직접 연결 경로·기본 경로를 자동 설정하는지 실제 출력으로 확인한다. 주소를 가이드 예시 값으로 단정하지 않는다. 생성 오류 시 후속 명령을 멈춘다.
- Ubuntu 호스트의 br-lab과 Docker Desktop 엔진의 demo-net은 별도 구성이다. Docker 쪽 브리지·veth·NAT 관찰과 DNS 비교는 후속 단계로 남긴다. 아직 who2는 생성하지 않았다.

### 2026-09-24 — 실습 2-6: Docker 자동 구성 확인·엔진 내부 조회 안내
- 확인 주체: 사용자 제공 Ubuntu 출력. demo-net ID `0256008dc5469c41348d647848f828025bfe42f649f0e231ef566e2de2567378`, who1 ID `daa6f5865d91572f756ce3cfdb2f1a8aa9390dead07b18bf888fbae74e56e904` 생성 확인.
- network inspect: Driver=bridge, Subnet=172.19.0.0/16, Gateway=172.19.0.1. who1은 lo가 활성이고 eth0@if7에 172.19.0.2/16, UP·LOWER_UP이 표시됐다.
- who1 경로는 `default via 172.19.0.1 dev eth0` 및 `172.19.0.0/16 dev eth0 scope link src 172.19.0.2`. 사용자가 IP·기본 경로를 직접 추가하지 않아도 Docker가 설정함을 확인했다.
- 다음은 Docker 엔진 쪽 브리지·veth·NAT 관찰이다. Docker Desktop 네트워킹 공식 문서와 netshoot README의 namespace 진단 방식을 참고했다: https://docs.docker.com/desktop/features/networking/ , https://github.com/nicolaka/netshoot . 아래는 이 환경에 맞춘 조회 안내이며 아직 실행 결과가 없다.

```bash
docker run --rm --network none --privileged --pid=host nicolaka/netshoot:v0.13 nsenter -t 1 -n sh -c '
ip -brief link show type bridge
bridge link
iptables -t nat -S POSTROUTING
'
```

- Ubuntu에서 Docker Desktop 엔진에 임시 관찰용 컨테이너 실행을 요청한다. --pid=host와 nsenter는 엔진 호스트 PID 1의 네트워크 공간을 관찰하기 위한 것이며 --privileged는 해당 공간 진입·규칙 조회에 필요한 권한을 제공한다. 내부 명령은 조회뿐이다. --network none으로 진단 컨테이너의 불필요한 브리지 연결을 피하고 --rm으로 종료 시 제거한다.
- 결과에서 demo-net에 해당하는 브리지와 who1의 veth 포트, 172.19.0.0/16 대상 MASQUERADE를 확인할 예정이다. 접근 제한·규칙 미표시가 있으면 실제 출력으로 관찰 위치와 방화벽 백엔드를 진단한다. 호스트 보안 설정 변경은 안내하지 않았다.
- DNS 비교와 who2 생성은 아직 미진행이다. 기존 다른 프로젝트의 네트워크·컨테이너는 변경하지 않는다.

### 2026-09-24 — 실습 2-6: Docker 브리지·veth·NAT 확인
- 확인 주체: 사용자 제공 Ubuntu 터미널 출력. 안내한 netshoot 임시 컨테이너로 Docker 엔진의 네트워크 공간을 조회했다. Codex 직접 실행 결과가 아니다.
- demo-net의 브리지는 `br-0256008dc546`, 상태 UP·LOWER_UP이다. 네트워크 ID 앞 12자리와 일치한다. 호스트 쪽 `vethef0bed3`(인덱스 7)가 이 브리지에 소속돼 forwarding 상태이며, 앞서 who1의 eth0@if7과 연결 관계가 일치한다.
- NAT에서 `-A POSTROUTING -s 172.19.0.0/16 ! -o br-0256008dc546 -j MASQUERADE`를 확인했다. 수동 구성의 실습 대역·br-lab 규칙과 같은 형태다. 이 외 LOCAL 출발지용 규칙, docker0·기존 프로젝트 브리지의 규칙도 조회됐으며 변경하지 않았다.
- docker0와 기존 프로젝트 브리지는 NO-CARRIER·관리상 UP·동작 상태 DOWN이다. 이 표시만으로 장애로 판정하지 않는다. 진단 명령은 완료돼 터미널로 돌아왔으며 --rm 컨테이너의 별도 목록 재조회는 하지 않았다.
- 다음 안내(아직 실행 결과 없음):

```bash
docker run -d --rm --name who2 alpine:3.20 sleep 3600
docker exec who1 cat /etc/resolv.conf
docker exec who2 cat /etc/resolv.conf
docker exec who1 nslookup who1
docker exec who2 nslookup who2
```

- who2는 --network를 생략해 기본 bridge에 연결한다. who1은 demo-net을 유지한다. 먼저 DNS 설정을 비교하고 각각 자신의 컨테이너 이름을 DNS로 조회한다. 서로 다른 네트워크 사이의 통신 시험은 아니다.
- 가이드 예상: who1은 Docker DNS 127.0.0.11을 사용해 who1 이름을 자신의 IP로 해석하며, 기본 bridge의 who2에는 컨테이너 이름 자동 DNS 해석이 제공되지 않는다. who2의 실제 nameserver 주소·응답은 출력으로 확인한다. 실패 출력도 비교 자료로 기록한다.
- who2 생성 오류가 나면 멈추고 확인한다. 기존 수동 네트워크와 Docker의 다른 프로젝트는 변경하지 않는다.

### 2026-09-24 — 실습 2-6: DNS 비교·절 완료
- 확인 주체: 사용자 제공 Ubuntu 출력. who2 ID `b775f30092654ecdcac584873642340798e7db8d997150f6820f616a2a2c3ad5` 생성 확인. --network 생략으로 기본 bridge에 연결한 명령을 실행했다.
- who1의 resolv.conf: `nameserver 127.0.0.11`, `options ndots:0`, internal resolver, ExtServers=[host(192.168.65.7)]. who2: `nameserver 192.168.65.7`, legacy. 실제 Docker Desktop DNS 주소는 가이드 예시의 8.8.8.8/8.8.4.4와 다르다.

```text
$ docker exec who1 nslookup who1
Server: 127.0.0.11
Address: 127.0.0.11:53
Non-authoritative answer:
Name: who1
Address: 172.19.0.2
$ docker exec who2 nslookup who2
Server: 192.168.65.7
Address: 192.168.65.7:53
** server can't find who2: NXDOMAIN
```

- 결과: demo-net의 who1은 Docker 내장 DNS로 이름을 자기 IP로 해석했다. 기본 bridge의 who2 이름은 사용한 DNS에서 존재하지 않는다는 응답을 받았다. NXDOMAIN은 이 이름의 DNS 조회 실패이며 컨테이너 실행 실패나 인터넷 전체 단절의 증거가 아니다.
- Docker 자동 IP·경로, 엔진 브리지·veth·NAT와 DNS 차이까지 확인해 2-6 완료로 판정한다. 서로 다른 네트워크 간 연결이나 실제 DB 통신을 시험한 것은 아니다.
- who1·who2는 각각 --rm·sleep 3600으로 실행했고 demo-net도 유지한다. 최종 정리 시 실제 잔존 여부를 확인해 이번 실습 자원만 제거한다. 기존 koica 프로젝트 자원은 정리 대상이 아니다.
- 다음 시작 지점은 2-7의 메모리 제한·cgroup 관찰이다. 2-7과 Day 전체 정리·자기점검은 아직 시작하지 않았다.

### 2026-09-24 — 실습 2-7 시작: 메모리 제한·cgroup 조회 안내
- 사용자 요청으로 2-7 가이드와 진행·환경·Day 2 기록을 확인했다. 네임스페이스가 네트워크 등의 관찰 범위를 분리하는 기능이라면 cgroup은 프로세스 집단의 자원 사용을 제어하는 기능임을 설명한다.
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`에서 Docker Desktop 엔진에 명령한다.
- 아래 명령은 안내만 했으며 아직 실행 결과가 없다. Codex가 컨테이너를 직접 생성한 것은 아니다.

```bash
docker run -d --rm --name lim --memory=64m alpine:3.20 sleep 3600
docker stats --no-stream lim
docker exec lim sh -c 'cat /sys/fs/cgroup/memory.max 2>/dev/null || cat /sys/fs/cgroup/memory/memory.limit_in_bytes'
```

- --memory=64m은 메모리 상한 64MiB를 지정한다. 64MiB를 즉시 사용하거나 전용으로 예약한다는 의미가 아니다. 실제 사용량은 stats에서 별도로 확인한다. 대화 시간을 고려해 가이드 sleep 300 대신 3600을 사용한다.
- 기대 출력: stats의 MEM USAGE / LIMIT에 사용량 / 64MiB, cgroup 상한 파일에서 67108864(64×1024×1024) 바이트. cgroup v2 memory.max를 먼저 읽고 없으면 v1 경로를 읽는다.
- 컨테이너 생성 오류 시 멈추고 확인한다. 이름 충돌 시 기존 lim을 임의로 삭제하지 않는다. 이번 실습은 제한 설정·값 관찰이며 메모리 소진·OOM 재현은 수행하지 않는다.

### 2026-09-24 — 실습 2-7: 메모리 상한 확인·절 완료
- 실행 위치: 사용자 Ubuntu WSL2 `~/onprem-lab/day02`에서 Docker Desktop 엔진에 명령.
- 확인 주체: 사용자 제공 출력. Codex 직접 실행 결과가 아니다.
- `docker run -d --rm --name lim --memory=64m alpine:3.20 sleep 3600`으로 컨테이너 ID `98f480bce73ac1cd1a8f7f468aec65f1c3e62e4d62e3958688c63a8b05199520` 생성 확인.

```text
$ docker stats --no-stream lim
CONTAINER ID   NAME   CPU %   MEM USAGE / LIMIT   MEM %   NET I/O      BLOCK I/O   PIDS
98f480bce73a   lim    0.00%   416KiB / 64MiB      0.63%   872B / 126B  0B / 0B     1
$ docker exec lim sh -c 'cat /sys/fs/cgroup/memory.max 2>/dev/null || cat /sys/fs/cgroup/memory/memory.limit_in_bytes'
67108864
```

- 결과: Docker의 메모리 상한 64MiB와 cgroup 값 67108864바이트(64×1024×1024)가 일치한다. stats의 사용량은 조회 순간 416KiB이며 상한과 구분한다. 2-7 완료로 판정한다.
- 이 명령은 v2 경로를 우선하고 실패 시 v1 경로로 대체하므로 출력 숫자만으로 cgroup 버전을 별도 판정하지 않는다. 실제 메모리 소진·OOM 동작은 시험하지 않았다.
- 실습 2-1~2-7은 완료했지만 Day 전체 정리·자기점검은 남아 있다. lim·who1·who2는 --rm·sleep 3600이므로 정리 시 실제 잔존 상태를 확인한다. demo-net과 Ubuntu의 biz·db·br-lab·veth·실습 NAT·ip_forward=1도 아직 최종 정리하지 않았다.
- 다음은 사용자와 자원 정리·최종 자기점검을 진행할 범위를 정한 뒤 이어 간다. 기존 다른 프로젝트 자원은 정리 대상이 아니며 ip_forward 사전 값은 0이다. 이번 turn에는 정리 명령을 실행하거나 안내하지 않았다.

## 오류와 해결
- 2-1의 `Network is unreachable`·종료 코드 2는 의도된 관찰 결과다. 설치 오류나 예기치 않은 실습 실패로 처리하지 않는다.
- 2-4 사전 조회의 `sudo: iptables: command not found`는 후속 사용자 출력의 v1.8.10 (nf_tables) 및 규칙 조회 성공으로 해소 확인했다. apt 로그 자체는 미제공이다.
- 2-5의 tcpdump 명령 미검출은 후속 사용자 출력의 tcpdump 4.99.4 실행 성공으로 해소 확인했다.
- 2-6의 Docker WSL 연동 안내 오류는 후속 사용자 docker version 출력의 Client·Server 정상 응답으로 해소 확인했다. 이후 네트워크·컨테이너·이미지 재조회도 성공했다.

## 배운 내용과 질문

### 네트워크 공간 분리와 보안망 분리
biz·db는 독립된 네트워크 설정을 갖지만 이번에는 같은 브리지·같은 대역에 연결했다. 실제 업무망·DB망을 방화벽 정책으로 나눈 구성까지 만든 것은 아니다. 이름이 db여도 실제 DB 서버를 설치한 것은 아니다.

### 경로·전달·NAT·진단
기본 경로는 “어디에 맡길지”, IP forwarding은 “호스트가 넘겨줄지”, NAT는 “이번 구성에서 출발지 주소를 어떻게 바꿀지”를 담당한다. 패킷이 어느 구간에서 사라졌는지는 ping 손실만으로 확정할 수 없다. 올바른 위치·필터에서 요청 도착과 응답 송신을 관찰해 조사 범위를 좁힌다. 이번 외부 NAT는 Ubuntu의 사설 eth0 주소로 변환하는 구성이며 상위 Windows/망의 추가 NAT는 조회하지 않았다.

### Docker 자동화와 원하는 구성
사용자가 network create·run에 네트워크와 연결 대상을 지정하면 Docker 엔진이 OS 기능으로 브리지·veth·IP·경로·NAT 등을 구성한다. 모든 세부 커맨드를 사용자가 실행할 필요가 없다. 이번 명령형 요청과 설정 파일에 원하는 구성을 작성하는 Compose 방식은 구분한다. 자동 생성이 외부 수동 변경을 항상 감시·복구한다는 보장은 아니다. Docker는 네트워크 전용 서비스가 아니라 이미지·컨테이너 실행·저장소 연결·자원 제한을 관리하는 플랫폼이다. 이 설명은 이번 bridge 구성에 관한 것이며 모든 네트워크 드라이버가 동일한 부품·NAT를 쓴다는 뜻은 아니다.

### vSphere·VM과 Docker·컨테이너
vSphere는 VM 인프라를 운영하는 플랫폼이다. ESXi는 물리 서버에서 VM을 실행하고 vCenter는 여러 호스트와 VM을 중앙 관리한다. VM은 자체 게스트 OS·커널을 갖는다. 그 Linux VM 안에 Docker를 설치하면 여러 컨테이너가 VM의 커널을 공유하면서 각자의 실행 환경을 갖는다. 예: 물리 서버 → ESXi → Linux VM → Docker → 에이전트 컨테이너. VM의 메모리 크기 조정과 특정 컨테이너의 cgroup 상한 조정은 다른 계층의 작업이다. 현재 PC에서는 vSphere VM을 만들지 않았으며 Day 1 vm-agent-01·02도 VM 역할을 흉내 낸 컨테이너였다.

### 최종 자기점검
개념별 질의응답은 진행했으나 가이드 5문항을 사용자 답변으로 별도 평가하지 않았다. 복습할 내용은 NAT의 출발지 관찰 위치, 경로 없음과 응답 없음, SYN만 보일 때의 진단, Docker DNS 차이, cgroup과 메모리 상한이다. OOM 재현은 하지 않았다.

## 가이드와 실제 환경의 차이
공통 환경은 [환경 기록](../docs/environment.md)을 참고한다. 2-2에서 추가 FORWARD 허용 규칙 없이 biz→db ping이 성공했다. 후속 2-4 조회에서 iptables v1.8.10 (nf_tables), FORWARD 기본 ACCEPT·개별 규칙 없음을 확인했다. bridge netfilter 설정은 미조회다. 변경 전 ip_forward는 0이었으며 1로 설정하고 실습 NAT 한 개를 추가한 뒤 외부 TCP 연결이 성공했다.

## 다음에 이어 할 지점
실습 2-1~2-7 및 정리 완료. 컨테이너 세 개·demo-net 삭제, 빈 네임스페이스·브리지 목록, 실습 NAT 제거, ip_forward=0 복구를 확인했다. 별도 자기점검 또는 Day 3은 사용자 요청에 따라 진행한다. Day 3은 시작하지 않았다.

## 2026-09-25 — 세션 종료·기록 정리 및 PR 준비

- 사용자가 Day 2 기록 정리와 GitHub PR 생성을 요청했다. 사용자 실행 결과를 요약·증거·환경 차이·질의응답으로 정리한다. 실행한 명령과 당시 안내만 한 명령을 구분한다.
- 사용자 제공 정리 출력에서 who1·who2·lim·demo-net 삭제를 확인했고 ip netns list는 빈 출력이었다. 나머지 정리 명령은 오류를 숨겼으므로 echo의 “정리 완료”만으로 NAT·브리지 제거를 모두 확정하지 않는다. ip_forward 복구 명령도 포함되지 않았다.
- 추가 안내(결과 대기): Ubuntu에서 `sudo sysctl -w net.ipv4.ip_forward=0`, `sudo iptables -t nat -S POSTROUTING`, `ip -brief link show type bridge`. Codex가 대신 실행하지 않았다.
- 첫 추가 확인은 세 명령이 줄바꿈·구분자 없이 붙어 `sysctl: invalid option -- 't'`로 실패했다. 세미콜론으로 구분한 한 줄을 재안내했으며 설정 복구 성공으로 기록하지 않았다.
- Git 원격 갱신으로 Day 1 PR #3의 main 병합 커밋 `abb2ffb`를 확인했다. 이 main과 기존 Day 1 브랜치 HEAD의 파일 트리는 동일했다. 최신 main에서 `codex/day02-results`를 만들고 현재 Day 2 변경을 유지했다.
- GitHub CLI 인증은 실패했으며 브라우저의 로그인된 GitHub 화면을 확인했다. PR 생성 결과와 검증 결과는 아래에 이어 기록한다.
- 후속 사용자 출력으로 정리 완료 확인: 세미콜론으로 구분해 재실행한 결과 `net.ipv4.ip_forward = 0`, NAT POSTROUTING은 `-P POSTROUTING ACCEPT`만 출력, 브리지 목록은 빈 출력이었다. 앞선 삭제 결과와 합쳐 Day 2 실습·정리 완료로 갱신했다. 가이드 자기점검 5문항은 별도 평가하지 않았다.
- Codex의 Windows 문서 검증: 변경 문서·증거 7개 파일의 LF와 로컬 링크 45개 존재 확인, `git diff --check` 통과. `day02/netns-lab.sh`의 SHA-256은 `8AD5DC88E164BFC2C5725731B97754FC1495B8343A8DFEEA9F308C2B55972DEE`로 기존과 동일하다. 문서만 변경했으므로 Ubuntu 실습 재실행이나 가이드 재빌드는 하지 않았다.
- 제출 결과: 실습 기록 커밋 `031989d`를 push한 뒤 [PR #4](https://github.com/shanis345/Deploy_Practice/pull/4)를 생성했다. 대상은 `codex/day02-results` → `main`이며 생성 시 open·미병합 상태를 확인했다. 이 PR 링크를 진행 현황과 인수인계에도 추가했다.
