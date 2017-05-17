#!/usr/bin/env python

import sys
import os
import getopt
import httplib2
from xml.etree import ElementTree as ET
from xml.dom import minidom
from ConfigParser import ConfigParser
from ConfigParser import NoSectionError
import getpass
import socket
import re
import urllib2
from pac_api import *

def logon_usage():
	print """
pacclient.py logon usage:

pacclient.py logon [--help|-h] [--url|-l URL] [--user|-u user_name] [--pass|-p password]

Logs you in to PAC.

For example:
pacclient.py logon -l http://hostA:8080/ -u user2 -p mypassword

Use double quotes around any value that contains spaces. 
If any parameter is omitted, you will be prompted interactively.
Once you are logged in, you may run other pacclient commands, until you log out. You will be logged out automatically if you do not run any pacclient commands for 60 minutes consecutively.

[--url|-l URL]
	Specify the URL of the PAC web service in the format:
	http://host_name:port_number/ or https://host_name:port_number/
[--user|-u user_name]
	Specify your user name.
[--pass|-p password]
	Specify your password.
[--help|-h]
	Display subcommand usage. 
"""

def main_logon(argv):
	url=''
	user=''
	password=''
	try:                                
		opts, args = getopt.getopt(argv, "hl:u:p:", ['help','url=','user=','pass=']) 
	except getopt.GetoptError:           
		logon_usage()                        
		return
	for opt, arg in opts:                
		if ((opt == "-h") | (opt == "--help")) :      
			logon_usage()                     
			return                  
		elif ((opt == '-l') | (opt == "--url")) :
			url = arg  
		elif ((opt == '-u') | (opt == "--user")) :                
			user = arg  
		elif ((opt == '-p') | (opt == "--pass")) :                
			password = arg  

	if len(url) == 0:	
		url=raw_input("URL:")
	p = re.compile('^(http|https)://[\w\W]+:\d+[/]{0,1}$')
	if (len(url) == 0) | (p.match(url.lower()) == None):
		print "Specify the URL of the PAC web services in the format: http://host_name:port_number or https://host_name:port_number"
		return
	
	url = removeQuote(url)
	x509Flag, key, cert = checkX509PEMCert(url)

	if (x509Flag == False) | ( len(user) > 0) | (len(password) > 0):
		if len(user) == 0:
			user=raw_input("Username:")
		if len(user) == 0:
			print "Specify your user name."
			return
		if len(password) == 0:
			password=getpass.getpass()
		if len(password) == 0:
			print "Specify your password."
			return
		user = removeQuote(user)
		
	# Log on action
	logon(url, user, password)

def submit_usage():
	print """
pacclient.py submit usage:

pacclient.py submit [--help|-h] [--conf|-c file_path ] [--param|-p field_ID=value;[field_ID=value;]...] --app|-a app_name[:template_name]

Submits a job to PAC.

For example:
pacclient.py submit -a "FLUENT" -c C:\mydir\\fluentconf.txt -p "CONSOLE_SUPPORT=yes;CAS_INPUT_FILE=C:\mydir\\fluent\\fluent-test.cas.gz,link"

Use double quotes around any value that contains spaces.
Parameters defined in the command line (-p) override all others; parameters defined in a file (-c) override parameters defined in an application form (-a).

--app|-a app_name[:template_name] 
	Required. Specify the application form to use for default job submission parameters.
	Specify the application name and optionally the name of your customized template.
[--conf|-c file_path ]
	Define the job submission parameters from a file.
	Specify the path to a file on the local host that defines job parameters and input files. The file format is a list of field ID and value pairs:
	* field_ID
		Specify the field ID from the application form template. You must be an administrator to access editing mode and view the field IDs.
	* value
		Specify the value for the field input. If the field requires a file for input, you must also choose to upload the file, copy the file to the job directory, or link the file to the job directory. Specify the value in the format:
		file_path,upload|copy|link
	For example:
	[Parameter]
	JOB_NAME=FF_20100329
	VERSION=6.3.26
	CONSOLE_SUPPORT=No
	[Inputfile]
	FLUENT_JOURNAL=C:\demo\\fluent\\fluent-test.jou,upload
	CAS_INPUT_FILE=C:\demo\\fluent\\fluent-test.cas.gz,upload
[--param|-p field_ID=value;[field_ID=value;]...]
	Define the job submission parameters in the command line.
	Specify field ID and value pairs as described in the --conf|-c option.
[--help|-h]
	Display subcommand usage.

"""

