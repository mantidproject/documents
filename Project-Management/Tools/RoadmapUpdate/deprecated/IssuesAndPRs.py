import requests

import json
from oauth2client.client import SignedJwtAssertionCredentials

#disable a warning about being insecure
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

#Control variables
sheet_name = "Mantid Roadmap"
tab_name = "All Tasks"
dry_run = True

# Package requirements
# pip install pyOpenSSL
# pip install requests
# pip install gspread
# pip install oauth2client==1.5.2

# script requirements
# The script must be in the same directory as the oauth2 file
#   MantidUpdateRoadmap-c75ebc2eae19.json
# The sheet to be updated must have been shared for update with
#   mantidupdateroadmap@appspot.gserviceaccount.com
# There must be a file "login.txt" with your github username and password
# in the script directory (one per line)
#   Do not submit that to github

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

def clean_milestone(github_milestone):
    ''' Cleans the hithub milestone string
    :param github_milestone: the milestone string from Github
    :return: A cleaned version of the string
    '''
    return github_milestone.replace("Release","").strip()

def parse_priority(label_list):
    ''' Transaltes the labels to a priority string
    :param label_list: The list of json labels from gitbub
    :return: A string of the priority
    '''
    priority = "2-Medium"
    for label in label_list:
        if label["name"] == "High Priority":
            priority = "1-High"
        if label["name"] == "Low Priority":
            priority = "3-Low"
    return priority

def list_issues(username=None,password=None):
    ''' extract the issue datils
    :return: A dictionary object of the issues
    '''

    github_root = 'https://api.github.com/repos/mantidproject/mantid/issues?state=closed&page='

    page_num=1
    should_continue = True
    ret_dictionary = {}
    while should_continue:
        print github_root + str(page_num)
        if username is None:
            r = requests.get(github_root + str(page_num))
        else:
            r = requests.get(github_root + str(page_num), auth=(username, password))
        if(r.ok):
            milestone = ""
            owner = ""
            list_json = json.loads(r.text or r.content)
            print len(list_json)
            if len(list_json) == 0:
                should_continue = False
            for issue_json in list_json:
                try:
                    milestone = clean_milestone(issue_json["milestone"]["title"])
                except TypeError:
                    milestone = None
                try:
                    owner = issue_json["assignee"]["login"]
                except TypeError:
                    owner = None
                type = "Issue"
                if "pull_request" in issue_json:
                    type = "PR"
                try:
                    ret_dictionary[owner][milestone][type] += 1
                except KeyError:
                    if owner not in ret_dictionary.keys():
                        ret_dictionary[owner] = {}
                    if milestone not in ret_dictionary[owner].keys():
                        ret_dictionary[owner][milestone] = {}
                    ret_dictionary[owner][milestone][type] = 1
            print ret_dictionary
            page_num+=1
            print page_num
        else:
            print "Not OK", r.content
            should_continue = False
    return ret_dictionary

#extract the details for the issues from github
username, password = load_login_details("login.txt")
updated_cells = []
result_dict = list_issues(username, password)
print "developer","milestone","Issues","PRs Tested"
for developer in result_dict.keys():
    for milestone in result_dict[developer].keys():
        issues = 0
        prs = 0
        try:
            issues = result_dict[developer][milestone]["Issue"]
        except KeyError:
            issues = 0
        try:
            prs = result_dict[developer][milestone]["PR"]
        except KeyError:
            prs = 0
        print developer,milestone,issues,prs

print "Completed"