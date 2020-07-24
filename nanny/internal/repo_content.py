import base64
import requests
from requests.auth import HTTPBasicAuth


def get_file_content(gh_login, gh_token, repo_org, repo_name,
                     file_path):
    return base64.b64decode(_get_file(gh_login, gh_token, repo_org, repo_name,
                                      file_path)['content']).decode('utf-8')


def _get_file(gh_login, gh_token, repo_org, repo_name, file_path):
    res = requests.get(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/contents/{file_path}",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    return res.json()
