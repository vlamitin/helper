import settings_global
import settings_user

REPO_ORG = hasattr(settings_user, 'REPO_ORG') \
                     and settings_user.REPO_ORG \
                     or settings_global.REPO_ORG

REPO_NAME = hasattr(settings_user, 'REPO_NAME') \
                     and settings_user.REPO_NAME \
                     or settings_global.REPO_NAME

JIRA_DOMAIN = hasattr(settings_user, 'JIRA_DOMAIN') \
                     and settings_user.JIRA_DOMAIN \
                     or settings_global.JIRA_DOMAIN


def to_milestone_title(branch_name):
    if hasattr(settings_user, 'to_milestone_title'):
        return settings_user.to_milestone_title(branch_name)

    return settings_global.to_milestone_title(branch_name)


def to_version(branch_name):
    if hasattr(settings_user, 'to_version'):
        return settings_user.to_version(branch_name)

    return settings_global.to_version(branch_name)


def to_release_branch_name(version):
    if hasattr(settings_user, 'to_release_branch_name'):
        return settings_user.to_release_branch_name(version)

    return settings_global.to_release_branch_name(version)


def to_jira_task_keys(branch_name):
    if hasattr(settings_user, 'to_jira_task_keys'):
        return settings_user.to_jira_task_keys(branch_name)

    return settings_global.to_jira_task_keys(branch_name)


def to_pr_labels(branch_name):
    if hasattr(settings_user, 'to_pr_labels'):
        return settings_user.to_pr_labels(branch_name)

    return settings_global.to_pr_labels(branch_name)


def to_pr_title(jira_tasks, cli_args_pr_title, brief_milestone):
    if hasattr(settings_user, 'to_pr_title'):
        return settings_user.to_pr_title(jira_tasks, cli_args_pr_title, brief_milestone)

    return settings_global.to_pr_title(jira_tasks, cli_args_pr_title, brief_milestone)


all_build_contexts = hasattr(settings_user, 'all_build_contexts') \
                     and settings_user.all_build_contexts \
                     or settings_global.all_build_contexts


def to_build_trigger_comment(builds):
    if hasattr(settings_user, 'to_build_trigger_comment'):
        return settings_user.to_build_trigger_comment(builds)

    return settings_global.to_build_trigger_comment(builds)
