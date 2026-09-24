/* 站内搜索：第一次打开时下载 search.json，按空格分词、全部命中才算结果。
   中文不分词，直接做子串匹配；标题命中排在正文命中之前。 */
(function () {
  var dialog = document.getElementById('search-dialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  var input = document.getElementById('search-input');
  var list = document.getElementById('search-results');
  var status = document.getElementById('search-status');
  var MAX = 20;
  var index = null;
  var loading = null;
  var active = -1;
  var timer = null;

  function load() {
    if (!loading) {
      loading = fetch(dialog.getAttribute('data-index'))
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          return r.json();
        })
        .then(function (docs) {
          index = docs.map(function (d) {
            d.hay = [d.title, d.nav, d.desc, d.text].join('\n').toLowerCase();
            return d;
          });
        })
        .catch(function () {
          loading = null;
          status.textContent = '搜索索引加载失败，请检查网络后重试。';
        });
    }
    return loading;
  }

  function open() {
    if (!dialog.open) dialog.showModal();
    input.focus();
    input.select();
    load().then(run);
  }

  function close() {
    if (dialog.open) dialog.close();
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function escapeRe(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function highlight(s, re) {
    var out = '';
    var last = 0;
    s.replace(re, function (m, offset) {
      out += escapeHtml(s.slice(last, offset)) + '<mark>' + escapeHtml(m) + '</mark>';
      last = offset + m.length;
      return m;
    });
    return out + escapeHtml(s.slice(last));
  }

  function count(hay, term) {
    var n = 0;
    var i = hay.indexOf(term);
    while (i !== -1 && n < 5) {
      n++;
      i = hay.indexOf(term, i + term.length);
    }
    return n;
  }

  function score(d, terms) {
    var total = 0;
    for (var i = 0; i < terms.length; i++) {
      var t = terms[i];
      if (d.hay.indexOf(t) === -1) return 0;
      if (d.title.toLowerCase().indexOf(t) !== -1) total += 10;
      if ((d.nav || '').toLowerCase().indexOf(t) !== -1) total += 6;
      if ((d.desc || '').toLowerCase().indexOf(t) !== -1) total += 4;
      total += count(d.text.toLowerCase(), t);
    }
    return total;
  }

  /* 摘要取正文里第一个命中词前后一段；正文没命中（只命中标题）就用页面简介 */
  function snippet(d, terms) {
    var lower = d.text.toLowerCase();
    var at = -1;
    for (var i = 0; i < terms.length && at === -1; i++) at = lower.indexOf(terms[i]);
    if (at === -1) return d.desc || d.text.slice(0, 90);
    var start = Math.max(0, at - 30);
    var end = Math.min(d.text.length, at + 90);
    return (start > 0 ? '…' : '') + d.text.slice(start, end) + (end < d.text.length ? '…' : '');
  }

  function setActive(i) {
    var items = list.children;
    if (active >= 0 && items[active]) items[active].classList.remove('is-active');
    active = i;
    if (active >= 0 && items[active]) {
      items[active].classList.add('is-active');
      items[active].scrollIntoView({ block: 'nearest' });
    }
  }

  function run() {
    if (!index) return;
    var q = input.value.trim();
    list.innerHTML = '';
    active = -1;
    if (!q) {
      status.textContent = '输入关键词搜索全部 ' + index.length + ' 篇指南。';
      return;
    }
    var terms = q.toLowerCase().split(/\s+/);
    var hits = [];
    for (var i = 0; i < index.length; i++) {
      var s = score(index[i], terms);
      if (s) hits.push({ doc: index[i], score: s });
    }
    hits.sort(function (a, b) { return b.score - a.score; });
    status.textContent = hits.length
      ? '找到 ' + hits.length + ' 篇' + (hits.length > MAX ? '，显示前 ' + MAX + ' 篇' : '')
      : '没有找到「' + q + '」，换个说法试试，比如用英文或更短的词。';
    var re = new RegExp(terms.map(escapeRe).join('|'), 'gi');
    hits.slice(0, MAX).forEach(function (h) {
      var d = h.doc;
      var li = document.createElement('li');
      li.innerHTML =
        '<a class="search-hit" href="' + escapeHtml(d.url) + '">' +
          '<span class="search-hit-nav">' + escapeHtml(d.nav || '') + '</span>' +
          '<span class="search-hit-title">' + highlight(d.title, re) + '</span>' +
          '<span class="search-hit-text">' + highlight(snippet(d, terms), re) + '</span>' +
        '</a>';
      list.appendChild(li);
    });
    if (list.children.length) setActive(0);
  }

  input.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(run, 80);
  });

  input.addEventListener('keydown', function (e) {
    var n = list.children.length;
    if (e.key === 'ArrowDown' && n) {
      e.preventDefault();
      setActive((active + 1) % n);
    } else if (e.key === 'ArrowUp' && n) {
      e.preventDefault();
      setActive((active - 1 + n) % n);
    } else if (e.key === 'Escape') {
      /* type=search 的输入框会先吞掉 Esc 用来清空，这里直接关弹窗 */
      e.preventDefault();
      close();
    } else if (e.key === 'Enter') {
      e.preventDefault();
      var a = list.children[active] && list.children[active].querySelector('a');
      if (a) a.click();
    }
  });

  dialog.querySelector('.search-form').addEventListener('submit', function (e) {
    e.preventDefault();
  });
  dialog.querySelector('.search-close').addEventListener('click', close);

  /* 点弹窗外的遮罩关闭 */
  dialog.addEventListener('click', function (e) {
    if (e.target === dialog) close();
  });

  list.addEventListener('click', function (e) {
    if (typeof gtag === 'function' && e.target.closest('a')) {
      gtag('event', 'search', { search_term: input.value.trim() });
    }
  });

  document.querySelectorAll('[data-search-open]').forEach(function (btn) {
    btn.addEventListener('click', open);
  });

  document.addEventListener('keydown', function (e) {
    if (dialog.open || e.defaultPrevented) return;
    var tag = (e.target.tagName || '').toLowerCase();
    var typing = tag === 'input' || tag === 'textarea' || tag === 'select' || e.target.isContentEditable;
    if ((e.key === 'k' || e.key === 'K') && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      open();
    } else if (e.key === '/' && !typing && !e.ctrlKey && !e.metaKey && !e.altKey) {
      e.preventDefault();
      open();
    }
  });
})();
