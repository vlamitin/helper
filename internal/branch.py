import requests
import os
from pprint import pprint
from requests.auth import HTTPBasicAuth

import settings


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


def get_latest_release(gh_login, gh_token, repo_org, repo_name):
    res = requests.get(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/releases/latest",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    return res.json()


def check_tag_exists(gh_login, gh_token, repo_org, repo_name, tag_name):
    res = requests.get(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/readme?ref={tag_name}",
        auth=HTTPBasicAuth(gh_login, gh_token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    readme_res = res.json()
    if 'message' in readme_res and 'No commit found for the ref' in readme_res['message']:
        return False
    else:
        return True


def find_active_patch_branch_name(gh_login, gh_token, repo_org, repo_name, version):
    while check_tag_exists(gh_login, gh_token, repo_org, repo_name, settings.to_release_tag(version)):
        version = settings.next_patch(version)

    if check_branch_exists(gh_login, gh_token, repo_org, repo_name, settings.to_release_branch_name(version)):
        return settings.to_release_branch_name(version)

    return None


def get_closest_unreleased_minor(gh_login, gh_token, repo_org, repo_name):
    version = settings.tag_to_version(
        get_latest_release(gh_login, gh_token, repo_org, repo_name)['tag_name']
    )

    while check_tag_exists(gh_login, gh_token, repo_org, repo_name, settings.to_release_tag(version)):
        version = settings.next_minor(version)

    return version


def check_code_freeze(gh_login, gh_token, repo_org, repo_name):
    unreleased_minor = get_closest_unreleased_minor(gh_login, gh_token, repo_org, repo_name)
    return check_branch_exists(
        gh_login, gh_token, repo_org, repo_name, settings.to_release_branch_name(unreleased_minor)
    )


if __name__ == '__main__':
    print("script: setting creds from envs ...")
    try:
        GH_LOGIN = os.environ['PR_HELPER_GH_LOGIN']
        GH_TOKEN = os.environ['PR_HELPER_GH_TOKEN']
    except KeyError:
        print("script: (!) no envs set, exiting")
        quit(0)

    pprint("TODO debug")
    # pprint(get_closest_unreleased_minor(GH_LOGIN, GH_TOKEN, settings.REPO_ORG, settings.REPO_NAME))
    # pprint(check_code_freeze(GH_LOGIN, GH_TOKEN, settings.REPO_ORG, settings.REPO_NAME))
