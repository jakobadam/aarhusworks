// Table of contents for long posts, in the right margin on wide screens and
// as a folded "Indhold" box above the text on narrow ones. Built from the
// post's own h2/h3, so the Markdown needs no markup. The section being read
// is marked (aria-current) as the page scrolls.
//
// Only headings that are direct children of the article count: one inside a
// blockquote (the KLADDE notice) or inside a page's own components (the
// timeline) is not a section.
(function () {
  var MIN_SECTIONS = 3;   // fewer h2 than this, and the post gets no TOC
  var OFFSET = 96;        // a heading this close to the top counts as reached

  var article = document.querySelector('.post');
  var content = article && article.querySelector('.post-content');
  if (!content) return;

  var headings = [].filter.call(content.children, function (el) {
    return el.tagName === 'H2' || el.tagName === 'H3';
  });
  if (headings.filter(function (h) { return h.tagName === 'H2'; }).length < MIN_SECTIONS) return;

  var details = document.createElement('details');
  details.className = 'toc';
  var summary = document.createElement('summary');
  summary.textContent = 'Indhold';
  details.appendChild(summary);

  var root = document.createElement('ol');
  details.appendChild(root);
  var list = root, links = [], parents = [], parent = null, used = {};

  headings.forEach(function (h) {
    if (!h.id) {
      var base = h.textContent.trim().toLowerCase().replace(/[^\wæøå]+/g, '-').replace(/^-|-$/g, '') || 'afsnit';
      var id = base, n = 2;
      while (document.getElementById(id) || used[id]) id = base + '-' + n++;
      h.id = id;
    }
    used[h.id] = true;

    var li = document.createElement('li');
    var a = document.createElement('a');
    a.href = '#' + encodeURIComponent(h.id);
    a.textContent = h.textContent.trim();
    li.appendChild(a);

    if (h.tagName === 'H2' || !parent) {
      root.appendChild(li);
      parent = li;
      list = null;
    } else {
      if (!list) { list = document.createElement('ol'); parent.appendChild(list); }
      list.appendChild(li);
    }
    links.push(a);
    parents.push(h.tagName === 'H3' ? parent : null);
  });

  var rail = document.createElement('div');
  rail.className = 'toc-rail';
  rail.appendChild(details);
  var header = article.querySelector('.post-header');
  article.insertBefore(rail, header ? header.nextSibling : content);
  article.classList.add('has-toc');

  // Open in the margin, folded above the text ($toc-wide in main.scss).
  var wide = window.matchMedia('(min-width: 1280px)');
  function fit() { details.open = wide.matches; }
  fit();
  if (wide.addEventListener) wide.addEventListener('change', fit); else wide.addListener(fit);
  summary.addEventListener('click', function (e) { if (wide.matches) e.preventDefault(); });
  details.addEventListener('click', function (e) {
    if (!wide.matches && e.target.tagName === 'A') details.open = false;
  });

  var current = -1;
  function mark() {
    var i = -1;
    for (var k = 0; k < headings.length; k++) {
      if (headings[k].getBoundingClientRect().top <= OFFSET) i = k; else break;
    }
    // At the very bottom the last sections may never reach the top.
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) i = headings.length - 1;
    if (i === current) return;

    if (current >= 0) {
      links[current].removeAttribute('aria-current');
      if (parents[current]) parents[current].classList.remove('toc-open');
    }
    current = i;
    if (i < 0) return;
    links[i].setAttribute('aria-current', 'true');
    if (parents[i]) parents[i].classList.add('toc-open');

    // Keep the mark in view when the list is taller than the window, by
    // scrolling the list itself -- never the page.
    if (wide.matches && details.scrollHeight > details.clientHeight) {
      var top = links[i].offsetTop;   // the sticky <details> is the offsetParent
      if (top < details.scrollTop + 40 || top > details.scrollTop + details.clientHeight - 40) {
        details.scrollTop = top - details.clientHeight / 3;
      }
    }
  }

  var queued = false;
  function onScroll() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(function () { queued = false; mark(); });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  mark();
})();
