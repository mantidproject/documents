## Example script for IN5

**To Do: Test these and tidy them up**

Data -[IN5_He4](https://www.ill.eu/fileadmin/users_files/img/instruments_and_support/support_facilities/computing_for_science/Computing_for_Science/Data_analysis/IN5_He4.zip)

```python
# --------------------------------------------------------------------------
#
#   vana 4.0A: 95895 - 95897
#   vana 4.8A: 95893 - 95894
#   vana 3.2A: 95898 - 95900
#
#   He4 3.2A 2K SVP: 95985 - 95990
#   He4 3.2A LT SVP: 96010 - 96012
#   He4 4.0A LT SVP: 95997 - 96002
#   He4 4.8A LT SVP: 96003 - 96009
#
#   EC  4.0A LT SVP: 95933 - 95939
#
# Run in the python interface:
# -----------------------------
# In [4]: execfile('he_4A.py')
#
#    In [23]: execfile('he_4A.py')
#    Load vana  7.30283904076 seconds
#    Load sample  29.9830768108 seconds
#    Load sample  32.7425868511 seconds
#     -------------------------------------------
#    Total time spent =  273.347508907  sec.
#     -------------------------------------------
#
#  Monitor norrmsalisation ?
#
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# from mantid import mantid defs
import os
from mantid import config 

# --------------------------------------------------------------------------
# Only edit this bit!
# --------------------------------------------------------------------------
dataFolder    = '/usr/illdata/121/in5/'
dataFileNames = r'95997-96002'
vanaFileNames = r'95895-95896'
ECFileNames   = r'95933-95939'

# range in TOF ( for vana ELP integration )
vanadiumFRangeLower = 6000
vanadiumFRangeUpper = 6500

maskFile = '/opt/Mantid/instrument/masks/IN5_Mask.xml'
transmission     =  0.98           # Sample transmission
rebiningInEnergy = '-1.0,0.02,3.7' # from, step, to (according to setup and Temp)
rebiningInQ      = '0,0.02,3.0'    # from, step, to

# Add directory to the list (for numors)
config.appendDataSearchDir('/usr/illdata/121/in5/') 

# Load Mask of bad spectra (incomplet!)
LoadMask(Instrument='IN5',InputFile=maskFile ,OutputWorkspace='IN5_Mask')

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# start of the full operation (from load raw data to display S(Q,w)
#	 -------------------------------------------
#		Total time spent =  519.700006962  sec.
#	 -------------------------------------------
# --------------------------------------------------------------------------
t0 = time.time()

# --------------------------------------------------------------------------
#  Load the vanadium 
# --------------------------------------------------------------------------
start_time = time.time()
Load(Filename = vanaFileNames,OutputWorkspace = 'Vana')
print "Load vana ", time.time() - start_time, "seconds"

# -----------------------------------------------------------------------------------------
# 1.1.2) Eventually remove bad pixels
# -----------------------------------------------------------------------------------------
# Apply mask to the detector - data
MaskDetectors(Workspace='Vana',MaskedWorkspace='IN5_Mask')

# --------------------------------------------------------------------------
#  Load the Data He 4A 
# (Neeed the vana for ELP)
# --------------------------------------------------------------------------
start_time = time.time()
Load(Filename = dataFileNames, FilenameVanadium=r'95895',OutputWorkspace='Data')
print "Load sample ", time.time() - start_time, "seconds"

# -----------------------------------------------------------------------------------------
# 1.1.2) Eventually remove bad pixels
# -----------------------------------------------------------------------------------------
# Apply mask to the detector - data
MaskDetectors(Workspace='Data',MaskedWorkspace='IN5_Mask')

# --------------------------------------------------------------------------
#  Load the  EC for 4A 
# (Neeed the vana for ELP)
# --------------------------------------------------------------------------
start_time = time.time()
Load(Filename = ECFileNames, FilenameVanadium=r'95895',OutputWorkspace='EC')
print "Load sample ", time.time() - start_time, "seconds"

# -----------------------------------------------------------------------------------------
# 1.1.2) Eventually remove bad pixels
# -----------------------------------------------------------------------------------------
# Apply mask to the detector - data
MaskDetectors(Workspace='Data',MaskedWorkspace='IN5_Mask')

# -----------------------------------------------------------------------------------------
# 1.3) Do sample - t*EC
# -----------------------------------------------------------------------------------------
MultiplyRange(InputWorkspace = 'EC',OutputWorkspace = 'tEC',Factor=transmission)
DataEC = Minus('Data','tEC')

# -----------------------------------------------------------------------------------------
#  1.4) Correct for self-shielding/self-absorption
#  
#     Duusn't wuuk !!
#
# -----------------------------------------------------------------------------------------
# Change WS to wavelenth
# Units available here: http://www.mantidproject.org/Unit_Factory
ConvertUnits(InputWorkspace='DataEC',OutputWorkspace='DataEC_lambda',Target='Wavelength',EMode='Direct')
# -----------------------------------------------------------------------------------------
# Load material properties in the workspace
# -----------------------------------------------------------------------------------------
# SetSampleMaterial started
# Found 1 types of atoms in "He"
# Sample number density = 0.0183556 atoms/Angstrom^3
# Cross sections for wavelength = 1.7982Angstroms
#     Coherent 1.34 barns
#     Incoherent 0 barns
#     Total 1.34 barns
#     Absorption 0.00747 barns
# -----------------------------------------------------------------------------------------
SetSampleMaterial(InputWorkspace = 'DataEC_lambda', ChemicalFormula='He')
# CylinderAbsorption(InputWorkspace='DataEC_lambda',OutputWorkspace='DataEC_lambda_abs',EMode='Direct', 
#                  CylinderSampleHeight='4.5',CylinderSampleRadius='0.6',NumberOfSlices='5',NumberOfAnnuli='2')

# CylinderAbsorption(InputWorkspace='DataEC_lambda',OutputWorkspace='DataEC_lambda_abs',EMode='Direct', 
# 				     AttenuationXSection =  0.00747, ScatteringXSection = 1.34, 
# 				     SampleNumberDensity = 0.0183555921468085, 
#                    CylinderSampleHeight='4.5',CylinderSampleRadius='0.6',NumberOfSlices='5',NumberOfAnnuli='2')

# ---------------------------------------------------------------------
#  3)  Normalize by the elastic peak of the vanadium          
# ---------------------------------------------------------------------
#Integrate Vanadium in time (1 bin in time only)
# ---------------------------------------------------------------------
Integration(InputWorkspace='Vana',OutputWorkspace='Vana_I',RangeLower=vanadiumFRangeLower,RangeUpper=vanadiumFRangeUpper)

# ---------------------------------------------------------------------
# Divide the data by the Vanadium integrated in time
# ---------------------------------------------------------------------
#   Divide(LHSWorkspace='DataEC_lambda_abs',RHSWorkspace='Vana_I',OutputWorkspace='DataECV',ClearRHSWorkspace='1')
Divide(LHSWorkspace='DataEC_lambda',RHSWorkspace='Vana_I',OutputWorkspace='DataECV',ClearRHSWorkspace='1')

# ---------------------------------------------------------------------
# Replace NaN and Infinity
# ---------------------------------------------------------------------
ReplaceSpecialValues(InputWorkspace='DataECV',OutputWorkspace='DataECVana',NaNValue='0',InfinityValue='0')

# ---------------------------------------------------------------------
#  4) Correction for detector wavelength-efficiency +
#    remove flat bkgd.
# ---------------------------------------------------------------------
# Convert from TOF to Energy
# ---------------------------------------------------------------------
ConvertUnits(InputWorkspace='DataECVana',OutputWorkspace='DataECVana_E',Target='DeltaE',EMode='Direct')

# ---------------------------------------------------------------------
# Detector efficiency: only runs for in4,5,6
# ---------------------------------------------------------------------
DetectorEfficiencyCorUser(InputWorkspace='DataECVana_E',OutputWorkspace='DataECVana_E_eff')

# ---------------------------------------------------------------------
# Is missing or could replace4 the above
# ---------------------------------------------------------------------
# He3TubeEfficiency
# DetectorEfficiencyCor

# ---------------------------------------------------------------------
# Rebin in energy
# ---------------------------------------------------------------------
Rebin(InputWorkspace='DataECVana_E_eff',OutputWorkspace='DataECVana_Rebin',Params=rebiningInEnergy,PreserveEvents='0')

# ---------------------------------------------------------------------
# SofQW
# ---------------------------------------------------------------------
start_time = time.time()
SofQW3(InputWorkspace='DataECVana_Rebin',OutputWorkspace='Sqw',QAxisBinning=rebiningInQ,EMode='Direct')
print " SofQW3: ", time.time() - start_time, "seconds"

# ---------------------------------------------------------------------
#   Intensity corrections
#   Performs ki / kf multiplication, in order to transform differential 
#   scattering cross section into dynamic structure factor. 
# ---------------------------------------------------------------------
CorrectKiKf(InputWorkspace='Sqw',OutputWorkspace='Sqw_KiKf')

# ---------------------------------------------------------------------
# Get axes in the usual order, Q is x axis, En is y axis
# ---------------------------------------------------------------------
Transpose(InputWorkspace='Sqw_KiKf',OutputWorkspace='Sqw_KiKf_T')

print " -------------------------------------------"
print "Total time spent = ",time.time() - t0," sec."
print " -------------------------------------------"


# Generate automatically the python script corresopnding to a given output workspace
# Same as history in graphic mode
GeneratePythonScript(InputWorkspace='Sqw_KiKf', 
                     Filename='/home/tofhr/ollivier/utils/Mantid/He4/generated_he_4A.py')
```

## Example script for IN6

**To Do: Test these and tidy them up**

Data - [IN6](https://www.ill.eu/fileadmin/users_files/img/instruments_and_support/support_facilities/computing_for_science/Computing_for_Science/Data_analysis/IN6_Script_Data.zip)

```python
#!/usr/bin/python

#
# IN6
# 
# From raw data to SofQw
#
# Open MantidPlot and launch the IPython console
#
# Add directory to the list (you can add as many as you want)
#
# If needed:
# from mantid import config 
# config.appendDataSearchDir('/usr/illdata/121/in5') 


# from mantid.simpleapi import *


##########################################
# Only edit this bit!

dataFolder = '/home/tofhr/lambda/MANTID/IN6/3rd_exp'
dataFileNames = ['164198','164199','164200']
mergedWorkspaceName = 'data_merged'



vanaFileNames = ['164192','164193','164194']
vanaMergedWorkspaceName = 'vana_merged'

# range in TOF
vanadiumFRangeLower=4000
vanadiumFRangeUpper=5000

spectraListToMask = [1,2,3,4,5,6,11,14,30,69,90,93,95,97,175,184,190,215,216,217,251,252,253,255,289,317,335,337]

transmission  =  0.95  # Sample transmission
rebiningInEnergy = '-50,0.1,3' # from, step, to
rebiningInQ = '0,0.04,30' # from, step, to



##########################################
# 1) Load Sample

for file in dataFileNames:
    fullPath = os.path.join(dataFolder,file+'.nxs')
    Load(Filename=fullPath,OutputWorkspace=file)

# Merge runs
if len(dataFileNames) > 1 :
    fileNamesToMerge = ','.join(map(str,dataFileNames))
    MergeRuns(InputWorkspaces=fileNamesToMerge,OutputWorkspace=mergedWorkspaceName)


# 1.1.2) Eventually remove spectra
if spectraListToMask is not None:
    MaskDetectors(Workspace=mergedWorkspaceName,SpectraList=spectraListToMask)

#1.3) Do sample - t*EC
MultiplyRange(InputWorkspace=mergedWorkspaceName,OutputWorkspace='Data_t',Factor=transmission)

# ; ---------------------------------------------------------------------
# ;  1.4) Correct for self-shielding/self-absorption

# Change WS to wavelenth
# Units available here: http://www.mantidproject.org/Unit_Factory

ConvertUnits(InputWorkspace='Data_t',OutputWorkspace='Data_t_lambda',Target='Wavelength',EMode='Direct')

# 1. Set sample Material
# ChemicalFormula or AtomicNumber must be given. 
# see: http://www.mantidproject.org/SetSampleMaterial
# SetSampleMaterial : [ChemicalFormula],[AtomicNumber],[MassNumber],[UnitCellVolume],
#                     [ZParameter],[AttenuationXSection],[ScatteringXSection], [SampleNumberDensity])

# Sample contents:

# DOES NOT WORK!
# SetSampleMaterial(InputWorkspace = 'Data_t_lambda', AtomicNumber=393.91, UnitCellVolume=196.4, ZParameter=1 )
SetSampleMaterial(InputWorkspace = 'Data_t_lambda', ChemicalFormula='Mg-Cu3-O6-Cl2-D6' , UnitCellVolume=196.4, ZParameter=1 )

# Absorption Correction:
# See: http://www.mantidproject.org/AbsorptionCorrection
# if known shape use:
#   CylinderAbsorption
#   FlatPlateAbsorption
#   SphericalAbsorption
# else use:
#   AbsorptionCorrection with CreateSampleShape before
# 

## Attention defaults for the slices and annuli are both 1.  
CylinderAbsorption(InputWorkspace='Data_t_lambda',OutputWorkspace='Data_t_lambda_abs',EMode='Direct', CylinderSampleHeight='5',CylinderSampleRadius='0.2',NumberOfSlices='5',NumberOfAnnuli='2')

# ;
# ;  2)          Vanadium 
# ;
# ; ---------------------------------------------------------------------
# ; 2.1) load vana
# ; ---------------------------------------------------------------------

# Load Vanadium

for file in vanaFileNames:
    fullPath = os.path.join(dataFolder,file+'.nxs')
    Load(Filename=fullPath,OutputWorkspace=file)

# Merge runs
if len(vanaFileNames) > 1 :
    fileNamesToMerge = ','.join(map(str,vanaFileNames))
    MergeRuns(InputWorkspaces=fileNamesToMerge,OutputWorkspace=vanaMergedWorkspaceName)


# ; ---------------------------------------------------------------------
# ; 2.2) Eventually remove bad spectra
# ; ---------------------------------------------------------------------

# Apply mask to the detector - data
if spectraListToMask is not None:
    MaskDetectors(Workspace=vanaMergedWorkspaceName,SpectraList=spectraListToMask)


# ; ---------------------------------------------------------------------
# ; 2.5) Do vanadium - EC        
# ; ---------------------------------------------------------------------
MultiplyRange(InputWorkspace=vanaMergedWorkspaceName,OutputWorkspace='Vanadium_t',Factor=transmission)

# ; ---------------------------------------------------------------------
# ;  2.6) Correct for self-shielding/self-absorption
# ;  (VF. Sears like) for vanadium
# ;

ConvertUnits(InputWorkspace='Vanadium_t',OutputWorkspace='Vanadium_t_lambda',Target='Wavelength',EMode='Direct')
SetSampleMaterial(InputWorkspace = 'Vanadium_t_lambda', ChemicalFormula='Mg-Cu3-O6-Cl2-D6' , UnitCellVolume=196.4, ZParameter=1 )
CylinderAbsorption(InputWorkspace='Vanadium_t_lambda',OutputWorkspace='Vanadium_t_lambda_abs',EMode='Direct', CylinderSampleHeight='5',CylinderSampleRadius='0.2',NumberOfSlices='5',NumberOfAnnuli='2')


# ; ---------------------------------------------------------------------
# ;
# ; 3)  Normalize by the elastic peak of the vanadium          
# ;

#Integrate Vanadium in time (1 bin in time only)
Integration(InputWorkspace='Vanadium_t',OutputWorkspace='Vanadium_I',RangeLower=vanadiumFRangeLower,RangeUpper=vanadiumFRangeUpper)
# Divide the data by the Vanadium integrated in time
Divide(LHSWorkspace='Data_t',RHSWorkspace='Vanadium_I',OutputWorkspace='Division',ClearRHSWorkspace='1')
# Replace NaN
ReplaceSpecialValues(InputWorkspace='Division',OutputWorkspace='Data_c',NaNValue='0',InfinityValue='0')



# ; ---------------------------------------------------------------------
# ;
# ; 4) Correction for detector wavelength-efficiency +
# ;    remove flat bkgd.

# Convert from TOF to Energy
ConvertUnits(InputWorkspace='Data_c',OutputWorkspace='Data_c_DeltaE',Target='DeltaE',EMode='Direct')
# Detctor efficiency: only runs for in4,5,6
DetectorEfficiencyCorUser(InputWorkspace='Data_c_DeltaE',OutputWorkspace='Data_c_DeltaE_effc')

# Optionally this should also be tried
# He3TubeEfficiency
# DetectorEfficiencyCor

# Rebin in energy
Rebin(InputWorkspace='Data_c_DeltaE_effc',OutputWorkspace='Data_DeltaE_Rebin',Params=rebiningInEnergy,PreserveEvents='0')
# SofQW
SofQW3(InputWorkspace='Data_DeltaE_Rebin',OutputWorkspace='Data_DeltaE_SofQW',QAxisBinning=rebiningInQ,EMode='Direct')
#
CorrectKiKf(InputWorkspace='Data_DeltaE_SofQW',OutputWorkspace='Data_DeltaE_KiKf')

# Those are optional!
#
# Transpose(InputWorkspace='Data_DeltaE_KiKf',OutputWorkspace='Data_DeltaE_KiKf_T')
#
# Logarithm(InputWorkspace='Data_DeltaE_KiKf_T',OutputWorkspace='Data_DeltaE_KiKf_T_log')
#
Logarithm(InputWorkspace='Data_DeltaE_KiKf',OutputWorkspace='Data_DeltaE_KiKf_log')
```

