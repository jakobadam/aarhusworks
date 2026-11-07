#!/usr/bin/env bash
export MSYS_NO_PATHCONV=1
docker run --rm -it \
  -v "$PWD":/site -w /site \
  -p 4000:4000 -p 35729:35729 \
  ruby:3.3 \
  bash -c "bundle install && bundle exec jekyll serve --drafts --host 0.0.0.0 --livereload --force_polling"
