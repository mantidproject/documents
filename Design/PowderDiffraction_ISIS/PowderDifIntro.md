
Introduction
============

Purpose of this Document: This document describes the detailed design of the new Powder Differaction in the MantidPlot application.
 
Objectives
===========

As we are learning and not fully aware of the objectives that need to be achieved. The describtion will include intial investigation 
that is being carried out, what files, algorithm, workspaces are being used in order to work the old Powder Diffraction by Aziz. 

Detailed Objectives
===================

Basic Objectives
----------------

*	Integrate Powder Diffraction algorithm in Mantid
*	Being able to drive effective codes from previously Powder Diffractions code which have been done by different departments 	
*	Being able to satisfy the demands of the scientists 
  

Previous PowderDif Algorithms
=============================

Mantid Algorithms Used
----------------------

These algorithms were used during the process (in chronological order) of running the previous Powder Diffraction Plug-in 
to Mantid by Aziz. (By exposing the repository to python script in Mantid.property). The new Powder Diffraction could possibly
still be using the following algorithms too:

| Mantid Algorithms               | Summary                                                       | 
| :-----------------------------: | :-----------------------------------------------------------: | 
| LoadRaw v3                      | Loads the raw data.                                           | 
| MaskBins v1 x5                  | Bins falling within the range given are masked .              | 
| CreateSingleValuedWorkspace v1  | To do binary operations between workspace and a single value. | 
| Divide v1                       | Will divide the data values and calculate error values.       | 
| Integration v1                  | Sums the data values that are inputted.                       | 
| MaskDetectorsIf v1              | Adjust the selected field for a CalFile depending on input.   | 
| SolidAngle v1                   | Calculates the solid angle in steradians of the detectors.    | 
| CreateSingleValuedWorkspace v1  | To do binary operations between workspace and a single value. | 
| Multiply v1                     | Will multiply the data values and calculate error values.     | 
| Divide v1                       | Will divide the data values and calculate error values.       | 
| ConvertUnits v1                 | Perform a unit change on the X values of a workspace.         | 
| Integration v1                  | Sums the data values that are inputted.                       | 
| Multiply v1                     | Will multiply the data values and calculate error values.     | 
| CreateSingleValuedWorkspace v1  | To do binary operations between workspace and a single value. | 
| Divide v1                       | Will divide the data values and calculate error values.       | 
| LoadNexusProcessed v1 x3        | Loads the given nexus processed file contain matid workspace. | 
| MaskBins v1 x5                  | Bins falling within the range given are masked.               | 
| CreateSingleValuedWorkspace v1  | To do binary operations between workspace and a single value. | 
| Divide v1                       | Will divide the data values and calculate error values.       | 
| Integration v1                  | Sums the data values that are inputted.                       | 
| MaskDetectorsIf v1              | Adjust the selected field for a CalFile depending on input.   | 
| AlignDetectors v1               | Performs a unit change from TOP to DSpacing, correcting the   | 
|                                 | x Values to account for small errors in detector's positions. | 
| Divide v1                       | Will divide the data values and calculate error values.       | 
| CreateSingleValuedWorkspace v1  | To do binary operations between workspace and a single value. | 
| Multiply v1                     | Will multiply the data values and calculate error values.     | 
| DiffractionFocussing v2         | To Focus powder diffraction data in a number of histograms    | 
|                                 | according to a grouping scheme defined in a CalFile.          | 
| CropWorkspace v1 x3             | Extracts a `block` from WS and place it in a new WS.          | 
| RebinToWorkspace v1             | Alters binning so that all its spectra match of 1st spectrum  | 
|                                 | , the algorithm builds parameter list passed to the Rebin v1. | 
| Divide v1                       | Will divide the data values and calculate error values.       | 
| RebinToWorkspace v1             | Alters binning so that all its spectra match of 1st spectrum. | 
| Divide v1                       | Will divide the data values and calculate error values.       | 
| RebinToWorkspace v1             | Alters binning so that all its spectra match of 1st spectrum. | 
| Divide v1                       | Will divide the data values and calculate error values.       | 
| Rebin v1 x3                     | Rebin data with new X bin boundaries.                         |
| ConvertUnits v1                 | Perform a unit change on the X values of a workspace.         | 
| ReplaceSpecialValues v1 x2      | Replaces instances of NaN and infinity or abs val in the WS   | 
|                                 | with user defined numbers; if not provided it will not check  | 
| ConvertUnits v1                 | Perform a unit change on the X values of a workspace.         | 
| ReplaceSpecialValues v1 x2      | Replaces instances of NaN and infinity in the workspace.      | 
| ConvertUnits v1                 | Perform a unit change on the X values of a workspace.         | 
| ReplaceSpecialValues v1 x2      | Replaces instances of NaN and infinity in the workspace.      | 
| GroupWorkspaces v1              | Takes workspaces as input and groups similar WS together.     | 
| SaveGSS v1 x4                   | Saves a fucsed data set into a three column GSAS format.      | 
| SaveNexusProcessed v1           | Writes given Mantid WS to Nexus file, can also be invoked by  | 
|                                 | SaveNexus too.                                                | 
| SaveFocusedXYE v1 x6            | Saves a focused data set (usually output of a diffraction     | 
|                                 | focusing routine) in to a three column format contian X_i,    | 
|                                 | Y_i and E_i.                                                  | 


