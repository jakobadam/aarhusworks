"""Checks that quoted text in a post actually appears in the source it cites.

Called by bin/check-anmodning.ps1 -Quotes. Requires PyMuPDF (pip install pymupdf).

Matching is exact containment after normalisation — never fuzzy. A quote that is
95% right is a defect in a document like this, and a similarity threshold would
hide exactly that.

Three things are deliberately treated as wildcards rather than literal text,
because they mark places the author signalled a change from the original:
an ellipsis, and editorial brackets like [er] or [k]ommunen. The fragments
around them must still appear, in order.
"""

import io
import pathlib
import re
import sys
import unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import fitz
except ImportError:
    print('ERROR: PyMuPDF not installed — run: pip install pymupdf')
    sys.exit(2)

ROOT = pathlib.Path(sys.argv[1]).resolve()
POST = pathlib.Path(sys.argv[2]).resolve()

QUOTE = re.compile(r'"([^"\r\n]{15,}?)"')
LINK = re.compile(r'\]\(https://aarhusworks\.com/(assets/[^)#\s]+)(?:#page=(\d+))?\)')
ANY_ASSET = re.compile(r'https://aarhusworks\.com/(assets/[^)#\s]+)')
EDITORIAL = re.compile(r'\[[^\]]{0,40}\]')
ELLIPSIS = re.compile(r'\(\s*\.\.\.\s*\)|\.\.\.|…')


def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('­', '')
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)      # inline link -> its text
    s = re.sub(r'[*_`]', '', s)                          # markdown emphasis
    for a, b in (('“', '"'), ('”', '"'), ('„', '"'),
                 ('’', "'"), ('‘', "'"),
                 ('–', '-'), ('—', '-'), ('−', '-'),
                 (' ', ' ')):
        s = s.replace(a, b)
    s = re.sub(r'-\s*\n\s*', '', s)                      # hyphenated line break
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


_cache = {}


def source_pages(rel):
    """-> list of normalised page texts, or None if the source has no text."""
    if rel in _cache:
        return _cache[rel]
    path = ROOT / rel
    pages = None
    try:
        if path.suffix.lower() == '.pdf':
            doc = fitz.open(path)
            pages = [norm(p.get_text()) for p in doc]
            if sum(len(p) for p in pages) < 50:
                pages = None                              # scan with no text layer
        elif path.suffix.lower() in ('.txt', '.md'):
            pages = [norm(path.read_text(encoding='utf-8', errors='replace'))]
    except Exception:
        pages = None
    _cache[rel] = pages
    return pages


def find_in(rel, frags, cited=0):
    """-> 1-based page the quote is on, or None.

    The cited page is tried first: a phrase that recurs throughout a report
    would otherwise be reported as a page mismatch just because some earlier
    page also contains it.
    """
    pages = source_pages(rel)
    if not pages:
        return None
    if cited and 1 <= cited <= len(pages) and contains_in_order(pages[cited - 1], frags):
        return cited
    for i, page in enumerate(pages):
        if contains_in_order(page, frags):
            return i + 1
    joined = ' '.join(pages)                              # spans a page break
    return 0 if contains_in_order(joined, frags) else None


raw = POST.read_text(encoding='utf-8')
all_assets = sorted(set(ANY_ASSET.findall(raw)))

ok_cited = []        # verified on the cited page
ok_otherpage = []    # verified, but the #page anchor points elsewhere
ok_elsewhere = []    # no adjacent link; found in some other cited source
missing = []         # not found in the source it cites
unmatched = []       # no adjacent link and found nowhere
notext = {}          # sources with no extractable text
skipped = 0

for m in QUOTE.finditer(raw):
    quote = m.group(1)
    # An unbalanced " anywhere in the document shifts every pair after it, so
    # a "quote" that opens on markdown punctuation is a mis-paired span, not
    # something to report against a source.
    if '](' in quote or len(quote) > 600 or quote.lstrip()[:1] in '*])>|':
        skipped += 1
        continue
    frags = fragments(norm(quote))
    if not frags:
        skipped += 1
        continue

    link = LINK.search(raw[m.end(): m.end() + 260])
    short = quote[:80].replace('\n', ' ')

    if link:
        rel, cited = link.group(1), int(link.group(2) or 0)
        if source_pages(rel) is None:
            notext.setdefault(rel, 0)
            notext[rel] += 1
            continue
        page = find_in(rel, frags, cited)
        if page is None:
            # The nearest link is only a guess at which source a quote belongs
            # to — a law quoted mid-paragraph picks up the next link in the
            # text. Before calling it missing, look everywhere else.
            hit = next((a for a in all_assets
                        if a != rel and find_in(a, frags) is not None), None)
            if hit:
                ok_elsewhere.append((short, hit))
            else:
                missing.append((short, rel, cited))
        elif cited and page and page != cited:
            ok_otherpage.append((short, rel, cited, page))
        else:
            ok_cited.append(short)
    else:
        hit = next((a for a in all_assets if find_in(a, frags) is not None), None)
        if hit:
            ok_elsewhere.append((short, hit))
        else:
            unmatched.append(short)

total = (len(ok_cited) + len(ok_otherpage) + len(ok_elsewhere)
         + len(missing) + len(unmatched) + sum(notext.values()))

print(f'{total} quotes examined ({skipped} spans skipped as not cleanly quoted)')
print(f'  verified against the source they cite : {len(ok_cited)}')
print(f'  verified, but on a different page     : {len(ok_otherpage)}')
print(f'  verified against another cited source : {len(ok_elsewhere)}')
print(f'  NOT FOUND in the source they cite     : {len(missing)}')
print(f'  no citation and found nowhere         : {len(unmatched)}')
print(f'  in sources with no text layer         : {sum(notext.values())}')

if notext:
    print('\nCannot verify — no extractable text (scanned?):')
    for rel, n in sorted(notext.items()):
        print(f'  {n:3} quote(s) in {rel}')

if ok_otherpage:
    print('\nPage anchor points at the wrong page:')
    for short, rel, cited, page in ok_otherpage:
        print(f'  cited #page={cited}, found on page {page} — {rel}')
        print(f'      "{short}"')

if missing:
    print('\nNOT FOUND in the cited source:')
    for short, rel, cited in missing:
        where = f'#page={cited}' if cited else '(no page given)'
        print(f'  {rel} {where}')
        print(f'      "{short}"')

if unmatched:
    print(f'\nNo adjacent citation and no match in any cited source '
          f'({len(unmatched)}) — these need checking by hand:')
    for short in unmatched:
        print(f'      "{short}"')

sys.exit(1 if (missing or unmatched) else 0)
