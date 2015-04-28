#!/usr/bin/env python

import sys
import os
import getopt
import httplib
import httplib2
import urllib
import urllib2

from xml.etree import ElementTree as ET
from xml.dom import minidom
from xml.parsers.expat import ExpatError
import getpass

PACPASSFILE='.pacpass'
ACCEPT_TYPE='text/plain,application/xml,text/xml'
ERROR_STR='errMsg'
NOTE_STR='note'
ERROR_TAG='<' + ERROR_STR + '>'
ACTION_STR='actionMsg'
ACTION_TAG='<' + ACTION_STR + '>'
CMD_STR='cmdMsg'
CMD_TAG='<' + CMD_STR + '>'
APP_NAME='APPLICATION_NAME'

def downloadFile(srcName, dstName, jobId):
	url,token = getToken();
	
	x509Flag, keypemfile, certpemfile = checkX509PEMCert(url)
	
	if ( (x509Flag == False) & (len(token) <= 0) ):
		print "You must log on to PAC. To log on, run pacclient logon."
		return
	
	http = httplib2.Http(ca_certs='UKe-ScienceRoot.crt')
	if ( (x509Flag == True) & (len(token) <= 0) ):
		# X509Flag is True and token is empty, then add the key/cert files into http request.
		http.add_certificate(keypemfile, certpemfile, '')
	
	url_file = url + 'webservice/pacclient/file/' + jobId
	body=srcName
	headers = {'Content-Type': 'text/plain', 'Cookie': token, 'Accept': ACCEPT_TYPE}
	try:
		response, content = http.request(url_file, 'GET', body=body, headers=headers)
		if len(content) > 0:
			f=open(dstName,'wb')
			f.write(content)
			f.close()
		else:
			nList = srcName.split('/')
			srcName= nList.pop()
			print "Download failed. you have no permission or the specified file does not exist: %s" % srcName
	except AttributeError:
		print "Cannot connect to the web service: %s" % url
	except IOError:
		print "   --Permission denied to write the file: %s" % dstName

def downloadJobFiles(jobId, dstPath, dFile):
	url, token = getToken();
	
	x509Flag, keypemfile, certpemfile = checkX509PEMCert(url)
	
	if ( (x509Flag == False) & (len(token) <= 0) ):
		print "You must log on to PAC. To log on, run pacclient logon."
		return
	
	http = httplib2.Http(ca_certs='UKe-ScienceRoot.crt')
	if ( (x509Flag == True) & (len(token) <= 0) ):
		# X509Flag is True and token is empty, then add the key/cert files into http request.
		http.add_certificate(keypemfile, certpemfile, '')
		
	if os.access(dstPath, os.W_OK) == 0:
		print "You do not have write permission on the directory: %s" % dstPath
		return
	url_jobfiles= url + 'webservice/pacclient/jobfiles/' + jobId
	headers = {'Content-Type': 'text/plain', 'Cookie': token, 'Accept': ACCEPT_TYPE}
	try:
		if len(dFile) > 0:
			downloadUtil(dstPath, dFile, jobId)
		else:		
			response, content = http.request(url_jobfiles, 'GET', headers=headers)
			if ('\\' not in content) and ('/' not in content):
				print content
				return
			print "Start to download..."
			files = content.split(';')
			for ff in files:
				if len(ff) <= 0:
					break
				downloadUtil(dstPath, ff, jobId)
	except AttributeError:
		print "Cannot connect to the web service: %s" % url
		
def downloadUtil(dstPath, dFile, jobId):
	"""
	download a file from server into local host path :dstPath.
	"""
	nList = dFile.split('/')
	fName= nList.pop()

        print "downloading"
        print "dstPath: ", dstPath
        print "dFile: ", dFile
        print "jobId: ", jobId

        if fName[-1] == ' ':
		fName = fName[0:-1]
	if len(dstPath) > 0:
		if dstPath[-1] != getFileSeparator():
			dstName= dstPath + getFileSeparator() + fName
		else:
			dstName= dstPath + fName
	else:
		dstName= fName
	print "Downloading file: " + fName + " to " + dstName
	downloadFile(dFile, dstName, jobId)

def uploadUtil(dstPath, dFile, jobId):
	"""
	upload a file to server :dstPath.
	"""
	if dstPath.strip()=='':
		dstPath = 'current job directory'
	nList = dFile.split(',')
	fName= nList
	for ff in fName:
			if len(ff) <= 0:
				break
			print "Uploading file: " + ff + " to " + dstPath

