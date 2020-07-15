import argparse
import os
import time
from pprint import pprint

import settings
from internal.branch import check_branch_exists
from internal.jira_task import get_jira_task
from internal.pr import create_pr, update_pr
from internal.pr_build_statuses import get_blocking_builds, list_pr_build_statuses
from internal.pr_comments import create_issue_comment
from internal.pr_milestone import to_brief_milestones, get_milestones, \
    brief_milestone_and_base_branch_name_by_head_branch
from internal.pr_reviews import request_pr_reviews
from internal.repo import check_collaborator
from internal.repo_content import get_file_content


def get_new_pr_props_by_head_branch_name(
        gh_login, gh_token, repo_org, repo_name,
        jira_domain, jira_login, jira_token,
        head_branch_name, title_content_list
):
    labels = settings.to_pr_labels(head_branch_name)
    task_keys = settings.to_jira_task_keys(head_branch_name)
    jira_tasks = [get_jira_task(jira_domain, jira_login, jira_token, x) for x in task_keys]
    brief_milestones = to_brief_milestones(get_milestones(gh_login, gh_token, repo_org, repo_name))
    brief_milestone, base_branch_name = brief_milestone_and_base_branch_name_by_head_branch(
        head_branch_name,
        brief_milestones
    )

    title = settings.to_pr_title(jira_tasks,
                                 title_content_list and len(title_content_list) == 1 and title_content_list[0] or '',
                                 brief_milestone)

    jira_links_comment = '\n'.join(
        [
            f"[{x['key']} - {x['fields']['summary']}]({settings.JIRA_DOMAIN}/browse/{x['key']})"
            for x in jira_tasks
        ]
    )

    return {
        'title': title,
        'task_keys': task_keys,
        'jira_links_comment': jira_links_comment,
        'milestone_number': brief_milestone['number'],
        'milestone_title': brief_milestone['title'],
        'labels': labels,
        'head_branch_name': head_branch_name,
        'base_branch_name': base_branch_name,
    }


def run_scenario():
    arg_parser = argparse.ArgumentParser(description='Create pr from given head branch name')
    arg_parser.add_argument('head_branch', nargs=1, type=str, help='head branch name')
    arg_parser.add_argument('--reviewers', nargs='*', type=str, help='space delimited list of reviewers')
    arg_parser.add_argument('--title_content', nargs=1, type=str, help='pr title (between jira task keys and version)')
    args = arg_parser.parse_args()

    print("script: setting creds from envs ...")
    try:
        GH_LOGIN = os.environ['PR_HELPER_GH_LOGIN']
        GH_TOKEN = os.environ['PR_HELPER_GH_TOKEN']
        JIRA_DOMAIN = os.environ['PR_HELPER_JIRA_DOMAIN']
        JIRA_LOGIN = os.environ['PR_HELPER_JIRA_LOGIN']
        JIRA_TOKEN = os.environ['PR_HELPER_JIRA_TOKEN']
    except KeyError:
        print("script: (!) no envs set, exiting")
        quit(0)

    head_branch = vars(args)['head_branch'][0]
    reviewers = vars(args)['reviewers']
    title_content_list = vars(args)['title_content']

    for reviewer in reviewers:
        if not (check_collaborator(GH_LOGIN, GH_TOKEN, settings.REPO_ORG, settings.REPO_NAME, reviewer)):
            print(f"script: (!) {reviewer} is not a collaborator")
            quit(0)

    if not check_branch_exists(GH_LOGIN, GH_TOKEN, settings.REPO_ORG, settings.REPO_NAME, head_branch):
        print(f"script: (!) head branch \"{head_branch}\" does not exist on remote")
        quit(0)

    print("script: fetching branch new pr summary...")
    new_pr_summmary = get_new_pr_props_by_head_branch_name(
        GH_LOGIN, GH_TOKEN, settings.REPO_ORG, settings.REPO_NAME,
        JIRA_DOMAIN, JIRA_LOGIN, JIRA_TOKEN,
        head_branch, title_content_list
    )

    pprint(new_pr_summmary, width=140, indent=2)

    if not check_branch_exists(GH_LOGIN, GH_TOKEN, settings.REPO_ORG, settings.REPO_NAME,
                               new_pr_summmary['base_branch_name']):
        print(f"script: (!) base branch \"{new_pr_summmary['base_branch_name']}\" does not exist on remote")
        quit(0)

    continue_choice = input(
        "script: PR with this ^ props will be created, press \"Enter\" or to continue, \"n\" to quit ..."
    )
    if continue_choice in ["n", "N"]:
        quit(0)

    pr_body_template = get_file_content(GH_LOGIN, GH_TOKEN, settings.REPO_ORG, settings.REPO_NAME, 'PULL_REQUEST_TEMPLATE.md')
    pr_body = pr_body_template.replace(
        f"[Ссылка на задачу]({settings.JIRA_DOMAIN}/browse/)",
        new_pr_summmary['jira_links_comment'],
    )

    print("script: creating pr ...")
    created_pr = create_pr(GH_LOGIN, GH_TOKEN, settings.REPO_ORG, settings.REPO_NAME,
                           new_pr_summmary['title'], pr_body,
                           new_pr_summmary['head_branch_name'], new_pr_summmary['base_branch_name'])
    print(f"script: created pr https://github.com/{settings.REPO_ORG}/{settings.REPO_NAME}/pull/{created_pr['number']}")

    print("script: setting milestone and labels ...")
    update_pr(GH_LOGIN, GH_TOKEN, settings.REPO_ORG, settings.REPO_NAME,
                           created_pr['number'], new_pr_summmary['milestone_number'], new_pr_summmary['labels'])
    print("script: successfully updated pr with milestone and labels")

    if reviewers and len(reviewers) > 0:
        print(f"script: requesting reviewers {reviewers} ...")
        request_pr_reviews(GH_LOGIN, GH_TOKEN, settings.REPO_ORG, settings.REPO_NAME,
                           created_pr['number'], reviewers)
        print(f"review requested ...")

    print("script: sleeping for 180s before triggering build ...")
    time.sleep(180)

    build_trigger_comment = settings.to_build_trigger_comment(
        get_blocking_builds(
            list_pr_build_statuses(
                GH_LOGIN, GH_TOKEN, created_pr['statuses_url']
            )
        )
    )
    print(f"script: creating comment \n{build_trigger_comment}\n ...")
    create_issue_comment(GH_LOGIN, GH_TOKEN, settings.REPO_ORG, settings.REPO_NAME,
                         created_pr['number'], build_trigger_comment)
    print(f"script: comment created")
    print(f"script: done, link once again: " +
          f" https://github.com/{settings.REPO_ORG}/{settings.REPO_NAME}/pull/{created_pr['number']}")


if __name__ == '__main__':
    try:
        run_scenario()
    except KeyboardInterrupt:
        print(f"\nscript: KeyboardInterrupt, exiting ...")
        quit(0)
