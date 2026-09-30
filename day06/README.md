# Day 6 — 망분리 재현: DMZ · 업무망 · DB존, 그리고 방화벽 신청서

- 가이드: [해당 Day 원문](../docs/guide/src/07-day06.md)
- 학습 기록: [SESSION.md](SESSION.md)
- 전체 진행: [PROGRESS.md](../PROGRESS.md)

## 최종 상태 (2026-09-30)
- **Day 6 종료.** 6-1~6-3·6-4 학습용 신청서 초안 작성 및 설명·화면 관찰·누적 장애 5개 재현과 안내에 따른 진단·복구를 마쳤다.
- 사용자 출력으로 컨테이너 7개·네트워크 3개 제거, Day 6 잔존 목록 없음·8080 리스너 부재를 확인했다. [정리 증거](evidence/cleanup-user-2026-09-30.txt).
- 별도 자기점검·독립 진단 평가는 미실시다. 실제 고객사 제출·정책 적용은 하지 않았다. 아래 실행 상태는 정리 전 이력이다.

## 진행 결과 이력 (2026-09-29~30)
- **6-1 완료.** 사용자 Ubuntu 출력으로 컨테이너 7개 Up, agent·postgres healthy, gateway의 127.0.0.1:8080 게시를 확인했다.
- 네트워크 3개의 internal 값과 소속이 구성과 일치한다. dmz(false): gateway·probe-dmz, biz(true): gateway·erp·agent·probe-biz, dbzone(true): agent·postgres·probe-db.
- 파일 3개 해시 일치·Compose 문법 정상·필요 이미지 5개 존재를 먼저 확인하고 로컬 이미지로 기동했다.
- 기동 당시 실행 상태를 확인했다. 종료 시 해당 자원은 제거했다. [기동 증거](evidence/startup-user-2026-09-29.txt).
- **6-2 완료.** 다음 결과는 모두 사용자 제공 Ubuntu 출력에 근거한다.

| 항목 | 경로 | 확인 결과 |
|---|---|---|
| ① | Ubuntu → gateway → agent | healthz 정상·버전 0.2.0 |
| ② | agent → postgres:5432 | TCP 성공·1ms |
| ③ | probe-dmz → DB | 이름 해석 실패, IP 172.22.0.4:5432 직접 연결도 타임아웃 |
| ④ | probe-biz → example.com:80 | 이름 해석 실패, IPv4 내부 경로만 존재·default 없음 |
| ⑤ | 실제 agent → erp:8080 | HTTP 200·Name: erp-api |
| ⑥ | agent → http://example.com | ok=false·gaierror·8ms |
| ⑦ | probe-db → agent:8000 | 172.22.0.3:8000 TCP 성공·종료코드 0 |

- 핵심: 존을 분리해도 같은 dbzone을 공유하는 DB존 단말→agent 신규 연결은 가능하다. 방향별 차단 정책은 별도로 필요하다. DB 인증·SQL·모든 외부 IP 및 IPv6를 시험한 것은 아니다.
- 증거: [①②](evidence/connectivity-01-02-user-2026-09-29.txt), [③ DNS](evidence/connectivity-03-dns-user-2026-09-29.txt), [③ IP](evidence/connectivity-03-ip-user-2026-09-29.txt), [④](evidence/connectivity-04-user-2026-09-29.txt), [⑤](evidence/connectivity-05-user-2026-09-29.txt), [⑥](evidence/connectivity-06-user-2026-09-29.txt), [⑦](evidence/connectivity-07-user-2026-09-29.txt).
- **6-3 완료.** DMZ 추가 후 healthy·healthz 정상과 외부 HTTP 200(105ms)을 확인했다. 백업 원복 후 원본 해시 일치·biz/dbzone만 연결·healthy·healthz 정상·외부 요청 gaierror(7ms) 복귀를 확인했다. /tmp/day06-compose.OTTiFi 백업은 삭제하지 않았다. [재현 증거](evidence/63-dmz-added-user-2026-09-29.txt), [원복 증거](evidence/63-restored-user-2026-09-29.txt).

- **6-4 초안 작성·설명 완료.** [방화벽 신청서 연습 초안](FIREWALL-REQUEST.md)에 7행·흐름도·최소 권한 근거와 실습 대조를 작성했다. 주소는 가이드 예시이며 실제 고객사 적용·제출이나 사용자 독립 작성 평가는 하지 않았다.

- **화면 관찰 완료(2026-09-30).** 사용자 화면에서 7개 서비스 running·agent/postgres healthy·3존 목록을 확인했다. Containers: none 표시는 CLI로 보완했으며 3존 internal 값·소속은 모두 예상과 일치한다. agent는 DMZ에 없다. [조회 증거](evidence/network-observation-user-2026-09-30.txt).

## 누적 장애 5개 결과

2026-09-30 사용자 출력으로 모두 복구를 확인한 뒤 자원 정리를 마쳤다. 안내에 따른 진단이며 독립 진단 평가 통과와 구분한다.

| 번호 | 증상과 원인 | 복구 및 확인 |
|---|---|---|
| 1 | DB 이름 해석 실패: agent의 DB존 연결 이탈 | DB존 재연결 후 DB TCP 성공·1ms |
| 2 | ERP 이름 해석 실패: ERP 중지 | ERP 시작 후 agent→ERP HTTP 200 |
| 3 | 사용자 요청 타임아웃: gateway의 업무망 연결 이탈 | 업무망 재연결 후 사용자 healthz HTTP 200 |
| 4 | agent Up (Paused), 요청 타임아웃 | unpause 후 HTTP 200, 후속 healthy·연속 실패 0·최근 검사 5회 성공 |
| 5 | 정상 서비스 상태에서 외부 HTTP 200: agent의 DMZ 추가 연결 | DMZ 연결 제거 후 healthz 정상·외부 요청 gaierror·1ms |

상세 명령과 사용자 출력은 [SESSION](SESSION.md)에 있다. 같은 오류라도 원인은 다를 수 있으며 실행 상태·실제 응답·통신 제한을 별도로 확인했다.

## 진행 방식

이 Day의 Codex 작업에서 사용자와 합의한 절만 한 단계씩 진행한다.
실행 기록·오류 해결·다음 시작 지점은 SESSION.md에 남긴다.
실습은 Ubuntu WSL2에서 실행하며 Windows 프로젝트 폴더와의 파일 동기화 여부를 먼저 확인한다.

## 실습 파일
- [break.sh](break.sh)
- [compose.yaml](compose.yaml)
- [gateway.conf](gateway.conf)

## 증거 자료
필요한 출력과 화면 캡처를 `evidence/`에 보관하고 SESSION.md에서 링크한다.
실제 비밀 값은 제거한다. 증거가 생길 때 폴더를 만든다.