def uploadJobFiles(jobId, dstPath, dFile):
	url, token = getToken();
		
	x509Flag, keypemfile, certpemfile = checkX509PEMCert(url)
	
	if ( (x509Flag == False) & (len(token) <= 0) ):
		print "You must log on to PAC. To log on, run pacclient logon."
		return
	
	http = httplib2.Http(ca_certs='UKe-ScienceRoot.crt')
	if ( (x509Flag == True) & (len(token) <= 0) ):
		# X509Flag is True and token is empty, then add the key/cert files into http request.
		http.add_certificate(keypemfile, certpemfile, '')
		
	boundary='4k89ogja023oh1-gkdfk903jf9wngmujfs95m'
	status,body = encode_body_upfile(boundary, dstPath, dFile)
	if status == 'error':
		print body
	headers = {'Content-Type': 'multipart/mixed; boundary=' + boundary,
				'Accept': 'text/plain;', 'Cookie': token,
				'Content-Length': str(len(body))}
	url_upfile = url + 'webservice/pacclient/upfile/' + jobId
        print "uploadjobfiles , jobid: " , jobId
        print "url_upfile: ", url_upfile
	try:
		print "Start to upload..."
		uploadUtil(dstPath, dFile, jobId)
		response, content = http.request(url_upfile, 'POST', body=body, headers=headers)
		if response['status'] == '200':
			print content
		else:
			print "Failed to connect to web service and file upload failed."
	except AttributeError:
		print "Cannot connect to the web service: %s" % url
		
def jobdataList(jobId):
	url, token = getToken()
		
	x509Flag, keypemfile, certpemfile = checkX509PEMCert(url)
	
	if ( (x509Flag == False) & (len(token) <= 0) ):
		print "You must log on to PAC. To log on, run pacclient logon."
		return
	
	http = httplib2.Http(ca_certs='UKe-ScienceRoot.crt')
	if ( (x509Flag == True) & (len(token) <= 0) ):
		# X509Flag is True and token is empty, then add the key/cert files into http request.
		http.add_certificate(keypemfile, certpemfile, '')
		
	url_jobfiles= url + 'webservice/pacclient/jobfiles/' + jobId
	headers = {'Content-Type': 'text/plain', 'Cookie': token, 'Accept': ACCEPT_TYPE}
	try:
		response, content = http.request(url_jobfiles, 'GET', headers=headers)
		if ('\\' not in content) and ('/' not in content):
		    print content
		    return ''
		files = content.split(';')
		return files
	except AttributeError:
		print "Cannot connect to the web service: %s" % url 

def logon(url, username, password):
	if url[len(url) -1 ] != '/':
		url += '/'
	
	http = httplib2.Http(ca_certs='UKe-ScienceRoot.crt')
	
	# Check whether or not to use the X509 client authentication
	x509Flag, keypemfile, certpemfile = checkX509PEMCert(url)
	
	# Initial the variables
	url_logon= url + 'webservice/pacclient/logon/'
	headers = {}
	body = ''
	
	# If not X509 client authentication, use the normal way.
	# When set the username value, that is to say you want to use the normal authentication to logon.
	if ( (x509Flag == False) | (len(username) > 0) ):
		url_check, token = getToken()
		if url_check != url:
			token = "platform_token="
		headers = {'Content-Type': 'application/xml', 'Cookie': token, 'Accept': ACCEPT_TYPE}
		body='<User><name>%s</name> <pass>%s</pass> </User>' % (username, password)
	else:
		headers = {'Content-Type': 'application/xml', 'Accept': ACCEPT_TYPE}
		body='<User></User>'
		# http object add the certificate for http request
		http.add_certificate(keypemfile, certpemfile, '')
		
	try:
		response, content = http.request(url_logon, 'GET', body=body, headers=headers)
		if response['status'] == '200':
			xdoc=minidom.parseString(content)
			tk=xdoc.getElementsByTagName("token")
			
			if x509Flag == True:
				if len(username) <= 0:
					# For X509 client authentication
					username = xdoc.getElementsByTagName("name")
					if len(username) > 0:
						print "You have logged on to PAC as: " + username[0].childNodes[0].nodeValue
						saveToken(url, '')
					else:
						try:
							err=xdoc.getElementsByTagName("errMsg")
							print err[0].childNodes[0].nodeValue
						except IndexError:
							print "Cannot connect to the web service: %s" % url
				else:
					if len(tk) > 0:
						print "You have logged on to PAC as: " + username
						#print tk[0].childNodes[0].nodeValue
						saveToken(url, tk[0].childNodes[0].nodeValue)
					else:
						err=xdoc.getElementsByTagName("errMsg")
						print err[0].childNodes[0].nodeValue
			else:
				if len(tk) > 0:
					print "You have logged on to PAC as: " + username
					#print tk[0].childNodes[0].nodeValue
					saveToken(url, tk[0].childNodes[0].nodeValue)
				else:
					err=xdoc.getElementsByTagName("errMsg")
					print err[0].childNodes[0].nodeValue
					print 'Logging using scarf credentials'
					logon_scarf(username,password)
		else:
			print "Failed to connect to web service URL: %s" % url_logon
	except (AttributeError, httplib2.ServerNotFoundError, httplib.InvalidURL, ExpatError):
		print "Cannot connect to the web service: %s" % url

