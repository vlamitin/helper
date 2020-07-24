import json

import requests
import os
from pprint import pprint
from requests.auth import HTTPBasicAuth
from datetime import timedelta, datetime


# https://docs.atlassian.com/software/jira/docs/api/REST/7.3.3/#api/2/issue
def get_worklogs(jira_domain, jira_login, jira_token, task_key):
    res = requests.get(
        f"{jira_domain}/rest/api/2/issue/{task_key}/worklog",
        auth=HTTPBasicAuth(jira_login, jira_token),
    )
    return res.json()['worklogs']


# does not work
# https://stackoverflow.com/questions/12776109/how-to-get-all-work-logs-for-a-period-of-time-from-the-jira-rest-api
# since in dd.mm.yyyy format
def get_worklogs_since(jira_domain, jira_login, jira_token, since):
    updated_ids_res = requests.get(
        f"{jira_domain}/rest/api/2/worklog/updated",
        auth=HTTPBasicAuth(jira_login, jira_token),
        params={'since': _date_string_to_timestamp(since)}
    )
    updated_ids = [x['worklogId'] for x in updated_ids_res.json()['values']]

    worklogs_res = requests.post(
        f"{jira_domain}/rest/api/2/worklog/list",
        auth=HTTPBasicAuth(jira_login, jira_token),
        data=json.dumps({'ids': updated_ids})
    )

    if worklogs_res.text:
        return worklogs_res.json()


def _date_string_to_timestamp(date_string):
    date = datetime.strptime(date_string, '%d.%m.%Y')
    # in ms
    return int(datetime.timestamp(date)) * 1000


def to_worklogs_dict(worklogs):
    result_dict = {}

    for item in worklogs:
        if item['author']['displayName'] in result_dict:
            result_dict[item['author']['displayName']] += item['timeSpentSeconds']
        else:
            result_dict[item['author']['displayName']] = item['timeSpentSeconds']

    return dict(
        [
            (
                x,
                str(timedelta(seconds=result_dict[x]))
            )
            for x in result_dict
        ]
    )


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
