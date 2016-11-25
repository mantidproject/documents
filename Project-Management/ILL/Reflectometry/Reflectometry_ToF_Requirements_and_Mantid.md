# Reflectometry (ToF) at ILL Using Mantid - Initial Requirements Analysis

## Generic Reduction Procedure

This is based on the [COSMOS Procedure document](COSMOS Procedure.pdf). Anything in brackets refers to monochromatic mode, not to be addressed initially.

**&#10004;** Indicates something that Mantid should generally be able to do, **~** something that might need adapting, **&#10007;** something it can not, and **?** for unknown.

### Read Input
Requirements:
* User input: Runnumbers (REF, DB, WATER, INST BACK) **&#10004;**
* Metadata: slits, detector angle, sample angle, MONITOR, TIME ... **&#10004;**
* User input data: foreground range, background range, wavelength range, grouping **&#10004;**
* Detector: 2D, line, 1D **&#10004;**

**Currently Mantid will load data for old D17 data only, in both ToF and non-ToF modes. In newer data some NeXus entires are moved/missing.**

To implement:
* Add Figaro instrument definition
* Check D17 instrument definition
* Verify and update `LoadILLReflectometry`
 * Check how ToF axis should be determined for newer data sets
 * Any missing metadata that needs to be loaded

### Determine Measurement Type

Requirements:
* A: ToF (Polarised or Unpolarised) **~**
* (B: Monochromatic (Polarised or Unpolarised))
* Determine if kinetic / streaming **~**

To implement:
* The measurement type should be determined from the NeXus file, by the loader
* Need to load the 4 polarisation states, from 4 numours, into one workspace for D17
* For kinetic files need to load the extra dimension into the files

### Axes

Requirements:
* Determine XYZ coordinate of axis **&#10004;**
* If detector XY: Integrate loose collimation direction **~**
* (If monochromatic: determine scan axis, stack data on scan axis direction)

To implement:
* This should also be dealt with by the loader
* The loose collimation direction needs to be implemented for cases where the NeXus file has the full 2D detector data

### Sort or group measurements to measurement type

* Different measurements can be stored in 5th dimension
* 1: x-axis, 2: y-axis, 3: intensity, 4: polarization, 5: time/streaming/temperature/fields/etc...
* (If Monochromatic: sort scan axis, sort polarizations, sort measurements in sequence)
* If TOF: sort polarizations, sort angles, sort measurements in sequence
* If kinetic: loop through slices
* If streaming: sort cyclic data and average similar input

**The basic operations should be available in Mantid, and these can be implemented in the workflow algorithm. Will need to understand what options are required.**

To implement:
* Sort/Group measurements on a given parameter

### Errors

Requirements:
* Calculate errors and propagate appropriately through following steps **&#10004;**

**Mantid should always do this.**

### Find Regions of Interest

Requirements:
* Find region of interest peak for sample run in reflected and direct beam, and for background **~**
* If no Direct Beam: Direct Beam=monitor OR Direct Beam=1 **~**
* Here a binning can take place, but that requires calculating lambda, theta and the resolutions before **~**

**Mantid has a number of fitting and peaking finding routines.**

To implement:
* Determine what fitting/peaking finding needs to be used in Mantid

### Normalization

Requirements:
* slits **~**
* water **~**
* monitor/time **&#10004;**

