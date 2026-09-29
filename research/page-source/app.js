(function () {
  // Code blocks: wrap each <pre> and add a copy button.
  document.querySelectorAll('.content pre').forEach(function (pre) {
    var box = document.createElement('div');
    box.className = 'codeblock';
    pre.parentNode.insertBefore(box, pre);
    box.appendChild(pre);
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy';
    btn.textContent = 'Copy';
    btn.addEventListener('click', function () {
      var code = pre.querySelector('code') || pre;
      var text = code.innerText;
      var reset = function () { setTimeout(function () { btn.textContent = 'Copy'; }, 1600); };
      var fallback = function () {
        var range = document.createRange();
        range.selectNodeContents(code);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        btn.textContent = 'Selected';
        reset();
      };
      try {
        navigator.clipboard.writeText(text).then(function () { btn.textContent = 'Copied'; reset(); }, fallback);
      } catch (e) { fallback(); }
    });
    box.appendChild(btn);
  });

  // Catalog
  var dataEl = document.getElementById('tool-data');
  var grid = document.getElementById('grid');
  if (!dataEl || !grid) return;
  var data = JSON.parse(dataEl.textContent);
  var tools = data.tools;
  var cats = data.categories;
  var catLabel = {};
  cats.forEach(function (c) { catLabel[c.key] = c.label; });
  var LIC = { ok: 'Commercial use OK', nc: 'Non-commercial only', check: 'Check license', paid: 'Paid' };
  var state = { q: '', cat: 'all', commercial: false, gui: false, nogpu: false };

  var chipsEl = document.getElementById('cat-chips');
  function makeChip(label, key, n) {
    var b = document.createElement('button');
    b.type = 'button';
    b.dataset.key = key;
    b.textContent = label;
    var s = document.createElement('span');
    s.className = 'n';
    s.textContent = n;
    b.appendChild(s);
    b.addEventListener('click', function () { state.cat = key; syncChips(); render(); });
    return b;
  }
  function syncChips() {
    chipsEl.querySelectorAll('button').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.key === state.cat));
    });
  }
  chipsEl.appendChild(makeChip('All', 'all', tools.length));
  cats.forEach(function (c) {
    var n = tools.filter(function (t) { return t.c === c.key; }).length;
    if (n) chipsEl.appendChild(makeChip(c.label, c.key, n));
  });
  syncChips();

  function matches(t) {
    if (state.cat !== 'all' && t.c !== state.cat) return false;
    if (state.commercial && t.lk !== 'ok') return false;
    if (state.gui && !t.gui) return false;
    if (state.nogpu && t.gpu !== 'none') return false;
    if (state.q) {
      var hay = [t.n, t.w, t.f, t.i, t.h, t.l, t.k || '', catLabel[t.c] || ''].join(' ').toLowerCase();
      return state.q.split(/\s+/).every(function (w) { return hay.indexOf(w) !== -1; });
    }
    return true;
  }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function card(t) {
    var c = el('article', 'card');
    c.appendChild(el('span', 'tag', catLabel[t.c] || t.c));
    var h = el('h3');
    var a = el('a', null, t.n);
    a.href = t.u;
    a.target = '_blank';
    a.rel = 'noopener';
    h.appendChild(a);
    c.appendChild(h);
    c.appendChild(el('p', null, t.w));
    if (t.f) {
      var use = el('p', 'use');
      use.appendChild(el('b', null, 'Use it for: '));
      use.appendChild(document.createTextNode(t.f));
      c.appendChild(use);
    }
    var meta = el('div', 'meta');
    meta.appendChild(el('span', 'pill ' + t.lk, LIC[t.lk] + (t.l ? ' · ' + t.l : '')));
    if (t.i) meta.appendChild(el('span', 'pill', t.i));
    if (t.h) meta.appendChild(el('span', 'pill', t.h));
    if (t.s) meta.appendChild(el('span', 'pill', '★ ' + t.s));
    if (t.d) meta.appendChild(el('span', 'pill', 'Updated ' + t.d));
    if (t.v === false) meta.appendChild(el('span', 'pill check', 'Not verified at source'));
    c.appendChild(meta);
    return c;
  }

  var countEl = document.getElementById('count');
  function render() {
    var list = tools.filter(matches);
    grid.replaceChildren.apply(grid, list.map(card));
    if (!list.length) {
      grid.appendChild(el('p', 'empty', 'Nothing matches these filters. Turn off a filter or try a shorter search word.'));
    }
    countEl.textContent = list.length + ' of ' + tools.length + ' tools shown';
  }

  var q = document.getElementById('q');
  q.addEventListener('input', function () { state.q = q.value.trim().toLowerCase(); render(); });
  [['f-commercial', 'commercial'], ['f-gui', 'gui'], ['f-nogpu', 'nogpu']].forEach(function (pair) {
    var box = document.getElementById(pair[0]);
    box.addEventListener('change', function () { state[pair[1]] = box.checked; render(); });
    state[pair[1]] = box.checked;
  });
  state.q = q.value.trim().toLowerCase();
  render();
})();
