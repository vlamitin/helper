import os
from pprint import pprint
from webbrowser import open_new_tab

from internal.jira_task import get_my_tasks

DESCRIPTION = "Opens your jira tasks in browser"


def run_scenario():
    print("script: setting creds from envs ...")
    try:
        JIRA_DOMAIN = os.environ['PR_HELPER_JIRA_DOMAIN']
        JIRA_LOGIN = os.environ['PR_HELPER_JIRA_LOGIN']
        JIRA_TOKEN = os.environ['PR_HELPER_JIRA_TOKEN']
    except KeyError:
        print("script: (!) no envs set, exiting")
        quit(0)

    print(f"script: fetching created {JIRA_LOGIN} jira tasks ...")
    jira_tasks = get_my_tasks(
        JIRA_DOMAIN, JIRA_LOGIN, JIRA_TOKEN
    )
    print(f"script: {len(jira_tasks)} jira_tasks fetched")

    for jira_task in jira_tasks:
        url = f"{JIRA_DOMAIN}/browse/{jira_task['key']}"
        print(f"script: opening {url} in browser ...")
        open_new_tab(url)


if __name__ == '__main__':
    try:
        run_scenario()
    except KeyboardInterrupt:
        print(f"\nscript: KeyboardInterrupt, exiting ...")
        quit(0)

    pprint("TODO debug")
