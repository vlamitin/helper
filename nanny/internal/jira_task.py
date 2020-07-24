import requests
import os
from pprint import pprint
from requests.auth import HTTPBasicAuth


# https://docs.atlassian.com/software/jira/docs/api/REST/7.3.3/#api/2/issue
from internal.jira_worklog import to_worklogs_dict


def get_jira_task(jira_domain, jira_login, jira_token, task_key):
    res = requests.get(
        f"{jira_domain}/rest/api/2/issue/{task_key}",
        auth=HTTPBasicAuth(jira_login, jira_token),
    )
    return res.json()


def _to_brief_jira_task(jira_task):
    return {
        'key': jira_task['key'],
        'summary': jira_task['fields']['summary'],
        'assignee': jira_task['fields']['assignee'] and jira_task['fields']['assignee']['displayName'],
        'fixVersions': [x['name'] for x in jira_task['fields']['fixVersions']],
        'status': jira_task['fields']['status']['name'],
        'worklogs': to_worklogs_dict(jira_task['fields']['worklog']['worklogs']),
    }


if __name__ == '__main__':
    print("script: setting creds from envs ...")
    try:
        JIRA_DOMAIN = os.environ['PR_HELPER_JIRA_DOMAIN']
        JIRA_LOGIN = os.environ['PR_HELPER_JIRA_LOGIN']
        JIRA_TOKEN = os.environ['PR_HELPER_JIRA_TOKEN']
    except KeyError:
        print("script: (!) no envs set, exiting")
        quit(0)

    pprint("TODO debug")
