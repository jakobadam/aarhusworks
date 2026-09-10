---
name: verify-anmodning
description: Verify the Ankestyrelsen filing (_posts/2026-08-26-anmodning-om-tilsynssag.md) after editing it — checks front matter and title rendering, that the published URL has not moved, that every bilag link points at a committed file, that internal cross-references resolve, and what TODOs remain before it can be filed. Use after any edit to that post, or when asked whether it still builds and renders correctly.
---

# Verify the Ankestyrelsen filing

`_posts/2026-08-26-anmodning-om-tilsynssag.md` is a ~1000-line
administrative complaint citing ~90 distinct bilag, with ~235 internal
cross-reference links pointing at some two dozen distinct targets. The script
counts distinct paths and targets, so its totals are smaller than the number
of links in the text. Prose review is a human job; what tooling catches here
is links and headings silently breaking.

## Run it

```powershell
pwsh bin/check-anmodning.ps1           # static — seconds
pwsh bin/check-anmodning.ps1 -Build    # + Jekyll build and rendered-output checks
```

Use `-Build` before saying the document is correct. The static tier cannot see
what Jekyll actually produced, and the failure this repo has already hit —
a duplicated title — is only visible in the rendered HTML.

First `-Build` run takes ~3 minutes while the `aarhusworks-bundle` docker
volume fills with gems; later runs are the ~40s build alone.

## What it checks, and why each one is there

**Front matter and the title.** The post once had no front matter at all.
Jekyll then titleizes the *filename* into the page `<h1>`
("Anmodning Om Tilsynssag Ankestyrelsen") while the document's own
`# Anmodning om tilsynssag` renders right below it — two stacked titles.
The fix is a `title:` in front matter and no h1 in the body; the script
enforces both, and `-Build` asserts the rendered page has exactly one `<h1>`
matching the front matter title.

**The published URL.** Jekyll's default permalink is
`/:categories/:year/:month/:day/:title.html`. Adding `categories: vejstøj` to
match the sibling posts would move this post to `/vejstøj/2026/08/26/...` and
404 the address people already have. That is why this post — alone among the
Giber Ringvej posts — carries no category. If a category is ever genuinely
wanted, add `redirect_from` for the old path; the script accepts that and
rejects a bare category.

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
