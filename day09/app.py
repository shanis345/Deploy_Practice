"""
학습용 에이전트 더미 — 표준 라이브러리만 사용 (의존성: pyyaml 하나, rubric 읽기용).
배포 실습용이므로 로직은 일부러 단순합니다. 엔드포인트:

  GET  /healthz            생존 확인
  GET  /diag               환경 진단 (프록시·CA·LLM·DB 설정 여부, 실데이터 노출 없음)
  GET  /egress?url=...     외부 연결 가능 여부 (프록시·CA 문제 재현용)
  GET  /tcp?host=&port=    TCP 포트 도달 여부 (DB·게이트웨이 방화벽 확인용)
  GET  /prompt             현재 프롬프트 (파일 변경 시 자동 재적재)
  POST /ask {"question"}   LLM 호출 (LLM_BASE_URL 없으면 에코)
  GET  /metrics            Prometheus 텍스트 포맷
  GET  /_lab/exit          (실습용) 프로세스를 비정상 종료 — 재시작 정책 실험
  GET  /_lab/hang          (실습용) 이후 모든 요청을 무응답 상태로 — 헬스체크·liveness 실험
로그는 JSON Lines로 stdout에 남깁니다.
"""
import hashlib
import json
import os
import socket
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VERSION = os.getenv("APP_VERSION", "0.1.0")
HOST = socket.gethostname()
PROMPT_PATH = os.getenv("PROMPT_PATH", "/app/config/prompt.txt")
RUBRIC_PATH = os.getenv("RUBRIC_PATH", "/app/config/rubric.yaml")
LLM_BASE = os.getenv("LLM_BASE_URL", "").rstrip("/")
LLM_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
DB_DSN = os.getenv("DB_DSN", "")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

_metrics = {}
_metrics_lock = threading.Lock()
_hang = {"on": False}
_prompt_cache = {"mtime": 0.0, "text": "", "checked": 0.0}


