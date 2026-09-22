#!/usr/bin/env bash
# 진단 3단계 — 컨테이너(또는 Pod) 안에서 실행. 사용법: ./diag3.sh <호스트> <포트> [경로]
#   예: ./diag3.sh postgres 5432        ./diag3.sh agent 8000 /healthz
set -u
H="${1:?호스트}"; P="${2:?포트}"; URLPATH="${3:-/}"
echo "① 이름 해석"; getent hosts "$H" || nslookup "$H" 2>/dev/null | tail -2 || echo "  실패 → DNS / 네트워크 소속 / NetworkPolicy DNS 규칙"
echo "② 포트"; if command -v nc >/dev/null; then nc -zv -w3 "$H" "$P"; else timeout 3 bash -c "</dev/tcp/$H/$P" && echo "  OPEN" || echo "  CLOSED/timeout → 방화벽·미기동·127.0.0.1 바인딩"; fi
echo "③ HTTP"; curl -s -o /dev/null -m5 -w "  %{http_code} (%{time_total}s)\n" "http://$H:$P$URLPATH" || echo "  실패 → 애플리케이션(인증·경로·TLS·타임아웃)"
