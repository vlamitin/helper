import os
import requests
from pprint import pprint
from requests.auth import HTTPBasicAuth

import settings


def list_pr_build_statuses(gh_login, gh_token, link):
    res = requests.get(
        link,
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    return res.json()


def to_brief_build_statuses(build_statuses):
    return [{
        'context': x['context'],
        'created_at': x['created_at'],
        'description': x['description'],
        'id': x['id'],
        'state': x['state'],
        'updated_at': x['updated_at'],
    } for x in build_statuses]


def get_blocking_builds(build_statuses):
    result = []

    statuses_dict = {}
    for context in settings.all_build_contexts:
        statuses_dict[context] = []

    # build_statuses should be sorted by updated_at in reverse order
    for build_status in build_statuses:
        statuses_dict[build_status['context']].append(build_status)

    for status_context in statuses_dict:
        if len(statuses_dict[status_context]) == 0:
            result.append({
                'build_context': status_context,
                'reason': 'BUILD NOT STARTED'
            })
        elif statuses_dict[status_context][0]['state'] != 'success':
            result.append({
                'build_context': status_context,
                'reason': f"LAST BUILD STATE: {statuses_dict[status_context][0]['state']}"
            })

    return result


if __name__ == '__main__':
    print("script: setting creds from envs ...")
    try:
        GH_LOGIN = os.environ['PR_HELPER_GH_LOGIN']
        GH_TOKEN = os.environ['PR_HELPER_GH_TOKEN']
    except KeyError:
        print("script: (!) no envs set, exiting")
        quit(0)

    pprint("TODO debug")
