from . import github_helper


# Constants
ISSUE_STRING = """
====================================================
Title: {title} Issue #{number}
Milestone: {milestone}
Labels: {labels}
Assignees: {assignees}
Issue Description:\n{body}\n
====================================================
"""


class DryRunIssue:
    number: int = 0

    def __init__(self, title, body, milestone, labels, assignees = []):
        self.title = title
        self.body = body
        self.milestone = milestone
        self.labels = labels
        self.assignees = assignees
        self.number = DryRunIssue.number
        DryRunIssue.number += 1

    def __str__(self):
        return ISSUE_STRING.format(
            title = self.title,
            number = self.number,
            milestone = self.milestone.title,
            labels = self.labels,
            assignees = self.assignees,
            body = self.body,
        )

    def add_to_assignees(self, *args):
        self.assignees.extend(args)


class DryRunMilestone:
    def __init__(self, title, number = 12345):
        self.title = title
        self.number = number

    def __str__(self):
        return self.title


class DryRunRepo:
    def __init__(self, repo_name):
        try:
            gh_repo = github_helper.get_github_repo(repo_name)
        except:
            print("Bad token for GitHub.  Using defaults for dry run values")
            self.assignees = {"Bob", "Steve"}
            self.milestones = set()
        else:
            self.assignees = {user.login for user in gh_repo.get_assignees()}
            self.milestones = {milestone.title: milestone for milestone in gh_repo.get_milestones()}

    def get_matching_milestone(self, milestone_title):
        if len(self.milestones) == 0:
            return DryRunMilestone(milestone_title)
        elif milestone_title in self.milestones:
            return self.milestones[milestone_title]
        else:
            return None
                  
    def get_possible_assignees(self):
        return self.assignees
    
    def get_matching_labels(self, issue_labels: dict[str, str]):
        return issue_labels
        
    def create_issue(self, title, *, body, milestone, labels):
        issue = DryRunIssue(title, body, milestone, labels)
        print(issue)
        return issue
