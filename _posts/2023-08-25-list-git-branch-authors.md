---
title: "Git: Listing branch authors"
author: Jakob Aarøe Dam
---

In Git, a ref is a named reference to a commit hash, such as a branch name pointing to a commit hash. Git maintains this
mapping in the `.git/refs` directory, which contains subdirectories for `heads`, `tags`, and `remotes`.

```
$ git init refs-test ; cd refs-test
$ git checkout -b mine/bugfix/1
$ touch foo
$ git add foo
$ git commit -m "add foo"
```

Now, the heads directory contains a file named `mine/bugfix/1` for this new branch, referencing the commit.

```
$ find .git/refs/heads/*
.git/refs/heads/mine
.git/refs/heads/mine/bugfix
.git/refs/heads/mine/bugfix/1
```

Although many of us prefer short-lived branches, the reality often is another thing.
In larger projects, the number of branches tends to reproduce rapidly. Over time, people leave, and stale branches
accumulate.

To address this, I prefer putting my own branches into a dedicated directory within `refs` by prefixing branch names
with my initials.

This approach makes it easy to display my own branches:

```
$ find .git/refs/heads/mine -type f
.git/refs/heads/mine/bugfix/1
```

However, it's still nice to try to get rid of those old stale branches. The first step is to list them, for which
the [`git for-each-ref`](https://git-scm.com/docs/git-for-each-ref) is the right tool.

From the above, we now know that each branch has a `ref`, and the `git for-each-ref` can be used to iterate over
it and pretty print it.

```bash
#!/bin/sh
# list all git branches and its author sorted by date ascending
git for-each-ref --format='%(color:cyan)%(authordate:format:%Y-%d-%m) %(align:32,left)%(color:yellow)%(authorname)%(end) %(color:reset)%(refname:strip=3)' --sort=authordate refs/remotes
```

Used on the Angular `ngx-charts` open source project:

```bash
$ git for-each-ref --format='%(color:cyan)%(authordate:format:%Y-%d-%m) %(align:32,left)%(color:yellow) **** NAME HIDDEN **** %(end) %(color:reset)%(refname:strip=3)' --sort=authordate refs/remotes
2017-21-02  **** NAME HIDDEN ****        legend-position
2018-17-05  **** NAME HIDDEN ****        docs-test
2018-20-07  **** NAME HIDDEN ****        feature/improved-number-cards
2019-15-01  **** NAME HIDDEN ****        7.x
2019-29-01  **** NAME HIDDEN ****        clapis-master
2019-13-02  **** NAME HIDDEN ****        advanced-legend-trucated-label-click-fix
2019-08-05  **** NAME HIDDEN ****        deprecate-force-directed
2019-21-05  **** NAME HIDDEN ****        gnomeontherun-gauge-no-text-option
2019-29-05  **** NAME HIDDEN ****        rework-mouse-events
...
```

Which indicates to us that house cleaning might not be of the biggest priority for that project, or that they forgot
the command to delete the remote branch:

```bash
git push origin --delete branch-name
```


