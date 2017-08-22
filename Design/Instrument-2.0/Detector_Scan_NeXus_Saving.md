Detector Scan NeXus Saving
==========================

## Background

Workspaces in Mantid can now support detector scans, but these can not currently be saved in the Mantid NeXus Processed format. In related work the ESS are looking at saving a new style instrument definition in their raw files, to be read, and eventually saved by Mantid. The new style instrument should be able to save the scan information within itself, but for now something similar could be stored separately in the Mantid NeXus processed files, that will be moved when the NeXus instrument definition is available.

## Technical Requirements

### Detector Scan Types

Two types of scan are now supported, normal scans where every detector can scan independently (asynchronously), and sync scans where every detector has the same set of scan intervals. Only synchronous scans are currently used within Mantid.

### Information to be saved in Mantid Nexus Processed

#### DetectorInfo

* The position of each detector for each scan interval
  * Stored in `DetectorInfo` as a 3-vector containing the absolute position
* The rotation of each detector at each scan interval
  * Stored in `DetectorInfo` as a quaternion containing the absolute rotation
* The mask flag for each detector for each scan interval
* For each detector position & rotation a mapping to the detector and scan interval that it refers to
  * The detector ID for each entry
  * The time index for each entry
* Scan intervals - a set of start and end times need to be stored:
  * Synchronous scan - a single set of scan intervals for every point in the detector scan
  * Asynchronous scan - **not necessarily required for now** - an independent set of scan intervals for every detector

#### SpectrumInfo

 * `SpectrumInfo` also contains a vector of `SpectrumDefinition` objects, which contain a pair consisting of the detector index and time index
 * In non-scanning cases the time index is always 0

### Notes

`DetectorInfo` also has a vector for storing monitor flags. This has no time dependence so would be read from the instrument as for a non-scanning workspace.

## Current Implementation

Spectra to detector mapping is stored in `mantid_workspace_1/instrument/detector`. There are five fields, `spectra` which provides the spectrum numbers, `detector_count` which provides the number of detectors for each spectra, `detector_list` which provides a list of all the detectors, `detector_index`, which gives the entry point into `detector_list` for a given spectra and `detector_positions` which, for unknown reasons, gives the R, &theta; and &phi; coordinates of every detector.

The 'true' source for the detector positions and rotations is in `mantid_workspace_1/instrument/instrument_parameter_map/data`. They are only stored here if they differ from the base instrument.


## Implementation Plans

TBC

