# Serve the site with native Ruby on Windows, no Docker (cf. serve-it.sh).
# Ruby: RubyInstaller 3.3 with devkit in C:\Tools\Ruby33 (or $env:RUBY_HOME),
# deliberately not on PATH so it does not reorder the MSYS git/python there.
param([int]$Port = 4000)

$ruby = if ($env:RUBY_HOME) { $env:RUBY_HOME } else { 'C:\Tools\Ruby33' }
$env:PATH = "$ruby\bin;$env:PATH"

bundle install --quiet
bundle exec jekyll serve --drafts --livereload --port $Port
