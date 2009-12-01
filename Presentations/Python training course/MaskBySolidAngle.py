# -----------------------------------------------------
#  Python Training Exercise 4 Solution.
#  Masking detectors by solid angle
#------------------------------------------------------
from mantidsimple import *

inputData = "GEM40979"
path = "C:\\Mantid\\Test\\data\\"
# Load the first bank of a GEM set
LoadRaw(Filename = path + inputData + ".raw", OutputWorkspace = inputData, SpectrumMin="101",SpectrumMax="430")

# Integrate the workspace and overwrite the raw data workspace
# The output will be a workspace with 1 value per spectra
summed = "SummedData"
Integration(inputData, summed)

# Get the workspace from mantid
integrated = mantid.getMatrixWorkspace(summed)
nhist = integrated.getNumberHistograms()

# Need to find the sample position to be able to calculate the solid angle for a specific detector
# The instrument knows about the sample
instrument = integrated.getInstrument()
sample_pos = instrument.getSample().getPos()

# Divide by the solid angle for each spectra. Define a list to append to
normalized_values = []
sum_total = 0.0
counter = 0
notfound = []
for index in range(0, nhist):
	counts = integrated.readY(index)[0]
	try:
		detector = integrated.getDetector(index)
		if detector.isMonitor() == True:
			normalized_values.append(0.0)
			notfound.append(index)
			continue
		solid_angle = detector.solidAngle(sample_pos)
		counts_per_sa = counts/solid_angle
		# Store the counts/solid angle for later
		normalized_values.append(counts_per_sa)
		# Add to get the average
		sum_total += counts_per_sa
		counter +=1
	except:
		# Append a zero but do not increment the counter
		normalized_values.append(0.0)
		notfound.append(index)
		pass

if not len(normalized_values) == nhist:
	exit("An error occurred while processing the solid angle loop")
	
# Divide the sum by the number of values to get the average
average = sum_total/counter

# Deviation in percent
deviation = 100.0
mask_string = ''
for index in range(0, nhist):
	y = normalized_values[index]
	# Avoid divide by zero 
	if y < 1e-08:
		continue
	test = abs(y - average) / y
	if test * 100.0 > deviation and not index in notfound:
		mask_string+=  str(integrated.getDetector(index).getID())+ ","

# Finally mask those detectors that deviate too far from the average
MaskDetectors(inputData, DetectorList=mask_string)
