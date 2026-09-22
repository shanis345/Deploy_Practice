#!/usr/bin/env python3
"""
build.py — src/*.md 를 하나의 오프라인 HTML(dist/*.html)로 만든다.

사용법:
    python3 build.py            # dist/onprem-agent-deploy-guide.html 생성
    python3 build.py --check    # 빌드 + 소스 안의 YAML/셸 블록 기계 검사

의존성: pip install markdown pygments pyyaml pymdown-extensions
"""
import argparse
import hashlib
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown
from markdown.extensions.toc import slugify_unicode

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
THEME = ROOT / "theme"
DIST = ROOT / "dist"
OUT_NAME = "onprem-agent-deploy-guide.html"

TITLE = "대기업 에이전트 배포 속성 가이드북"
SUBTITLE = "온프렘 · 망분리 · 폐쇄망 환경에 AI 에이전트를 올리는 14일"

# ---------------------------------------------------------------------------
# 1. 마크다운 → HTML 조각
# ---------------------------------------------------------------------------

ADMON_LABELS = {
    "why": "왜 중요한가",
    "expect": "예상 출력 — 이렇게 나오면 성공",
    "fail": "의도된 실패 — 이 오류가 나오는 것이 정상",
    "eye": "눈으로 확인",
    "note": "참고",
    "warn": "주의",
    "tip": "실무 팁",
    "check": "고객사마다 다름 — 확인할 것",
    "os": "OS별 차이",
    "rollback": "오류 대응 — 어긋났을 때 되돌리기",
    "unverified": "미검증 — 세션 안에서 실행해 보지 못함",
    "verified": "검증됨 — 세션 안에서 실제 실행",
    "say": "고객사에 이렇게 말하세요",
    "checkpoint": "체크포인트",
}


def md_to_html(text: str) -> str:
    md = markdown.Markdown(
        extensions=[
            "tables", "attr_list", "def_list", "footnotes", "md_in_html",
            "admonition",
            "sane_lists",
            "pymdownx.highlight",
            "pymdownx.superfences",   # 상자(admonition) 안의 ``` 코드 블록 지원
            "toc",
        ],
        extension_configs={
            "pymdownx.highlight": {"css_class": "hl", "guess_lang": False, "use_pygments": True},
            "pymdownx.superfences": {"disable_indented_code_blocks": True},
            "toc": {"slugify": slugify_unicode, "permalink": False, "toc_depth": "1-3"},
        },
        output_format="html5",
    )
    return md.convert(text)


def inline_images(fragment: str) -> str:
    """<img src="shots/x.png" alt="캡션"> → base64 data URI + <figure>."""
    import base64, mimetypes
    def repl(m):
        src, alt = m.group(1), m.group(2)
        path = ROOT / src
        if not path.exists():
            return f'<div class="admonition warn"><p class="admonition-title">이미지 없음</p><p>{html.escape(src)}</p></div>'
        mime = mimetypes.guess_type(str(path))[0] or "image/png"
        data = base64.b64encode(path.read_bytes()).decode()
        cap = f'<figcaption>{alt}</figcaption>' if alt else ""
        return f'<figure class="shot"><img src="data:{mime};base64,{data}" alt="{alt}" loading="lazy">{cap}</figure>'
    return re.sub(r'<p><img alt="([^"]*)" src="([^"]+)"\s*/?></p>', lambda m: repl(type("M", (), {"group": lambda self, i: (m.group(2), m.group(1))[i-1]})()), fragment)


def transform_tasks(fragment: str, day_key: str) -> str:
    """'- [ ] 항목' 을 체크박스로. 키는 day + 텍스트 해시."""
    def repl(m):
        inner = m.group(2)
        key = day_key + ":" + hashlib.sha1(re.sub(r"<.*?>", "", inner).encode()).hexdigest()[:10]
        return (f'<li class="task"><label><input type="checkbox" data-key="{key}">'
                f'<span>{inner}</span></label></li>')
    return re.sub(r"<li>(\[ \]|\[x\]) ?(.*?)</li>", repl, fragment, flags=re.S)


def transform_admonitions(fragment: str) -> str:
    """python-markdown admonition div에 아이콘/기본 라벨 부여."""
    def repl(m):
        kind = m.group(1)
        rest = m.group(2)
        title_m = re.search(r'<p class="admonition-title">(.*?)</p>', rest, re.S)
        if title_m and title_m.group(1).strip() == kind.capitalize():
            # 제목을 안 준 경우 기본 라벨로 교체
            rest = rest.replace(title_m.group(0),
                                f'<p class="admonition-title">{ADMON_LABELS.get(kind, kind)}</p>', 1)
        return f'<div class="admonition {kind}" data-kind="{kind}">{rest}</div>'
    return re.sub(r'<div class="admonition ([a-z]+)">(.*?)</div>\n?(?=\n|<)', repl, fragment, flags=re.S)


