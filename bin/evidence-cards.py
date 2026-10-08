"""Renders an "evidence card" for every quotation a post makes from a PDF.

    python bin/evidence-cards.py _posts/2026-08-26-anmodning-om-tilsynssag.md

For each quote that bin/check-quotes.py would verify against the source it
cites, this crops the PDF page around the quote, highlights the quoted words,
and saves the crop as WebP under assets/evidence/<post slug>/. The reader then
sees the document itself, not our retyping of it.

The post is never touched. A manifest, _data/evidence/<post slug>.json, maps
each citation link (its href and which occurrence of that href it is) to its
cards, and assets/js/evidence.js attaches them in the browser. The filing PDF
from bin/anmodning2pdf.mjs is built from the Markdown and so never sees them.

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
from quotelib import Sources, cited_quotes, norm              # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DPI = 144
CONTEXT = 40          # a context line further than this from the quote is left out
PAD = 6               # points of white around the outermost lines
MARGIN = 14           # points of white beside the text column
MAX_WIDTH = 1400      # pixels; twice the post column, so it stays sharp
RENDER = 1            # raise when the crop or highlight changes, to redraw all
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
        n = norm(w[4]).replace(' ', '')
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


def build(post):
    raw = post.read_text(encoding='utf-8')
    slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', post.stem)
    outdir = ROOT / 'assets' / 'evidence' / slug
    outdir.mkdir(parents=True, exist_ok=True)

    sources = Sources(ROOT)
    docs = {}
    cards = {}
    made = set()
    focus = {}
    eligible = 0
    reused = 0
    unplaced = []

    manifest = ROOT / '_data' / 'evidence' / f'{slug}.json'
    old_focus = {}
    if manifest.exists():
        for entries in json.loads(manifest.read_text(encoding='utf-8')).values():
            for c in entries:
                old_focus[c['src'].rsplit('/', 1)[-1]] = c['focus']

    for item in cited_quotes(raw):
        if item is None:
            continue
        m, quote, frags, link = item
        if link is None or not link.group(1).lower().endswith('.pdf'):
            continue
        rel, cited = link.group(1), int(link.group(2) or 0)
        page_no = sources.find_in(rel, frags, cited)
        if not page_no:             # not verified, no text layer, or spans pages
            continue
        eligible += 1

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
                    unplaced.append((quote[:70].replace('\n', ' '), rel, page_no))
                    continue
                img, focus[name] = render(page, rects)
                img.save(img_path, 'WEBP', quality=72, method=6)
            made.add(name)
        w, h = Image.open(img_path).size

        href = f'https://aarhusworks.com/{rel}' + (f'#page={cited}' if cited else '')
        n = occurrence(raw, href, link.start())
        cards.setdefault(f'{href}|{n}', []).append({
            'src': f'/assets/evidence/{slug}/{name}',
            'w': w, 'h': h,
            'focus': focus[name],
            'page': page_no,
            'file': unquote(rel.rsplit('/', 1)[-1]),
            'pdf': f'https://aarhusworks.com/{rel}#page={page_no}',
            'quote': ' '.join(re.sub(r'\\(.)', r'\1', quote.replace('*', '')).split()),
            # The browser shows the card only if this text is next to the
            # link, so an edit that shifts the link count drops the card
            # rather than hanging it on the wrong citation.
            'anchor': frags[0].replace(' ', ''),
        })

    for stale in outdir.glob('*.webp'):
        if stale.name not in made:
            stale.unlink()

    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps(cards, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

    size = sum(p.stat().st_size for p in outdir.glob('*.webp'))
    print(f'{post.name}: {eligible} quotes verified on a PDF page, '
          f'{eligible - len(unplaced)} carded, {len(made)} images '
          f'({len(made) - reused} drawn, {reused} unchanged; {size // 1024} KB) '
          f'in assets/evidence/{slug}/')
    return [outdir, manifest]
    if unplaced:
        print('  Verified but not located word by word — no card:')
        for short, rel, page_no in unplaced:
            print(f'    {rel} p. {page_no}: "{short}"')


stage = '--stage' in sys.argv
outputs = []
for arg in sys.argv[1:]:
    if arg != '--stage':
        outputs += build(pathlib.Path(arg).resolve())
if stage and outputs:
    # -A so images the post no longer uses leave the commit along with it.
    subprocess.run(['git', 'add', '-A', '--', *map(str, outputs)], cwd=ROOT, check=True)
