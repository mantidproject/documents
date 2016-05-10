from mantid import config
from mantid.kernel import *
from mantid.api import *

class OverPlot(PythonAlgorithm):
	
	def PyInit(self):
		self.declareProperty(WorkspaceProperty(name='Workspace1', defaultValue='', direction=Direction.Input))
		self.declareProperty(WorkspaceProperty(name='Workspace2', defaultValue='', direction=Direction.Input))
		self.declareProperty(name='Scale', defaultValue='max', doc='Scale with maximum or minimum point', validator=StringListValidator(['max','min','none']))
		self.declareProperty(name='Spectra', defaultValue=0, doc='Spectra to plot', validator=IntMandatoryValidator())
		self.declareProperty(name='Spectra2', defaultValue=-1, doc='If you want the same spectra, leave empty', validator=IntMandatoryValidator())
		self.declareProperty(name='Title', defaultValue=' ', validator=StringMandatoryValidator())
		self.declareProperty(name='PlotFrom', defaultValue='0', doc='X value to plot from', validator=StringMandatoryValidator())
		self.declareProperty(name='PlotTo', defaultValue='100', doc='X value to plot to', validator=StringMandatoryValidator())
		self.declareProperty(name='Errors', defaultValue=False, doc='Plot error bars or not')


	def PyExec(self):
		ws1 = self.getProperty('Workspace1').value
		ws2 = self.getProperty('Workspace2').value
		scale = self.getProperty('Scale').value
		spectra = self.getProperty('Spectra').value
		spectra2 = self.getProperty('Spectra2').value
		plotfrom = float(self.getProperty('PlotFrom').value)
		plotto = float(self.getProperty('PlotTo').value)
		title = self.getProperty('Title').value
		errors = self.getProperty('Errors').value
		
		if title == ' ':
			title = str(ws1) + ' vs ' + str(ws2)
		
		# if spectra2 is not specified, then set it to same as spectra1
		if spectra2 == -1:
			spectra2 = spectra
		if scale != 'none':
			if scale == 'max': # if you want to rescale with maximum
				# get maximum values, for rescaling
				max1 = max(ws1.readY(spectra))
				max2 = max(ws2.readY(spectra2))
			elif scale == 'min':
				# get minimum values for rescaling
				max1 = min(ws1.readY(spectra))
				max2 = min(ws2.readY(spectra2))
			ratio = max1/max2
			print ratio
		
			# Scale with ratio
			scaled = Scale(InputWorkspace=ws2, Factor=ratio, OutputWorkspace= str(ws2) + '_' + str(spectra) + '_scaled')
		else:
			scaled = ws2
		
		# Overplot them
		if errors:
			g1 = plotSpectrum(ws1, spectra, error_bars=True)
			g2 = plotSpectrum(scaled, spectra2, error_bars=True)
		else:
			g1 = plotSpectrum(ws1, spectra)
			g2 = plotSpectrum(scaled, spectra2)
		g3 = mergePlots(g1, g2)
		g3.activeLayer().setTitle(title)
		g3.activeLayer().setAxisScale(Layer.Bottom, plotfrom, plotto)
		g3.activeLayer().setCurveTitle(0, str(ws1))
		g3.activeLayer().setCurveTitle(1, str(ws2))
		
AlgorithmFactory.subscribe(OverPlot)		
		
		