To implement:
* Slit normalisation - multiply by factor
* Water normalisation should be possible just using divide
* Normalisation by monitor time can be done with [`NormaliseToMonitor`](http://docs.mantidproject.org/nightly/algorithms/NormaliseToMonitor-v1.html) or just using `Integration` and `Divide`

### Background

Requirements:
* Subtract instrument background from reflected and direct beam, subtract background from reflected and direct beam (averaged or fitted) **&#10004;**

**Mantid has some rountines for background fitting, e.g. [`CalculateFlatBackground`](http://docs.mantidproject.org/nightly/algorithms/CalculateFlatBackground-v1.html).**

To implement:
* Workspace arithmetic if just subtracting backgrounds
* Need to work out if we can use existing routines for fitting background, or need to implement new ones

### Average data at similar XY coordinates

Requirements:
* (If monochromatic average same theta/2theta values)
* If TOF probably no further averaging

**Nothing to implement for now.**

### Gravity

Requirements:
* Gravity correction for horizontal reflectometer **&#10007;**

**Currently used for SANS in Mantid, no user algorithm but class [`GravitySANSHelper`](https://github.com/mantidproject/mantid/blob/master/Framework/Algorithms/src/GravitySANSHelper.cpp) exists. Reflectometry case is more complex. If this is used at ISIS some scripts may exist to do this.**

To implement:
* Gravity correction algorithm
 * Might be possible to use parts of `GravitySANSHelper` into a new algorithm

### Calculate missing axes

Requirements:
* theta, 2theta, lambda **?**
* Reflection UP or DOWN in horizontal reflectometer **?**
* Coherent or incoherent analysis **?**

**Can the conversions be done using [`ConvertUnits`](http://docs.mantidproject.org/nightly/algorithms/ConvertUnits-v1.html) or [`ConvertAxisByFormula`](http://docs.mantidproject.org/nightly/algorithms/ConvertAxisByFormula-v1.html)?**

### Calculate angular width

Requirements:
* Calculate angular width on detector of Reflected and Direct Beam => sample waviness for coherent **?**

To implement:
* This will be some work to implement - should be able to follow as it is done in Cosmos

### Polarisation correction

Requirements:
* If polarised Correct 1D DB for polarization efficiency **~**
* If polarised ToF loop to get all polarization efficiencies as a function of lambda **~**
* Perform polarization efficiency correction on all spin channels column wise **~**

**Mantid has a [`PolarizationCorrection`](http://docs.mantidproject.org/nightly/algorithms/PolarizationCorrection-v1.html) algorithm for reflectometry. Based on *Fredrikze, H, et al. 'Calibration of a polarized neutron reflectometer' Physica B 297 (2001)*, not *Wildes, Rev. Sci. Instrum., 70 (1999) 4241*.**

To implement:
* Determine if existing algorithm can be used or adapted

### Calculate 1D reflectivity

Requirements:
* Incoherent 
 * Integrate at constant lambda over 2theta => 1D REF **&#10004;**
 * Divide 1D REF by 1D DB => 1D REF/DB + E **&#10004;**
* Coherent
 * Divide 2D REF by 1D DB column wise **&#10004;**
 * Regroup data within new wavelength limits onto a given 2theta line **~**
* Bent sample
* Divergent beam
 * 1D REF/DB + E **&#10004;**

**These cover standard operations for workspaces in Mantid, and the grouping is mentioned under *Sort or group measurements to measurement type*.**

To implement:
* Implement options as part of workflow

### Calculate resolutions

Requirements:
* Theta, lambda
* Incoherent, Coherent

**The [`CalculateResolution`](http://docs.mantidproject.org/nightly/algorithms/CalculateResolution-v1.html) used for ISIS reflectometry should be able to calculate this.**

To implement:
* See if `CalculateResolution` algorithm works as desired
* Resolution for theta, lambda

### Q and Q binning

Requirements:
* Calculate Q **&#10004;**
* Group to a fraction of the Q resolution **&#10004;**

**Mantid has algorithms [`ConvertUnits`](http://docs.mantidproject.org/nightly/algorithms/ConvertUnits-v1.html) and [`ConvertToReflectometryQ`](http://docs.mantidproject.org/nightly/algorithms/ConvertToReflectometryQ-v1.html). For rebinning [`Rebin`](http://docs.mantidproject.org/nightly/algorithms/Rebin-v1.html) is normally used.**

### 2D Reflectivity

Requirements:
* Calculate 2D reflectivity in requested coordinates: 
 * Qx/Qy **&#10004;**
 * Pi/Pf **&#10004;**
 * theta/2theta **&#10007;**
* Divide 2D REF by 1D DB column wise

**Mantid has an algorithm for converting to (Qx, Qy), (Pi, Pf) and (Ki, Kf) - [`ConvertToReflectometryQ`](http://docs.mantidproject.org/nightly/algorithms/ConvertToReflectometryQ-v1.html).**

To implement:
* See if ConvertToReflectometryQ method can be used
* Similar methods for theta/2theta?

### Final normalisation corrections and join

Requirements:
* Normalise data so it can be joined **~**
* Join data corresponding to 1 measurement **&#10004;**

**Mantid has the [`Stitch1D`](http://docs.mantidproject.org/nightly/algorithms/Stitch1D-v3.html) - is this what is required?**

To implement:
* Determine required 
* See if `Stich1D` can be used for this

### Saving

Requirements:
* Store 1D and 2D outputs in readable format with metadata **~**

**Mantid can save a range of file types, e.g. [`SaveNexus`](http://docs.mantidproject.org/nightly/algorithms/SaveNexus-v1.html)**

To implement:
* Extra file types - most likely ASCII data in columns with headers for analysis programs

### Workflow algorithms

**[`ReflectometryReductionOne`](http://docs.mantidproject.org/nightly/algorithms/ReflectometryReductionOne-v1.html)** - used at ISIS

### GUI for reduction

We are planning something along the lines of the COSMOS interface for the ILL ToF GUI. This will likely be based on the generic `DataProcessorWidget` in Mantid, as used for reflectometry at ISIS. This might be a good fit for ILL reflectometry reduction too.

[ISIS Reflectometry Interface](http://docs.mantidproject.org/nightly/interfaces/ISIS_Reflectometry.html)


