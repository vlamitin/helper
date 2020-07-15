import os
from pprint import pprint


def git_demo_prepare(project_path, demo_br_name, branches):
    print("script: fetching ...")
    os.system(f"git -C {project_path} fetch")
    print("script: checkouting origin/master ...")
    os.system(f"git -C {project_path} checkout origin/master")
    print("script: checkouting new branch ...")
    os.system(f"git -C {project_path} checkout -b {demo_br_name}")

    for branch in branches:
        print(f"script: merging {branch}...")
        os.system(f"git -C {project_path} merge origin/{branch}")


if __name__ == '__main__':
    print("script: setting creds from envs ...")
    try:
        GH_LOGIN = os.environ['PR_HELPER_GH_LOGIN']
        GH_TOKEN = os.environ['PR_HELPER_GH_TOKEN']
    except KeyError:
        print("script: (!) no envs set, exiting")
        quit(0)

    pprint("TODO debug")
