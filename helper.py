import argparse

import open_jira_tasks
import print_jira_tree
import merge_prs_local
import create_pr
import open_prs
import update_prs


def run_scenario():
    arg_parser = argparse.ArgumentParser(prog="helper", description="Type helper {command} -h for each command help")
    subparsers = arg_parser.add_subparsers(title="commands", dest="command")

    create_pr_parser = subparsers.add_parser('create_pr', help=create_pr.DESCRIPTION)
    create_pr.add_arguments(create_pr_parser)

    open_prs_parser = subparsers.add_parser('open_prs', help=open_prs.DESCRIPTION)

    open_jira_tasks_parser = subparsers.add_parser('open_jira_tasks', help=open_jira_tasks.DESCRIPTION)

    merge_prs_local_parser = subparsers.add_parser('merge_prs_local', help=merge_prs_local.DESCRIPTION)
    merge_prs_local.add_arguments(merge_prs_local_parser)

    update_prs_parser = subparsers.add_parser('update_prs', help=update_prs.DESCRIPTION)
    update_prs.add_arguments(update_prs_parser)

    print_jira_tree_parser = subparsers.add_parser('print_jira_tree', help=print_jira_tree.DESCRIPTION)
    print_jira_tree.add_arguments(print_jira_tree_parser)

    args = arg_parser.parse_args()
    args_dict = vars(args)

    if args_dict['command'] == 'create_pr':
        arguments_dict = create_pr.parse_args(args_dict)
        create_pr.run_scenario(
            arguments_dict['head_branch'], arguments_dict['reviewers'], arguments_dict['title_content']
        )
    elif args_dict['command'] == 'open_prs':
        open_prs.run_scenario()
    elif args_dict['command'] == 'open_jira_tasks':
        open_jira_tasks.run_scenario()
    elif args_dict['command'] == 'merge_prs_local':
        arguments_dict = merge_prs_local.parse_args(args_dict)
        merge_prs_local.run_scenario(arguments_dict['merge_branch_name'])
    elif args_dict['command'] == 'print_jira_tree':
        arguments_dict = print_jira_tree.parse_args(args_dict)
        print_jira_tree.run_scenario(arguments_dict['task_key'])
    elif args_dict['command'] == 'update_prs':
        arguments_dict = update_prs.parse_args(args_dict)
        update_prs.run_scenario(arguments_dict['base_branch'])
    else:
        arg_parser.print_usage()

    # TODO
    # worklog adder
    # check nearest minor version
    # check if code freeze


if __name__ == '__main__':
    try:
        run_scenario()
    except KeyboardInterrupt:
        print(f"\nscript: KeyboardInterrupt, exiting ...")
        quit(0)
