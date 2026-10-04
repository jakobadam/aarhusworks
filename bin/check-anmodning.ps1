# Verifies the Ankestyrelsen filing — _posts/2026-08-26-anmodning-om-tilsynssag.md
# and its tillæg, _posts/2026-08-26-anmodning-om-tilsynssag-tillaeg.md. They are
# long, heavily cross-referenced (within each post and between the two) and
# cite ~90 bilag by URL, so the things that break are links and headings, not
# prose.
#
# Usage: pwsh bin/check-anmodning.ps1          # static checks only, seconds
#        pwsh bin/check-anmodning.ps1 -Quotes  # + every quote against its source
#        pwsh bin/check-anmodning.ps1 -Build   # + Jekyll build and render checks
#
# Exit 1 on any ERROR. NOTEs are informational and never fail the run.

[CmdletBinding()]
param(
    [switch]$Build,
    [switch]$Quotes,
    [string]$Post = '_posts/2026-08-26-anmodning-om-tilsynssag.md',
    [string]$Tillaeg = '_posts/2026-08-26-anmodning-om-tilsynssag-tillaeg.md'
)

$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)

$errors = @()
$notes = @()

# Each post, with the URL it is published at. Both carry no category, so the
# URL is /:year/:month/:day/:title.html — see the permalink note below.
$docs = @()
foreach ($p in @($Post, $Tillaeg)) {
    if (-not (Test-Path $p)) { Write-Host "ERROR: $p not found"; exit 1 }
    $slug = [IO.Path]::GetFileNameWithoutExtension($p) -replace '^\d{4}-\d{2}-\d{2}-', ''
    $date = ([IO.Path]::GetFileName($p) -replace '^(\d{4})-(\d{2})-(\d{2})-.*', '$1/$2/$3')
    $docs += [pscustomobject]@{
        Path  = $p
        Name  = [IO.Path]::GetFileName($p)
        Lines = @(Get-Content $p)
        Raw   = Get-Content $p -Raw
        Rel   = "$date/$slug.html"
        Url   = "https://aarhusworks.com/$date/$slug.html"
        Title = $null
    }
}
$anmodning = $docs[0]

foreach ($d in $docs) {
    $lines = $d.Lines
    $tag = "$($d.Name):"

    # --- Title --------------------------------------------------------------
    # The invariant is that exactly one title renders, not that front matter
    # exists. With front matter the title comes from title:; without it Jekyll
    # titleizes the filename. Either is fine — what breaks the page is a
    # heading in the body on top of whichever one the layout already renders.
    $bodyStart = 0
    if ($lines[0].Trim() -ne '---') {
        $slug = [IO.Path]::GetFileNameWithoutExtension($d.Path) -replace '^\d{4}-\d{2}-\d{2}-', ''
        $d.Title = (($slug -split '-') | ForEach-Object {
            if ($_) { $_.Substring(0,1).ToUpper() + $_.Substring(1) }
        }) -join ' '
        $notes += "$tag no front matter — Jekyll derives the title from the filename: `"$($d.Title)`""
    } else {
        $close = 1
        while ($close -lt $lines.Count -and $lines[$close].Trim() -ne '---') { $close++ }
        if ($close -ge $lines.Count) {
            $errors += "$tag front matter is never closed by a second '---'"
            $bodyStart = $lines.Count
        } else {
            $bodyStart = $close + 1
            $fm = $lines[1..($close - 1)]
            $titleLine = $fm | Where-Object { $_ -match '^\s*title\s*:' } | Select-Object -First 1
            if (-not $titleLine) {
                $errors += "$tag front matter has no title:"
            } else {
                $d.Title = ($titleLine -replace '^\s*title\s*:\s*', '').Trim().Trim('"', "'")
            }

            # The default permalink is /:categories/:year/:month/:day/:title.html,
            # so adding a category moves the post and 404s the published URL —
            # and every link the other document holds to it. Allowed only if a
            # redirect_from preserves the old path.
            if (($fm -match '^\s*categories\s*:') -and -not ($fm -match "redirect_from.*$([regex]::Escape($d.Rel))")) {
                $errors += "$tag categories: in front matter moves the post's URL — add redirect_from for /$($d.Rel) or drop it"
            }
        }
    }

    # A body-level h1 stacks a second title under whichever one the layout
    # renders, so it is wrong with or without front matter.
    $fenced = $false
    for ($i = $bodyStart; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '^\s*(```|~~~)') { $fenced = -not $fenced; continue }
        if (-not $fenced -and $lines[$i] -match '^#\s+\S') {
            $errors += "$tag line $($i + 1) is a body-level h1 — the layout already renders the title"
        }
    }

    # --- Bilag links --------------------------------------------------------
    # The invariant is that the asset is committed: a PDF that exists only on
    # this machine 404s for every reader of aarhusworks.com.
    $assets = [regex]::Matches($d.Raw, 'https://aarhusworks\.com/(assets/[^)\s"]+)') |
        ForEach-Object { [System.Uri]::UnescapeDataString(($_.Groups[1].Value -split '#')[0]) } |
        Sort-Object -Unique
    $uncommitted = @()
    $missing = @()
    foreach ($a in $assets) {
        git cat-file -e "HEAD:$a" 2>$null
        if ($LASTEXITCODE -ne 0) {
            if (Test-Path $a) { $uncommitted += $a } else { $missing += $a }
        }
    }
    foreach ($m in $missing) { $errors += "$tag bilag link has no such file: $m" }
    foreach ($u in $uncommitted) { $errors += "$tag bilag exists locally but is not committed (404 for readers): $u" }
    $notes += "$tag $(@($assets).Count) distinct bilag paths checked, $(@($assets).Count - $missing.Count - $uncommitted.Count) committed"
}

