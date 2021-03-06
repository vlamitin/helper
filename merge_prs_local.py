import argparse
import os
from pprint import pprint

import settings
from internal.pr import list_open_prs

DESCRIPTION = "Creates local merge branch"


def add_arguments(arg_parser):
    arg_parser.add_argument('--merge_branch_name', nargs=1, type=str, help='base branch name', required=True)
    arg_parser.add_argument('--base_branch_name', nargs=1, type=str, help='base branch name', required=True)
    return arg_parser


def parse_args(args_dict):
    return {
        'merge_branch_name': args_dict['merge_branch_name'][0],
        'base_branch_name': args_dict['base_branch_name'][0]
    }


def run_scenario(merge_branch_name, base_branch_name):
    creds = settings.get_creds()

    open_prs = list_open_prs(creds['GH_LOGIN'], creds['GH_TOKEN'], settings.REPO_ORG, settings.REPO_NAME)
    prs_to_merge_local = settings.filter_prs_to_merge_local(open_prs)
    short_prs_to_merge_local = [(x['head']['ref'], x['base']['ref']) for x in prs_to_merge_local]

    # given prs [branch_1 <- branch_2, branch_3 <- branch_4, master <- branch_1],
    # returns [master <- branch_1, branch_1 <- branch_2]
    # because you'll need to merge that prs in that order
    branches_chain = [x for x in short_prs_to_merge_local if x[1] == base_branch_name]
    branches_chain = [
        *branches_chain,
        *[x for x in short_prs_to_merge_local if x[1] in [y[0] for y in branches_chain]]
    ]

    print("script: prs to be merged local:")
    pprint([f"{i + 1}. {x[0]} -> {x[1]}" for i, x in enumerate(branches_chain)])
    project_path = settings.LOCAL_PROJECT_PATH
    print("script: project_path:", project_path)
    continue_choice = input(
        "script: this prs ^ will be merged local, press \"Enter\" to continue, \"q\" to quit: "
    )
    if continue_choice in ["q", "Q"]:
        quit(0)

    print("script: git fetch ...")
    os.system(f"git -C {project_path} fetch")
    print(f"script: checkouting origin/{base_branch_name} ...")
    os.system(f"git -C {project_path} checkout origin/{base_branch_name}")
    print(f"script: checkouting new branch {merge_branch_name} ...")
    create_branch_code = os.system(f"git -C {project_path} checkout -b {merge_branch_name}")
    if create_branch_code != 0:
        print("script: (!) failed to create branch, exiting")
        quit(0)

    for head_branch_name, base_branch_name in branches_chain:
        print(f"script: merging {head_branch_name}...")
        git_merge_code = os.system(f"git -C {project_path} merge origin/{head_branch_name}")
        if git_merge_code != 0:
            print(f"script: (!) failed to merge origin/{head_branch_name}, exiting")
            quit(0)


if __name__ == '__main__':
    try:
        ap = add_arguments(argparse.ArgumentParser(description=DESCRIPTION))
        arguments_dict = parse_args(vars(ap.parse_args()))
        run_scenario(arguments_dict['merge_branch_name'], arguments_dict['base_branch_name'])
    except KeyboardInterrupt:
        print(f"\nscript: KeyboardInterrupt, exiting ...")
        quit(0)