def main_submit(argv):
	if len(argv) == 0:
		submit_usage()                        
		return
	appName=''
	profile=''
	params=''
	slash = getFileSeparator()
	try:                                
		opts, args = getopt.getopt(argv, "ha:c:p:", ['help','app=','conf=', 'param=']) 
	except getopt.GetoptError:           
		submit_usage()                        
		return

	for opt, arg in opts:                
		if ((opt == "-h") | (opt == "--help")) :      
			submit_usage()                     
			return                  
		elif ((opt == '-a') | (opt == "--app")) :                
			appName = arg  
		elif ((opt == '-c') | (opt == "--conf")) :                
			profile = arg  
		elif ((opt == '-p') | (opt == "--param")) :                
			params = arg  
	if len(appName) <= 0:
		print "This required argument is missing: -a app_name[:template_name]. To view the command usage, run pacclient.py submit -h. "
		return

	inputParams={}
	inputFiles={}
	
	if len(profile) > 0:
		profile = removeQuote(profile)
		if (":" not in profile) & ( slash != profile[0]):
			dir = os.getcwd() + slash
			profile = dir + profile
			if os.path.isfile(profile) is False:
				print "The specified file does not exist: %s" % profile
				return
		config = ConfigParser()
		config.optionxform = str #make option name case-sensitive
		try:
			config.read(profile)
		except IOError:
			print "Cannot open the file: %s" % profile
			return
		try:
			for option in config.options('Parameter'):
				inputParams[option]=config.get('Parameter', option)
		except NoSectionError:
			print "The [Parameter] section is missing from the file: %s" % profile
			return
		try:
			for option in config.options('Inputfile'):
				inputFiles[option]=config.get('Inputfile', option)
		except NoSectionError:
			print "The [Inputfile] section is missing from the file: %s" % profile
			return
			

	if len(params) > 0:
		for pp in params.split(';'):
			if len(pp) > 0:
				nv = pp.split('=',1)
				if len(nv) > 1:
					if ',' in nv[1]:
						inputFiles[nv[0]] = nv[1]
					else:
						inputParams[nv[0]] = nv[1]
				else:
					print "The input parameters are invalid.To view the command usage, run pacclient.py submit --help."                     
					return

	JobDict={}
	JobDict[APP_NAME]=appName
	try:
		span = inputParams['SPAN']
		inputParams['SPAN'] = "span[%s]" % span
	except KeyError:
		pass
	JobDict['PARAMS']=inputParams
	JobDict['INPUT_FILES']=inputFiles
	

	status, message = submitJob(JobDict)
	if status == 'ok':
		print 'The job has been submitted successfully: job ID ' + message
	else:
		print message
		
def job_usage():
	print """
Usage:

pacclient.py job
pacclient.py job [-l] [-u user_name | -u all ] [-p hours] job_ID | "job_ID[index_list]"
pacclient.py job -s Pending | Running | Done | Exit | Suspended [-l] [-u user_name | -u all ] [-p hours]
pacclient.py job -n job_name [-l] [-u user_name | -u all ] [-p hours]
pacclient.py job -g jobgroup_name [-l] [-u user_name | -u all ] [-p hours]
pacclient.py -h 

Description:
By default, displays information about jobs submitted by the user running this command.

job_ID | "job_ID[index_list]"
 Displays information about the specified jobs or job arrays.

-l
 Long format. Displays detailed information for each job, job array, or job group in a multiline format.

-u user_name | -u all
 Only displays information about jobs that have been submitted by the specified user. The keyword all specifies all users. 
 
-p hours 
 In addition to active jobs, displays information about all Done and Exited jobs that have ended within the specified number of hours. 

-s Pending | Running | Done | Exit | Suspended
 Displays information only about jobs that have the specified state.

-n job_name
 Displays information about jobs or job arrays with the specified job name. The wildcard character (*) can be used within a job name, but cannot appear within array indices. For example job* returns jobA and jobarray[1], *AAA*[1] returns the first element in all job arrays with names containing AAA, however job1[*] will not return anything since the wildcard is within the array index.

-g jobgroup_name
 Displays information about jobs attached to the specified job group.
 
-h 
 Displays command usage.

"""

