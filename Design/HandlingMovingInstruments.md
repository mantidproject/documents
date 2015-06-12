#Handling instruments with moving components#

##Introduction##

The purpose of this (use case) document is to form a top level discussion of handling of data coming off instruments with moving components. The initial version of this document includes outcomes from discussions from the development workshop 2015. 

Further this document has been updated with email contributions from Nick Draper (ND), Marina Ganeva (MG), Mark Koennecke (MK) and Mark Johnson (MJ) and Timothy Charlton (TC).

##Motivation##

Mantid can already handling instrument with moving components, to an extent, by associating the position of a component with a log entry. Specifically this is done in an Instrument Definition File (IDF) using the notation: 
```xml
<parameter name="x">
  <logfile id="trolley2_x_displacement" extract-single-value-as="position 1" />
</parameter>
```
This example reads: take the first value in the log-file `trolley2_x_displacement` and use this value to overwrite the `x` position of a component.

The current limitation of this approach is that only one position value is calculated from a log-file time series.  Hence, by default this approach will not handle the case where different data in a file are associated with different geometry orientations of the instrument. The later can be handed, post loading of data, by taking a workspace of data and split it up into a series of workspaces, where each such workspace only contains data with log-file values from one geometry orientation of the instrument (and where these new log-file values have been used to update the instrument geometry). 

Here report on moving instrument use cases and some high level suggestions for implementing such use cases. 

##Use cases##

Here is a breakdown of the use cases provided. Some use cases contain sub use cases, these are labelled with letters rather than numbers. 

###Use Case 1, Extending detector coverage###
A simplified instrument here could be considered to be a pack of PSD tubes on a rotatable arm that can be moved to increase coverage area. The arm would record at several positions to increase coverage within a single run, each position and pixel pair would have a separate neutron count associated. 

At PSI: the monitor needs to be kept with the data. At our place the different parts may be collected with different statistics and people get excited about how the different contributions get merged. That merging is definitely a separate algorithm. Here need to merge the data, and applying correct error processing.

###Use Case 2, Triple Axis Spectrometry###
Similar to use case 1 with additional degrees of motion.  Many of the TAS machines output in Qx,Qy,Qz in the output file. 

At PSI: TAS stores Qx,Qy,Qz, EN. But normally the angle values for the various motors A1-A6 are stored too in order to be able to recalculate QE. Which raises the question how to find the axis to plot the data against. In terms of data processing: TAS use case and many others: We take the data, choose an axis, and fit something against it. Mostly a number of gaussians.

At ILL: Several elements of the instrument geometry/configuration and the sample orientation are varied to create scan points. Data from multiple scan points are stored in a single file. The data is recorded in physical, reciprocal space (Q,w) so no transformations from detector space and e.g. time-of-flight need to be performed. MJ would like to:

1.	Load such data into a workspace
2.	Perform simple manipulations of such data

###Use Case 3, scan against a detector###
PSI examples:
- BOA regularly scans against a CCD camera (2D) for neutron optics and imaging. Neutron imaging is basically a rotation scan against a 2D detector
- At TRICS we sometimes scan single crystal reflections against a 2D detector. In fact there are a number of such instruments at ILL too
- RITA-2 in energy analyzing mode is a multi analyser TAS which regularly scans against a 2D detector. The data reduction is summing the windows corresponding to the different analyser plates

###Use case 4, ISIS Reflectometry####
**A**. Stop/start experiment. Instrument moves, data collected, instrument moves, data collected etc., where each data collection is stored as a ‘period’ in the data file stored to disk. When this data file is loaded the entire content is loaded into a group workspace containing a matrixworkspace for each period in the file. TC would like to be able to merge the information from all these periods into one workspace.

**B**. Components of instruments are moving during data collection. Logs are recorded to the same level of time binning as the level time binning (DAE) of neutron detection, regardless of whether this is histogram or event data. It is assumed that the instrument components are moving slow enough that neutron collected at a given value, time bin value, can all be assumed to have been recorded where the instrument was at the recorded position. In the post analysis of such data TC wants to either:

1. Be able to know where components were for each recorded neutron event or counts in histogram bin
2. Or where you don’t care about as such detail, rebin the data, and then for each rebinned bin be able to say what are the average position values of the moving components

###Use case 5, MLZ, DNS instrument###
Diffuse scattering neutron TOF spectrometer with polarization analysis at MLZ called DNS.
Currently operate in none-TOF mode, but work is in process to operate this instrument in TOF mode also. In none TOF mode the data are recorded as neutron counts per pixel per run. 

**A**. Start/stop experiments: Instrument moves, data collected, run saved to file, instrument moves, data collected, run saved to file and so on.
MG would like to:

