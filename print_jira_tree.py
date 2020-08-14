import argparse
from pprint import pprint

import settings
from internal.jira_task import get_brief_tasks_tree, get_jira_task

DESCRIPTION = "Prints tree of subtasks for given task key or epic jira key"


def add_arguments(arg_parser):
    arg_parser.add_argument('task_key', nargs=1, type=str, help='root jira task key')

    return arg_parser


def parse_args(args_dict):
    return {
        'task_key': args_dict['task_key'][0],
    }


def run_scenario(task_key):
    creds = settings.get_creds()

    pprint(get_brief_tasks_tree(creds['JIRA_DOMAIN'], creds['JIRA_LOGIN'], creds['JIRA_TOKEN'],
                                get_jira_task(creds['JIRA_DOMAIN'], creds['JIRA_LOGIN'], creds['JIRA_TOKEN'], task_key))
           )


if __name__ == '__main__':
    try:
        ap = add_arguments(argparse.ArgumentParser(description=DESCRIPTION))
        arguments_dict = parse_args(vars(ap.parse_args()))
        run_scenario(arguments_dict['task_key'])
    except KeyboardInterrupt:
        print(f"\nscript: KeyboardInterrupt, exiting ...")
        quit(0)
