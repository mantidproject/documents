import time
import getpass
import os
from github import Github

# constants
WAIT_TIME = 2 # Work around Github Secondary Rate Limits
TOKEN_ENV_NAME = "CREATE_ISSUES_TOKEN"

def get_github_repo(repo_name: str):
    gh = Github(github_oauth_token())
    return gh.get_repo(repo_name)

def check_token(repo_name):
    try:
        get_github_repo(repo_name)
    except:
        print(f"Bad token for {repo_name}; check authorization scope is set to repo_public and try again")
        return 1
    else:
        print("The token worked!")
        return 0

def github_oauth_token() -> str:
    """Retrieve the oauth token for authenticating with GitHub
    Checks for CREATE_ISSUES_TOKEN env variable and falls back to
    asking on the command line
    """
    token = os.environ.get(TOKEN_ENV_NAME, None)
    if token is None:
        token = getpass.getpass(prompt=f"Enter GitHub personal access token:")

    return token


class GitHubRepo:
    def __init__(self, repo_name):
        self.repo = get_github_repo(repo_name)

    def get_possible_assignees(self):
        return {user.login for user in self.repo.get_assignees()}
    
    def get_matching_milestone(self, milestone_title):
        gh_milestone = None
        for loop_milestone in self.repo.get_milestones():
            if loop_milestone.title == milestone_title:
                gh_milestone = loop_milestone
        return gh_milestone

    def get_matching_labels(self, issue_labels: dict[str, str]):
        gh_labels = {}
        for key, label in issue_labels.items():
            gh_label = self.repo.get_label(label)
            if gh_label is not None:
                gh_labels[key] = gh_label
        return gh_labels
    
    def create_issue(self, title, *, body, milestone, labels, assignees):
        time.sleep(WAIT_TIME)
        issue = self.repo.create_issue(title, body=body, milestone=milestone, labels=labels)
        if len(assignees) > 0:
            issue.add_to_assignees(*assignees)
        return issue