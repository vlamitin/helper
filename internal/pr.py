import json
import os
import requests
from pprint import pprint
from requests.auth import HTTPBasicAuth

from internal.pr_build_statuses import get_blocking_builds, list_pr_build_statuses
from internal.pr_reviews import _get_pr_reviews_status


def list_prs(gh_login, gh_token, repo_org, repo_name, base):
    res = requests.get(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/pulls",
        params={'base': base},
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    return res.json()


def list_open_prs(gh_login, gh_token, repo_org, repo_name):
    res = requests.get(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/pulls",
        params={'per_page': 100},
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    return res.json()

# returns some kind of short version of pr-s
# def list_open_prs(gh_login, gh_token, repo_org, repo_name):
#     res = requests.get(
#         f"https://api.github.com/search/issues?q=is:open%20is:pr%20repo:{repo_org}/{repo_name}&per_page=100",
#         auth=HTTPBasicAuth(gh_login, gh_token),
#         headers={'Accept': 'application/vnd.github.v3+json'}
#     )
#     return res.json()['items']


# https://docs.github.com/en/github/searching-for-information-on-github/searching-issues-and-pull-requests#search-within-a-users-or-organizations-repositories
def get_user_created_prs(gh_login, gh_token, username):
    res = requests.get(
        f"https://api.github.com/search/issues?q=is:open%20is:pr%20author:{username}%20archived:false",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    return res.json()['items']


def get_open_prs_for_jira_key(gh_login, gh_token, jira_key):
    res = requests.get(
        f"https://api.github.com/search/issues?q=is:open%20is:pr%20{jira_key}%20in:title%20archived:false",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    return res.json()['items']


def get_closed_prs_for_jira_key(gh_login, gh_token, jira_key):
    res = requests.get(
        f"https://api.github.com/search/issues?q=is:closed%20is:pr%20{jira_key}%20in:title%20archived:false",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    return res.json()['items']


def get_user_request_reviews(gh_login, gh_token,
                             username):
    res = requests.get(
        f"https://api.github.com/search/issues?q=is:open%20is:pr%20review-requested:{username}%20archived:false",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    return res.json()['items']


def get_pr_summary(gh_login, gh_token, repo_org, repo_name, pr_number):
    pr = get_pr(gh_login, gh_token, repo_org, repo_name, pr_number)

    return {
        **to_brief_pr(pr),
        'blocking_builds': get_blocking_builds(
            list_pr_build_statuses(gh_login, gh_token, pr['statuses_url'])
        ),
        'review_statuses': _get_pr_reviews_status(
            gh_login, gh_token, repo_org, repo_name, pr_number, pr['user']['login']
        )
    }


def create_pr(
        gh_login, gh_token, repo_org, repo_name,
        title, body,
        head_branch, base_branch
):
    res = requests.post(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/pulls",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'},
        data=json.dumps({'title': title, 'body': body, 'head': head_branch, 'base': base_branch})
    )
    return res.json()


def update_pr(
        gh_login, gh_token, repo_org, repo_name,
        pr_number, milestone_number, labels,
):
    request_data = {'labels': labels}
    if milestone_number:
        request_data['milestone'] = milestone_number

    res = requests.patch(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/issues/{pr_number}",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'},
        data=json.dumps(request_data)
    )
    return res.json()


def get_pr(gh_login, gh_token, repo_org, repo_name, pr_number):
    res = requests.get(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/pulls/{pr_number}",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    return res.json()


def to_brief_pr(pr):
    return {
        'user_login': pr['user']['login'],
        'title': pr['title'],
        'updated_at': pr['updated_at'],
        'state': pr['state'],
        'number': pr['number'],
        'milestone': pr['milestone'] and {
            'number': pr['milestone']['number'],
            'state': pr['milestone']['state'],
            'title': pr['milestone']['title']
        },
        'locked': pr['locked'],
        'labels': pr['labels'] and [lbl['name'] for lbl in pr['labels']],
        'head_ref': pr['head']['ref'],
        'base': pr['base']['ref'],
        'comments_url': pr['comments_url'],
        'commits_url': pr['commits_url'],
        'created_at': pr['created_at'],
    }


if __name__ == '__main__':
    print("script: setting creds from envs ...")
    try:
        GH_LOGIN = os.environ['PR_HELPER_GH_LOGIN']
        GH_TOKEN = os.environ['PR_HELPER_GH_TOKEN']
    except KeyError:
        print("script: (!) no envs set, exiting")
        quit(0)

    pprint("TODO debug")
