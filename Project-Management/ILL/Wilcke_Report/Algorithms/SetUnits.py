from mantid import config
from mantid.kernel import *
from mantid.api import *
import numpy

class SetUnits(PythonAlgorithm):
	
	def PyInit(self):
		units = ['Degrees','DeltaE','DeltaE_inWavenumber','dSpacing','Empty','Energy','Energy_inWavenumber','Momentum','MomentumTransfer','QSquared','Spectrum','SpinEchoLength','SpinEchoTime','Time','TOF','Wavelength']
		self.declareProperty(WorkspaceProperty(name='InputWorkspace', defaultValue='', direction=Direction.Input))
		self.declareProperty(WorkspaceProperty(name='OutputWorkspace', defaultValue='', direction=Direction.Output))
		self.declareProperty(name='XUnit',defaultValue='TOF', validator=StringListValidator(units))
		self.declareProperty(name='YUnit', defaultValue='SpectraNumber', validator=StringListValidator(units))
		self.declareProperty(name='YLabel', defaultValue='')
		self.declareProperty(name='ParentWorkspace', defaultValue='',doc='If you want to import units from an existing workspace')
		self.declareProperty(name='UseParentData',defaultValue=False,doc='Whether to use X-data from the parent workspace')
		self.declareProperty(name='KeepMonitors',defaultValue=False,doc='Whether keep monitors in parent data')
		self.declareProperty(name='Histogram',defaultValue=False,doc='Whether to add an X-value, to make it histogram data')
	def PyExec(self):
		ws = self.getProperty('InputWorkspace').value
		xunit = self.getProperty('XUnit').value
		yunit = self.getProperty('YUnit').value
		ylabel = self.getProperty('YLabel').value
		try:
			parent = mtd[self.getProperty('ParentWorkspace').value]
		except: #if this throws a error, it's because an invalid (or no) parentworkspace was given, so use nothing
			parent = ''
		parentdata = self.getProperty('UseParentData').value
		histo = self.getProperty('Histogram').value
		monitors = self.getProperty('KeepMonitors').value
		lines = ws.getNumberHistograms()
		
		if (histo) & (not ws.isHistogramData()): #if the user wants the output to be a histogram and the data is not already in histogram form, add one x value
			lenx = len(ws.readX(0)) +1
		else:
			lenx = len(ws.readX(0))
		leny = len(ws.readY(0))
		
		if parent != '': #if using a aprentworkspace
			i = 0
			if not monitors: #if ignoring monitors
				while parent.getDetector(i).isMonitor(): #iterate until first non monitor spectrum
					i+=1
			croppedparent = CropWorkspace(parent, StartWorkspaceIndex=i) #crop parent to remove monitors
			output = WorkspaceFactory.create(croppedparent, NVectors=lines, XLength=lenx, YLength=leny) #create output using cropped parent
		else: # if not, just create one using the input workspace as base
			output = WorkspaceFactory.create(ws, NVectors=lines, XLength=lenx, YLength=leny)
			# set units
			try:
				output.getAxis(0).setUnit(xunit)
			except:
				output.getAxis(0).setUnit('Label').setLabel(xunit,'')
			try:
				output.getAxis(1).setUnit(yunit)
			except:
				output.getAxis(1).setUnit('Label').setLabel(yunit, '')
			output.setYUnitLabel(ylabel)
				
		if parentdata: #if user wants to replace x data with the parent data
			try:
				datax = numpy.delete(croppedparent.readX(0), range(lenx, len(croppedparent.readX(0))))
				print 'datax', len(datax)
			except: # if the above throws an error, it is because an invalid/no parentworkspace was specfied
				datax = ws.readX(0) # continue as if no parent workspace was specified
				print 'You are not using a parent workspace' #report the error to let user know

		else:
			datax = ws.readX(0) # use the input data
		try:	
			DeleteWorkspace(croppedparent) # we do not need the cropped parent for anything else
		except:
			pass # if this throws an erorr, it is because no parentworkspace is being used, so we can safely ignore it

		if (histo) & (len(datax) != lenx): # if the length of datax and the length of the x-array in the workspace are not the same, add a data point to datax
										    # so that the length becomes the same
			ind = len(datax)
			datax = numpy.append(datax,  2*datax[ind-1] - datax[ind - 2])			
		 
		#set data
		for i in range(0, lines):
			datay = ws.readY(i)
			datae = ws.readE(i)
			
			output.setX(i, datax)
			output.setY(i, datay)
			output.setE(i, datae)
		
		
			
		self.setProperty('OutputWorkspace',output)
		
AlgorithmFactory.subscribe(SetUnits)
			
		
		