import argparse
from pprint import pprint
from webbrowser import open_new_tab

import settings
from internal.pr import get_user_created_prs, get_user_request_reviews

DESCRIPTION = "Opens your created and your review requested prs"


def run_scenario():
    creds = settings.get_creds()
    
    print(f"script: fetching created by {creds['GH_LOGIN']} prs ...")
    created_prs = get_user_created_prs(creds['GH_LOGIN'], creds['GH_TOKEN'], creds['GH_LOGIN'])
    print(f"script: {len(created_prs)} created_prs fetched")

    print(f"script: fetching review from {creds['GH_LOGIN']} requested prs ...")
    requested_pr_reviews = get_user_request_reviews(
        creds['GH_LOGIN'], creds['GH_TOKEN'], creds['GH_LOGIN'],
    )

    print(f"script: {len(requested_pr_reviews)} requested_pr_reviews fetched")

    for pr in [*created_prs, *requested_pr_reviews]:
        print(f"script: opening {pr['html_url']} in browser ...")
        open_new_tab(pr['html_url'])


if __name__ == '__main__':
    try:
        arg_parser = argparse.ArgumentParser(description=DESCRIPTION)
        arg_parser.parse_args()
        run_scenario()
    except KeyboardInterrupt:
        print(f"\nscript: KeyboardInterrupt, exiting ...")
        quit(0)

    pprint("TODO debug")
