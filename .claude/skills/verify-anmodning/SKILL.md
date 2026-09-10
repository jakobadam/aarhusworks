---
name: verify-anmodning
description: Verify the Ankestyrelsen filing (_posts/2026-08-26-anmodning-om-tilsynssag.md) after editing it — checks that quoted text actually appears in the PDF it cites, that the title renders once, that the published URL has not moved, that every bilag link points at a committed file, that internal cross-references resolve, and what TODOs remain before it can be filed. Use after any edit to that post, or when asked whether it still builds and renders correctly.
---

# Verify the Ankestyrelsen filing

`_posts/2026-08-26-anmodning-om-tilsynssag.md` is a ~1000-line
administrative complaint citing ~90 distinct bilag, with ~235 internal
cross-reference links pointing at some two dozen distinct targets. The script
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

Either source of the title is fine. The post currently has no front matter and
takes its title from the filename — `2026-08-26-anmodning-om-tilsynssag.md`
renders as "Anmodning Om Tilsynssag" — and the script reports which title that
yields rather than demanding front matter. Adding `title:` to front matter is
equally valid and gives control over the casing ("Anmodning om tilsynssag").
What is always wrong is an h1 in the body, because it stacks a second title
under whichever one the layout already renders; the script rejects that either
way, and `-Build` asserts the rendered page has exactly one `<h1>` carrying
the expected text.

**The published URL.** Jekyll's default permalink is
`/:categories/:year/:month/:day/:title.html`. Adding `categories: vejstøj` to
match the sibling posts would move this post to `/vejstøj/2026/08/26/...` and
404 the address people already have. That is why this post — alone among the
Giber Ringvej posts — carries no category. If a category is ever genuinely
wanted, add `redirect_from` for the old path; the script accepts that and
rejects a bare category.

**Quotes against their sources** (`-Quotes`). Every `"..."` in the document is
matched against the text of the PDF it cites. Matching is exact containment
after normalising whitespace, hyphenated line breaks, dashes and quote glyphs —
never fuzzy. A 95%-similar quote is a defect in a filing like this, and a
similarity threshold would hide precisely that. Ellipses and editorial brackets
(`[er]`, `[k]ommunen`) are treated as wildcards, but the fragments around them
must still appear *in order*, so an insertion cannot smuggle in a change of
meaning.

Read the output as four separate things:

- *verified against the source they cite* — matched on the page the link names.
- *verified, but on a different page* — the text is in that PDF, elsewhere.
  The `#page=` anchor is wrong, or the quote picked up a neighbouring link.
- *verified against another cited source* — no citation next to the quote, so
  it was matched against every source the document cites. Usually a phrase
  quoted again after being cited properly earlier. Weaker evidence: it confirms
  the words exist somewhere in the material, not that this passage cites them.
- *NOT FOUND* and *no citation and found nowhere* — the honest residue. These
  need a human. Expect some to be document *titles* in quotation marks rather
  than quotations, which this cannot distinguish.

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
section silently breaks every `](#...)` pointing into it.

**TODOs.** Listed, never treated as failures. This is a deliberate KLADDE and
the markers are the remaining blockers before filing (missing addresses, the
send date). Treat the list as the pre-filing checklist.

## Interpreting a failure

Errors are real defects in the published document. Notes are status. If the
build tier reports the post rendering somewhere other than
`_site/2026/08/26/anmodning-om-tilsynssag.html`, stop and fix
the front matter before committing — that is a broken public URL, not a
cosmetic issue.