def main_job(argv):
	jobStatus=''
	jobName=''
	jobId=''
	long=''
	group=''
	user=''
	past=''
	try:                                
		opts, args = getopt.getopt(argv, "hu:ls:n:g:p:", ['help','user=','long','status=','name=','group=','past=']) 
	except getopt.GetoptError:          
		job_usage()                        
		return

	for opt, arg in opts:                
		if ((opt == "-h") | (opt == "--help")) :      
			job_usage()                     
			return 
		elif ((opt=='-u') | (opt == '--user')) :
			user=arg
		elif ((opt=='-l') | (opt == '--long')) :
			long='yes'                 
		elif ((opt == '-s') | (opt == "--status")) :                
			jobStatus = arg  
		elif ((opt == '-n') | (opt == "--name")) :                
			jobName = urllib2.quote(arg)
		elif ((opt == '-g') | (opt == "--group")) :
			group=urllib2.quote(arg)
		elif ((opt == '-p') | (opt == '--past')) :
			past=arg
	if len(args) > 0:
		jobId = args[0]
		p = re.compile('^[1-9]{1}[0-9]{0,}$')
		pl = re.compile('^[1-9]{1}[0-9]{0,}\[{1}[0-9]{0,}\]{1}$')
		if (len(jobId) == 0) | ((p.match(jobId.lower()) == None) and (pl.match(jobId.lower()) == None)) | (len(args)>1):
			job_usage()
			return	
	if (len(jobStatus) > 0 and len(jobName) > 0) | (len(jobStatus) > 0 and len(jobId) > 0) | (len(jobId) > 0 and len(jobName) > 0) | (len(jobId)>0 and len(group)>0) | (len(jobName)>0 and len(group)>0) | (len(jobStatus)>0 and len(group)>0):
		print "The options -s, -n, -g, and job ID cannot be used together."
		return
	status = ''
	message = ''
	statusFlag = False
	nameFlag = False
	groupFlag=False
	if len(jobStatus) > 0:
		status, message = getJobListInfo('status='+jobStatus+'&user='+user+'&details='+long+'&past='+past)
		statusFlag = True
	elif len(jobName) > 0:
		status, message = getJobListInfo('name='+jobName+'&user='+user+'&details='+long+'&past='+past)
		nameFlag = True
	elif len(group) > 0:
		status, message = getJobListInfo('group='+group+'&user='+user+'&details='+long+'&past='+past)
		groupFlag=True
	if status != '':
		if status == 'ok':
			tree = ET.fromstring(message)
			jobs =tree.getiterator("Job")
			if len(jobs) == 0:
				if statusFlag == True:
					print "There are no jobs matching the query: job status " + jobStatus
				elif nameFlag == True:
					print "There are no jobs matching the query: job name " + jobName
				elif groupFlag== True:
					print "There are no jobs matching the query: job group "+ group
				return
			showJobinfo(jobs,long)
		else:
			print message
		return

	if len(jobId) > 0:
		status, message= getJobListInfo('id='+jobId+'&user='+user+'&details='+long+'&past='+past)
		if status == 'ok':
			tree = ET.fromstring(message)
			jobs =tree.getiterator("Job")
			showJobinfo(jobs,long)
		else:
			print message
		return
	else:
		status, message= getJobListInfo('user='+user+'&details='+long+'&past='+past)
		if status == 'ok':
			tree = ET.fromstring(message)
			jobs =tree.getiterator("Job")
			showJobinfo(jobs,long)
		else:
			print message
		return
	job_usage()