def log(level, **kv):
    if LOG_LEVEL == "INFO" and level == "DEBUG":
        return
    kv.update(ts=time.strftime("%Y-%m-%dT%H:%M:%S%z"), level=level, service="agent", version=VERSION, host=HOST)
    sys.stdout.write(json.dumps(kv, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def load_prompt():
    """파일 변경을 감지해 자동 재적재. 5초마다만 stat 호출."""
    now = time.time()
    if now - _prompt_cache["checked"] < 5:
        return _prompt_cache["text"]
    _prompt_cache["checked"] = now
    try:
        m = os.stat(PROMPT_PATH).st_mtime
        if m != _prompt_cache["mtime"]:
            with open(PROMPT_PATH, encoding="utf-8") as f:
                _prompt_cache["text"] = f.read()
            _prompt_cache["mtime"] = m
            log("INFO", event="prompt_reloaded", path=PROMPT_PATH, sha=hashlib.sha256(_prompt_cache["text"].encode()).hexdigest()[:12])
    except FileNotFoundError:
        _prompt_cache["text"] = ""
    return _prompt_cache["text"]


def load_rubric():
    try:
        import yaml  # noqa
        with open(RUBRIC_PATH, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:  # noqa
        return {"error": type(e).__name__}


def count(path, status):
    with _metrics_lock:
        k = (path, str(status))
        _metrics[k] = _metrics.get(k, 0) + 1


class H(BaseHTTPRequestHandler):
    server_version = "agent/" + VERSION

    def log_message(self, *a):  # 기본 access log 억제 (JSON 로그로 대체)
        pass

    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype + ("; charset=utf-8" if ctype.startswith("text") or ctype.endswith("json") else ""))
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Request-Id", self.rid)
        self.end_headers()
        self.wfile.write(data)
        count(self.path.split("?")[0], code)
        log("INFO", event="request", method=self.command, path=self.path.split("?")[0], status=code,
            ms=int((time.time() - self.t0) * 1000), request_id=self.rid)

    def do_GET(self):
        self.t0, self.rid = time.time(), self.headers.get("X-Request-Id") or uuid.uuid4().hex[:12]
        u = urllib.parse.urlparse(self.path)
        q = dict(urllib.parse.parse_qsl(u.query))
        if _hang["on"]:
            time.sleep(3600)  # 살아 있지만 응답하지 않는 상태 (데드락·GC 정지 흉내)
        if u.path == "/_lab/exit":
            log("ERROR", event="lab_exit", request_id=self.rid)
            self._send(200, {"bye": True})
            os._exit(1)
        if u.path == "/_lab/hang":
            _hang["on"] = True
            log("WARN", event="lab_hang", request_id=self.rid)
            return self._send(200, {"hang": True})
        if u.path == "/healthz":
            return self._send(200, {"status": "ok", "version": VERSION, "host": HOST})
        if u.path == "/diag":
            return self._send(200, {
                "version": VERSION, "host": HOST, "uid": os.getuid(), "gid": os.getgid(),
                "llm_base_url": LLM_BASE or "(unset)", "llm_key_set": bool(LLM_KEY), "llm_model": LLM_MODEL,
                "db_dsn_set": bool(DB_DSN),
                "proxy": {k: os.getenv(k, "(unset)") for k in ("HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "http_proxy", "https_proxy", "no_proxy")},
                "ca": {k: os.getenv(k, "(unset)") for k in ("SSL_CERT_FILE", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE")},
                "prompt_path": PROMPT_PATH, "prompt_exists": os.path.exists(PROMPT_PATH),
                "prompt_sha": hashlib.sha256(load_prompt().encode()).hexdigest()[:12],
                "rubric": load_rubric(), "log_level": LOG_LEVEL,
            })
        if u.path == "/egress":
            url = q.get("url", "https://example.com")
            t = time.time()
            try:
                with urllib.request.urlopen(url, timeout=int(q.get("timeout", "8"))) as r:
                    return self._send(200, {"ok": True, "url": url, "status": r.status, "elapsed_ms": int((time.time() - t) * 1000)})
            except urllib.error.HTTPError as e:
                return self._send(200, {"ok": False, "url": url, "error_type": "HTTPError", "status": e.code, "error": str(e), "elapsed_ms": int((time.time() - t) * 1000)})
            except urllib.error.URLError as e:
                return self._send(200, {"ok": False, "url": url, "error_type": type(e.reason).__name__, "error": str(e.reason), "elapsed_ms": int((time.time() - t) * 1000)})
            except Exception as e:  # noqa
                return self._send(200, {"ok": False, "url": url, "error_type": type(e).__name__, "error": str(e), "elapsed_ms": int((time.time() - t) * 1000)})
        if u.path == "/tcp":
            host, port = q.get("host", "postgres"), int(q.get("port", "5432"))
            t = time.time()
            try:
                socket.create_connection((host, port), timeout=3).close()
                return self._send(200, {"ok": True, "host": host, "port": port, "elapsed_ms": int((time.time() - t) * 1000)})
            except Exception as e:  # noqa
                return self._send(200, {"ok": False, "host": host, "port": port, "error_type": type(e).__name__, "error": str(e)})
        if u.path == "/prompt":
            return self._send(200, load_prompt().encode() or b"(no prompt)", "text/plain")
        if u.path == "/metrics":
            with _metrics_lock:
                lines = ["# HELP agent_requests_total 요청 수", "# TYPE agent_requests_total counter"]
                lines += [f'agent_requests_total{{path="{p}",status="{s}"}} {n}' for (p, s), n in sorted(_metrics.items())]
            return self._send(200, ("\n".join(lines) + "\n").encode(), "text/plain")
        return self._send(404, {"error": "not found", "path": u.path})

    def do_POST(self):
        self.t0, self.rid = time.time(), self.headers.get("X-Request-Id") or uuid.uuid4().hex[:12]
        if self.path != "/ask":
            return self._send(404, {"error": "not found"})
        n = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._send(400, {"error": "invalid json"})
        question = str(body.get("question", ""))
        if not LLM_BASE:
            return self._send(200, {"answer": f"(echo) {question}", "mode": "offline", "prompt_sha": hashlib.sha256(load_prompt().encode()).hexdigest()[:12]})
        payload = json.dumps({"model": LLM_MODEL, "messages": [
            {"role": "system", "content": load_prompt() or "You are a helpful assistant."},
            {"role": "user", "content": question}]}).encode()
        req = urllib.request.Request(f"{LLM_BASE}/chat/completions", data=payload, headers={
            "Content-Type": "application/json", "Authorization": f"Bearer {LLM_KEY}", "X-Request-Id": self.rid})
        t = time.time()
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read())
            return self._send(200, {"answer": data["choices"][0]["message"]["content"], "mode": "llm", "model": data.get("model", LLM_MODEL),
                                    "usage": data.get("usage"), "elapsed_ms": int((time.time() - t) * 1000)})
        except urllib.error.HTTPError as e:
            return self._send(502, {"answer": None, "mode": "error", "error_type": "HTTPError", "status": e.code, "error": e.read().decode(errors="replace")[:500]})
        except Exception as e:  # noqa
            return self._send(502, {"answer": None, "mode": "error", "error_type": type(e).__name__, "error": str(e)})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    log("INFO", event="startup", port=port, llm_base=LLM_BASE or "(unset)", prompt_path=PROMPT_PATH)
    ThreadingHTTPServer(("0.0.0.0", port), H).serve_forever()
