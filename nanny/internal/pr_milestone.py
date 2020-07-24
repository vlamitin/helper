import requests
import os
from pprint import pprint
from requests.auth import HTTPBasicAuth

import settings


def get_milestones(gh_login, gh_token, repo_org, repo_name):
    res = requests.get(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/milestones",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    return res.json()


def to_brief_milestones(milestones):
    return [
        {
            'closed_issues': x['closed_issues'],
            'open_issues': x['open_issues'],
            'number': x['number'],
            'title': x['title'],
            'state': x['state'],
        }
        for x in milestones
    ]


def brief_milestone_and_base_branch_name_by_head_branch(head_branch_name, brief_milestones):
    branch_milestone_title = settings.to_milestone_title(head_branch_name)

    result_milestone = None
    result_base_branch = None

    sorted_mstones = sorted(brief_milestones, key=lambda mstone: mstone['title'], reverse=True)

    if branch_milestone_title:
        matching_milestones = [x for x in brief_milestones if x['title'] == branch_milestone_title]
        if len(matching_milestones) == 1:
            result_milestone = matching_milestones[0]
            if matching_milestones[0]['title'] == sorted_mstones[0]['title']:
                result_base_branch = 'master'
            else:
                result_base_branch = settings.to_release_branch_name(settings.to_version(head_branch_name))
    else:
        if sorted_mstones[0]['title'][-1] == '0':
            result_milestone = sorted_mstones[0]
            result_base_branch = 'master'

    return result_milestone, result_base_branch


if __name__ == '__main__':
    print("script: setting creds from envs ...")
    try:
        GH_LOGIN = os.environ['PR_HELPER_GH_LOGIN']
        GH_TOKEN = os.environ['PR_HELPER_GH_TOKEN']
    except KeyError:
        print("script: (!) no envs set, exiting")
        quit(0)

    pprint("TODO debug")
