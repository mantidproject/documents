#!/usr/bin/env python
"""Process spreadsheet assigning smoke testing issues
to developers and creates issues on GitHub. It requires a GitHub
access token that can be provided on the command line
"""
import argparse
import getpass
import os
import sys
import time

from github import Github
import pandas as pd

# Constants
WAIT_TIME = 2 # Work around Github Secondary Rate Limits
DEFAULT_REPOSITORY = "mantidproject/mantid"
TOKEN_ENV_NAME = "CREATE_ISSUES_TOKEN"
ISSUE_LABELS = ['Manual Tests', 'Windows Only', 'macOS Only', 'Linux Only']
body_text_test = '''

**Before testing**:
- Check this testing issue relates to the OS you will test on.
- If unassigned, please assign yourself as for a normal Github issue.
- Please run these tests on the release package of Mantid; **not a locally built version**.

**Afterwards**:
- Comment below with any issues you came across.
- If no major issues were found, please **close this testing issue**.
- Check the main issue for this OS for other unassigned smoke tests.

If you have any questions please contact the creator of this issue.

'''
body_text_main = '''

**Before testing**:
- Check this main issue relates to the OS you will test on.
- Tick the box beside a testing issue listed below to mark *you are testing this issue*
- Enter the testing task issue and assign yourself as for a normal Github issue.

**Afterwards**:
- Comment on the testing issue with any issues you came across.
- If no major issues were found, please **close the testing issue**.

If you have any questions please contact the creator of this issue.

### Tick below before testing the related issue

'''

def main() -> int:
    """
    Main entry point
    """
    cmd_args = parse_args()

    gh = Github(github_oauth_token())
    repo = gh.get_repo(cmd_args.repository)
    possible_assignees = repo.get_assignees()

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
        f"Creating smoke testing issues for '{milestone_title}' (GitHub milestone number {gh_milestone.number})"
    )

    # translate the label strings into gh objects
    gh_labels = []
    for label in ISSUE_LABELS:
        gh_label = repo.get_label(label)
        if gh_label is not None:
            gh_labels.append(gh_label)

    print("\nLabels: ", gh_labels)
    print("\nLoading Issues")
    OS_instructions = pd.read_excel("issue_template.xlsx", "OS instructions")
    issues = pd.read_excel("issue_template.xlsx", "issues")
    print(f"\nCreating Issues...with {WAIT_TIME} seconds intervals... go make a cup of tea |_|¬\n\n")

    for num, OS_row in OS_instructions.iterrows():
        operating_system = OS_row["Operating System"]
        additional_instructions = OS_row["Additional Instructions"]
        body_text_main_OS = additional_instructions + "\n"
        body_text_main_OS += body_text_main

        proposed_assignees = str(OS_row['Assignee']).split(", ")
        gh_assignees = []
        if pd.notnull(OS_row['Assignee']):
            for loop_proposed_assignee in proposed_assignees:
                for loop_possible_assignee in possible_assignees:
                    if loop_possible_assignee.login == loop_proposed_assignee:
                        gh_assignees.append(loop_proposed_assignee)
                if not gh_assignees:
                    print("could not find gh assignee for ", loop_proposed_assignee,
                          ". Continuing without assignment.")

        for index, issue_row in issues.iterrows():
            test_title = operating_system + " " + issue_row['Title'] + " " + issue_row['Emoji']
            test_instructions = additional_instructions + "\n"
            test_instructions += body_text_test + issue_row['Emoji'] + "\n\n" + issue_row['Additional Body Text']

            if not cmd_args.dry_run:
                time.sleep(WAIT_TIME)
                issue = repo.create_issue(test_title,
                                          body=test_instructions,
                                          milestone=gh_milestone,
                                          labels=[gh_labels[0], gh_labels[num + 1]])
                print(issue.number, issue.title)
                body_text_main_OS += "\n\n- [ ] #" + str(int(issue.number))

            else: # in case of dry run
                print(test_title, gh_milestone, [gh_labels[0], gh_labels[num + 1]])

        main_title = operating_system + " Smoke Tests: " + gh_milestone.title
        if not cmd_args.dry_run:
            time.sleep(WAIT_TIME)
            OS_issue = repo.create_issue(main_title,
                                         body=body_text_main_OS,
                                         milestone=gh_milestone,
                                         labels=[gh_labels[0], gh_labels[num + 1]])
            if gh_assignees:
                for gh_assignee in gh_assignees:
                    OS_issue.add_to_assignees(gh_assignee)
            print("Main Smoke issue for: ", operating_system, OS_issue.number, OS_issue.title, "\n\n")

        else: # in case of dry run
            print("Main Smoke issue for: ", operating_system, main_title, gh_milestone, [gh_labels[0], gh_labels[num + 1]], "\n\n")
    return 0


def parse_args() -> argparse.Namespace:
    """Parse commandline arguments and return them as a Namespace"""
    parser = argparse.ArgumentParser(
        description="Create GitHub issues for Smoke testing of Mantid")
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
