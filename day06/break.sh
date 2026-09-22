#!/usr/bin/env bash
# 누적 점검 1 — 고장 심기. 사용법: ./break.sh <1-5> | ./break.sh fix
# 어떤 고장인지 보지 말고, Day 4의 진단 3단계로 원인을 찾은 뒤 답을 확인하세요.
set -u
case "${1:-}" in
  1) docker network disconnect day06_dbzone day06-agent-1 ;;
  2) docker compose stop erp >/dev/null 2>&1 ;;
  3) docker network disconnect day06_biz day06-gateway-1 ;;
  4) docker pause day06-agent-1 ;;
  5) docker network connect day06_dmz day06-agent-1 ;;
  fix) docker unpause day06-agent-1 >/dev/null 2>&1; docker compose up -d --force-recreate >/dev/null 2>&1 && echo "복구 완료" ;;
  answer)
    cat <<'A'
1: 에이전트가 DB존에서 떨어짐        → /tcp?host=postgres 실패(gaierror). docker network inspect day06_dbzone 에 agent 없음
2: ERP(사내 시스템) 중단             → probe-biz에서 nslookup erp 실패. docker compose ps 에 erp exited
3: 게이트웨이가 업무망에서 떨어짐     → curl localhost:8080 타임아웃/504. gateway에서 nslookup agent 실패
4: 에이전트 프로세스 정지(pause)      → curl 타임아웃. docker compose ps 의 STATUS가 Paused. Day 5 ③과 같은 "살아 있지만 무응답"
5: 에이전트가 DMZ에 붙음 (보안 위반)  → 아무 증상 없음! /egress?url=http://example.com 이 ok:true. docker network inspect day06_dmz 에 agent 있음
A
    ;;
  *) echo "사용법: $0 <1-5> | fix | answer" ;;
esac
