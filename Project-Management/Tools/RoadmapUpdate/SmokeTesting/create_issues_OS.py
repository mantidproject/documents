import sys
from github import Github
import pandas as pd
import xlrd
import numpy as np
#pip install xlrd, pip install pandas, pip install PyGithub if not already


def load_login_details(filename):
    ''' Loads login details from a simple text file
    :param filename: the filename containing the login details
    :return: the username and password
    '''
    user = None
    pswd = None
    try:
        file = open(filename)
        user = file.readline().strip()
        pswd = file.readline().strip()
    except:
        print( "Trouble loading login details from", filename)
        print( "There must be a file ", filename, " with your github username and password")
        print( "in the script directory (one per line)")
        print( "We will continue anonymously, but expect rate limit problems")
    finally:
        file.close()
    return user, pswd

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
USERNAME, PASSWORD = load_login_details("login.txt")
# will be loaded from login.txt:
# USERNAME = 'DanielMurphy22'
# PASSWORD = '******'
# The repository to add this issue to
REPO_NAME = 'mantid'
REPO_OWNER = 'mantidproject'

gh = Github(USERNAME, PASSWORD)
repo = gh.get_user(REPO_OWNER).get_repo(REPO_NAME)
assignees = repo.get_assignees()

milestone = "Release 6.0"
gh_milestone = None
for loop_milestone in repo.get_milestones():
    if loop_milestone.title == milestone:
        gh_milestone = loop_milestone
if gh_milestone is None:
    print( "could not find milestone " + milestone)
    sys.exit(0)
print( "Milestone", gh_milestone.number, gh_milestone.title)

labels = ['Manual Tests','Windows Only','macOS Only','Linux Only','Linux Only']
#translate the label strings into gh objects
gh_labels = []
for label in labels:
    gh_label = repo.get_label(label)
    if gh_label is not None:
        gh_labels.append(gh_label)

print( "Labels", gh_labels)

body_text_test = '''

Before testing:
- Check this testing issue relates to the OS you will test on.
- If unassigned, please assign yourself as for a normal Github issue.
- Please run these tests on the release package of Mantid; **not a locally built version**.

Afterwards:
- Comment below with any issues you came across.
- If no issues were found, or they are now all resolved, please close the testing issue.
- Check the master issue for this OS for other unassigned smoke tests.

If you have any questions please contact the creator of this issue.

'''

body_text_master = '''

Before testing:
- Check this master issue relates to the OS you will test on.
- Find an unassigned testing issue below and assign yourself.
- Please run these tests on the release package of Mantid; **not a locally built version**.

Afterwards:
- Comment on the testing issue with any issues you came across.
- If no issues were found, or they are now all resolved, please close the testing issue.

If you have any questions please contact the creator of this issue.

'''

print( "\nLoading Issues")
df = pd.read_excel("issue_template.xlsx","issues")
print( "\nCreating Issues")

OS_to_test = ['Windows', 'MacOS', 'Redhat', 'Ubuntu']

for num, OS in enumerate(OS_to_test):
    body_text_master_OS = ""
    if OS == 'Redhat':
        body_text_master_OS += "## If at ISIS, please test on IDAaaS\n\n"
    body_text_master_OS += body_text_master

    for index, row in df.iterrows():
        test_title =  OS + " " + row['Title']
        test_instructions = ""
        if OS == 'Redhat':
            test_instructions += "## If at ISIS, please test on IDAaaS\n\n"
        test_instructions += body_text_test + row['Emoji'] + "\n\n" + row['Additional Body Text'] 

        issue = repo.create_issue(test_title, body = test_instructions, milestone = gh_milestone, labels = [gh_labels[0],gh_labels[num+1]]) #COMMENT THIS OUT TO TEST BEFORE MAKING ISSUES
        print(issue.number, issue.title)

        body_text_master_OS += "\n\n## "+ str(index+1) + ". " + test_title + row['Emoji']
        body_text_master_OS += ' #' + str(int(issue.number))

    master_title = OS + " Smoke Tests: " + milestone  
    print (master_title,gh_milestone,[gh_labels[0],gh_labels[num+1]])
    issue = repo.create_issue(master_title, body = body_text_master_OS, milestone = gh_milestone, labels = [gh_labels[0],gh_labels[num+1]]) #COMMENT THIS OUT TO TEST BEFORE MAKING ISSUES
    print("Master issue for ", OS, issue.number, issue.title)
