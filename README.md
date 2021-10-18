
# githubtools

Some programs that make use of the [python github api](https://pygithub.readthedocs.io/en/latest/reference.html)


help text for makepr.py

```
This program does the following steps; it assumes that the current directory is in a git tree.

for the --new-pr option:
    1. Creates a feature branch for the current branch, and pushes the feature branch.
    2. Opens a pull request, it is assumed that a continuous integration build is then triggered.
    3. The program then waits that the continuous integration build for that pull request has completed.
    4. At the end of the build, a sound is played, and the url with the build log is written to standard output.

for the --update-pr option:
    1. Push the current state of local branch to the feature banch
    2. The program waits that the continuous integration build for the top commit has completed.
    3. At the end of the build, a sound is played, and the url with the build log is written to standard output.

for the --wait option:
    2. The program waits that the continuous integration build for the top commit has completed.
    3. At the end of the build, a sound is played, and the url with the build log is written to standard output.

Note that you need to set the organization (-o option) in the case of a private repository.

This program allows you to do some sword fighting, while the continuous integration build is going on ;-(

This program assumes that the environment GITHUB_TOKEN is exported, and that it has the token of the current user.
This program assumes the github api to be installed - pip install python-github-api

Push or update a pull request and wait for the continuous integration build to complete:
  --new-pr, -n       create new pull request (default: False)
  --update-pr, -u    update and push to existing pull request (default: False)
  --wait, -w         wait for ongoing build of top commit to complete (default: False)
  --org ORG, -o ORG  specify organization used to lookup the repository (default: )
  --showlog, -s      show the build log in a browser window (default: False)
  --verbose, -v      trace all commands, verbose output (default: False)
```

help text for starcounter.py

```
shows number of star of project owned by current github user
It also compares the number of stars against the previous state, and reports any difference. The new state is then stored in the starcounter.data file.

This program assumes that the environment GITHUB_TOKEN is exported, and that it has the token of the current user.
This program assumes the github api to be installed - pip install python-github-api
```

this is what we get when running it on my humble efforts here ;-)

```
name: duckduckbang stars:  20
name: jq-illustrated stars:  20
name: kind-helper stars:  18
name: cppcombinator stars:  16
name: cstuff stars:  11
name: s9k stars:  11
name: pythonimportplayground stars:  5
name: myenv stars:  4
name: pygamewrap stars:  3
name: pythoncourse stars:  2
name: roget-thesaurus-parser stars:  2
name: gitblame stars:  1
name: k8explain stars:  1
name: opinionated-fortune-cow stars:  1
name: pprintex stars:  1
name: bloxroutehomework stars:  0
name: follow-kube-logs stars:  0
name: githubapitools stars:  0
name: github_pr_comments stars:  0
name: grpc-spring-boot-starter-utils stars:  0
name: ls-annotations stars:  0
name: microsofthomework stars:  0
name: my-notes stars:  0
name: scriptrunner-operator stars:  0
name: visual-python-strace stars:  0
name: zipit stars:  0
***
total stars:  116
```