def logon_scarf(username, password):
        url = 'https://portal.scarf.rl.ac.uk/cgi-bin/token.py'
        params = urllib.urlencode({
          'username': username,
          'password': password
        })
        response = urllib2.urlopen(url, params).read()
        if "https://portal.scarf.rl.ac.uk" in response:
                url_token = response.splitlines()
                saveToken(url_token[0], url_token[1])
                print "You have now successfully logged onto PAC"
        else:
                print response
		
def logout():
	url, token = getToken()

        print "Got token, (url: %s, token: %s): "%(url, token)
        
	x509Flag, keypemfile, certpemfile = checkX509PEMCert(url)
	
	if ( (x509Flag == False) & (len(token) <= 0) ):
		print "You must log on to PAC. To log on, run pacclient logon."
		return
	
	http = httplib2.Http(ca_certs='UKe-ScienceRoot.crt')
	if ( (x509Flag == True) & (len(token) <= 0) ):
		# For X.509 client authentication, don't need to send HTTP request to logout
		# We can only tell user that you have logout successfully
		http.add_certificate(keypemfile, certpemfile, '')
		#print "you have logout successfully."
		
	url_logout= url + 'webservice/pacclient/logout/'
	headers = {'Content-Type': 'text/plain', 'Cookie': token, 'Accept': ACCEPT_TYPE}
	try:
		response, content = http.request(url_logout, 'GET', headers=headers)
                print "GOT status: ", response['status']
                print "GOT reply: ", content
		if response['status'] == '200':
			if content == 'ok':
				if os.name == 'nt':	
					fpath=os.environ['HOMEPATH']
					if len(fpath) > 0:
						fpath = os.environ['HOMEDRIVE'] + fpath + '\\' +PACPASSFILE
					else:
						fpath += '\\' + PACPASSFILE
				else:
					fpath = os.environ['HOME'] + '/' + PACPASSFILE
				os.remove(fpath)
				print "you have logout successfully."
			else:
				print content
		else:
			print "Failed to connect to web service URL: %s" % url_logout
	except AttributeError:
		print "Cannot connect to the web service: %s" % url
		
def getJobListInfo(parameter):
	url, token = getToken()
			
	x509Flag, keypemfile, certpemfile = checkX509PEMCert(url)

	print " In getJobListInfo... "

	if ( (x509Flag == False) & (len(token) <= 0) ):
		return 'error', "You must log on to PAC. To log on, run pacclient logon."

	# MODIFIED
	#http = httplib2.Http(ca_certs='UKe-ScienceRoot.crt')
        http = httplib2.Http(disable_ssl_certificate_validation=True)

        if ( (x509Flag == True) & (len(token) <= 0) ):
		# X509Flag is True and token is empty, then add the key/cert files into http request.
		http.add_certificate(keypemfile, certpemfile, '')

        print " Trying GET request..."
	url_job = url + 'webservice/pacclient/jobs?' + parameter
	headers = {'Content-Type': 'application/xml', 'Cookie': token, 'Accept': ACCEPT_TYPE}
	try:
		response, content = http.request(url_job, 'GET', headers=headers)
		if response['status'] == '200':
			xdoc=ET.fromstring(content)
			if ERROR_TAG in content:
				tree=xdoc.getiterator("Jobs")
				err=tree[0].find(ERROR_STR)
				return 'error', err.text
			elif NOTE_STR in content:
				tree=xdoc.getiterator("Jobs")
				err=tree[0].find(NOTE_STR)
				return 'error', err.text
			else:
				return 'ok', content
		else:
			return 'error', "Failed to connect to web service URL: %s" % url_job
	except (AttributeError, ExpatError):
		return 'error', "Cannot connect to the web service: %s" % url