def showJobinfo(jobs,long):
	if long == '':
		print 'JOBID     STATUS    EXTERNAL_STATUS        JOB_NAME                 COMMAND'
		for xdoc in jobs:
			jobId=xdoc.find('id').text
			status=xdoc.find('status')
			extStatus=xdoc.find('extStatus')
			name=xdoc.find('name').text
			cmd=xdoc.find('cmd')
			print '%-10s%-10s%-23s%-25s%s' % (jobId, checkFieldValidity(status), SubStr(checkFieldValidity(extStatus)), SubStr(name),checkFieldValidity(cmd))
	else:
		for xdoc in jobs:
			jobId=xdoc.find('id').text
			name=xdoc.find('name').text
			user=xdoc.find('user')
			jobType=xdoc.find('jobType')
			status=xdoc.find('status')
			appType=xdoc.find('appType')
			submitTime=xdoc.find('submitTime')
			endTime=xdoc.find('endTime')
			startTime=xdoc.find('startTime')
			queue=xdoc.find('queue')
			cmd=xdoc.find('cmd')
			projectName=xdoc.find('projectName')
			pendReason=xdoc.find('pendReason')
			description=xdoc.find('description')
			extStatus=xdoc.find('extStatus')
			priority=xdoc.find('priority')
			exitCode=xdoc.find('exitCode')
			swap=xdoc.find('swap')
			pgid=xdoc.find('pgid')
			pid=xdoc.find('pid')
			nthreads=xdoc.find('nthreads')
			numProcessors=xdoc.find('numProcessors')
			fromHost=xdoc.find('fromHost')
			exHosts=xdoc.find('exHosts')
			askedHosts=xdoc.find('askedHosts')
			runTime=xdoc.find('runTime')
			mem=xdoc.find('mem')
			timeRemaining=xdoc.find('timeRemaining')
			estimateRunTime=xdoc.find('estimateRunTime')
			infile=xdoc.find('infile')
			outfile=xdoc.find('outfile')
			execCwd=xdoc.find('execCwd')
			graphicJob=xdoc.find('graphicJob')
			cwd=xdoc.find('cwd')
			timeRemaining=xdoc.find('timeRemaining')
			app=xdoc.find('app')
			print 'Job ID:%s' % jobId
			print 'Job Name:%s' % name
			print 'Job Type:%s' % checkFieldValidity(jobType)
			print 'Status:%s' % checkFieldValidity(status)
			print 'Application Type:%s' % checkFieldValidity(appType)
			print 'Submission Time:%s' % checkFieldValidity(submitTime)
			print 'User:%s' % checkFieldValidity(user)
			print 'End Time:%s' % checkFieldValidity(endTime)
			print 'Start Time:%s' % checkFieldValidity(startTime)
			print 'Queue:%s' % checkFieldValidity(queue)
			print 'Command:%s' % checkFieldValidity(cmd)
			print 'Project Name:%s' % checkFieldValidity(projectName)
			print 'Pending Reason:%s' % checkFieldValidity(pendReason)
			print 'Job Description:%s' % checkFieldValidity(description)
			print 'External Status:%s' % checkFieldValidity(extStatus)
			print 'Job Priority:%s' % checkFieldValidity(priority)
			print 'Exit Code:%s' % checkFieldValidity(exitCode)
			print 'Mem:%s' % checkFieldValidity(mem)
			print 'Swap:%s' % checkFieldValidity(swap)
			print 'Process Group ID:%s' % checkFieldValidity(pgid)
			print 'Process ID:%s' % checkFieldValidity(pid)
			print 'Number Of Threads:%s' % checkFieldValidity(nthreads)
			print 'Required Processors:%s' % checkFieldValidity(numProcessors)
			print 'Submission Host:%s' % checkFieldValidity(fromHost)
			print 'Execution Hosts:%s' % checkFieldValidity(exHosts)
			print 'Requested Hosts:%s' % checkFieldValidity(askedHosts)
			print 'Run Time:%s' % checkFieldValidity(runTime)
			print 'Time Remaining:%s' % checkFieldValidity(timeRemaining)
			print 'Estimated Run Time:%s' % checkFieldValidity(estimateRunTime)
			print 'Input Files:%s' % checkFieldValidity(infile)
			print 'Output Files:%s' % checkFieldValidity(outfile)
			print 'Execution CWD:%s' % checkFieldValidity(execCwd)
			print 'Graphic Job:%s' % checkFieldValidity(graphicJob)
			print 'Current Working Dir:%s' % checkFieldValidity(cwd)
			print 'Application Profile:%s' % checkFieldValidity(app)
			if len(jobs)>1:
				print ' '
				print ' '
				
