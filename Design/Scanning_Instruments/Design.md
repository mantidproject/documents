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

#### D7

### Proposed solution

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
</parameter>```

<img src="D2B_Single_Angle.png" alt="D2B Single Angle" style="width: 800px;"/>

<center> A single angle in a MatrixWorkspace using `LoadILLASCII` </center>

<img src="D2B_VATES.png" alt="D2B VATES" style="width: 800px;"/>

<center> 25 angles from one file in VATES (merge to an MDWorkspace) </center>

### SNS StepScan

[SNS StepScan](http://docs.mantidproject.org/nightly/algorithms/StepScan-v1.html)

### DNS MergeRuns

[DNSMergeRuns](https://github.com/mantidproject/mantid/blob/e5d13b3ea533aab6a33ea65c281a20719ee5e6d1/Framework/PythonInterface/plugins/algorithms/DNSMergeRuns.py) - DNS is a neutron time-of-flight spectometer with movable detectors.

`DNSMergeRuns` allows merging multiple data files with the detectors at different positions. Here one data file corresponds to one detector positions. The algorithm takes a number of files, and converts to either 2theta, |Q| or d-Spacing.