def getJobInfo(jobId):
	url, token = getToken()
			
	x509Flag, keypemfile, certpemfile = checkX509PEMCert(url)
	
	if ( (x509Flag == False) & (len(token) <= 0) ):
		return 'error', "You must log on to PAC. To log on, run pacclient logon."
	
	# MODIFIED
	#http = httplib2.Http(ca_certs='UKe-ScienceRoot.crt')
        http = httplib2.Http(disable_ssl_certificate_validation=True)
	if ( (x509Flag == True) & (len(token) <= 0) ):
		# X509Flag is True and token is empty, then add the key/cert files into http request.
		http.add_certificate(keypemfile, certpemfile, '')
		
	url_job = url + 'webservice/pacclient/jobs/' + jobId
	headers = {'Content-Type': 'application/xml', 'Cookie': token, 'Accept': ACCEPT_TYPE}
	try:
		response, content = http.request(url_job, 'GET', headers=headers)
		if response['status'] == '200':
			xdoc=minidom.parseString(content)
			if ERROR_TAG in content:
				err=xdoc.getElementsByTagName(ERROR_STR)
				return 'error', err[0].childNodes[0].nodeValue
			else:
				return 'ok', content
		else:
			return 'error', "Failed to connect to web service URL: %s" % url_job
	except (AttributeError, ExpatError):
		return 'error', "Cannot connect to the web service: %s" % url

def getJobForStatus(jobStatus):
	url, token = getToken()
			
	x509Flag, keypemfile, certpemfile = checkX509PEMCert(url)
	
	if ( (x509Flag == False) & (len(token) <= 0) ):
		return 'error', "You must log on to PAC. To log on, run pacclient logon."
	
	http = httplib2.Http(ca_certs='UKe-ScienceRoot.crt')
	if ( (x509Flag == True) & (len(token) <= 0) ):
		# X509Flag is True and token is empty, then add the key/cert files into http request.
		http.add_certificate(keypemfile, certpemfile, '')
		
	url_job = url + 'webservice/pacclient/jobsforstatus/' + jobStatus
	headers = {'Content-Type': 'application/xml', 'Cookie': token, 'Accept': ACCEPT_TYPE}
	try:
		response, content = http.request(url_job, 'GET', headers=headers)
		if response['status'] == '200':
			xdoc=minidom.parseString(content)
			if ERROR_TAG in content:
				err=xdoc.getElementsByTagName(ERROR_STR)
				return 'error', err[0].childNodes[0].nodeValue
			else:
				return 'ok', content
		else:
			return 'error', "Failed to connect to web service URL: %s" % url_job
	except (AttributeError, ExpatError):
		return 'error', "Cannot connect to the web service: %s" % url
	
def getJobForName(jobName):
	url, token = getToken()
			
	x509Flag, keypemfile, certpemfile = checkX509PEMCert(url)
	
	if ( (x509Flag == False) & (len(token) <= 0) ):
		return 'error', "You must log on to PAC. To log on, run pacclient logon."
	
	http = httplib2.Http(ca_certs='UKe-ScienceRoot.crt')
	if ( (x509Flag == True) & (len(token) <= 0) ):
		# X509Flag is True and token is empty, then add the key/cert files into http request.
		http.add_certificate(keypemfile, certpemfile, '')
		
	url_job = url + 'platform/webservice/pacclient/jobsforname/' + jobName
	headers = {'Content-Type': 'application/xml', 'Cookie': token, 'Accept': ACCEPT_TYPE}
	try:
		response, content = http.request(url_job, 'GET', headers=headers)
		if response['status'] == '200':
			xdoc=minidom.parseString(content)
			if ERROR_TAG in content:
				err=xdoc.getElementsByTagName(ERROR_STR)
				return 'error', err[0].childNodes[0].nodeValue
			else:
				return 'ok', content
		else:
			return 'error', "Failed to connect to web service URL %s" % url_job
	except (AttributeError, ExpatError):
		return 'error',"Cannot connect to the web service: %s" % url

