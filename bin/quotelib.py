"""Shared quote matching for bin/check-quotes.py and bin/evidence-cards.py.

Finding a quotation in a post, deciding which source link it belongs to, and
normalising text so a quote compares equal to a PDF text layer are the same
problem for the checker (is the quote really there?) and for the evidence
cards (where on the page is it?). Keeping one copy means a card can never be
drawn for a quote the checker would have matched differently.

Requires PyMuPDF (pip install pymupdf).
"""

import difflib
import hashlib
import html
import json
import re
import unicodedata
import urllib.request
from urllib.parse import unquote, urlparse

import fitz

LINK = re.compile(r'\]\(https://aarhusworks\.com/(assets/[^)#\s]+)(?:#page=(\d+))?\)')
ANY_ASSET = re.compile(r'https://aarhusworks\.com/(assets/[^)#\s]+)')
EXT_LINK = re.compile(r'\]\((https?://(?!aarhusworks\.com)[^)\s]+)\)')
SECTION = re.compile(r'^#{1,6} ', re.M)
TODO = re.compile(r'\[TODO:[^\]]*\]')
# "* **Bilag 48:** Aarhus Kommune, *"Oversigt høringsbidrag"*" names a
# document; the quotation marks set off its title, they do not quote it.
BILAG_LINE = re.compile(r'[ \t]*[*-][ \t]+\*\*Bilag[ \t]+\w+:\*\*')
MIN_QUOTE = 15

# Sources outside the site: laws on danskelove.dk, ombudsman statements and
# guidance on retsinformation.dk, and the like. They are fetched once and kept
# as text under CACHE, so the check also runs offline and in the hook.
CACHE = 'bin/kildecache'
PAYWALL = ('ing.dk',)
SUMMARY = 2500        # characters; less than this is an abstract, not the text
GAP = 600             # characters of running header/footer at a page break

# Quotations checked by hand, against a scan with no text layer and the like.
MANUAL = 'bin/kilder-manuelt.json'
EDITORIAL = re.compile(r'\[[^\]]{0,40}\]')
ELLIPSIS = re.compile(r'\(\s*\.\.\.\s*\)|\.\.\.|…')

# The filing links to its own rendered PDFs — the anmodning and the tillæg link
# to themselves and to each other — which contain every word of the filing.
# Left in the pool of cited sources they verify every quote against GRG's own
# text, so NOT FOUND drops to zero and the check goes blind. Exclude them,
# both as the pool and as the citation a quote is attached to.
SELF = ('assets/giber-ringvej/klage/anmodning-om-tilsynssag.pdf',
        'assets/giber-ringvej/klage/anmodning-om-tilsynssag-tillaeg.pdf')


