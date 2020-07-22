import os
from pprint import pprint

import requests
from requests.auth import HTTPBasicAuth


def list_pr_commits(gh_login, gh_token, repo_org, repo_name, pr_number):
    res = requests.get(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/pulls/{pr_number}/commits",
        params={'per_page': 100},
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
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
