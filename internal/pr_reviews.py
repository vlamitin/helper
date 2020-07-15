import json
import os
import requests
from pprint import pprint
from requests.auth import HTTPBasicAuth


def request_pr_reviews(gh_login, gh_token, repo_org, repo_name,
                       pr_number, reviewers):
    res = requests.post(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/pulls/{pr_number}/requested_reviewers",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'},
        data=json.dumps({'reviewers': reviewers})
    )
    return res.json()


def _list_pr_reviews(gh_login, gh_token, repo_org, repo_name, pr_number):
    res = requests.get(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/pulls/{pr_number}/reviews",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    return res.json()


def _list_pr_review_requests(gh_login, gh_token, repo_org, repo_name, pr_number):
    res = requests.get(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/pulls/{pr_number}/requested_reviewers",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    return res.json()


def _get_pr_reviews_status(gh_login, gh_token, repo_org, repo_name, pr_number, pr_creator_login):
    rv_requests = _list_pr_review_requests(gh_login, gh_token, repo_org, repo_name, pr_number)
    rvs = _list_pr_reviews(gh_login, gh_token, repo_org, repo_name, pr_number)

    result = {
        'approved': True,
        'reviewers': {}
    }

    for rv in rvs:
        if rv['user']['login'] == pr_creator_login:
            continue

        rv_result = {
            'state': rv['state'],
            'submitted_at': rv['submitted_at']
        }

        if rv['user']['login'] not in result['reviewers']:
            result['reviewers'][rv['user']['login']] = [rv_result]
        else:
            result['reviewers'][rv['user']['login']].append(rv_result)

    for rv_rq_user in rv_requests['users']:
        if rv_rq_user['login'] == pr_creator_login:
            continue

        if rv_rq_user['login'] not in result['reviewers']:
            result['reviewers'][rv_rq_user['login']] = [{
                'state': 'REQUESTED'
            }]

    if len(result['reviewers']) == 0:
        result['approved'] = False

    for reviewer in result['reviewers']:
        approved = False

        # reviews are sorted by submitted_at
        for rv_result in result['reviewers'][reviewer]:
            if rv_result['state'] == 'APPROVED':
                approved = True
            elif rv_result['state'] == 'CHANGES_REQUESTED':
                approved = False

        if not approved:
            result['approved'] = False

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
