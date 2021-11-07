
# githubtools

Some programs that make use of the [python github api](https://pygithub.readthedocs.io/en/latest/reference.html)

At work, I am using the ```makepr.py``` script to automate deployment tasks; most deployment tasks involve the following steps: Commit the change, open a pull request, wait for the CI build to complete and download the build log, extract an image id from the CI build log, put it in some other repository and commit the change. It is possible to automate the first three steps with the github api (if your shop is using github). The rest of the deployment process is also scriptable.

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
  --stats-time STAT_TIME, -t STAT_TIME
                        time resulution of views (for --show-views) (default: week)
```

Also it gives you some visitor statistics, without having to use the google analytics spyware. (I am not using google analytics)
This is what we get when running it on my humble efforts here ;-)

```
name: duckduckbang stars:  21
name: jq-illustrated stars:  20
name: kind-helper stars:  20
name: cppcombinator stars:  17
name: s9k stars:  12
name: cstuff stars:  11
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
name: flagged-hn stars:  0
name: follow-kube-logs stars:  0
name: githubapitools stars:  0
name: github_pr_comments stars:  0
name: grpc-spring-boot-starter-utils stars:  0
name: kwchecker stars:  0
name: ls-annotations stars:  0
name: microsofthomework stars:  0
name: my-notes stars:  0
name: printb stars:  0
name: scriptrunner-operator stars:  0
name: subb stars:  0
name: vimcrypt stars:  0
name: vimcrypt2 stars:  0
name: visual-python-strace stars:  0
name: zipit stars:  0
***
total stars:  121

Traffic report

repo: vimcrypt2 views: total: 80 unique:  20
Views:
	 2021-10-30 00:00:00 total: 36 unique: 11
	 2021-10-31 00:00:00 total: 12 unique: 4
	 2021-11-01 00:00:00 total: 17 unique: 5
	 2021-11-02 00:00:00 total: 1 unique: 1
	 2021-11-03 00:00:00 total: 4 unique: 1
	 2021-11-05 00:00:00 total: 5 unique: 2
	 2021-11-06 00:00:00 total: 4 unique: 3
	 2021-11-07 00:00:00 total: 1 unique: 1
	 Referrers:
		Count: 15 Unique: 2 Url: github.com
		Count: 13 Unique: 6 Url: vim.org
		Count: 1 Unique: 1 Url: DuckDuckGo

repo: gitblame views: total: 66 unique:  20
Views:
	 2021-10-24 00:00:00 total: 24 unique: 5
	 2021-10-25 00:00:00 total: 7 unique: 2
	 2021-10-26 00:00:00 total: 8 unique: 4
	 2021-10-27 00:00:00 total: 6 unique: 2
	 2021-10-28 00:00:00 total: 7 unique: 3
	 2021-10-29 00:00:00 total: 1 unique: 1
	 2021-10-30 00:00:00 total: 2 unique: 1
	 2021-10-31 00:00:00 total: 4 unique: 2
	 2021-11-01 00:00:00 total: 1 unique: 1
	 2021-11-03 00:00:00 total: 2 unique: 1
	 2021-11-04 00:00:00 total: 2 unique: 2
	 2021-11-05 00:00:00 total: 1 unique: 1
	 2021-11-06 00:00:00 total: 1 unique: 1
	 Referrers:
		Count: 16 Unique: 10 Url: vim.org
		Count: 3 Unique: 2 Url: github.com

repo: subb views: total: 46 unique:  3
Views:
	 2021-11-01 00:00:00 total: 43 unique: 3
	 2021-11-02 00:00:00 total: 1 unique: 1
	 2021-11-05 00:00:00 total: 2 unique: 1
	 Referrers:
		Count: 20 Unique: 2 Url: github.com
		Count: 6 Unique: 1 Url: pypi.org

repo: flagged-hn views: total: 40 unique:  5
Views:
	 2021-11-04 00:00:00 total: 21 unique: 2
	 2021-11-05 00:00:00 total: 16 unique: 5
	 2021-11-07 00:00:00 total: 3 unique: 1
	 Referrers:
		Count: 18 Unique: 3 Url: news.ycombinator.com
		Count: 11 Unique: 2 Url: github.com

repo: vimcrypt views: total: 28 unique:  6
Views:
	 2021-10-29 00:00:00 total: 15 unique: 4
	 2021-10-30 00:00:00 total: 3 unique: 2
	 2021-10-31 00:00:00 total: 6 unique: 2
	 2021-11-01 00:00:00 total: 2 unique: 1
	 2021-11-06 00:00:00 total: 1 unique: 1
	 2021-11-07 00:00:00 total: 1 unique: 1
	 Referrers:
		Count: 2 Unique: 1 Url: github.com

repo: kind-helper views: total: 25 unique:  3
Views:
	 2021-10-25 00:00:00 total: 19 unique: 2
	 2021-10-27 00:00:00 total: 4 unique: 1
	 2021-11-05 00:00:00 total: 2 unique: 1
	 Referrers:
		Count: 10 Unique: 1 Url: hn.algolia.com
		Count: 7 Unique: 2 Url: github.com

repo: kwchecker views: total: 24 unique:  3
Views:
	 2021-11-03 00:00:00 total: 24 unique: 3
	 Referrers:
		Count: 13 Unique: 3 Url: github.com
		Count: 3 Unique: 1 Url: pypi.org

repo: my-notes views: total: 18 unique:  4
Views:
	 2021-10-25 00:00:00 total: 3 unique: 2
	 2021-10-28 00:00:00 total: 1 unique: 1
	 2021-10-29 00:00:00 total: 2 unique: 1
	 2021-11-03 00:00:00 total: 4 unique: 3
	 2021-11-06 00:00:00 total: 8 unique: 2
	 Referrers:
		Count: 7 Unique: 3 Url: github.com

repo: pygamewrap views: total: 18 unique:  5
Views:
	 2021-10-28 00:00:00 total: 2 unique: 1
	 2021-10-31 00:00:00 total: 2 unique: 1
	 2021-11-02 00:00:00 total: 10 unique: 1
	 2021-11-03 00:00:00 total: 2 unique: 1
	 2021-11-05 00:00:00 total: 1 unique: 1
	 2021-11-06 00:00:00 total: 1 unique: 1
	 Referrers:
		Count: 3 Unique: 1 Url: github.com
		Count: 1 Unique: 1 Url: reddit.com

repo: githubapitools views: total: 17 unique:  7
Views:
	 2021-10-27 00:00:00 total: 2 unique: 1
	 2021-10-28 00:00:00 total: 1 unique: 1
	 2021-10-31 00:00:00 total: 1 unique: 1
	 2021-11-03 00:00:00 total: 10 unique: 5
	 2021-11-04 00:00:00 total: 2 unique: 1
	 2021-11-05 00:00:00 total: 1 unique: 1
	 Referrers:
		Count: 10 Unique: 6 Url: news.ycombinator.com
		Count: 3 Unique: 2 Url: github.com

repo: s9k views: total: 12 unique:  4
Views:
	 2021-10-25 00:00:00 total: 5 unique: 1
	 2021-11-03 00:00:00 total: 1 unique: 1
	 2021-11-04 00:00:00 total: 3 unique: 1
	 2021-11-05 00:00:00 total: 1 unique: 1
	 2021-11-06 00:00:00 total: 2 unique: 2
	 Referrers:
		Count: 5 Unique: 1 Url: github.com
		Count: 3 Unique: 1 Url: Google

repo: myenv views: total: 11 unique:  6
Views:
	 2021-10-24 00:00:00 total: 4 unique: 1
	 2021-10-26 00:00:00 total: 1 unique: 1
	 2021-10-28 00:00:00 total: 2 unique: 1
	 2021-10-29 00:00:00 total: 2 unique: 1
	 2021-11-05 00:00:00 total: 1 unique: 1
	 2021-11-07 00:00:00 total: 1 unique: 1
	 Referrers:
		Count: 2 Unique: 2 Url: github.com

repo: opinionated-fortune-cow views: total: 11 unique:  1
Views:
	 2021-10-24 00:00:00 total: 7 unique: 1
	 2021-10-25 00:00:00 total: 3 unique: 1
	 2021-10-29 00:00:00 total: 1 unique: 1

repo: cppcombinator views: total: 10 unique:  9
Views:
	 2021-10-27 00:00:00 total: 1 unique: 1
	 2021-10-28 00:00:00 total: 1 unique: 1
	 2021-10-29 00:00:00 total: 1 unique: 1
	 2021-10-31 00:00:00 total: 1 unique: 1
	 2021-11-01 00:00:00 total: 2 unique: 1
	 2021-11-02 00:00:00 total: 1 unique: 1
	 2021-11-03 00:00:00 total: 1 unique: 1
	 2021-11-06 00:00:00 total: 1 unique: 1
	 2021-11-07 00:00:00 total: 1 unique: 1
	 Referrers:
		Count: 5 Unique: 4 Url: github.com

repo: cstuff views: total: 10 unique:  4
Views:
	 2021-10-27 00:00:00 total: 2 unique: 2
	 2021-10-31 00:00:00 total: 7 unique: 1
	 2021-11-04 00:00:00 total: 1 unique: 1
	 Referrers:
		Count: 1 Unique: 1 Url: github.com

repo: printb views: total: 10 unique:  1
Views:
	 2021-10-25 00:00:00 total: 7 unique: 1
	 2021-10-28 00:00:00 total: 1 unique: 1
	 2021-11-04 00:00:00 total: 2 unique: 1

repo: zipit views: total: 8 unique:  6
Views:
	 2021-10-24 00:00:00 total: 3 unique: 1
	 2021-10-28 00:00:00 total: 3 unique: 3
	 2021-11-06 00:00:00 total: 2 unique: 2

repo: roget-thesaurus-parser views: total: 7 unique:  1
Views:
	 2021-10-27 00:00:00 total: 7 unique: 1

repo: pprintex views: total: 6 unique:  4
Views:
	 2021-10-27 00:00:00 total: 2 unique: 1
	 2021-10-28 00:00:00 total: 1 unique: 1
	 2021-11-03 00:00:00 total: 2 unique: 1
	 2021-11-05 00:00:00 total: 1 unique: 1

repo: pythonimportplayground views: total: 6 unique:  3
Views:
	 2021-10-28 00:00:00 total: 1 unique: 1
	 2021-10-31 00:00:00 total: 4 unique: 1
	 2021-11-04 00:00:00 total: 1 unique: 1
	 Referrers:
		Count: 4 Unique: 1 Url: github.com
		Count: 1 Unique: 1 Url: reddit.com

repo: jq-illustrated views: total: 5 unique:  2
Views:
	 2021-10-30 00:00:00 total: 2 unique: 1
	 2021-11-01 00:00:00 total: 2 unique: 1
	 2021-11-04 00:00:00 total: 1 unique: 1
	 Referrers:
		Count: 3 Unique: 2 Url: github.com

repo: ls-annotations views: total: 5 unique:  1
Views:
	 2021-10-25 00:00:00 total: 5 unique: 1
	 Referrers:
		Count: 2 Unique: 1 Url: Google

repo: grpc-spring-boot-starter-utils views: total: 4 unique:  2
Views:
	 2021-10-25 00:00:00 total: 3 unique: 1
	 2021-10-28 00:00:00 total: 1 unique: 1
	 Referrers:
		Count: 2 Unique: 1 Url: github.com

repo: pythoncourse views: total: 4 unique:  1
Views:
	 2021-10-25 00:00:00 total: 4 unique: 1
	 Referrers:
		Count: 4 Unique: 1 Url: github.com

repo: follow-kube-logs views: total: 3 unique:  1
Views:
	 2021-10-31 00:00:00 total: 3 unique: 1
	 Referrers:
		Count: 2 Unique: 1 Url: github.com

repo: visual-python-strace views: total: 2 unique:  2
Views:
	 2021-11-06 00:00:00 total: 1 unique: 1
	 2021-11-07 00:00:00 total: 1 unique: 1

repo: duckduckbang views: total: 1 unique:  1
Views:
	 2021-10-31 00:00:00 total: 1 unique: 1
	 Referrers:
		Count: 1 Unique: 1 Url: DuckDuckGo

repo: github_pr_comments views: total: 1 unique:  1
Views:
	 2021-11-01 00:00:00 total: 1 unique: 1
	 Referrers:
		Count: 1 Unique: 1 Url: github.com

repo: bloxroutehomework views: total: 0 unique:  0

repo: k8explain views: total: 0 unique:  0

repo: microsofthomework views: total: 0 unique:  0

repo: scriptrunner-operator views: total: 0 unique:  0


***
Total views: 478

```
# Installation

You need to install the following packages:

- ```pip3 install PyGithub```
- ```pip3 install websocket-client``` 

or install via requirements.txt file

```pip3 install -r requirements.txt```

