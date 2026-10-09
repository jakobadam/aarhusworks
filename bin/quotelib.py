"""Shared quote matching for bin/check-quotes.py and bin/evidence-cards.py.

Finding a quotation in a post, deciding which source link it belongs to, and
normalising text so a quote compares equal to a PDF text layer are the same
problem for the checker (is the quote really there?) and for the evidence
cards (where on the page is it?). Keeping one copy means a card can never be
drawn for a quote the checker would have matched differently.

Requires PyMuPDF (pip install pymupdf).
"""

import re
import unicodedata
from urllib.parse import unquote

import fitz

QUOTE = re.compile(r'"([^"\r\n]{15,}?)"')
LINK = re.compile(r'\]\(https://aarhusworks\.com/(assets/[^)#\s]+)(?:#page=(\d+))?\)')
ANY_ASSET = re.compile(r'https://aarhusworks\.com/(assets/[^)#\s]+)')
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
        joined = ' '.join(pages)                          # spans a page break
        return 0 if contains_in_order(joined, frags) else None


def cited_quotes(raw):
    """Yield every quotation in a post with the source link it belongs to.

    Yields (match, quote, frags, link) where link is a LINK match or None, or
    None alone for a span that looks quoted but is not a quotation.
    """
    for m in QUOTE.finditer(raw):
        quote = m.group(1)
        # An unbalanced " anywhere in the document shifts every pair after it, so
        # a "quote" that opens on markdown punctuation is a mis-paired span, not
        # something to report against a source.
        # An HTML attribute value is not a quotation: <a id="tillaeg-prissaetning">
        # otherwise reads as one and gets checked against the nearest source.
        if m.start() > 0 and raw[m.start() - 1] == '=':
            yield None
            continue
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
        line_start = raw.rfind('\n', 0, m.start()) + 1
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
