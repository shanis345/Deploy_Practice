#!/usr/bin/env bash
# 배포 직후 전 경로 관통 검증. 결과를 그대로 배포 확인서에 첨부한다.
# 사용법: ./verify.sh [BASE_URL]   (기본 http://localhost:8080)
set -u
BASE="${1:-http://localhost:${PUBLIC_PORT:-8080}}"
pass=0; fail=0
chk() { # chk <설명> <기대> <실제>
  if [ "$2" = "$3" ]; then printf "  [OK]   %s\n" "$1"; pass=$((pass+1))
  else printf "  [FAIL] %s (기대=%s 실제=%s)\n" "$1" "$2" "$3"; fail=$((fail+1)); fi
}
j() { docker compose exec -T "$@"; }

echo "== 1. 사용자 진입 (DMZ → 업무망)"
code=$(curl -s -o /dev/null -w '%{http_code}' "$BASE/healthz")
chk "GET /healthz" "200" "$code"
ver=$(curl -s "$BASE/healthz" | python3 -c 'import sys,json;print(json.load(sys.stdin)["version"])' 2>/dev/null)
chk "버전 = ${AGENT_VERSION:-0.2.0}" "${AGENT_VERSION:-0.2.0}" "$ver"
code=$(curl -s -o /dev/null -w '%{http_code}' "$BASE/_lab/hang")
chk "실습용 엔드포인트 차단 (/_lab/*)" "403" "$code"

echo "== 2. 환경 진단 (실데이터 노출 없음)"
diag=$(curl -s "$BASE/diag")
chk "LLM 엔드포인트 = 게이트웨이" "http://llm-gateway:4000/v1" "$(echo "$diag" | python3 -c 'import sys,json;print(json.load(sys.stdin)["llm_base_url"])')"
chk "프롬프트 파일 마운트됨" "True" "$(echo "$diag" | python3 -c 'import sys,json;print(json.load(sys.stdin)["prompt_exists"])')"
chk "non-root (uid 10001)" "10001" "$(echo "$diag" | python3 -c 'import sys,json;print(json.load(sys.stdin)["uid"])')"

echo "== 3. 에이전트 인터넷 직접 접근 차단"
out=$(curl -s "$BASE/egress?url=http://example.com" | python3 -c 'import sys,json;print(json.load(sys.stdin)["ok"])')
chk "에이전트 → 인터넷 직접" "False" "$out"

echo "== 4. DB — 조회 전용 계정 (읽기 허용 / 쓰기 차단)"
out=$(curl -s "$BASE/tcp?host=postgres&port=5432" | python3 -c 'import sys,json;print(json.load(sys.stdin)["ok"])')
chk "에이전트 → DB 포트 도달" "True" "$out"
r=$(j postgres psql -tAq -U ro_user -d appdb -c "SELECT count(*) FROM sample_records;" 2>/dev/null | tr -d '[:space:]')
chk "조회 전용 계정 읽기 (3건)" "3" "$r"
w=$(j postgres psql -tAq -U ro_user -d appdb -c "INSERT INTO sample_records(title) VALUES ('x');" 2>&1 | grep -qi "denied" && echo DENIED || echo ALLOWED)
chk "조회 전용 계정 쓰기 차단" "DENIED" "$w"

echo "== 5. LLM 게이트웨이 경유 호출과 통제"
ans=$(curl -s -X POST "$BASE/ask" -H 'Content-Type: application/json' -d '{"question":"검증 질문"}' | python3 -c 'import sys,json;print(json.load(sys.stdin).get("mode"))')
chk "에이전트 → 게이트웨이 → 모델" "llm" "$ans"
code=$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:${ADMIN_PORT:-4000}/v1/chat/completions" -H "Authorization: Bearer wrong-key" -H 'Content-Type: application/json' -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"x"}]}')
chk "게이트웨이 잘못된 키 거부" "401" "$code"

echo "== 6. 감사 로그 적재"
sleep 6
n=$(j audit-db psql -tAq -U audit -d auditdb -c 'SELECT count(*) FROM "LiteLLM_SpendLogs";' 2>/dev/null | tr -d '[:space:]')
[ "${n:-0}" -ge 1 ] && chk "감사 DB 기록 ≥ 1건 (${n}건)" "yes" "yes" || chk "감사 DB 기록" "yes" "no"

echo "== 7. 프록시 화이트리스트 (게이트웨이 → 외부)"
# LiteLLM 이미지에는 curl이 없으므로 파이썬으로 (프록시 환경변수는 컨테이너에 이미 설정됨)
pyprobe='import sys,urllib.request
try: print(urllib.request.urlopen(sys.argv[1],timeout=10).status)
except Exception as e: print(getattr(e,"code",type(e).__name__))'
ok=$(j llm-gateway python3 -c "$pyprobe" http://example.com 2>/dev/null | tr -d '[:space:]')
chk "허용 목적지 example.com" "200" "$ok"
deny=$(j llm-gateway python3 -c "$pyprobe" http://www.google.com 2>/dev/null | tr -d '[:space:]')
chk "비허용 목적지 차단 (403)" "403" "$deny"

echo
echo "결과: 통과 $pass / 실패 $fail"
[ "$fail" -eq 0 ] || exit 1
