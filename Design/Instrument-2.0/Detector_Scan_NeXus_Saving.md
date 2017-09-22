Detector Scan NeXus Saving
==========================

## Background

Workspaces in Mantid can now support detector scans, but these can not currently be saved in the Mantid NeXus Processed format. In related work the ESS are looking at saving a new style instrument definition in their raw files, to be read, and eventually saved by Mantid. The new style instrument should be able to save the scan information within itself.

For now something similar could be stored separately in the Mantid NeXus processed files, that will be moved when the NeXus instrument definition is available. However, this would create legacy files for a short period, which would be best avoided.

## Technical Requirements

### Detector Scan Types

Two types of scan are now supported, normal scans where every detector can scan independently (asynchronously), and sync scans where every detector has the same set of scan intervals. Only synchronous scans are currently used within Mantid, for D20 and D2B at the ILL.

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
  * Asynchronous scan - an independent set of scan intervals for every detector

#### SpectrumInfo

 * `SpectrumInfo` also contains a vector of `SpectrumDefinition` objects, which contain a pair consisting of the detector index and time index
 * In non-scanning cases the time index is always 0

**Note** `DetectorInfo` also has a vector for storing monitor flags. This has no time dependence so would be read from the instrument as for a non-scanning workspace.

## Current Implementation

Spectra to detector mapping is stored in `mantid_workspace_1/instrument/detector`. There are five fields, `spectra` which provides the spectrum numbers, `detector_count` which provides the number of detectors for each spectra, `detector_list` which provides a list of all the detectors, `detector_index`, which gives the entry point into `detector_list` for a given spectra and `detector_positions` which, for unknown reasons, gives the R, &theta; and &phi; coordinates of every detector.

The 'true' source for the detector positions and rotations is in `mantid_workspace_1/instrument/instrument_parameter_map/data`. They are only stored here if they differ from the base instrument.

## Implementation Ideas

### New NeXus Instrument Format

_Based on discussion with Matt Jones_

Work has been done for the ESS for a new instrument format in the NeXus files. The approach in the new format, effectively a replacement for the old XML IDF, contains detectors (components in Mantid terminology) with pixels, for example a detector tube or bank with sub-pixels.

See the example for the NeXus hierarchy below. For a component with pixels in 3-dimensions the detector numbers are given, and then the offsets are given in x, y and z. Not all of the offsets are required, for example a tube might only require the `y_pixel_offset` entry.

```
raw_data_1
├───instrument
│   ├───detector_1
│   │   ├───detector_number (size is number of detectors)
│   │   ├───x_pixel_offset (size is number of detectors)
│   │   ├───y_pixel_offset (size is number of detectors)
│   │   ├───z_pixel_offset (size is number of detectors)
│   │   ├───...
│   ├───detector_2
│   ├───...
├───sample
```

The suggested method for dealing with detector scans is to add entries as `NXtransformations` to the detector entry. This is shown in the example hierarchy below. For each position and rotation axis a separate entry is required within the detector, such as `position_scan_x`, `position_scan_y`, `position_scan_z`, `rotation_scan_x`, `rotation_scan_y` and `rotation_scan_z`.

```
raw_data_1
├───instrument
│   ├───detector_1
│   │   ├───detector_number
│   │   ├───x_pixel_offset
│   │   ├───y_pixel_offset
│   │   ├───z_pixel_offset
│   │   ├───transformations (NXtransformations class)
│   │   │   ├───position_scan_x (attribute 'vector' for transformation, e.g. (1., 0., 0.))
│   │   │       ├───time (contains the time for each entry in value)
│   │   │       ├───value (single number per time entry, describing the distance along 'vector')
│   │   │   ├───position_scan_...
│   ├───detector_2
│   ├───...
├───sample
```

An open question here, especially when considering conversion from the old IDFs, is how to define the components that would be written as a NeXus detector. Technically this could be anything from the whole instrument to individual pixels, but logically it should be something like a tube. The only requirement is that a detector has pixels with a fixed offset at all times.

#### Differences Between NeXus and Mantid Approach

In the `DetectorInfo` representation in Mantid each position, rotation and mask flag of each pixel at each time index is stored separately. The scans are done on a pixel-by-pixel basis, and the components can not currently do any scanning. Different pixels are allowed to be given different scan intervals even within a component.

The NeXus instrument proposal would not support scanning at the pixel level. The offset entries would be the same for each time index, with the position entries giving the scan for a component. In other words you cannot scale a bank via a scan - the pixel gap is constant in time. Scanning something like a monitor would still be possible, but if this is done for all pixels there would be a large overhead in the NeXus file with the above proposal.

In the case of writing raw NeXus files from the instrument it is likely you would only need a subset of the offset, position scan and rotation entries based on physical knowledge of the instrument. After processing with Mantid this might not be so easy to achieve, as detectors can be moved around in an arbitrary way, e.g. for calibration.

The NeXus proposal for scanning allows the start and end positions and rotations to be different for a scan interval. Logically you might then interpolate between the start and end values for something that is continuously moving. This is not supported in Mantid, during a scan interval the detector is stationary.

### Component Scanning

_Based on discussion with Simon Heybrock._

To resolve the differences between the NeXus proposal and Mantid one option is to allow components to scan. This is similar to how `RectangularDetector` works. The changes required would be:

* Add the scan interface in `DetectorInfo` to `ComponentInfo`
  * E.g. in addition to `ComponentInfo::setPosition(detIndex)` we have `ComponentInfo::setPosition({detIndex, timeIndex})`
  * A `ComponentInfo::setPosition()` call updates all of the child positions (same for rotations)
* For setting positions, rotations or mask that can change with the time index, both `ComponentInfo` and `DetectorInfo` will require a check to see if the parent is scanning
  * If the parent is scanning it should throw
* The in memory representation is the same as before - the absolute position and rotation of all pixels are stored

The performance impact of this is that every call to `DetectorInfo::setPosition()` and similar will have an extra branch, even for non-scanning workspaces.

An alternative approach is to have something similar to `RectangularDetectors`. Here instead of storing the scan positions for each detector we would just store the position for the parent. Positions would need to computed on the fly to get the actual position for each detector. This would have the advantage of reducing memory use*, at the cost of more CPU work. This would be a step away from some of the Instrument 2.0 design principles.

*Note that the memory overhead due to scanning is not the main issue for the ILL instruments, addressing the overhead from using histograms with a  single count (no ToF) is a higher priority.

#### Outstanding Question

* If components scan, are pixels within that component still allowed to scan independently?
  * Possible use cases for this would be tubes that might change in time, for example temperature, during a scan. The calibration might then be time dependent.
  * If the answer to this is that we do need per-pixel scans then how can we support this in the NeXus file? A different proposal may be required.
  * Do we then need a mechanism in Mantid to define which components can scan, and which can not?

This is the key question to answer - if we restrict the scans in this way we should be able to use the NeXus Instrument proposal as it stands. If we do not impose this restriction we will likely need something to allow the values in `x_pixel_offset` and similar to be set per time interval.

## Early Implementation of Scan Saving

_Plan to be added..._


