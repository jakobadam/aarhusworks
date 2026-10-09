// Evidence cards: shows, beside a quotation, the cropped page of the source PDF
// with the quoted words highlighted. The cards are made by
// bin/evidence-cards.py; the post itself carries no markup for them.
//
// window.EVIDENCE maps "<href>|<n>" to the cards for the n-th link (0-based)
// to that exact href in the post. Counting links in the rendered page gives
// the same n, since kramdown keeps the order of links.
(function () {
  var cards = window.EVIDENCE;
  var root = document.querySelector('.post-content');
  if (!cards || !root) return;

  var BLOCK = 'p, li, blockquote, td, th, dd';
  var MIN_WIDTH = 560;
  var seen = {};

  root.querySelectorAll('a[href]').forEach(function (a) {
    // Rendered mermaid diagrams are generated SVG, not prose; their links
    // are not in the count bin/evidence-cards.py makes.
    if (a.closest('.mermaid-svg')) return;
    var href = a.getAttribute('href');
    var n = seen[href] = (seen[href] === undefined ? 0 : seen[href] + 1);
    var list = cards[href + '|' + n];
    if (!list) return;
    // The post may have been edited since the cards were made; a card whose
    // quote is not beside this link belongs to another citation.
    var near = norm(nearby(a));
    list = list.filter(function (c) { return near.indexOf(c.anchor) >= 0; });
    if (list.length) attach(a, list);
  });

  // The text a citation documents: its block, and for a lead-in line
  // ("jf. [bilag 56, s. 4]:") the block quote that follows it.
  function nearby(a) {
    var block = a.closest(BLOCK);
    if (!block) return a.parentNode.textContent;
    var next = block.nextElementSibling;
    return block.textContent + ' ' + (next ? next.textContent : '');
  }

  // bin/quotelib.py's norm(), with whitespace dropped as the anchor is.
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

  function attach(a, list) {
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'ev-toggle';
    button.setAttribute('aria-expanded', 'false');
    button.title = 'Vis citatet i kilden';
    button.innerHTML = '<span aria-hidden="true">¶</span><span class="ev-label">kilde</span>';
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

    var figure = null;
    button.addEventListener('click', function () {
      if (!figure) {
        figure = render(list);
        place(a, button, figure);
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
  function place(a, button, figure) {
    var block = a.closest(BLOCK);
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
})();
