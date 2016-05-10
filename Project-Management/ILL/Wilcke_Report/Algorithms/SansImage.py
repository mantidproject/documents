from mantid import config
from mantid.kernel import *
from mantid.api import *
import numpy as np

class SANSImage(PythonAlgorithm):
	
	def PyInit(self):
		self.declareProperty(WorkspaceProperty(name='InputWorkspace', defaultValue='', direction=Direction.Input))
		self.declareProperty(name='OutputWorkspace',defaultValue='', doc='Name of the output workspace')
		self.declareProperty(IntArrayProperty(name='Frames'), doc='Frames or wavelengths to be plotted')
		self.declareProperty(name='Method', defaultValue='Sum', doc='Whether to sum or to average the frames', validator=StringListValidator(['Sum','Average']))
		
	def PyExec(self):
		ws = self.getProperty('InputWorkspace').value
		output = self.getProperty('OutputWorkspace').value
		frames = self.getProperty('Frames').value
		method = self.getProperty('Method').value		
		if ws.getAxis(0).getUnit().caption() == 'Wavelength': 
			for i in range(0, ws.getNumberHistograms()): # get first non-monitor index
				if not ws.getDetector(i).isMonitor():
					break
			CropWorkspace(ws, StartWorkspaceIndex=i, EndWorkspaceIndex=128*256+1, OutputWorkspace=str(ws)+'_c') #crop to remove monitors, and to remove pannels, keeping only central detector
			ws = Transpose(InputWorkspace=str(ws)+'_c', OutputWorkspace=str(ws)+'_c') # transpose data
		
		# format data to image
		x = range(1,257)*128
		y = np.zeros(len(ws.readY(0)))
		e = np.zeros(len(ws.readY(0)))
		if len(frames)>1: # if several frames are used, average them
			for i in frames: #iterate through the frames
				y += ws.readY(i) #add the data together
				e += ws.readE(i)
			if method == 'Average':
				y = y/float(len(frames)) #divide by length
				e = e/float(len(frames))
		else: # if just one frame, read it
			y = ws.readY(frames[0])
			e = ws.readE(frames[0])
		
		#create output, reformating data to have 128 spectra
		output = CreateWorkspace(DataX=x, DataY=y, DataE=e, NSpec=128, OutputWorkspace=output)
		#set units
		output.getAxis(0).setUnit('Label').setLabel('Pixels','')
		output.getAxis(1).setUnit('Label').setLabel('Pixels','')
		output.setYUnit('Neutron')
		output.setYUnit('Counts')

		
AlgorithmFactory.subscribe(SANSImage)