def preprocess_screens(md_text: str) -> str:
    """```screen 블록 → 창 모양 목업(raw HTML). 첫 줄이 '# 제목'이면 제목표시줄."""
    def repl(m):
        body = m.group(1).rstrip("\n")
        lines = body.split("\n")
        title = "화면"
        if lines and lines[0].startswith("# "):
            title = lines[0][2:].strip()
            lines = lines[1:]
        content = html.escape("\n".join(lines))
        return (f'\n<div class="screen" markdown="0"><div class="screen-bar"><span class="dot"></span>'
                f'<span class="dot"></span><span class="dot"></span>'
                f'<span class="screen-title">{html.escape(title)}</span></div>'
                f'<pre class="screen-body">{content}</pre></div>\n')
    return re.sub(r"^```screen[^\n]*\n(.*?)^```[ \t]*$", repl, md_text, flags=re.S | re.M)


CODE_RE = re.compile(r'<div class="hl"><pre><span></span><code>(.*?)</code></pre></div>', re.S)


def transform_code_blocks(fragment: str) -> str:
    """모든 코드 블록을 .codeblock 으로 감싸고, 첫 줄이 '#file: 경로'면 파일명 탭을 붙인다."""
    def repl(m):
        body = m.group(1)
        first, nl, rest = body.partition("\n")
        plain = html.unescape(re.sub(r"<.*?>", "", first)).strip()
        for marker in ("#file:", "//file:", "--file:", "; file:", "<!--file:"):
            if plain.startswith(marker):
                fname = plain.split("file:", 1)[1].strip().rstrip("->").strip()
                return (f'<div class="codeblock" data-file="{html.escape(fname)}">'
                        f'<div class="code-tab">{html.escape(fname)}</div>'
                        f'<div class="hl"><pre><span></span><code>{rest}</code></pre></div></div>')
        return f'<div class="codeblock"><div class="hl"><pre><span></span><code>{body}</code></pre></div></div>'
    return CODE_RE.sub(repl, fragment)


# ---------------------------------------------------------------------------
# 2. 소스 수집 + 목차
# ---------------------------------------------------------------------------

LAB = ROOT.parents[1]  # Repository root: docs/guide -> project root
LAB_MANIFEST = ROOT / "lab-files.txt"
LAB_EXCLUDE_DIRS = {"wheels", "trivy-cache", "certs", "__pycache__", ".venv", "x", "leak"}
LAB_EXCLUDE_SUFFIX = (".tar", ".tar.gz", ".sha256", ".json", ".gitignore", ".bak", ".pyc")
LANG_BY_EXT = {".py": "python", ".yaml": "yaml", ".yml": "yaml", ".sh": "bash", ".conf": "nginx",
               ".md": "markdown", ".ini": "ini", ".tpl": "yaml", ".txt": "text", ".example": "ini",
               ".sql": "sql", "": "text"}


def lab_files():
    """Collect only explicit lab sources, excluding session notes and local secrets."""
    out = []
    for entry in LAB_MANIFEST.read_text(encoding="utf-8").splitlines():
        entry = entry.strip()
        if not entry or entry.startswith("#"):
            continue
        rel = Path(entry)
        if rel.is_absolute() or ".." in rel.parts:
            raise ValueError(f"Invalid lab manifest entry: {entry}")
        path = LAB / rel
        if not path.resolve().is_relative_to(LAB.resolve()):
            raise ValueError(f"Lab source outside repository: {entry}")
        if any(part in LAB_EXCLUDE_DIRS for part in rel.parts):
            continue
        if path.name.endswith(LAB_EXCLUDE_SUFFIX) and not path.name.endswith(".example"):
            continue
        if path.name == ".gitignore":
            continue
        if not path.is_file():
            raise FileNotFoundError(f"Missing lab source: {entry}")
        out.append(path)
    return sorted(out)


def lab_tree():
    lines = ["onprem-lab/"]
    files = lab_files()
    dirs = {}
    for f in files:
        rel = f.relative_to(LAB)
        dirs.setdefault(rel.parent.as_posix() if rel.parent != Path(".") else "", []).append(rel.name)
    for d in sorted(dirs):
        if d:
            depth = d.count("/") + 1
            lines.append("    " * (depth - 1) + "├── " + d.split("/")[-1] + "/")
        for n in dirs[d]:
            depth = (d.count("/") + 1) if d else 0
            lines.append("    " * depth + "├── " + n)
    return "\n".join(lines)


