from mantid import config
from mantid.kernel import *
from mantid.api import *
import os
import string

class TOFTreatment(PythonAlgorithm):
	
	def PyInit(self):
		self.declareProperty(name='Data Folder', defaultValue='', doc='Where the data is stored', validator=StringMandatoryValidator())
		self.declareProperty(IntArrayProperty(name='File Range', direction=Direction.Input), doc='Data files to read')
		self.declareProperty(name='CorrectX', defaultValue=False, doc='Correct X values for datasets that have different ones')
		self.declareProperty(IntArrayProperty(name='Vanadium Range', direction=Direction.Input), doc='Vanadium files to read')
		self.declareProperty(IntArrayProperty(name='Vanadium FRange', direction=Direction.Input), doc='First and last TOF value to normalise by')
		self.declareProperty(IntArrayProperty(name='Subtract Range', direction=Direction.Input), doc='Empty can files to subtract')
		self.declareProperty(name='Subtraction Fraction', defaultValue=1.0, doc='Amount of background signal to be subtracted')
		self.declareProperty(IntArrayProperty(name='Spectra to mask', direction=Direction.Input), doc='List of spectra to mask')
		self.declareProperty(name='Transmission', defaultValue=1.0, doc='Transmission factor', validator=FloatMandatoryValidator())
		self.declareProperty(name='DetectorEffc', defaultValue=False, doc='Do Detector Efficiency?')
		self.declareProperty(name='CorrectKiKf', defaultValue=False, doc='Do Ki/Kf correction?')
		self.declareProperty(name='Rebin in Energy', defaultValue='-20,0.01,4', doc='Energy rebin parameters : from, bin, to. Use \'No\' none is required', validator=StringMandatoryValidator())
		self.declareProperty(name='Rebin', defaultValue='Classic', doc='Rebin to use', validator=StringListValidator(['Classic','Lamp']))
		self.declareProperty(name='Rebin in Q', defaultValue='0,0.05,4.35', doc='Q rebin parameters : from, bin, to. Use \'No\' none is required', validator=StringMandatoryValidator())
		self.declareProperty(name='Replace NaN', defaultValue=False, doc='Replace NaN values in final data with 0?')


		
	def PyExec(self):
		dataFolder = self.getProperty('Data Folder').value
		fileRange  = self.getProperty('File Range').value
		fileLength = len(fileRange)
		correctx = self.getProperty('CorrectX').value
		vanaRange = self.getProperty('Vanadium Range').value
		vanaLength = len(vanaRange)
		spectraListToMask = self.getProperty('Spectra to mask').value
		transmission = self.getProperty('Transmission').value
		minusRange = self.getProperty('Subtract Range').value
		minusLength = len(minusRange)
		c = self.getProperty('Subtraction Fraction').value
		rebiningInEnergy = self.getProperty('Rebin in Energy').value
		rebinstyle = self.getProperty('Rebin').value
		rebiningInQ = self.getProperty('Rebin in Q').value
		replace = self.getProperty('Replace NaN').value
		correct = self.getProperty('CorrectKiKf').value
		effc = self.getProperty('DetectorEffc').value
		wholevana = False
		try:
			vanadiumFRangeLower= self.getProperty('Vanadium FRange').value[0]
			vanadiumFRangeUpper= self.getProperty('Vanadium FRange').value[-1]
		except:
			wholevana = True
		
		# Read data
		dataFileNames = map(str, fileRange)
		mergedWorkspaceName = 'data_merged'
		
		#Load data
		xvalues = []
		for file in dataFileNames:
			fullPath = os.path.join(dataFolder,file+'.nxs')
			Load(Filename=fullPath,OutputWorkspace=file)
			if correctx:
				xvalues += [mtd[file].readX(0)[0]] # to be able to get most common starting x value
		#Correct the data
		
		if correctx:
			common = max(xvalues, key=xvalues.count) # get most common x value
			foundcorrect = False
			tocorrect = []
		
			for file in dataFileNames:
				ws = mtd[file]
				if ws.readX(0)[0] != common: # if wrong starting x value, add to tocorrect list
					tocorrect += [ws]
				elif not foundcorrect: # for the first correct ws, store it in a variable to be used for setunits
					correctws = ws
					foundcorrect = True
				
			for ws in tocorrect: # correct workspaces in tocorrect
				SetUnits(ws, ParentWorkspace=correctws, UseParentData=True, KeepMonitors=True,Histogram=False, OutputWorkspace=ws)
			

		# Merge runs
		if len(dataFileNames) > 1 :
			fileNamesToMerge = ','.join(dataFileNames)
			MergeRuns(InputWorkspaces=fileNamesToMerge,OutputWorkspace=mergedWorkspaceName)
		else:
			CloneWorkspace(InputWorkspace=dataFileNames[0], OutputWorkspace=mergedWorkspaceName)
			
		# Do sample - t*EC
		MultiplyRange(InputWorkspace=mergedWorkspaceName,OutputWorkspace='Data_t',Factor=transmission)
		
		if (vanaLength>0) & (minusLength>0):
			
			minusFileNames = map(str, minusRange)
			minusMergedWorkspaceName = 'minus_merged'
			
			# Load minus
			
			for file in minusFileNames:
				fullPath = os.path.join(dataFolder,file+'.nxs')
				Load(Filename=fullPath,OutputWorkspace=file)
			
			# Merge runs
			if len(minusFileNames) > 1 :
				fileNamesToMerge = ','.join(minusFileNames)
				MergeRuns(InputWorkspaces=fileNamesToMerge,OutputWorkspace=minusMergedWorkspaceName)
			else:
				CloneWorkspace(InputWorkspace=minusFileNames[0], OutputWorkspace=minusMergedWorkspaceName)
			
			# Do minus - t*EC
			MultiplyRange(InputWorkspace=minusMergedWorkspaceName,OutputWorkspace='Minus_t',Factor=transmission)
			MultiplyRange(InputWorkspace='Minus_t', OutputWorkspace='Minus_t', Factor=c)
			
			# Subtract
			Minus(LHSWorkspace='Data_t',RHSWorkspace='Minus_t', OutputWorkspace='Subtraction', AllowDifferentNumberSpectra=True)
			# Replace NaN
			ReplaceSpecialValues(InputWorkspace='Subtraction', NaNValue='0', InfinityValue='0', OutputWorkspace='Subtraction')
			
			# Read vana
			vanaFileNames = map(str, vanaRange)
			vanaMergedWorkspaceName = 'vana_merged'
			
			# Load vana
			
			for file in vanaFileNames:
				fullPath = os.path.join(dataFolder,file+'.nxs')
				Load(Filename=fullPath,OutputWorkspace=file)
			
			# Merge runs
			if len(vanaFileNames) > 1 :
				fileNamesToMerge = ','.join(vanaFileNames)
				MergeRuns(InputWorkspaces=fileNamesToMerge,OutputWorkspace=vanaMergedWorkspaceName)
			else:
				CloneWorkspace(InputWorkspace=vanaFileNames[0], OutputWorkspace=vanaMergedWorkspaceName)
			
			# Do vanadium - t*EC
			MultiplyRange(InputWorkspace=vanaMergedWorkspaceName,OutputWorkspace='Vanadium_t',Factor=transmission)
			
			# Integrate by bounds if given, whole if not
			if wholevana:
				Integration(InputWorkspace='Vanadium_t',OutputWorkspace='Vanadium_I')
			else:
				Integration(InputWorkspace='Vanadium_t',OutputWorkspace='Vanadium_I',RangeLower=vanadiumFRangeLower,RangeUpper=vanadiumFRangeUpper)
			# Divide the data by the Vanadium integrated in time
			Divide(LHSWorkspace='Subtraction',RHSWorkspace='Vanadium_I',OutputWorkspace='Division',ClearRHSWorkspace='1')
			# Replace NaN
			ReplaceSpecialValues(InputWorkspace='Division',OutputWorkspace='Data_c',NaNValue='0',InfinityValue='0')
			
		elif vanaLength>0: #if only vanadium normalisation is required
			
			# Read vana
			vanaFileNames = map(str, vanaRange)
			vanaMergedWorkspaceName = 'vana_merged'
			
			# Load vana
			
			for file in vanaFileNames:
				fullPath = os.path.join(dataFolder,file+'.nxs')
				Load(Filename=fullPath,OutputWorkspace=file)
			
			# Merge runs
			if len(vanaFileNames) > 1 :
				fileNamesToMerge = ','.join(vanaFileNames)
				MergeRuns(InputWorkspaces=fileNamesToMerge,OutputWorkspace=vanaMergedWorkspaceName)
			else:
				CloneWorkspace(InputWorkspace=vanaFileNames[0], OutputWorkspace=vanaMergedWorkspaceName)
			
			# Do vanadium - t*EC
			MultiplyRange(InputWorkspace=vanaMergedWorkspaceName,OutputWorkspace='Vanadium_t',Factor=transmission)
			
			# Integrate by bounds if given, whole if note
			if wholevana:
				Integration(InputWorkspace='Vanadium_t',OutputWorkspace='Vanadium_I')
			else:
				Integration(InputWorkspace='Vanadium_t',OutputWorkspace='Vanadium_I',RangeLower=vanadiumFRangeLower,RangeUpper=vanadiumFRangeUpper)
			# Divide the data by the Vanadium integrated in time
			Divide(LHSWorkspace='Data_t',RHSWorkspace='Vanadium_I',OutputWorkspace='Division',ClearRHSWorkspace='1')
			# Replace NaN
			ReplaceSpecialValues(InputWorkspace='Division',OutputWorkspace='Data_c',NaNValue='0',InfinityValue='0')
		
		elif minusLength >0: #if only EC subtraction is required
			minusFileNames = map(str, minusRange)
			minusMergedWorkspaceName = 'minus_merged'
			
			# Load minus
			
			for file in minusFileNames:
				fullPath = os.path.join(dataFolder,file+'.nxs')
				Load(Filename=fullPath,OutputWorkspace=file)
			
			# Merge runs
			if len(minusFileNames) > 1 :
				fileNamesToMerge = ','.join(minusFileNames)
				MergeRuns(InputWorkspaces=fileNamesToMerge,OutputWorkspace=minusMergedWorkspaceName)
			else:
				CloneWorkspace(InputWorkspace=minusFileNames[0], OutputWorkspace=minusMergedWorkspaceName)
			
			# Do minus - t*EC
			MultiplyRange(InputWorkspace=minusMergedWorkspaceName,OutputWorkspace='Minus_t',Factor=transmission)
			MultiplyRange(InputWorkspace='Minus_t', OutputWorkspace='Minus_t', Factor=c)
			
			# Subtract
			Minus(LHSWorkspace='Data_t',RHSWorkspace='Minus_t', OutputWorkspace='Subtraction', AllowDifferentNumberSpectra=True)
			# Replace NaN
			ReplaceSpecialValues(InputWorkspace='Subtraction', NaNValue='0', InfinityValue='0', OutputWorkspace='Data_c')
			
		else: #if nothing is required
			ReplaceSpecialValues(InputWorkspace='data_merged',OutputWorkspace='Data_c',NaNValue='0',InfinityValue='0')
		
		# Apply mask
		MaskDetectors(Workspace='Data_c',SpectraList=spectraListToMask)
		
		# Convert from TOF to Energy
		ConvertUnits(InputWorkspace='Data_c',OutputWorkspace='deltaE',Target='DeltaE',EMode='Direct')

		# If asked for, DetectorEffc
		if effc:
			DetectorEfficiencyCorUser(InputWorkspace='deltaE', OutputWorkspace='deltaE')		
		# If asked for, KiKf correction
		if correct:
			CorrectKiKf('deltaE', OutputWorkspace='deltaE')

		
		# Rebin in energy
		if rebiningInEnergy != 'No':
			if rebinstyle=='Classic':
				Rebin(InputWorkspace='deltaE',OutputWorkspace='deltaE_r',Params=rebiningInEnergy,PreserveEvents='0')
			else:
				params = map(float, string.split(rebiningInEnergy, ','))
				LampRebin(InputWorkspace='deltaE', StartBin=int(params[0]), BinWidth=params[1], EndBin=int(params[2]), OutputWorkspace='deltaE_r')
		else:
			return
		
		# Apply SofQW
		if rebiningInQ != 'No':
			SofQW3(InputWorkspace='deltaE_r',OutputWorkspace='SofQW',QAxisBinning=rebiningInQ,EMode='Direct')
		else:
			return
		
		# If asked for, replace nan with 0
		if replace:
			ReplaceSpecialValues('SofQW', NaNValue='0', InfinityValue='0', OutputWorkspace='SofQW')
			
AlgorithmFactory.subscribe(TOFTreatment)
		
			
		
		
		
		
		
		
		
		
