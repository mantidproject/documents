Motivation
==========

The ISIS powder diffraction scientists have identified a problem with their powder diffraction reduction workflow. The workflow is as follows (algorithm names in brackets):

* calibration ([CrossCorrelate](https://docs.mantidproject.org/nightly/algorithms/CrossCorrelate.html), [GetDetectorOffsets](https://docs.mantidproject.org/nightly/algorithms/GetDetectorOffsets.html)). Various approaches available here as described in the Mantid [concept page](https://docs.mantidproject.org/nightly/concepts/calibration/PowderDiffractionCalibration.html). ISIS tend to use CrossCorrelate\GetDetectorOffsets which generates a "per detector" correction in the form of a peak offset. The peak offset can easily be converted into a DIFC diffractometer constant. An alternative is the PDCalibration algorithm that directly outputs DIFC as well as DIFA\TZERO
* convert data from TOF to d spacing ([AlignDetectors](https://docs.mantidproject.org/nightly/algorithms/AlignDetectors.html)). Uses the diffractometer constants generated in the calibration step
* focus ([DiffractionFocussing](https://docs.mantidproject.org/nightly/algorithms/DiffractionFocussing.html)). Focus the data for each bank of detectors according to grouping data in a .cal file
* convert data back to TOF ([ConvertUnits](https://docs.mantidproject.org/nightly/algorithms/ConvertUnits-v1.html))
* Save data to file for downstream processing ([SaveGSS](https://docs.mantidproject.org/nightly/algorithms/SaveGSS-v1.html))

I believe there is a similar workflow followed at SNS using the [AlignAndFocusPowder](https://docs.mantidproject.org/nightly/algorithms/AlignAndFocusPowder-v1.html) workflow algorithm. ISIS use some python scripts to chain together the different steps but it achieves a similar process to AlignAndFocusPowder

The problem is that the final ConvertUnits step to convert from d spacing to TOF doesn't use the diffractometer constants. Following the focussing the data isn't "per detector" any more but it should still be possible to use a "per bank" DIFC\DIFA\TZERO to convert the data back to TOF

There is also a more minor problem that the SaveGSS algorithm recalculates a per bank DIFC value and writes it into a header for each bank in the .gss file. This calculation also ignores the calibration output. It seems that GSAS isn't reading this header though so this problem just creates potential confusion for anyone reading the file rather than incorrect figures in GSAS.

Possible solutions
==================

We could create a "backwards" mode to the AlignDetectors algorithm that performs the d spacing to TOF unit conversion including the diffractometer constants. This would then be called instead of ConvertUnits near the end of the reduction workflow.

This still leaves the burden on the user\developer to remember to load the calibration data as an input parameter at two points in the workflow. Since this information has already been loaded once it seems like it should be stored in the workspace somewhere. Also the algorithm name "AlignDetectors" doesn't obviously suggest it does a unit conversion. 

So on balance we prefer to put the new functionality in the ConvertUnits algorithm which is a more obvious place.

Proposed Solution
=================

Modify ConvertUnits so it can incorporate diffractometer constants in its unit conversion from TOF to d spacing and vice versa.

Store the "per detector" diffractometer constants in the instrument parameter map once they are applied to a workspace. A similar approach is already used to store the efixed values for indirect instruments (see ConvertUnits::getDetectorValues). This would mean that if a workspace is saved to a Nexus file, the diffractometer constants would also be saved.

Create a new algorithm to load and store the diffractometer constants in the workspace called ApplyDiffCal. This would take one of three inputs:
* calibration file (.cal or hdf)
* a [calibration table workspace](https://docs.mantidproject.org/nightly/concepts/DiffractionCalibrationWorkspace.html)
* an offsets table workspace

When ConvertUnits does a conversion between TOF and d spacing check if the instrument map contains diffractometer constants. Use them if they're found. If none found use existing logic

For unit conversions applied to spectra with multiple detectors, just use average of diffractometer constants

Label the AlignDetectors algorithm as deprecated.

Add some way of viewing the diffractometer data that is stored in a workspace:
* Show the diffractometer constants in the "Show Detectors" screen?
* Perhaps provide an algorithm to output the data to a separate table workspace eg CreateDiffCal. Although I note this would make the list of xxxDiffCal algorithms even longer

Clear the diffractometer constants from the instrument parameter map if any of the detector positions in the workspace are modified (eg by running ApplyCalibration which applies an x,y,z offset to each detector). This provides a basic way of ensuring the diffractometer constants and the detector positions are in sync

With this solution, the existing file formats (.cal or hdf) are still an essential part of storing the calibration outside of a "signal workspace" so it can be reused. The calibration table workspace becomes a bit redundant but would leave it and any algorithms that use it or write to it in place for backwards compatibility.
