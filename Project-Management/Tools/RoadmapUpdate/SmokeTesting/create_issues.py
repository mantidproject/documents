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

milestone = "Release 4.3"
gh_milestone = None
for loop_milestone in repo.get_milestones():
    if loop_milestone.title == milestone:
        gh_milestone = loop_milestone
if gh_milestone is None:
    print( "could not find milestone " + milestone)
    sys.exit(0)
print( "Milestone", gh_milestone.number, gh_milestone.title)

labels = ['Manual Tests']
#translate the label strings into gh objects
gh_labels = []
for label in labels:
    gh_label = repo.get_label(label)
    if gh_label is not None:
        gh_labels.append(gh_label)

print( "Labels", gh_labels)


body_text = '''

Before testing, Edit the Smoke Testing Umbrella Issue to add your name beside the OS you are running this test on.
Then tick the adjacent tick box once testing is complete.

Please run these tests on the compiled package of Mantid; **not a locally compiled version**.
Test MantidPlot AND Workbench!

Comment below with the OS you tested on
and any issues you came across.

If you have any questions please contact the creator of this issue.

'''
print( "\nLoading Issues")
df = pd.read_excel("issue_template.xlsx","issues")
um = pd.read_excel("umbrella_issue_template.xlsx","issues")
print( "\nCreating Issues")
issue_numbers = np.zeros(25)
for index, row in df.iterrows():
    title =  row['Title']
    additional_body = row['Additional Body Text'] 
    my_body = body_text
    if pd.notnull(additional_body):
        my_body += "\n\n## Checklist/directions\n\n" + additional_body
    #print (title,gh_milestone,gh_labels)
    issue = repo.create_issue(title, body = my_body, milestone = gh_milestone, labels = gh_labels) #COMMENT THIS OUT TO TEST BEFORE MAKING ISSUES
    print(issue.number, issue.title)
    issue_numbers[index] = issue.number

my_body = ""
for index, row in um.iterrows():
    additional_body = row['Additional Body Text']
    if pd.notnull(row['Additional Body Text']):
        my_body += additional_body
        if  issue_numbers[index] != 0:
            my_body += str(int(issue_numbers[index]))
        my_body += "\n"
my_body += "\n **Manually make this Umbrella into an Epic!** "       
title = 'Smoke Testing Umbrella Issue'
#print (title,gh_milestone,gh_labels)
issue = repo.create_issue(title, body = my_body, milestone = gh_milestone, labels = gh_labels) #COMMENT THIS OUT TO TEST BEFORE MAKING ISSUES
print(issue.number, issue.title)