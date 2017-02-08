## Scanning Instrument Support for the ILL

### Background

#### Instrument 2.0

The full discussion on Instrument 2.0 is beyond the scope of this document, more details are contained in this [requirements document](requirements-v2.md). A short summary on [scanning instrument requirements is given](requirements-v2.md#moving-instruments-requirements) within this document. See also [notes](https://github.com/DMSC-Instrument-Data/documents/blob/master/meeting_notes/January_2017/scanning.md) from the meeting between Simon, Owen and Ian in January 2017

For the purposes of the discussion here scanning instruments (or moving instruments) describe instruments that have detectors that can be in different positions during a single run. This forms a step scan. This is often used to cover data collection where there are gaps between detectors. The aim of this work is to be able to deal with such detectors that move during a run, and be able to accumulate the data into a single workspace with the detectors at different positions throughout the run. This does not include two other use cases from the Instrument 2.0 requirements document; continuous scans and triple axis spectrometers.

#### ILL Requirements

The ILL have a requirement to implement support for moving instruments by the end of April 2017, in order to work with some of the diffractometers in use there. It is planned to implement the Instrument 2.0 support for moving instruments early in Mantid, to support the work at the ILL in a way that will not need to change with the full implementation of instrument 2.0. This document aims to describe the necessary steps to implement the Instrument 2.0 parts required. Some more information on ILL's requirements is given in [this document](ScanningInstruments_ILL.md).

#### Overview of Proposed Implementation

Two classes related to this have already been partially implemented in Mantid, [`SpectrumInfo`](https://github.com/mantidproject/mantid/pull/17394) and [`DetectorInfo`](https://github.com/mantidproject/mantid/pull/18318). These define the new way of working with commonly used information about a spectrum, namely `isMasked`, `isMonitor`, `l2`, `twoTheta`, `signedTwoTheta`, `position` and `rotation`. Eventually `DetectorInfo` will be responsible for the ownership of the parameters for the position and rotation, so for example moving a detector would have the new position stored in the `DetectorInfo` class, instead of the parameter map as is done currently. Values such as `l2` and `twoTheta` would use the new position when called and cache the return value, until another position change invalidates it.

Support for the moving instruments will be implemented via the `DetectorInfo` class. The usage of the `SpectrumInfo` class needs no direct knowledge of the time indexing. The methods on the `DetectorInfo` class for accessing detector information will be accessed by giving a detector index and an optional time index. It will also hold information on the start and end times for each time index. Any further information, for example to normalise to monitor counts, can then be held in a time series sample log.

Currently initialisation of workspaces is usually done in an incremental way. Exactly how this is done varies between loaders, but is often spectrum-by-spectrum. For example a common pattern for an instrument with PSD tubes would be as follows:

```cpp
for (size_t i = 0; i < numberOfTubes; ++i) {
  for (size_t j = 0; j < m_numberOfPixelsPerTube; ++j) {
    int *data_p = &data(static_cast<int>(i), static_cast<int>(j), 0);
    m_localWorkspace->setHistogram(spec, m_localWorkspace->binEdges(0),
        Counts(data_p, data_p + m_numberOfChannels));
    spec++;
  }
}
```

This will have performance impacts for the loader, but can also leave the workspace in an inconsistent state. For the scanning instrument design the workspace should be initialised all at once, see [StepScan construction](#stepscan-construction), which will ensure the loader creates a workspace in a consistent state. While the example above relates to the `Historgram` aspect of the workspace, this is analogous to the information that will be cached in `DetectorInfo`.

### Design

#### `DetectorInfo`

The core of the changes to support scanning instruments will be in the [`DetectorInfo`](https://github.com/mantidproject/mantid/blob/master/Framework/Beamline/inc/MantidBeamline/DetectorInfo.h) class. Currently the methods `isMonitor`, `isMasked`, `l2`, `twoTheta`, `signedTwoTheta`, `position`, `rotation`, `setPosition` and `setRotationEach` are accessed by a detector index.

The current plan is to access to add methods that take a detector index and an optional time index. Accessing a scanning instrument with just a detector index would throw an exception. This will save memory on detector metadata which would not change for different time indices, such as the monitor flag. See the [end of this document](#new-detectorinfo-signatures) for the changes to the signature of some of the public `DetectorInfo` methods.

`DetectorInfo` will ultimately store the information for positions and rotation, so will need to do this in a way that can be accessed by both the detector index and time index. Masking would be done at the spectrum level, if it is required for a detector for some time steps, but not all. `DetectorInfo` will also hold the start and end times for each step in the scan. The objects it would need, usually passed in to the constructor, would be:
* `const std::vector<std::vector<size_t>> &monitorIndices` (already implemented)
* `const std::vector<std::vector<Eigen::Vector3d>> &positions`
* `const std::vector<std::vector<Eigen::Vector3d>> &rotations`
* `const std::vector<std:pair<Kernel::DateAndTime, Kernel::DateAndTime>> &timeRanges`

Appropriate typedefs should be used here for readability. The first index for the outer vector for `positions` and `rotations` would be the time index, and the second index for the inner vector would be the detector index - e.g. `positions[time_index][detector_index]`. For the `timeRanges` vector this would be just a vector of time indexes - `timeRanges[time_index]`.

**Note:** that the `Eigen` library is planned to be used for the linear algebra routines. As `Kernel::V3D` and `Mantid::Kernel::Quat` are widely used in Mantid these will be wrapped, to go from the `Eigen` library to `Mantid::Kernel` where needed. These would be replaced with `Eigen::Vector3d` and `Eigen::Quaternion` respectively.

**Note:** `IComponent::getPos` will be overridden in `Detector` to use positions from `DetectorInfo` cached in `ParameterMap` if available. Throws if scanning (will fail for `InstrumentView` for now), since access only with detector index (no time index).

#### `SpectrumInfo`

Currently [`SpectrumInfo`](https://github.com/mantidproject/mantid/blob/master/Framework/API/inc/MantidAPI/SpectrumInfo.h) has a private `getDetector` method for finding the detector for the workspace. This uses the `getSpectrum(index)` method on `MatrixWorkspace` to return the detector IDs for the spectrum.

For the spectra the current access by detector IDs will be replaced with access by a `SpectrumDefinition` object, which holds a vector of size pairs - `std::vector<std::pair<size_t, size_t>>`. The first element in the pair corresponds to the detector index, and the second entry corresponds to the time index. This can be obtained by a call to `SpectrumInfo::spectrumDefinition`. `SpectrumDefinitions` will be set via `MatrixWorkspace::setIndexInfo`.

This can be used to access methods on `DetectorInfo`, for example `m_detectorInfo.twoTheta(detIndex, timeIndex)`. Because Mantid algorithms usually work with either spectra or detectors, but not both, this should not be commonly used.

#### `MatrixWorkspace` & `ISpectrum`/`Spectrum`

The original methods such as `this->detectorIDs.insert(detID)` should remain for now. This allows existing algorithms, e.g. loaders, that do not need time indexing to work as before. Similarly the `getDetectorIDs(index)` method would still return detector IDs without the time indexing information.

**Note:** working directly with the detector IDs is something that should be eliminated with the use of `SpectrumInfo` and `DetectorInfo`. The use of a `getDetectorIDs` should not be needed in the final Instrument 2.0. Similarly the method `getSpectrum(index)` on `MatrixWorkspace` should eventually be eliminated.

#### Moves

Currently moves were done by `ComponentHelper::moveComponent`. These will now go via the `DetectorInfo` layer, `DetectorInfo::setPosition(const IComponent &comp)`. This change is also included in the refactoring work.

#### StepScan Construction

There will be a new constructor which takes as an argument everything that is required for step scans. This would be the instrument, the parameter map, positions for each time index, rotations for each time index and the start and end times for each time index (as described under [`DetectorInfo`](#detectorinfo)).

It is important that the scan positions are created in a consistent state. These should be created with the aid of a class, which will return a `StepScanInfo` object that contains the positions, rotations and start and end times. This could follow the builder pattern for creating the `StepScanInfo` object. The loader will set the required values for position, rotation and time ranges and the `StepScanInfoBuilder` will ensure these are created in an internally consistent state. For example:
* A position, rotation and time range exist for every detector for each point in the scan
* The time ranges do not overlap
* The end times are always after the start times

The `StepScanInfo` object would have the following fields:
* `std::vector<std::vector<Kernel::V3D>> positions`
* `std::vector<std::vector<Kernel::V3D>> rotations`
* `std::vector<std:pair<Kernel::DateAndTime, Kernel::DateAndTime>> timeRanges`

As in the [`DetectorInfo`](#detectorinfo) class the first index for the outer vector for `positions` and `rotations` would be the time index, and the second index for the inner vector would be the detector index - e.g. `positions[time_index][detector_index]`. For the `timeRanges` vector this would be just a vector of time indexes - `timeRanges[time_index]`. All of the vector object would have the same size, the number of time steps for the time indexed vector and the number of detectors for the vector of positions.

The construction of `DetectorInfo` should be done in one call, and no more time indexes for the step scan should be allowed to be created after the construction of `DetectorInfo`. Care should be taken to move the vectors in `StepScanInfo`, to avoid copying them.

The only exception to this will be when using live data, where workspaces are built up in parts. In this case `DetectorInfo` should have a method to merge another `DetectorInfo` object, and deal correctly with the shifting the time indices. Both `DetectorInfo` objects will be in a valid state, but there would still need to be checks to ensure the time indices do not overlap between the two `DetectorInfo` objects.

The construction of `SpectrumInfo` should be done in a similar way. This needs to take a vector of `SpectrumDefinition` objects for step scans. The `StepScanInfo` could also have a method to return such an object, also ensuring it is in a consistent state with valid detector IDs and time indices. This would create an extra field in `StepScanInfo`:
* `std::vector<SpectrumDefinition>`

`ExperimentInfo::setInstrument(...)` will have an optional argument to pass `Beamline::DetectorInfo`. This would be used to set a `DetectorInfo` with scan information.

### Instrument Access

Algorithms should always get the geometry information via the `DetectorInfo`/`SpectrumInfo` class as opposed to the static instrument. There will not be any runtime checking performed to prevent this, but eventually the API will make it hard to get the geometry from the instrument itself without going through the new layers.

### Saving

The information relating to step scans needs loading and saving in the `LoadNexusProcessed` and `SaveNexusProcessed` algorithms. Currently the detector information is saved in the `instrument` NeXus group. Within the `detector` entry in `instrument` information about the location of the detectors is saved, with any moves to the base instrument applied. 

The base instrument definition from the XML file is saved in `instrument_xml`. The parameter map is also saved in its entirety in the `instrument_parameters` entry.

As the storage of this information is moved out from the parameter map and into `DetectorInfo` and `SpectrumInfo` within Mantid it should also be stored within a corresponding NeXus entries `detector_info` and `spectrum_info`. In the case of a step scan `detector_info` should contain an appropriate flag that a step scan is being stored. In this case some of the entries will contain an extra dimension corresponding to the step scan. For example a list of detector positions would be of size `n_detectors` normally, or `n_detectors x n_steps` for a step scan.

### Implementation

For this design to be implemented the use of `SpectrumInfo` and `DetectorInfo` will need to be rolled out in Mantid. The rollout for [`SpectrumInfo`](https://github.com/mantidproject/mantid/issues/17743) is fairly far advanced, with most algorithms now updated.

### New DetectorInfo Signatures

Currently detector info public methods look like the following.

```cpp
DetectorInfo(boost::shared_ptr<const Geometry::Instrument> instrument,
           Geometry::ParameterMap *pmap = nullptr);

bool isMonitor(const size_t index) const;
bool isMasked(const size_t index) const;
double l2(const size_t index) const;
double twoTheta(const size_t index) const;
double signedTwoTheta(const size_t index) const;
Kernel::V3D position(const size_t index) const;
Kernel::Quat rotation(const size_t index) const;

void setPosition(const size_t index, const Kernel::V3D &position);
void setRotation(const size_t index, const Kernel::Quat &rotation);

void setPosition(const Geometry::IComponent &comp, const Kernel::V3D &pos);
void setRotation(const Geometry::IComponent &comp, const Kernel::Quat &rot);
```

The following methods will be given require a time index access, in addition to the detector index.

```cpp
DetectorInfo(boost::shared_ptr<const Geometry::Instrument> instrument,
           Geometry::ParameterMap *pmap = nullptr);

bool isMonitor(const size_t index) const;
bool isMasked(const size_t index) const;
double l2(const size_t index, const size_t timeIndex) const;
double twoTheta(const size_t index) const;
double twoTheta(std::pair<size_t, size_t>) const;
double signedTwoTheta(const size_t index) const;
double signedTwoTheta(std::pair<size_t, size_t>) const;
Kernel::V3D position(const size_t index) const;
Kernel::V3D position(std::pair<size_t, size_t>) const;
Kernel::Quat rotation(const size_t index) const;
Kernel::Quat rotation(std::pair<size_t, size_t>) const;

void setPosition(const size_t index, const Eigen::Vector3d &position);
void setPosition(std::pair<size_t, size_t> const Eigen::Vector3d &position);
void setRotation(const size_t index, const Eigen::Quaternion &rotation);
void setRotation(std::pair<size_t, size_t> const Eigen::Quaternion &rotation);
```

`isMonitor` and `isMasked` do not need to have moving instrument access. Monitors should not ever need to change. If a specific detector position needs to be masked that should be done by masking the spectrum.

The routines without time indexing should always throw if they are attempted to be used on a non-moving instrument.

It would also be nice to have the following methods, to move banks and tubes, but component positions would not be stored in `DetectorInfo`, so this will not be implemented for now. Eventually there will also be a `ComponentInfo`, that follows similar lines to the `DetectorInfo` object.

```cpp
void setPosition(const Geometry::IComponent &comp, const Kernel::V3D &pos, const size_t timeIndex = 0);
void setRotation(const Geometry::IComponent &comp, const Kernel::Quat &rot, const size_t timeIndex = 0);
```

