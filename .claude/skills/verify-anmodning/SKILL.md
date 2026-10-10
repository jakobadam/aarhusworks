---
name: verify-anmodning
description: Verify the Ankestyrelsen filing (_posts/2026-08-26-anmodning-om-tilsynssag.md and its tillæg, _posts/2026-08-26-anmodning-om-tilsynssag-tillaeg.md) after editing either — checks that quoted text actually appears in the PDF it cites, that the title renders once, that the published URL has not moved, that every bilag link points at a committed file, that cross-references resolve within and between the two posts, and what TODOs remain before it can be filed. Use after any edit to either post, or when asked whether it still builds and renders correctly.
---

# Verify the Ankestyrelsen filing

`_posts/2026-08-26-anmodning-om-tilsynssag.md` is a ~900-line
administrative complaint citing ~90 distinct bilag, with ~235 internal
cross-reference links pointing at some two dozen distinct targets. Its
post-by-post review of the municipality's accounts — the *tillæg* — lives in
its own post, `_posts/2026-08-26-anmodning-om-tilsynssag-tillaeg.md`, and
some 30 links run between the two as absolute aarhusworks.com URLs with an
`#anchor`. The script checks both posts in every tier. The script
counts distinct paths and targets, so its totals are smaller than the number
of links in the text. Judging the argument is a human job; what tooling catches
here is links and headings silently breaking, and quotations drifting from the
sources they rest on.

## Run it

```powershell
pwsh bin/check-anmodning.ps1           # static — seconds
pwsh bin/check-anmodning.ps1 -Quotes   # + every quote against the PDF it cites
pwsh bin/check-anmodning.ps1 -Build    # + Jekyll build and rendered-output checks
```

The three tiers are independent. `-Quotes` needs Python with PyMuPDF
(`pip install pymupdf`) and the PDFs in `assets/`; `-Build` needs docker.

Use `-Build` before saying the document is correct. The static tier cannot see
what Jekyll actually produced, and the failure this repo has already hit —
a duplicated title — is only visible in the rendered HTML.

First `-Build` run takes ~3 minutes while the `aarhusworks-bundle` docker
volume fills with gems; later runs are the ~40s build alone.

## What it checks, and why each one is there

**Exactly one title renders.** The post used to show two stacked titles: it
had no front matter, so Jekyll titleized the *filename* into the page `<h1>`
("Anmodning Om Tilsynssag Ankestyrelsen"), and the document's own
`# Anmodning om tilsynssag` rendered right below it.

Either source of the title is fine; both posts now carry `title:` in front
matter ("Anmodning om tilsynssag", "Støjpuljen, post for post"). Without
front matter Jekyll titleizes the filename, and the script reports which title
that yields rather than demanding front matter.
What is always wrong is an h1 in the body, because it stacks a second title
under whichever one the layout already renders; the script rejects that either
way, and `-Build` asserts the rendered page has exactly one `<h1>` carrying
the expected text.

**The published URLs.** Jekyll's default permalink is
`/:categories/:year/:month/:day/:title.html`. Adding `categories: vejstøj` to
match the sibling posts would move this post to `/vejstøj/2026/08/26/...` and
404 the address people already have — and every link the other document
holds to it. That is why these two posts — alone among the Giber Ringvej posts
— carry no category. If a category is ever genuinely
wanted, add `redirect_from` for the old path; the script accepts that and
rejects a bare category.

**Quotes against their sources** (`-Quotes`). Every `"..."` in the document is
matched against the text of the PDF it cites. Matching is exact containment
after normalisation — never fuzzy. A 95%-similar quote is a defect in a filing
like this, and a similarity threshold would hide precisely that. Normalisation
absorbs what a PDF text layer does to words rather than what an author does to
a quotation: whitespace, dashes and quote glyphs, hyphens (dropped on both
sides, since a line break can fall on a real compound hyphen such as
*VVM-bekendtgørelsen*), and footnote markers glued to the preceding word. Ellipses and editorial brackets
(`[er]`, `[k]ommunen`) are treated as wildcards, but the fragments around them
must still appear *in order*, so an insertion cannot smuggle in a change of
meaning.

