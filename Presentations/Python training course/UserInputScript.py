# -----------------------------------------------------
#  Python Training Exercise 2 Solution.
#  A generalized script
#------------------------------------------------------

# Load the monitor spectrum, asking the  user for file
loadalg = LoadRawDialog(OutputWorkspace="Monitor",spectrummin="2",spectrummax="2",message="Enter the raw file you want to process")

# Retrieve the file that was loaded
file = loadalg.getPropertyValue("Filename")
# Load the main data bank (same file)
LoadRaw(Filename=file,OutputWorkspace="Small_Angle",spectrummin="130",spectrummax="16130")

# Remove the prompt pulse from the monitor
RemoveBins(InputWorkspace="Monitor",OutputWorkspace="Monitor",XMin="19900",XMax="20500",Interpolation="Linear")

# Correct monitor for a flat background
FlatBackground(InputWorkspace="Monitor",OutputWorkspace="Monitor",SpectrumIndexList="0",StartX="31000",EndX="39000")

# Convert monitor to wavelength
ConvertUnits(InputWorkspace="Monitor",OutputWorkspace="Monitor",Target="Wavelength")

# Rebin with a suggested set of parameters
rebinalg = RebinDialog(InputWorkspace="Monitor",OutputWorkspace="Monitor",params="?2.2,-0.035,10",message="Enter the binning you want to use, in wavelength")
rebinparam = rebinalg.getPropertyValue("params")

# Convert data to wavelength
ConvertUnits(InputWorkspace="Small_Angle",OutputWorkspace="Small_Angle",Target="Wavelength")

# Rebin the small angle workspace with the same parameters as the previous Rebin
Rebin(InputWorkspace="Small_Angle",OutputWorkspace="Small_Angle",params=rebinparam)

# Finally, correct for incident beam monitor
Divide(InputWorkspace1="Small_Angle",InputWorkspace2="Monitor",OutputWorkspace="Corrected data")
