import sys
from github import Github
import pandas as pd
import xlrd

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
# USERNAME = 'keeeto'
# PASSWORD = '******'
# The repository to add this issue to
REPO_NAME = 'mantid'
REPO_OWNER = 'mantidproject'

gh = Github(USERNAME, PASSWORD)
repo = gh.get_user(REPO_OWNER).get_repo(REPO_NAME)
assignees = repo.get_assignees()

#Lookup milestone sting to get number
milestone = "Release 4.2"
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
You have been assigned unscripted testing. The hope is to catch as many problems with the code before release, so it would be great if you can take some time to give a serious test to your assigned area. Thank you!!

The general guide to unscripted testing:

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

print( "\nLoading Issues")
df = pd.read_excel("issue_template.xlsx","issues")

print( "\nCreating Issues")
for index, row in df.iterrows():
    title =  row['Title']
    additional_body = row['Additional Body Text'] 
    assignee =  row['Assignee']
    gh_assignee = None
    if pd.notnull(assignee):
        for loop_assignee in assignees:
            if loop_assignee.login == assignee:
                gh_assignee = assignee
        if gh_assignee is None:
            print( "could not find gh assignee for ", assignee, ". Continuing without assignment.")

    my_body = body_text
    if pd.notnull(additional_body):
        my_body += "\n\n### Specific Notes:\n\n" + additional_body
    print (title,gh_assignee,gh_milestone,gh_labels)
    issue = repo.create_issue(title, my_body, gh_assignee, gh_milestone, gh_labels) #COMMENT THIS OUT TO TEST BEFORE MAKING ISSUES
    print(issue.number, issue.title)
