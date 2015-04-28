#!/usr/bin/python
import urllib
import urllib2
import os
import getpass
import pac_api
from argparse import ArgumentParser

import ssl

PACPASSFILE='.pacpass'

parser = ArgumentParser()

parser.add_argument("-u",  dest="federalid",
                    help="Your federal id", metavar="Federal ID",required=True)

args = parser.parse_args()

username=(args.federalid)
password = getpass.getpass()
url = 'https://portal.scarf.rl.ac.uk/cgi-bin/token.py'
params = urllib.urlencode({
  'username': username,
  'password': password
})

# This is needed from Python 2.7.9, but not supported in <=2.7.8
# Context with old default behavior: don't do certificate validation
# This require 'import ssl', see above
# context = ssl._create_unverified_context()
# commented out: this will do certificate validation from python >= 2.7.9
# and that is very prone to fail.
##response = urllib2.urlopen(url, params).read()
# Use certificate-ignoring context:
#response = urllib2.urlopen(url, params, context=context).read()

response = urllib2.urlopen(url, params).read()

if "https://portal.scarf.rl.ac.uk" in response:
        url_token = response.splitlines()
        pac_api.saveToken(url_token[0], url_token[1])
        print "You have now successfully logged onto PAC"
else:
        print response
        print response
