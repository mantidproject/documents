import sys, StringIO, re
import urllib2
import socket


def captureMantidHelp(name=""):
	"""Capture the output from mtdHelp and return as a string"""
	#capture object
	capture = StringIO.StringIO()
	
	#store stdout and replace with capture
	savedValue = sys.stdout
	sys.stdout = capture

	mtdHelp(name)
	#replace stdout
	sys.stdout = savedValue
	
	return capture.getvalue()


def getAglorithmList():
	"""parse the algorithm list from mtdHelp and return a list of algorithms"""
	return re.findall("\\t(\\w+)$", captureMantidHelp(),re.MULTILINE)
	
def CheckWikiPageExists(url,useProxy=0):
	"""returns true if the url exists, otherwise false
	If useProxy is 0 and it is refused by the proxy it will try again, this time using the standard proxy.
	"""
	timeout = 15 #5 seconds
	socket.setdefaulttimeout(timeout)
  
	if useProxy:
		#set proxy
		proxies = {'http': 'http://wwwcache.rl.ac.uk:8080/'}
	else:
		proxies = {}
	proxy_support = urllib2.ProxyHandler(proxies)
	opener = urllib2.build_opener(proxy_support)
	urllib2.install_opener(opener)
  
	#print message
	try:
		f = urllib2.urlopen(url) 
		return True
	except urllib2.HTTPError, e:
		if (e.code == 404): #not found
			return False
	except:
		if useProxy==0:
			return sendNotification(url,1)
		else:
			raise


def checkAlgDocumentation():
	"""prints a line for all algorithms that do not have a wiki page"""
	#mantid wiki url
	baseurl = "http://www.mantidproject.org/"
	
	for alg in getAglorithmList():
		try:
			if (CheckWikiPageExists(baseurl+alg,1) == False):
				print alg
		except urllib2.URLError, e:
			print alg,e

def createAlgPage(alg):
	"""creates the algorithm help page for the project wiki and returns it as a string"""
	helpStr = captureMantidHelp(alg)
	if helpStr.strip().endswith("not found in help list"):
		return helpStr
		
	usageMatch = re.search("Usage:\s*(\w.+)$",helpStr,re.MULTILINE)
	usage = usageMatch.group(1)
	algNameMatch = re.search("(\w+)\(",usage)
	algName = algNameMatch.group(1)
	
	retVal = createAlgWikiHeader(algName)
	retVal += createAlgWikiTableHeader()
	
	#strip off the usage lines and column headers
	paramTable = re.sub("^.*Allowed Values(?s)","",helpStr).strip()
	#split into each parameter
	paramTableList = re.split("-{10,}",paramTable)
	i=0
	for pt in paramTableList:
		pt = pt.strip()
		if pt != "":
			(name, direction, type, isRequired, description, allowed) = parseParamter(pt)
			i+=1
			retVal += createAlgWikiTableEntry(i,name, direction, type, isRequired, description, allowed)

	retVal += createAlgWikiTableFooter()
	retVal += createAlgWikiFooter(algName)
	return retVal

def parseParamter(parameterString):
	"""Parses a single parameter entry from MantidHelp
	outputs a tuple of name, direction, type, isRequired, description, allowed values
	"""
	output= ["","","","","","",""]	

	for line in parameterString.split("\n"):
		columns = re.split(r"\|",line)
		for i in range(0,len(columns)):
			column = columns[i]
			column = column.strip()
			if column != "":
				output[i] = output[i] + column
	#columns are this in order dummy, name, direction, type, isRequired, description, allowed values
	return (output[1], output[2], output[3], output[4], output[5], output[6])

def createAlgWikiHeader(algName):
	"""creates the header for an algorithm wiki page"""
	return """== Summary ==

"""

def createAlgWikiFooter(algName):
	"""creates the header for an algorithm wiki page"""
	retval = "== Description ==\n\n"
	retval += "[[Category:Algorithms]]\n"
	retval += "[[Category:Library MantidDataHandling]]\n"
	retval += "{{AlgorithmLinks|" + str(algName) + "}}\n"
	return retval

def createAlgWikiTableHeader():
	"""creates the header for an algorithm properties table"""
	return """== Properties ==
{| border="1" cellpadding="5" cellspacing="0"
!Order
!Name
!Direction
!Type
!Default
!Description
|-
"""

def createAlgWikiTableFooter():
	"""creates the header for an algorithm properties table"""
	return "|}\n"

def createAlgWikiTableEntry(index,name, direction, type, isRequired, description, allowed):
	"""creates an entry for an algorithm properties table"""
	retval = "|" + convertTowikiTableString(index) + "\n"
	retval += "|" + convertTowikiTableString(name) + "\n"
	retval += "|" + convertTowikiTableString(direction) + "\n"
	retval += "|" + convertTowikiTableString(type) + "\n"
	retval += "|"
	if (len(isRequired.strip())>0):
		retval +="Mandatory"
	else:
		retval +="&nbsp;"
	retval += "\n"
	retval += "|" + convertTowikiTableString(description) + "\n"
	if (len(allowed.strip())>0):
		retval += "Allowed Values are: " + str(allowed) + "\n"
	
	retval += "|-\n"
	return retval

def convertTowikiTableString(value):
	valueStr = str(value)
	if len(valueStr.strip()) == 0:
		valueStr = "&nbsp;"
	return valueStr

print createAlgPage("MaskDetectorsIf")

