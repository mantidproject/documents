"""
Exports Issues from a specified repository to a CSV file

Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
"""
import csv
import requests


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


GITHUB_USER = ''
GITHUB_PASSWORD = ''
GITHUB_USER, GITHUB_PASSWORD = load_login_details("login.txt")
REPO = 'mantidproject/mantid'  # format is username/repo
ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues?state=all' % REPO
AUTH = (GITHUB_USER, GITHUB_PASSWORD)

def write_issues(response):
    "output a list of issues to csv"
    if not r.status_code == 200:
        raise Exception(r.status_code)
    for issue in r.json():
        csvout.writerow([issue['number'],
                         issue['title'].encode('utf-8'),
                         issue['state'].encode('utf-8'),
                         issue['created_at'][0:10],
                         issue['updated_at'][0:10],
                         '' if issue['assignee'] is None else issue['assignee']['login'].encode('utf-8'),
                         'Y' if 'pull_request' in issue else 'N',
                         issue['user']['login'].encode('utf-8'),
                         '' if  issue['milestone'] is None else issue['milestone']['title'].encode('utf-8')
                        ])


r = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)
csvfile = '%s-issues.csv' % (REPO.replace('/', '-'))
csvout = csv.writer(open(csvfile, 'wb'))
csvout.writerow(('id', 'Title', 'State', 'Created At', 'Updated At', 'Assignee', 'isPR','Author', 'milestone'))
write_issues(r)
page_count = 1
print("Written page %s" % page_count)

#more pages? examine the 'link' header returned
if 'link' in r.headers:
    pages = dict(
        [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
            [link.split(';') for link in
                r.headers['link'].split(',')]])
    while 'last' in pages and 'next' in pages:
        r = requests.get(pages['next'], auth=AUTH)
        write_issues(r)
        page_count += 1
        print("Written page %s" % page_count)
        if pages['next'] == pages['last']:
            break
        pages = dict(
            [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])


print("Finished")