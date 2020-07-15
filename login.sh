#!/bin/bash
echo "enter connection string (<gh_login>@@@@@<gh_token>@@@@@<jira_domain>@@@@@<jira_login>@@@@@<jira_token>): "; read -s IN; \
export PR_HELPER_GH_LOGIN=$(echo $IN | awk -F '@@@@@' '{print $1}'); \
export PR_HELPER_GH_TOKEN=$(echo $IN | awk -F '@@@@@' '{print $2}'); \
export PR_HELPER_JIRA_DOMAIN=$(echo $IN | awk -F '@@@@@' '{print $3}'); \
export PR_HELPER_JIRA_LOGIN=$(echo $IN | awk -F '@@@@@' '{print $4}'); \
export PR_HELPER_JIRA_TOKEN=$(echo $IN | awk -F '@@@@@' '{print $5}'); \
([[ -z $PR_HELPER_GH_LOGIN ]] \
  || [[ -z $PR_HELPER_GH_TOKEN ]] \
  || [[ -z $PR_HELPER_JIRA_DOMAIN ]] \
  || [[ -z $PR_HELPER_JIRA_LOGIN ]] \
  || [[ -z $PR_HELPER_JIRA_TOKEN ]]) && echo "(!) failed to parse pr-helper connection string"