def SubStr(field):
	if len(field) > 10 :
		field = '*' + field[-9:]
	return field
					
def checkFieldValidity(field):
	if field != None:
		if field.text == None :
			field = ''
		else:
			field = field.text
	else:
		field='-'
	return field

def download_usage():
	print """
pacclient.py download usage:

pacclient.py download [--help|-h] [--dir|-d directory] [--file|-f file_name] job_ID

Download job data for a job.

For example:
pacclient.py download 54321

By default, copy all job data files to the current working directory.

[--dir|-d directory]
	Copy files to the specified directory.
[--file|-f file_name]
	Download the specified file only.
job_ID
	Specify the job ID.
[--help|-h]
	Display subcommand usage.

"""

def main_download(argv):
	if len(argv) == 0:
		download_usage()                       
		return
	dir=''
	file = ''
	jobId=''
	try:                                
		opts, args = getopt.getopt(argv, "hd:f:", ['help','dir=','file=']) 
	except getopt.GetoptError:           
		download_usage()                        
		return

	for opt, arg in opts:                
		if ((opt == "-h") | (opt == "--help")) :      
			download_usage()                     
			return                  
		elif ((opt == '-d') | (opt == "--dir")) :                
			dir = arg  
		elif ((opt == '-f') | (opt == '--file')) :
			file = arg
	if dir == '' and file == '' and len(args) <=0:
	   download_usage()
	   return
	if len(args) <= 0:
		print 'Please specify a job ID.'
		return
	if len(dir) <=0:
		dir = os.getcwd()
	jobId = args[0]
	if os.path.exists(dir) == False :
		print "The specified directory does not exist: %s" % dir
		return

	dir = removeQuote(dir)
	file = removeQuote(file)
	downloadJobFiles(jobId, dir, file)

def upload_usage():
	print """
pacclient.py upload usage:

pacclient upload  [-d dir_name] -f file_name[,file_name..] job_ID
pacclient upload  -d host_name:dir_name -f file_name[,file_name..] 
pacclient upload -h


Description:

Uploads data for a job to the job directory on the web server or the remote directory on a specific host.
By default, if a job ID is specified but no directory is specified, files are uploaded to the job directory on the web server.


Options:

-d dir_name
        Copies files to the specified directory on the web server. The directory can be an
        absolute path on the web server or a relative path to the job directory on the web server. 

-d host_name:dir_name
        Copies files to the specified job directory on the host. The directory can be 
        an absolute path to the remote job directory on the host, or a relative path to
        the remote job directory on the host.
                                                                                         
-f file_name[,file_name..]
        Uploads the specified file. Specify the path. Separate multiple files with a comma.

job_ID
        ID of the job for which to upload files.
        
-h
        Displays command usage.


Examples: 

Upload files to the job directory on the web server
pacclient upload -f /dir1/file1,/dir2/file2 54321

Upload file1 into the result subdirectory under job 101's job directory                                           

pacclient.py upload -d result -f file1 101

Upload file1 into /tmp/result on the web server
pacclient.py upload -d /tmp/result -f file1

Upload file1 into absolute path /tmp/result on remote host 
pacclient.py upload -d  host1:/tmp/result -f file1

"""

