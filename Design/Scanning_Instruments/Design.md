# Scanning Instruments for the ILL

## Introduction

Some details on requirements for the ILL were originally provided in a document from [development workshop discussions in 2015](https://github.com/mantidproject/documents/blob/master/Design/HandlingMovingInstruments.md).

The three instruments concerned with this work at ILL are D2B, D4 and D7. D16 also potentially has a similar mode to D4, and the TAS instruments should be kept in mind, although not in the scope of this work.

### D2B

D2B is the most straightforward case. D2B is a high-resolution two-axis diffractometer with 64 detectors, each with 256 pixels (= 16384 spectra). A complete diffraction pattern is obtained by 100 steps of 0.025&deg; as the detectors are spaced at 2.5&deg; intervals. One numor contains data from 25 detector positions. The base position is given as the angle x 1000.

For example 

147.496
147.548
...
148.647
148.699

The file format used by D2B is [described here](https://www.ill.eu/instruments-support/computing-for-science/data-analysis/raw-data/).

### Requirements

#### General

* Loading data results in a MatrixWorkspace
* There is a spectrum for every detector at every position
* Each spectrum has knowledge of its detector and the angle the detector was at
 * The detectors can be seen in their duplicated positions in the instrument view
* Merging or summing runs with different detector positions is possible, while still keeping the correct instrument view

#### D2B

* Angles are read from the ASCII file
* 100 steps can be supported
 * 100 steps x 64 detectors x 256 pixels = 1,638,400 spectra

#### D4

> Operates like D2B, except that it has much more flexible scanning practices and the detector does not have vertical resolution.

#### D7

> Compared to D2B and D4 this instrument uses fewer scan points, and data from each scan point is stored in separate files.

### Outstanding Questions

* What normalisation is required for the different merged runs?
 * Time or monitor counts?
 * Any use for not normalising straight away - how to keep appropriate meta-data for later normalsiations?
* Overlaps between detector positions expected for D2B (see `LoadILLASCII` description below)
 * For D2B the discussion document indicates no overlap, but is this true with the full detector geometry?
* How would masking bad detectors work, for all pixels or changing based on detector positions?

### Solution Ideas - Loading

#### Conjoin

1. Load each workspace and merge workspaces with different spectrum number ranges

This might be less helpful on instruments with flexible scanning practices - spectrum number would not have any meaning.

##### Merge Workspaces

1. Load each angle into a separate workspace
1. Call a merge algorithm (either one by one or on entire loaded workspace)

### Solution Ideas - Workspace Form

#### Instrument Clone

1. Base instruments with detectors in home positions, tagged as movable
1. Number of positions and angle of displacement recorded in NeXus file
1. Make unique copy of each detector bas instrument in memory
 1. Clone each component with unique detector IDs (negative IDs?)
 1. Cloned detectors need to map back to original detector
1. Assign spectra to appropriate detector

#### Angle Map

1. Base instruments with detectors in home positions, tagged as movable
1. Number of positions and angle of displacement recorded in NeXus file
1. Each spectrum has the associated detector as normal, but also a knowledge of which position the detector was at
 1. This could be a TableWorkspace, which records angle, and information required for normalisation, and sample log information or a new workspace type

For this what changes could be required to support getting the detector positions in Mantid? For example for the instrument view and the S(Q,&omega;) conversion.

**Notes**

* Overlapping detectors should only be a problem in the instrument view.
* For D2B taking into account 100 steps ~1 million detectors, which takes about 400 MB of memory (probably OK, but not optimal)
* Look at ray tracing - any issues with overlapping detectors?

## Notes on other solutions

### LoadILLASCII

[LoadILLASCII](http://docs.mantidproject.org/nightly/algorithms/LoadILLAscii-v1.html)

Usage example:

```python
Load(Filename='/home/cs/bush/Mantid/data/Scanning_Instruments/exp_5-31-2497/rawdata/526105', OutputWorkspace='526105')
BinMD(InputWorkspace='526105', AlignedDim0='x,0,1.99989,100', AlignedDim1='y,-0.15,0.15,100', AlignedDim2='z,-1.93185,1.99239,100', OutputWorkspace='ws')
```

`LoadILLASCII` loads data from an ILL ASCII file into 25 workspaces (as there are 25 angles per file), with the instrument set with the correct rotation angle. This is done by setting an extra rotation in the 

```xml
<parameter name="t-position">
   <logfile id="rotangle"  eq="0.0+value"/>
</parameter>
```

<img src="D2B_Single_Angle.png" alt="D2B Single Angle" style="width: 800px;"/>

<center> A single angle in a MatrixWorkspace using `LoadILLASCII` </center>

<img src="D2B_VATES.png" alt="D2B VATES" style="width: 800px;"/>

<center> 25 angles from one file in VATES (merge to an MDWorkspace) </center>


### SNS StepScan

[SNS StepScan](http://docs.mantidproject.org/nightly/algorithms/StepScan-v1.html)

### DNS MergeRuns

[DNSMergeRuns](https://github.com/mantidproject/mantid/blob/e5d13b3ea533aab6a33ea65c281a20719ee5e6d1/Framework/PythonInterface/plugins/algorithms/DNSMergeRuns.py) - DNS is a neutron time-of-flight spectometer with movable detectors.

`DNSMergeRuns` allows merging multiple data files with the detectors at different positions. Here one data file corresponds to one detector positions. The algorithm takes a number of files, and converts to either 2theta, |Q| or d-Spacing.



