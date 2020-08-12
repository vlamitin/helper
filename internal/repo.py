import requests
from pprint import pprint
from requests.auth import HTTPBasicAuth


def check_collaborator(
        gh_login, gh_token, repo_org, repo_name,
        username
):
    res = requests.get(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/collaborators/{username}",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'},
    )
    if res.status_code == 204:
        return True

    if res.status_code == 404:
        return False

    return None


if __name__ == '__main__':
    pprint("TODO debug")
