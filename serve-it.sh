#!/usr/bin/env bash
export MSYS_NO_PATHCONV=1
docker run --rm -v "${PWD}:/site" -w /site -p 4000:4000 ruby:3.1 bash -c "gem install bundler -v 2.5.10 --quiet && bundle install --quiet && bundle exec jekyll serve --draft --host 0.0.0.0 --force_polling"
