#!/usr/bin/env node
// Render the Ankestyrelsen filing and its tillæg to paginated A4 PDFs.
//
//   node bin/anmodning2pdf.mjs            # write both PDFs
//   node bin/anmodning2pdf.mjs --check    # exit 1 if a committed PDF is stale
//   node bin/anmodning2pdf.mjs --stage    # write them and git add the results (hook)
//
// Every mode handles both documents: the tillæg is filed with the anmodning
// and takes its draft status and date from it (see DOCS below).
//
// The PDF is the copy that gets filed, so a draft must never look clean: while
// [TODO: markers remain in the anmodning, every page carries KLADDE in the
// running header and a watermark. The filenames stay the same either way —
// the filing links to them, so the URLs must not move when the draft goes
// final. Layout follows the afklaringsnotater — A4, title and date in a
// running header, "N af M" in the footer.
//
// marked and puppeteer are declared in package.json; run `npm install` once.

import { readFileSync, writeFileSync, existsSync, rmSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import puppeteer from 'puppeteer';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const KLAGE = 'assets/giber-ringvej/klage';

// The anmodning comes first: it decides draft status and header date for both.
// ANMODNING_PDF_OUT renders the anmodning somewhere else — useful when a PDF
// viewer holds a lock on the real file, which Windows enforces. It does not
// move the tillæg.
const DOCS = [
  {
    source: resolve(repo, '_posts/2026-08-26-anmodning-om-tilsynssag.md'),
    out: process.env.ANMODNING_PDF_OUT
      ? resolve(process.env.ANMODNING_PDF_OUT)
      : resolve(repo, KLAGE, 'anmodning-om-tilsynssag.pdf'),
    title: 'Anmodning om tilsynssag — Giber Ringvej',
  },
  {
    source: resolve(repo, '_posts/2026-08-26-anmodning-om-tilsynssag-tillaeg.md'),
    out: resolve(repo, KLAGE, 'anmodning-om-tilsynssag-tillaeg.pdf'),
    title: 'Tillæg til anmodning om tilsynssag — Giber Ringvej',
  },
];

const check = process.argv.includes('--check');
const stage = process.argv.includes('--stage');

// ---------------------------------------------------------------- source

// Jekyll front matter (title/description only — no categories, see
// verify-anmodning) is for the web page; marked would print it as a rule and
// a line of text.
const read = (path) => readFileSync(path, 'utf8').replace(/^﻿?---\r?\n[\s\S]*?\r?\n---\r?\n/, '');

// Passages the web page wants but the PDF must not carry — the link to the
// document's own PDF, above all. The markers are HTML comments, so they render
// as nothing on aarhusworks.com and need no counterpart in the Jekyll build.
const skip = (source) => source.replace(/[^\S\n]*<!--\s*pdf:skip\s*-->[\s\S]*?<!--\s*\/pdf:skip\s*-->[^\S\n]*\n?/g, '');

// The tillæg has no TODOs of its own; judged alone it would render as a clean,
// filed-looking PDF while the anmodning is still a draft.
const anmodning = read(DOCS[0].source);
const isDraft = anmodning.includes('[TODO:');

// The header date is the filing's own "**Dato:**" line once it is filled in.
const dateLine = skip(anmodning).match(/^\*\*Dato:\*\*\s*(.+)$/m)?.[1]?.trim() ?? '';
const headerDate = /TODO/.test(dateLine) || !dateLine
  ? `Udkast ${new Date().toISOString().slice(0, 10)}`
  : dateLine.replace(/[*_]/g, '').trim();

// Images are written as absolute aarhusworks.com URLs so the web page works.
// Chrome would fetch those over the network, which makes the PDF depend on
// being online and on the file already being live — render before pushing and
// the page silently gets a blank gap instead. Inline the repo's own copy.
const SITE = 'https://aarhusworks.com/';
const MIME = { png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', gif: 'image/gif', svg: 'image/svg+xml' };

function bodyOf(doc) {
  const source = read(doc.source);
  const md = skip(source);
  if (md === source) console.warn(`Bemaerk: ingen <!-- pdf:skip -->-afsnit fundet i ${rel(doc.source)}.`);

  // Every cross-reference inside a document targets an explicit <a id="...">
  // anchor, so marked needs no heading-id extension for the section links to
  // resolve inside the PDF. Links between the two documents and bilag URLs
  // are absolute and stay clickable.
  let body = marked.parse(md, { gfm: true, breaks: false });
  doc.inlined = 0;
  body = body.replace(/(<img\b[^>]*?\bsrc=")([^"]+)(")/g, (whole, pre, src, post) => {
    if (!src.startsWith(SITE)) return whole;
    const local = resolve(repo, decodeURIComponent(src.slice(SITE.length)));
    const mime = MIME[local.split('.').pop().toLowerCase()];
    if (!existsSync(local) || !mime) {
      console.error(`FEJL: billedet findes ikke i repoet: ${src}`);
      process.exit(1);
    }
    doc.inlined++;
    return `${pre}data:${mime};base64,${readFileSync(local).toString('base64')}${post}`;
  });
  return body;
}

// Headings, header and footer want Helvetica Neue, which is a licensed
// Monotype face: present on macOS, absent on Windows, and not installable
// here. Inter is embedded straight after it so the headings look the same for
// the recipient no matter which machine rendered the file — it is the closest
// free neo-grotesque and its OFL licence permits embedding. Swap the first two
// entries if you would rather have deterministic output than Helvetica Neue
// winning wherever it happens to be installed.
const SANS = '"Helvetica Neue", Inter, Helvetica, "Nimbus Sans", Arial, sans-serif';

// Weights actually used below: 400 (header/footer), 700 (headings, th,
// watermark) and 400 italic (emphasis inside headings and table cells).
const FACES = [
  ['inter-latin-400-normal.woff2', 400, 'normal'],
  ['inter-latin-400-italic.woff2', 400, 'italic'],
  ['inter-latin-700-normal.woff2', 700, 'normal'],
  ['inter-latin-700-italic.woff2', 700, 'italic'],
];

function face([file, weight, style]) {
  const path = resolve(repo, 'node_modules/@fontsource/inter/files', file);
  if (!existsSync(path)) {
    console.error(`FEJL: ${file} mangler — koer: npm install`);
    process.exit(1);
  }
  const b64 = readFileSync(path).toString('base64');
  return `@font-face{font-family:Inter;font-style:${style};font-weight:${weight};` +
    `font-display:block;src:url(data:font/woff2;base64,${b64}) format("woff2");}`;
}

const fontFaces = FACES.map(face).join('\n');

// The running header and footer stay on the installed fallback. Chrome renders
// them as their own documents, which inherit none of the page CSS, and putting
// a <style> block with the embedded face into the templates makes Chrome drop
// them altogether — verified: no header, no footer, no page numbers. So the
// 7.5-8pt running text is Arial (or whatever the stack resolves to) while the
// headings are Inter. Do not "fix" this by re-adding <style> to the templates.
// Chrome renders the header and footer as separate documents that do not
// inherit the page CSS, so the stack has to be repeated inline — with single
// quotes, since it sits inside a double-quoted style attribute.
const SANS_ATTR = SANS.replaceAll('"', "'");

const css = `
  ${fontFaces}
  :root { --sans: ${SANS}; }
  @page { size: A4; margin: 24mm 18mm 20mm 18mm; }
  html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  body {
    font: 10.5pt/1.5 Georgia, "Times New Roman", serif;
    color: #111; margin: 0; hyphens: auto;
  }
  h1, h2, h3, h4 {
    font-family: var(--sans);
    line-height: 1.25; break-after: avoid; margin: 1.4em 0 .5em;
  }
  h2 { font-size: 15pt; border-bottom: .8pt solid #bbb; padding-bottom: .15em; }
  h3 { font-size: 12.5pt; }
  h4 { font-size: 11pt; color: #333; }
  p, li { orphans: 3; widows: 3; }
  ul, ol { padding-left: 1.4em; }
  a { color: #1a3f6f; text-decoration: none; }
  strong { font-weight: 700; }
  blockquote {
    margin: .9em 0 .9em 1.2em; padding: .1em 0 .1em 1em;
    border-left: 2.5pt solid #c9c9c9; color: #222; break-inside: avoid;
  }
  table {
    border-collapse: collapse; width: 100%; margin: .9em 0;
    font-size: 9.5pt; break-inside: avoid;
  }
  thead { display: table-header-group; }
  th, td { border: .6pt solid #999; padding: 4pt 6pt; vertical-align: top; text-align: left; }
  th { background: #f0f0f0; font-family: var(--sans); }
  tr { break-inside: avoid; }
  hr { border: 0; border-top: .6pt solid #ccc; margin: 1.4em 0; }
  img, svg { max-width: 100%; }
  figure { margin: 1.1em 0; break-inside: avoid; }
  figure img { display: block; width: 100%; border: .6pt solid #bbb; }
  /* A before/after pair is only worth embedding if both fit one page: keep the
     pair together as one block and cap the heights so the reader can compare
     without turning the sheet. */
  .parpair { break-inside: avoid; }
  .parpair figure { margin: .7em 0; }
  .parpair img { width: auto; height: auto; max-width: 100%; max-height: 88mm; }
  .parpair figcaption { margin-top: .3em; }
  figcaption {
    font: 9pt/1.4 var(--sans); color: #444;
    margin-top: .45em; padding-left: .2em;
  }
  code, pre { font-family: "Courier New", monospace; font-size: 9.5pt; }
  /* KLADDE-stempel — fjernes af sig selv, når de sidste TODO'er er udfyldt. */
  body.kladde::before {
    content: "KLADDE — IKKE INDGIVET";
    position: fixed; top: 44%; left: 0; right: 0;
    text-align: center; font: 700 42pt/1 var(--sans);
    color: rgba(190, 30, 30, .13); transform: rotate(-28deg);
    letter-spacing: .04em; z-index: 0; pointer-events: none;
  }
`;

for (const doc of DOCS) {
  doc.html = `<!doctype html><html lang="da"><head><meta charset="utf-8">
<title>${doc.title}</title><style>${css}</style></head>
<body class="${isDraft ? 'kladde' : ''}">${bodyOf(doc)}</body></html>`;

  // Chrome stamps a creation date into every PDF, so the PDF bytes are never
  // stable. Compare the rendered HTML instead: same input HTML, same document.
  // The kladde class is part of that HTML, so finalizing the anmodning makes
  // the tillæg stale too and forces it to re-render.
  doc.stampPath = doc.out + '.sha256';
  doc.stamp = createHash('sha256').update(doc.html).digest('hex');
}

// ---------------------------------------------------------------- check mode

if (check) {
  let stale = 0;
  for (const doc of DOCS) {
    if (!existsSync(doc.out)) {
      console.error(`FEJL: ${rel(doc.out)} findes ikke — kør: node bin/anmodning2pdf.mjs`);
      stale++;
    } else if (readStamp(doc) !== doc.stamp) {
      console.error(`FEJL: ${rel(doc.out)} er forældet — kør: node bin/anmodning2pdf.mjs`);
      stale++;
    } else {
      console.log(`OK — ${rel(doc.out)} svarer til kilden.`);
    }
  }
  process.exit(stale ? 1 : 0);
}

// Chrome writes a fresh creation timestamp into every render, so re-rendering
// an unchanged document still produces different bytes — and the hook would
// add a 3 MB blob to the history on every commit. Skip documents whose source
// has not moved; --force re-renders anyway (e.g. after changing the layout).
const force = process.argv.includes('--force');
const todo = DOCS.filter((doc) => force || !existsSync(doc.out) || readStamp(doc) !== doc.stamp);
for (const doc of DOCS.filter((d) => !todo.includes(d))) {
  if (stage) git(['add', '--', doc.out, doc.stampPath]);
  console.log(`${rel(doc.out)} er allerede aktuel — springer gengivelse over (--force gennemtvinger).`);
}
if (!todo.length) process.exit(0);

// ---------------------------------------------------------------- render

const headerHtml = (title) => `
  <div style="font:7.5pt ${SANS_ATTR};color:#555;width:100%;
              margin:0 18mm;display:flex;justify-content:space-between;
              border-bottom:.5pt solid #ccc;padding-bottom:3pt;">
    <span>${title}${isDraft ? ' · KLADDE' : ''}</span><span>${headerDate}</span>
  </div>`;

const footerHtml = `
  <div style="font:8pt ${SANS_ATTR};color:#555;width:100%;
              margin:0 18mm;text-align:right;">
    <span class="pageNumber"></span> af <span class="totalPages"></span>
  </div>`;

const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
try {
  for (const doc of todo) {
    const page = await browser.newPage();
    await page.setContent(doc.html, { waitUntil: 'load' });
    try {
      await page.pdf({
        path: doc.out,
        format: 'A4',
        printBackground: true,
        displayHeaderFooter: true,
        headerTemplate: headerHtml(doc.title),
        footerTemplate: footerHtml,
        margin: { top: '24mm', bottom: '20mm', left: '18mm', right: '18mm' },
        tagged: true,
      });
    } catch (err) {
      // Windows keeps the file locked while a PDF viewer has it open, and the
      // error Chrome surfaces for that does not say so.
      if (err?.code === 'EBUSY') {
        console.error(`FEJL: ${rel(doc.out)} er laast af et andet program — luk PDF'en i din fremviser og koer igen.`);
        process.exit(1);
      }
      throw err;
    }
    await page.close();

    writeFileSync(doc.stampPath, doc.stamp + '\n');
    // Called from the pre-commit hook: the artifact belongs in the same commit
    // as the source it was rendered from, the way bin/mermaid2svg.sh stages
    // its SVGs.
    if (stage) git(['add', '--', doc.out, doc.stampPath]);
    console.log(`Skrev ${rel(doc.out)} — ${doc.inlined} indlejret billede(r)${isDraft ? ', KLADDE (der er stadig [TODO:-markører i anmodningen)' : ''}`);
  }
} finally {
  await browser.close();
}

function rel(p) {
  return p.slice(repo.length + 1).replaceAll('\\', '/');
}

function readStamp(doc) {
  return existsSync(doc.stampPath) ? readFileSync(doc.stampPath, 'utf8').trim() : '';
}

function git(args) {
  execFileSync('git', args, { cwd: repo, stdio: 'inherit' });
}
