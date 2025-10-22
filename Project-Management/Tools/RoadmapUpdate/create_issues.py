#!/usr/bin/env python
"""Process spreadsheet assigning manual testing issues
to developers and creates issues on GitHub. It requires a GitHub
access token that can be provided on the command line
"""
import argparse
import sys
import yaml

from tools import dryrun, github_helper

# Constants
DEFAULT_REPOSITORY = "mantidproject/mantid"
TOKEN_ENV_NAME = "CREATE_ISSUES_TOKEN"
BODY_TEXT = '''
You have been assigned manual testing. The hope is to catch as many problems with the code before release, so it would be great if you can take some time to give a serious test to your assigned area. Thank you!!

The general guide to manual testing:

* The tests must be performed on the installer versions of the final release candidate. Not on local compiled code.
* Serious errors involving loss of functionality, crashes etc. should be raised
as issues with the current release as a milestone and an email sent to the project manager immediately.
* Minor and cosmetic issues should be raised as issues against the forthcoming
releases.
* First try things that should work, then try to break Mantid, e.g. entering invalid values, unexpected characters etc.
* Don't spend more than a few hours on the testing as fatigue will kick in.
* If you find errors in the documentation, please correct them.
* Comment against this ticket the OS environment you are testing against.
* Disable Usage reporting before you start testing
* Close the this issue once you are done.
* Time how long this manual test takes for you to do and leave a comment about it in this issue.
'''
ISSUE_LABELS = {"manual": "Manual Tests"}


def main() -> int:
    """
    Main entry point
    """
    cmd_args = parse_args()

    # if checking token, make sure it is valid and then stop
    if cmd_args.check_token:
        return github_helper.check_token(cmd_args.repository)

    # setup the repo
    if cmd_args.dry_run:
        repo = dryrun.DryRunRepo(cmd_args.repository)
    else:
        repo = github_helper.GitHubRepo(cmd_args.repository)

    possible_assignees = repo.get_possible_assignees()

    # Lookup milestone string to get number
    milestone_title = cmd_args.milestone
    gh_milestone = repo.get_matching_milestone(milestone_title)
    if gh_milestone is None:
        print(f"Unable to find a milestone with title '{milestone_title}'",
              file=sys.stderr)
        return 1
    print(
        f"Creating manual testing issues for '{milestone_title}' (GitHub milestone number {gh_milestone.number})"
    )

    # translate the label strings into gh objects
    gh_labels = list(repo.get_matching_labels(ISSUE_LABELS).values())

    print("Labels", gh_labels)
    print("\nLoading issue assignment spreadsheet")
    with open(cmd_args.assignment_spreadsheet, 'r') as f:
        issues = yaml.safe_load(f)["issues"]
    print(f"\nCreating {len(issues)} issues")
    for row in issues:
        title = str(row['title']).strip()
        additional_body = row.get('body')
        if additional_body is not None:
            additional_body = str(additional_body).strip()
        assignee_str = row.get('assignee')
        proposed_assignees = str(assignee_str).split(", ") if assignee_str else []
        gh_assignees = []
        for proposed_assignee in proposed_assignees:
            if proposed_assignee in possible_assignees:
                gh_assignees.append(proposed_assignee)
            if not gh_assignees:
                print("could not find gh assignee for ", proposed_assignee,
                        ". Continuing without assignment.")

        my_body = BODY_TEXT
        if additional_body is not None:
            my_body += "\n\n### Specific Notes:\n\n" + additional_body
        print(title, gh_milestone, gh_labels, gh_assignees)
        issue = repo.create_issue(title,
                                    body=str(my_body).strip(),
                                    milestone=gh_milestone,
                                    labels=gh_labels,
                                    assignees=gh_assignees)
        print(issue.number, issue.title, issue.assignees)

    return 0


def parse_args() -> argparse.Namespace:
    """Parse commandline arguments and return them as a Namespace"""
    parser = argparse.ArgumentParser(
        description="Create GitHub issues for Manual testing of Mantid")
    parser.add_argument("milestone",
                        help="Title of GitHub milestone for issue assignment")
    parser.add_argument("assignment_spreadsheet",
                        help="Excel spreadsheet defining test assignments")
    parser.add_argument(
        "--repository",
        type=str,
        default=DEFAULT_REPOSITORY,
        help=
        "GitHub repository where issues should be created specified as org/repo"
    )
    parser.add_argument(
        "--check-token",
        action="store_true",
        default=False,
        help=
        "If passed, only verify that the token can reach the repository")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help=
        "If passed, print what would happen but do not perform issue creation")

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
