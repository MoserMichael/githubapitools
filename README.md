
# githubtools

Some programs that make use of the [python github api](https://pygithub.readthedocs.io/en/latest/reference.html)


help text for makepr.py

```
This program does the following steps:

- creates a feature branch, and pushes the branch.
- opens a pull request, it is assumed that a continuous integration build is then triggered.
- the program then waits that the continuous integration build for that PR has completed.
- At the end of the build, a sound is played, and the url with the build log is written to standard output.

This program allows you to do some swordfighting, while the PR build is going on ;-(

This program assumes that the environment GITHUB_TOKEN is exported, and that it has the token of the current user.
This program assumes the github api to be installed - pip install python-github-api
```

help text for starcounter.py

```
shows number of star of project owned by current github user
It also compares the number of stars against the previous state, and reports any difference. The new state is then stored in the starcounter.data file.

This program assumes that the environment GITHUB_TOKEN is exported, and that it has the token of the current user.
This program assumes the github api to be installed - pip install python-github-api
```

