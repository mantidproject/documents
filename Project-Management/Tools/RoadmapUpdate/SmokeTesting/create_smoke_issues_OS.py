#!/usr/bin/env python
"""Process spreadsheet assigning smoke testing issues
to developers and creates issues on GitHub. It requires a GitHub
access token that can be provided on the command line
"""
import argparse
import sys
import yaml

import os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir)) 
sys.path.insert(0, parent_dir) # Add the parent directory to the beginning of sys.path
from tools import dryrun, github_helper

# Constants
WAIT_TIME = 2 # Work around Github Secondary Rate Limits
DEFAULT_REPOSITORY = "mantidproject/mantid"
ISSUE_LABELS = {
    "smoke": 'Smoke Tests',
    "Windows": 'Windows Only',
    "MacOS": 'macOS Only',
    "Linux": 'Linux Only',
    "IDAaaS": 'IDAaaS Only',
    "MacOS_arm": 'macOS ARM Only'
}
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
        f"Creating smoke testing issues for '{milestone_title}' (GitHub milestone number {gh_milestone.number})"
    )

    # translate the label strings into gh objects
    gh_labels = repo.get_matching_labels(ISSUE_LABELS)

    print("\nLabels: ", gh_labels)
    print("\nLoading Issues")
    with open('issue_template_os.yml', 'r') as f:
        yaml_file = yaml.safe_load(f)
        release = yaml_file["release"]
        OS_instructions = yaml_file["instructions"]
    with open('issue_template.yml', 'r') as f:
        issues = yaml.safe_load(f)["issues"]
    print(f"\nCreating Issues...with {WAIT_TIME} seconds intervals... go make a cup of tea |_|¬\n\n")

    # Create the issues
    for OS_row in OS_instructions:
        operating_system = OS_row["os"]
        additional_instructions = str(OS_row["text"]).format(release)
        body_text_main_OS = f"{additional_instructions }\n{body_text_main}"

        # check the assignees for this OS
        gh_assignees = []
        if OS_row.get('assignee') is not None:
            proposed_assignees = str(OS_row["assignee"]).split(", ")
            for proposed_assignee in proposed_assignees:
                if proposed_assignee in possible_assignees:
                    gh_assignees.append(proposed_assignee)
                else:
                    print(f"Could not find {proposed_assignee} on GitHub. Continuing without assignment.")

        # the labels to use for smoke tests on this OS
        os_labels = [gh_labels["smoke"], gh_labels[operating_system]]

        # make each indivual side issue
        for issue_row in issues:
            test_title = f"{operating_system} {issue_row['title']} {issue_row['emoji']}"
            test_instructions = additional_instructions + "\n"
            test_instructions += f"{body_text_test}{issue_row['emoji']}\n\n{issue_row['body']}"

            issue = repo.create_issue(test_title,
                                         body=test_instructions,
                                         milestone=gh_milestone,
                                         labels=os_labels,
                                         assignees=gh_assignees)
            if cmd_args.verbose:
                print(issue)
            else:
                print(f"{issue.number:<6}\t{issue.milestone}\t{issue.title} {issue.labels}")
            body_text_main_OS += "\n\n- [ ] #" + str(int(issue.number))

        # make the main OS issue for tracking all side issues
        main_title = f"{operating_system} Smoke Tests: {gh_milestone.title}"
        OS_issue = repo.create_issue(main_title,
                                     body=body_text_main_OS,
                                     milestone=gh_milestone,
                                     labels=os_labels,
                                     assignees=gh_assignees)
        print(OS_issue.number, OS_issue.title)
    return 0


def parse_args() -> argparse.Namespace:
    """Parse commandline arguments and return them as a Namespace"""
    parser = argparse.ArgumentParser(
        description="Create GitHub issues for Smoke testing of Mantid")
    parser.add_argument("milestone",
                        help="Title of GitHub milestone for issue assignment")
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
        "--verbose",
        action="store_true",
        default=False,
        help=
        "Print entire task description")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help=
        "If passed, print what would happen but do not perform issue creation")

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
