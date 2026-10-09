"""Renders an "evidence card" for every quotation a post makes from a PDF.

    python bin/evidence-cards.py _posts/2026-08-26-anmodning-om-tilsynssag.md

For each quote that bin/check-quotes.py would verify against the source it
cites, this crops the PDF page around the quote, highlights the quoted words,
and saves the crop as WebP under assets/evidence/<post slug>/. The reader then
sees the document itself, not our retyping of it.

A quote gets a card at its own citation link when that source holds it.
Otherwise only when the source is not in doubt: the nearest citation before
it in its section holds it, or (for quotes of MIN_WORDS words or more) the
same quote is carded at its link elsewhere, or exactly one cited document
contains it. Those cards hang on the quotation itself.

The post is never touched. A manifest, _data/evidence/<post slug>.json, holds
the cards by link (href and which occurrence of it) and by quotation (its
normalised text and which occurrence), and assets/js/evidence.js attaches
them in the browser. It also records, for every quotation, why it has a card
or not; while the filing is a draft (the anmodning still has [TODO: markers,
as for the KLADDE stamp in bin/anmodning2pdf.mjs) the page marks every
quotation and lists what to check. Once filed, the published page leaves
that out, and only a local build shows it. The filing PDF from
bin/anmodning2pdf.mjs is built from the Markdown and so never sees any of it.

The pre-commit hook runs it with --stage whenever the post is staged, and adds
the images and manifest to the commit. Only new or changed quotes are drawn:
an image is named by a hash of its source PDF's content, the page, the quote
and RENDER, so an existing file is still correct. Images no longer referenced
by the post are deleted. Requires PyMuPDF and Pillow.
"""

import hashlib
import io
import json
import pathlib
import re
import subprocess
import sys
from urllib.parse import unquote

from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, str(pathlib.Path(__file__).parent))

import fitz                                                   # noqa: E402
from quotelib import (ANY_ASSET, LINK, SELF, Sources,          # noqa: E402
                      cited_quotes, norm)

ROOT = pathlib.Path(__file__).resolve().parent.parent
DPI = 144
CONTEXT = 40          # a context line further than this from the quote is left out
PAD = 6               # points of white around the outermost lines
MARGIN = 14           # points of white beside the text column
MAX_WIDTH = 1400      # pixels; twice the post column, so it stays sharp
RENDER = 1            # raise when the crop or highlight changes, to redraw all
MIN_WORDS = 4         # a shorter quote found in one document only is too generic
SECTION = re.compile(r'^#{1,6} ', re.M)
SHEET = 700           # points; text wider than this is a drawing, not prose
SHEET_CONTEXT = 160   # points of a drawing shown around the quote

# Many municipal PDFs have a broken tag tree; MuPDF reports it on every page
# it reads, and it has no bearing on the text or the rendering.
fitz.TOOLS.mupdf_display_errors(False)


def locate(page, frags):
    """-> list of rects, one per line of the page the quote covers, or None.

    norm() works on whole strings, so it is applied here word by word and the
    words are joined without separators: a wrap hyphen, a soft hyphen or a
    footnote digit then disappears exactly as it does for the checker, and
    the match maps straight back to the words it came from.
    """
    words = page.get_text('words')
    text, owner = [], []
    for i, w in enumerate(words):
        word = w[4]
        # A range wrapped after its hyphen ("1-" / "2 dB") is split over two
        # words; norm() only sees the range when both halves are in view.
        if (re.search(r'\d[-–—−]$', word) and i + 1 < len(words)
                and words[i + 1][4][:1].isdigit()):
            word = word[:-1] + '~'
        n = norm(word).replace(' ', '')
        text.append(n)
        owner.extend([i] * len(n))
    text = ''.join(text)

    frags = [f.replace(' ', '') for f in frags]
    starts, pos = [], 0
    for f in frags:
        i = text.find(f, pos)
        if i < 0:
            return None
        starts.append(i)
        pos = i + len(f)
    # Fragments split by an ellipsis or a bracket ("projektet [er] fortsat")
    # are found first-come, and a short one can match a paragraph too early.
    # Pull each back to the occurrence nearest the fragment after it.
    for k in range(len(frags) - 2, -1, -1):
        starts[k] = text.rfind(frags[k], 0, starts[k + 1])
    hit = set()
    for f, i in zip(frags, starts):
        hit.update(owner[i:i + len(f)])

    lines = {}
    for i in sorted(hit):
        x0, y0, x1, y1, _, block, line, _ = words[i]
        r = lines.setdefault((block, line), fitz.Rect(x0, y0, x1, y1))
        r.include_rect(fitz.Rect(x0, y0, x1, y1))
    return list(lines.values())


