import requests
import os
from pprint import pprint
from requests.auth import HTTPBasicAuth


def get_labels(gh_login, gh_token, repo_org, repo_name):
    res = requests.get(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/labels",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    return res.json()


def _to_brief_labels(labels):
    return [x['name'] for x in labels]


if __name__ == '__main__':
    print("script: setting creds from envs ...")
    try:
        GH_LOGIN = os.environ['PR_HELPER_GH_LOGIN']
        GH_TOKEN = os.environ['PR_HELPER_GH_TOKEN']
    except KeyError:
        print("script: (!) no envs set, exiting")
        quit(0)

    pprint("TODO debug")
