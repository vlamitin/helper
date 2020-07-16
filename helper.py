import argparse
import create_pr
import open_my_prs


def run_scenario():
    arg_parser = argparse.ArgumentParser(prog="helper")
    subparsers = arg_parser.add_subparsers(title="commands", dest="command")

    create_pr_parser = subparsers.add_parser('create_pr', help="creates a pr")
    create_pr_parser = create_pr.add_arguments(create_pr_parser)

    open_prs_parser = subparsers.add_parser('open_prs', help="open your prs in browser")

    args = arg_parser.parse_args()

    args_dict = vars(args)

    if args_dict['command'] == 'create_pr':
        print(create_pr.parse_args(args_dict))
        arguments_dict = create_pr.parse_args(args_dict)
        create_pr.run_scenario(
            arguments_dict['head_branch'], arguments_dict['reviewers'], arguments_dict['title_content']
        )
    elif args_dict['command'] == 'open_prs':
        open_my_prs.run_scenario()


if __name__ == '__main__':
    try:
        run_scenario()
    except KeyboardInterrupt:
        print(f"\nscript: KeyboardInterrupt, exiting ...")
        quit(0)