def lab_file_blocks():
    blocks = []
    for f in lab_files():
        rel = f.relative_to(LAB).as_posix()
        ext = f.suffix if f.suffix else ""
        if f.name == "Dockerfile" or f.name.startswith("Dockerfile."):
            lang = "dockerfile"
        elif f.name == "squid.conf":
            lang = "squid"
        else:
            lang = LANG_BY_EXT.get(ext, "text")
        body = f.read_text(encoding="utf-8", errors="replace").rstrip("\n")
        size = f.stat().st_size
        kb = f"{size/1024:.1f} KB"
        blocks.append(f'<details markdown="1"><summary><code>{html.escape(rel)}</code> &nbsp;<span class="muted">{kb}</span></summary>\n\n```{lang}\n{body}\n```\n\n</details>')
    return "\n\n".join(blocks)


def load_sources():
    files = sorted(SRC.glob("*.md"))
    parts = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        if "{{LAB_TREE}}" in text:
            text = text.replace("{{LAB_TREE}}", lab_tree())
        if "{{LAB_FILES}}" in text:
            text = text.replace("{{LAB_FILES}}", lab_file_blocks())
        # 첫 H1 = 파트 제목
        m = re.search(r"^# (.+)$", text, re.M)
        title = m.group(1).strip() if m else f.stem
        key = f.stem
        parts.append({"key": key, "title": title, "md": text, "file": f.name})
    return parts


HEADING_RE = re.compile(r'<h([23]) id="([^"]+)">(.*?)</h\1>', re.S)


def build_nav(parts):
    """사이드바용 계층 목차와 검색 인덱스."""
    nav = []
    for p in parts:
        items = []
        for m in HEADING_RE.finditer(p["html"]):
            level, hid, text = int(m.group(1)), m.group(2), re.sub(r"<.*?>", "", m.group(3))
            items.append({"level": level, "id": hid, "text": html.unescape(text)})
        nav.append({"key": p["key"], "id": p["id"], "title": p["title"],
                    "short": p["short"], "items": items})
    return nav


def build_search_index(parts):
    """섹션 단위 텍스트 인덱스 (제목 + 본문 평문)."""
    idx = []
    for p in parts:
        # h2/h3 기준으로 쪼갠다
        chunks = re.split(r'(?=<h[23] id=")', p["html"])
        for c in chunks:
            hm = re.match(r'<h([23]) id="([^"]+)">(.*?)</h\1>', c, re.S)
            if hm:
                hid = hm.group(2)
                title = html.unescape(re.sub(r"<.*?>", "", hm.group(3)))
            else:
                hid = p["id"]
                title = p["title"]
            body = re.sub(r"<[^>]+>", " ", c)
            body = html.unescape(re.sub(r"\s+", " ", body)).strip()
            if len(body) < 20:
                continue
            idx.append({"p": p["short"], "id": hid, "t": title, "b": body[:1200]})
    return idx


# ---------------------------------------------------------------------------
# 3. 기계 검사 (--check)
# ---------------------------------------------------------------------------

def check_blocks(parts):
    import yaml
    errors = 0
    fence = re.compile(r"^```(\w+)[^\n]*\n(.*?)^```", re.S | re.M)
    for p in parts:
        for m in fence.finditer(p["md"]):
            lang, body = m.group(1), m.group(2)
            first = body.split("\n", 1)[0]
            if first.startswith("#file:") or first.startswith("//file:") or first.startswith("--file:"):
                body = body.split("\n", 1)[1] if "\n" in body else ""
            first_plain = body.split("\n", 1)[0]
            if lang == "yaml":
                if "{{" in body or "부분" in first or "부분" in first_plain or "추가" in first:
                    continue  # Helm 템플릿·부분 발췌는 단독 YAML이 아니다
                try:
                    list(yaml.safe_load_all(body))
                except Exception as e:  # noqa
                    errors += 1
                    print(f"[YAML] {p['file']}: {e}")
            elif lang in ("bash", "sh"):
                if re.search(r"<[A-Za-z가-힣_\-]+>", body):
                    continue  # 자리표시자 <이름> 포함 블록은 문법 검사 생략
                with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as t:
                    t.write(body)
                    name = t.name
                r = subprocess.run(["bash", "-n", name], capture_output=True, text=True)
                if r.returncode != 0:
                    errors += 1
                    print(f"[BASH] {p['file']}: {r.stderr.strip()[:300]}")
    print(f"기계 검사 완료 — 오류 {errors}건")
    return errors


# ---------------------------------------------------------------------------
# 4. 조립
# ---------------------------------------------------------------------------

