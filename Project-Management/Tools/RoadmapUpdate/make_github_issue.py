import json
import requests

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
# will be loaded from login.txt
USERNAME = 'CHANGEME'
PASSWORD = 'CHANGEME'

# The repository to add this issue to
REPO_OWNER = 'mantidproject'
REPO_NAME = 'mantid'

def make_github_issue(title, body=None, assignee=None, milestone=None, labels=None):
    '''Create an issue on github.com using the given parameters.'''
    # Our url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    # Create an authenticated session to create the issue
    session = requests.session()
    session.auth=(USERNAME, PASSWORD)
    # Create our issue
    issue = {'title': title,
             'body': body,
             'assignee': assignee,
             'milestone': milestone,
             'labels': labels}
    # Add the issue to our repository
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        print 'Successfully created Issue "%s"' % title
    else:
        print 'Could not create Issue "%s"' % title
        print 'Response:', r.content


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


USERNAME, PASSWORD = load_login_details("login.txt")
#could do with a find milestone number for name at some point
milestone = 5
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
assignee = None
labels = ['Quality: Manual Tests']

issue_dict = {
    'Unscripted Testing Mantidplot Group 1' : None,
    'Unscripted Testing Mantidplot Group 2' : None,
    'Unscripted Testing Mantidplot Group 3' : None,
    'Unscripted Testing Mantidplot Group 4' : None,
    'Unscripted Testing Live Data ISIS' : None,
    'Unscripted Testing Live Data ORNL' : None,
    'Unscripted Testing Workspace Groups' : 'Ensure MantidPlot displays Group Workspaces correctly in the workspace tree',
    'Unscripted Testing Documentation' : '''Qt Assistant offline documentation
* Algorithm, fit, concept and api pages should be generated
* Algorithm dialog snapshots should appear on algorithm pages in offline help
* Math formulae should appear on algorithm pages in offline help
* workflow diagrams should appear on algorithm pages in offline help''',
    'Unscripted Testing ORNL SANS' : None,
    'Unscripted Testing ORNL HFIR diffraction & 4Circle' : None,
    'Unscripted Testing ORNL Powder Diffraction' : 'See http://www.mantidproject.org/PowderDiffractionReduction',
    'Unscripted Testing ISIS SANS' : 'See http://www.mantidproject.org/SANS_Data_Analysis_at_ISIS',
    'Unscripted Testing Muon' : '''As a minimum test http://www.mantidproject.org/Unscripted_Manual_Testing_MuonAnalysis.
For more info see http://www.mantidproject.org/Muon''',
    'Unscripted Testing DGSReduction' : '''See http://www.mantidproject.org/Direct:DgsReduction
     and http://www.mantidproject.org/Create_MD_Workspace_GUI#Direct_Inelastic_Mod_Q''',
    'Unscripted Testing DGSPlanner' : None,
    'Unscripted Testing DynamicPDF' : None,
    'Unscripted Testing Multi dataset fitting' : None,
    'Unscripted Testing Sample Transmission calculator' : None,
    'Unscripted Testing Step scan analysis' : 'See http://www.mantidproject.org/Step_Scan_Interface',
    'Unscripted Testing ISIS Indirect interfaces' : '''See
* http://www.mantidproject.org/Indirect:ConvertToEnergy
* http://www.mantidproject.org/Indirect:Indirect_Data_Analysis
* http://www.mantidproject.org/UsingElwin
* http://www.mantidproject.org/UsingFury
    ''',
    'Unscripted Testing SCD event data reduction' : None,
    'Unscripted Testing Engineering Diffraction' : None,
    'Unscripted Testing ISIS Reflectometry' : 'For testing procedures see http://www.mantidproject.org/Testing_ISIS_Reflectometry_GUI',
    'Unscripted Testing ORNL reflectometry interfaces, REFL reduction, Refl SF Calculator, REFM reduction' : None,
    'Unscripted Testing FilterEvents' : None,
    'Unscripted Testing QECoverage' : None,
    'Unscripted Testing TofConverter' : None,
    'Unscripted Testing Vates' : 'Including data loading in Vates via ParaView. For help see [[Testing_Notes_2.5.0|here]]'
}

for title, additional_body in issue_dict.iteritems():
    my_body = body_text
    if additional_body is not None:
        my_body += "\n\n### Specific Notes:\n\n" + additional_body
    print "\n\n" + title
    print  my_body
    make_github_issue(title, my_body, assignee, milestone, labels)
