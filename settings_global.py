import os
import re

REPO_ORG = 'github'
REPO_NAME = 'markup'

LOCAL_PROJECT_PATH = '/home/user/projects/markup'

reviewers_shortlist = []


def get_creds():
    print("script: getting creds from envs ...")
    try:
        return {
            'GH_LOGIN': os.environ['PR_HELPER_GH_LOGIN'],
            'GH_TOKEN': os.environ['PR_HELPER_GH_TOKEN'],
            'JIRA_DOMAIN': os.environ['PR_HELPER_JIRA_DOMAIN'],
            'JIRA_LOGIN': os.environ['PR_HELPER_JIRA_LOGIN'],
            'JIRA_TOKEN': os.environ['PR_HELPER_JIRA_TOKEN'],
        }
    except KeyError:
        print("script: (!) no envs set, exiting")
        quit(0)


def to_milestone_title(branch_name):
    to_version_re = re.compile(r"to[-|_]?(\d\d\.\d[\d]?)")
    matches = to_version_re.findall(branch_name)
    if len(matches) == 1:
        return matches[0]

    return None


def to_version(branch_name):
    to_version_re = re.compile(r"to[-|_]?(\d\d\.\d[\d]?)")
    matches = to_version_re.findall(branch_name)
    if len(matches) == 1:
        return matches[0]

    return None


def to_new_version_branch_name(branch_name, version):
    return re.sub(r"to[-|_]?(\d\d\.\d[\d]?)", f"to-{'.'.join(version.split('.')[2:])}", branch_name)


def to_release_branch_name(version):
    return 'release_' + version


def to_release_tag(version):
    return 'v' + version


def tag_to_version(release_tag):
    return release_tag[1:]


def next_patch(version):
    version_parts = version.split('.')
    return '.'.join(version_parts[:-1]) + f".{int(version_parts[-1]) + 1}"


def next_minor(version):
    version_parts = version.split('.')
    return '.'.join(version_parts[:-2]) + f".{int(version_parts[-2]) + 1}.0"


def to_version_sort_key(version):
    return sum([int(x) * 10 ** (i + 1) for i, x in enumerate(reversed(version.split('.')))])


def to_jira_task_keys(branch_name):
    jira_keys = []

    jira_key_re = re.compile(r"(([task|TASK]+)-\d{1,4})")
    match_tuples = jira_key_re.findall(branch_name)
    for match_tuple in match_tuples:
        jira_keys.append(match_tuple[0])

    return list(set(jira_keys))


def to_pr_labels(branch_name):
    computed_labels = []

    if 'fix' in branch_name.lower():
        computed_labels.append('Fix 💩')

    return list(set(computed_labels))


def to_pr_title(jira_tasks, cli_args_pr_title, brief_milestone):
    title = ', '.join([x['key'] for x in jira_tasks]) + ' - '
    if cli_args_pr_title:
        title += cli_args_pr_title
    else:
        title += jira_tasks[0]['fields']['summary']

    title += f" (to {brief_milestone['title']})"
    return title


all_build_contexts = [
    'SonarQube analysis',
    'sonarqube'
]

created_pr_default_comment = '\n'.join([
    'SonarQube analysis',
    'sonarqube'
])


def to_build_trigger_comment(builds):
    return '\n'.join(list(set([x['build_context'] for x in builds])))


def filter_prs_to_update(prs):
    return prs


def filter_prs_to_merge_local(prs):
    return prs