1. Be able to merge the information from different runs into one workspace. Information required for the normalization (monitor counts, duration of the run or proton charge) must not get lost. Sometimes, due to the technical reasons, DNS is operated without monitor. In these cases duration of the run is used for normalization.
2. Have a algorithm in Mantid for combining information from different workspaces into a single workspace where none of the instrument and normalisation information is lost
 
**B**. Components of instruments are moving during data collection (For future event experiments). Initially the log records for detector positions etc will likely be written out with time interval larger than the DAE (Data Acquisition Electronics) time binning for the recorded bins. MG would like:

1. Load these event data into one workspace. Then be able to bin this event workspace to e.g. the time binning of the log records ending up with a workspace equivalent to that in item 2 above
  
###Use case 6, ILL, D2b, D4 and D7 instruments###
This use case may be consider a detailed example of use case 1, in particular for D2b.

**Description of: D2b, high resolution powder diffractometer**. This instrument does not operate in TOF (time-of-flight) mode. Detector and monitor data are stored as neutron counts per pixel per scan point. There is one monitor count per scan point. On D2b a scan point is defined by a 2theta value. More specifically it has 128, position-sensitive tubes and typically (always!) a 25 point scan is produced to cover the gap between neighbouring tubes. The scan in one data file therefore produces a continuous diffraction pattern from 2theta_min to 2theta_max, without any overlap of detector tube positions. Each detector tube has a known efficiency (calibration data is used to generate a calibration file which is read at the same time as the data) and normalisation with respect to the incident beam is performed when the scan points are combined to produce a single workspace. The resulting workspace (in our data treatment software - LAMP) has axes '2theta' and 'height' (since the vertical tubes are position-sensitive) and is therefore independent of detector id and efficiency and the normalisation that has already been performed. Integration over detector height (Debye Scherrer cones) is performed based on '2theta', 'height' and 'sample-detector distance'.
The data from multiple scan points are stored in one file.

**Description of: D4, a liquids diffractometer**. Operates like D2b, except that it has much more flexible scanning practices and the detector does not have vertical resolution. 

**Description of: D7, similar to DNS at FRM2**. Compared to D2b and D4 this instrument uses fewer scan points, and data from each scan point is stored in separate files.

#####MJ would like to:#####
1. Be able to merge data from different scan points into one workspace where information about normalisation and instrument geometry is not lost. This is both in the process of loading data and to have a generic algorithm in Mantid for merging information in workspaces already loaded into Mantid
2. Be able to use algorithm to correct data in a workspace generated from item 1
3. Be able to transform the unit of a workspace generated from item 1 into Q-space. Once transformed into Q-space knowledge of the instrument is no longer needed

###Grouping of the use cases collected###
For example use cases 1 and 6, and use cases 4b and 5b may be considered to fall within the same category. 

##Other comments provided to this proposal##

MK: One general problem is that anything can be scanned against anything. And each scan needs to be treated differently. 
The UI for anything scan related will need a control to step from scan point to scan point
In my view a scan gives rise to a multidimensional dataset nScanPoint versus dimensions of the detector. All the values logged or varied during a scan are alternative axes along the scan dimension. 

MK: on 2D detector scan: 
   * we wish to step through the data and look at each image individually
   * we might select a window on the data and sum the window for each scan point and continue to work with the resulting 1D dataset
  * we might want to process each image individually resulting in some data, not necessarily a scalar. Think about a SANS scan where each image would yield a I(q) spectrum
  * we might wish to look at the data from another angle then the scan axis, for example along x or y of the detector
  * The imaging guys may want to calculate a reconstruction

MG: One should distinguish between the instruments moving between the runs and instruments moving during the run.

Since the data loading algorithm may be instrument-specific, I suggest to separate the data loading algorithm and algorithm to combine or merge the workspaces. The latter algorithm should be generic and should combine/merge the existing 2D workspaces created by the data loading algorithm. For different use cases different combining/merging algorithms may be needed.

For the data analysis order of operations is important. Therefore, I suggest either to leave the normalization behind the 'combine workspaces' algorithm or make it optional. However, the information required for the normalization (monitor counts or proton charge) must not get lost during combining of the workspaces.

##Suggestions##

###Suggestion 1###

When a data file is loaded, a MatrixWorkspace is created, which stores an extended instrument which has been created from a base instrument during the loading of the data file, and ensuring that each spectrum in the created workspace is associated with a unique detector or monitor. An advantage of this approach is that all algorithms currently working with MatrixWorkspaces will also work for this workspace. The question of the handling of monitor data needs to be addressed. 