Files that are being used
-------------------------
Input Files
------------
These are the files that are essentially required and are utilised in order to run the cry_example.py and the system test file

| Input Files                                       |
| :-----------------------------------------------: |
| hrp39191.raw                                      |
| hrp39187.raw                                      |
| hrp43022.raw                                      |
| hrpd/test/GrpOff/hrpd_new_072_01.cal              |
| hrpd/test/GrpOff/hrpd_new_072_01_corr.cal         |
| hrpd/test/cycle_09_2/Calibration/van_s1_old-0.nxs |
| hrpd/test/cycle_09_2/Calibration/van_s1_old-1.nxs |
| hrpd/test/cycle_09_2/Calibration/van_s1_old-2.nxs |
| hrpd/test/cycle_09_2/tester/mtd.pref              |



Output Files
------------
These are the files that are generated when cry_example.py file is executed

| Output Files                   | 
| :----------------------------: | 
| hrpd/test/cycle_09_2/Calibration/hrpd_new_072_01_corr.cal    |
| hrpd/test/cycle_09_2/tester/hrp43022_s1_old.gss              |
| hrpd/test/cycle_09_2/tester/hrp43022_s1_old.nxs              |
| hrpd/test/cycle_09_2/tester/hrp43022_s1_old_b1_D.dat         |
| hrpd/test/cycle_09_2/tester/hrp43022_s1_old_b1_TOF.dat       |
| hrpd/test/cycle_09_2/tester/hrp43022_s1_old_b2_D.dat         |
| hrpd/test/cycle_09_2/tester/hrp43022_s1_old_b2_TOF.dat       |
| hrpd/test/cycle_09_2/tester/hrp43022_s1_old_b3_D.dat         |
| hrpd/test/cycle_09_2/tester/hrp43022_s1_old_b3_TOF.dat       |
| hrpd/test/cycle_09_2/hrpd_new_072_01_corr.cal                |



MantidPlot Output Workspaces
-----------------------
These are the workspaces produced in MantidPlot by running the cry_example.py file

| Output Workspace               | 
| :----------------------------: | 
| ResultD-1: MatrixWorkspace     | 
| ResultD-2: MatrixWorkspace     | 
| ResultD-3: MatrixWorkspace     | 
| ResultTOFgrp: TableWorkspace   | 
| totuamps: MatrixWorkspace      |


ResultTOFgrp found in the MantidPlot output workspace and file found in the following directory
hrpd/test/cycle_09_2/tester/hrp43022_s1_old.nxs are containing the same data.

Variables from mtd.pref file
============================

Inside the `cry_ini.py` file, most of the variables from `mtd.pref` have been pre-defined. The variables
that have been pre-defined, they are being updated from the `mtd.pref` file and imported in to the “cry_ini.py”
file inside `Def __init__`.

The initialise function inside the `cry_ini.py` file seems to be updating values from `mtd.pref` with special
function; ```self.OffDir = self.updatePrefVal("", self.OffDir)```, this would seem to update the .py file with
provided data.

