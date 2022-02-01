import sys
from github import Github
import pandas as pd
# also needs xlrd



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
        print "Trouble loading login details from", filename
        print "There must be a file ", filename, " with your github username and password"
        print "in the script directory (one per line)"
        print "We will continue anonymously, but expect rate limit problems"
    finally:
        file.close()
    return user, pswd

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
# will be loaded from login.txt
USERNAME, PASSWORD = load_login_details("login.txt")

# The repository to add this issue to
REPO_OWNER = 'mantidproject'
REPO_NAME = 'mantid'

gh = Github(USERNAME, PASSWORD)
repo = gh.get_user(REPO_OWNER).get_repo(REPO_NAME)
assingnees = repo.get_assignees()

#Lookup milestone sting to get number
milestone = "Release 4.1"
gh_milestone = None
for loop_milestone in repo.get_milestones():
	if loop_milestone.title == milestone:
		gh_milestone = loop_milestone
if gh_milestone is None:
	print "could not find milestone " + milestone
	sys.exit(0)
print "Milestone", gh_milestone.number, gh_milestone.title

labels = ['Quality: Manual Tests']
#translate the label strings into gh objects
gh_labels = []
for label in labels:
	gh_label = repo.get_label(label)
	if gh_label is not None:
		gh_labels.append(gh_label)

print "Labels", gh_labels


body_text = '''1. Read http://www.mantidproject.org/Unscripted_Manual_Testing
1. Comment against this ticket the OS environment you are testing against.
1. Don't spend more than a few hours on the testing as fatigue will kick in.
1. If you find errors in the possibly scant documentation, then correct them.
1. Close the this issue once you are done.

If you find bugs:
* Search to see if an issue already exists
* create an issue if it is new
 * Urgent bugs or crashes should by against the current release, and assigned to a developer, then go and talk to the developer if possible.
 * Less urgent bugs should be against a subsequent release, and assigned if the correct developer is known.
'''

#df = pd.DataFrame(list(issue_dict.iteritems()), columns=["Title","Additional Body Text"])
#df.to_csv("issue_template.csv")
print "\nLoading Issues"
df = pd.read_excel("issue_template.xlsx","issues")

print "\nCreating Issues"
for index, row in df.iterrows():
    title =  row['Title']
    additional_body = row['Additional Body Text'] 
    assignee =  row['Assignee']
    gh_assignee = None
    if pd.notnull(assignee):
        for loop_assignee in assingnees:
            if loop_assignee.login == assignee:
                gh_assignee = assignee
        if gh_assignee is None:
        	print "could not find gh assignee for ", assignee, ". Continuing without assignment."

    my_body = body_text
    if pd.notnull(additional_body):
        my_body += "\n\n### Specific Notes:\n\n" + additional_body
    #print title,gh_assignee,gh_milestone,gh_labels
    issue = repo.create_issue(title,my_body,gh_assignee,gh_milestone,gh_labels)
    print issue.number, issue.title