def saveToken(url, token):
	#if len(token) <= 0:
	#	return
	if os.name == 'nt':	
		fpath=os.environ['HOMEPATH']
		if len(fpath) > 0:
			fpath = os.environ['HOMEDRIVE'] + fpath + '\\' +PACPASSFILE
		else:
			fpath += '\\' + PACPASSFILE
	else:
		fpath = os.environ['HOME'] + '/' + PACPASSFILE
	try:
		ff= open(fpath, "wb")
	except IOError as e:
		print "Can not open file '" + fpath + "', " + e.strerror + "."
	else:
		ff.write(url)
		ff.write('\n')
		ff.write(token)
		ff.close

def getToken():
	token=''
	url=''
	if os.name == 'nt':	
		fpath=os.environ['HOMEPATH']
		if len(fpath) > 0:
			fpath = os.environ['HOMEDRIVE'] + fpath + '\\' +PACPASSFILE
		else:
			fpath += '\\' + PACPASSFILE
	else:
		fpath = os.environ['HOME'] + '/' + PACPASSFILE
	try:
		ff= open(fpath, "rb")		
	except IOError:
		return url,token
	else:
		url_token=ff.read().splitlines() #.rstrip().split('\n')
		ff.close()
		url=url_token[0]
		token=url_token[1].replace('"', '#quote#')
		if len(token) <= 0:
			return url, token
		else:
			return url, 'platform_token='+token

def getFileSeparator():
	if os.name == 'nt':
		return '\\'
	else:
		return '/'

def submitJob(jobDict):
	url, token = getToken()
			
	x509Flag, keypemfile, certpemfile = checkX509PEMCert(url)
	
	if ( (x509Flag == False) & (len(token) <= 0) ):
		return 'error', "You must log on to PAC. To log on, run pacclient logon."
	
	http = httplib2.Http(ca_certs='UKe-ScienceRoot.crt')
	if ( (x509Flag == True) & (len(token) <= 0) ):
		# X509Flag is True and token is empty, then add the key/cert files into http request.
		http.add_certificate(keypemfile, certpemfile, '')
		

	if len(jobDict) == 0:
		return 'error', 'The file does not contain any job parameters. The job cannot be submitted.'
	if  APP_NAME not in jobDict.keys():
		return 'error', 'Cannot find the published application: %s. This job cannot be submitted.' % APP_NAME
	
	boundary='bqJky99mlBWa-ZuqjC53mG6EzbmlxB'
	if 'PARAMS'  in jobDict.keys():
		job_params=jobDict['PARAMS']
	else:
		job_params={}
	
	if 'INPUT_FILES' in jobDict.keys():
		job_files=jobDict['INPUT_FILES']
	else:
		job_files={}

	body = encode_body(boundary, jobDict[APP_NAME], job_params, job_files)
	if body == None:
		return 'error',"The profile Inputfile section or inputfile param format is wrong\nsee the help."
	if "Submit job failed" in body:
		return 'error', body
	headers = {'Content-Type': 'multipart/mixed; boundary='+boundary,
                   'Accept': 'text/xml,application/xml;', 'Cookie': token,
                   'Content-Length': str(len(body))}
	url_submit = url + 'webservice/pacclient/submitapp'

        print " ================== BODY: ==================="
        print body
        print " ================= END BODY ================ "
	#url_submit = 'http://localhost:8080/platform/webservice/pacclient/submitapp'
	try:
		response, content = http.request(url_submit, 'POST', body=body, headers=headers)
		if response['status'] == '200':
			xdoc=minidom.parseString(content)
			if ERROR_TAG not in content:
				jobIdTag=xdoc.getElementsByTagName("id")
				return 'ok', jobIdTag[0].childNodes[0].nodeValue
			else:
				err=xdoc.getElementsByTagName(ERROR_STR)
				return 'error', err[0].childNodes[0].nodeValue
		else:
                        print "GOT Return status: ", response['status']
                        print "GOT 'Location':: ", response['location']
			return 'error', "Failed to connect to web service and submission failed."
	except (AttributeError, ExpatError):
		return 'error',"Cannot connect to the web service: %s" % url
	
