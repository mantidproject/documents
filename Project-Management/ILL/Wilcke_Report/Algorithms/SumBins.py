from mantid import config
from mantid.kernel import *
from mantid.api import *
import numpy
import math

# used to get the start and end values of a specfiic workspace
def getBoundary(Workspace, spectrum):
	ws = Workspace
	datax = ws.readX(spectrum)
	datay = ws.readY(spectrum)
	start = 0 #initialise at 0
	end = 0 # intialise at 0
	for i in range(0, len(datay)): #iterate through the data
		if (datay[i] != 0): #until the data is no longer 0
			start = datax[i] #return the start value
			break #and end loop

	for i in range(len(datay)-1, 0, -1): #same process for end
		if datay[i] != 0:
			end = datax[i]
			break
	
	return start, end

#used to get the spectra number with the closest start and end values
def getNum(Workspace, Start, End):
	ws = Workspace
	lines = ws.getNumberHistograms()
	lenx = len(ws.readX(0))
	leny = len(ws.readY(0))
	dif = -1 #initialise at -1, which is an impossible difference, to make sure that it is not interfering with the loop
	ind = 0
	for i in range(0, lines): #iterate through spectra
			open, close = getBoundary(Workspace, i) #get the start and end of this spectra
			temp = math.fabs(Start-open) + math.fabs(End-close) #store total difference in temp
			if (dif==-1) | (temp<dif): #if first run or if the temp difference is smaller than smallest difference, continue
				dif = temp
				ind = i
	return ind #at the end of the loop, contains closest match
	
class SumBins(PythonAlgorithm):
	
	def PyInit(self):
		self.declareProperty(WorkspaceProperty(name='InputWorkspace', defaultValue='', direction=Direction.Input))
		self.declareProperty(WorkspaceProperty(name='OutputWorkspace', defaultValue='', direction=Direction.Output))
		self.declareProperty(name='Xunit', defaultValue='Detector ID', doc='Unit of the output workspace', validator=StringListValidator(['Detector ID','MomentumTransfer']))
		self.declareProperty(name='Qbinning', defaultValue=0.05, doc='Q binning of the workspace, to be able to convert to Q')
		self.declareProperty(name='AdjustQvalue', defaultValue='', doc='Workspace with the Q values to adjust to')
		self.declareProperty(name='Monitors', defaultValue=False, doc='Whether to include monitors or not')
		
	def PyExec(self):
		ws = self.getProperty('InputWorkspace').value
		unit = self.getProperty('Xunit').value
		bin = self.getProperty('Qbinning').value
		adjust = self.getProperty('AdjustQvalue').value
		monitors = self.getProperty('Monitors').value
		start = 0
		if not monitors:
			while ws.getDetector(start).isMonitor():
				start+=1
		lines = ws.getNumberHistograms()
		datay = numpy.zeros(lines-start) # for the y-data
		datae = numpy.zeros(lines-start) # for the errors
		prog_reporter = Progress(self,start=0.0,end=1.0, nreports=lines)
		for i in range(start, lines):
			datay[i-start] = sum(ws.readY(i)) #set each value to the sum of the line
			datae[i-start] = sum(ws.readE(i)) #do the same for errors
			prog_reporter.report()
			
		# create the output
		output = WorkspaceFactory.create('Workspace2D', NVectors=1, XLength=lines-start, YLength=lines-start)
		# set the units
		if unit=='Detector ID':
			output.getAxis(0).setUnit('Label').setLabel(unit, '')
		else:
			output.getAxis(0).setUnit(unit)
		output.setYUnit('Label')
		output.setYUnitLabel('Counts')
		
		# if not adjusting to another workspace, just use values from 0 to end for x data
		if len(adjust) == 0:
			datax = numpy.arange(0,lines-start)
		else: # for adjusting x data
			comp = mtd[adjust] #get the workspace to adjust to
			spectra =  [] #initialise empty list
			for v in range(start, lines):
				open, close = getBoundary(ws, v) #get start and end values of the workspace
				spectra += [getNum(comp, open, close)] #get closest match in adjusting workspace, and append it to the list
			datax = numpy.asarray([int(spectra[i]) for i in range(0, lines-start)]) #replace each detector id with the closest one, which is stored in spectra
		if unit=='MomentumTransfer': # if you want the data in q, multiply x data by the q binning
			datax = numpy.asarray([x*bin for x in datax])
		output.setX(0, datax)
		output.setY(0, datay)
		output.setE(0, datae)
		
		self.setProperty('OutputWorkspace',output)
		
AlgorithmFactory.subscribe(SumBins)
		

		
