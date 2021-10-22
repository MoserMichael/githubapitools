
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

This program assumes that the environment GITHUB_TOKEN is exported (github access token of the current user)
Requires the following pip packages: PyGithub websocket-client

This program allows you to do some sword fighting, while the continuous integration build is going on ;-)

Push or update a pull request and wait for the continuous integration build to complete:
  --new-pr, -n          create new pull request (default: False)
  --update-pr, -u       update and push to existing pull request (default: False)
  --wait, -w            wait for ongoing build of top commit to complete (default: False)
  --org ORG, -o ORG     specify organization used to lookup the repository (default: )
  --showlog, -s         show the build log in a bew browser (default: False)
  --dumplog DUMPLOG, -d DUMPLOG
                        dump the build log in json format to file name (default: )
  --verbose, -v         trace all commands, verbose output (default: False)
```

help text for starcounter.py

```
usage: starcounter.py [-h] [--show-stars] [--show-views]

shows number of star of project owned by current github user and usage
statistics This program assumes that the environment GITHUB_TOKEN is exported,
and that it has the token of the current user. It also compares the number of
stars against the previous state, and reports any difference. The new state is
then stored in the starcounter.data file. This program assumes the github api
to be installed - pip install python-github-api

optional arguments:
  -h, --help        show this help message and exit

view github data on current users repositories:
  --show-stars, -s  show stars (default: True)
  --show-views, -v  show views (default: False)
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
name: printb stars:  0
name: scriptrunner-operator stars:  0
name: visual-python-strace stars:  0
name: zipit stars:  0
***
total stars:  116

Traffic report

repo: gitblame views: total: 93 unique:  11
	 2021-10-04 00:00:00 total: 50 unique: 5
	 2021-10-11 00:00:00 total: 40 unique: 9
	 2021-10-18 00:00:00 total: 3 unique: 2
repo: githubapitools views: total: 41 unique:  5
	 2021-10-11 00:00:00 total: 30 unique: 4
	 2021-10-18 00:00:00 total: 11 unique: 3
repo: pythonimportplayground views: total: 37 unique:  12
	 2021-10-04 00:00:00 total: 24 unique: 5
	 2021-10-11 00:00:00 total: 10 unique: 8
	 2021-10-18 00:00:00 total: 3 unique: 1
repo: pythoncourse views: total: 35 unique:  4
	 2021-10-04 00:00:00 total: 16 unique: 2
	 2021-10-11 00:00:00 total: 19 unique: 3
repo: printb views: total: 28 unique:  5
	 2021-10-11 00:00:00 total: 21 unique: 5
	 2021-10-18 00:00:00 total: 7 unique: 2
repo: my-notes views: total: 22 unique:  4
	 2021-10-04 00:00:00 total: 11 unique: 2
	 2021-10-11 00:00:00 total: 9 unique: 3
	 2021-10-18 00:00:00 total: 2 unique: 1
repo: ls-annotations views: total: 13 unique:  2
	 2021-10-04 00:00:00 total: 2 unique: 1
	 2021-10-11 00:00:00 total: 11 unique: 1
repo: pygamewrap views: total: 13 unique:  6
	 2021-10-04 00:00:00 total: 9 unique: 2
	 2021-10-11 00:00:00 total: 4 unique: 4
repo: cppcombinator views: total: 11 unique:  6
	 2021-10-04 00:00:00 total: 2 unique: 2
	 2021-10-11 00:00:00 total: 8 unique: 3
	 2021-10-18 00:00:00 total: 1 unique: 1
repo: jq-illustrated views: total: 8 unique:  1
	 2021-10-18 00:00:00 total: 8 unique: 1
repo: kind-helper views: total: 7 unique:  5
	 2021-10-04 00:00:00 total: 4 unique: 2
	 2021-10-11 00:00:00 total: 2 unique: 2
	 2021-10-18 00:00:00 total: 1 unique: 1
repo: s9k views: total: 7 unique:  3
	 2021-10-04 00:00:00 total: 5 unique: 1
	 2021-10-11 00:00:00 total: 2 unique: 2
repo: zipit views: total: 7 unique:  6
	 2021-10-04 00:00:00 total: 3 unique: 3
	 2021-10-11 00:00:00 total: 3 unique: 2
	 2021-10-18 00:00:00 total: 1 unique: 1
repo: duckduckbang views: total: 6 unique:  5
	 2021-10-04 00:00:00 total: 4 unique: 3
	 2021-10-11 00:00:00 total: 2 unique: 2
repo: github_pr_comments views: total: 6 unique:  2
	 2021-10-11 00:00:00 total: 6 unique: 2
repo: pprintex views: total: 4 unique:  2
	 2021-10-04 00:00:00 total: 3 unique: 2
	 2021-10-11 00:00:00 total: 1 unique: 1
repo: cstuff views: total: 3 unique:  2
	 2021-10-04 00:00:00 total: 1 unique: 1
	 2021-10-11 00:00:00 total: 1 unique: 1
	 2021-10-18 00:00:00 total: 1 unique: 1
repo: follow-kube-logs views: total: 2 unique:  1
	 2021-10-11 00:00:00 total: 2 unique: 1
repo: bloxroutehomework views: total: 1 unique:  1
	 2021-10-11 00:00:00 total: 1 unique: 1
repo: grpc-spring-boot-starter-utils views: total: 1 unique:  1
	 2021-10-04 00:00:00 total: 1 unique: 1
repo: myenv views: total: 1 unique:  1
	 2021-10-11 00:00:00 total: 1 unique: 1
repo: opinionated-fortune-cow views: total: 1 unique:  1
	 2021-10-04 00:00:00 total: 1 unique: 1
repo: scriptrunner-operator views: total: 1 unique:  1
	 2021-10-11 00:00:00 total: 1 unique: 1
repo: k8explain views: total: 0 unique:  0
repo: microsofthomework views: total: 0 unique:  0
repo: roget-thesaurus-parser views: total: 0 unique:  0
repo: visual-python-strace views: total: 0 unique:  0
```
# Installation

You need to install the following packages:

- ```pip3 install PyGithub```
- ```pip3 install websocket-client``` 

or install via requirements.txt file

```pip3 install -r requirements.txt```

