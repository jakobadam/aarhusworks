#!/usr/bin/env node
// Render the Ankestyrelsen filing to a paginated A4 PDF.
//
//   node bin/anmodning2pdf.mjs            # write the PDF
//   node bin/anmodning2pdf.mjs --check    # exit 1 if the committed PDF is stale
//   node bin/anmodning2pdf.mjs --stage    # write it and git add the result (hook)
//
// The PDF is the copy that gets filed, so a draft must never look clean: while
// [TODO: markers remain in the source, every page carries KLADDE in the running
// header and page 1 gets a watermark. The filename stays the same either way —
// the filing links to it, so the URL must not move when the draft goes final.
// Layout follows the afklaringsnotater — A4, title and date in a running
// header, "N af M" in the footer.
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
const SOURCE = resolve(repo, '_posts/2026-08-26-anmodning-om-tilsynssag.md');
// ANMODNING_PDF_OUT renders somewhere else — useful when a PDF viewer holds a
// lock on the real file, which Windows enforces.
const out = process.env.ANMODNING_PDF_OUT
  ? resolve(process.env.ANMODNING_PDF_OUT)
  : resolve(repo, 'assets/giber-ringvej/klage/anmodning-om-tilsynssag.pdf');
const TITLE = 'Anmodning om tilsynssag — Giber Ringvej';

const check = process.argv.includes('--check');
const stage = process.argv.includes('--stage');

// ---------------------------------------------------------------- source

const source = readFileSync(SOURCE, 'utf8');
const isDraft = source.includes('[TODO:');

// Passages the web page wants but the PDF must not carry — the link to this
// very PDF, above all. The markers are HTML comments, so they render as
// nothing on aarhusworks.com and need no counterpart in the Jekyll build.
const md = source.replace(/[^\S\n]*<!--\s*pdf:skip\s*-->[\s\S]*?<!--\s*\/pdf:skip\s*-->[^\S\n]*\n?/g, '');
if (md === source) console.warn('Bemaerk: ingen <!-- pdf:skip -->-afsnit fundet i kilden.');

// The header date is the filing's own "**Dato:**" line once it is filled in.
const dateLine = md.match(/^\*\*Dato:\*\*\s*(.+)$/m)?.[1]?.trim() ?? '';
const headerDate = /TODO/.test(dateLine) || !dateLine
  ? `Udkast ${new Date().toISOString().slice(0, 10)}`
  : dateLine.replace(/[*_]/g, '').trim();

// Every internal cross-reference in the filing targets an explicit
// <a id="..."> anchor, so marked needs no heading-id extension for the 25
// section links to resolve inside the PDF. Bilag URLs are left alone and stay
// clickable.
const body = marked.parse(md, { gfm: true, breaks: false });

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

const html = `<!doctype html><html lang="da"><head><meta charset="utf-8">
<title>${TITLE}</title><style>${css}</style></head>
<body class="${isDraft ? 'kladde' : ''}">${body}</body></html>`;

// ---------------------------------------------------------------- check mode

// Chrome stamps a creation date into every PDF, so the PDF bytes are never
// stable. Compare the rendered HTML instead: same input HTML, same document.
const stampPath = out + '.sha256';
const stamp = createHash('sha256').update(html).digest('hex');

if (check) {
  if (!existsSync(out)) {
    console.error(`FEJL: ${rel(out)} findes ikke — kør: node bin/anmodning2pdf.mjs`);
    process.exit(1);
  }
  if (readStamp() !== stamp) {
    console.error(`FEJL: ${rel(out)} er forældet — kør: node bin/anmodning2pdf.mjs`);
    process.exit(1);
  }
  console.log(`OK — ${rel(out)} svarer til kilden.`);
  process.exit(0);
}

// Chrome writes a fresh creation timestamp into every render, so re-rendering
// an unchanged document still produces different bytes — and the hook would
// add a 3 MB blob to the history on every commit. Skip when the source has not
// moved; --force re-renders anyway (e.g. after changing the layout below).
if (existsSync(out) && readStamp() === stamp && !process.argv.includes('--force')) {
  if (stage) git(['add', '--', out, stampPath]);
  console.log(`${rel(out)} er allerede aktuel — springer gengivelse over (--force gennemtvinger).`);
  process.exit(0);
}

// ---------------------------------------------------------------- render

const headerHtml = `
  <div style="font:7.5pt ${SANS_ATTR};color:#555;width:100%;
              margin:0 18mm;display:flex;justify-content:space-between;
              border-bottom:.5pt solid #ccc;padding-bottom:3pt;">
    <span>${TITLE}${isDraft ? ' · KLADDE' : ''}</span><span>${headerDate}</span>
  </div>`;

const footerHtml = `
  <div style="font:8pt ${SANS_ATTR};color:#555;width:100%;
              margin:0 18mm;text-align:right;">
    <span class="pageNumber"></span> af <span class="totalPages"></span>
  </div>`;

const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
try {
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'load' });
  await page.pdf({
    path: out,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: headerHtml,
    footerTemplate: footerHtml,
    margin: { top: '24mm', bottom: '20mm', left: '18mm', right: '18mm' },
    tagged: true,
  });
} catch (err) {
  // Windows keeps the file locked while a PDF viewer has it open, and the
  // error Chrome surfaces for that does not say so.
  if (err?.code === 'EBUSY') {
    console.error(`FEJL: ${rel(out)} er laast af et andet program — luk PDF'en i din fremviser og koer igen.`);
    process.exit(1);
  }
  throw err;
} finally {
  await browser.close();
}

writeFileSync(stampPath, stamp + '\n');

// Only one of the two filenames may exist, or the filing folder ends up with a
// stale draft next to a final copy.
// Called from the pre-commit hook: the artifact belongs in the same commit as
// the source it was rendered from, the way bin/mermaid2svg.sh stages its SVGs.
if (stage) git(['add', '--', out, stampPath]);

console.log(`Skrev ${rel(out)}${isDraft ? '  (KLADDE — der er stadig [TODO:-markører i kilden)' : ''}`);

function rel(p) {
  return p.slice(repo.length + 1).replaceAll('\\', '/');
}

function readStamp() {
  return existsSync(stampPath) ? readFileSync(stampPath, 'utf8').trim() : '';
}

function git(args) {
  execFileSync('git', args, { cwd: repo, stdio: 'inherit' });
}
