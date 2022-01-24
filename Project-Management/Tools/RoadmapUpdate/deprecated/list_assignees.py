import sys
from github import Github


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


for assignee in repo.get_assignees():
	print assignee.login, '"' + str(assignee.name) + '"'

