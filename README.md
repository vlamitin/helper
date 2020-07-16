# Helper
scripts to ease work with github, jira, jenkins

## TODO (currently linux only)

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
