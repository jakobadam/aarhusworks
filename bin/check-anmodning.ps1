# Verifies _posts/2026-08-26-anmodning-om-tilsynssag.md — the
# Ankestyrelsen filing. It is long, heavily cross-referenced and cites ~90
# bilag by URL, so the things that break are links and headings, not prose.
#
# Usage: pwsh bin/check-anmodning.ps1          # static checks only, seconds
#        pwsh bin/check-anmodning.ps1 -Build   # + Jekyll build and render checks
#
# Exit 1 on any ERROR. NOTEs are informational and never fail the run.

[CmdletBinding()]
param(
    [switch]$Build,
    [string]$Post = '_posts/2026-08-26-anmodning-om-tilsynssag.md'
)

$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)

$errors = @()
$notes = @()

if (-not (Test-Path $Post)) { Write-Host "ERROR: $Post not found"; exit 1 }

$lines = @(Get-Content $Post)
$raw = Get-Content $Post -Raw

# --- Title ------------------------------------------------------------------
# The invariant is that exactly one title renders, not that front matter
# exists. With front matter the title comes from title:; without it Jekyll
# titleizes the filename. Either is fine — what breaks the page is a heading
# in the body on top of whichever one the layout already renders.
$title = $null
$bodyStart = 0
if ($lines[0].Trim() -ne '---') {
    $slug = [IO.Path]::GetFileNameWithoutExtension($Post) -replace '^\d{4}-\d{2}-\d{2}-', ''
    $title = (($slug -split '-') | ForEach-Object {
        if ($_) { $_.Substring(0,1).ToUpper() + $_.Substring(1) }
    }) -join ' '
    $notes += "no front matter — Jekyll derives the title from the filename: `"$title`""
} else {
    $close = 1
    while ($close -lt $lines.Count -and $lines[$close].Trim() -ne '---') { $close++ }
    if ($close -ge $lines.Count) {
        $errors += "front matter is never closed by a second '---'"
        $bodyStart = $lines.Count
    } else {
        $bodyStart = $close + 1
        $fm = $lines[1..($close - 1)]
        $titleLine = $fm | Where-Object { $_ -match '^\s*title\s*:' } | Select-Object -First 1
        if (-not $titleLine) {
            $errors += "front matter has no title:"
        } else {
            $title = ($titleLine -replace '^\s*title\s*:\s*', '').Trim().Trim('"', "'")
        }

        # The default permalink is /:categories/:year/:month/:day/:title.html,
        # so adding a category moves the post and 404s the published URL.
        # Allowed only if a redirect_from preserves the old path.
        if (($fm -match '^\s*categories\s*:') -and -not ($fm -match 'redirect_from.*2026/08/26')) {
            $errors += "categories: in front matter moves the post's URL — add redirect_from for /2026/08/26/anmodning-om-tilsynssag.html or drop it"
        }
    }
}

# A body-level h1 stacks a second title under whichever one the layout renders,
# so it is wrong with or without front matter.
$fenced = $false
for ($i = $bodyStart; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^\s*(```|~~~)') { $fenced = -not $fenced; continue }
    if (-not $fenced -and $lines[$i] -match '^#\s+\S') {
        $errors += "line $($i + 1) is a body-level h1 — the layout already renders the title"
    }
}

# --- Bilag links ------------------------------------------------------------
# The invariant is that the asset is committed: a PDF that exists only on this
# machine 404s for every reader of aarhusworks.com.
$assets = [regex]::Matches($raw, 'https://aarhusworks\.com/(assets/[^)\s"]+)') |
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
foreach ($m in $missing) { $errors += "bilag link has no such file: $m" }
foreach ($u in $uncommitted) { $errors += "bilag exists locally but is not committed (404 for readers): $u" }
$notes += "$($assets.Count) distinct bilag paths checked, $($assets.Count - $missing.Count - $uncommitted.Count) committed"

# --- Draft status -----------------------------------------------------------
if ($raw -notmatch 'KLADDE') {
    $notes += "the KLADDE banner is gone — this now reads as a filed document"
}
$todo = @($lines | Where-Object { $_ -match '\[TODO' })
if ($todo.Count -gt 0) {
    $notes += "$($todo.Count) unresolved [TODO] marker(s) — still a draft:"
    $todo | ForEach-Object { $notes += "    " + $_.Trim() }
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

    $expected = '_site/2026/08/26/anmodning-om-tilsynssag.html'
    if (-not (Test-Path $expected)) {
        $built = Get-ChildItem _site -Recurse -Filter 'anmodning-om-tilsynssag*.html' -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if ($built) {
            $errors += "post rendered to $($built.FullName.Replace($PWD.Path,'')) — the published URL $expected moved"
        } else {
            $errors += "post did not render at all"
        }
    } else {
        $html = Get-Content $expected -Raw

        $h1 = [regex]::Matches($html, '<h1[^>]*>(.*?)</h1>')
        if ($h1.Count -ne 1) {
            $errors += "expected exactly 1 <h1> in the rendered page, found $($h1.Count): " +
                       (($h1 | ForEach-Object { '"' + $_.Groups[1].Value + '"' }) -join ', ')
        } elseif ($title -and $h1[0].Groups[1].Value.Trim() -ne $title) {
            $errors += "rendered <h1> is `"$($h1[0].Groups[1].Value.Trim())`" but front matter title is `"$title`""
        }

        # Anchors are checked against the ids kramdown actually emitted rather
        # than guessed from the markdown headings.
        $ids = @{}
        [regex]::Matches($html, 'id="([^"]+)"') | ForEach-Object { $ids[$_.Groups[1].Value] = $true }
        $anchors = [regex]::Matches($raw, '\]\(#([^)]+)\)') |
            ForEach-Object { [System.Uri]::UnescapeDataString($_.Groups[1].Value) } | Sort-Object -Unique
        $dead = $anchors | Where-Object { -not $ids.ContainsKey($_) }
        foreach ($d in $dead) { $errors += "cross-reference points at nothing: #$d" }
        $notes += "$($anchors.Count) distinct anchor targets checked, $($anchors.Count - @($dead).Count) resolve"
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
