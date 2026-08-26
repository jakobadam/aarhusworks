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

## Mermaid diagrams in posts

`package.json`/`husky`/`lint-staged` wire a pre-commit hook (`.husky/pre-commit` → `npm run lint-staged`) that runs `bin/mermaid2svg.sh` on every staged `*.md` file. That script finds ```` ```mermaid ```` fenced blocks and appends a rendered SVG (via `mmdc`, the `@mermaid-js/mermaid-cli` package) directly after each block, wrapped in `<div class="mermaid-svg">...</div><!--mermaid-svg-end-->`. This means:
- Rendered SVGs in committed Markdown are generated artifacts, not hand-written — don't hand-edit them; edit the mermaid source block and let the hook regenerate the SVG on commit.
- `npm install` is required once to get `mmdc` available for the hook to work.

## Site structure notes

- `_config.yml` — Jekyll site settings (title, url, theme `minima`, plugins `jekyll-feed`/`jekyll-redirect-from`). Not reloaded by `jekyll serve --watch`; restart the server after editing it.
- `_layouts/my.css` — custom stylesheet overrides on top of the `minima` theme.
- `assets/` — post images plus a large body of source PDFs/documents backing the Giber Ringvej and related traffic-noise posts (Aarhus Kommune noise action plans, VVM documents, hearing responses, court rulings, etc.). Posts link to these by URL (`https://aarhusworks.com/assets/...`) rather than embedding them.
- `_site/` and `node_modules/` are build/dependency output — don't hand-edit.
