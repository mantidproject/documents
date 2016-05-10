from mantid import config
from mantid.kernel import *
from mantid.api import *
import numpy
import math

def GetDict(InputWorkspace, Spectrum, Start, BinWidth, End):

	# Get the data
	datax = InputWorkspace.readX(Spectrum)
	datay = InputWorkspace.readY(Spectrum)
	
	# Get the start and end index
	start_i = 0
	end_i = len(datax)
	for i in range(0, len(datax)):
		if datax[i]>Start:
			start_i = i
			break
	for i in range(len(datax), start_i, -1):
		if datax[i-1]<End:
			end_i = i
			break
	# Create end data arrays
	endx = numpy.arange(Start, End+BinWidth, BinWidth)
	endy = numpy.empty(len(endx))
	ind  = start_i
	dic = {}
	# Iterate through the x values
	for v in range(0, len(endx)):
		value = endx[v] # get value at index
		dif = 0 # variable to get closest x value
		found = False # variable to know when to break
		start = ind # variable to start where last loop left off
		for i in range(start, end_i): #iterate through original xvalues
			temp = math.fabs((datax[i] - value)) # get difference
			if (dif == 0) | (temp<dif): # only select the lowest difference
				dif = temp
				ind = i # at the end of the loop, should contain the index of the closest x value in the original x data
			if (round(temp) == 0) & (found == False): #once you've got the right integer value, you've "found" the value
				found = True
			if (round(temp) !=0) & (found == True): #if you've found and it's not longer the right integer, you've gone too far
				break
		dic[v] = ind
	return dic


def TestRebin(Input, Spectrum, Start, Bin, End, Dic):
		
	# Get the data
	datax = Input.readX(Spectrum)
	datae = Input.readE(Spectrum)
	datay = Input.readY(Spectrum)
	
	# Create end data arrays
	endx = numpy.arange(Start, End+Bin, Bin)
	endy = numpy.empty(len(endx)-1)
	ende = numpy.empty(len(endy))
	
	for i in range(0, len(endy)):
		try:
			endy[i] = datay[Dic[i]] #look the value up in the provided dictionnary
			ende[i] = datae[Dic[i]]
		except:
			endy[i] = 0
			ende[i] = 0
		
	output = WorkspaceFactory.create("Workspace2D", NVectors=1, XLength=len(endx), YLength=len(endy))
	output.setX(0, endx)
	output.setY(0, endy)
	output.setE(0, ende)
	return output
 
class LampRebin(PythonAlgorithm):
	
	def PyInit(self):
		self.declareProperty(WorkspaceProperty(name='InputWorkspace', defaultValue='', direction=Direction.Input))
		self.declareProperty(IntArrayProperty('Spectra'))
		self.declareProperty('StartBin',0, IntMandatoryValidator())
		self.declareProperty('BinWidth', 1.0, FloatMandatoryValidator())
		self.declareProperty('EndBin', 0, IntMandatoryValidator())
		self.declareProperty(WorkspaceProperty(name="OutputWorkspace", defaultValue="",direction=Direction.Output))
		
		
	def PyExec(self):
		ws = self.getProperty('InputWorkspace').value
		spectra = self.getProperty('Spectra').value
		if len(spectra)==0:
			spectra = numpy.arange(0, ws.getNumberHistograms())
			
		start = self.getProperty('StartBin').value
		bin = self.getProperty('BinWidth').value
		end = self.getProperty('EndBin').value		
		lines = ws.getNumberHistograms()
		length = int((end-start)/bin) + 1
		for i in range(0, ws.getNumberHistograms()): # get first non-monitor index
			if not ws.getDetector(i).isMonitor():
				break
		Dic = GetDict(ws, i, start, bin, end) #get dictionnary for first non monitor index
		output_ws = WorkspaceFactory.create(ws, NVectors=lines, XLength=length, YLength=length-1)
		prog_reporter = Progress(self,start=0.0,end=1.0, nreports=len(spectra))
		for i in spectra:
			data = TestRebin(ws,i, start, bin, end, Dic)
			output_ws.setX(i, data.readX(0))
			output_ws.setY(i, data.readY(0))
			output_ws.setE(i, data.readE(0))
			prog_reporter.report()

		self.setProperty('OutputWorkspace', output_ws)

AlgorithmFactory.subscribe(LampRebin)
