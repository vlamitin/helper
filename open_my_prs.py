import argparse
import os
from pprint import pprint
from webbrowser import open_new_tab

from internal.pr import get_user_created_prs, get_user_request_reviews


def run_scenario():
    arg_parser = argparse.ArgumentParser(description='Opens your created and your review requested prs')
    arg_parser.parse_args()

    print("script: setting creds from envs ...")
    try:
        GH_LOGIN = os.environ['PR_HELPER_GH_LOGIN']
        GH_TOKEN = os.environ['PR_HELPER_GH_TOKEN']
    except KeyError:
        print("script: (!) no envs set, exiting")
        quit(0)

    print(f"script: fetching created by {GH_LOGIN} prs ...")
    created_prs = get_user_created_prs(
        GH_LOGIN, GH_TOKEN, GH_LOGIN,
    )
    print(f"script: {len(created_prs)} created_prs fetched")

    print(f"script: fetching review from {GH_LOGIN} requested prs ...")
    requested_pr_reviews = get_user_request_reviews(
        GH_LOGIN, GH_TOKEN, GH_LOGIN,
    )

    print(f"script: {len(requested_pr_reviews)} requested_pr_reviews fetched")

    for pr in [*created_prs, *requested_pr_reviews]:
        print(f"script: opening {pr['html_url']} in browser ...")
        open_new_tab(pr['html_url'])


if __name__ == '__main__':
    try:
        run_scenario()
    except KeyboardInterrupt:
        print(f"\nscript: KeyboardInterrupt, exiting ...")
        quit(0)

    pprint("TODO debug")
