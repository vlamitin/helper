import requests
import os
import json
from pprint import pprint
from requests.auth import HTTPBasicAuth


def get_issue_comments(gh_login, gh_token, repo_org, repo_name, pr_number):
    res = requests.get(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/issues/{pr_number}/comments",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    return res.json()


def create_issue_comment(gh_login, gh_token, repo_org, repo_name, pr_number, comment):
    res = requests.post(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/issues/{pr_number}/comments",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'},
        data=json.dumps({'body': comment})
    )
    return res.json()


if __name__ == '__main__':
    print("script: setting creds from envs ...")
    try:
        GH_LOGIN = os.environ['PR_HELPER_GH_LOGIN']
        GH_TOKEN = os.environ['PR_HELPER_GH_TOKEN']
    except KeyError:
        print("script: (!) no envs set, exiting")
        quit(0)

    pprint("TODO debug")
