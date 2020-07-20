import argparse
import os
import subprocess
from pprint import pprint

import settings
from internal.branch import check_tag_exists, get_closest_unreleased_minor, check_branch_exists
from internal.jira_task import get_jira_task, to_brief_jira_task
from internal.pr import list_prs

DESCRIPTION = 'Cherry-picks <n> commits from current branch in LOCAL_PROJECT_PATH to all current patches'


def add_arguments(arg_parser):
    arg_parser.add_argument('commits_count', nargs=1, type=int, help='commits count to cherry-pick')

    return arg_parser


def parse_args(args_dict):
    return {
        'commits_count': args_dict['commits_count'][0],
    }


def run_scenario(commits_count):
    print("script: setting creds from envs ...")
    try:
        GH_LOGIN = os.environ['PR_HELPER_GH_LOGIN']
        GH_TOKEN = os.environ['PR_HELPER_GH_TOKEN']
        JIRA_DOMAIN = os.environ['PR_HELPER_JIRA_DOMAIN']
        JIRA_LOGIN = os.environ['PR_HELPER_JIRA_LOGIN']
        JIRA_TOKEN = os.environ['PR_HELPER_JIRA_TOKEN']
    except KeyError:
        print("script: (!) no envs set, exiting")
        quit(0)

    git_log_output = subprocess.check_output(
        f"git -C {settings.LOCAL_PROJECT_PATH} log -{abs(commits_count)} --pretty=format:'%H'", shell=True
    )
    commit_hashes = git_log_output.decode('utf-8').split("\n")

    git_current_branch_name_output = subprocess.check_output(
        f"git -C {settings.LOCAL_PROJECT_PATH} rev-parse --abbrev-ref HEAD", shell=True
    )
    current_branch_name = git_current_branch_name_output.decode('utf-8').split("\n")[0]

    task_keys = settings.to_jira_task_keys(current_branch_name)
    jira_tasks = [get_jira_task(JIRA_DOMAIN, JIRA_LOGIN, JIRA_TOKEN, x) for x in task_keys]

    base_branches = get_base_brahches(GH_LOGIN, GH_TOKEN, jira_tasks)

    for jira_task in jira_tasks:
        brief_jt = to_brief_jira_task(jira_task)
        print(f"script: {brief_jt['key']} with affectedVersions {brief_jt['affectedVersions']} " +
              f"and fixVersions {brief_jt['fixVersions']} => to releases: {[x[1] for x in base_branches]}")

    continue_choice = input(
        "script: PRs with this ^ props will be created, press \"Enter\" to continue, \"q\" to quit ..."
    )
    if continue_choice in ["q", "Q"]:
        quit(0)

    project_path = settings.LOCAL_PROJECT_PATH
    os.system(f"git -C {project_path} fetch")

    for version, base_branch in base_branches:
        new_branch_name = settings.to_new_version_branch_name(current_branch_name, version)
        if check_branch_exists(GH_LOGIN, GH_TOKEN, settings.REPO_ORG, settings.REPO_NAME, new_branch_name):
            continue_choice = input(
                f"script: (!) branch {new_branch_name} " +
                f"already exists in remote; press \"Enter\" to skip this branch, \"q\" to quit ..."
            )
            if continue_choice in ["q", "Q"]:
                quit(0)
            else:
                continue

        print(f"script: checkouting {base_branch} ...")
        checkout_code = os.system(f"git -C {project_path} checkout origin/{base_branch}")
        if checkout_code != 0:
            print("script: (!) failed to checkout, exiting")
            quit(0)

        print(f"script: creating {new_branch_name} ...")
        create_branch_code = os.system(f"git -C {project_path} checkout -b {new_branch_name}")
        if create_branch_code != 0:
            print("script: (!) failed to create branch, exiting")
            quit(0)

        for commit_hash in commit_hashes:
            if branch_contains_commit(new_branch_name, commit_hash):
                print(f"script: (!) {new_branch_name} already contains commit {commit_hash}")

            cherry_pick_code = os.system(f"git -C {project_path} cherry-pick {commit_hash}")
            if cherry_pick_code != 0:
                print(f"script: (!) failed to cherry-pick {commit_hash} to {new_branch_name}, exiting")
                quit(0)

        print(f"script: pushing {new_branch_name} to origin ...")
        git_push_code = os.system(f"git -C {project_path} push origin {new_branch_name}")
        if git_push_code != 0:
            print(f"script: (!) failed to push {new_branch_name} to origin, exiting")
            quit(0)