However there are some variables which have not been assigned previously and they are being defined by using the
 following function.
```self.OffFile = self.read_prefline("Offsets")```, these variables are compulsory, unless Powder Diffraction
script will not function.

Backed up by an important comment found in `cry_ini.py` which should be considered:
-	# Read preference file: default, read_prefline-label ALWAYS REQUIRED in pref-file
-	# Read preference file: optional params read with updatePrefVal
```
class Files:
    def __init__(self, instr, RawDir="", Analysisdir="", UnitTest=False, debugMode=False,
    forceRootDirFromScripts=True, inputInstDir=''):
```

( # Read preference file: optional params read with updatePrefVal )

| All variables defined in "cry_ini.py" | Equals "="                                 | Equals & Found in mtd.pref | 
| :-----------------------------------: | :----------------------------------------: | :------------------------: | 
| RawDir                                | If self.RawDir = " ": Self. RawDir         | Null                |
|                                       | = join(r'\\isis\inst$\ndx%s' % self.instr, |                     |
|                                       | 'instrument', 'data', Cycle)               |                     |
| VanDir                                | = self.RawDir                              | Null                |
| VEmptyDir                             | = self.RawDir                              | Null                |
| SEmptyDir                             | = self.RawDir                              | Null                |
| CorrVanDir                            | = join(self.Analysisdir, Cycle,            | Null                |
| CorrVanDir                            | "Calibration")                             | Null                |
| GrpDir                                | = join(self.Analysisdir, "GrpOff")         | Null                |
| VanFile                               | = []                                       |                     |
| VEmptyFile                            | = []                                       |                     |
| SEmptyFile                            | = []                                       |                     |
| AutoVan                               | Default: False = ""                        |                     |
| CorrVanFile                           | if self.CorrVanFile =="" : AutoVan = True  | van_s1_old          |
|                                       | if AutoVan:                                |                     |
|                                       | self.CorrVanFile = "van_" +                |                     |
|                                       | self.VrunnoList + "_" + self.VErunnoList   |                     |
| SacEffFile                            | if AutoVan:True                            |                     |
|                                       | self.SacEffFile="corr_" + self.VrunnoList  |                     |
|                                       | else:                                      |                     |
|                                       | self.SacEffFile = self.updatePrefVal(      |                     |
|                                       | "SacEffFile", self.SacEffFile)             |                     |
| ExistV                                | = "no"                                     |                     |
| VGrpfocus                             | = "van"                                    |                     |
| Path2DatGrpFile                       | = ""                                       | 2                   |
| VHeight                               | = "2"                                      | 0.4                 |
| VRadius                               | = "0.4"                                    | 5.1                 |
| VAttenuationXSection                  | = "5.1"                                    | 5.08                |
| VScatteringXSection                   | = "5.08"                                   | 0.072               |
| VanaNumberDensity                     | = "0.072"                                  | 10                  |
| VNumberOfSlices                       | = "10"                                     | 10                  |
| VNumberOfAnnuli                       | = "10"                                     | 100                 |
| VNumberOfWavelengthPoints             | = "100"                                    | Normal              |
| VExpMethod                            | = "Normal"                                 | 100                 |
| VanSmooth                             | = "100"                                    | 60                  |
| VanSplineCoef                         | = "15"                                     | 15                  |
| VanPeakRemove                         | = "interpol"                               | interpol            |
| VanPeakFile                           | = 'VanaPeaks.dat'                          | VanaPeaks.dat       |
| VanPeakList                           | = []                                       |                     |
| VanPeakWdt                            | = [20, 50, 0]                              |                     |
| VanPeakTol                            | = [4, 4, 0]                                |                     |
| CorrectSampleAbs                      | = "no"                                     | no                  |
| SampleAbsCorrected                    | = False                                    |                     |
| SampleHeight                          | = "0.0"                                    | 0.0                 |
| SampleRadius                          | = "0.0"                                    | 0.0                 |
| SampleAttenuationXSection             | = "0.0"                                    | 0.0                 |
| SampleScatteringXSection              | = "0.0"                                    | 0.0                 |
| SampleNumberDensity                   | = "1"                                      | 1                   |
| SampleNumberOfSlices                  | = "10"                                     | 10                  |
| SampleNumberOfAnnuli                  | = "10"                                     | 10                  |
| SampleNumberOfWavelengthPoints        | = "100"                                    | 100                 |
| SampleExpMethod                       | = "Normal"                                 | Normal              |
| LowerLambda                           | = 1.4                                      | 1.4                 |
| UpperLambda                           | = 3.0                                      | 3                   |
| OutSuf                                | = ""                                       | "Output" = s1_old   |
| XYEDspc                               | = "yes"                                    |                     |
| XYEtof                                | = "yes"                                    |                     |
| GSS                                   | = "yes"                                    |                     |
| Nex                                   | = "yes"                                    |                     |
| NBank                                 | = 3                                        | 3                   |
| bankList                              | = [1, 2, 3]                                | 1-3                 |
| Drange                                | = []                                       |                     |

These variables listed below in the table are read directly from the `mtd.pref` file in
``` def initialize(self, Cycle, user, prefFile="", prefDir="", Verbose=False)``` function.
Example of how its defined in `cry_ini.py`
- ```self.OffFile = self.read_prefline( "Offsets" )```

( # Read preference file: default, read_prefline-label ALWAYS REQUIRED in pref-file )

| All variables defined | Variables name | Equals = in mtd.pref       |                          |
| in cry_ini.py         | in mtd.pref    |                            |                          |
| def initialize()      |                |                            |                          |
| :-------------------: | :------------: | :--------------------------| :-----------------------:|
| OffFile               | Offsets        | hrpd_new_072_01_corr.cal   |                          |
| GrpFile               | Grouping       | hrpd_new_072_01_corr.cal   |                          |
| VrunnoList            | Vanadium       | 39191                      |                          |
| VErunnoList           | V-Empty        | 39187                      |                          |
| SErunnoList           | S-Empty        | 0                          |                          |
| ExistV                | ExistingV      | yes                        |                          |
| XYEtof                | XYE-TOF        | yes                        |                          |
| XYEdspc               | XYE-D          | yes                        |                          |
| GSS                   | GSS            | yes                        |                          |
| Nex                   | Nexus          | yes                        |                          |
| saveXYEtof (bool)     |                |                            | XYEtof == "yes"          |
| saveXYEd (bool)       |                |                            | XYEdspc == "yes"         |
| Nbank                 | Nbank          | 3                          |                          |
| CropRange             | CropRange      | 0.05 0.95                  | = ("0.05 0.95", Nbank)   |
| Bining                | Bining         | 0.0001                     | = (0.0001, Nbank)        |
| bankList              | BankList       | 1-3                        | if (saveXYEtof ||        |
|                       |                |                            | saveXYEd){ bankList =    |
|                       |                |                            | cry_utils.get_lis        |


Prototype example usage
=======================

```python
import sys
#sys.path.append('...\GitHub\mantid\Code\Mantid\scripts\PowderISIS')

import cry_ini
import cry_focus

from mantid.simpleapi import config
config['datasearch.searcharchive'] = 'On'
print config['datasearch.searcharchive']
	
expt=cry_ini.Files("hrpd",Analysisdir='test')
#expt.RawDir="C:/AZIZWORK/BigData/HRPD/Bigg"
expt.initialize('cycle_09_2',user = 'tester',prefFile='mtd.pref')
expt.tell()
#------------------------------------
# 1) process single runs, given as 
#     a list of mubers OR ranges (raw):
# eg: "1000 1005 1250-1260" 
#    AND/OR process a range of runs merging data every n runs 
#    (checks for 0 uamps data)
# eg: "1300-1200-5"
# The two options can be used together
# 3) XOR: process several instermediate saves
# eg: s42356 1-3 5
#------------------------------------
#cry_focus.FocusAll(expt,"43022-43025 43028-43045-3")
cry_focus.focus_all(expt, "43022")
# Optional : 
# Skip Normalization & user-defined scale, e.g:
#cry_focus.FocusAll(expt,"1000 1005 1250-1260" , scale=100, Norm=False)
```