def doJobAction(jobAction, jobId):
	url, token = getToken()
			
	x509Flag, keypemfile, certpemfile = checkX509PEMCert(url)
	
	if ( (x509Flag == False) & (len(token) <= 0) ):
		return 'error', "You must log on to PAC. To log on, run pacclient logon."
	
	http = httplib2.Http(ca_certs='UKe-ScienceRoot.crt')
	if ( (x509Flag == True) & (len(token) <= 0) ):
		# X509Flag is True and token is empty, then add the key/cert files into http request.
		http.add_certificate(keypemfile, certpemfile, '')
		
	url_jobaction = url + 'webservice/pacclient/jobOperation/' + jobAction +'/' + jobId
	headers = {'Content-Type': 'text/plain', 'Cookie': token, 'Accept': ACCEPT_TYPE}
	try:
		response, content = http.request(url_jobaction, 'GET', headers=headers)
		if response['status'] == '200':
			xdoc = minidom.parseString(content)
			if ERROR_TAG in content:
				err = xdoc.getElementsByTagName(ERROR_STR)
				return 'error', err[0].childNodes[0].nodeValue
			elif ACTION_TAG in content:
				action = xdoc.getElementsByTagName(ACTION_STR)
				return 'ok', action[0].childNodes[0].nodeValue
			else:
				return 'error', "Failed to connect to web service and logon."
		else:
			return 'error', "Failed to connect to web service URL: %s" % url_jobaction
	except (AttributeError, ExpatError):
		return 'error',"The web service isn't ready on URL: %s" % url_jobaction

def doUserCmd(userCmd):
	url, token = getToken()
			
	x509Flag, keypemfile, certpemfile = checkX509PEMCert(url)
	
	if ( (x509Flag == False) & (len(token) <= 0) ):
		return 'error', "You must log on to PAC. To log on, run pacclient logon."
	
	http = httplib2.Http(ca_certs='UKe-ScienceRoot.crt')
	if ( (x509Flag == True) & (len(token) <= 0) ):
		# X509Flag is True and token is empty, then add the key/cert files into http request.
		http.add_certificate(keypemfile, certpemfile, '')
		

	body = '<UserCmd><cmd>%s</cmd></UserCmd>' % (userCmd)
	headers = {'Content-Type': 'application/xml',
				'Accept': 'text/xml;', 'Cookie': token,
				'Content-Length': str(len(body))}
	
	url_usercmd = url + 'webservice/pacclient/userCmd'
	try:
		response, content = http.request(url_usercmd, 'POST', body=body, headers=headers)
		if response['status'] == '200':
			xdoc = minidom.parseString(content)
			msg = ''
			if ERROR_TAG in content:
				err = xdoc.getElementsByTagName(ERROR_STR)
				if ((err.length > 0) and (err[0].childNodes.length > 0)):
					msg = err[0].childNodes[0].nodeValue
				return 'error', msg
			elif CMD_STR in content:
				cmd = xdoc.getElementsByTagName(CMD_STR)
				if ((cmd.length > 0) and (cmd[0].childNodes.length > 0)):
					msg = cmd[0].childNodes[0].nodeValue
				return 'ok', msg
			else:
				return 'error', "Failed to connect to web service and logon."
		else:
			return 'error', "Failed to connect to web service URL: %s" % url_usercmd
	except (AttributeError, ExpatError):
		return 'error',"The web service isn't ready on URL: %s" % url_usercmd

		
def ping(url):
	if url[len(url) -1 ] != '/':
		url += '/'
			
	x509Flag, keypemfile, certpemfile = checkX509PEMCert(url)
	
	http = httplib2.Http(ca_certs='UKe-ScienceRoot.crt')
	if x509Flag == True:
		# X509Flag is True and token is empty, then add the key/cert files into http request.
		http.add_certificate(keypemfile, certpemfile, '')
		
	url_ping = url + 'platform/webservice/pacclient/ping/'
	body = url
	headers = {'Content-Type': 'text/plain', 'Accept': ACCEPT_TYPE}
	try:
		response, content = http.request(url_ping, 'GET', body=body, headers=headers)
		if response['status'] == '200':
			print content
		else:
			print "Web services aren't ready on URL: %s" % url_ping
	except (AttributeError, httplib2.ServerNotFoundError, httplib.InvalidURL):
		print "Cannot connect to the web service: %s" % url
	
def removeQuote(str):
	"""
	Remove the single or double quote. for example: 'abc' --> abc
	"""
	while len(str) > 2:
		if ((str[0] == '"') & (str[-1] == '"')):
			str = str[1:-1]
		elif ((str[0] == "'") & (str[-1] == "'")):
			str = str[1:-1]
		else:
			break
	return str

