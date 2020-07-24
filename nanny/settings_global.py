import re

REPO_ORG = 'github'
REPO_NAME = 'markup'

JIRA_DOMAIN = 'https://atlassian.atlassian.net'


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


def to_release_branch_name(version):
    return 'release_' + version


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


def to_build_trigger_comment(builds):
    return '\n'.join(list(set([x['build_context'] for x in builds])))