ND (more details of process for this):

1. The Base instrument description describes the physical instrument (with the movable components in one position, and tagged in some way as the movable component)
2. The input file will have details of the number of positions that were recorded and the angles or displacements of each.
3. On Loading the loading alg would start with the base instrument, but then make a unique copy of it (not storing this again in the IDS). 
4. The movable component would be moved to the first position.
5. Copies of the movable components would be made for  all subsequent positions, and moved to the correct place, new detector_id’s would be created (perhaps negative or beyond some range to avoid clashes).
The disadvantage of all the instrument geometries being visible at the same time in the instrument view is actually an advantage, especially if you are doing it to increase coverage.  The question of normalising the separate runs remains.
 
Changes Required:

1. Add the ability to clone an IComponent within an instrument.
2. Make it easy to assign new detector id’s to a component assembly
3. Write a loader that does this
4. Handle the normalisation question

ND: We discussed (during the 2015 workshop) that several of these steps could be combined into a sub algorithm called something like “Combine Workspaces”.  That would just do the job to combining two workspaces (or a workspace group) with possible differences in the instrument into one workspace, not by adding the counts, but by adding those portions of the instruments into a single combined instrument.
This would take steps 3-5 and change them to this

3. On loading the specific load algorithm would create a new workspace for each position, and use Combine Workspaces as a sub algorithm to merge them into a single workspace for output (optionally, don’t combine and just output as a workspace group).
4. Combine Workspaces would add the instrument components for each instrument into a single instrument (reassigning component names and detector id’s as appropriate), all data would be conjoined into the workspace (corrected for new detector ids).
5. Combine workspace would also include normalisation option, such  normalise to a monitor, or normalise by proton charge.

This approach would make Combine Workspaces a more generally useful algorithm for other usage examples

MK: I have a difficulty understanding this. Can an example be given? How does this work with a 2D detector?

MJ: seems good to me for the first use case listed above, using the two step process suggested by Nick of creating a 2D workspace for each detector position and then combining these into another 2D workspace, for which the instrument definition (including detector IDs) has been updated (internally, in memory?) – as stated this would allow the instrument view to show the whole, scanned detector array for the combined workspace. When generating the combined workspace, the incident flux (monitor) for each scan point needs to be taken into account, but this information can then be ‘dropped’ if necessary in the combined workspace – only an average monitor for the whole, scanned data set is then meaningful.

###Suggestion 2###

When a data file is loaded, a MD-workspace is created, where each data point is associated with an instrument geometry. Currently Mantid has limited support for MD-algorithms and no support for the visualisation of such workspaces in instrument view.

ND: Makes sense if little to no reduction is required, perhaps for use case 2, although the workflow for TAS needs to be investigated to evaluate this.

MK: Is more or less my favorite. See above. Lacking a context object, I would store the arrays of varied and logged values as properties of the WS. A way would need to be invented for the geometry processing bits of Mantid to find this stuff.

MG: may have certain benefits for the diffuse scattering spectrometers. It may make sense to create a MD-Workspace and then extract a particular axis/dimension into a matrix workspace if needed

MJ: using the MD workspace seems appropriate for the 2nd use case – complex scanning instruments. Andrei and colleagues at SNS appear to have used this to treat ‘simple scanning instruments’ (use case 1 above), in particular their powder diffractometer may be like D2b or D4

Related to this document is a design proposal to expose MDEvents to Python, see [Python Algorithms For MDEvents](https://github.com/mantidproject/documents/blob/master/Design/pythonAlgorithmsForMDEvents.rst).

###Suggestion 3###

Currently a workspace can be split into smaller workspaces, where each of these workspaces only contains data from one instrument geometry. An expert mantid user can do this from a Python script by splitting data into new workspaces where for each of these workspaces the position of moveable components have been set according to values in log entries. 

This suggestion is mentioned since this may be all that is needed in some cases, but perhaps with convenience for doing this.

###Suggestion 4###

Extend how Mantid can query the position of a component, where a log entry contains information about a component as a function of time.  

Have a workspace, which automatically make use of time series log information without the user needing to know the names of log entries or the user needing to split the workspace. 

A very high level implementation is

1. In IDF specify which log time-series entry contains information about which component
2. Extend how instrument parameters are used, to be able to ask not only where a component is positioned but where it is at a given time
3. Have this information automatically used when users and algorithms ask for where a component is at a given time

One implementation challenge, for this suggestion, is how to apply the Plus algorithm on workspaces of this type, meaning how to combine log information for components into merged log entries in a summed workspace. Not providing a solution for this may be OK, but then this need to be made transparent to users and automatically detectable by algorithms.