def main_upload(argv):
	if len(argv) == 0:
		upload_usage()                       
		return
	dir=''
	file = ''
	jobId=''
	try:                                
		opts, args = getopt.getopt(argv, "hd:f:") 
	except getopt.GetoptError:           
		upload_usage()                        
		return

	for opt, arg in opts:                
		if ((opt == "-h")) :      
			upload_usage()                     
			return                  
		elif ((opt == '-d')) :                
			dir = arg  
		elif ((opt == '-f')) :
			file = arg

	dir = removeQuote(dir)
	file = removeQuote(file)
	if file == '':
		print 'Please specify the source files to upload.'
		return
	p = re.compile('^[\w\W]+:/[\w\W]+')
	if (((dir == '') | ((len(dir) > 0) and (('/' != dir[0]) and (p.match(dir.lower()) == None)))) and (len(args) <= 0)):
		print 'Please specify a job ID if the -d option is omitted or specifies a relative local path.'
		return
	p = re.compile('^[\w\W]+:[^/][\w\W]+')
	if (p.match(dir.lower()) != None):
		print "The directory cannot be relative if it is remote. Specify an absolute path for the directory."
		return
	cwd = os.getcwd()
	files = file.split(',')
	paths = ''
	p = re.compile('^[a-zA-Z]:[/\\][\w\W]+')
	slash = getFileSeparator()
	valid = True
	for f in files:
		f.strip()
		if len(f) > 0:
			if ((slash != f[0]) and (p.match(f.lower()) == None)):
				f = cwd + slash + f
			if not os.path.isfile(f):
				valid = False
				print "The specified file does not exist: %s" % f
			elif os.access(f, os.R_OK) == 0:
				valid = False
				print "You do not have read permission on the file: %s" % f
			else:
				paths = paths + f + ','
	if not valid:
		return
	elif len(paths)<=0:
		print "The specified file does not exist: %s" % file
		return
	else:
		paths = paths[:-1]
	p = re.compile('^[\w\W]+:/[\w\W]+')
	if ((len(dir) > 0) and (('/' == dir[0]) | (p.match(dir.lower()) != None))):
		jobId = '0'
	else:
		jobId = args[0]
		p = re.compile('^[1-9]{1}[0-9]{0,}$')
		if p.match(jobId.lower()) == None:
			print "The job ID must be a positive integer."
			return
	uploadJobFiles(jobId, dir, paths)

def jobaction_usage():
	print """
pacclient.py jobaction usage:

pacclient.py jobaction [--help|-h] --action|-a kill|suspend|requeue|resume job_ID 

Perform a job action on a job.

For example:
pacclient.py jobaction -a resume 54321

--action|-a kill|suspend|requeue|resume
	Specify the job action. You can kill, suspend, requeue, or resume a job.
job_ID
	Specify the job ID.
[--help|-h]
	Display subcommand usage.

"""

def main_jobaction(argv):
	jobAction=''
	jobId=''
	try:                                
		opts, args = getopt.getopt(argv, "ha:", ['help','action=']) 
	except getopt.GetoptError:           
		jobaction_usage()                        
		return

	for opt, arg in opts:                
		if ((opt == "-h") | (opt == "--help")) :      
			jobaction_usage()                     
			return                  
		elif ((opt == '-a') | (opt == "--action")) :                
			jobAction = arg  
	if len(args) <= 0 and len(jobAction) <= 0:
		jobaction_usage()
		return
	if len(args) <= 0:
		print 'You must specify the job ID.'
		return
	if len(args) >0 :
		jobId = args[0]
		p = re.compile('^[1-9]{1}[0-9]{0,}$')
		pl = re.compile('^[1-9]{1}[0-9]{0,}\[{1}[0-9]{0,}\]{1}$')
		if (p.match(jobId.lower()) == None) and (pl.match(jobId.lower()) == None):
			jobaction_usage()
			return
	jobId=args[0]
	status, message = doJobAction(jobAction, jobId)
	print message

def usercmd_usage():
	print """
pacclient.py usercmd usage:

pacclient.py usercmd -c user_command
pacclient.py -h

Description:

Runs the specified command.

By default, the following LSF commands are allowed:
- bbot
- bchkpnt
- bkill
- bpost
- brequeue
- brestart
- bresume
- brun
- bstop
- btop
- bswitch
- bmig

The administrator can configure support for additional commands in the file
$GUI_CONFDIR/webservice.usercmd.


Options:

-c user_command
   Specify the executable command with its full path and options.

-h 
   Displays command usage.


Examples:

Kill job 101 by sending a SIGTERM signal
pacclient.py usercmd -c bkill -s SIGTERM 101

Force checkpoint of job 201 every 5 minutes
pacclient.py usercmd -c bchkpnt -f -p 5 201

"""

