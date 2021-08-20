#!/usr/bin/env python
"""Process spreadsheet assigning manual testing issues
to developers and creates issues on GitHub. It requires a GitHub
access token that can be provided on the command line
"""
import argparse
import getpass
import os
import sys

from github import Github
import pandas as pd

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
* Close the this issue once you are done.
'''
ISSUE_LABELS = ["Manual Tests"]


def main() -> int:
    """
    Main entry point
    """
    cmd_args = parse_args()

    gh = Github(github_oauth_token())
    repo = gh.get_repo(cmd_args.repository)
    assignees = repo.get_assignees()

    # Lookup milestone string to get number
    milestone_title = cmd_args.milestone
    gh_milestone = None
    for loop_milestone in repo.get_milestones():
        if loop_milestone.title == milestone_title:
            gh_milestone = loop_milestone
    if gh_milestone is None:
        print(f"Unable to find a milestone with title '{milestone_title}'",
              file=sys.stderr)
        return 1
    print(
        f"Creating manual testing issues for '{milestone_title}' (GitHub milestone number {gh_milestone.number})"
    )

    # translate the label strings into gh objects
    gh_labels = []
    for label in ISSUE_LABELS:
        gh_label = repo.get_label(label)
        if gh_label is not None:
            gh_labels.append(gh_label)

    print("Labels", gh_labels)
    print("\nLoading issue assignment spreadsheet")
    df = pd.read_excel(cmd_args.assignment_spreadsheet, "issues")

    print(f"\nCreating {len(df.index)} issues")
    for _, row in df.iterrows():
        title = str(row['Title']).strip()
        additional_body = str(row['Additional Body Text']).strip()
        gh_labels = [repo.get_label('Manual Tests')]
        assignee = row['Assignee']
        gh_assignee = None
        if pd.notnull(assignee):
            for loop_assignee in assignees:
                if loop_assignee.login == assignee:
                    gh_assignee = assignee
            if gh_assignee is None:
                print("could not find gh assignee for ", assignee,
                      ". Continuing without assignment.")

        my_body = BODY_TEXT
        if pd.notnull(additional_body):
            my_body += "\n\n### Specific Notes:\n\n" + additional_body
        print(title, gh_milestone, gh_labels, gh_assignee)
        if not cmd_args.dry_run:
            issue = repo.create_issue(title,
                                      body=str(my_body).strip(),
                                      milestone=gh_milestone,
                                      labels=gh_labels,
                                      assignee=gh_assignee)
            print(issue.number, issue.title)

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
        "--dry-run",
        action="store_true",
        default=False,
        help=
        "If passed, print what would happen but do not perform issue creation")

    return parser.parse_args()


def github_oauth_token() -> str:
    """Retrieve the oauth token for authenticating with GitHub
    Checks for CREATE_ISSUES_TOKEN env variable and falls back to
    asking on the command line
    """
    token = os.environ.get(TOKEN_ENV_NAME, None)
    if token is None:
        token = getpass.getpass(prompt=f"Enter GitHub personal access token:")

    return token


if __name__ == "__main__":
    sys.exit(main())