# --- Draft status -----------------------------------------------------------
# The tillæg is filed with the anmodning: it must say KLADDE exactly as long as
# the anmodning does, or one of them reads as filed while the other is a draft.
$draft = $anmodning.Raw -match 'KLADDE'
if (-not $draft) { $notes += "the KLADDE banner is gone — the anmodning now reads as a filed document" }
foreach ($d in $docs | Select-Object -Skip 1) {
    if (($d.Raw -match 'KLADDE') -ne $draft) {
        $errors += "$($d.Name): KLADDE banner $(if ($draft) { 'missing' } else { 'still present' }) — must match the anmodning"
    }
}
# Both the inline *[TODO: ...]* placeholders and bare "TODO ..." notes left at
# the start of a line. Requiring line-start keeps the word out of prose.
foreach ($d in $docs) {
    $todo = @($d.Lines | Where-Object { $_ -match '\[TODO' -or $_ -match '^\s*TODO\b' })
    if ($todo.Count -gt 0) {
        $notes += "$($d.Name): $($todo.Count) unresolved [TODO] marker(s) — still a draft:"
        $todo | ForEach-Object { $notes += "    " + $_.Trim() }
    }
}

# --- Quotes against their sources -------------------------------------------
# Independent of -Build: this needs Python and the PDFs, not docker.
if ($Quotes) {
    foreach ($d in $docs) {
        Write-Host "Checking quotes in $($d.Name) against the cited PDFs..."
        $quoteScript = Join-Path $PSScriptRoot 'check-quotes.py'
        & python $quoteScript (Get-Location).Path (Resolve-Path $d.Path).Path
        if ($LASTEXITCODE -eq 2) {
            $errors += "$($d.Name): quote check could not run (see message above)"
        } elseif ($LASTEXITCODE -ne 0) {
            $errors += "$($d.Name): quotes could not be verified against their sources — see the list above"
        }
    }
}