def render(parts):
    css = (THEME / "style.css").read_text(encoding="utf-8")
    js = (THEME / "app.js").read_text(encoding="utf-8")
    from pygments.formatters import HtmlFormatter
    hl_light = HtmlFormatter(style="friendly").get_style_defs(".hl")
    hl_dark = HtmlFormatter(style="monokai").get_style_defs('[data-theme="dark"] .hl')

    for p in parts:
        frag = md_to_html(preprocess_screens(p["md"]))
        frag = transform_admonitions(frag)
        frag = transform_code_blocks(frag)
        frag = inline_images(frag)
        frag = transform_tasks(frag, p["key"])
        # H1 id
        m = re.search(r'<h1 id="([^"]+)">', frag)
        p["id"] = m.group(1) if m else p["key"]
        sm = re.match(r"(Day \d+|부록 [A-Z]|들어가며|마치며)", p["title"])
        p["short"] = sm.group(1) if sm else p["title"][:8]
        p["html"] = frag

    nav = build_nav(parts)
    index = build_search_index(parts)

    body_parts = []
    for p in parts:
        body_parts.append(f'<section class="part" id="part-{p["key"]}" data-part="{p["id"]}">{p["html"]}</section>')

    nav_html = []
    for n in nav:
        sub = "".join(
            f'<li class="lv{i["level"]}"><a href="#{i["id"]}">{html.escape(i["text"])}</a></li>'
            for i in n["items"] if i["level"] == 2
        )
        nav_html.append(
            f'<li class="nav-part" data-part="{n["id"]}">'
            f'<a class="nav-title" href="#{n["id"]}"><span class="nav-short">{html.escape(n["short"])}</span>'
            f'<span class="nav-text">{html.escape(n["title"].split("—",1)[-1].strip() if "—" in n["title"] else n["title"])}</span>'
            f'<span class="nav-prog" data-prog="{n["id"]}"></span></a>'
            f'<ul class="nav-sub">{sub}</ul></li>'
        )

    doc = f"""<!DOCTYPE html>
<html lang="ko" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{SUBTITLE}">
<style>
{css}
/* ---- pygments ---- */
{hl_light}
{hl_dark}
</style>
</head>
<body>
<a class="skip" href="#content">본문으로</a>
<header class="topbar">
  <button class="icon-btn" id="navToggle" aria-label="목차 열기">☰</button>
  <a class="brand" href="#top"><span class="brand-main">{TITLE}</span><span class="brand-sub">{SUBTITLE}</span></a>
  <div class="topbar-right">
    <div class="search" id="search">
      <input id="searchInput" type="search" placeholder="본문 검색 (/)" autocomplete="off" aria-label="본문 검색">
      <div class="search-results" id="searchResults" hidden></div>
    </div>
    <button class="icon-btn" id="themeToggle" aria-label="라이트/다크 전환" title="라이트/다크 전환">◐</button>
  </div>
</header>
<div class="layout">
<nav class="sidebar" id="sidebar" aria-label="목차">
  <div class="sidebar-inner">
    <div class="sidebar-head">
      <span>목차</span>
      <button class="link-btn" id="resetProgress" title="체크 표시 초기화">진행 초기화</button>
    </div>
    <ul class="nav">{"".join(nav_html)}</ul>
    <div class="sidebar-foot">
      <div class="overall"><div class="overall-bar"><span id="overallBar"></span></div><span id="overallText"></span></div>
    </div>
  </div>
</nav>
<div class="backdrop" id="backdrop"></div>
<main class="content" id="content">
<a id="top"></a>
{"".join(body_parts)}
<footer class="foot">
  <p>이 문서는 단일 HTML 파일이며 인터넷 없이 동작합니다. 체크 표시는 이 브라우저에만 저장됩니다.</p>
</footer>
</main>
</div>
<button class="totop" id="toTop" aria-label="맨 위로">↑</button>
<script id="searchIndex" type="application/json">{json.dumps(index, ensure_ascii=False)}</script>
<script>
{js}
</script>
</body>
</html>
"""
    return doc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="YAML/셸 블록 기계 검사")
    ap.add_argument("--out", default=str(DIST / OUT_NAME))
    args = ap.parse_args()

    parts = load_sources()
    if not parts:
        print("src/*.md 가 없습니다.", file=sys.stderr)
        sys.exit(1)
    if args.check:
        if check_blocks(parts):
            sys.exit(2)
    doc = render(parts)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    size = out.stat().st_size / 1024
    print(f"생성: {out} ({size:.0f} KB, 파트 {len(parts)}개)")


if __name__ == "__main__":
    main()
