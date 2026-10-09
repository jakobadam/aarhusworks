# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`aarhusworks` is Jakob Aarøe Dam's personal Jekyll blog, published at https://aarhusworks.com, hosted via GitHub Pages (this working copy is on the `gh-pages` branch). Posts live in `_posts/` as Markdown with Jekyll front matter (`title`, `author`, `categories`, etc.), using the `minima` theme.

A large, recurring share of the content is one long-running advocacy campaign: **"Giber Ringvej"** — a road-noise dispute between local residents (Giber Ringvej Gruppen, GRG, of which Jakob is a spokesperson) and Aarhus Kommune / Teknik og Miljø (MTM) over unmet VVM (environmental-impact) permit conditions (screening vegetation, noise-reducing pavement, and a ~20M DKK noise-mitigation pool). Posts, fact sheets ("faktaark"), hearing responses ("høringssvar"), and supporting PDFs about this campaign accumulate under `assets/giber-ringvej/` and related `assets/*stoej*`/`assets/mtm-modsvar*` directories. When editing anything in this area, match the existing register: precise, source-cited, Danish administrative/legal language — see `.github/agents/kommunal-modstander.md` for the adversarial-review persona used to pressure-test complaint drafts, and `assets/giber-ringvej/klage/README.txt` for how the complaint working-folder (`klage/`) is organized (source PDFs stay in `assets/`, referenced by URL, never copied into `klage/`).

## Commands

**Serve the site locally (Docker, recommended — no local Ruby needed):**
```powershell
./serve-it.sh
# or directly:
docker run --rm -v "${PWD}:/site" -w /site -p 4000:4000 ruby:3.1 bash -c "gem install bundler -v 2.5.10 --quiet && bundle install --quiet && bundle exec jekyll serve --host 0.0.0.0 --force_polling"
```
Open http://localhost:4000 — the site live-reloads on file changes.

**Serve the site locally (native Ruby):**
```shell
gem install jekyll bundler
bundle install
bundle exec jekyll serve
```

There are no automated tests, lint scripts beyond the pre-commit hook below, or CI build step in this repo — "does it build with Jekyll and render correctly" is the practical check.

The one exception is the Ankestyrelsen filing (`_posts/2026-08-26-anmodning-om-tilsynssag.md` and its tillæg, `_posts/2026-08-26-anmodning-om-tilsynssag-tillaeg.md`), which has `bin/check-anmodning.ps1` (`-Build` adds Jekyll build and rendered-output checks, `-Quotes` checks quotations against their PDFs) — see the `verify-anmodning` skill for what it checks and why. Note the trap it guards: Jekyll's default permalink includes `:categories`, so adding a category to an existing post moves its URL and 404s the published address. Both posts get a PDF in `assets/giber-ringvej/klage/` from `bin/anmodning2pdf.mjs`, which the pre-commit hook runs when either post is staged; the tillæg takes its KLADDE status and date from the anmodning. The same hook runs `bin/evidence-cards.py --stage`, which renders a highlighted crop of the source PDF page for every quote `check-quotes.py` verifies (`assets/evidence/<slug>/`, manifest in `_data/evidence/<slug>.json`, shown by `assets/js/evidence.js`); only new or changed quotes are drawn, and the post's Markdown is never touched. The hook prints, per post, how many quotations got a card and why the rest did not; the same per-quotation status, with a concrete list of what to check, is shown on the page while the anmodning still has `[TODO:` markers (the KLADDE test), and disappears from the published page once it is filed.

## Mermaid diagrams in posts

`package.json`/`husky`/`lint-staged` wire a pre-commit hook (`.husky/pre-commit` → `npm run lint-staged`) that runs `bin/mermaid2svg.sh` on every staged `*.md` file. That script finds fenced code blocks tagged `mermaid` and appends a rendered SVG (via `mmdc`, the `@mermaid-js/mermaid-cli` package) directly after each block, wrapped in a `mermaid-svg` div closed by an end-marker comment. This means:
- The script matches the opening fence anywhere in a file, even inside running text, so never write the three backticks followed by the word mermaid literally in prose (this file included) — it rewrites the sentence. Describe it in words, as here.
- Rendered SVGs in committed Markdown are generated artifacts, not hand-written — don't hand-edit them; edit the mermaid source block and let the hook regenerate the SVG on commit.
- `npm install` is required once to get `mmdc` available for the hook to work.

## Site structure notes

- `_config.yml` — Jekyll site settings (title, url, theme `minima`, plugins `jekyll-feed`/`jekyll-redirect-from`). Not reloaded by `jekyll serve --watch`; restart the server after editing it.
- `_layouts/my.css` — custom stylesheet overrides on top of the `minima` theme.
- `assets/` — post images plus a large body of source PDFs/documents backing the Giber Ringvej and related traffic-noise posts (Aarhus Kommune noise action plans, VVM documents, hearing responses, court rulings, etc.). Posts link to these by URL (`https://aarhusworks.com/assets/...`) rather than embedding them.
- Front-page thumbnails and the author portrait are small WebP copies in `assets/thumbs/` and `assets/images/profil-128.webp`, mapped in `_data/thumbs.yml`. They are generated by `node bin/thumbs.cjs` (after a Jekyll build) and committed. Re-run it when a post adds or changes its first image; without it the feed falls back to the full-size image.
- `_site/` and `node_modules/` are build/dependency output — don't hand-edit.
