"""Checks that quoted text in a post actually appears in the source it cites.

Called by bin/check-anmodning.ps1 -Quotes. Requires PyMuPDF (pip install pymupdf).

Matching is exact containment after normalisation — never fuzzy. A quote that is
95% right is a defect in a document like this, and a similarity threshold would
hide exactly that.

Three things are deliberately treated as wildcards rather than literal text,
because they mark places the author signalled a change from the original:
an ellipsis, and editorial brackets like [er] or [k]ommunen. The fragments
around them must still appear, in order.

The normalisation and the quote-to-link association live in bin/quotelib.py,
shared with bin/evidence-cards.py.
"""

import io
import pathlib
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from quotelib import ANY_ASSET, SELF, Sources, cited_quotes
except ImportError:
    print('ERROR: PyMuPDF not installed — run: pip install pymupdf')
    sys.exit(2)

ROOT = pathlib.Path(sys.argv[1]).resolve()
POST = pathlib.Path(sys.argv[2]).resolve()

sources = Sources(ROOT)
source_pages, find_in = sources.pages, sources.find_in

raw = POST.read_text(encoding='utf-8')

all_assets = sorted(a for a in set(ANY_ASSET.findall(raw)) if a not in SELF)

ok_cited = []        # verified on the cited page
ok_otherpage = []    # verified, but the #page anchor points elsewhere
ok_elsewhere = []    # no adjacent link; found in some other cited source
missing = []         # not found in the source it cites
unmatched = []       # no adjacent link and found nowhere
notext = {}          # sources with no extractable text
skipped = 0

for item in cited_quotes(raw):
    if item is None:
        skipped += 1
        continue
    m, quote, frags, link = item
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
