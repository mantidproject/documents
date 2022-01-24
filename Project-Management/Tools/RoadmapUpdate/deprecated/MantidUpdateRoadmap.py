import requests

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

#disable a warning about being insecure
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

#Control variables
sheet_name = "Mantid Roadmap"
tab_name = "All Tasks"
dry_run = False

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
        if label["name"] == "Priority: High":
            priority = "1-High"
        if label["name"] == "Priority: Low":
            priority = "3-Low"
    return priority

def get_issue_details(issue,username=None,password=None):
    ''' extract the issue datils ofr an issue number from github
    :param issue: The issue number
    :return: A dictionary object of the details
    '''

    github_root = 'https://api.github.com/repos/mantidproject/mantid/issues/'

    if username is None:
        r = requests.get(github_root + str(issue))
    else:
        r = requests.get(github_root + str(issue), auth=(username, password))
    if(r.ok):
        ret_dictionary = {}
        ret_dictionary["issue"] = issue
        issue_json = json.loads(r.text or r.content)
        ret_dictionary["title"] = issue_json["title"]
        ret_dictionary["state"] = issue_json["state"]
        try:
            ret_dictionary["milestone"] = clean_milestone(issue_json["milestone"]["title"])
        except TypeError:
            ret_dictionary["milestone"] = None
        try:
            ret_dictionary["owner"] = issue_json["assignee"]["login"]
        except TypeError:
            ret_dictionary["owner"] = None
        ret_dictionary["priority"] = parse_priority(issue_json["labels"])
        print ret_dictionary
        return ret_dictionary
    else:
        print "Not OK", r.content
        return None

def get_cell_range(wks,from_row,from_col):
    ''' Gets a cell range of one column from the title to the end of the sheet
    :param wks: the worksheet
    :param from_row: the row of the title
    :param from_col: the column of the title
    :return: a list of the cells
    '''
    range_string = wks.get_addr_int(from_row, from_col) + ":" + \
                   wks.get_addr_int(wks.row_count, from_col)
    print "range_string", range_string
    return wks.range(range_string)

def update_cell(cell,new_value,updated_cells):
    ''' Updates a cell if the value differs and add it to a list of updated cells
    :param cell: The cell to update
    :param new_value: the new value to use
    :param updated_cells: The list of cell that have been updated
    :return: Nothing
    '''
    if cell.value != new_value:
        if new_value is None:
            cell_value = ""
        else:
            cell.value = new_value
        updated_cells.append(cell)

print "Authenticating with google sheets"
json_key = json.load(open('MantidUpdateRoadmap-c75ebc2eae19.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
gc = gspread.authorize(credentials)

print "Opening",sheet_name, ", tab", tab_name
wks = gc.open(sheet_name).worksheet(tab_name)

#find the titles
print "Determining cell ranges"
issue_coltitle_cell = wks.find("Issue")
priority_coltitle_cell = wks.find("Priority")
status_coltitle_cell = wks.find("Status")
owner_coltitle_cell = wks.find("Owner")
milestone_coltitle_cell = wks.find("Milestone")

#get the cell ranges (matched lists)
issue_cell_range = get_cell_range(wks,issue_coltitle_cell.row,issue_coltitle_cell.col)
priority_cell_range = get_cell_range(wks,issue_coltitle_cell.row,priority_coltitle_cell.col)
status_cell_range = get_cell_range(wks,issue_coltitle_cell.row,status_coltitle_cell.col)
owner_cell_range = get_cell_range(wks,issue_coltitle_cell.row,owner_coltitle_cell.col)
milestone_cell_range = get_cell_range(wks,issue_coltitle_cell.row,milestone_coltitle_cell.col)

print "Searching for issue numbers"
#get the issues
issue_row_hash = {}
for idx, cell in enumerate(issue_cell_range):
    if cell.value is not None:
        try:
            issue_num = int(cell.value)
            if issue_num > 0:
                issue_row_hash[issue_num] = idx
        except ValueError:
            pass

print "Found", len(issue_row_hash), "issues"

#extract the details for the issues from github
username, password = load_login_details("login.txt")
updated_cells = []
for issue in issue_row_hash.keys():
    issue_details = get_issue_details(issue, username, password)
    #update cells that do not match
    issue_idx = issue_row_hash[issue]
    update_cell(owner_cell_range[issue_idx],issue_details["owner"],updated_cells)
    update_cell(status_cell_range[issue_idx],issue_details["state"],updated_cells)
    update_cell(milestone_cell_range[issue_idx],issue_details["milestone"],updated_cells)
    # don't update the priority if it is custom (longer than the max label length)
    if len(priority_cell_range[issue_idx].value) <= len("2-Medium"):
        update_cell(priority_cell_range[issue_idx],issue_details["priority"],updated_cells)

if dry_run:
    print "Dry Run - Would update the worksheet with", len(updated_cells), "cells"
else:
    print "Updating the worksheet with", len(updated_cells), "cells"
    wks.update_cells(updated_cells)
print "Completed"