import argparse

import merge_prs_local
import create_pr
import open_my_prs
import update_prs


def run_scenario():
    arg_parser = argparse.ArgumentParser(prog="helper")
    subparsers = arg_parser.add_subparsers(title="commands", dest="command")

    create_pr_parser = subparsers.add_parser('create_pr', help="creates a pr")
    create_pr.add_arguments(create_pr_parser)

    open_prs_parser = subparsers.add_parser('open_prs', help="open your prs in browser")

    merge_prs_local_parser = subparsers.add_parser('merge_prs_local', help="creates local merge branch")
    merge_prs_local.add_arguments(merge_prs_local_parser)

    update_prs_parser = subparsers.add_parser('update_prs', help="merges base branch in prs head branch")
    update_prs.add_arguments(update_prs_parser)

    args = arg_parser.parse_args()
    args_dict = vars(args)

    if args_dict['command'] == 'create_pr':
        arguments_dict = create_pr.parse_args(args_dict)
        create_pr.run_scenario(
            arguments_dict['head_branch'], arguments_dict['reviewers'], arguments_dict['title_content']
        )
    elif args_dict['command'] == 'open_prs':
        open_my_prs.run_scenario()
    elif args_dict['command'] == 'merge_prs_local':
        arguments_dict = merge_prs_local.parse_args(args_dict)
        merge_prs_local.run_scenario(arguments_dict['merge_branch_name'])
    elif args_dict['command'] == 'update_prs':
        arguments_dict = update_prs.parse_args(args_dict)
        update_prs.run_scenario(arguments_dict['base_branch'])


if __name__ == '__main__':
    try:
        run_scenario()
    except KeyboardInterrupt:
        print(f"\nscript: KeyboardInterrupt, exiting ...")
        quit(0)