def context_band(page, quote):
    """-> (top, bottom) showing the quote plus one whole line above and below.

    Word boxes span the font's full ascender and descender and overlap the
    next line, so cutting on them slices a neighbouring line in half. Lines
    are measured from their baseline instead, and each cut falls midway in
    the gap between two lines.
    """
    lines = {}
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            for span in line['spans']:
                if not span['text'].strip():
                    continue
                base, size = span['origin'][1], span['size']
                key = round(base)
                top, bot = lines.get(key, (base - 0.8 * size, base + 0.25 * size))
                lines[key] = (min(top, base - 0.8 * size), max(bot, base + 0.25 * size))
    lines = sorted(lines.items())
    inside = [ext for base, ext in lines if quote.y0 < base <= quote.y1]
    if not inside:
        return quote.y0 - PAD, quote.y1 + PAD
    q_top, q_bot = min(e[0] for e in inside), max(e[1] for e in inside)
    above = [ext for base, ext in lines if ext[1] <= q_top + 1][::-1]
    below = [ext for base, ext in lines if ext[0] >= q_bot - 1]

    top = q_top - PAD
    if above and q_top - above[0][0] <= CONTEXT:
        top = (above[1][1] + above[0][0]) / 2 if len(above) > 1 else above[0][0] - PAD
        top = min(top, above[0][0] - 2)
    bottom = q_bot + PAD
    if below and below[0][1] - q_bot <= CONTEXT:
        bottom = (below[0][1] + below[1][0]) / 2 if len(below) > 1 else below[0][1] + PAD
        bottom = max(bottom, below[0][1] + 2)
    return top, bottom


def render(page, rects):
    """-> PIL image of the page around rects, with rects highlighted."""
    column = fitz.Rect()
    for w in page.get_text('words'):
        column.include_rect(fitz.Rect(w[:4]))
    quote = fitz.Rect(rects[0])
    for r in rects[1:]:
        quote.include_rect(r)
    sheet = column.width > SHEET

    if sheet:
        # Drawing labels are often set vertically, and a highlight on rotated
        # text renders as a blob. A frame reads the same at any angle.
        annot = page.add_rect_annot(quote + (-4, -4, 4, 4))
        annot.set_colors(stroke=(0.93, 0.6, 0))
        annot.set_border(width=3)
    else:
        annot = page.add_highlight_annot(rects)
        annot.set_colors(stroke=(1, 0.86, 0.2))
    annot.update()

    if sheet:
        # A drawing's "column" is the whole sheet; show the quote's surroundings.
        clip = quote + (-SHEET_CONTEXT, -SHEET_CONTEXT, SHEET_CONTEXT, SHEET_CONTEXT)
    else:
        top, bottom = context_band(page, quote)
        clip = fitz.Rect(min(column.x0, quote.x0) - MARGIN, top,
                         max(column.x1, quote.x1) + MARGIN, bottom)
    # Words and annotations are placed on the unrotated page, but the pixmap is
    # clipped on the page as displayed — a rotated drawing otherwise crops to
    # an empty strip off its edge.
    clip = (clip * page.rotation_matrix) & page.rect

    # Drawings and maps are printed at A1 and larger; at a fixed DPI their
    # crop would be tens of thousands of pixels wide.
    zoom = min(DPI / 72, MAX_WIDTH / clip.width)
    pix = page.get_pixmap(clip=clip, matrix=fitz.Matrix(zoom, zoom), annots=True)
    page.delete_annot(annot)
    # Where the quote sits across the crop, 0..1, so a phone that shows the
    # crop scrolled sideways can open it on the quote.
    shown = quote * page.rotation_matrix
    focus = round(((shown.x0 + shown.x1) / 2 - clip.x0) / clip.width, 3)
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples), focus


_digests = {}


def digest(path):
    """-> hash of a source file, so a replaced PDF gets its images redrawn."""
    if path not in _digests:
        _digests[path] = hashlib.sha1(path.read_bytes()).hexdigest()
    return _digests[path]


def occurrence(raw, href, before):
    """-> how many links to exactly href precede offset `before` in the post.

    The browser counts the same thing over the rendered links, which is how a
    card finds its link without the post carrying any marker.
    """
    target = re.compile(r'(?:\]\(|href=")' + re.escape(href) + r'(?:\)|")')
    return len(target.findall(raw, 0, before))


