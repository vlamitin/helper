import requests
import os
from pprint import pprint
from requests.auth import HTTPBasicAuth


# https://docs.atlassian.com/software/jira/docs/api/REST/7.3.3/#api/2/issue
from internal.jira_worklog import to_worklogs_dict, to_human_readable_jira_period


def get_jira_task(jira_domain, jira_login, jira_token, task_key):
    res = requests.get(
        f"{jira_domain}/rest/api/2/issue/{task_key}",
        auth=HTTPBasicAuth(jira_login, jira_token),
    )
    return res.json()


def get_children_tasks(jira_domain, jira_login, jira_token, task_key):
    res = requests.get(
        f"{jira_domain}/rest/api/2/search?jql=parent%20%3D%20{task_key}%20ORDER%20BY%20priority%20DESC",
        auth=HTTPBasicAuth(jira_login, jira_token),
    )
    return res.json()['issues']


def get_tasks_for_epic(jira_domain, jira_login, jira_token, epic_key):
    res = requests.get(
        f"{jira_domain}/rest/api/2/search?jql=cf%5B11000%5D%3D{epic_key}%20ORDER%20BY%20priority%20DESC",
        auth=HTTPBasicAuth(jira_login, jira_token),
    )
    return res.json()['issues']


def _to_brief_jira_task(jira_task):
    return {
        'key': jira_task['key'],
        'summary': jira_task['fields']['summary'],
        'creator': jira_task['fields']['creator'] and jira_task['fields']['creator']['displayName'],
        'assignee': jira_task['fields']['assignee'] and jira_task['fields']['assignee']['displayName'],
        'fixVersions': [x['name'] for x in jira_task['fields']['fixVersions']],
        'affectedVersions': jira_task['fields']['versions']
                            and [x['name'] for x in jira_task['fields']['versions']]
                            or [],
        'status': jira_task['fields']['status']['name'],
        'worklogs': 'worklog' in jira_task['fields']
                    and to_worklogs_dict(jira_task['fields']['worklog']['worklogs'])
                    or [],
        'timeoriginalestimate': jira_task['fields']['timeoriginalestimate'],
        'timeoriginalestimate_h': to_human_readable_jira_period(jira_task['fields']['timeoriginalestimate']),
        'timespent': jira_task['fields']['timespent'],
        'timespent_h': to_human_readable_jira_period(jira_task['fields']['timespent']),
    }


# parent_task can be epic or just task with subtasks
def get_brief_tasks_tree(jira_domain, jira_login, jira_token, root_task):
    epic_subtasks = get_tasks_for_epic(jira_domain, jira_login, jira_token, root_task['key'])
    subtasks = []

    if len(epic_subtasks) > 0:
        subtasks = epic_subtasks
    else:
        subtasks = get_children_tasks(jira_domain, jira_login, jira_token, root_task['key'])

    children = [get_brief_tasks_tree(jira_domain, jira_login, jira_token, x) for x in subtasks]
    sum_estimate = (sum([x['sum_estimate'] or 0 for x in children]) or 0) + \
                   (root_task['fields']['timeoriginalestimate'] or 0)
    return {
        'is_epic': len(epic_subtasks) > 0,
        'children': children,
        'sum_estimate': sum_estimate,
        'sum_estimate_h': to_human_readable_jira_period(sum_estimate),
        **_to_brief_jira_task(root_task)
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