# --- Rendered output --------------------------------------------------------
if ($Build) {
    Write-Host "Building with Jekyll (docker)..."
    # The named volume persists installed gems; without it every run redoes
    # bundle install (~3 min) for a 40s build, and gets skipped in practice.
    docker run --rm -v "${PWD}:/site" -v aarhusworks-bundle:/usr/local/bundle -w /site ruby:3.1 `
        bash -c "gem install bundler -v 2.5.10 --quiet >/dev/null 2>&1; bundle install --quiet && bundle exec jekyll build" |
        Select-Object -Last 3
    if ($LASTEXITCODE -ne 0) { $errors += "jekyll build failed" }

    # The ids each page actually emitted, by published URL. Anchors are checked
    # against these rather than guessed from the markdown headings.
    $idsByUrl = @{}
    foreach ($d in $docs) {
        $expected = "_site/$($d.Rel)"
        if (-not (Test-Path $expected)) {
            $name = [IO.Path]::GetFileName($d.Rel)
            $built = Get-ChildItem _site -Recurse -Filter $name -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($built) {
                $errors += "$($d.Name): rendered to $($built.FullName.Replace($PWD.Path,'')) — the published URL /$($d.Rel) moved"
            } else {
                $errors += "$($d.Name): did not render at all"
            }
            continue
        }
        $html = Get-Content $expected -Raw

        $h1 = [regex]::Matches($html, '<h1[^>]*>(.*?)</h1>')
        if ($h1.Count -ne 1) {
            $errors += "$($d.Name): expected exactly 1 <h1> in the rendered page, found $($h1.Count): " +
                       (($h1 | ForEach-Object { '"' + $_.Groups[1].Value + '"' }) -join ', ')
        } elseif ($d.Title -and $h1[0].Groups[1].Value.Trim() -ne $d.Title) {
            $errors += "$($d.Name): rendered <h1> is `"$($h1[0].Groups[1].Value.Trim())`" but front matter title is `"$($d.Title)`""
        }

        $ids = @{}
        [regex]::Matches($html, 'id="([^"]+)"') | ForEach-Object { $ids[$_.Groups[1].Value] = $true }
        $idsByUrl[$d.Url] = $ids
    }

    # Within a post: (#id). Between the two: the absolute URL of the other post
    # with #id — the split moved some 30 links across, and the bilag check
    # above only covers /assets/.
    $pageUrls = ($docs | ForEach-Object { [regex]::Escape($_.Url) }) -join '|'
    foreach ($d in $docs) {
        if (-not $idsByUrl.ContainsKey($d.Url)) { continue }
        $targets = @()
        $targets += [regex]::Matches($d.Raw, '\]\(#([^)]+)\)') |
            ForEach-Object { [pscustomobject]@{ Url = $d.Url; Id = [System.Uri]::UnescapeDataString($_.Groups[1].Value) } }
        $targets += [regex]::Matches($d.Raw, "\]\(($pageUrls)#([^)]+)\)") |
            ForEach-Object { [pscustomobject]@{ Url = $_.Groups[1].Value; Id = [System.Uri]::UnescapeDataString($_.Groups[2].Value) } }
        $distinct = $targets | Sort-Object Url, Id -Unique
        $dead = @($distinct | Where-Object { -not ($idsByUrl.ContainsKey($_.Url) -and $idsByUrl[$_.Url].ContainsKey($_.Id)) })
        foreach ($x in $dead) {
            $where = if ($x.Url -eq $d.Url) { '' } else { $x.Url + ' ' }
            $errors += "$($d.Name): cross-reference points at nothing: $where#$($x.Id)"
        }
        $notes += "$($d.Name): $(@($distinct).Count) distinct anchor targets checked, $(@($distinct).Count - $dead.Count) resolve"
    }
}

# --- Report -----------------------------------------------------------------
if ($notes) {
    Write-Host ""
    Write-Host "Notes:"
    $notes | ForEach-Object { Write-Host "  $_" }
}
if ($errors) {
    Write-Host ""
    Write-Host "Errors:"
    $errors | ForEach-Object { Write-Host "  $_" }
    Write-Host ""
    Write-Host "$($errors.Count) error(s)."
    exit 1
}
Write-Host ""
Write-Host ("OK — no errors" + $(if ($Build) { " (static + rendered)" } else { " (static only; add -Build for render checks)" }) + ".")