def getAllAppStatus():
	url, token = getToken()
			
	x509Flag, keypemfile, certpemfile = checkX509PEMCert(url)
	
	if ( (x509Flag == False) & (len(token) <= 0) ):
		return 'error', "You must log on to PAC. To log on, run pacclient logon."
	
	http = httplib2.Http(ca_certs='UKe-ScienceRoot.crt')
	if ( (x509Flag == True) & (len(token) <= 0) ):
		# X509Flag is True and token is empty, then add the key/cert files into http request.
		http.add_certificate(keypemfile, certpemfile, '')
	url_app = url + 'webservice/pacclient/appStatus'
	print('Url',url,'full url',url_app)
	headers = {'Content-Type': 'text/plain', 'Cookie': token, 'Accept': ACCEPT_TYPE}
	try:
		response, content = http.request(url_app, 'GET', headers=headers)
		if response['status'] == '200':
			xdoc = minidom.parseString(content)
			if ERROR_TAG in content:
				err=xdoc.getElementsByTagName(ERROR_STR)
				return 'error', err[0].childNodes[0].nodeValue
			else:
				return 'ok', content
		else:
			return 'error', "Failed to connect to web service URL: %s" % url_app
	except (AttributeError, ExpatError):
		return 'error', "Cannot connect to the web service: %s" % url
	
def getAppParameter(appName):
	url, token = getToken()
			
	x509Flag, keypemfile, certpemfile = checkX509PEMCert(url)
	
	if ( (x509Flag == False) & (len(token) <= 0) ):
		return 'error', "You must log on to PAC. To log on, run pacclient logon."
	
	http = httplib2.Http(ca_certs='UKe-ScienceRoot.crt')
	if ( (x509Flag == True) & (len(token) <= 0) ):
		# X509Flag is True and token is empty, then add the key/cert files into http request.
		http.add_certificate(keypemfile, certpemfile, '')
		
	url_app = url + 'webservice/pacclient/appParams'
	body = appName
	headers = {'Content-Type': 'text/plain', 'Cookie': token, 'Accept': ACCEPT_TYPE}
	try:
		response, content = http.request(url_app, 'GET', body = body, headers=headers)
		if response['status'] == '200':
			xdoc = minidom.parseString(content)
			if ERROR_TAG in content:
				err=xdoc.getElementsByTagName(ERROR_STR)
				return 'error', err[0].childNodes[0].nodeValue
			else:
				return 'ok', content
		else:
			return 'error', "Failed to connect to web service URL: %s" % url_app
	except (AttributeError, ExpatError):
		return 'error', "Cannot connect to the web service: %s" % url


def encode_body(boundary, appName, params, inputFiles):
	slash = getFileSeparator()
	boundary2='_Part_1_701508.1145579811786'
	def encode_appname():
		return ('--' + boundary,
                'Content-Disposition: form-data; name="AppName"',
		'Content-ID: <AppName>',
                '', appName)

	def encode_paramshead():
		return('--' + boundary,
		'Content-Disposition: form-data; name="data"',
		'Content-Type: multipart/mixed; boundary='+ boundary2,
		'Content-ID: <data>', '')

	def encode_param(param_name):
		return('--' + boundary2,
		'Content-Disposition: form-data; name="%s"' % param_name,
		'Content-Type: application/xml; charset=US-ASCII',
		'Content-Transfer-Encoding: 8bit',
		'', '<AppParam><id>%s</id><value>%s</value><type></type></AppParam>' %(param_name, params[param_name]))

	def encode_fileparam(param_name, param_value):
		return('--' + boundary2,
		'Content-Disposition: form-data; name="%s"' % param_name,
		'Content-Type: application/xml; charset=US-ASCII',
		'Content-Transfer-Encoding: 8bit',
		'', '<AppParam><id>%s</id><value>%s</value><type>file</type></AppParam>' %(param_name, param_value))

	def encode_file(filepath, filename):
		return('--' + boundary,
			'Content-Disposition: form-data; name="%s"; filename="%s"' %(filename, filename),
			'Content-Type: application/octet-stream',
			'Content-Transfer-Encoding: UTF-8',
			'Content-ID: <%s>' % filename,
			'', open(filepath, 'rb').read ())

	lines = []
	upType = ''
	upFlag = False
	lines.extend(encode_appname())
	lines.extend(encode_paramshead())
	for name in params:
		lines.extend (encode_param(name))
	for name in inputFiles:
		value=inputFiles[name]
		if ',' in value:
			try:
				upType = value.split(',')[1]
				if (upType == 'link') | (upType == 'copy'):
					lines.extend (encode_fileparam(name, value))
					if upType == 'copy':
						print "Copying server file: %s " % value.split(',')[0]
				else:
					upFlag = True
					filename = value.replace('\\', '/').split('/').pop()	
					lines.extend (encode_fileparam(name, filename))
			except IndexError:
				return
		else:
			return
	
	lines.extend (('--%s--' % boundary2, ''))
	if upFlag == True:
		for name in inputFiles:
			value=inputFiles[name]
			if ',' in value:
				upType = value.split(',')[1]
				filepath = value.split(',')[0]
				if upType == 'upload':
					filename = filepath.replace('\\', '/').split('/').pop()
					try:
						lines.extend(encode_file(filepath, filename))
					except IOError:
						return "Submit job failed, No such file or directory: %s" % filepath
					print "Uploading input file: %s" % filepath
	lines.extend (('--%s--' % boundary, ''))
	return '\r\n'.join (lines)