def main_usercmd(argv):
	userCmd=''

	for i in range(0, len(argv)):
		if ((argv[i] == '-h')):
			usercmd_usage()
			return
		elif (((argv[i] == '-c')) & (i+1 < len(argv))):
			userCmd = removeQuote(argv[i+1]).strip()
			if len(userCmd) <= 0:
				usercmd_usage()
				return
			for arg in argv[i+2:]:
				temp = removeQuote(arg).strip()
				if len(temp) > 0:
					userCmd = userCmd + ' "' + temp + '"'
			break
		else:
			usercmd_usage()
			return

	if len(userCmd) <= 0:
		usercmd_usage()
		return

	status, message = doUserCmd(userCmd)
	print message

def ping_usage():
	print """
pacclient.py ping usage:

pacclient.py ping [--help|-h] [--url|-l URL]

Detects whether or not the web service is running at the specified URL.

For example:
pacclient.py ping -l http://hostA:8080/

If -l is omitted, you will be prompted interactively.

[--url|-l URL]
	Specify the URL of the PAC web service in the format:
	http://host_name:port_number/
[--help|-h]
	Display subcommand usage.
"""

def main_ping(argv):
	url = ''
	try:                                
		opts, args = getopt.getopt(argv, "hl:", ['help','url='])
	except getopt.GetoptError:           
		ping_usage()                        
		return

	for opt, arg in opts:                
		if ((opt == "-h") | (opt == "--help")) :      
			ping_usage()                     
			return   
		elif ((opt == '-l') | (opt == "--url")) :
			url = arg         
	if len(url) == 0:	
		url=raw_input("URL:")
	p = re.compile('^(http|https)://[\w\W]+:\d+[/]{0,1}$')
	if (len(url) == 0) | (p.match(url.lower()) == None):
		print "Specify the URL of the PAC web services in the format: http://host_name:port_number or https://host_name:port_number"
		return
	ping(url)

def logout_usage():
	print """
pacclient.py logout usage:

pacclient.py logout [--help|-h]

Logs you out of PAC.

For example:
pacclient.py logout

Once you are logged out, you must log in to run more pacclient commands.
You will be logged out automatically if you do not run any pacclient commands for 60 minutes consecutively.

[--help|-h]
	Display subcommand usage.

"""

def main_logout(argv):
	try:                                
		opts, args = getopt.getopt(argv, "h", ['help'])
	except getopt.GetoptError:           
		logout_usage()                        
		return

	for opt, arg in opts:                
		if ((opt == "-h") | (opt == "--help")) :      
			logout_usage()                     
			return                  
	logout()

def main_usage():
	print """
pacclient.py usage:

ping      --- Check whether the web service is available
logon     --- Log on to IBM Platform Application Center
logout    --- Log out from IBM Platform Application Center
app       --- List applications or parameters of an application
submit    --- Submit a job
job       --- Show information for one or more jobs  
jobaction --- Perform a job action on a job 
jobdata   --- List all the files for a job 
download  --- Download job data for a job
upload    --- Upload job data for a job
usercmd   --- Perform a user command
help      --- Display command usage
"""
	
def app_usage():
	print """
pacclient.py app usage:

pacclient.py app [--help|-h] [--list|-l] | [--param|-p app_name[:template_name]] 

List applications or parameters of an application.

For example, to list all the parameters and default values for an application:
pacclient.py app -p FLUENT

[--param|-p app_name[:template_name]]
	List all parameters and default values for an application. To see parameter values saved in your customized application, specify both the published form name and the custom template name.
[--list|-l]
	Lists all applications and application status
[--help|-h]
	Display subcommand usage.
	
"""	

