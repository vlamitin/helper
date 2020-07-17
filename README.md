# Helper
scripts to ease work with github, jira, jenkins

## TODO (currently linux only)

## Features
- create PR with all that milestones, labels, title, body, links to jira, reviewers, etc from command line
- open all review requested PRs in browser
- list jira tasks tree with brief info
- update all outdated prs at once
- merge all your prs at local branch

## Prerequisites
- linux
- bash
- make
- python 3
- [get jira token](https://id.atlassian.com/manage-profile/security/api-tokens)
- [get github token](https://github.com/settings/tokens) (with scope 'repo')

## install
- `cp settings_global.py settings_user.py`
- fill settings_user.py
- `make install` - installs virtualenv and all dependencies (locally), creates /home/$USER/bin/helper script

## usage
- `source login.sh` (once per terminal session, to set tokens)
- `helper -h`