A quote is looked for, in turn, in the source its link points to (the text
layer and the comments in the PDF — the kommune answers fact sheets in
comments), in the other cited files, and in the external sources the section
and then the post link to: laws on danskelove.dk, ombudsman statements and
guidance on retsinformation.dk (read through the ELI address plus `/xml`).
These are fetched once into `bin/kildecache/` and committed, so the check runs
offline. A sentence that continues on the next page is found across the
running header and footer between its halves. Quotation marks are paired in
order within a line, and the front matter, `[TODO: ...]` instructions and
document titles in the bilag list are not treated as quotations.

Read the output as these separate things:

- *verified* — against the cited source, another cited file, a linked external
  source; or the quote names a section of the filing itself ("uddybes
  nedenfor under ..."), or it is a bilag's title in the bilag list.
- *found, but not on the page the link gives* — the `#page=` anchor is wrong,
  or the quote picked up a neighbouring link. Not reported when the link's
  text gives a range that covers the page ("s. 6–7"), when the same paragraph
  also cites that page, or when the quote is the document's title on page 1.
- *cannot be checked automatically* — the source cannot be read (a scanned
  page, a paywall, an ombudsman statement that retsinformation.dk only has as
  an abstract), or no source is given. With the reason. Not a pass and not a
  failure: confirm by hand, and record it in `bin/kilder-manuelt.json`
  (`citat`, `kilde`, `side`, `kontrol`), after which it counts as verified.
- *NOT in the source they cite* — the only failure. The source can be read and
  the quote is not in it, or the quote has no source but is nearly the words of
  one (a near match is a misquote, not an unreadable source). The output shows
  what the source actually says.

**What it cannot tell you.** Scanned PDFs with no text layer are named
explicitly rather than counted as passing — nothing can verify those
mechanically. It also cannot judge whether a quote is fair in context, only
whether the words are present. Do not read a clean run as "the quotations are
sound"; read it as "no quotation is verifiably wrong, and here is what is left
for you to check."

**Bilag links.** The test is whether the asset is *committed*, not whether it
exists locally. A PDF sitting untracked in `assets/` resolves fine on this
machine and 404s for every reader. Anything reported as "exists locally but is
not committed" means commit the PDF, not fix the link.

**Cross-references.** Checked against the `id="..."` attributes kramdown
actually emitted, not guessed from the markdown headings — renumbering a
section silently breaks every `](#...)` pointing into it. Links between the
two posts (`https://aarhusworks.com/2026/08/26/<slug>.html#id`) are checked
against the other page's ids; the bilag check covers only `/assets/` and
would otherwise let them rot silently.

**The filing's own PDFs are not sources.** Both posts link to their own PDFs
and to each other's, and those PDFs contain every word of the filing. The quote
check excludes them, as a pool and as the citation next to a quote — otherwise
every quote "verifies" against GRG's own text. A quote in the tillæg must cite
its source in the tillæg itself; a source cited only in the anmodning is not in
the tillæg's pool.

**KLADDE in both.** The tillæg is filed with the anmodning and has no TODOs of
its own. It must carry the KLADDE banner exactly as long as the anmodning
does, and its PDF takes the draft stamp and header date from the anmodning
(`bin/anmodning2pdf.mjs` renders both on every run).

**TODOs.** Listed, never treated as failures. This is a deliberate KLADDE and
the markers are the remaining blockers before filing (missing addresses, the
send date). Treat the list as the pre-filing checklist.

## Interpreting a failure

Errors are real defects in the published document. Notes are status. If the
build tier reports a post rendering somewhere other than
`_site/2026/08/26/anmodning-om-tilsynssag.html` or
`_site/2026/08/26/anmodning-om-tilsynssag-tillaeg.html`, stop and fix
the front matter before committing — that is a broken public URL, not a
cosmetic issue.