def in_range(raw, link, page_no):
    """-> whether the link's own text ("bilag 58, s. 6–7") spans page_no.

    #page= can only open the first page of a range; a quote on the next page
    of it is cited correctly.
    """
    text = raw[raw.rfind('[', 0, link.start()):link.start()]
    return any(int(a) <= page_no <= int(b)
               for a, b in re.findall(r's\.\s*(\d+)\s*[–-]\s*(\d+)', text))


def qkey(quote):
    """-> a quote as the browser finds it between its quotation marks.

    assets/js/evidence.js normalises the rendered text the same way; kramdown
    turns "..." into an ellipsis character, so both sides spell it out.
    """
    return norm(re.sub(r'\\(.)', r'\1', quote)).replace('…', '...').replace(' ', '')


def all_cards(manifest):
    """-> every card in a manifest, in either the old or the current layout."""
    if 'links' not in manifest:
        return [c for entries in manifest.values() for c in entries]
    return ([c for entries in manifest['links'].values() for c in entries]
            + [c for q in manifest['quotes'] for c in q['cards']])


def build(post):
    raw = post.read_text(encoding='utf-8')
    slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', post.stem)
    outdir = ROOT / 'assets' / 'evidence' / slug
    outdir.mkdir(parents=True, exist_ok=True)
    front = re.match(r'﻿?---\r?\n.*?\r?\n---\r?\n', raw, re.S)
    body_start = front.end() if front else 0

    sources = Sources(ROOT)
    pdfs = sorted(a for a in set(ANY_ASSET.findall(raw))
                  if a not in SELF and a.lower().endswith('.pdf'))
    docs = {}
    made = set()
    focus = {}
    reused = 0

    manifest = ROOT / '_data' / 'evidence' / f'{slug}.json'
    old_focus = {}
    if manifest.exists():
        for c in all_cards(json.loads(manifest.read_text(encoding='utf-8'))):
            old_focus[c['src'].rsplit('/', 1)[-1]] = c['focus']

    def card(rel, page_no, frags, quote):
        """-> the card for a quote on a page, or None if its words are not found."""
        nonlocal reused
        # The name is a hash of everything the image depends on, so an image
        # already on disk under it is still right and need not be drawn again.
        key = f'{RENDER}|{digest(sources.path(rel))}|{rel}|{page_no}|{" ".join(frags)}'
        name = hashlib.sha1(key.encode('utf-8')).hexdigest()[:12] + '.webp'
        img_path = outdir / name
        if name not in made:
            if img_path.exists() and name in old_focus:
                focus[name] = old_focus[name]
                reused += 1
            else:
                if rel not in docs:
                    docs[rel] = fitz.open(sources.path(rel))
                page = docs[rel][page_no - 1]
                rects = locate(page, frags)
                if not rects:
                    return None
                img, focus[name] = render(page, rects)
                img.save(img_path, 'WEBP', quality=72, method=6)
            made.add(name)
        w, h = Image.open(img_path).size
        return {
            'src': f'/assets/evidence/{slug}/{name}',
            'w': w, 'h': h,
            'focus': focus[name],
            'page': page_no,
            'file': unquote(rel.rsplit('/', 1)[-1]),
            'pdf': f'https://aarhusworks.com/{rel}#page={page_no}',
            'quote': ' '.join(re.sub(r'\\(.)', r'\1', quote.replace('*', '')).split()),
        }

    links = {}       # cards hung on their citation link: "<href>|<n>" -> cards
    quotes = []      # cards hung on the quotation itself, which has no link
    status = []      # every quotation and whether it got a card, for authors
    seen = {}        # qkey -> how many quotations with that text so far
    by_text = {}     # " ".join(frags) -> card made at a link, for repeats
    pending = []

    # Pass 1: quotations whose own citation link holds them.
    for item in cited_quotes(raw):
        if item is None or item[0].start() < body_start:
            continue
        m, quote, frags, link = item
        k = qkey(quote)
        shown = ' '.join(re.sub(r'\\(.)', r'\1', quote).split())
        if len(shown) > 120:
            shown = shown[:117].rsplit(' ', 1)[0] + ' …'
        record = {'key': k, 'n': seen.get(k, 0), 'quote': shown}
        seen[k] = record['n'] + 1
        status.append(record)

        if link is not None:
            rel, cited = link.group(1), int(link.group(2) or 0)
            # The source the text points to, so a quote to check can be
            # looked up without hunting for its link.
            record['src'] = unquote(rel.rsplit('/', 1)[-1]) + (f', s. {cited}' if cited else '')
            if not rel.lower().endswith('.pdf'):
                ext = rel.rsplit('.', 1)[-1].lower()
                record['note'] = f'kilden er en {ext}-fil, ikke en PDF'
                continue
            if sources.pages(rel) is None:
                record['note'] = 'kilden er en scanning uden tekst'
                continue
            page_no = sources.find_in(rel, frags, cited)
            if page_no == 0:
                record['note'] = 'citatet går over et sideskift'
                continue
            if page_no:
                c = card(rel, page_no, frags, quote)
                if c is None:
                    record['note'] = 'ordene kunne ikke placeres på siden'
                    continue
                href = f'https://aarhusworks.com/{rel}' + (f'#page={cited}' if cited else '')
                n = occurrence(raw, href, link.start())
                # The browser shows the card only if this text is next to the
                # link, so an edit that shifts the link count drops the card
                # rather than hanging it on the wrong citation.
                links.setdefault(f'{href}|{n}', []).append(
                    dict(c, anchor=frags[0].replace(' ', '')))
                by_text.setdefault(' '.join(frags), c)
                record['card'] = True
                record['note'] = ('ved henvisningen' if not cited or page_no == cited
                                  or in_range(raw, link, page_no) else
                                  f'henvisningen siger s. {cited}, citatet står på '
                                  f's. {page_no} — tjek, om henvisningen gælder citatet')
                continue
        pending.append((item, record))

    # Pass 2: quotations without a link that holds them. A card is made only
    # when the source is not in doubt; a phrase found in an arbitrary one of
    # the cited documents would put the wrong page beside the claim.
    # In order of how sure the source is: the nearest citation before the
    # quote in its section; then, for quotes long enough not to be a stock
    # phrase, the same quote carded at its link elsewhere, or the only cited
    # document that contains it.
    for (m, quote, frags, link), record in pending:
        c, note = None, None
        long_enough = len(quote.split()) >= MIN_WORDS
        section = max((h.start() for h in SECTION.finditer(raw, 0, m.start())),
                      default=body_start)
        for near in reversed(list(LINK.finditer(raw, section, m.start()))):
            rel = near.group(1)
            if rel in SELF or not rel.lower().endswith('.pdf'):
                continue
            page_no = sources.find_in(rel, frags, int(near.group(2) or 0))
            if page_no:
                c = card(rel, page_no, frags, quote)
                if c:
                    note = 'nærmeste henvisning før citatet i afsnittet'
                    break
        if c is None and long_enough and ' '.join(frags) in by_text:
            c, note = by_text[' '.join(frags)], 'samme citat har kort ved sin henvisning'
        if c is None:
            hits = [a for a in pdfs if sources.find_in(a, frags)]
            if len(hits) == 1 and long_enough:
                c = card(hits[0], sources.find_in(hits[0], frags), frags, quote)
                note = 'det eneste citerede dokument, der indeholder citatet'
            elif len(hits) > 1:
                note = f'står i {len(hits)} af de citerede dokumenter — kilden er tvetydig'
            elif hits:
                note = f'kun ét dokument, men under {MIN_WORDS} ord — for usikkert'
            elif link is not None:
                note = 'ikke fundet i den henviste kilde'
            else:
                note = 'ikke fundet i nogen citeret kilde (lovtekst, egne ord o.l.)'
        if c is not None:
            quotes.append({'key': record['key'], 'n': record['n'], 'cards': [c]})
            record['card'] = True
        record['note'] = note

    for stale in outdir.glob('*.webp'):
        if stale.name not in made:
            stale.unlink()

    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps({'links': links, 'quotes': quotes, 'status': status},
                                   ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

    carded = sum(1 for r in status if r.get('card'))
    size = sum(p.stat().st_size for p in outdir.glob('*.webp'))
    print(f'{post.name}: {carded} of {len(status)} quotations carded, {len(made)} images '
          f'({len(made) - reused} drawn, {reused} unchanged; {size // 1024} KB)')
    tally = {}
    for r in status:
        tally.setdefault((bool(r.get('card')), r['note'].split(' — ')[0]), []).append(r)
    for (ok, note), rs in sorted(tally.items(), key=lambda t: (not t[0][0], -len(t[1]))):
        print(f'  {"kort " if ok else "intet"} {len(rs):4}  {note}')
    return [outdir, manifest]


stage = '--stage' in sys.argv
outputs = []
for arg in sys.argv[1:]:
    if arg != '--stage':
        outputs += build(pathlib.Path(arg).resolve())
if stage and outputs:
    # -A so images the post no longer uses leave the commit along with it.
    subprocess.run(['git', 'add', '-A', '--', *map(str, outputs)], cwd=ROOT, check=True)