def encode_body_upfile(boundary, dir, filelist):
	slash = getFileSeparator()
	def encode_dir():
		return ('--' + boundary,
			'Content-Disposition: form-data; name="DirName"',
			'Content-ID: <DirName>',
			'', dir)

	def encode_file(filepath, filename):
		return('--' + boundary,
			'Content-Disposition: form-data; name="%s"; filename="%s"' %(filename, filename),
			'Content-Type: application/octet-stream',
			'Content-Transfer-Encoding: UTF-8',
			'Content-ID: <%s>' % filename,
			'', open(filepath, 'rb').read ())

	lines = []
	lines.extend(encode_dir())
	files = filelist.split(',')
	for f in files:
		filename = f.replace('\\', '/').split('/').pop()
		try:
			lines.extend(encode_file(f, filename))
		except IOError:
			return 'error',"Failed to read from file %s" % f
	lines.extend (('--%s--' % boundary, ''))
	return 'ok','\r\n'.join (lines)

# Check the X509 PEM key/cert files whether or not exist.
# Return three value: X509Cert flag, keypemfile path, certpemfile path
# If X509Cert flag is False, the other values are empty string
def checkX509PEMCert(url):
	# If url is invalid for https, won't check cert.
	if ( (len(url) == 0) | ('https' not in url.lower()) ):
		return False, '', ''
	
	# Get the current path for key/cert files
	cwdPath = os.getcwd() + getFileSeparator();
	
	# Create the variables of key/cert files absolute path
	keypemfile = cwdPath + '.key.pem'
	certpemfile = cwdPath + '.cert.pem'

        print " --- Looking for : ", keypemfile
        print " --- Looking for : ", certpemfile
        
	# Check .key.pem and .cer.pem whether or not exist
	if ( ( os.path.isfile(keypemfile) == True ) & ( os.path.isfile(certpemfile) == True ) ):
                print " --- Returning true"
		return True, keypemfile, certpemfile
	else:
                print " --- Returning false"
		return False, '', ''

def main(argv):
	"""
	url=raw_input("URL:")
	if len(url) == 0:
		print "Wrong URL format. proper format: http://hostname:port/"
		return
	u=raw_input("Username:")
	
	if len(u) == 0:
		print "Empty username, can not logon."
		return
	p=getpass.getpass()
	if len(p) == 0:
		print "Password can not be empty."
		return
	logon(url, u, p)
	"""
	getJobInfo('356')
	
	downloadJobFiles('353', 'c:\\webservice\\350' )
	"""
	JobDict={}
	
	JobDict[APP_NAME]='FLUENT:FLUENT_WEB'                 #format: "app_type:app_name"
	JobDict['PARAMS']= {'JOB_NAME': 'FF_20100329',
	                    'RELEASE': '6.3.26',
			    'CONSOLE_SUPPORT': 'No'}
	JobDict['INPUT_FILES']={ 'FLUENT_JOURNAL':'C:\\portal_demo\\fluent\\fluent-test.jou,upload',
	                         'CAS_INPUT_FILE':'C:\\portal_demo\\fluent\\fluent-test.cas.gz,upload'}
	JobDict['RETURN_FILES']={ 'TARGET_DIR':'C:\jobResults', 'FILES':['*.zip', '*.txt']}
	status, message = submitJob(JobDict)
	print 'status =' + status
	print 'message =' + message
	"""
	
if __name__ == "__main__":
	main(sys.argv[1:])

