import argparse
import os
from pprint import pprint

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
    print("script: setting creds from envs ...")
    try:
        JIRA_DOMAIN = os.environ['PR_HELPER_JIRA_DOMAIN']
        JIRA_LOGIN = os.environ['PR_HELPER_JIRA_LOGIN']
        JIRA_TOKEN = os.environ['PR_HELPER_JIRA_TOKEN']
    except KeyError:
        print("script: (!) no envs set, exiting")
        quit(0)

    pprint(get_brief_tasks_tree(JIRA_DOMAIN, JIRA_LOGIN, JIRA_TOKEN,
                                get_jira_task(JIRA_DOMAIN, JIRA_LOGIN, JIRA_TOKEN, task_key)))


if __name__ == '__main__':
    try:
        ap = add_arguments(argparse.ArgumentParser(description=DESCRIPTION))
        arguments_dict = parse_args(vars(ap.parse_args()))
        run_scenario(arguments_dict['task_key'])
    except KeyboardInterrupt:
        print(f"\nscript: KeyboardInterrupt, exiting ...")
        quit(0)
