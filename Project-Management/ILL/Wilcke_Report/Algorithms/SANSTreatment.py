from mantid import config
from mantid.kernel import *
from mantid.api import *

class SANSTreatment(PythonAlgorithm):
	
	def PyInit(self):
		self.declareProperty(name='DataDir',defaultValue='',doc='Where the data is stored', validator=StringMandatoryValidator())
		self.declareProperty(name='WavelengthDir', defaultValue='', doc='Where the frame/wavelength correspondance file is stored')
		self.declareProperty(IntArrayProperty(name='MaskedDetectors', direction=Direction.Input))
		self.declareProperty(name='Sample', defaultValue='', validator=StringMandatoryValidator())
		self.declareProperty(name='BeamCenter', defaultValue='', validator=StringMandatoryValidator())
		self.declareProperty(name='DarkCurrent', defaultValue='', validator=StringMandatoryValidator())
		self.declareProperty(name='SampleTransmission', defaultValue='', validator=StringMandatoryValidator())
		self.declareProperty(name='EmptyTransmission', defaultValue='', validator=StringMandatoryValidator())
		self.declareProperty(name='BckEmptyTransmission', defaultValue='', validator=StringMandatoryValidator())
		self.declareProperty(name='Background', defaultValue='', validator=StringMandatoryValidator())
		self.declareProperty(name='BckSampleTransmission', defaultValue='', validator=StringMandatoryValidator())
		self.declareProperty(FloatArrayProperty(name='Parameters', direction=Direction.Input), doc='First frame, bindwidth and last frame, or start bin, binwidth and end bin')
	
	def PyExec(self):
		data_dir = self.getProperty('DataDir').value
		sample_file = data_dir + self.getProperty('Sample').value + '.nxs'
		frames = self.getProperty('Parameters').value
		try: #if this raises an error, it's because something is wrong with the wavlength file (wrong format, wrong directory, etc...)
			file = open(self.getProperty('WavelengthDir').value) #get the file
			values = map(lambda x: round(float(x), 2), file.readlines()) #round everything to 2 significant figures
			parameters = str(values[int(frames[0]-1)]) + ',' + str(frames[1]) + ',' + str(values[int(frames[2]-1)]) #get wavelengths corresponding to given frames
			print 'Using Frames'
			file.close()
		except:
			parameters = ','.join(map(str, frames)) #join values given, putting them in readable format
			print 'Using Wavelength'
		detectors = self.getProperty('MaskedDetectors').value
		beam = self.getProperty('BeamCenter').value + '.nxs'
		darkcurrent = self.getProperty('DarkCurrent').value + '.nxs'
		sampletrans = self.getProperty('SampleTransmission').value + '.nxs'
		emptytrans = self.getProperty('EmptyTransmission').value + '.nxs'
		bckemptytrans = self.getProperty('BckEmptyTransmission').value + '.nxs'
		bck = self.getProperty('Background').value + '.nxs'
		bcksampletrans = self.getProperty('BckSampleTransmission').value + '.nxs'
		
		SetupILLD33Reduction(
			# Beam center shouldn't work
			#BeamCenterMethod="None",
			MaskedDetectorList=detectors,
			BeamCenterMethod="DirectBeam",
			BeamCenterFile="%s/%s" % (data_dir, beam),
			Normalisation="Timer",
			DarkCurrentFile= "%s/%s" % (data_dir, darkcurrent),
			TransmissionMethod="DirectBeam",
			TransmissionSampleDataFile= "%s/%s" % (data_dir, sampletrans),
			TransmissionEmptyDataFile= "%s/%s" % (data_dir, emptytrans),
			BckTransmissionEmptyDataFile= "%s/%s" % (data_dir, bckemptytrans),
			TransmissionBeamRadius = 3,
			TransmissionUseSampleDC=False,
			BackgroundFiles="%s/%s" % (data_dir, bck),
			BckTransmissionSampleDataFile="%s/%s" % (data_dir, bcksampletrans),
			DoAzimuthalAverage=False,
			Do2DReduction=False,
			ComputeResolution=True,
			ReductionProperties="d33")
			
		SANSReduction(Filename=sample_file, ReductionProperties="d33",OutputWorkspace="d33out")

		Rebin(InputWorkspace='d33out',OutputWorkspace='d33out_rebin',Params=parameters)
		SANSAzimuthalAverage1D(InputWorkspace='d33out_rebin',Binning='0.001,0.0002,0.07',OutputWorkspace='IQ_curve')
		
AlgorithmFactory.subscribe(SANSTreatment)
		
		
		
