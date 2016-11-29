# Scanning Instruments for the ILL

## Introduction

Some details on requirements for the ILL were originally provided in a document from [development workshop discussions in 2015](https://github.com/mantidproject/documents/blob/master/Design/HandlingMovingInstruments.md).

The three instruments concerned with this work at ILL are D2B, D4 and D7. D16 also potentially has a similar mode to D4, and the TAS instruments should be kept in mind, although not in the scope of this work.

**Note:** These are some initial notes on the ILL instrument requirements. Further clarification is still required.

### D2B

[D2B](https://www.ill.eu/instruments-support/instruments-groups/instruments/d2b/) is a high-resolution two-axis diffractometer.

D2B is the most straightforward case. D2B is a high-resolution two-axis diffractometer with 64 detectors, each with 256 pixels (= 16384 spectra). A complete diffraction pattern is obtained by 100 steps of 0.025&deg; as the detectors are spaced at 2.5&deg; intervals. One numor contains data from 25 detector positions. The base position is given as the angle x 1000.

For example one file might contain the angles:

147.496
147.548
...
148.647
148.699

The detectors operate in continuous mode, so each NeXus file just contains counts for each detector.

The file format used by D2B is [described here](https://www.ill.eu/instruments-support/computing-for-science/data-analysis/raw-data/). Currently only ASCII files are produced, but NeXus files should be produced in the future, and before any loaders are written.

### D7

[D7](https://www.ill.eu/?id=13310) is a diffuse scattering spectrometer.

D7 is the only instrument with NeXus files available, so will most likely be the first target for the scanning instrument work at the ILL. Each scan point is stored in a separate NeXus file, with ~10 files being typical for a run. Scanning is done to cover the gaps between detector banks (?). 

D7 has three banks of 44 detectors. Angular offsets are stored in the NeXus file for each bank. Each detector has an angular offset from the centre of the bank given in the NeXus file too, as they are not regularly spaced. These do not change with different runs.

As for D2B, D7 operatees in continuous mode.

### D4

[D4(c)](https://www.ill.eu/instruments-support/instruments-groups/instruments/d4/) is a disordered materials diffractometer.

D4 is similar to D2B, but has no vertical resolution. The scanning practices are more flexible.

The ASCII files do not appear to contain the angles. It needs to be established how these are stored.

### D16

[D16](https://www.ill.eu/instruments-support/instruments-groups/instruments/d16/) is a small momentum transfer diffractometer.

**To be confirmed:** need to obtain data for D16 to check requirements.

### Requirements

#### General

* Loading data results in a MatrixWorkspace
* There is a spectrum for every detector at every position
* Each spectrum has knowledge of its detector and the angle the detector was at
 * The detectors can be seen in their duplicated positions in the instrument view
* Merging or summing runs with different detector positions is possible, while still keeping the correct instrument view

#### D2B

* Angles are read from the ASCII file (or NeXus file if available)
* 100 steps can be supported
 * 100 steps x 64 detectors x 256 pixels = 1,638,400 spectra

#### D7

* Read angle for each numor from NeXus file 
* Merge ~10 files, each with 44 detectors

#### D4

* Can handle 'flexible' scanning practices

### Outstanding Questions

* What normalisation is required for the different merged runs?
 * Time or monitor counts?
 * Any use for not normalising straight away - how to keep appropriate meta-data for later normalsiations?
* Overlaps between detector positions expected for D2B (see `LoadILLASCII` description below)
 * For D2B the discussion document indicates no overlap, but is this true with the full detector geometry?
* How would masking bad detectors work, for all pixels or changing based on detector positions?

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



