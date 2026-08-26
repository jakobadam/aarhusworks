# Fonts

Self-hosted rather than loaded from Google Fonts, so that reading a høringssvar
here makes no request to a third party.

Each file is the **latin subset** (`U+0000–00FF` and friends — covers æ, ø, å),
downloaded from the Google Fonts CDN. Regenerate by re-requesting the `css2`
endpoint for the families below and saving the `/* latin */` `woff2` for each
weight, then updating `fonts.css`.

| Family | Weights | Role | Licence |
| --- | --- | --- | --- |
| Barlow Condensed | 500, 600, 700 | Display, labels, wordmark | SIL Open Font License 1.1 |
| Source Serif 4 | 400, 400 italic, 600 | Long-form body text | SIL Open Font License 1.1 |
| IBM Plex Mono | 400, 600 | Dates, decibels, journal numbers, code | SIL Open Font License 1.1 |

All three are licensed under the SIL Open Font License 1.1, which permits
redistribution as part of a website. Full licence texts:

- Barlow — <https://github.com/jpt/barlow/blob/main/OFL.txt>
- Source Serif 4 — <https://github.com/adobe-fonts/source-serif/blob/release/LICENSE.md>
- IBM Plex — <https://github.com/IBM/plex/blob/master/LICENSE.txt>

`fonts.css` is hand-maintained and served directly (it is not run through Sass).
