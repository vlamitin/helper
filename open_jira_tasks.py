from pprint import pprint
from webbrowser import open_new_tab

import settings
from internal.jira_task import get_my_tasks

DESCRIPTION = "Opens your jira tasks in browser"


def run_scenario():
    creds = settings.get_creds()

    print(f"script: fetching created {creds['JIRA_LOGIN']} jira tasks ...")
    jira_tasks = get_my_tasks(
        creds['JIRA_DOMAIN'], creds['JIRA_LOGIN'], creds['JIRA_TOKEN']
    )
    print(f"script: {len(jira_tasks)} jira_tasks fetched")

    for jira_task in jira_tasks:
        url = f"{creds['JIRA_DOMAIN']}/browse/{jira_task['key']}"
        print(f"script: opening {url} in browser ...")
        open_new_tab(url)


if __name__ == '__main__':
    try:
        run_scenario()
    except KeyboardInterrupt:
        print(f"\nscript: KeyboardInterrupt, exiting ...")
        quit(0)

    pprint("TODO debug")
