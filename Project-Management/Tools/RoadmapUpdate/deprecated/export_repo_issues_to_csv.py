"""
Exports Issues from a specified repository to a CSV file

Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
"""
import csv
import requests

githubCalls = 0

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
ISSUES_FOR_REPO_URL = 'http://api.github.com/repos/%s/issues?state=all' % REPO
AUTH = (GITHUB_USER, GITHUB_PASSWORD)

def write_issues(response):
    "output a list of issues to csv"
    lookupCalls = 0
    if not r.status_code == 200:
        raise Exception(r.status_code)
    for issue in r.json():
        assignee = '' if issue['assignee'] is None else issue['assignee']['login'].encode('utf-8')
        milestone ='' if  issue['milestone'] is None else issue['milestone']['title'].encode('utf-8')
        isPR = 'Y' if 'pull_request' in issue else 'N'

        if ('pull_request' in issue) and (issue['assignee'] is None):
             #try to look up a name from the reviews
            reviewer = get_approving_reviewer(issue['number'])
            lookupCalls += 1
            if reviewer is not None:
                assignee = reviewer

        csvout.writerow([issue['number'],
                         issue['title'].encode('utf-8'),
                         issue['state'].encode('utf-8'),
                         issue['created_at'][0:10],
                         issue['updated_at'][0:10],
                         assignee,
                         isPR,
                         issue['user']['login'].encode('utf-8'),
                         milestone
                        ])
    return lookupCalls


def get_approving_reviewer(prId):
    "Tries to get the name of the approving reviewer from github, or None on failure"
    REVIEWS_FOR_PR_URL = 'http://api.github.com/repos/%s/pulls/%s/reviews' % (REPO, prId)
    reviews = requests.get(REVIEWS_FOR_PR_URL, auth=AUTH)
    for review in reviews.json():
        if review['state'].encode('utf-8') == "APPROVED":
            return review['user']['login'].encode('utf-8')
    return None

r = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)
githubCalls += 1
csvfile = '%s-issues.csv' % (REPO.replace('/', '-'))
csvout = csv.writer(open(csvfile, 'wb'))
csvout.writerow(('id', 'Title', 'State', 'Created At', 'Updated At', 'Assignee', 'isPR','Author', 'milestone'))
githubCalls += write_issues(r)
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
        githubCalls += 1
        githubCalls += write_issues(r)
        page_count += 1
        print("Written page %s" % page_count)
        if pages['next'] == pages['last']:
            break
        pages = dict(
            [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])


print("Finished, %s calls to the Github API" % githubCalls)