def get_base_brahches(gh_login, gh_token, jira_tasks):
    print("script: calculating base branches ...")
    branches_dict = dict([(x['key'], []) for x in jira_tasks])

    for jira_task in [to_brief_jira_task(x) for x in jira_tasks]:
        current_fix_versions = sorted(jira_task['fixVersions'], key=settings.to_version_sort_key)
        current_affected_versions = sorted(jira_task['affectedVersions'], key=settings.to_version_sort_key)
        # sorted("This is a test string from Andrew".split(), key=str.lower)
        # current_affected_versions[0]
        unreleased_minor = get_closest_unreleased_minor(gh_login, gh_token, settings.REPO_ORG, settings.REPO_NAME)
        current_patch_version = settings.next_patch(current_affected_versions[0])
        current_minor_version = None

        while current_minor_version != unreleased_minor:
            while check_tag_exists(gh_login, gh_token, settings.REPO_ORG, settings.REPO_NAME,
                                   settings.to_release_tag(current_patch_version)):
                if current_patch_version in current_fix_versions:
                    # nonlocal current_minor_version
                    current_minor_version = settings.next_minor(current_patch_version)
                    current_patch_version = settings.next_minor(current_patch_version)
                    break
                else:
                    current_patch_version = settings.next_patch(current_patch_version)

            branch = settings.to_release_branch_name(current_patch_version)
            if not check_branch_exists(gh_login, gh_token, settings.REPO_ORG, settings.REPO_NAME, branch):
                print(f"script: (!) need patch to {branch}, " +
                      f"but branch {branch} does not exist on remote")
                quit(0)
            branches_dict[jira_task['key']].append((current_patch_version, branch))
            current_minor_version = settings.next_minor(current_patch_version)
            current_patch_version = settings.next_minor(current_patch_version)

        if unreleased_minor not in current_fix_versions:
            if check_branch_exists(gh_login, gh_token, settings.REPO_ORG, settings.REPO_NAME,
                                   settings.to_release_branch_name(unreleased_minor)):
                branches_dict[jira_task['key']].append(
                    (unreleased_minor, settings.to_release_branch_name(unreleased_minor))
                )
            else:
                branches_dict[jira_task['key']].append((unreleased_minor, 'master'))

    # remove base branches where pr is already open
    for jira_task in [to_brief_jira_task(x) for x in jira_tasks]:
        for release_version, release_branch in branches_dict[jira_task['key']]:
            prs = list_prs(gh_login, gh_token, settings.REPO_ORG, settings.REPO_NAME, release_branch)
            for pr in prs:
                if jira_task['key'].lower() in pr['head']['ref'].lower():
                    print(f"script: (!) {jira_task['key']} already has PR to {pr['head']['ref']}, skipping ...")
                    branches_dict[jira_task['key']].remove((release_version, release_branch))

    if len(set(
            ['__'.join(branches_dict[jira_key][1]) for jira_key in branches_dict]
    )) != 1:
        print(f"script: (!) potential release branches in {[x['key'] for x in jira_tasks]}, " +
              f"does not match")
        quit(0)
        return []

    return branches_dict[jira_tasks[0]['key']]


def branch_contains_commit(branch, commit_hash):
    contains_output = subprocess.check_output(
        f"git -C {settings.LOCAL_PROJECT_PATH} branch {branch} --contains {commit_hash}", shell=True
    )

    return contains_output.decode('utf-8').replace("\n", "") != ""


if __name__ == '__main__':
    try:
        ap = add_arguments(argparse.ArgumentParser(description=DESCRIPTION))
        arguments_dict = parse_args(vars(ap.parse_args()))
        run_scenario(arguments_dict['commits_count'])
    except KeyboardInterrupt:
        print(f"\nscript: KeyboardInterrupt, exiting ...")
        quit(0)
