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


def print_group_utilization(file):
    import yaml
    assignee_counts = dict()
    tottime = 0
    with open(file, 'r') as f:
        issues = yaml.safe_load(f)["issues"]
    for row in issues:
        # get the assignees from the string
        assignee = row.get('assignee')
        if not assignee:
            title = str(row['title']).strip()
            print(f"Warning: No valid assignees found for issue {title}.")
        # now update counts
        avgtime = 0
        if row.get("times"):
            times = [x for x in row["times"] if x is not None]
            avgtime = sum(times)/len(times)
            tottime += avgtime
        assignee_counts[assignee] = assignee_counts.get(assignee, 0) + avgtime

    # this is the case for Non-ISIS assignments; simply count number of tasks
    if tottime == 0:
        for row in issues:
            assignee = row.get('assignee')
            if assignee:
                assignee_counts[assignee] = assignee_counts.get(assignee, 0) + 1
        tottime = len(issues)
    namesize = max([len(x) for x in assignee_counts.keys()])
    
    for assignee, count in assignee_counts.items():
        print(f"{assignee.ljust(namesize)}\t\tassigned to\t{count:.0f} of {tottime:.0f}")


def print_smoketest_utilization(osfile, taskfile):
    import yaml
    assignee_counts = dict()

    with open(taskfile, 'r') as f:
        issues = yaml.safe_load(f)["issues"]
    tasks_per_os = len(issues)

    with open(osfile, 'r') as f:
        yaml_file = yaml.safe_load(f)

    instructions = yaml_file["instructions"]
    for instruction in instructions:
        assignee = instruction["assignee"]
        assignee_counts[assignee] = assignee_counts.get(assignee, 0) + tasks_per_os
            
    namesize = max(assignee_counts.values())    
    for assignee, count in assignee_counts.items():
        print(f"{assignee.ljust(2 * namesize)}\t\tassigned to\t{count} of {len(issues) * len(instructions)}")


class DryRunIssue:
    number: int = 0

    def __init__(self, title, body, milestone, labels, assignees = None):
        self.title = title
        self.body = body
        self.milestone = milestone
        self.labels = labels
        self.assignees = assignees if assignees is not None else []
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
            self.milestones = {}
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
        
    def create_issue(self, title, *, body, milestone, labels, assignees):
        issue = DryRunIssue(title, body, milestone, labels, assignees)
        return issue
