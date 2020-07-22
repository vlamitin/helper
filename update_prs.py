import argparse
import os
from pprint import pprint

import settings
from internal.pr import list_open_prs


DESCRIPTION = "Merges base branch in each prs head branch"


def add_arguments(arg_parser):
    arg_parser.add_argument('base_branch', nargs=1, type=str, help='base branch name')

    return arg_parser


def parse_args(args_dict):
    return {
        'base_branch': args_dict['base_branch'][0]
    }


def run_scenario(base_branch_name):
    print("script: setting creds from envs ...")
    try:
        GH_LOGIN = os.environ['PR_HELPER_GH_LOGIN']
        GH_TOKEN = os.environ['PR_HELPER_GH_TOKEN']
    except KeyError:
        print("script: (!) no envs set, exiting")
        quit(0)

    open_prs = list_open_prs(GH_LOGIN, GH_TOKEN, settings.REPO_ORG, settings.REPO_NAME)
    prs_to_update = settings.filter_prs_to_update(open_prs)
    short_prs_to_update = [(x['head']['ref'], x['base']['ref']) for x in prs_to_update]

    # given prs [branch_1 <- branch_2, branch_3 <- branch_4, master <- branch_1],
    # returns [master <- branch_1, branch_1 <- branch_2]
    # because you'll need to merge that prs in that order
    branches_chain = [x for x in short_prs_to_update if x[1] == base_branch_name]
    branches_chain = [
        *branches_chain,
        *[x for x in short_prs_to_update if x[1] in [y[0] for y in branches_chain]]
    ]

    print("script: prs to be updated:")
    pprint(branches_chain)
    project_path = settings.LOCAL_PROJECT_PATH
    print("script: project_path:", project_path)
    continue_choice = input(
        "script: this prs ^ will be updated, press \"Enter\" to continue, \"q\" to quit: "
    )
    if continue_choice in ["q", "Q"]:
        quit(0)

    project_path = settings.LOCAL_PROJECT_PATH

    os.system(f"git -C {project_path} fetch")
    for branch in branches_chain:
        print(f"script: checkout {branch[0]} ...")
        checkout_code = os.system(f"git -C {project_path} checkout {branch[0]}")
        if checkout_code != 0:
            print("script: (!) failed to checkout, exiting")
            quit(0)

        print(f"script: pull origin {branch[0]}")
        git_pull_1_code = os.system(f"git -C {project_path} pull origin {branch[1]}")
        if git_pull_1_code != 0:
            print("script: (!) failed to pull, exiting")
            quit(0)

        print(f"script: pull origin {branch[1]}")
        git_pull_code = os.system(f"git -C {project_path} pull origin {branch[1]}")
        if git_pull_code != 0:
            print("script: (!) failed to pull, exiting")
            quit(0)

        print(f"CHANGES=$(git -C {project_path} cherry -v origin/{branch[0]} | wc -l);" +
              f" [ $CHANGES != '0' ] " +
              f"&& git -C {project_path} push origin {branch[0]}")

        print(f"script: push origin {branch[0]}")
        git_push_code = os.system(f"CHANGES=$(git -C {project_path} cherry -v origin/{branch[0]} | wc -l);" +
                                  f" [ $CHANGES != '0' ] " +
                                  f"&& git -C {project_path} push origin {branch[0]} || echo 'already pushed'")
        print("git_push_code", git_push_code)
        if git_push_code != 0:
            print("script: (!) failed to push, exiting")
            quit(0)


if __name__ == '__main__':
    try:
        ap = add_arguments(argparse.ArgumentParser(description=DESCRIPTION))
        arguments_dict = parse_args(vars(ap.parse_args()))
        run_scenario(arguments_dict['base_branch'])
    except KeyboardInterrupt:
        print(f"\nscript: KeyboardInterrupt, exiting ...")
        quit(0)
