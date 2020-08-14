import argparse

import settings
from internal.jira_task import get_my_tasks
from internal.jira_worklog import add_worklog, to_jira_seconds

DESCRIPTION = 'Adds worklog'


def add_arguments(arg_parser):
    arg_parser.add_argument('--jira_key', nargs=1, type=str, help='key of jira task')
    arg_parser.add_argument('--jira_period_pieces', nargs='*', type=str, help='worklog in "1d 2h 3m" format')

    return arg_parser


def parse_args(args_dict):
    return {
        'jira_key': args_dict['jira_key'] and args_dict['jira_key'][0] or '',
        'jira_period_pieces': args_dict['jira_period_pieces'] or [],
    }


def run_scenario(jira_key, jira_period_pieces):
    creds = settings.get_creds()
    
    if not jira_key:
        print(f"script: no jira_key specified, fetching created {creds['JIRA_LOGIN']} jira tasks ...")
        jira_tasks = get_my_tasks(
            creds['JIRA_DOMAIN'], creds['JIRA_LOGIN'], creds['JIRA_TOKEN']
        )
        print(f"script: {len(jira_tasks)} jira_tasks fetched")

        for index, jira_task in enumerate(jira_tasks):
            print(f"{index + 1}. {jira_task['key']} ({jira_task['fields']['summary']})")
        jira_tasks_choice = input(
            "script: Choose one task number: "
        )
        jira_key = jira_tasks[int(jira_tasks_choice) - 1]['key']
        print(f"script: {jira_key} selected as jira_key")

    if not jira_period_pieces:
        jira_period_pieces_choice = input(
            "script: Enter worklog. Like so: \"2d 4h\": "
        )
        jira_period_pieces = jira_period_pieces_choice.split(" ")
        print(f"script: {jira_period_pieces} selected as jira_period_pieces")

    created_worklog = add_worklog(creds['JIRA_DOMAIN'], creds['JIRA_LOGIN'], creds['JIRA_TOKEN'], jira_key,
                                  to_jira_seconds(jira_period_pieces))
    print(f"created! {creds['JIRA_DOMAIN']}/browse/{jira_key}?focusedWorklogId={created_worklog['id']}")


if __name__ == '__main__':
    try:
        ap = add_arguments(argparse.ArgumentParser(description=DESCRIPTION))
        arguments_dict = parse_args(vars(ap.parse_args()))
        run_scenario(
            arguments_dict['jira_key'],
            arguments_dict['jira_period_pieces'],
        )
    except KeyboardInterrupt:
        print(f"\nscript: KeyboardInterrupt, exiting ...")
        quit(0)
