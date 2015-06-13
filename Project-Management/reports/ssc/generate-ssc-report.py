from __future__ import (absolute_import, division, print_function, unicode_literals)

__author__ = 'Stuart Campbell'

import argparse
import json
import os
import requests
import shutil

def generate_tablerow_from_issue(ticket):
    issue_text = '[{0}](https://github.com/mantidproject/mantid/issue/{0})'.format(str(ticket['number']))
    milestone = ticket['milestone']
    assignee = ticket['assignee']
    if assignee is not None:
        login = assignee['login']
    else:
        login = ''
    if milestone is not None:
        milestone_title = milestone['title']
    else:
        milestone_title = ''

    priority = 'NORMAL'
    if 'labels' in ticket:
        labels = ticket['labels']
        for label in labels:
            if label['name'] is 'High Priority':
                priority = "LOW"
            if label['name'] is 'High Priority':
                priority = "HIGH"

    _row_data = '| {0} | {1} | {2} | {3} | {4} | {5} | \n' \
        .format(issue_text,
                ticket['title'],
                milestone_title,
                login,
                ticket['state'],
                priority)

    return _row_data


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('template', type=str, help='Template for Report')
    args = parser.parse_args()
    inputTemplate = args.template

    print('Parsing temple file: {0}'.format(inputTemplate))
    filename = inputTemplate.replace('template', 'report')
    print('Generating report : {0}'.format(filename))

    # Try and read the auth token from an environment variable
    token = os.getenv('GITHUB_CI_TOKEN')
    if token is not None:
        _header = {'Authorization': ' token {0}'.format(token)}
        print("Performing authenticated query.")
    else:
        _header = {}
        print("Performing unauthenticated query.")

    if not os.path.isfile(inputTemplate):
        print("ERROR: Specified file does not exist.")
        exit()

    # If report already exists, then back it up.
    if os.path.exists(filename):
        shutil.copy(filename, '{0}.bak'.format(filename))

    infile = open(inputTemplate, 'r')
    outfile = open(filename, "w")

    json_section = False
    json_buffer = ''
    output_data = ''
    total_tickets = 0

    for line in infile:
        if line.startswith('START>>>'):
            # print('START>>>')
            json_section = True
            continue

        # Reached the section end - now parse it.
        if line.startswith('<<<END'):
            # print('<<<END')
            json_section = False

            rawdata = json.loads(json_buffer)
            # Now clear the json data buffer in case we need to use
            # it for another data section
            json_buffer = ''

            # print(type(rawdata))

            if type(rawdata) is dict:
                template_data = [rawdata]
            else:
                template_data = rawdata

            table_data = '| Issue | Title | Milestone | Assignee | State | Priority | \n'
            table_data += '| ----- | ----- | --------- | -------- | ----- | -------- | \n'

            # Construct the query
            query_data = {}
            query_url = ''

            for data in template_data:

                if 'labels' in data:
                    query_data['state'] = 'all'
                    query_data['filer'] = 'all'
                    query_data['labels'] = data['labels']
                    query_url = 'https://api.github.com/repos/mantidproject/mantid/issues'

                if 'issue' in data:
                    query_url = 'https://api.github.com/repos/mantidproject/mantid/issues/{0}'.format(
                        str(data['issue']))

                # print(json.dumps(query_data, indent=2))

                # print(query_url)

                r = requests.get(query_url, headers=_header, params=query_data)
                # print(r)

                req_data = r.json()

                if isinstance(req_data, list):
                    for issue in req_data:
                        total_tickets += 1
                        table_data += generate_tablerow_from_issue(issue)
                else:
                    # Single Issue
                    total_tickets += 1
                    table_data += generate_tablerow_from_issue(req_data)

            outfile.write(table_data)
            continue

        # Either write the raw or generated Markdown to the output file
        if json_section:
            json_buffer += line
        else:
            outfile.write(line)

    # print(json_buffer)

    outfile.write('The total number of issues is {0}.'.format(str(total_tickets)))

    infile.close()
    outfile.close()

    print('Finished.')
