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
    print('DEBUG')
