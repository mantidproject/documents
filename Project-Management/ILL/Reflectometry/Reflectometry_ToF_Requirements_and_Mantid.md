# Reflectometry (ToF) at ILL Using Mantid - Initial Requirements Analysis

## Generic Reduction Procedure

This is based on the [COSMOS Procedure document](COSMOS Procedure.pdf) Anything in brackets refers 

**&#10004;** Indicates something that Mantid should generally be able to do, **&#10007;** something it can not, and **?** for unknown.

#### 1 Read Input:
Requirements:
* User input: Runnumbers (REF, DB, WATER, INST BACK) **&#10004;**
* Metadata: slits, detector angle, sample angle, MONITOR, TIME ... **&#10004;**
* User input data: foreground range, background range, wavelength range, grouping, **&#10004;**
* Detector: 2D, line, 1D **&#10004;**

** Currently Mantid will load data for old D17 data only, in both ToF and non-ToF modes. In newer data some NeXus entires are moved/missing**

To implement:
* Add Figaro instrument definition
* Check D17 instrument definition
* Verify and update `LoadILLReflectometry`
 * Check how ToF axis should be determined for newer data sets
 * Any missing metadata that needs to be loaded

#### 2 Determine Measurement Type

Requirements:
* A: ToF (Polarised or Unpolarised) **&#10004;**
* (B: Monochromatic (Polarised or Unpolarised))

To implement:
* The measurement type should be determined from the NeXus file, by the loader

#### 3 Kinetic / Streaming

Requirements:
* Determine if kinetic / streaming

To implement:
* Determined by loader?

#### 4 Axes

Requirements:
* Determine XYZ coordinate of axis **&#10004;**
* If detector XY: Integrate loose collimation direction **?**
* (If monochromatic: determine scan axis, stack data on scan axis direction)

#### 5 Sort or group measurements to measurement type

* Different measurements can be stored in 5th dimension
* 1: x-axis, 2: y-axis, 3: intensity, 4: polarization, 5: time/streaming/temperature/fields/etc...
* (If Monochromatic: sort scan axis, sort polarizations, sort measurements in sequence)
* If TOF: sort polarizations, sort angles, sort measurements in sequence
* If kinetic: loop through slices
* If streaming: sort cyclic data and average similar input

**The basic operations should be available in Mantid, and these can be implemented in the workflow algorithm. Will need to understand what options are required.**

To implement:
* Sort/Group measurements on a given parameter

#### 6 Errors

Requirements:
* Calculate errors and propagate appropriately through following steps **&#10004;**

**Mantid should always do this**

#### 7 Determine foreground (ROI) and background (back)

Requirements:
* If no DB: DB=monitor OR DB=1
* Here a binning can take place, but that requires calculating lambda, theta and the resolutions before.

#### 8 Normalization:

Requirements:
* slits **~**
* water **~**
* monitor/time **&#10004;**

To implement:
* Slit and water normalisation. Could just be done using standard workspace arithmetic, divide/subtract?

#### 9 Background:

Requirements:
* Subtract instrument background from REF and DB, subtract background from REF and DB (averaged or fitted) **&#10004;**

To implement:
* Any different methods for determining background for reflectometry at the ILL

#### 10 Average data at similar XY coordinates:

Requirements:
* (IF MONO: average same theta/2theta values)
* IF TOF: probably no further averaging

Nothing to implement for now.

#### 11 Gravity

Requirements:
* Gravity correction for horizontal reflectometer

**Currently used for SANS in Mantid, no user algorithm but class [`GravitySANSHelper`](https://github.com/mantidproject/mantid/blob/master/Framework/Algorithms/src/GravitySANSHelper.cpp) exists to perform calculations.**

To implement:
* Gravity correction in reflectometry workflow
 * Possible to turn `GravitySANSHelper` into a new algorithm

#### 12 Calculate missing axes

Requirements:
* theta, 2theta, lambda
* Reflection UP or DOWN in horizontal reflectometer
* Coherent or incoherent analysis

**Can the conversions be done using [`ConvertUnits`](http://docs.mantidproject.org/nightly/algorithms/ConvertUnits-v1.html) or [`ConvertAxisByFormula`](http://docs.mantidproject.org/nightly/algorithms/ConvertAxisByFormula-v1.html)?**

#### 13 Calculate angular width on detector of REF and DB => sample waviness for coherent

?

#### 14 IF DB supplied: Integrate DB foreground
IF TOF: => 1D DB(lambda)
IF MONO: => 1D DB(scan axis)

#### 15 IF POL: Correct 1D DB for polarization efficiency

#### 16 Calculate 1D reflectivity:
CASE: incoherent
Integrate at constant lambda over 2theta => 1D REF
Divide 1D REF by 1D DB => 1D REF/DB + E
CASE: coherent
Divide 2D REF by 1D DB column wise
Regroup data within new wavelength limits onto a given 2theta line
CASE: bent sample
CASE: divergent beam
=> 1D REF/DB + E

#### 17 IF TOF POL: loop to get all the polarizations to correct for efficiencies the 1D REF/DB as a function of
lambda
IF POL MONO: loop to get all polarizations to correct for polarization efficiency at fixed lambda


#### 18 Calculate resolutions in theta, lambda
CASE: incoherent
CASE: coherent

#### 19 Q

Requirements:
* Calculate Q

**Mantid has algorithms [`ConvertUnits`](http://docs.mantidproject.org/nightly/algorithms/ConvertUnits-v1.html) and [`ConvertToReflectometryQ`](http://docs.mantidproject.org/nightly/algorithms/ConvertToReflectometryQ-v1.html)**

#### 20 Group to a fraction of the Q resolution
NOTE: for the incoherent method it is possible here to use 1D REF(rebinned)/1D DB (rebinned)

#### 21 Calculate 2D reflectivity in requested coordinates: QX/QZ, pi/pf/ theta/2theta
Divide 2D REF by 1D DB column wise

#### 22 Polarization

Requirement:
* Perform polarization efficiency correction on all spin channels column wise

**Potential candidate is the Mantid algorithm [`PolarizationCorrection`](http://docs.mantidproject.org/nightly/algorithms/PolarizationCorrection-v1.html)**

#### 23 Update storage with direct beam

?

#### 24 IF kinetic: loop over slices

?

#### 25 IF multiple datasets: loop over 5 th dimension

?

#### 26 Perform final normalization corrections

What are the final normalization corrections?

#### 27 Join data corresponding to 1 measurement

?

#### 28 Saving

Requirements:
* Store 1D and 2D outputs in readable format with metadata

**Mantid can save a range of file types, e.g. [`SaveNexus`](http://docs.mantidproject.org/nightly/algorithms/SaveNexus-v1.html)**

#### Workflow algorithms

**[`ReflectometryReductionOne`](http://docs.mantidproject.org/nightly/algorithms/ReflectometryReductionOne-v1.html)** - used at ISIS and elsewhere???

#### GUI for reduction

We are planning something along the lines of the COSMOS interface for the ILL ToF GUI. This will likely be based on the generic `DataProcessorWidget` in Mantid, as used for reflectometry at ISIS. This might be a good fit for ILL reflectometry reduction too.

[ISIS Reflectometry Interface](http://docs.mantidproject.org/nightly/interfaces/ISIS_Reflectometry.html)


