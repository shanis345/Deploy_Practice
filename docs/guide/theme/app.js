/* 가이드북 클라이언트 스크립트 — 외부 의존성 없음 */
(function () {
  'use strict';
  var LS = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v === null ? d : v; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) { /* 저장 불가 환경: 무시 */ } },
    del: function (k) { try { localStorage.removeItem(k); } catch (e) {} }
  };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- 테마 ---------- */
  var root = document.documentElement;
  function applyTheme(t) { root.setAttribute('data-theme', t); LS.set('guide.theme', t); }
  (function initTheme() {
    var saved = LS.get('guide.theme', null);
    if (saved) { applyTheme(saved); return; }
    var prefers = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    root.setAttribute('data-theme', prefers ? 'dark' : 'light');
  })();
  $('#themeToggle').addEventListener('click', function () {
    applyTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  });

  /* ---------- 사이드바 (모바일) ---------- */
  var sidebar = $('#sidebar'), backdrop = $('#backdrop');
  function closeNav() { sidebar.classList.remove('open'); backdrop.classList.remove('show'); }
  $('#navToggle').addEventListener('click', function () {
    sidebar.classList.toggle('open'); backdrop.classList.toggle('show', sidebar.classList.contains('open'));
  });
  backdrop.addEventListener('click', closeNav);
  $$('.nav a').forEach(function (a) { a.addEventListener('click', function () { if (window.innerWidth <= 900) closeNav(); }); });
  $$('.nav-title').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var li = a.parentNode;
      // 현재 파트가 아닌 항목은 클릭 시 하위 목차를 펼쳐 둔다
      li.classList.add('open');
    });
  });

  /* ---------- 코드 복사 버튼 ---------- */
  $$('.codeblock').forEach(function (block) {
    var pre = $('pre', block); if (!pre) return;
    var btn = document.createElement('button');
    btn.className = 'copy-btn'; btn.type = 'button'; btn.textContent = '복사';
    btn.addEventListener('click', function () {
      var text = pre.innerText.replace(/\n$/, '');
      function done() { btn.textContent = '복사됨'; btn.classList.add('done'); setTimeout(function () { btn.textContent = '복사'; btn.classList.remove('done'); }, 1400); }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () { fallback(text); done(); });
      } else { fallback(text); done(); }
    });
    block.appendChild(btn);
  });
  function fallback(text) {
    var ta = document.createElement('textarea'); ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); } catch (e) {} document.body.removeChild(ta);
  }

  /* ---------- 표 가로 스크롤 래핑 ---------- */
  $$('.content table').forEach(function (t) {
    if (t.parentNode.classList.contains('table-wrap')) return;
    var w = document.createElement('div'); w.className = 'table-wrap';
    t.parentNode.insertBefore(w, t); w.appendChild(t);
  });

  /* ---------- 체크박스 진행 저장 ---------- */
  var boxes = $$('li.task input[type=checkbox]');
  function partOf(el) { var p = el.closest('.part'); return p ? p.getAttribute('data-part') : ''; }
  function updateProgress() {
    var perPart = {}, total = 0, done = 0;
    boxes.forEach(function (b) {
      var p = partOf(b); perPart[p] = perPart[p] || { t: 0, d: 0 };
      perPart[p].t++; total++;
      if (b.checked) { perPart[p].d++; done++; }
    });
    $$('.nav-prog').forEach(function (el) {
      var s = perPart[el.getAttribute('data-prog')];
      el.textContent = s ? (s.d + '/' + s.t) : '';
    });
    var bar = $('#overallBar'), txt = $('#overallText');
    if (bar) bar.style.width = (total ? Math.round(done / total * 100) : 0) + '%';
    if (txt) txt.textContent = total ? ('체크 ' + done + '/' + total) : '';
  }
  boxes.forEach(function (b) {
    var k = 'guide.task.' + b.getAttribute('data-key');
    b.checked = LS.get(k, '0') === '1';
    b.addEventListener('change', function () { LS.set(k, b.checked ? '1' : '0'); updateProgress(); });
  });
  updateProgress();
  var resetBtn = $('#resetProgress');
  if (resetBtn) resetBtn.addEventListener('click', function () {
    if (!confirm('모든 체크 표시를 지울까요?')) return;
    boxes.forEach(function (b) { b.checked = false; LS.del('guide.task.' + b.getAttribute('data-key')); });
    updateProgress();
  });

  /* ---------- 현재 위치 하이라이트 ---------- */
  var partEls = $$('.part');
  var navParts = {}; $$('.nav-part').forEach(function (li) { navParts[li.getAttribute('data-part')] = li; });
  var subLinks = {}; $$('.nav-sub li a').forEach(function (a) { subLinks[a.getAttribute('href').slice(1)] = a.parentNode; });
  var h2s = $$('.content h2[id]');
  var currentPart = null, currentH2 = null;
  function setCurrent() {
    var y = window.scrollY + 90, part = null, h2 = null;
    for (var i = 0; i < partEls.length; i++) { if (partEls[i].offsetTop <= y) part = partEls[i]; }
    for (var j = 0; j < h2s.length; j++) { if (h2s[j].offsetTop <= y) h2 = h2s[j]; }
    var pid = part ? part.getAttribute('data-part') : null;
    if (pid !== currentPart) {
      Object.keys(navParts).forEach(function (k) { navParts[k].classList.toggle('current', k === pid); navParts[k].classList.remove('open'); });
      currentPart = pid;
    }
    var hid = h2 && part && part.contains(h2) ? h2.id : null;
    if (hid !== currentH2) {
      Object.keys(subLinks).forEach(function (k) { subLinks[k].classList.toggle('active', k === hid); });
      currentH2 = hid;
      var act = hid && subLinks[hid]; if (act && sidebar.scrollHeight > sidebar.clientHeight) {
        var r = act.getBoundingClientRect(), sr = sidebar.getBoundingClientRect();
        if (r.top < sr.top + 40 || r.bottom > sr.bottom - 40) act.scrollIntoView({ block: 'center' });
      }
    }
    var top = $('#toTop'); if (top) top.classList.toggle('show', window.scrollY > 600);
  }
  var ticking = false;
  window.addEventListener('scroll', function () { if (!ticking) { requestAnimationFrame(function () { setCurrent(); ticking = false; }); ticking = true; } });
  window.addEventListener('resize', setCurrent);
  setTimeout(setCurrent, 50);
  $('#toTop').addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });

  /* ---------- 검색 ---------- */
  var index = [];
  try { index = JSON.parse($('#searchIndex').textContent); } catch (e) { index = []; }
  var input = $('#searchInput'), results = $('#searchResults'), activeIdx = -1;
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function snippet(body, terms) {
    var low = body.toLowerCase(), pos = -1;
    for (var i = 0; i < terms.length; i++) { pos = low.indexOf(terms[i]); if (pos >= 0) break; }
    if (pos < 0) pos = 0;
    var start = Math.max(0, pos - 60), end = Math.min(body.length, pos + 120);
    var s = (start > 0 ? '…' : '') + body.slice(start, end) + (end < body.length ? '…' : '');
    s = esc(s);
    terms.forEach(function (t) { if (!t) return; s = s.replace(new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'), function (m) { return '<mark>' + m + '</mark>'; }); });
    return s;
  }
  function doSearch() {
    var q = input.value.trim().toLowerCase();
    activeIdx = -1;
    if (q.length < 2) { results.hidden = true; results.innerHTML = ''; return; }
    var terms = q.split(/\s+/).filter(Boolean);
    var hits = [];
    for (var i = 0; i < index.length; i++) {
      var it = index[i], tl = it.t.toLowerCase(), bl = it.b.toLowerCase(), score = 0, ok = true;
      for (var j = 0; j < terms.length; j++) {
        var t = terms[j];
        if (tl.indexOf(t) >= 0) score += 10; else if (bl.indexOf(t) >= 0) score += 1; else { ok = false; break; }
      }
      if (ok) hits.push({ it: it, score: score });
    }
    hits.sort(function (a, b) { return b.score - a.score; });
    hits = hits.slice(0, 30);
    if (!hits.length) { results.innerHTML = '<div class="sr-empty">결과 없음</div>'; results.hidden = false; return; }
    results.innerHTML = hits.map(function (h) {
      return '<a class="sr" href="#' + h.it.id + '"><span class="sr-part">' + esc(h.it.p) + '</span><span class="sr-title">' + esc(h.it.t) + '</span><div class="sr-snip">' + snippet(h.it.b, terms) + '</div></a>';
    }).join('');
    results.hidden = false;
    $$('.sr', results).forEach(function (a) { a.addEventListener('click', function () { results.hidden = true; }); });
  }
  var timer = null;
  input.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(doSearch, 120); });
  input.addEventListener('focus', function () { if (results.innerHTML) results.hidden = false; });
  input.addEventListener('keydown', function (e) {
    var items = $$('.sr', results);
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault(); if (!items.length) return;
      activeIdx = (activeIdx + (e.key === 'ArrowDown' ? 1 : -1) + items.length) % items.length;
      items.forEach(function (a, i) { a.classList.toggle('active', i === activeIdx); });
      items[activeIdx].scrollIntoView({ block: 'nearest' });
    } else if (e.key === 'Enter') {
      var a = items[activeIdx >= 0 ? activeIdx : 0]; if (a) { location.hash = a.getAttribute('href'); results.hidden = true; }
    } else if (e.key === 'Escape') { results.hidden = true; input.blur(); }
  });
  document.addEventListener('click', function (e) { if (!e.target.closest('#search')) results.hidden = true; });
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== input && !/input|textarea/i.test(document.activeElement.tagName)) { e.preventDefault(); input.focus(); input.select(); }
  });
})();
