## Running locally with Docker (recommended)

```powershell
./serve-it.sh
```

Open http://127.0.0.1:4000. The site live-reloads on file changes.

## Running locally with Ruby

```
curl -sSL https://get.rvm.io | bash -s stable
rvm install ruby-2.7.2
rvm use 2.7.2
```


```
gem install jekyll bundler
```

Install needed deps:
```
bundle install
```

```
bundle update jekyll
```

``` shell
bundle exec jekyll serve
```
