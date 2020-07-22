import json
import math
import re

import requests
import os
from pprint import pprint
from requests.auth import HTTPBasicAuth
from datetime import datetime


# https://docs.atlassian.com/software/jira/docs/api/REST/7.3.3/#api/2/issue
def get_worklogs(jira_domain, jira_login, jira_token, task_key):
    res = requests.get(
        f"{jira_domain}/rest/api/2/issue/{task_key}/worklog",
        auth=HTTPBasicAuth(jira_login, jira_token),
    )
    return res.json()['worklogs']


def add_worklog(jira_domain, jira_login, jira_token, task_key, time_spent_seconds):
    res = requests.post(
        f"{jira_domain}/rest/api/3/issue/{task_key}/worklog",
        auth=HTTPBasicAuth(jira_login, jira_token),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            'started': datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '.094+0300',
            'timeSpentSeconds': time_spent_seconds
        })
    )
    return res.json()


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
            result_dict[item['author']['displayName']]['timeSpentSeconds'] += item['timeSpentSeconds']
            result_dict[item['author']['displayName']]['timeSpent_h']\
                = to_human_readable_jira_period(result_dict[item['author']['displayName']]['timeSpentSeconds'])
        else:
            result_dict[item['author']['displayName']] = {
                'timeSpentSeconds': item['timeSpentSeconds'],
                'timeSpent_h': to_human_readable_jira_period(item['timeSpentSeconds']),
            }

    return result_dict


def to_human_readable_jira_period(jira_seconds):
    if not jira_seconds:
        return "0s"

    result = ""

    minute_in_seconds = 60
    hour_in_seconds = minute_in_seconds * 60
    day_in_seconds = hour_in_seconds * 8  # work day

    days = 0
    hours = 0
    minutes = 0

    days += math.floor(jira_seconds / day_in_seconds)
    jira_seconds -= days * day_in_seconds
    if days:
        result += f"{days}d"

    hours += math.floor(jira_seconds / hour_in_seconds)
    jira_seconds -= hours * hour_in_seconds
    if hours:
        if result:
            result += " "
        result += f"{hours}h"

    minutes += math.floor(jira_seconds / minute_in_seconds)
    jira_seconds -= minutes * minute_in_seconds
    if minutes:
        if result:
            result += " "
        result += f"{minutes}m"

    if jira_seconds:
        if result:
            result += " "
        result += f"{jira_seconds}s"

    return result


def to_jira_seconds(jira_period_pieces):
    result = 0

    minute_in_seconds = 60
    hour_in_seconds = minute_in_seconds * 60
    day_in_seconds = hour_in_seconds * 8  # work day

    for period_piece in jira_period_pieces:
        value = int(re.compile(r"(\d+)").match(period_piece).group())
        if "d" in period_piece:
            result += value * day_in_seconds
        elif "h" in period_piece:
            result += value * hour_in_seconds
        elif "m" in period_piece:
            result += value * minute_in_seconds

    return result


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
    # print("676800", to_human_readable_jira_period(676800))
    # print("14400 (4h)", to_human_readable_jira_period(14400))
    # print("115200 (4d)", to_human_readable_jira_period(115200))
    # print("23d 4h (676800)", to_jira_seconds(["23d", "4h"]))
    # print("4d (115200)", to_jira_seconds(["4d"]))
