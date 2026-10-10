"""Checks that quoted text in a post actually appears in the source it cites.

Called by bin/check-anmodning.ps1 -Quotes. Requires PyMuPDF (pip install pymupdf).

Matching is exact containment after normalisation — never fuzzy. A quote that is
95% right is a defect in a document like this, and a similarity threshold would
hide exactly that.

Three things are deliberately treated as wildcards rather than literal text,
because they mark places the author signalled a change from the original:
an ellipsis, and editorial brackets like [er] or [k]ommunen. The fragments
around them must still appear, in order.

A quote is checked against, in turn: the source its link points to (text,
and comments in the PDF), the other cited files, and the external sources
the section links to (laws, ombudsman statements; fetched once into
bin/kildecache). Only a source that can be read and does not hold the quote
is an error. A source that cannot be read — a scan, a paywall, an abstract —
or a quote with no source at all is reported as not checkable, with the
reason, and can be confirmed by hand in bin/kilder-manuelt.json.

The rules live in bin/quotelib.py, shared with bin/evidence-cards.py.
"""

import io
import pathlib
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from quotelib import (ANY_ASSET, SELF, Sources, cited_quotes, labels,
                          linked_posts, manual, verify)
except ImportError:
    print('ERROR: PyMuPDF not installed — run: pip install pymupdf')
    sys.exit(2)

ROOT = pathlib.Path(sys.argv[1]).resolve()
POST = pathlib.Path(sys.argv[2]).resolve()

sources = Sources(ROOT)
raw = POST.read_text(encoding='utf-8')
assets = sorted(a for a in set(ANY_ASSET.findall(raw)) if a not in SELF)
own = labels(raw, *linked_posts(raw, POST.parent))
by_hand = manual(ROOT)

KINDS = {
    'cited': 'verified against the source they cite',
    'elsewhere': 'verified against another cited file',
    'external': 'verified against a linked external source',
    'internal': 'name a section of the filing itself',
    'title': "are a bilag's title in the bilag list",
    'manual': 'checked by hand (bin/kilder-manuelt.json)',
}
counts = dict.fromkeys(KINDS, 0)
warnings, unverifiable, errors = [], [], []
skipped = 0

for item in cited_quotes(raw):
    if item is None:
        skipped += 1
        continue
    m, quote, frags, link = item
    short = quote[:80].replace('\n', ' ')
    line = raw.count('\n', 0, m.start()) + 1
    state, kind, detail = verify(raw, item, sources, own, by_hand, assets)
    if state == 'ok':
        counts[kind] += 1
    elif state == 'warn':
        warnings.append((line, short, detail))
    elif state == 'unverifiable':
        unverifiable.append((line, short, detail))
    else:
        errors.append((line, short, kind, detail))

total = sum(counts.values()) + len(warnings) + len(unverifiable) + len(errors)
print(f'{total} quotes examined ({skipped} quoted spans are titles, instructions '
      f'or mis-paired, not quotations)')
for kind, label in KINDS.items():
    print(f'  {label:<44}: {counts[kind]}')
print(f'  {"found, but not on the page the link gives":<44}: {len(warnings)}')
print(f'  {"cannot be checked automatically":<44}: {len(unverifiable)}')
print(f'  {"NOT in the source they cite":<44}: {len(errors)}')

if warnings:
    print('\nPage anchor points at another page than the quote:')
    for line, short, (rel, cited, page) in warnings:
        print(f'  L{line}: cited #page={cited}, found on page {page} — {rel}')
        print(f'      "{short}"')

if unverifiable:
    print('\nCannot be checked automatically — confirm by hand, and record it in '
          'bin/kilder-manuelt.json:')
    for line, short, why in unverifiable:
        print(f'  L{line}: {why}')
        print(f'      "{short}"')

if errors:
    print('\nNOT FOUND — the source can be read, and the quote is not in it:')
    for line, short, kind, detail in errors:
        near = None
        if kind == 'missing':
            rel, cited, near = detail
            print(f'  L{line}: {rel}' + (f' #page={cited}' if cited else ''))
        elif kind == 'differs':
            near = detail
            print(f'  L{line}: no source given, but close to a source that can be read')
        else:
            print(f'  L{line}: none of the sources the section links to: '
                  + ', '.join(detail))
        print(f'      quote : "{short}"')
        if near:
            where, page, words = near
            print(f'      source: "{words[:160]}" — {where}' + (f', p. {page}' if page else ''))

sys.exit(1 if errors else 0)
