import requests
import os
from pprint import pprint
from requests.auth import HTTPBasicAuth


def get_branch(gh_login, gh_token, repo_org, repo_name, branch_name):
    res = requests.get(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/branches/{branch_name}",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    return res.json()


def check_branch_exists(gh_login, gh_token, repo_org, repo_name, branch_name):
    checked_branch_response = get_branch(gh_login, gh_token, repo_org, repo_name, branch_name)
    if 'message' in checked_branch_response and checked_branch_response['message'] == 'Branch not found':
        return False
    else:
        return True


if __name__ == '__main__':
    print("script: setting creds from envs ...")
    try:
        GH_LOGIN = os.environ['PR_HELPER_GH_LOGIN']
        GH_TOKEN = os.environ['PR_HELPER_GH_TOKEN']
    except KeyError:
        print("script: (!) no envs set, exiting")
        quit(0)

    pprint("TODO debug")
