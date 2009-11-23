# -----------------------------------------------------
#  Python Training Exercise 2 Solution.
#  A generalized script
#------------------------------------------------------

# Load the monitor spectrum, asking the  user for file
loadalg = LoadRawDialog(OutputWorkspace="Monitor",SpectrumMin="2", SpectrumMax="2",Message="Enter the raw file you want to process")

# Retrieve the file that was loaded
file = loadalg.getPropertyValue("Filename")
# Load the main data bank (same file)
LoadRaw(Filename=file,OutputWorkspace="Small_Angle",SpectrumMin="130", SpectrumMax="16130")

# Remove the prompt pulse from the monitor
RemoveBins(InputWorkspace="Monitor",OutputWorkspace="Monitor",XMin="19900",XMax="20500",Interpolation="Linear")

# Correct monitor for a flat background
FlatBackground(InputWorkspace="Monitor",OutputWorkspace="Monitor",WorkspaceIndexList="0",StartX="31000",EndX="39000")

# Convert monitor to wavelength
ConvertUnits(InputWorkspace="Monitor",OutputWorkspace="Monitor",Target="Wavelength")

# Rebin with a suggested set of parameters
rebinalg = RebinDialog(InputWorkspace="Monitor",OutputWorkspace="Monitor",Params="2.2,-0.035,10",Message="Enter the binning you want to use, in wavelength",Enable="Params")
rebinparam = rebinalg.getPropertyValue("Params")

# Convert data to wavelength
ConvertUnits(InputWorkspace="Small_Angle",OutputWorkspace="Small_Angle",Target="Wavelength")

# Rebin the small angle workspace with the same parameters as the previous Rebin
Rebin(InputWorkspace="Small_Angle",OutputWorkspace="Small_Angle",Params=rebinparam)

# Finally, correct for incident beam monitor
Divide(LHSWorkspace="Small_Angle",RHSWorkspace="Monitor",OutputWorkspace="Corrected data")
