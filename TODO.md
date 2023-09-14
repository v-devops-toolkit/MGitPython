# TO DO

* install MGitPython in https://pypi.org/
* parse toml file and use version in `MultiGit.version` command
* use `commands.yaml` file with commands defined as

```
name: info
cmds:
    - ["git", "status", "-sb"]
    - ["git", "rev-parse", "--short=8", "HEAD"]
    - ["git", "describe", "--tags"]


name: update
cmds:
    - ["git", "fetch"]
    - ["git", "reset", "--hard"]
    - ["git", "clean", "-df"]
    - ["git", "rebase"]
```

* parse all git aliases with

```
git config --get-regexp '^alias\.'
```

* use default command for aliases:

```
mgit s  => mgit git s
```