def main_app(argv):
	if len(argv) == 0:
		app_usage()
		return
	appName = ''
	list = False
	try:
		opts, args = getopt.getopt(argv, "hlp:", ['help','list','param='])
	except getopt.GetoptError:
		app_usage()
		return
	for opt, arg in opts:
		if ((opt == "-h") | (opt == "--help")):
			app_usage()
			return
		elif ((opt == "-l") | (opt == "--list")):
			list = True
		elif ((opt == "-p") | (opt == "--param")):
			appName = arg
	
	if list == True:
		status, message = getAllAppStatus()
		if status == 'ok':
			xdoc = minidom.parseString(message)
			apps = xdoc.getElementsByTagName('AppInfo')
			if len(apps) == 0:
				print "There are no published application"
				return
			print 'APPLICATION NAME        STATUS'
			for app in apps:
				appStatus=''
				appName=''
				for apparg in app.childNodes:
					if apparg.nodeName == 'appName':
						appName = apparg.childNodes[0].nodeValue
					elif apparg.nodeName == 'status':
						appStatus = apparg.childNodes[0].nodeValue
				
				print '%-24s%-15s' % (appName, appStatus)
		else:
			print message
		return
	
	if len(appName) > 0:
		status, message = getAppParameter(appName)
		if status == "ok":
			xdoc = minidom.parseString(message)
			params = xdoc.getElementsByTagName('AppParam')
			print 'ID                LABEL                              MANDATORY  DEFAULT VALUE'
			for param in params:
				id = ''
				label = ''
				mandatory = ''
				dValue = ''
				for paramValue in param.childNodes:
					if paramValue.nodeName == 'id':
						id = paramValue.childNodes[0].nodeValue
					elif paramValue.nodeName == 'label':
						label = paramValue.childNodes[0].nodeValue
					elif paramValue.nodeName == 'mandatory':
						mandatory = paramValue.childNodes[0].nodeValue
					elif paramValue.nodeName == 'defaultValue':
						dValue = paramValue.childNodes[0].nodeValue
				print '%-18s%-35s%-11s%-10s' % (id, label, mandatory, dValue)
		else:
			print message
		return
	app_usage()
	return

def jobdata_usage():
	print """
pacclient.py jobdata usage:

pacclient.py jobdata [--help|-h] [--list|-l] job_ID 


For example:
pacclient.py jobdata -l 1234

job_ID
	Specify the job ID.
[--list|-l]
	List all the files for a job.
[--help|-h]
	Display subcommand usage.
	
"""

def main_jobdata(argv):
	if len(argv) == 0:
		jobdata_usage()
		return
	jobId = ''
	list = False
	try:
		opts, args = getopt.getopt(argv, "hl",['help','list'])
	except getopt.GetoptError:
		jobdata_usage()
		return
	for opt, arg in opts:
		if ((opt == "-h") | (opt == "--help")):
			jobdata_usage()
			return
		elif ((opt == "-l") | (opt == "--list")):
			list = True
	if len(args) <= 0:
		print "Please specify the job id."
		return
	jobId = args[0]
	if list == False:
		print "Please specify the proper parameters."
		jobdata_usage()
		return
	files = jobdataList(jobId)
	if len(files) > 0:
		print "HOSTNAME            JOB DATA"
	else:
		return
	try:
		for f in files:
			fileArray = f.split(":")
			if len(fileArray) == 2:
				print "%-20s%-40s" % (fileArray[0], fileArray[1])
	except TypeError:
		print "There are no job data for job " + jobId
		return
	
def main(argv):
	try:
		if ((len(argv) <= 0) | (argv[0] == 'help')):
			main_usage()
			return
		if argv[0] == 'logon':
			main_logon(argv[1:])
			return
		if argv[0] == 'submit':
			main_submit(argv[1:])
			return 
		if argv[0] == 'job':
			main_job(argv[1:])
			return	
		if argv[0] == 'download':
			main_download(argv[1:])
			return
		if argv[0] == 'logout':
			main_logout(argv[1:])
			return
		if argv[0] == 'ping':
			main_ping(argv[1:])
			return
		if argv[0] == 'jobaction':
			main_jobaction(argv[1:])
			return
		if argv[0] == 'app':
			main_app(argv[1:])
			return
		if argv[0] == 'jobdata':
			main_jobdata(argv[1:])
			return
		if argv[0] == 'usercmd':
			main_usercmd(argv[1:])
			return
		if argv[0] == 'upload':
			main_upload(argv[1:])
			return
		print 'This subcommand is not supported: %s.  To view the command usage, run pacclient help. ' % argv[0]
		main_usage()
		return
	except socket.error:
		errno, errstr = sys.exc_info()[:2]
		if errno == socket.timeout:
			print "There was a timeout"
		else:
			print "There was some other socket error"
                        print "errno %s, errstr: %s",(errno, errstr)
	except (KeyboardInterrupt,EOFError):
		pass
	
if __name__ == "__main__":
	if len(sys.argv) <= 1:
		main_usage()
	else:
		main(sys.argv[1:])