def norm(s):
    s = unicodedata.normalize('NFC', s)
    # A soft hyphen marks a wrap the layout program inserted, and the text
    # layer often keeps the line break as a space after it: "for<shy> ventes".
    # Dropping the character alone leaves "for ventes", which matches nothing.
    s = re.sub('­\\s*', '', s)
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)      # inline link -> its text
    s = re.sub(r'[*_`]', '', s)                          # markdown emphasis
    for a, b in (('“', '"'), ('”', '"'), ('„', '"'),
                 ('’', "'"), ('‘', "'"),
                 ('–', '-'), ('—', '-'), ('−', '-'),
                 (' ', ' ')):
        s = s.replace(a, b)
    # Quotation marks inside a quote are a matter of house style: the filing
    # sets the source's ”notat vedr. …” as 'notat vedr. …', and an apostrophe
    # may be ' or ’. Neither side's marks carry the words, so both are dropped.
    s = re.sub('["\']', '', s)
    # PDF text layers break words across lines with a hyphen, but Danish
    # administrative prose is also full of real compound hyphens
    # ("VVM-bekendtgørelsen"), and a line break can fall on one of those.
    # Removing the hyphen turns it into "VVMbekendtgørelsen"; keeping it
    # turns a wrap into "anlægs-virkning". Dropping every hyphen on both
    # sides is symmetric, so either spelling compares equal.
    # Except between digits: there the hyphen is a range, and dropping it
    # makes "1-2 dB" equal "12 dB". A range wrapped after its hyphen
    # ("1-" / "2 dB") once passed as twelve. Mark it instead, wrap or not.
    s = re.sub(r'(?<=\d)-\s*(?=\d)', '~', s)
    s = re.sub(r'-\s*\n\s*', '-', s)
    s = s.replace('-', '')
    # A footnote marker in a PDF text layer glues its digit to the preceding
    # word ("miljøvurderingslovens1 § 57"), which no quotation reproduces.
    # Only digits directly abutting a letter are dropped; every ordinary
    # number in the text is preceded by a space and survives.
    s = re.sub(r'(?<=[a-zæøåA-ZÆØÅ])\d{1,2}(?!\d)', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip().lower()


def fragments(quote):
    """Quote -> the literal pieces that must appear, in order."""
    parts = ELLIPSIS.split(quote)
    out = []
    for p in parts:
        out.extend(EDITORIAL.split(p))
    return [f.strip() for f in out if len(f.strip()) > 6]


def contains_in_order(haystack, frags):
    pos = 0
    for f in frags:
        i = haystack.find(f, pos)
        if i < 0:
            return False
        pos = i + len(f)
    return True


class Sources:
    """Cited files under the site root, opened and normalised once each."""

    def __init__(self, root):
        self.root = root
        self._cache = {}
        self._annots = {}
        self._ext = {}

    def path(self, rel):
        # Links are URL-encoded (æøå, spaces). Without decoding, fitz.open
        # raises, the caller swallows it, and a perfectly readable PDF is
        # reported as a scan with no text layer — so its quotes are never
        # checked at all.
        return self.root / unquote(rel)

    def pages(self, rel):
        """-> list of normalised page texts, or None if the source has no text."""
        if rel in self._cache:
            return self._cache[rel]
        path = self.path(rel)
        pages = None
        try:
            if path.suffix.lower() == '.pdf':
                doc = fitz.open(path)
                pages = [norm(p.get_text()) for p in doc]
                if sum(len(p) for p in pages) < 50:
                    pages = None                          # scan with no text layer
            elif path.suffix.lower() in ('.txt', '.md'):
                pages = [norm(path.read_text(encoding='utf-8', errors='replace'))]
        except Exception:
            pages = None
        self._cache[rel] = pages
        return pages

    def annots(self, rel):
        """-> per page, the normalised text of its comments (sticky notes etc.).

        The kommune answers fact sheets by commenting in the PDF; those
        answers are quoted, and they are not in the page's text layer.
        """
        if rel not in self._annots:
            out = []
            try:
                if self.path(rel).suffix.lower() == '.pdf':
                    for page in fitz.open(self.path(rel)):
                        out.append(norm(' '.join(a.info.get('content', '')
                                                  for a in page.annots() or [])))
            except Exception:
                out = []
            self._annots[rel] = out
        return self._annots[rel]

    def in_annotation(self, rel, frags, page):
        notes = self.annots(rel)
        return 1 <= page <= len(notes) and contains_in_order(notes[page - 1], frags)

    def find_in(self, rel, frags, cited=0):
        """-> 1-based page the quote is on, 0 if it spans a page break, or None.

        The cited page is tried first: a phrase that recurs throughout a report
        would otherwise be reported as a page mismatch just because some earlier
        page also contains it.
        """
        pages = self.pages(rel)
        if not pages:
            return None
        if cited and 1 <= cited <= len(pages) and contains_in_order(pages[cited - 1], frags):
            return cited
        for i, page in enumerate(pages):
            if contains_in_order(page, frags):
                return i + 1
        spans = across(pages, frags)
        if spans:
            return cited if cited in spans else spans[0]
        for i, notes in enumerate(self.annots(rel)):
            if notes and contains_in_order(notes, frags):
                return i + 1
        joined = ' '.join(pages)                          # spans a page break
        return 0 if contains_in_order(joined, frags) else None

    def external(self, url):
        """-> (normalised texts or None, why it cannot be checked or None)."""
        if url not in self._ext:
            host = urlparse(url).hostname or ''
            if any(host == d or host.endswith('.' + d) for d in PAYWALL):
                self._ext[url] = (None, 'er bag betalingsmur')
            else:
                text = self._fetch(url)
                if text is None:
                    self._ext[url] = (None, 'kunne ikke hentes')
                elif host.endswith('retsinformation.dk') and len(text) < SUMMARY:
                    # Older ombudsman statements are on retsinformation.dk as
                    # an index entry only. (A short text elsewhere is just a
                    # short provision, and is checked like any other.)
                    self._ext[url] = ([norm(text)], 'har kun et resumé, ikke selve teksten')
                else:
                    self._ext[url] = ([norm(text)], None)
        return self._ext[url]

    def _fetch(self, url):
        cache = self.root / CACHE / (hashlib.sha1(url.encode()).hexdigest()[:16] + '.txt')
        if cache.exists():
            return cache.read_text(encoding='utf-8').split('\n', 1)[1]
        # retsinformation.dk serves a JavaScript app; the document itself is
        # at the same ELI address with /xml added.
        get = url
        if urlparse(url).hostname in ('retsinformation.dk', 'www.retsinformation.dk') \
                and '/eli/' in url and not url.rstrip('/').endswith('/xml'):
            get = url.rstrip('/') + '/xml'
        try:
            req = urllib.request.Request(get, headers={'User-Agent': 'Mozilla/5.0 aarhusworks citatkontrol'})
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read()
                kind = r.headers.get('content-type', '')
        except Exception:
            return None
        if 'pdf' in kind or body[:5] == b'%PDF-':
            text = ' '.join(p.get_text() for p in fitz.open(stream=body, filetype='pdf'))
        else:
            page = body.decode('utf-8', 'replace')
            page = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', page)
            text = html.unescape(re.sub(r'<[^>]+>', ' ', page))
        text = ' '.join(text.split())
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(url + '\n' + text, encoding='utf-8')
        return text


def across(pages, frags):
    """-> (page, next page) if the quote runs over a page break, else None.

    A sentence that continues on the next page has the running footer of one
    page and the header of the next between its halves ("... som deciderede
    TEKNIK OG MILJØ ... Side 2 af 2 støjvolde."). One fragment is allowed to
    break there, provided each half is long enough to identify it and sits
    within GAP characters of the break.
    """
    for j, f in enumerate(frags):
        if len(f) < 24:
            continue
        for i in range(len(pages) - 1):
            a, b = pages[i], pages[i + 1]
            tail, head = a[-(GAP + len(f)):], b[:GAP + len(f)]
            if f[:12] not in tail and f[-12:] not in head:
                continue
            for k in range(len(f) - 6, 5, -1):
                p = tail.rfind(f[:k])
                if p < 0 or len(tail) - (p + k) > GAP:
                    continue
                q = head.find(f[k:])
                if q < 0 or q > GAP:
                    continue
                if (contains_in_order(a[:len(a) - len(tail) + p], frags[:j])
                        and contains_in_order(b[q + len(f) - k:], frags[j + 1:])):
                    return i + 1, i + 2
    return None


def in_range(raw, link, page_no):
    """-> whether the link's own text ("bilag 58, s. 6–7") spans page_no.

    #page= can only open the first page of a range; a quote on the next page
    of it is cited correctly.
    """
    text = raw[raw.rfind('[', 0, link.start()):link.start()]
    return any(int(a) <= page_no <= int(b)
               for a, b in re.findall(r's\.\s*(\d+)\s*[–-]\s*(\d+)', text))


def labels(*raws):
    """-> the headings and bold lead-ins of the posts, normalised.

    "uddybes nedenfor under "Kommunens forsvar rækker ikke"" names a section
    of the filing; it does not quote a source.
    """
    out = set()
    for raw in raws:
        for m in re.finditer(r'^#{1,6}\s+(.+?)\s*$', raw, re.M):
            out.add(norm(m.group(1)).rstrip('.'))
        # Only a bold lead-in opening a paragraph; bold inside running text
        # is emphasis, often of words inside a quotation.
        for m in re.finditer(r'^(?:[ \t]*(?:>|[*-]|\d+\.)[ \t]*)?\*\*([^*\n]{3,200}?)\*\*', raw, re.M):
            out.add(norm(m.group(1)).rstrip('.'))
    return out


def linked_posts(raw, posts):
    """-> the text of the posts this one links to (the anmodning and its tillæg
    refer to each other's sections by name)."""
    out = []
    for y, mo, d, slug in set(re.findall(
            r'aarhusworks\.com/(?:[^/\s)]+/)?(\d{4})/(\d{2})/(\d{2})/([\w-]+)\.html', raw)):
        path = posts / f'{y}-{mo}-{d}-{slug}.md'
        if path.exists():
            out.append(path.read_text(encoding='utf-8'))
    return out


def manual(root):
    """-> checked-by-hand entries from MANUAL, keyed by the quote's fragments."""
    path = root / MANUAL
    if not path.exists():
        return {}
    entries = json.loads(path.read_text(encoding='utf-8'))
    return {' '.join(fragments(norm(e['citat']))): e for e in entries}


def verify(raw, item, sources, own, by_hand, assets):
    """-> (state, kind, detail) for one quotation from cited_quotes().

    state is 'ok', 'warn' (found, but the citation's page is another),
    'unverifiable' (the source cannot be read, or none is given; detail says
    why) or 'error' (the source can be read and the quote is not in it).
    """
    m, quote, frags, link = item
    entry = by_hand.get(' '.join(frags))
    if entry:
        return 'ok', 'manual', entry

    unread = None    # why the linked source cannot be read
    why = None       # why an external source in the section cannot be read
    rel = link.group(1) if link else None
    if link:
        cited = int(link.group(2) or 0)
        if sources.pages(rel) is None:
            unread = f'kilden ({unquote(rel.rsplit("/", 1)[-1])}) er en scanning eller et billede uden tekst'
        else:
            page = sources.find_in(rel, frags, cited)
            if page is None and cited and len(sources.pages(rel)) >= cited \
                    and len(sources.pages(rel)[cited - 1]) < 50:
                unread = (f's. {cited} i kilden ({unquote(rel.rsplit("/", 1)[-1])}) '
                       f'er en scanning uden tekst')
            if page is not None:
                if (not cited or page in (0, cited) or in_range(raw, link, page)
                        or _page_cited_nearby(raw, (m.start(), link.start()), rel, page)
                        or (page == 1 and contains_in_order(sources.pages(rel)[0][:300], frags))):
                    return 'ok', 'cited', (rel, cited, page)
                return 'warn', 'otherpage', (rel, cited, page)

    for a in assets:
        if a != rel:
            page = sources.find_in(a, frags)
            if page is not None:
                return 'ok', 'elsewhere', (a, page)

    section = max((h.start() for h in SECTION.finditer(raw, 0, m.start())), default=0)
    following = SECTION.search(raw, m.end())
    urls = list(dict.fromkeys(EXT_LINK.findall(raw, section, following.start() if following else len(raw))))
    for url in urls:
        texts, reason = sources.external(url)
        if texts and any(contains_in_order(t, frags) for t in texts):
            return 'ok', 'external', url
        if reason and why is None:
            why = f'kilden ({urlparse(url).hostname}) {reason}'
    # Failing the section's own sources, any external source the post cites:
    # a statement is often quoted where it is discussed, and linked where it
    # was first introduced.
    for url in dict.fromkeys(EXT_LINK.findall(raw)):
        if url not in urls:
            texts, _ = sources.external(url)
            if texts and any(contains_in_order(t, frags) for t in texts):
                return 'ok', 'external', url
    # Only now, so that a quote which is also a section's name is checked
    # against its source first: a reference to a section of the filing, and a
    # document's title in the bilag list, which may be the document's own
    # name for itself rather than words printed in it.
    if norm(quote).rstrip('.') in own:
        return 'ok', 'internal', None
    if BILAG_LINE.match(raw, raw.rfind('\n', 0, m.start()) + 1):
        return 'ok', 'title', None

    # Not found. A source that can be read and does not hold the quote makes
    # it an error, whatever else in the section cannot be read: a paywalled
    # article two sentences on does not excuse a misquoted report.
    near = closest(sources, quote, assets, EXT_LINK.findall(raw))
    if link and not unread:
        return 'error', 'missing', (rel, int(link.group(2) or 0), near)
    # Nearly the words of a source that can be read is a misquote, not a quote
    # from somewhere unreadable — it differs from what the source says.
    if near:
        return 'error', 'differs', near
    if unread or why:
        return 'unverifiable', 'unreadable', unread or why
    if urls:
        return 'error', 'unmatched', urls
    return 'unverifiable', 'nosource', 'der er ingen kilde ved citatet, der kan kontrolleres mod'


def closest(sources, quote, assets, urls):
    """-> (where, page, the source's own words) closest to a quote, or None.

    Only for quotes that matched nowhere: a near match is reported, with what
    the source actually says, so a quote that is almost right is shown as
    the misquote it is rather than as one whose source cannot be found. Short
    quotes need a closer match, since a few common words match anything.
    """
    q = norm(EDITORIAL.sub(' ', ELLIPSIS.sub(' ', quote)))
    q = re.sub(r'\s+', ' ', q).strip()
    if len(q) < MIN_QUOTE:
        return None
    need = 0.9 if len(q) < 40 else 0.85
    words = set(re.findall(r'\w{6,}', q))
    best = (need, None)
    pool = [(a, i + 1, t) for a in assets for i, t in enumerate(sources.pages(a) or [])]
    pool += [(a, i + 1, t) for a in assets for i, t in enumerate(sources.annots(a)) if t]
    pool += [(u, 0, t) for u in dict.fromkeys(urls) for t in (sources.external(u)[0] or [])]
    for where, page, text in pool:
        for w in sorted((w for w in words if w in text), key=text.count)[:2]:
            for hit in list(re.finditer(re.escape(w), text))[:20]:
                window = text[max(0, hit.start() - len(q)): hit.end() + len(q)]
                sm = difflib.SequenceMatcher(None, window, q, autojunk=False)
                blocks = [b for b in sm.get_matching_blocks() if b.size]
                ratio = sum(b.size for b in blocks) / len(q)
                if ratio > best[0]:
                    words_from = window.rfind(' ', 0, blocks[0].a) + 1
                    words_to = window.find(' ', blocks[-1].a + blocks[-1].size)
                    words_seen = window[words_from:None if words_to < 0 else words_to]
                    best = (ratio, (where, page, words_seen.replace('~', '-')))
    return best[1]


def _page_cited_nearby(raw, offsets, rel, page):
    """-> whether the quote's paragraph, or its link's, also cites that page.

    "jf. [bilag 56, s. 3](…). … Teknisk Udvalgs erklæring … ([bilag 56,
    s. 5](…)):" — the block quote below takes the first link as its own, but
    the lead-in cites the page it is on as well. A link to the whole document
    counts too.
    """
    for at in offsets:
        start = raw.rfind('\n', 0, at) + 1
        end = raw.find('\n', at)
        for other in LINK.finditer(raw, start, len(raw) if end < 0 else end):
            if other.group(1) == rel and int(other.group(2) or 0) in (0, page):
                return True
    return False


class _Span:
    """A quotation in the post: the text between its marks, and where it is."""

    def __init__(self, start, end, text):
        self._start, self._end, self.text = start, end, text

    def start(self):
        return self._start

    def end(self):
        return self._end


def quotations(raw):
    """Yield every run of text between straight quotation marks.

    Marks are paired in order within a line, as kramdown pairs them. Matching
    each opening mark with the next mark at least so many characters on, as
    a single pattern does, pairs a short quote's closing mark with the next
    quote's opening one and checks the prose in between as a quotation.
    An HTML attribute value (id="tillaeg-b6") is not a quotation.
    """
    for line in re.finditer(r'[^\n]+', raw):
        s, off = line.group(0), line.start()
        start, attr = None, False
        for j, ch in enumerate(s):
            if ch != '"':
                continue
            if attr:
                attr = False
            elif start is None:
                if j > 0 and s[j - 1] == '=':
                    attr = True
                else:
                    start = j
            else:
                yield _Span(off + start, off + j + 1, s[start + 1:j])
                start = None


def body_start(raw):
    front = re.match(r'﻿?---\r?\n.*?\r?\n---\r?\n', raw, re.S)
    return front.end() if front else 0


def cited_quotes(raw):
    """Yield every quotation in a post with the source link it belongs to.

    Yields (match, quote, frags, link) where link is a LINK match or None, or
    None alone for a span that looks quoted but is not a quotation.
    """
    body = body_start(raw)
    todos = [(t.start(), t.end()) for t in TODO.finditer(raw)]
    for m in quotations(raw):
        quote = m.text
        if len(quote) < MIN_QUOTE:
            continue
        # The title in the front matter and the instructions in a [TODO: ...]
        # are not quotations.
        line_start = raw.rfind('\n', 0, m.start()) + 1
        if m.start() < body or any(a <= m.start() < b for a, b in todos):
            yield None
            continue
        # A line with an unbalanced " shifts every pair after it, so a "quote"
        # that opens on markdown punctuation is a mis-paired span, not
        # something to report against a source.
        if '](' in quote or len(quote) > 600 or quote.lstrip()[:1] in '*])>|':
            yield None
            continue
        frags = fragments(norm(quote))
        if not frags:
            yield None
            continue

        # A quote set as a block quote carries its citation in the lead-in line
        # above it ("... bestemmer udtrykkeligt, jf. [bilag 56, s. 4](...):"),
        # not after it. Looking only forward attaches such a quote to whatever
        # link happens to open the next paragraph, which then reads as a wrong
        # page anchor. Look backwards for these, forwards for everything else —
        # a plain running-text quote preceded by an unrelated link must not be
        # captured by it.
        in_blockquote = raw[line_start:m.start()].lstrip().startswith('>')

        link = None

        # In a table the citation lives in a cell of the same row — sometimes after
        # the quote ("| quote ([bilag 22, s. 5]) |"), sometimes in an earlier cell
        # ("| Rambøll, [bilag 16a, s. 3] | quote |"). Either way it must not be
        # taken from a neighbouring paragraph, so the search is confined to the row.
        if raw[line_start:m.start()].lstrip().startswith('|'):
            row_end = raw.find('\n', m.end())
            row_end = len(raw) if row_end < 0 else row_end
            after = LINK.search(raw[m.end():row_end])
            if after:
                link = _shift(after, m.end())
            else:
                in_row = list(LINK.finditer(raw[line_start:m.start()]))
                link = _shift(in_row[-1], line_start) if in_row else None

        window = max(0, m.start() - 300)
        before = list(LINK.finditer(raw[window:m.start()]))
        if link is None and before:
            between = raw[window + before[-1].end(): m.start()]
            # "jf. [bilag 15, s. 2](...): *"..."*" — a citation separated from its
            # quote by nothing but a colon introduces that quote, whether the quote
            # follows in running text or as a block quote.
            introduces = ':' in between and not between.strip(' *_"\r\n\t>:')
            if in_blockquote or introduces:
                link = _shift(before[-1], window)
        if link is None:
            after = LINK.search(raw[m.end(): m.end() + 260])
            link = _shift(after, m.end()) if after else None
        if link and link.group(1) in SELF:
            link = None
        yield m, quote, frags, link


class _Shifted:
    """A LINK match found in a slice of the post, with offsets into the whole."""

    def __init__(self, m, offset):
        self._m, self._offset = m, offset

    def group(self, i):
        return self._m.group(i)

    def start(self):
        return self._m.start() + self._offset


def _shift(m, offset):
    return _Shifted(m, offset)
