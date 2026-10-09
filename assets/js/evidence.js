// Evidence cards: shows, beside a quotation, the cropped page of the source PDF
// with the quoted words highlighted. The cards are made by
// bin/evidence-cards.py; the post itself carries no markup for them.
//
// window.EVIDENCE has two kinds of cards:
//   links  — "<href>|<n>" -> cards for the n-th link (0-based) to that exact
//            href. Counting links in the rendered page gives the same n,
//            since kramdown keeps the order of links.
//   quotes — cards for a quotation with no link of its own, found by its
//            text: the n-th quotation on the page with exactly that text.
// and, in local builds only, `status`: every quotation and why it has a card
// or not, shown by the "Kildestatus" panel. It is left out of the published
// page, which the other party can read.
(function () {
  var data = window.EVIDENCE;
  var root = document.querySelector('.post-content');
  if (!data || !root) return;

  var BLOCK = 'p, li, blockquote, td, th, dd';
  var MIN_WIDTH = 560;

  // Quotations are found before anything is inserted, then filled in from
  // the last to the first, so a split text node never moves a later target.
  var found = quotations();
  var byKey = {};
  found.forEach(function (q) { (byKey[q.key] = byKey[q.key] || []).push(q); });
  function at(key, n) { return (byKey[key] || [])[n]; }

  var jobs = [];
  (data.quotes || []).forEach(function (e) {
    var q = at(e.key, e.n);
    if (q) jobs.push({ q: q, order: 1, run: function (q) { attachToQuote(q, e.cards); } });
  });
  var missing = [];
  (data.status || []).forEach(function (r) {
    var q = at(r.key, r.n);
    if (q) jobs.push({ q: q, order: 0, run: function (q) { insertAfter(q, mark(r)); } });
    else missing.push(r);
  });
  jobs.sort(function (a, b) { return b.q.index - a.q.index || a.order - b.order; });
  jobs.forEach(function (j) { j.run(j.q); });

  var seen = {};
  root.querySelectorAll('a[href]').forEach(function (a) {
    // Rendered mermaid diagrams are generated SVG, not prose; their links
    // are not in the count bin/evidence-cards.py makes.
    if (a.closest('.mermaid-svg')) return;
    var href = a.getAttribute('href');
    var n = seen[href] = (seen[href] === undefined ? 0 : seen[href] + 1);
    var list = (data.links || {})[href + '|' + n];
    if (!list) return;
    // The post may have been edited since the cards were made; a card whose
    // quote is not beside this link belongs to another citation.
    var near = norm(nearby(a));
    list = list.filter(function (c) { return near.indexOf(c.anchor) >= 0; });
    if (list.length) attachToLink(a, list);
  });

  if (data.status) panel(data.status, missing);

  // Every run of text between quotation marks, with where its closing mark is.
  function quotations() {
    var out = [];
    var cur = null;
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    for (var t = walker.nextNode(); t; t = walker.nextNode()) {
      if (t.parentNode.closest('.mermaid-svg, script, style')) continue;
      for (var i = 0; i < t.data.length; i++) {
        var ch = t.data[i];
        if (ch === '“' || ch === '”' || ch === '"' || ch === '„') {
          if (cur && ch !== '„') {
            cur.end = t;
            cur.offset = i;
            cur.key = key(cur.text);
            cur.index = out.length;
            out.push(cur);
            cur = null;
          } else {
            cur = { text: '' };
          }
        } else if (cur) {
          cur.text += ch;
          if (cur.text.length > 4000) cur = null;      // an unpaired mark
        }
      }
    }
    return out;
  }

  // bin/evidence-cards.py's qkey().
  function key(s) {
    return norm(s.replace(/[*_`]/g, '')).replace(/…/g, '...');
  }

  // bin/quotelib.py's norm(), with whitespace dropped.
  function norm(s) {
    return s.normalize('NFC')
      .replace(/­/g, '')
      .replace(/[“”„]/g, '"').replace(/[’‘]/g, "'")
      .replace(/(\d)[-–—−]\s*(?=\d)/g, '$1~')
      .replace(/[-–—−]/g, '')
      .replace(/([a-zæøåA-ZÆØÅ])\d{1,2}(?!\d)/g, '$1')
      .replace(/\s+/g, '')
      .toLowerCase();
  }

  // Right after the closing quotation mark, and outside the <em> the
  // quotation is usually set in, so the button is not italic.
  function insertAfter(q, node) {
    var t = q.end;
    var i = q.offset + 1;
    if (i < t.data.length) {
      t.splitText(i);
      t.after(node);
      return;
    }
    var el = t;
    while (el.parentNode !== root && el.parentNode.lastChild === el &&
           /^(EM|STRONG|I|B)$/.test(el.parentNode.tagName)) {
      el = el.parentNode;
    }
    el.after(node);
  }

  // The text a citation documents: its block, and for a lead-in line
  // ("jf. [bilag 56, s. 4]:") the block quote that follows it.
  function nearby(a) {
    var block = a.closest(BLOCK);
    if (!block) return a.parentNode.textContent;
    var next = block.nextElementSibling;
    return block.textContent + ' ' + (next ? next.textContent : '');
  }

  function toggleButton() {
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'ev-toggle';
    button.setAttribute('aria-expanded', 'false');
    button.title = 'Vis citatet i kilden';
    button.innerHTML = '<span aria-hidden="true">¶</span><span class="ev-label">kilde</span>';
    return button;
  }

  function attachToQuote(q, list) {
    var button = toggleButton();
    insertAfter(q, button);
    wire(button, list);
  }

  function attachToLink(a, list) {
    var button = toggleButton();
    // After a closing bracket or quote mark that ends the citation, held on
    // one line with it, so "(bilag 20)" never wraps between ")" and button.
    var next = a.nextSibling;
    var tail = next && next.nodeType === 3 && /^[)\]”"’]+/.exec(next.data);
    if (tail) {
      var glue = document.createElement('span');
      glue.className = 'ev-glue';
      next.splitText(tail[0].length);
      next.before(glue);
      glue.append(next, button);
    } else {
      a.after(button);
    }
    wire(button, list);
  }

  function wire(button, list) {
    var figure = null;
    button.addEventListener('click', function () {
      if (!figure) {
        figure = render(list);
        place(button, figure);
        focus(figure, list);
      } else {
        figure.hidden = !figure.hidden;
      }
      button.setAttribute('aria-expanded', String(!figure.hidden));
    });
  }

  // A figure cannot sit inside a <p>, so it goes after the paragraph. In a
  // list item or table cell it stays inside, so it is not cut loose from the
  // point it documents.
  function place(button, figure) {
    var block = button.closest(BLOCK);
    if (!block || !root.contains(block)) {
      button.after(figure);
    } else if (block.matches('li, td, th, dd')) {
      block.appendChild(figure);
    } else {
      block.after(figure);
    }
  }

  // Scroll each too-wide crop so the highlighted quote is in view.
  function focus(figure, list) {
    figure.querySelectorAll('.ev-shot').forEach(function (shot, i) {
      if (shot.scrollWidth > shot.clientWidth) {
        shot.scrollLeft = list[i].focus * shot.scrollWidth - shot.clientWidth / 2;
      }
    });
  }

  function render(list) {
    var figure = document.createElement('figure');
    figure.className = 'ev-card';
    list.forEach(function (c) {
      var link = document.createElement('a');
      link.href = c.pdf;
      link.className = 'ev-shot';
      var img = document.createElement('img');
      img.src = c.src;
      img.width = c.w;
      img.height = c.h;
      img.loading = 'lazy';
      // Never smaller than the page printed at 100%: on a phone the crop
      // scrolls sideways rather than shrinking the text past reading.
      img.style.minWidth = Math.min(MIN_WIDTH, c.w / 2) + 'px';
      img.alt = 'Udsnit af ' + c.file + ', side ' + c.page +
                ', med citatet fremhævet: "' + c.quote + '"';
      link.appendChild(img);
      figure.appendChild(link);
    });
    var c = list[0];
    var caption = document.createElement('figcaption');
    caption.textContent = c.file + ', s. ' + c.page + ' — ';
    var open = document.createElement('a');
    open.href = c.pdf;
    open.textContent = 'åbn hele dokumentet';
    caption.appendChild(open);
    figure.appendChild(caption);
    return figure;
  }

  // ---- Local builds only: which quotations have a card, and why not.

  function mark(r) {
    var span = document.createElement('span');
    var warn = r.card && r.note.indexOf(' — ') >= 0;
    span.className = 'ev-mark ' + (warn ? 'ev-mark--warn' : r.card ? 'ev-mark--ok' : 'ev-mark--miss');
    span.textContent = r.card && !warn ? '✓' : (r.card ? '! ' : '✗ ') + r.note;
    span.title = r.note;
    return span;
  }

  function panel(status, missing) {
    var carded = status.filter(function (r) { return r.card; }).length;
    var box = document.createElement('aside');
    box.className = 'ev-panel';
    var text = document.createElement('span');
    text.textContent = 'Kildekort: ' + carded + ' af ' + status.length + ' citater';
    var button = document.createElement('button');
    button.type = 'button';
    box.append(text, button);
    if (missing.length) {
      var lost = document.createElement('span');
      lost.className = 'ev-panel-lost';
      lost.textContent = missing.length + ' citat(er) ikke fundet på siden';
      lost.title = missing.map(function (r) { return '"' + r.quote + '" — ' + r.note; }).join('\n');
      box.appendChild(lost);
    }
    function set(on) {
      root.classList.toggle('ev-status-on', on);
      button.textContent = on ? 'Skjul status' : 'Vis status';
    }
    button.addEventListener('click', function () {
      set(!root.classList.contains('ev-status-on'));
    });
    set(/[?&]kilder\b/.test(location.search));
    document.body.appendChild(box);
  }
})();
